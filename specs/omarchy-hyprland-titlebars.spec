# Plugin titlebar untuk mode floating Omarchy. Build dari tarball tag rilis
# upstream vX.Y.Z, mengikuti pola paket omacom lain di repo ini.
#
# Catatan penting: plugin Hyprland hanya bisa dimuat oleh build Hyprland yang
# PERSIS sama dengan header saat kompilasi. COPR ini menarik Hyprland 0.57.2
# dari repo tambahan lionheartp/Hyprland, jadi versi itu dikunci di Requires.
# Setiap kali Hyprland di_COPR_ naik versi, plugin ini harus dibangun ulang
# dan pin di bawah ikut diperbarui.
#
# CMake upstream memasang ke `lib/omarchy-hyprland-titlebars` (relatif prefix).
# Kami memaksa CMAKE_INSTALL_LIBDIR=lib secara eksplisit supaya tidak berubah
# jadi lib64 oleh makro CMake Fedora: Omarchy memuat path /usr/lib/... yang
# merupakan kontrak tetap.

Name:           omarchy-hyprland-titlebars
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Titlebars for Omarchy's floating workspaces
License:        BSD-3-Clause AND MIT
URL:            https://github.com/omacom/omarchy-hyprland-titlebars
Source0:        https://github.com/omacom/omarchy-hyprland-titlebars/archive/v%{version}/omarchy-hyprland-titlebars-%{version}.tar.gz
ExclusiveArch:  x86_64

%global debug_package %{nil}

BuildRequires:  cmake >= 3.27
BuildRequires:  gcc-c++
BuildRequires:  pkgconf-pkg-config
BuildRequires:  pkgconfig(hyprland)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(xkbcommon)

Requires:       hyprland = 0.57.2

%description
A native Hyprland plugin that draws Omarchy's theme-neutral titlebars on
floating windows. Dragging a titlebar moves the window, and dragging the
titlebar of a maximized window restores its floating size under the pointer.

This is a fork of Hypr Development's BSD-licensed hyprbars, adapted for the
Hyprland 0.57 Lua API. The library is installed at the fixed path expected by
Omarchy core and still registers itself with Hyprland as "hyprbars", keeping
the hl.plugin.hyprbars.add_button() interface and plugin.hyprbars.* options.

%prep
%autosetup -n omarchy-hyprland-titlebars-%{version}

%build
%__cmake -S . -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_LIBDIR=lib
%__cmake --build build

%install
DESTDIR=%{buildroot} %__cmake --install build
install -Dm644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
install -Dm644 LICENSE.MIT %{buildroot}%{_datadir}/licenses/%{name}/LICENSE.MIT

%files
%license %{_datadir}/licenses/%{name}/LICENSE
%license %{_datadir}/licenses/%{name}/LICENSE.MIT
%doc README.md
%{_prefix}/lib/omarchy-hyprland-titlebars/titlebars.so

%changelog
* Sat Nov 21 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial COPR package from upstream tag v%{version}.
- Pin Hyprland 0.57.2 to match the headers used in the COPR chroots.
- Force CMAKE_INSTALL_LIBDIR=lib to keep Omarchy's fixed /usr/lib path.
