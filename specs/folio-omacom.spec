# Nama paket sengaja "folio-omacom", bukan "folio": Fedora sudah punya paket
# bernama folio (aplikasi catatan Markdown untuk GNOME, binernya
# /usr/bin/com.toolstack.Folio). Nama sendiri membuat `dnf install` tidak
# ambigu dan kedua paket bisa hidup berdampingan karena tidak ada file yang
# bertabrakan.
#
# Isi paket tetap persis seperti upstream: biner /usr/bin/folio,
# folio.desktop, ikon folio.svg, dan plugin di /usr/share/folio/plugins.
# Path /usr/share/folio itu di-hardcode di src/plugins.cpp, jadi tidak boleh
# ikut di-rename walaupun nama paketnya lain.

Name:           folio-omacom
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Omarchy's file manager: quiet, keyboard-first, theme-following
License:        MIT
URL:            https://github.com/omacom/folio
Source0:        https://github.com/omacom/folio/archive/v%{version}/folio-%{version}.tar.gz
ExclusiveArch:  x86_64

BuildRequires:  cmake >= 3.21
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  desktop-file-utils

Requires:       qt6-qtbase
Requires:       qt6-qtdeclarative
Requires:       qt6-qtwayland
Requires:       qt6-qtimageformats
Requires:       qt6-qtmultimedia
Requires:       qt6-qtsvg
Requires:       glib2%{?_isa}
Requires:       hicolor-icon-theme
Requires:       xdg-utils

# Tombol "Compress" memanggil bsdtar lewat QProcess, bukan menautkan
# libarchive, jadi yang dibutuhkan binernya (paket bsdtar), bukan -devel.
Requires:       bsdtar

# Semua di bawah opsional: aplikasi tetap jalan tanpanya, hanya fitur terkait
# yang mati (preview PDF, thumbnail video/PDF, browsing tailnet lewat SFTP,
# plugin Tailscale, berbagi LocalSend).
Recommends:     qt6-qtpdf
Recommends:     ffmpegthumbnailer
Recommends:     poppler-utils
Recommends:     gvfs
Recommends:     jq

%description
Files (folio) is Omarchy's file manager: one quiet window that follows the
desktop theme and language, works entirely from the keyboard, and never
crawls your home folder in the background.

It offers a grid with real previews, a list, and Finder-style columns; Space
previews images, video, audio, PDFs, text and Markdown in their own window;
the sidebar holds your home folders, pinned folders (shared with GTK file
dialogs), Recents, Trash, drives, and machines on your tailnet over SFTP.
Copy/paste works with other apps, nothing is overwritten, and the window can
be split in two. Plugins add sidebar sections, Share entries and views.

Built from the upstream release tag; no vendor binary is bundled.

%prep
%autosetup -n folio-%{version}

%build
%cmake -G Ninja
%cmake_build

%install
# Upstream tidak punya aturan install() di CMake, jadi pemasangan mengikuti
# package() di PKGBUILD omarchy-pkgs: biner, desktop, ikon, dokumen, lalu
# seluruh isi plugins/ dengan bit executable dipertahankan.
install -Dm755 %{_vpath_builddir}/folio %{buildroot}%{_bindir}/folio
install -Dm644 share/folio.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/folio.svg
install -Dm644 share/folio.desktop %{buildroot}%{_datadir}/applications/folio.desktop
install -Dm644 docs/plugins.md %{buildroot}%{_docdir}/%{name}/plugins.md

find plugins -type f | while read -r file; do
    if [ -x "$file" ]; then mode=755; else mode=644; fi
    install -Dm"$mode" "$file" "%{buildroot}%{_datadir}/folio/${file}"
done

desktop-file-validate %{buildroot}%{_datadir}/applications/folio.desktop

%post
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q %{_datadir}/applications || :
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -qt %{_datadir}/icons/hicolor || :
fi

%postun
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q %{_datadir}/applications || :
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -qt %{_datadir}/icons/hicolor || :
fi

%files
%license LICENSE
%doc README.md
%{_docdir}/%{name}/plugins.md
%{_bindir}/folio
%{_datadir}/applications/folio.desktop
%{_datadir}/icons/hicolor/scalable/apps/folio.svg
%{_datadir}/folio/

%changelog
* Fri Nov 13 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Paket awal folio-omacom dari tag upstream (CMake + Qt6/QML).
- Nama diberi akhiran -omacom karena Fedora sudah punya paket `folio`
  (aplikasi catatan GNOME); biner dan path datanya tetap milik upstream.
- Plugin bawaan (Tailscale, Dropbox, LocalSend) ikut dipasang di
  /usr/share/folio/plugins sesuai path yang di-hardcode upstream.
