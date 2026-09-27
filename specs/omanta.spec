Name:           omanta
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Native file manager for Omarchy (Qt Quick + GIO)

License:        MIT
URL:            https://github.com/28allday/omanta
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:   x86_64

BuildRequires:  cmake >= 3.28
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  glib2-devel
BuildRequires:  libarchive-devel
BuildRequires:  tinysparql-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtsvg-devel

# GIO is how the app reaches remote locations and the icon theme carries the
# shipped omanta.svg, so those two are hard requirements.
Requires:       gvfs
Requires:       hicolor-icon-theme

# Optional per-protocol backends, thumbnailers and the full-text search index.
# omanta degrades gracefully without them, so they stay recommended.
Recommends:     gvfs-smb
Recommends:     gvfs-mtp
Recommends:     gvfs-gphoto2
Recommends:     ffmpegthumbnailer
Recommends:     localsearch

%description
A native file manager built with Qt Quick and GIO. Supports archive browsing
and extraction, image and video thumbnails, batch renaming, clipboard history
and a full-text search client for the localsearch index, plus a set of
context-menu actions exposed as TOML files under %{_datadir}/omanta/actions.

%prep
%autosetup -n %{name}-%{version}

%build
# Pakai binary cmake langsung, bukan makro %cmake/%cmake_build, supaya spec
# tidak bergantung pada macros.cmake dari paket cmake. %make_build juga tidak
# dipakai: %make_build memanggil make tanpa -C, sedangkan generator Ninja
# hanya menghasilkan build.ninja dan tidak menulis Makefile sama sekali.
cmake -S . -B build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DOMANTA_BUILD_TESTS=OFF
cmake --build build -j%{_nproc_build}

%install
DESTDIR=%{buildroot} cmake --install build

%files
%license %{_datadir}/licenses/omanta/LICENSE
%{_bindir}/omanta
%{_bindir}/omanta-launch
%{_bindir}/omanta-launch-cwd
%{_bindir}/omanta-switch
%{_bindir}/omanta-dropbox-link
%{_datadir}/applications/omanta.desktop
%{_datadir}/icons/hicolor/scalable/apps/omanta.svg
%{_datadir}/omanta/actions/*.toml

%changelog
* Sun Sep 27 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR build from upstream release tag
