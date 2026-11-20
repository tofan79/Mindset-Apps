# Omaview: image/video/audio viewer dari Omacom. Versi diambil dari tag rilis
# upstream (v0.1.1), sama seperti folio. CMake proyek ini sengaja tidak
# menuliskan versi, jadi %%{pkg_version} disuntik workflows saat membuat SRPM.
#
# Tidak ada akhiran -omacom di sini: Fedora tidak punya paket `omaview`, jadi
# nama hulu dipakai apa adanya. Path biner, desktop, ikon, dan lisensi juga
# sesuai install() di CMake / PKGBUILD omarchy-pkgs.

Name:           omaview
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Omarchy's picture viewer and media player
License:        MIT
URL:            https://github.com/omacom/omaview
Source0:        https://github.com/omacom/omaview/archive/v%{version}/omaview-%{version}.tar.gz
ExclusiveArch:  x86_64

%global debug_package %{nil}

BuildRequires:  cmake >= 3.21
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtmultimedia-devel

Requires:       qt6-qtbase
Requires:       qt6-qtdeclarative
Requires:       qt6-qtmultimedia
Requires:       qt6-qtsvg
Requires:       qt6-qtwayland
Requires:       qt6-qtimageformats
Requires:       wayland
Requires:       hicolor-icon-theme
Requires:       ffmpeg
Requires:       wl-clipboard
Requires:       xdg-desktop-portal

Recommends:     kimageformats
Recommends:     cups
Recommends:     wireplumber

%description
Omaview is Omarchy's picture viewer and media player. It opens a photo, a
video, a song, or a whole folder: arrow keys step through files, the wheel
zooms, Tab hides the controls, and Ctrl+M shows a folder as a grid with
silent film previews. Videos and music get a timeline, chapters, subtitles,
audio tracks, speed control and MPRIS. Pictures are decoded off the main
thread and videos through FFmpeg. It follows the desktop theme and language.

Built from the upstream release tag; no vendor binary is bundled.

%prep
%autosetup -n omaview-%{version}

%build
%cmake -G Ninja
# Bangun hanya aplikasi. CMake juga mendefinisikan omaview_tests, ui_tests dan
# cli_tests; semua butuh sesi desktop/offscreen yang tidak tersedia di mock.
%__cmake --build %{__cmake_builddir} --target omaview

%install
%cmake_install
desktop-file-validate %{buildroot}%{_datadir}/applications/omaview.desktop

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
%license %{_datadir}/licenses/omaview/LICENSE
%doc README.md
%{_bindir}/omaview
%{_datadir}/applications/omaview.desktop
%{_datadir}/icons/hicolor/scalable/apps/omaview.svg

%changelog
* Fri Nov 20 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial COPR package from upstream tag v%{version}.
- Build only the omaview target; UI/CLI tests need a desktop session.
- Follow upstream install paths: /usr/bin/omaview, desktop entry and icon.
