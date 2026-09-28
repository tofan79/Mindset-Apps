Name:           omareel-git
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Minimal, keyboard-driven video cutter for Wayland compositors
License:        MIT
URL:            https://github.com/omacom/omareel
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  x86_64

# CMakeLists.txt baris 2: cmake_minimum_required(VERSION 3.21)
BuildRequires:  cmake >= 3.21
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig

# CMakeLists.txt baris 9:
#   find_package(Qt6 6.8 REQUIRED COMPONENTS Core Concurrent Gui GuiPrivate
#               Quick QuickControls2 Multimedia OpenGL Svg Test)
# Core/Gui/Concurrent ikut qt6-qtbase-devel. Quick + QuickControls2 ikut
# qt6-qtdeclarative-devel. Multimedia → qt6-qtmultimedia-devel. Svg →
# qt6-qtsvg-devel.
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtmultimedia-devel

# "GuiPrivate" tidak diekspos paket qt6-qtbase-devel biasa — header privatnya
# ada di paket tersendiri. Tanpa BuildRequires ini, find_package(Qt6 ...
# COMPONENTS GuiPrivate) gagal dengan "Qt6GuiPrivate" tidak ditemukan.
BuildRequires:  qt6-qtbase-private-devel

# Test hanya dipakai unit test upstream; tidak perlu untuk RPM dan menambah
# waktu build. Diturn-offen di %build.
%if 0%{?with_tests}
BuildRequires:  qt6-qttest-devel
%endif

# CMakeLists.txt baris 10: find_package(LayerShellQt REQUIRED)
#
# Nama paket Fedora adalah "layer-shell-qt-devel" (dengan tanda hubung), bukan
# "layershellqt-devel". Modul CMake-nya memang LayerShellQt, dan inilah yang
# sering dikira salah ketik — sudah diverifikasi ada di F44
# (layer-shell-qt-devel-6.7.5-1.fc44.x86_64). Karena REQUIRED, build gagal
# tanpa ini.
BuildRequires:  layer-shell-qt-devel

# CMakeLists.txt baris 19-21 (pkg_check_modules ... REQUIRED IMPORTED_TARGET):
#
# Catatan penting: yang searched oleh pkg_check_modules adalah nama .pc
# ("libturbojpeg", "wayland-client"), BUKAN nama paket RPM. Nama paketnya
# berbeda: libturbojpeg → turbojpeg(-devel), wayland-client →
# libwayland-client. Menyalin nama .pc langsung ke BuildRequires akan
# menggagalkan build.
BuildRequires:  turbojpeg-devel
BuildRequires:  libevdev-devel
BuildRequires:  wayland-devel

# Pustaka runtime yang cocok dengan BuildRequires di atas.
Requires:       layer-shell-qt
Requires:       turbojpeg
Requires:       libevdev
Requires:       libwayland-client
Requires:       hicolor-icon-theme
# Quick/QuickControls2/Multimedia dipakai di runtime oleh QML. Di Fedora,
# libQt6Quick.so dimiliki paket qt6-qtdeclarative — tidak ada paket
# "qt6-qtbase-quick".
Requires:       qt6-qtbase-gui
Requires:       qt6-qtdeclarative
Requires:       qt6-qtmultimedia
Requires:       qt6-qtsvg

# Plugin Hyprland (capture-exclusion) tidak dikunci sebagai BuildRequires
# hyprland-devel: CMakeLists.txt memakai pkg_check_modules(HYPRLAND QUIET
# hyprland) dan hanya add_subdirectory(plugin) bila ditemukan. Jadi di chroot
# COPR yang tidak punya hyprland-devel, plugin dilewati diam-diam dan build
# tetap berhasil. Equal dipakai di %build lewat -DOMAREEL_BUILD_HYPRLAND_PLUGIN=OFF
# supaya perilaku di chroot deterministik dan tidak bergantung pada apa yang
# kebetulan terpasang.

%global debug_package %{nil}

%description
OmaReel is a minimal, keyboard-driven video cutter. It runs as a Wayland
client using Qt Quick, draws its own window with LayerShellQt so it can sit
flush against the screen edges, and cuts video by driving FFmpeg through the
multimedia stack (thumbnail previews come from libjpeg-turbo via
libturbojpeg; input events via libevdev).

%{name} is a daily rolling build tracking the tip of upstream's master
branch. Upstream has tagged v0.1.0, but this spec deliberately follows the
branch tip so post-0.1.0 fixes land without waiting on a new tag. %{version}
encodes the commit date and short SHA, e.g. 20260928.gitabcdef1.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -DOMAREEL_BUILD_HYPRLAND_PLUGIN=OFF
%cmake_build

%install
%cmake_install

%post
gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor >/dev/null 2>&1 || :
update-desktop-database -q >/dev/null 2>&1 || :

%postun
gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor >/dev/null 2>&1 || :
update-desktop-database -q >/dev/null 2>&1 || :

%files
%license LICENSE
%license LICENSES/lucide.txt
%doc README.md
%{_bindir}/omareel
# CMakeLists.txt baris 249 membuat symlink omarecord -> omareel lewat
# install(CODE ... create_symlink), jadi keduanya ikut terpasang.
%{_bindir}/omarecord
%{_datadir}/applications/omareel.desktop
%{_datadir}/icons/hicolor/scalable/apps/omareel.svg
# Baris 245-247 mengiterasi ukuran ikon 16..512 ke hicolor/<n>x<n>/apps/.
%{_datadir}/icons/hicolor/*/apps/omareel.png

%changelog
* Mon Sep 28 2026 Mindset Apps <mindset@example.com> - 20260928.git0000000-1
- Initial packaging of omareel-git.
- BuildRequires layer-shell-qt-devel (hyphenated Fedora name) for
  find_package(LayerShellQt REQUIRED).
- BuildRequires qt6-qtbase-private-devel for the Qt6 GuiPrivate component.
- Hyprland capture-exclusion plugin disabled explicitly in %build; upstream
  makes it optional and auto-skips when hyprland pkg-config is absent.
