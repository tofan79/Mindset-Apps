# umbriel-git: Wayland compositor dari branch main (build harian).
#
# Umbriel adalah kompositor C++23 berbasis wlroots 0.20. Upstream belum
# merilis tag yang stabil, jadi paket ini diperbarui setiap hari dari commit
# terbaru branch main. Sumber tarball disiapkan workflow
# `.github/workflows/umbriel-git.yml` agar puncak repositori tetap rapi.
#
# Scone lokal umbrielfx (hard fork SceneFX) ikut dibangun in-tree, sehingga
# paket SceneFX terpasang tidak diperlukan.

%global debug_package        %{nil}
%global _lto_cflags          %{nil}

Name:           umbriel-git
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Wayland compositor built on wlroots (daily build)
License:        MIT
URL:            https://github.com/noctalia-dev/umbriel
Source0:        %{name}-%{version}.tar.gz

ExclusiveArch:  x86_64 aarch64

BuildRequires:  meson >= 1.3
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git

BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  wlroots-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libinput-devel
BuildRequires:  libeis-devel
BuildRequires:  pixman-devel
BuildRequires:  tomlplusplus-devel
BuildRequires:  json-devel
BuildRequires:  cairo-devel
BuildRequires:  pango-devel
BuildRequires:  libdrm-devel
BuildRequires:  libdisplay-info-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xcb-util-cursor-devel
BuildRequires:  systemd-devel
BuildRequires:  lcms2-devel
BuildRequires:  zlib-ng-compat-devel

# libeis dan libinput ikut runtime melalui libwlroots.
Requires:       xorg-x11-server-Xwayland

%description
Umbriel adalah kompositor Wayland modern berbasis wlroots dengan scrolling,
dwindle, master layout, workspace per output, blur, shadows, dan animasi
halus. Paket ini dibangun harian dari branch main upstream.

%prep
%autosetup -n %{name}-%{version}

%build
%meson \
    --buildtype=release \
    -Dtests=disabled \
    -Dtracy=disabled \
    -Djemalloc=disabled \
    -Dlcms2=auto \
    -Dlocaled=enabled
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md PACKAGING.md
%{_bindir}/umbriel
%{_bindir}/start-umbriel
%{_datadir}/umbriel/
%{_datadir}/wayland-sessions/umbriel.desktop
%{_userunitdir}/umbriel.service
%{_userunitdir}/umbriel-session.target
%{_userunitdir}/umbriel-shutdown.target

%changelog
* Sat Oct 31 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial packaging for umbriel-git from branch main.