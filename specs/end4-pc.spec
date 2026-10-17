Name:           end4-pc
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        end4-pC Quickshell shell config (fork of dots-hyprland ii)

# LICENSE root GPL-3.0; font tulisan tangan di assets/fonts/handwriting
# berlisensi OFL-1.1 + Apache-2.0 (satu font), lihat LICENSES.txt.
License:        GPL-3.0-only AND OFL-1.1 AND Apache-2.0
URL:            https://github.com/pctrade/end4-pC
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

# Config ini adalah pendamping base illogical-impulse: ia memakai logika
# skrip base yang sama (env qsConfig=end4-pC di hyprland), jadi base ikut
# sebagai Requires. Modul QML wajib (org.kde.kirigami, syntaxhighlighting)
# sudah di-Requires base. quickshell-git, matugen, font, dan alat CLI
# dipasang manual lewat install plan rakuos-shell-picker (pola minimal
# ambxst, sama seperti inir-shell/illogical-impulse).
Requires:       illogical-impulse

# Skrip python payload memakai shebang venv upstream
# `#!/usr/bin/env -S /bin/sh -c "source ..."`. Varian yang di-escape
# (`-S\_`) lolos dari brp-mangle-shebangs, lalu generator dependensi rpm
# membaca seluruh baris shebang sebagai path interpreter dan menulis
# Requires karangan `/usr/bin/-S_/bin/sh_-c_...` yang tidak disediakan
# paket mana pun -> `rum install`/dnf gagal "nothing provides".
# Interpreter sebenarnya sudah dijamin (sh/bash/python3) dan venv dibuat
# install plan rakuos-shell-picker, jadi dependensi palsu itu disaring.
%global __requires_exclude ^/usr/bin/-S_

%description
end4-pC adalah fork komunitas dari config Quickshell illogical-impulse
(dots-hyprland) untuk desktop Hyprland: bar, dock, launcher, control center,
preset gallery, dan widget tambahan.

Paket ini berisi snapshot config fork (version 2026MMDD.git<sha>) di
%{_datadir}/quickshell/end4-pC (nama direktori case-sensitive; Session.qml
hardcode `qs -c end4-pC`). Penyaluran ke ~/.config/quickshell/end4-pC
dilakukan oleh skel rakuos-shell-picker — jangan jalankan installer/git
clone upstream di sistem yang config-nya dikelola paket.

Dua surface yang di-neutralkan saat build karena khusus Arch:
 1. services/DotsUpdater.qml — tombol "Update dots"/"Update system" diganti
    jadi notifikasi yang menunjuk `sudo dnf upgrade` (upstream akan git
    clone dan menimpa config).
 2. Perintah update di modules/ii/bar/UpdatesCount.qml dan default
    apps.update di modules/common/Config.qml — `yay`/`pacman` diganti
    `sudo dnf upgrade`.
Sisa penyebutan pacman/yay di scripts/ (mis. saran paket upscayl di
switchwall.sh) dibiarkan: jalur itu hanya fallback saran saat dependensi
opsional tidak ada dan tidak dijalankan paket ini.

%prep
%autosetup -n %{name}-%{version}

# --- Neutralisasi surface paket-manager Arch ---
# Stub DotsUpdater: pertahankan API yang dipanggil DashboardHomePage.qml /
# About.qml (runSystemUpdate, runUpdateDots), ganti isinya dengan notifikasi.
cat > services/DotsUpdater.qml <<'EOF'
pragma Singleton

import qs
import QtQuick
import Quickshell

// Dikelola paket RPM (rakuos): fungsi self-update upstream diganti info dnf
// supaya git clone / yay tidak menimpa config yang dipasang paket.
Singleton {
    id: root

    function runSystemUpdate() {
        Quickshell.execDetached(["notify-send", "end4-pC",
            "Sistem dikelola paket — jalankan: sudo dnf upgrade",
            "-a", "Shell"])
        Qt.callLater(() => GlobalStates.settingsOpen = false)
    }

    function runUpdateDots() {
        Quickshell.execDetached(["notify-send", "end4-pC",
            "Config dikelola paket end4-pc — jalankan: sudo dnf upgrade end4-pc",
            "-a", "Shell"])
        Qt.callLater(() => GlobalStates.settingsOpen = false)
    }
}
EOF

# Guard grep: kalau upstream mengganti string ini, build gagal supaya
# patch-nya ditinjau ulang (pola guard yang sama dengan kineticwe).
grep -q '"yay -Syu --combinedupgrade=false"' modules/ii/bar/UpdatesCount.qml \
    || { echo "UpdatesCount.qml: string yay berubah, tinjau ulang patch"; exit 1; }
sed -i 's|"yay -Syu --combinedupgrade=false"|"sudo dnf upgrade"|' modules/ii/bar/UpdatesCount.qml

grep -q "pkexec pacman -Syu" modules/common/Config.qml \
    || { echo "Config.qml: string pkexec pacman berubah, tinjau ulang patch"; exit 1; }
sed -i "s|kitty -1 --hold=yes fish -i -c 'pkexec pacman -Syu'|kitty -1 --hold=yes fish -i -c 'sudo dnf upgrade'|" modules/common/Config.qml

%install
mkdir -p %{buildroot}%{_datadir}/quickshell/end4-pC
cp -a . %{buildroot}%{_datadir}/quickshell/end4-pC/
# Screenshot README (8 MB) tidak dipakai runtime — tidak ikut ke paket,
# tapi tetap utuh di tarball SRPM sebagai sumber.
rm -rf %{buildroot}%{_datadir}/quickshell/end4-pC/screenshots

%files
%license LICENSE
%license assets/fonts/handwriting/LICENSES.txt
%{_datadir}/quickshell/end4-pC/

%changelog
* Sat Oct 17 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial COPR packaging of pctrade/end4-pC (RPM 2, lapisan fork di atas
  base illogical-impulse): snapshot main + payload ke
  /usr/share/quickshell/end4-pC.
- Require minimal: hanya illogical-impulse (base), sesuai pola ambxst;
  quickshell-git/matugen/font/alat CLI dipasang install plan picker.
- Neutralisasi surface Arch: DotsUpdater di-stub (notifikasi dnf),
  perintah update yay/pacman di UpdatesCount.qml dan Config.qml diganti
  sudo dnf upgrade (dengan guard grep).
- Filter requires karangan `/usr/bin/-S_...` dari shebang venv upstream
  (scripts/colors/*.py dan scripts/hyprland/*.py) via __requires_exclude
  supaya `rum install` tidak gagal "nothing provides".
