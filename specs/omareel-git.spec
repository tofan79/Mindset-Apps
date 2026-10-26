Name:           omareel-git
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Minimal, keyboard-driven video cutter for Wayland compositors
License:        MIT
URL:            https://github.com/omacom/omareel
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  x86_64

# CMakeLists.txt baris 2: cmake_minimum_required(VERSION 3.22)
BuildRequires:  cmake >= 3.22
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig

# Sejak 2026-10-25 (merge "rust-foundation" dkk.) upstream memindahkan logika
# program ke Rust: crates/omareel_core, omareel_record, dan omareel_qt yang
# diekspos ke QML lewat CXX-Qt 0.10. C++ yang tersisa hanya UI, plumbing Qt, dan
# plugin Hyprland.
#
# CMakeLists.txt baris 16: find_package(Corrosion REQUIRED). Tanpa paket ini
# configure berhenti dengan "FindCorrosion.cmake not found" — persis kegagalan
# build COPR 2026-10-26. corrosion 0.5.2 di Fedora sudah menyediakan
# corrosion_import_crate(... IMPORTED_CRATES ...) yang dipakai
# cmake/CxxQt.cmake (vendored dari cxx-qt-cmake 0.10).
BuildRequires:  corrosion
# Cargo.toml menetapkan edition 2024 dan rust-version = 1.86; Fedora 44 ke atas
# jauh di atas itu. Corrosion memanggil cargo untuk membangun workspace crates/
# (cxx-qt dan cxx-qt-lib diambil dari crates.io, Cargo.lock tidak memakai
# dependensi git).
BuildRequires:  rust
BuildRequires:  cargo

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

# Test (QtTest untuk sisi C++ dan cargo test untuk crates Rust) hanya dipakai
# upstream; tidak perlu untuk RPM dan menambah waktu build karena menyeret
# qt6-qttest-devel. CTest dimatikan di %build lewat -DBUILD_TESTING=OFF
# (CMakeLists.txt baris 223), yang juga mematikan target omareel_rust_tests.
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

# CMakeLists.txt baris 29-33 (pkg_check_modules ... REQUIRED IMPORTED_TARGET):
#
# Catatan penting: yang searched oleh pkg_check_modules adalah nama .pc
# ("libturbojpeg", "wayland-client"), BUKAN nama paket RPM. Nama paketnya
# berbeda: libturbojpeg → turbojpeg(-devel), wayland-client →
# libwayland-client. Menyalin nama .pc langsung ke BuildRequires akan
# menggagalkan build.
BuildRequires:  turbojpeg-devel
BuildRequires:  libevdev-devel
BuildRequires:  wayland-devel

# wayland-protocols-devel tidak lagi dibutuhkan: wayland-scanner/XForm di
# jalur C++ sudah hilang, dan protokol capture sekarang datang dari crate
# wayland-protocols (fitur "staging") yang isinya dibawa crates.io, bukan XML
# di /usr/share/wayland-protocols.

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
branch. Upstream tags releases (v0.3.0 is the last C++-only one), but this
spec deliberately follows the branch tip so post-release work lands without
waiting on a new tag. %{version} encodes the commit date and short SHA, e.g.
20260928.gitabcdef1.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -DOMAREEL_BUILD_HYPRLAND_PLUGIN=OFF -DBUILD_TESTING=OFF
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
# LICENSES/ kini juga memuat lisensi pihak ketiga: lucide, inter (font),
# cxx-qt-cmake, dan daftar crate Rust. Bawa seluruh direktori, bukan hanya
# lucide.txt, supaya semua lisensi ikut terpasang.
%license LICENSES/
%doc README.md
%{_bindir}/omareel
# CMakeLists.txt baris 218-220 membuat symlink omarecord -> omareel lewat
# add_custom_command(POST_BUILD) + install(CODE ... create_symlink).
%{_bindir}/omarecord
%{_datadir}/applications/omareel.desktop
%{_datadir}/icons/hicolor/scalable/apps/omareel.svg
# install() mengiterasi ukuran ikon 16, 32, 48, 64, 128, 256 ke
# hicolor/<n>x<n>/apps/omareel.png (512 tidak lagi dikirim upstream).
%{_datadir}/icons/hicolor/*/apps/omareel.png

%changelog
* Mon Oct 26 2026 Mindset Apps <mindset@example.com> - 20261026.git742abda5-1
- BuildRequires corrosion, rust, and cargo: upstream moved its program logic
  to Rust crates (CXX-Qt 0.10), so CMakeLists.txt now calls
  find_package(Corrosion REQUIRED) and failed without it.
- Require cmake >= 3.22 to match upstream's cmake_minimum_required.
- Drop wayland-protocols-devel: the C++ wayland-scanner path is gone and the
  capture protocols now come from the wayland-protocols crate.
- Ship the whole LICENSES/ directory; upstream added third-party licenses.

* Mon Sep 28 2026 Mindset Apps <mindset@example.com> - 20260928.git0000000-1
- Initial packaging of omareel-git.
- BuildRequires layer-shell-qt-devel (hyphenated Fedora name) for
  find_package(LayerShellQt REQUIRED).
- BuildRequires qt6-qtbase-private-devel for the Qt6 GuiPrivate component.
- Hyprland capture-exclusion plugin disabled explicitly in %build; upstream
  makes it optional and auto-skips when hyprland pkg-config is absent.
