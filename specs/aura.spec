# aura: pengelola wallpaper hidup native Rust untuk COSMIC/GNOME/KDE/Wayland.
# Upstream hanya menerbitkan tarball x86_64 dengan binary yang sudah di-build
# (aura + mpvpaper), jadi spec ini TIDAK membangun dari sumber: workflow
# mengunduh tarball rilis itu lalu memasang ulang isinya — pola yang sama
# dengan `sonora` dan `zapfast` di repo ini. Lebih penting lagi: Cargo.toml
# memakai dependensi git (pop-os/libcosmic), jadi build from source di chroot
# COPR justru paling tidak bisa dipercaya.
#
# Volatile deps dari `mpvpaper` (libmpv, libwayland-...) otomatis lahir dari
# soname lewat rpmbuild, tapi kami tetap menulis Requires: mpv-libs agar tujuan
# runtime jelas.

Name:           aura
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Live wallpaper manager for COSMIC, GNOME, KDE, and Wayland
License:        GPL-3.0-or-later
URL:            https://github.com/antwny/aura
Source0:        aura-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

ExclusiveArch:  x86_64

Requires:       mpv-libs
Requires:       hicolor-icon-theme

%description
Aura is a native Rust live wallpaper manager built for COSMIC Desktop, with
experimental support for GNOME and KDE Plasma on Wayland as well as generic
wlr-layer-shell compositors (Niri, Hyprland, Sway). It supports animated video
and image wallpapers, smart auto-pause at 0% CPU/GPU, dynamic desktop
auto-theming, multi-monitor arrangements, and a quick-switcher HUD.

This package repacks the upstream tarball; nothing is rebuilt on Fedora.

%prep
%setup -q -n aura-%{version}

%install
install -Dpm0755 aura %{buildroot}%{_bindir}/aura
install -Dpm0755 mpvpaper %{buildroot}%{_bindir}/mpvpaper

install -Dpm0644 io.github.antwny.aura.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/io.github.antwny.aura.svg
install -Dpm0644 navbar-open-symbolic.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/actions/navbar-open-symbolic.svg
install -Dpm0644 navbar-closed-symbolic.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/actions/navbar-closed-symbolic.svg

install -Dpm0644 io.github.antwny.aura.desktop \
    %{buildroot}%{_datadir}/applications/io.github.antwny.aura.desktop
# desktop entry upstream memakai nama tanpa path (Exec=aura). Desktop launcher
# di GNOME/COSMIC tidak selalu mewarisi PATH session, jadi mengikuti langkah
# install.sh upstream: tulis path absolut.
sed -i 's|^Exec=aura switcher$|Exec=%{_bindir}/aura switcher|' \
    %{buildroot}%{_datadir}/applications/io.github.antwny.aura.desktop
sed -i 's|^Exec=aura$|Exec=%{_bindir}/aura|' \
    %{buildroot}%{_datadir}/applications/io.github.antwny.aura.desktop
sed -i 's|^TryExec=aura$|TryExec=%{_bindir}/aura|' \
    %{buildroot}%{_datadir}/applications/io.github.antwny.aura.desktop
grep -q '^TryExec=' %{buildroot}%{_datadir}/applications/io.github.antwny.aura.desktop || \
    sed -i '/^Exec=/i TryExec=%{_bindir}/aura' %{buildroot}%{_datadir}/applications/io.github.antwny.aura.desktop

install -Dpm0644 io.github.antwny.aura.metainfo.xml \
    %{buildroot}%{_datadir}/metainfo/io.github.antwny.aura.metainfo.xml

%files
%license LICENSE
%{_bindir}/aura
%{_bindir}/mpvpaper
%{_datadir}/applications/io.github.antwny.aura.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.antwny.aura.svg
%{_datadir}/icons/hicolor/scalable/actions/navbar-open-symbolic.svg
%{_datadir}/icons/hicolor/scalable/actions/navbar-closed-symbolic.svg
%{_datadir}/metainfo/io.github.antwny.aura.metainfo.xml

%changelog
* Fri Nov 06 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package, repacked from the upstream x86_64 tarball.
- Build from source is intentionally NOT used: Cargo.toml pulls git
  (pop-os/libcosmic), which is not reliably available inside COPR chroots.