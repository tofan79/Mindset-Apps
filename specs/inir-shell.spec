# inir-shell — payload sistem iNiR (shell Quickshell untuk Niri).
#
# Sumber blueprint: distro/arch/inir-shell/PKGBUILD upstream + peta nama
# paket Fedora di sdata/dist-fedora/install-deps.sh. Layout di %install
# sengaja mengikuti PKGBUILD package() supaya launcher /usr/bin/inir
# menemukan payload di /usr/share/quickshell/inir (urutan deteksinya:
# ~/.config/quickshell/inir -> /usr/local/share/... -> /usr/share/...).
#
# Quickshell SENGAJA bukan Requires (pola ambxst/caelestia): paket Fedora
# bernama "quickshell" masih 0.2.1, sedangkan iNiR butuh 0.3+. Runtime yang
# dipakai ekosistem rakuos adalah quickshell-git 0.3.3, dipasang oleh image
# dan oleh install plan rakuos-shell-picker — bukan lewat resolver rpm.
#
# Tidak ada "Conflicts: noctalia": picker yang mengatur eksklusivitas antar
# shell (hanya satu shell berjalan), dan file kedua paket tidak bentrok.
# RPM-level Conflicts akan memaksa copot Noctalia bahkan saat hanya ingin
# mencoba iNiR di compositor berbeda.

Name:           inir-shell
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        iNiR desktop shell payload, launcher, and user service (Niri/Quickshell)
BuildArch:      noarch

License:        GPL-3.0-only
URL:            https://github.com/snowarch/iNiR
Source0:        %{name}-%{version}.tar.gz

# runtime-payload.py menyalurkan payload lewat rsync (include/exclude dari
# sdata/runtime-payload-dirs.txt + runtime-root-files.txt).
BuildRequires:  rsync
BuildRequires:  python3

# Requires = depends PKGBUILD upstream dipetakan ke nama Fedora lewat
# sdata/dist-fedora/install-deps.sh. Yang sengaja TIDAK ikut:
#  - quickshell  -> quickshell-git dipasang picker/image (lihat atas);
#  - qt6-qtmultimedia-ffmpeg -> tidak ada di Fedora 44 (backend ffmpeg
#    sudah menyatu di qt6-qtmultimedia);
#  - ttf-roboto-flex -> tidak dipaketkan (font fallback UI dipakai);
#  - ttf-jetbrains-mono-nerd -> jetbrains-mono-fonts-all (varian Nerd
#    tidak ada di Fedora);
#  - sisa optdepends Arch (kitty, nautilus, uv, yt-dlp, ...) cukup optdepends,
#    bukan Requires.
Requires:       bash
Requires:       brightnessctl
Requires:       cliphist
Requires:       curl
Requires:       fish
Requires:       google-noto-emoji-fonts
Requires:       golang
Requires:       grim
Requires:       gum
Requires:       jetbrains-mono-fonts-all
Requires:       jq
Requires:       kdialog
Requires:       kf6-kirigami
Requires:       kf6-syntax-highlighting
Requires:       libnotify
Requires:       material-symbols-fonts
Requires:       NetworkManager
Requires:       niri
Requires:       pipewire
Requires:       pipewire-alsa
Requires:       pipewire-pulseaudio
Requires:       playerctl
Requires:       polkit
Requires:       python3
Requires:       qt6-qt5compat
Requires:       qt6-qtbase
Requires:       qt6-qtdeclarative
Requires:       qt6-qtimageformats
Requires:       qt6-qtmultimedia
Requires:       qt6-qtsvg
Requires:       qt6-qtwayland
Requires:       rsync
Requires:       slurp
Requires:       swayidle
Requires:       swaylock
Requires:       wireplumber
Requires:       wl-clipboard
Requires:       wlsunset
Requires:       xdg-desktop-portal
Requires:       xdg-desktop-portal-gnome
Requires:       xdg-desktop-portal-gtk
Requires:       xdg-user-dirs
Requires:       xdg-utils
Requires:       xwayland-satellite

