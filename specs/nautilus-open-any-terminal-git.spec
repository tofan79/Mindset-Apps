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

# Skema GSettings TIDAK dikompilasi/dikirim di sini: gschemas.compiled dimiliki
# glib2 dan dikompilasi ulang otomatis oleh file trigger glib2 di Fedora.

# setup.py InstallCommand mendaftarkan modul ke BOTH
# share/nautilus-python/extensions dan share/caja-python/extensions
# (FILE_MANAGERS = ["nautilus", "caja"] di setup.py). Keduanya ikut
# terpasang di sini; caja-python sudah ada di repo Fedora, jadi tidak perlu
# dikunci sebagai Requires hanya karena file-nya ikut ter-install.

%post
# Skema sudah dikompilasi di %install; post hanya me-refresh cache yang
# relevan. glib-compile-schemas tidak perlu diulang karena .gschema.Compiled
# sudah ikut terpasang sebagai bagian dari file list RPM.
update-desktop-database -q >/dev/null 2>&1 || :

%postun
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
