Name:           omacut
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Dead-simple video length trimmer built with Qt Quick and ffmpeg

License:        MIT
URL:            https://github.com/omacom/omacut
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:   x86_64

BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.21
BuildRequires:  ninja-build
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtmultimedia-devel

# omacut drives the ffmpeg CLI through QProcess rather than linking against
# libav*, so only the runtime tool is needed, not the development headers.
Requires:       ffmpeg-free
Requires:       xdg-desktop-portal
Requires:       hicolor-icon-theme

# rpm di Fedora 44 otomatis membuat subpaket debuginfo sekaligus debugsource.
# build/install sudah berhasil, tetapi debugsource tidak punya satu pun file
# sumber yang bisa dikumpulkan sehingga rpm berhenti dengan
# "Empty files file .../debugsourcefiles.list". Aplikasi pihak ketiga yang
# dibangun dari tarball tidak punya layout debugsource yang bisa dietakan, jadi
# kedua subpaket itu dimatikan altogether.
%global debug_package %{nil}

%description
A small video trimmer: open a clip, drag the handles on the timeline to set
the start and end points, and write out the trimmed result. Rendering is done
by the ffmpeg command line tool and the interface with Qt Quick.

%prep
%autosetup -n %{name}-%{version}

%build
# Sejak v0.8.0 upstream pindah dari qmake ke CMake; omacut.pro sudah tidak
# ada di tarball rilis. Bangun hanya target aplikasi: tes upstream memakai
# QDragEnterEvent(QPointF, ...) yang tidak lagi valid di Qt 6.11 (butuh
# QPoint), dan tes memang tidak ikut dipasang ke RPM. CMakeLists tidak punya
# install(), jadi biner tetap dipasang manual di %install.
%cmake -G Ninja
%__cmake --build %{__cmake_builddir} --target omacut

%install
install -Dpm0755 %{_vpath_builddir}/omacut %{buildroot}%{_bindir}/omacut
install -Dpm0644 pkgbuild/omacut.desktop %{buildroot}%{_datadir}/applications/omacut.desktop
install -Dpm0644 pkgbuild/omacut.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/omacut.svg
install -Dpm0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%files
%license %{_datadir}/licenses/%{name}/LICENSE
%{_bindir}/omacut
%{_datadir}/applications/omacut.desktop
%{_datadir}/icons/hicolor/scalable/apps/omacut.svg

%changelog
* Sun Sep 27 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR build from upstream release tag
