Name:           nautilus-open-any-terminal-git
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Nautilus extension adding a context menu entry for other terminal emulators
License:        GPL-3.0-or-later
URL:            https://github.com/Stunkymonkey/nautilus-open-any-terminal
Source0:        %{name}-%{version}.tar.gz

# pyproject.toml: requires-python = ">=3.9", dependencies = [].
# Modulnya hanya mengimpor gi (PyGObject) dari stdlib gettext, jadi tidak ada
# dependensi Python pihak ketiga yang perlu RuntimeRequires.
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# pyproject.toml build-system: setuptools_scm[toml]>=6.2
# Nama paket Fedora memakai underscore: python3-setuptools_scm, bukan
# python3-setuptools-scm.
# Versi diambil dari git. Karena tarball SRPM tidak punya .git, setuptools_scm
# harus diberi nilai eksplisit lewat env var di %build — kalau tidak, build
# berhenti dengan "LookupError: setuptools-scm was unable to detect version".
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-wheel

# setup.py InstallCommand memanggil msgfmt (bagian build_mo) —
# python3-setuptools calling subprocess.run(["msgfmt", ...]).
BuildRequires:  gettext

# Modul mengimpor gi (gi.repository.Nautilus / Gtk), jadi PyGObject wajib
# ada saat runtime — inilah satu-satunya dependensi runtime nyata. Paket
# RPM-nya "python3-gobject"; "python3-gi" hanya nama provide/alias yang
# diimpor modul, bukan paket terpisah.
Requires:       python3-gobject
# Extension-nya sendiri di-*load* oleh Nautilus lewat bridge python-nya.
Requires:       nautilus-python
# GSettings schema yang diinstal ke %{_datadir}/glib-2.0/schemas harus
# dikompilasi supaya ekstensi bisa membaca pengaturannya.
Requires:       glib2
Requires:       gettext-runtime

%global debug_package %{nil}

# RPM Version "20260916.git0e34f87a" bukan versi PEP 440 yang valid, jadi
# setuptools_scm melempar InvalidVersion. Untuk Python, ubah ".git" -> "+git"
# (local version identifier): 20260916+git0e34f87a.
%global pep440_version %(echo %{version} | sed 's/\.git/+git/')

%description
Nautilus extension that adds a "Open in Terminal" style context menu entry
which lets you pick a terminal emulator other than gnome-terminal. The
terminals it finds are discovered at runtime by inspecting the .desktop
entries on the system, so it works with whichever emulators are installed
rather than a hardcoded list. Preferences (which emulators to show, and
their order) are stored in a GSettings schema.

%{name} is a daily rolling build tracking the tip of upstream's master
branch. Upstream has released 0.8.3, but this spec follows the branch tip so
new emulators and fixes land without waiting on a tag. %{version} encodes
the commit date and short SHA, e.g. 20260928.gitabcdef1.

%prep
%autosetup -n %{name}-%{version}

%build
# setuptools_scm tidak bisa menemukan .git di dalam tarball SRPM, jadi
# versikan diteruskan lewat env var. Nilai "0.0.0" hanya perantara —
# versi RPM yang dipakai rpm adalah %{version} di header.
SETUPTOOLS_SCM_PRETEND_VERSION=%{pep440_version} \
  %py3_build

%install
SETUPTOOLS_SCM_PRETEND_VERSION=%{pep440_version} \
  %py3_install

# Skema GSettings TIDAK dikompilasi di %install, dan gschemas.compiled tidak
# ikut dikirim di %files. Alasannya: gschemas.compiled adalah file milik glib2
# yang dibangun ulang untuk SELURUH direktori, jadi mengklaim kepemilikannya
# di sini akan saling tabrak dengan trigger glib2 saat glib2 di-upgrade.
# Kompilasi yang benar dilakukan di %post, karena glib-compile-schemas
# membaca seluruh .gschema.xml di direktori itu. Lihat catatan panjang di
# %post kenapa harus %post dan tidak bisa andalkan file trigger.

# setup.py InstallCommand mendaftarkan modul ke BOTH
# share/nautilus-python/extensions dan share/caja-python/extensions
# (FILE_MANAGERS = ["nautilus", "caja"] di setup.py). Keduanya ikut
# terpasang di sini; caja-python sudah ada di repo Fedora, jadi tidak perlu
# dikunci sebagai Requires hanya karena file-nya ikut ter-install.

%post
# glib-compile-schemas di sini WAJIB, bukan sekadar formalitas.
#
# Image RakuOS ini tidak punya file trigger RPM sama sekali: direktori
# /usr/lib/rpm/file-triggers/ tidak ada, dan tidak ada paket pun yang
# memiliki file di dalamnya. glib2 sendiri tidak membawa trigger apa pun.
# Jadi asumsi "dibiarkan oleh file trigger glib2" tidak berlaku di sini.
#
# Gejalanya sudah terbukti nyata di sistem ini: berkas
# /usr/share/glib-2.0/schemas/gschemas.compiled bertanggal 26 Sep,
# sedangkan nautilus-50.3 terpasang 28 Sep. Karena tidak ada yang membangun
# ulang database itu, nautilus crash:
#
#   GLib-GIO-ERROR: Settings schema 'org.gnome.nautilus.preferences' is not
#   installed
#   zsh: IOT instruction (core dumped)  nautilus
#
# Skema di bawah akan mengalami hal yang sama persis — terpasang ke direktori
# tapi tidak pernah terbaca, sehingga preferensi ekstensi (terminal mana yang
# ditampilkan) selalu kembali ke default tanpa error yang terlihat.
#
# glib-compile-schemas dibangun ulang untuk SELURUH direktori, jadi ini juga
# memperbaiki semua schema lain yang tertinggal, bukan hanya milik paket ini.
glib-compile-schemas %{_datadir}/glib-2.0/schemas >/dev/null 2>&1 || :
update-desktop-database -q >/dev/null 2>&1 || :

%postun
# Sama seperti %post: rebuild ulang supaya skema paket ini hilang dari DB
# setelah di-uninstall, dan jangan sampai meninggalkan entri yang rusak.
glib-compile-schemas %{_datadir}/glib-2.0/schemas >/dev/null 2>&1 || :
update-desktop-database -q >/dev/null 2>&1 || :

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/nautilus_open_any_terminal/
%{python3_sitelib}/nautilus_open_any_terminal-*.egg-info/
%{_datadir}/nautilus-python/extensions/nautilus_open_any_terminal.py
%{_datadir}/caja-python/extensions/nautilus_open_any_terminal.py
%{_datadir}/glib-2.0/schemas/com.github.stunkymonkey.nautilus-open-any-terminal.gschema.xml
%{_datadir}/locale/*/LC_MESSAGES/nautilus-open-any-terminal.mo

%changelog
* Mon Sep 28 2026 Mindset Apps <mindset@example.com> - 20260928.git0000000-1
- Initial packaging of nautilus-open-any-terminal-git.
- SETUPTOOLS_SCM_PRETEND_VERSION set in %build/%install: SRPM tarballs carry
  no .git, so setuptools_scm cannot detect a version on its own.
- GSettings schema compiled in %install; upstream's setup.py only prints a
  hint and never runs glib-compile-schemas.
