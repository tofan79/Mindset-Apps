Name:           gloview
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Minimal macOS-style window overview plugin for Hyprland
License:        GPL-3.0-or-later
URL:            https://github.com/fedsfarm/gloview
Source0:        gloview-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  hyprland-devel
BuildRequires:  lua-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  pkgconfig

Requires:       hyprland
Requires:       mesa-libGL
Requires:       lua-libs

%description
GloView is a macOS Mission Control-style window overview plugin for Hyprland.
Super+Tab toggles the overview, with a fully configurable keyboard layout and
styling via the plugin:gloview:* keys.

%prep
%setup -q -n gloview-main

%build
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j

%install
install -d %{buildroot}%{_libdir}
install -m 0755 build/gloview.so %{buildroot}%{_libdir}/gloview.so

%files
%{_libdir}/gloview.so

%changelog
* Thu Sep 17 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package from upstream source