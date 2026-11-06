# zapfast: native WhatsApp client (Rust + egui, MIT). Upstream menerbitkan RPM
# x86_64 di setiap rilis, jadi spec ini TIDAK membangun dari sumber: workflow
# mengunduh RPM rilis itu, membongkar payload-nya, lalu memasang ulang file
# yang sama (binary, .desktop, ikon, dokumentasi, hook tema Omarchy).
#
# Pola ini sama dengan `nuclear` dan `sonora` di repo ini. Untungnya: build
# COPR selesai dalam hitungan detik dan tidak pernah gagal karena perubahan
# dependensi Rust/crates.io. Ruginya: paket berisi binary hasil build upstream
# (glibc >= 2.35), bukan hasil kompilasi di Fedora, dan hanya untuk x86_64
# karena upstream hanya menerbitkan arsitektur itu.
#
# Alternatif build dari sumber sengaja tidak dipakai: Cargo.toml memakai
# dependensi git (whatsapp-rust dari github dengan rev tetap), sehingga build
# di chroot COPR bergantung pada GitHub tetap bisa diakses dan pada rev yang
# tidak hilang.

Name:           zapfast
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Fast native WhatsApp client built with Rust and egui
License:        MIT
URL:            https://github.com/crmne/zapfast
Source0:        zapfast-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

# Rilis upstream hanya menyediakan RPM x86_64.
ExclusiveArch:  x86_64

# Binary ini membuka libGL/libEGL (glow), libxkbcommon, dan libwayland lewat
# dlopen, jadi soname-nya tidak pernah muncul di ELF NEEDED dan rpmbuild tidak
# bisa menurunkannya sendiri. Daftar Requires ini disalin dari RPM upstream
# supaya dependensi runtime tidak hilang saat di-repack.
Requires:       libglvnd-glx
Requires:       libglvnd-egl
Requires:       libxkbcommon
Requires:       libxkbcommon-x11
Requires:       libwayland-client
Requires:       libwayland-cursor
Requires:       libwayland-egl
Requires:       libX11
Requires:       libX11-xcb
Requires:       libXcursor
Requires:       libXi
Requires:       libXrandr

%description
ZapFast is a fast, native WhatsApp client written in Rust and drawn with egui.
It runs as a single small binary instead of an Electron shell: the WhatsApp Web
protocol is spoken directly, so chats, media, calls, stickers, and polls work
without embedding a browser.

This package repacks the upstream x86_64 RPM; nothing is rebuilt locally.

%prep
%setup -q -n zapfast-%{version}

%install
install -Dpm0755 usr/bin/zapfast %{buildroot}%{_bindir}/zapfast

install -Dpm0644 usr/share/applications/zapfast.desktop \
    %{buildroot}%{_datadir}/applications/zapfast.desktop

install -Dpm0644 usr/share/icons/hicolor/scalable/apps/zapfast.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/zapfast.svg

# Hook tema Omarchy (skrip + template JSON) yang dipanggil lewat
# `omarchy hook install theme-set ...`. Bukan dependensi, tapi ikut dikirim
# upstream dan hanya berguna kalau ikut terpasang.
cp -a usr/share/zapfast %{buildroot}%{_datadir}/zapfast

# LICENSE dan README.md tidak di-stage ke %{buildroot} di sini: %license dan
# %doc mengambil berkasnya langsung dari direktori build lalu memasangnya ke
# /usr/share/licenses/zapfast/ dan /usr/share/doc/zapfast/.

%files
%license LICENSE
%doc README.md
%{_bindir}/zapfast
%{_datadir}/applications/zapfast.desktop
%{_datadir}/icons/hicolor/scalable/apps/zapfast.svg
%{_datadir}/zapfast/

%changelog
* Fri Nov 06 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package, repacked from the upstream x86_64 RPM.
