# Dua hal yang dulu dibaca dari path build-time (`env!("CARGO_MANIFEST_DIR")`)
# sudah diperbaiki di aplikasi, dan spec ini ikut menyesuaikan:
#  - Logo shell di-embed ke binary lewat include_bytes! (tidak ada file data).
#  - Skel template dibaca dari %{_datadir}/rakuos-shell-picker (fallback ke
#    source tree saat dev), jadi paket WAJIB menginstal seluruh skel/ ke sana
#    dengan layout yang mencerminkan src/compositor — lihat bagian %install.

# rpm di Fedora 44 otomatis membuat subpaket debuginfo/debugsource; dari
# tarball pihak ketiga tidak ada layout debugsource yang bisa dietakan,
# sehingga keduanya dimatikan (sama seperti software-center/omashow).
%global debug_package %{nil}

Name:           rakuos-shell-picker
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Pick the desktop shell (Noctalia/DMS/Caelestia/Ambxst) on Hyprland

License:        GPL-3.0-only
URL:            https://github.com/tofan79/rakuos-shell-picker
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  x86_64

# Rust + GTK4/libadwaita (gtk4 crate 0.9 butuh gtk4 >= 4.6; libadwaita crate
# 0.7 dengan feature v1_6 butuh libadwaita >= 1.6 — keduanya sudah jauh
# terpenuhi di Fedora 44, chroot COPR tidak perlu repo pihak ketiga).
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  desktop-file-utils

# Polkit agent dipanggil lewat `pkexec` untuk operasi install/uninstall paket.
# gtk4/libadwaita tidak ditulis manual: rpm mendeteksi soname ELF otomatis.
Requires:       polkit

%description
RakuOS Shell Picker memilih desktop shell (panel/widgets/lapisan status) yang
berjalan di atas compositor Hyprland, tanpa me-restart compositor. Shell yang
tersedia: Noctalia, DMS (DankMaterialShell), Caelestia, dan Ambxst. Setiap
switch mem-backup konfigurasi lama dan bisa di-rollback.

%prep
%autosetup -n %{name}-%{version}

%build
cargo build --release --locked

%install
install -Dpm0755 target/release/rakuos-shell-picker \
    %{buildroot}%{_bindir}/rakuos-shell-picker

install -Dpm0644 data/org.rakuos.ShellPicker.desktop \
    %{buildroot}%{_datadir}/applications/org.rakuos.ShellPicker.desktop

for s in 16 22 24 32 48 64 128 256 512; do
    install -Dpm0644 "data/icons/hicolor/${s}x${s}/apps/org.rakuos.ShellPicker.png" \
        "%{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/org.rakuos.ShellPicker.png"
done
install -Dpm0644 data/org.rakuos.ShellPicker.svg \
    "%{buildroot}%{_datadir}/icons/hicolor/scalable/apps/org.rakuos.ShellPicker.svg"

# Skel template: switch menyalin isinya ke home user. Layout harus mencerminkan
# src/compositor supaya jalur relatif skel_for() ketemu setelah dipasang
# (src/apply.rs). Tanpa ini, switch berhenti dengan "the skel has no .config/hypr".
for d in src/compositor/*/shells/*/skel; do
    rel="${d#src/compositor/}"
    install -d "%{buildroot}%{_datadir}/rakuos-shell-picker/${rel}"
    cp -a "$d/." "%{buildroot}%{_datadir}/rakuos-shell-picker/${rel}/"
done

%check
desktop-file-validate \
    %{buildroot}%{_datadir}/applications/org.rakuos.ShellPicker.desktop

%files
%license LICENSE
%{_bindir}/rakuos-shell-picker
%{_datadir}/applications/org.rakuos.ShellPicker.desktop
%{_datadir}/icons/hicolor/*/apps/org.rakuos.ShellPicker.png
%{_datadir}/icons/hicolor/scalable/apps/org.rakuos.ShellPicker.svg
%{_datadir}/rakuos-shell-picker/

%changelog
* Sat Oct 10 2026 Mindset Apps <mindset@example.com> - 0.9.3-1
- New app icon (folder glyph rendered from SVG), also shipped scalable.

* Sat Oct 10 2026 Mindset Apps <mindset@example.com> - 0.9.2-1
- Initial COPR packaging of rakuos-shell-picker.
- Ship the skel template tree under %{_datadir}/rakuos-shell-picker; the
  switch refuses to run without it ("the skel has no .config/hypr").
- Logo assets are compiled into the binary (include_bytes!).
