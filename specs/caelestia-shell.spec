# LTO dimatikan untuk seluruh paket ini. libcava menyematkan file data
# (contoh config, shader, tema) lewat third_party/incbin.h yang menghasilkan
# direktif assembler .incbin berpath relatif; path itu lolos saat compile
# biasa, tapi lto-wrapper mengulang-assembly di direktori sementara tanpa
# include-path sumber sehingga gagal "file not found" saat link. Opt-out ini
# cara resmi redhat-rpm-config, dan flag-nya diekspor otomatis ke CFLAGS
# oleh mekanisme _auto_set_build_flags.
%global _lto_cflags %{nil}

# Dua dependensi build TIDAK tersedia di Fedora, jadi dibundel langsung di
# sini (satu SRPM) alih-alih dijadikan BuildRequires terpisah:
#
#  - libcava (Source1): fork cava dengan API library. Plugin caelestia
#    memanggil pkg_check_modules(libcava) di plugin/CMakeLists.txt, dan
#    Fedora tidak membangun paket ini sama sekali.
#  - m3shapes (Source2): modul QML M3Shapes (Material Shapes). Repo upstream
#    tidak punya tag rilis, jadi versinya dipin ke commit yang sama dengan
#    yang di-lock flake.nix upstream shell.
#
# Kedua pin di bawah juga dibaca .github/workflows/caelestia-shell.yml (awk)
# untuk mengunduh Source1/Source2 — ubah versinya cukup di sini.
%global cava_version 1.0.0
%global m3shapes_rev 32ad9ce328bb77ed349b40a3be10ee9ea610b8ab

Name:           caelestia-shell
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Caelestia desktop shell for Wayland compositors (Quickshell)

License:        GPL-3.0-only
URL:            https://github.com/caelestia-dots/shell
Source0:        caelestia-shell-v%{version}.tar.gz
Source1:        cava-%{cava_version}.tar.gz
Source2:        m3shapes-%{m3shapes_rev}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  meson
BuildRequires:  pkgconf-pkg-config

# plugin/CMakeLists.txt: find_package(Qt6 ShaderTools Core Qml Gui Quick
# QuickControls2 Concurrent Sql Network DBus) + pkg_check_modules
# libqalculate, libpipewire-0.3, aubio + find_library(sensors).
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtshadertools-devel
BuildRequires:  libqalculate-devel
BuildRequires:  pipewire-devel
BuildRequires:  aubio-devel
BuildRequires:  lm_sensors-devel

# Untuk membangun libcava (Source1) sendiri: meson.build-nya mewajibkan
# fftw3 (dependency required) dan iniparser (find_library, lalu error kalau
# tidak ketemu).
BuildRequires:  fftw-devel
BuildRequires:  iniparser-devel

# Entry point "caelestia" dipakai untuk menjalankan/mengendalikan shell.
# Versinya sengaja tidak dikunci: caelestia-cli dirilis mandiri dari repo
# terpisah (1.1.3 saat shell 2.5.0), jadi `= %{version}-%{release}` selalu
# menghasilkan dependensi yang mustahil terpenuhi — resolver menolak shell
# dengan "nothing provides caelestia-cli = 2.5.0-1".
Requires:       caelestia-cli
Requires:       quickshell
# Alat yang dipanggil langsung dari QML/service: nmcli (NetworkManager),
# ddcutil (DDC/CI monitor), brightnessctl (backlight), swappy (anotasi
# screenshot), slurp (pilih area), wl-copy (clipboard), notify-send
# (notifikasi fallback), fish (wrap terminal), qt6-qtimageformats (webp dll),
# sh/bash untuk wrapper.
#
# power-profiles-daemon sengaja TIDAK dijadikan Requires. Panel profil daya
# membacanya lewat D-Bus (singleton QML PowerProfiles), jadi tanpa daemon itu
# cuma widgetnya yang kosong — shell tetap jalan. Paketnya pun tidak ada di
# semua distro, dan saat tidak tersedia instalasi berhenti di
# "none of the providers can be installed".
Requires:       bash
Requires:       fish
Requires:       ddcutil
Requires:       brightnessctl
Requires:       NetworkManager
Requires:       swappy
Requires:       slurp
Requires:       wl-clipboard
Requires:       libnotify
Requires:       qt6-qtimageformats
# Font fallback sengaja TIDAK dijadikan Recommends: biar instalasi tidak
# diam-diam menarik paket font. Daftarnya ada di README (manual, opsional).

%description
Caelestia is a desktop shell for Wayland compositors, built on Quickshell:
material-style UI, autoteming, Cava audio visualiser, workspace, system and
media services, launcher, lock screen, and more.

Paket ini membundel dua dependensi yang tidak dipaket di Fedora: libcava
(pustaka analisis audio untuk visualiser) dan m3shapes (modul QML Material
Shapes). CLI caelestia ada di paket terpisah caelestia-cli.

%prep
%setup -q -n caelestia-shell-v%{version}

# Sumber tambahan diekstrak sebagai saudara direktori utama (lihat %build).
# Tarball GitHub selalu punya satu direktori top-level, jadi
# --strip-components=1.
mkdir -p ../cava ../m3shapes
tar xf %{SOURCE1} --strip-components=1 -C ../cava
tar xf %{SOURCE2} --strip-components=1 -C ../m3shapes