%description
iNiR is a desktop shell for the Niri compositor built on Quickshell: bar,
panels, launcher, notifications, OSD, and a large set of first-party widgets.

Paket ini adalah payload sistem dari installer upstream: runtime QML ke
/usr/share/quickshell/inir (launcher /usr/bin/inir menemukannya di sana),
unit systemd user inir.service (Type=dbus, terkait ke niri.service), desktop
entry, dan ikon. Config pengguna disalurkan lewat skel rakuos-shell-picker,
bukan installer interaktif. Runtime quickshell-git dipasang oleh install plan
picker, bukan oleh resolver rpm.

%prep
# Tarball GitHub dari tag v%{version} selalu bernama iNiR-%{version}.
%autosetup -n iNiR-%{version}

%install
%{__install} -d %{buildroot}%{_datadir}/quickshell
python3 sdata/lib/runtime-payload.py copy --root . --target %{buildroot}%{_datadir}/quickshell/inir

chmod 0755 %{buildroot}%{_datadir}/quickshell/inir/setup
find %{buildroot}%{_datadir}/quickshell/inir/scripts -type f \
  \( -name '*.sh' -o -name '*.fish' -o -name '*.py' \) -exec chmod 0755 {} +

%{__install} -Dpm 0755 scripts/inir %{buildroot}%{_bindir}/inir
%{__install} -Dpm 0644 assets/systemd/inir.service %{buildroot}%{_userunitdir}/inir.service
%{__install} -Dpm 0644 assets/applications/inir.desktop %{buildroot}%{_datadir}/applications/inir.desktop
%{__install} -Dpm 0644 assets/applications/inir-settings.desktop %{buildroot}%{_datadir}/applications/inir-settings.desktop
%{__install} -Dpm 0644 assets/icons/desktop-symbolic.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/inir.svg

# version.json dibaca `inir version/update/doctor`. Adaptasi dari PKGBUILD
# package(): packageManager dnf, tanpa libalpm hook (tidak ada padanan Fedora).
cat > %{buildroot}%{_datadir}/quickshell/inir/version.json <<EOF
{
  "version": "%{version}",
  "commit": "release",
  "installed_at": "$(date -Iseconds)",
  "installedAt": "$(date -Iseconds)",
  "source": "dnf",
  "repo_path": "",
  "repoPath": "",
  "install_mode": "package-managed",
  "installMode": "package-managed",
  "update_strategy": "package-manager",
  "updateStrategy": "package-manager",
  "package_manager": "dnf",
  "packageManager": "dnf",
  "package_name": "inir-shell",
  "packageName": "inir-shell",
  "package_update_hint": "sudo dnf upgrade inir-shell",
  "packageUpdateHint": "sudo dnf upgrade inir-shell"
}
EOF

%files
%license LICENSE
%license NOTICE
%doc README.md docs/SETUP.md docs/IPC.md docs/GAME_PERFORMANCE.md
%{_bindir}/inir
%{_userunitdir}/inir.service
%{_datadir}/applications/inir.desktop
%{_datadir}/applications/inir-settings.desktop
%{_datadir}/icons/hicolor/scalable/apps/inir.svg
%{_datadir}/quickshell/inir/

%changelog
* Sat Oct 17 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial COPR packaging of iNiR (inir-shell) from upstream tag:
  payload via runtime-payload.py manifest (layout mengikuti PKGBUILD:
  /usr/share/quickshell/inir), /usr/bin/inir, inir.service, desktop
  entries, ikon, dan version.json dengan hint dnf package-managed.
- Requires dipetakan dari PKGBUILD depends ke nama Fedora; quickshell-git
  sengaja bukan Requires (dipasang install plan picker, pola ambxst).
- Tanpa Conflicts noctalia: eksklusivitas shell diatur rakuos-shell-picker.
