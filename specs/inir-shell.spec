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
# 2.33.0-2 sudah ada di COPR; -3 adalah build pertama yang membawa chmod
# rekursif di %install (script/*.sh|*.fish|*.py jadi 0755). Tanpa ini doctor
# upstream menyebut 5 script "diperbaiki" padahal /usr immutable menolak chmod.
Release:        3%{?dist}
Summary:        iNiR desktop shell payload, launcher, and user service (Niri/Quickshell)
BuildArch:      noarch

License:        GPL-3.0-only
URL:            https://github.com/snowarch/iNiR
Source0:        %{name}-%{version}.tar.gz

# runtime-payload.py menyalurkan payload lewat rsync (include/exclude dari
# sdata/runtime-payload-dirs.txt + runtime-root-files.txt).
BuildRequires:  rsync
BuildRequires:  python3

# Dipakai %%{_userunitdir} di %install/%files. Tanpa paket ini rpmbuild di
# chroot COPR (fedora-45) tidak mengenal macronya dan gagal dengan
# "File must begin with /: %%{_userunitdir}/inir.service".
BuildRequires:  systemd-rpm-macros

# ---- Konteks runtime; sengaja BUKAN Requires (pola ambxst/caelestia) ----
# quickshell-git, font (material-symbols-fonts, jetbrains-mono-fonts-all),
# dan alat CLI (grim, slurp, wl-clipboard, playerctl, golang untuk
# inir-washi, dst — peta lengkapnya di distro/arch/inir-shell/PKGBUILD)
# dipasang manual lewat install plan rakuos-shell-picker, bukan resolver rpm.
#
# Yang tetap Requires hanya modul QML yang WAJIB ada supaya shell bisa
# dimuat (alasan yang sama dengan ambxst): org.kde.kirigami dipakai panel
# (waffle bar, sidebar, close-confirm) dan org.kde.syntaxhighlighting
# dipakai MessageCodeBlock.qml — tanpa paketnya komponen gagal dimuat
# dengan "module ... is not installed".
Requires:       kf6-kirigami
Requires:       kf6-syntax-highlighting

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
- Requires minimal (pola ambxst): hanya kf6-kirigami + 
  kf6-syntax-highlighting (modul QML wajib). quickshell-git, font, dan
  alat CLI dipasang manual lewat install plan rakuos-shell-picker.
- Tanpa Conflicts noctalia: eksklusivitas shell diatur rakuos-shell-picker.
- BuildRequires systemd-rpm-macros supaya %{_userunitdir} ter-expand di
  chroot COPR (temuan build #11163782: "File must begin with /").
- Filter requires karangan `/usr/bin/-S_...` dari shebang venv upstream
  (${INIR_VENV:-...} di get_keybinds.py, generate_colors_material.py)
  via __requires_exclude supaya `rum install` tidak gagal.