%build
# --- libcava (Source1) ---
# Cuma pustaka: build_target default memang 'lib', tapi semua backend
# input/output dimatikan eksplisit supaya (a) tidak ikut tersandung
# dependensi yang tidak ada di buildroot (alsa/pulse/sdl/ncurses) dan
# (b) sanitizer 'auto' tidak ikut tersandung. Plugin caelestia menyerahkan
# audio sendiri lewat cava_execute(), jadi backend itu memang tidak dipakai.
cd ../cava
meson setup cava-build . \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --buildtype=release \
    -Dbuild_target=lib \
    -Dcava_font=false \
    -Dinput_alsa=disabled \
    -Dinput_portaudio=disabled \
    -Dinput_pulse=disabled \
    -Dinput_sndio=disabled \
    -Dinput_pipewire=disabled \
    -Dinput_oss=disabled \
    -Dinput_jack=disabled \
    -Dinput_coreaudio=disabled \
    -Dinput_coreaudio_tap=disabled \
    -Doutput_sdl=disabled \
    -Doutput_sdl_glsl=disabled \
    -Doutput_ncurses=disabled \
    -Dasan=disabled \
    -Dtsan=disabled \
    -Dubsan=disabled
meson compile -C cava-build

# Pasang ke staging prefix BUKAN ke %{buildroot}: configure shell butuh
# header + pustaka lewat pkg-config, sedangkan file yang nantinya masuk
# %{buildroot} (di %install) harus tetap memakai prefix /usr yang benar
# untuk end-user. Yang di-sed hanya pc-file di staging.
CAVA_STAGE=%{_builddir}/cava-stage
DESTDIR="${CAVA_STAGE}" meson install -C cava-build
PC=$(find "${CAVA_STAGE}" -name libcava.pc)
sed -i "s|^prefix=.*|prefix=${CAVA_STAGE}%{_prefix}|" "$PC"
# Cflags bawaan cuma memuat ${includedir}/cava, ${includedir}/cava/input dan
# ${includedir}/cava/output — cukup untuk konsumen yang menulis
# `#include <cavacore.h>`. Plugin caelestia menulis `#include <cava/cavacore.h>`,
# jadi butuh ${includedir} induknya; tanpa ini compile mati di cavaprovider.hpp
# dengan "cava/cavacore.h: No such file or directory".
sed -i 's|^Cflags: *|Cflags: -I${includedir} |' "$PC"

# --- m3shapes (Source2) ---
# INSTALL_QMLDIR default upstream "usr/lib/qt6/qml" (relatif, dirancang
# untuk prefix=/ ala AUR). QML import path Fedora ada di
# %{_libdir}/qt6/qml, jadi di-override dengan path absolut supaya cocok
# dengan %files.
cd ../m3shapes
cmake -S . -B build \
    -GNinja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DINSTALL_QMLDIR:PATH=%{_libdir}/qt6/qml
cmake --build build

# --- caelestia shell (Source0) ---
# Tanpa PKG_CONFIG_PATH ini pkg_check_modules(Cava) di plugin gagal: file
# .pc libcava belum (dan tidak boleh) terpasang di sistem.
export PKG_CONFIG_PATH="${CAVA_STAGE}%{_libdir}/pkgconfig${PKG_CONFIG_PATH:+:${PKG_CONFIG_PATH}}"

cd ../caelestia-shell-v%{version}
cmake -S . -B build \
    -GNinja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_sysconfdir} \
    -DDISTRIBUTOR="Mindset-Apps" \
    -DVERSION=%{version} \
    -DGIT_REVISION="$(cat REVISION 2>/dev/null || echo unknown)"
cmake --build build

%install
cd ../cava
DESTDIR=%{buildroot} meson install -C cava-build

cd ../m3shapes
DESTDIR=%{buildroot} cmake --install build

cd ../caelestia-shell-v%{version}
DESTDIR=%{buildroot} cmake --install build

%files
%license LICENSE
# Binary versi (extras/) dan modul QML: plugin Caelestia (termasuk backing
# lib di Caelestia/lib) + M3Shapes.
%{_libdir}/caelestia/
%{_libdir}/qt6/qml/Caelestia/
%{_libdir}/qt6/qml/M3Shapes/
# libcava yang dibundel (plugin men-link soname-nya di runtime).
%{_libdir}/libcava.so.*
# Tautan dev yang ikut terpasang dari `meson install`. Paket ini sudah membawa
# header dan libcava.pc, jadi tautannya memang bagian dari paket: kalau tidak
# dicantumkan, rpm berhenti di "Installed (but unpackaged) file(s)".
%{_libdir}/libcava.so
%{_libdir}/pkgconfig/libcava.pc
%{_includedir}/cava/
# Config quickshell: shell.qml, assets/ (termasuk wrap_term_launch.sh),
# components/, modules/, services/, utils/, LICENSE.
%{_sysconfdir}/xdg/quickshell/caelestia/

%changelog
* Thu Oct 08 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial COPR packaging of caelestia-shell.
- Bundles libcava (LukashonakV/cava 1.0.0) and m3shapes (pinned commit)
  as extra source tarballs: neither is packaged in Fedora, and
  lint-specs.yml requires every BuildRequires to resolve there.
- Cava is built library-only with every input/output backend disabled —
  the plugin feeds audio itself via cava_execute().
