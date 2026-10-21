# Whisker: payload Quickshell untuk Hyprland (plan 2, fase 1).
#
# Runtime quickshell-git, matugen, cava, mpvpaper, qt6ct, fish,
# NetworkManager, brightnessctl, power-profiles-daemon, wl-clipboard,
# cliphist, grim/slurp/wf-recorder, ffmpeg dan curl sengaja TIDAK dijadikan
# Requires/Recommends. Pola ambxst/caelestia/inir: install plan picker yang
# memasangnya, bukan resolver RPM.
#
# Dua pengecualian:
#  - whisker-cli adalah dependensi nyata: shell memanggil `whisker prefs`,
#    `whisker ipc`, dan `whisker notify` saat runtime.
#  - qt6-qtmultimedia menyediakan `import QtMultimedia`; tanpa modul QML itu
#    shell.qml tidak bisa dimuat.

%global debug_package %{nil}

Name:           whisker-shell
Version:        %{pkg_version}
Release:        1.20261018git7bf4078%{?dist}
Summary:        Whisker Quickshell desktop shell for Hyprland
License:        GPL-3.0-only
URL:            https://github.com/corecathx/whisker
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       whisker-cli
Requires:       qt6-qtmultimedia

%description
Whisker is a Material 3 desktop shell for Hyprland built with Quickshell: bar,
dock, launcher, quick panel, notifications, OSD, lock screen, and built-in
screenshot and clipboard surfaces.

The package installs the Quickshell payload at /usr/share/whisker and pulls
the whisker CLI. greetd integration files are examples only; RakuOS keeps its
own greeter.

%prep
%autosetup -n %{name}-%{version}

%install
install -d %{buildroot}%{_datadir}/whisker
cp -a . %{buildroot}%{_datadir}/whisker/
rm -rf %{buildroot}%{_datadir}/whisker/.git \
       %{buildroot}%{_datadir}/whisker/.github \
       %{buildroot}%{_datadir}/whisker/.gitignore
# LICENSE is shipped through %license, not duplicated in the payload.
rm -f %{buildroot}%{_datadir}/whisker/LICENSE

%files
%license LICENSE
%{_datadir}/whisker/

%changelog
* Wed Oct 21 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1.20261018git7bf4078
- Initial packaging of corecathx/whisker (main, no upstream tags).
- Payload at /usr/share/whisker, matching the AUR package layout.
- Runtime stays manual in the picker install plan; whisker-cli and
  qt6-qtmultimedia are the only Requires.
