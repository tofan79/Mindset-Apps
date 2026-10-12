# Quickshell Overview (Shanu-Kumawat/quickshell-overview) — workspace overview
# untuk Hyprland berbasis Quickshell: preview window live, drag-and-drop antar
# workspace, navigasi keyboard. QML murni, tidak ada kompilasi.
#
# Repo ml4w-quickshell-overview hanya installer yang menclone repo ini ke
# ~/.local/share/quickshell-overview; konten yang dipaket di sini adalah repo
# Shanu-Kumawat itu sendiri (yang launcher ML4W jalankan dengan
# `qs -p ~/.local/share/quickshell-overview`).
#
# License: README upstream menampilkan badge "GPL" dan AUR quickshell-overview-
# git mengemasnya sebagai GPL; file LICENSE tidak disertakan (API GitHub:
# license=None). Diasumsikan GPL-3.0-only, perlu diverifikasi.
#
# Penting: config pengguna BUKAN dibaca dari folder app, melainkan dari
# $XDG_CONFIG_HOME/quickshell/overview/config.json (common/Config.qml), dengan
# fallback ke nilai bawaan bila tidak ada. Maka direktori /usr/share aman
# read-only; config.example.json dikirim sebagai contoh.

Name:           ml4w-quickshell-overview-git
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Quickshell workspace overview for Hyprland (rolling build)

License:        GPL-3.0-only
URL:            https://github.com/Shanu-Kumawat/quickshell-overview
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

# Runtime (quickshell-git dsb.) TIDAK ditarik via Requires: dipasang eksplisit
# oleh install_plan shell ML4W di rakuos-shell-picker (rum install ...).

%description
Overview workspace Hyprland yang berdiri sendiri: menampilkan semua workspace
dengan preview window live, dukungan seret-dan-lepas antar workspace, dan
navigasi keyboard (Super+Tab). Dijalankan dengan `qs -p <dir>` dan dikontrol
lewat IPC.

Paket %{name} adalah build rolling yang mengikuti tip cabang main upstream
(versi = tanggal commit + SHA pendek).

%prep
%autosetup -n %{name}-%{version}

%build
# Tidak ada langkah build: paket berisi QML, bukan biner.

%install
install -Dpm0644 shell.qml %{buildroot}%{_datadir}/ml4w-quickshell-overview/shell.qml
install -Dpm0644 quickshell-overview.qml %{buildroot}%{_datadir}/ml4w-quickshell-overview/quickshell-overview.qml
install -Dpm0644 config.example.json %{buildroot}%{_datadir}/ml4w-quickshell-overview/config.example.json
cp -a modules services common assets %{buildroot}%{_datadir}/ml4w-quickshell-overview/

%files
%doc README.md
%{_datadir}/ml4w-quickshell-overview/

%changelog
* Mon Oct 12 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial COPR packaging (source: Shanu-Kumawat/quickshell-overview @ 2026-08-14 47f0d40).
- QML + aset ke /usr/share/ml4w-quickshell-overview; config pengguna dibaca
  dari ~/.config/quickshell/overview/config.json sesuai common/Config.qml.