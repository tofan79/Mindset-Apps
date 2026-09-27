Name:           omacut
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Dead-simple video length trimmer built with Qt Quick and ffmpeg

License:        MIT
URL:            https://github.com/omacom/omacut
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:   x86_64

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtmultimedia-devel

# omacut drives the ffmpeg CLI through QProcess rather than linking against
# libav*, so only the runtime tool is needed, not the development headers.
Requires:       ffmpeg-free
Requires:       xdg-desktop-portal
Requires:       hicolor-icon-theme

%description
A small video trimmer: open a clip, drag the handles on the timeline to set
the start and end points, and write out the trimmed result. Rendering is done
by the ffmpeg command line tool and the interface with Qt Quick.

%prep
%autosetup -n %{name}-%{version}

%build
mkdir -p build
cd build
# Panggil qmake6 langsung; makro %qmake6 tidak ada di semua instalasi rpm-build.
qmake6 ../%{name}.pro
%make_build

%install
install -Dpm0755 omacut %{buildroot}%{_bindir}/omacut
install -Dpm0644 ../pkgbuild/omacut.desktop %{buildroot}%{_datadir}/applications/omacut.desktop
install -Dpm0644 ../pkgbuild/omacut.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/omacut.svg
install -Dpm0644 ../LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%files
%license %{_datadir}/licenses/%{name}/LICENSE
%{_bindir}/omacut
%{_datadir}/applications/omacut.desktop
%{_datadir}/icons/hicolor/scalable/apps/omacut.svg

%changelog
* Sun Sep 27 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR build from upstream release tag
