# ML4W Dotfiles Settings (mylinuxforwork/ml4w-dotfiles-settings) — utility
# interaktif (Bash + gum) plus memberi UI Quickshell (lib/quickshell/
# SettingsApp). License: GPL-3.0 (LICENSE disertakan upstream).
#
# Layout RPM mengikuti kontrak upstream: `make install` menyalin isi lib/
# TANPA subfolder lib/ ke LIB_DIR, dan script CLI membaca $LIB_DIR/utils.sh
# serta $LIB_DIR/colors/. Di RPM:
#   /usr/share/ml4w-dotfiles-settings/     -> utils.sh, colors/, quickshell/, demo/
#   /usr/bin/ml4w-dotfiles-settings        -> script CLI (LIB_DIR di-patch)
#
# Dua baris di bin/ml4w-dotfiles-settings di-patch lewat sed pada %prep agar
# instalasi sistem berfungsi tanpa mengubah upstream:
#   LIB_DIR  "$HOME/.local/share/ml4w-dotfiles-settings"  -> /usr/share/mL4W...
#   DEMO_FILE "$APP_DIR/demo/settings.json"               -> /usr/share/.../demo:
# Deteksi dev (SCRIPT_DIR mengandung "/ml4w-dotfiles-settings/bin") tidak
# terpicu karena script berada di /usr/bin.
#
# Jalur autostart ML4W (`qs -p ~/.local/share/mL4W-dotfiles-settings/quickshell`)
# dijembatani oleh symlink skel shell ke /usr/share/ml4w-dotfiles-settings.
# Profil pengguna berada di ~/.config/ml4w-dotfiles-settings, bukan di LIB_DIR.

Name:           ml4w-dotfiles-settings-git
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        ML4W settings manager backed by Quickshell (Bash + gum CLI)

License:        GPL-3.0-only
URL:            https://github.com/mylinuxforwork/ml4w-dotfiles-settings
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

# Runtime TIDAK ditarik via Requires: quickshell-git, gum, jq, gawk dsb.
# dipasang eksplisit oleh install_plan shell ML4W di rakuos-shell-picker.

%description
Aplikasi pengaturan desktop ML4W: memilih dan mengganti nilai konfigurasi
melalui TUI (gum) atau melalui window Quickshell. Profil disimpan per-pengguna
di ~/.config/ml4w-dotfiles-settings/.

Paket %{name} adalah build rolling yang mengikuti tip cabang main upstream
(versi = tanggal commit + SHA pendek).

%prep
%autosetup -n %{name}-%{version}

# Patch jalur instalasi agar paket terpasang berfungsi dari /usr (tanpa
# mengubah file upstream).
sed -i \
    's|LIB_DIR="$HOME/.local/share/ml4w-dotfiles-settings"|LIB_DIR="/usr/share/ml4w-dotfiles-settings"|' \
    bin/ml4w-dotfiles-settings
sed -i \
    's|DEMO_FILE="$APP_DIR/demo/settings.json"|DEMO_FILE="/usr/share/ml4w-dotfiles-settings/demo/settings.json"|' \
    bin/ml4w-dotfiles-settings

%build
# Tidak ada langkah build: paket berisi script Bash + QML, bukan biner.

%install
install -Dpm0755 bin/ml4w-dotfiles-settings %{buildroot}%{_bindir}/ml4w-dotfiles-settings
install -Dpm0644 lib/utils.sh %{buildroot}%{_datadir}/ml4w-dotfiles-settings/utils.sh
install -d %{buildroot}%{_datadir}/ml4w-dotfiles-settings/colors
install -pm0644 lib/colors/colors.json %{buildroot}%{_datadir}/ml4w-dotfiles-settings/colors/colors.json
install -d %{buildroot}%{_datadir}/ml4w-dotfiles-settings/demo
install -pm0644 demo/settings.json demo/Theme.qml \
    %{buildroot}%{_datadir}/ml4w-dotfiles-settings/demo/
cp -a lib/quickshell %{buildroot}%{_datadir}/ml4w-dotfiles-settings/

%files
%license LICENSE
%doc README.md
%{_bindir}/ml4w-dotfiles-settings
%{_datadir}/ml4w-dotfiles-settings/

%changelog
* Mon Oct 12 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial COPR packaging (source: mylinuxforwork/ml4w-dotfiles-settings @ 2026-10-01 9199d4b).
- Bin CLI dipatch (LIB_DIR + DEMO_FILE) mengarah ke /usr/share, mengikuti
  kontrak layout `make install` upstream (isi lib/ tanpa folder lib/).