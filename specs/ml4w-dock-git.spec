# ML4W Dock (mylinuxforwork/ml4w-dock) dikemas sebagai paket noarch berisi
# QML murni; tidak ada kompilasi. Upstream belum menaruh file LICENSE di repo
# (API GitHub: license=None), sementara repo saudaranya di ml4w pakai
# GPL-3.0 — diasumsikan GPL-3.0-only dan perlu diverifikasi ke maintainer.
#
# Layout RPM:
#   /usr/share/ml4w-dock/        -> shell.qml + DockApp/ + bin/ml4w-dock
#   /usr/bin/ml4w-dock           -> symlink ../share/ml4w-dock/bin/ml4w-dock
#
# Script bin/ml4w-dock menghitung DOCK_DIR lewat readlink -f terhadap lokasi
# script lalu naik dua tingkat, sehingga symlink di /usr/bin ke bin/ di
# /usr/share/ml4w-dock membuat DOCK_DIR jatuh tepat ke /usr/share/ml4w-dock
# tanpa perlu patch upstream. Ia dijalankan `qs -n -p "$DOCK_DIR"`.
#
# Config pengguna ditulis ke ~/.config/.. (bukan di dalam dir app), jadi
# direktori terpasang boleh read-only. Jalur lama ML4W (~/.local/share/
# ml4w-dock) dipenuhi lewat symlink di skel shell.

Name:           ml4w-dock-git
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        ML4W dock for the Quickshell desktop shell (rolling build)

License:        GPL-3.0-only
URL:            https://github.com/mylinuxforwork/ml4w-dock
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

# Runtime (quickshell-git dsb.) TIDAK ditarik via Requires: dipasang eksplisit
# oleh install_plan shell ML4W di rakuos-shell-picker (rum install ...).

%description
Dock untuk desktop ML4W yang dijalankan di atas Quickshell (qs). Menampilkan
ikon aplikasi, peluncur, menu, dan dialog pengaturan; dikontrol lewat IPC
(dock toggle/enable/disable/reload/settings). Jalankan dengan `ml4w-dock start`.

Paket %{name} adalah build rolling yang mengikuti tip cabang main upstream
(versi = tanggal commit + SHA pendek).

%prep
%autosetup -n %{name}-%{version}

%build
# Tidak ada langkah build: paket berisi QML + script, bukan biner.

%install
install -Dpm0755 bin/ml4w-dock %{buildroot}%{_datadir}/ml4w-dock/bin/ml4w-dock
install -Dpm0644 shell.qml %{buildroot}%{_datadir}/ml4w-dock/shell.qml
cp -a DockApp %{buildroot}%{_datadir}/ml4w-dock/
install -d %{buildroot}%{_bindir}
ln -s ../share/ml4w-dock/bin/ml4w-dock %{buildroot}%{_bindir}/ml4w-dock

%files
%doc README.md
%doc screenshots/
%{_bindir}/ml4w-dock
%{_datadir}/ml4w-dock/

%changelog
* Mon Oct 12 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial COPR packaging (source: mylinuxforwork/ml4w-dock @ 2026-09-24 8d065e3).
- /usr/share/ml4w-dock + symlink /usr/bin/ml4w-dock yang mempertahankan
  logika DOCK_DIR bawaan upstream tanpa patch.