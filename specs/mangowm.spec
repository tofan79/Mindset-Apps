%global pkg_version %{version}

Name:           mangowm
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        mango — A Wayland compositor based on wlroots and scenefx

License:        MIT
URL:            https://github.com/mangowm/mango
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/mangowm-%{version}.tar.gz

%global debug_package %{nil}

BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(wayland-server) >= 1.23.1
BuildRequires:  pkgconfig(wlroots-0.19) >= 0.19.0
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libinput) >= 1.27.1
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(scenefx-0.4) >= 0.4.1
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libcjson)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  wayland-protocols-devel

Requires:       wayland-server >= 1.23.1
Requires:       wlroots0.19
Requires:       scenefx0.4
Requires:       xkbcommon
Requires:       libinput >= 1.27.1
Requires:       libpcre2-8
Requires:       pixman-1
Requires:       libcjson

%description
mango is a Wayland compositor based on wlroots and scenefx,
built with a focus on eye-candy and user experience.

%prep
%setup -q -n mango-%{version}

%build
%meson
%meson_build

%install
%meson_install

%files
%{_bindir}/mango
%{_bindir}/mmsg
%{_datadir}/wayland-sessions/mango.desktop
%{_datadir}/xdg-desktop-portal/mango-portals.conf
%dir %{_sysconfdir}/mango
%config(noreplace) %{_sysconfdir}/mango/config.conf

%changelog
* Thu May 28 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package