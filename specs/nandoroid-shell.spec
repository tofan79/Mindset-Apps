# NAnDoroid: payload Quickshell untuk Hyprland (plan 2, fase 1).
#
# Runtime quickshell-git, matugen, dgop, jq, python3 dan alat CLI/fitur
# sengaja TIDAK dijadikan Requires/Recommends. Pola ini sama dengan ambxst,
# caelestia-shell dan inir-shell: install plan rakuos-shell-picker yang
# memasangnya, jadi `rum install nandoroid-shell` tidak menarik setengah
# desktop. Daftar lengkapnya nanti ditulis di plan picker, bukan di spec.
#
# Pengecualian: qt6-qt5compat adalah modul QML yang wajib saat shell.qml
# dimuat (`import Qt5Compat.GraphicalEffects` di panel). Tanpa itu shell
# gagal total, alasan yang sama dengan kf6-syntax-highlighting di ambxst.

%global debug_package %{nil}

Name:           nandoroid-shell
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        NAnDoroid Quickshell desktop shell for Hyprland
License:        AGPL-3.0-only
URL:            https://github.com/na-ive/nandoroid-shell
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       qt6-qt5compat

%description
NAnDoroid is a Quickshell desktop shell for Hyprland that follows Android 16
Material 3 design: status bar, dock, dashboard, spotlight, quick settings,
notifications, lock screen, and first-party widgets.

The package contains the shell payload and matugen templates. It does not run
the upstream install.sh and does not modify ~/.config/hypr; the shell picker
owns the user configuration.

%prep
%autosetup -n %{name}-%{version}

%install
install -d %{buildroot}%{_datadir}/quickshell/nandoroid
cp -a dotfiles/.config/quickshell/nandoroid/. \
    %{buildroot}%{_datadir}/quickshell/nandoroid/

install -d %{buildroot}%{_datadir}/nandoroid
cp -a dotfiles/.config/matugen \
    %{buildroot}%{_datadir}/nandoroid/matugen
cp -a dotfiles/.config/hypr \
    %{buildroot}%{_datadir}/nandoroid/hypr

# Upstream currently ships this symlink with a missing target; drop it so
# rpmlint/packaging does not carry a dangling icon into the image.
rm -f %{buildroot}%{_datadir}/quickshell/nandoroid/assets/icons/ai-openai-symbolic.svg

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_datadir}/quickshell/nandoroid/
%{_datadir}/nandoroid/

%changelog
* Wed Oct 21 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial packaging of na-ive/nandoroid-shell (v1.6.0).
- Payload at /usr/share/quickshell/nandoroid; matugen templates and Hyprland
  integration examples at /usr/share/nandoroid.
- Runtime stays manual in the picker install plan; only the hard QML module
  qt6-qt5compat is a Requires.
