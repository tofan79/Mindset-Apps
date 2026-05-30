%global pkg_version %{version}
%global scenefx_version 0.4.1

Name:           mangowm
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        mango — A Wayland compositor based on wlroots and scenefx

License:        MIT
URL:            https://github.com/mangowm/mango
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/mangowm-%{version}.tar.gz
Source1:        https://github.com/wlrfx/scenefx/archive/refs/tags/%{scenefx_version}.tar.gz#/scenefx-%{scenefx_version}.tar.gz

%global debug_package %{nil}

BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(wayland-server) >= 1.23.1
BuildRequires:  pkgconfig(wlroots-0.19) >= 0.19.0
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libinput) >= 1.27.1
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libcjson)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  wayland-protocols-devel
BuildRequires:  libglvnd-devel
BuildRequires:  libdrm-devel

Requires:       wayland-server >= 1.23.1
Requires:       wlroots0.19
Requires:       xkbcommon
Requires:       libinput >= 1.27.1
Requires:       libpcre2-8
Requires:       pixman-1
Requires:       libcjson

%description
mango is a Wayland compositor based on wlroots and scenefx,
built with a focus on eye-candy and user experience.

%prep
%autosetup -n mango-%{version} -a 1

%build
# Build bundled scenefx
pushd ../scenefx-%{scenefx_version}
%meson -Dexamples=false
%meson_build
%meson_install
popd

# Build mangowm against bundled scenefx
export PKG_CONFIG_PATH="%{buildroot}%{_libdir}/pkgconfig${PKG_CONFIG_PATH:+:${PKG_CONFIG_PATH}}"
%meson
%meson_build

%install
pushd ../scenefx-%{scenefx_version}
%meson_install
popd
%meson_install

%files
%{_bindir}/mango
%{_bindir}/mmsg
%{_datadir}/wayland-sessions/mango.desktop
%{_datadir}/xdg-desktop-portal/mango-portals.conf
%dir %{_sysconfdir}/mango
%config(noreplace) %{_sysconfdir}/mango/config.conf
%{_libdir}/libscenefx-0.4.so.*

%changelog
* Thu May 28 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package
