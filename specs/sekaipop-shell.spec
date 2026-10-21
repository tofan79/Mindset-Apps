# SekaiPop: payload Quickshell untuk Hyprland (plan 3).
#
# Runtime quickshell-git, matugen, font, cava, dan alat CLI sengaja TIDAK
# dijadikan Requires. Pola nandoroid/whisker/ambxst: install plan
# rakuos-shell-picker yang memasangnya, bukan resolver RPM.
#
# Yang tetap Requires hanya modul QML yang wajib saat shell.qml dimuat
# (qt6-qtmultimedia untuk `import QtMultimedia`) dan python3 karena beberapa
# skrip shell memakai shebang python3.

%global debug_package %{nil}

Name:           sekaipop-shell
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        SekaiPop Quickshell desktop shell for Hyprland
License:        GPL-3.0-only
URL:            https://github.com/Blapples/SekaiPop
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  qt6-qtshadertools

Requires:       qt6-qtbase
Requires:       qt6-qtdeclarative
Requires:       qt6-qtmultimedia
Requires:       qt6-qtsvg
Requires:       qt6-qtimageformats
Requires:       qt6-qtwayland
Requires:       python3

%description
SekaiPop is a Project Sekai inspired Quickshell desktop shell for Hyprland:
bar, dock, phone, lock screen, notifications, polkit agent, wallpaper, and
first-party widgets.

The package installs the shell payload at /usr/share/quickshell/sekaipop and
Hyprland integration examples at /usr/share/sekaipop/hypr. It does not run
the upstream install.sh and does not modify ~/.config/hypr; the shell picker
owns the user configuration. The self-updater is disabled because /usr is
managed by RPM.

%prep
%autosetup -n %{name}-%{version}

# Paket ini dikelola RPM. Matikan self-update yang akan mencoba mengganti
# folder di /usr/share; halaman About tetap menampilkan versi tanpa menulis
# ke /usr dan tanpa melakukan request jaringan.
sed -i 's/readonly property bool canApply: isGit || managed/readonly property bool canApply: false/' \
    sekaipop/services/UpdateService.qml
sed -i '/^    function check(byUser) {/a\        root.status = "current"\n        root.latest = root.version\n        return' \
    sekaipop/services/UpdateService.qml

%build
# Fedora menaruh qsb di /usr/lib64/qt6/bin, bukan di PATH.
QSB=$(command -v qsb || true)
if [ -z "$QSB" ]; then
    for candidate in /usr/lib64/qt6/bin/qsb /usr/lib/qt6/bin/qsb; do
        if [ -x "$candidate" ]; then
            QSB="$candidate"
            break
        fi
    done
fi
[ -n "$QSB" ] || { echo "qsb not found (install qt6-qtshadertools)"; exit 1; }
PATH="$(dirname "$QSB"):$PATH" bash sekaipop/shaders/compile-shaders.sh

%install
install -d %{buildroot}%{_datadir}/quickshell/sekaipop
cp -a sekaipop/. %{buildroot}%{_datadir}/quickshell/sekaipop/
# Tests are development-only and not part of the runtime payload.
rm -rf %{buildroot}%{_datadir}/quickshell/sekaipop/tests

# Upstream stores some helper scripts as 0644 even though QML calls them
# directly. Mark the shebang scripts executable so the payload matches a
# normal git checkout.
find %{buildroot}%{_datadir}/quickshell/sekaipop/scripts \
     %{buildroot}%{_datadir}/quickshell/sekaipop/shaders \
     -type f \( -name '*.sh' -o -name '*.py' \) -exec chmod 0755 {} +

install -d %{buildroot}%{_datadir}/sekaipop
cp -a hypr %{buildroot}%{_datadir}/sekaipop/hypr

%files
%license LICENSE
%doc README.md
%{_datadir}/quickshell/sekaipop/
%{_datadir}/sekaipop/

%changelog
* Wed Oct 21 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial packaging of Blapples/SekaiPop from a pinned main snapshot.
- Shaders are rebuilt with Fedora qt6-qtshadertools; payload at
  /usr/share/quickshell/sekaipop, Hyprland examples at /usr/share/sekaipop/hypr.
- Self-update is disabled because /usr is RPM-managed. Runtime tools stay
  manual in the picker install plan; only hard QML modules and python3 are
  Requires.
