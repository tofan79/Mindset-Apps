# ML4W Power Menu (mylinuxforwork/ml4w-powermenu) dikemas sebagai paket noarch
# berisi QML murni; tidak ada kompilasi. Upstream belum menaruh file LICENSE
# (API GitHub: license=None); diasumsikan GPL-3.0-only (sama dengan repo
# saudaranya di ml4w) dan perlu diverifikasi.
#
# Layout RPM:
#   /usr/share/ml4w-powermenu/   -> shell.qml + PowerApp/ + bin/ml4w-powermenu
#   /usr/bin/ml4w-powermenu      -> symlink ../share/ml4w-powermenu/bin/...
#
# Sama seperti ml4w-dock, script menghitung MENU_DIR via readlink -f lalu naik
# dua tingkat; symlink di /usr/bin ke /usr/share/ml4w-powermenu/bin membuat
# MENU_DIR jatuh ke /usr/share/ml4w-powermenu tanpa patch. Dijalankan dengan
# `qs -n -p "$MENU_DIR"`.
#
# Config pengguna ditulis ke ~/.config/.., jadi direktori app boleh read-only.

Name:           ml4w-powermenu-git
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        ML4W power menu for the Quickshell desktop shell (rolling build)

License:        GPL-3.0-only
URL:            https://github.com/mylinuxforwork/ml4w-powermenu
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

# Runtime (quickshell-git dsb.) TIDAK ditarik via Requires: dipasang eksplisit
# oleh install_plan shell ML4W di rakuos-shell-picker (rum install ...).

%description
Menu daya (lock/logout/reboot/shutdown/suspend) untuk desktop ML4W yang
dijalankan di atas Quickshell. Dikontrol lewat IPC (`ml4w-powermenu start`
untuk menjalankan, `toggle`/`open`/`close`/`reload`/`edit` untuk kendali).

Paket %{name} adalah build rolling yang mengikuti tip cabang main upstream
(versi = tanggal commit + SHA pendek).

%prep
%autosetup -n %{name}-%{version}

%build
# Tidak ada langkah build: paket berisi QML + script, bukan biner.

%install
install -Dpm0755 bin/ml4w-powermenu %{buildroot}%{_datadir}/ml4w-powermenu/bin/ml4w-powermenu
install -Dpm0644 shell.qml %{buildroot}%{_datadir}/ml4w-powermenu/shell.qml
cp -a PowerApp %{buildroot}%{_datadir}/ml4w-powermenu/
install -d %{buildroot}%{_bindir}
ln -s ../share/ml4w-powermenu/bin/ml4w-powermenu %{buildroot}%{_bindir}/ml4w-powermenu

%files
%doc README.md
%doc screenshots/
%{_bindir}/ml4w-powermenu
%{_datadir}/ml4w-powermenu/

%changelog
* Mon Oct 12 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial COPR packaging (source: mylinuxforwork/ml4w-powermenu @ 2026-10-04 fff7ffe).
- /usr/share/ml4w-powermenu + symlink /usr/bin/ml4w-powermenu yang menjaga
  logika MENU_DIR bawaan upstream tanpa patch.