Name:           hyprpicker
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        A wlroots-compatible Wayland color picker

License:        BSD-3-Clause AND HPND-sell-variant
URL:            https://github.com/hyprwm/hyprpicker
Source0:        hyprpicker-%{version}.tar.gz

ExcludeArch:    %{ix86}

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(hyprutils) >= 0.2.0
BuildRequires:  pkgconfig(hyprwayland-scanner) >= 0.4.0
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)

Requires:       hyprutils
Recommends:     wl-clipboard

%description
A wlroots-compatible Wayland color picker for Hyprland and
other wlroots-based compositors. Supports picking colors from
anywhere on screen with zoom lens, live preview, and multiple
output formats.

%prep
%setup -q -n %{name}-%{version}

%build
%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

%files
%{_bindir}/hyprpicker
%{_mandir}/man1/hyprpicker.1*
%doc README.md
%license LICENSE

%changelog
* Thu May 14 2026 mindset <mindset@copr> - %{pkg_version}-1
- Auto-updated from upstream GitHub Releases
