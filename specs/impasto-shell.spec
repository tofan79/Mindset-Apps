# Impasto: payload Quickshell untuk Hyprland (plan 3).
#
# Runtime quickshell-git, awww, ImageMagick, wl-clipboard, playerctl, dan
# alat CLI lain sengaja TIDAK dijadikan Requires. Pola nandoroid/whisker/
# ambxst: install plan rakuos-shell-picker yang memasangnya.
#
# Requires hanya modul QML wajib (QtQuick.Effects dan QtMultimedia) dan
# python3 karena skrip shell memakai shebang python3.

%global debug_package %{nil}

Name:           impasto-shell
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Impasto Quickshell desktop shell for Hyprland
License:        GPL-3.0-only
URL:            https://github.com/andreumassanet/impasto
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       qt6-qtbase
Requires:       qt6-qtdeclarative
Requires:       qt6-qtmultimedia
Requires:       qt6-qtsvg
Requires:       qt6-qtimageformats
Requires:       qt6-qtwayland
Requires:       python3

%description
Impasto is a Quickshell desktop shell for Hyprland with a dynamic island,
desktop widgets, notes and tasks, a lock screen, and a Python IPC CLI.

The package installs the shell at /usr/share/quickshell/impasto, Hyprland
examples at /usr/share/impasto/hypr, and theme profiles at
/usr/share/impasto/share. It does not install the upstream desktop, PAM,
SDDM, or system polkit files; the shell picker owns the user configuration.

%prep
%autosetup -n %{name}-%{version}

# RPM menaruh shell di /usr/share/quickshell/impasto, bukan langsung di
# ~/.config/quickshell. Dua penyesuaian kecil supaya CLI tetap bekerja:
#  - panggilan IPC memakai `qs -c impasto` (bukan instance default)
#  - skrip capture dibaca dari folder impasto, bukan folder quickshell root.
sed -i 's|\["qs", "ipc", "call", target, function, "--", \*values\]|["qs", "-c", "impasto", "ipc", "call", target, function, "--", *values]|' \
    home/.local/bin/impasto
sed -i 's|os.path.join(config, "quickshell", "scripts", "capture.py")|os.path.join(config, "quickshell", "impasto", "scripts", "capture.py")|' \
    home/.local/bin/impasto

%install
install -d %{buildroot}%{_datadir}/quickshell/impasto
cp -a home/.config/quickshell/. %{buildroot}%{_datadir}/quickshell/impasto/

install -d %{buildroot}%{_datadir}/impasto
cp -a home/.config/hypr %{buildroot}%{_datadir}/impasto/hypr
cp -a home/.local/share/impasto %{buildroot}%{_datadir}/impasto/share

install -Dpm 0755 home/.local/bin/impasto %{buildroot}%{_bindir}/impasto

%files
%license LICENSE
%doc README.md
%{_bindir}/impasto
%{_datadir}/quickshell/impasto/
%{_datadir}/impasto/

%changelog
* Wed Oct 21 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial packaging of andreumassanet/impasto from tag v0.6.0.
- Shell at /usr/share/quickshell/impasto, Hyprland examples and theme
  profiles at /usr/share/impasto, and the impasto IPC CLI at /usr/bin.
- Does not install system/, PAM, SDDM, polkit, or the rest of the desktop.
  Runtime tools stay manual; only hard QML modules and python3 are Requires.
