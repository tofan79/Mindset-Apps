%global __cmake_in_source_build 0
# Pinned KDE master commits. kinetic-we needs the post-6.7 KGlobalAccelD API
# and the KDecoration3::Style enum (server-side drop shadows for CSD windows).
# Bump both pins on each upstream sync.
%{!?kglobalacceld_ref:%global kglobalacceld_ref 5cc88399d8e2a7951798f85127e23f73f1fa0889}
%{!?kdecoration_ref:%global kdecoration_ref d13049250c0ea1afc279aa8dc99243565c0d83e8}
# kconfig_compiler from KConfig < 6.30 generates uncompilable setters for
# enum-class kcfg entries (fixed in KConfig commit 41592cc, first released
# in 6.30). Build the fixed compiler from this pinned KConfig commit and use
# it for kcfg code generation. Drop this once the buildroot ships KConfig >= 6.30.
%{!?kconfig_compiler_ref:%global kconfig_compiler_ref 41592ccfd9748be82c83ce98912037bffb73954e}
# Noctalia greeter (kineticwe-greeter subpackage). Pinned to a stable commit.
%{!?noctalia_greeter_ref:%global noctalia_greeter_ref b3e3bc0268fc5aaf346a250faac70570d15e3bef}

# ===========================================================================
# REQUIRED PACKAGING PATCH: PORTAL LOCALE DOMAIN
#
# The upstream portal source still uses the KDE translation domain and locale
# filenames. The RPM build must rename them to xdg-desktop-portal-kwe so this
# package can coexist with stock xdg-desktop-portal-kde without file conflicts.
# The patch is applied in %prep below and intentionally does not modify the
# upstream source tree. Do not remove it unless the upstream source is fixed.
# ===========================================================================

Name:           kineticwe-git
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Tiling KWin Wayland compositor (daily build from kineticwe-2.0 git)

License:        GPL-2.0-or-later AND LGPL-2.0-or-later AND MIT AND BSD-3-Clause AND CC0-1.0
URL:            https://gitlab.com/theblackdon/kineticwe
Source0:        %{name}-%{version}.tar.gz
Source1:        kglobalacceld-%{kglobalacceld_ref}.tar.gz
Source3:        kineticwe.desktop
Source4:        kglobalacceld-mask.conf
Source5:        kconfig-%{kconfig_compiler_ref}.tar.gz
Source6:        kdecoration-%{kdecoration_ref}.tar.gz
Source8:        noctalia-greeter-%{noctalia_greeter_ref}.tar.gz
Source9:        kineticwe-setup-greeter.sh
Source10:       start-kineticwe.sh

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  extra-cmake-modules
BuildRequires:  pkgconf-pkg-config

BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qt5compat-devel
BuildRequires:  qt6-qtwayland-devel
BuildRequires:  qt6-qttools-devel

BuildRequires:  kf6-kauth-devel
BuildRequires:  kf6-kcolorscheme-devel
BuildRequires:  kf6-kconfig-devel
BuildRequires:  kf6-kcoreaddons-devel
BuildRequires:  kf6-kcrash-devel
BuildRequires:  kf6-kdbusaddons-devel
BuildRequires:  kf6-kglobalaccel-devel
BuildRequires:  kf6-kio-core-libs
BuildRequires:  kf6-kio-devel
BuildRequires:  kf6-kio-gui
BuildRequires:  kf6-kjobwidgets-devel
BuildRequires:  kf6-kguiaddons-devel
BuildRequires:  kf6-ki18n-devel
BuildRequires:  kf6-kidletime-devel
BuildRequires:  kf6-kpackage-devel
BuildRequires:  kf6-kservice-devel
BuildRequires:  kf6-ksvg-devel
BuildRequires:  kf6-kwidgetsaddons-devel
BuildRequires:  kf6-kwindowsystem-devel
BuildRequires:  kf6-kdeclarative-devel
BuildRequires:  kf6-kcmutils-devel
BuildRequires:  kf6-knewstuff-devel
BuildRequires:  kf6-kxmlgui-devel
BuildRequires:  kf6-krunner-devel
BuildRequires:  kf6-knotifications-devel
BuildRequires:  kf6-kirigami-devel
# xdg-desktop-portal-kwe subpackage (rebranded xdg-desktop-portal-kde)
BuildRequires:  kf6-kiconthemes-devel
BuildRequires:  kf6-kitemviews-devel
BuildRequires:  kf6-kstatusnotifieritem-devel
# KIOFileWidgets dev files come from kf6-kio-devel (above); this is the
# runtime library the portal links against.
BuildRequires:  kf6-kio-file-widgets

BuildRequires:  kwayland-devel
BuildRequires:  kscreenlocker-devel
BuildRequires:  knighttime-devel
BuildRequires:  plasma-wayland-protocols-devel
# plasma-activities-devel is intentionally NOT a BuildRequires: KineticWE
# 2.0 drops Activities support (docs/kineticwe-2.0.md Phase 6, "Patch out
# src/activities.cpp; drop the PlasmaActivities build dep"). Leaving that
# BuildRequires in place would have let find_package(PlasmaActivities)
# succeed and silently flip KWIN_BUILD_ACTIVITIES back ON, re-adding a
# hard runtime need on kactivitymanagerd (Plasma's activity manager) that
# the whole point of the 2.0 branch was to remove. -DKWIN_BUILD_ACTIVITIES=OFF
# below is kept as a second, explicit guard so this stays off regardless
# of what the buildroot happens to have installed.
BuildRequires:  libplasma-devel

BuildRequires:  libepoxy-devel
BuildRequires:  libglvnd-opengl
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libxkbcommon-x11-devel
BuildRequires:  libinput-devel
BuildRequires:  libdrm-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libdisplay-info-devel
BuildRequires:  lcms2-devel
BuildRequires:  libxcvt-devel
BuildRequires:  libcanberra-devel
BuildRequires:  libevdev-devel
BuildRequires:  systemd-devel
BuildRequires:  pipewire-devel
BuildRequires:  libEGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  freetype-devel
BuildRequires:  fontconfig-devel
BuildRequires:  vulkan-loader-devel
BuildRequires:  vulkan-headers

BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-cursor-devel
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-renderutil-devel

BuildRequires:  qaccessibilityclient-qt6-devel
BuildRequires:  cairo-devel
BuildRequires:  pango-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  glib2-devel
BuildRequires:  pam-devel
BuildRequires:  polkit-devel
BuildRequires:  libcurl-devel
BuildRequires:  libwebp-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libqalculate-devel
BuildRequires:  libxml2-devel
BuildRequires:  jemalloc-devel
BuildRequires:  json-devel

# Noctalia fork shell (kineticwe-noctalia / noctalia-kwe; vendored at shell/noctalia)
BuildRequires:  meson
BuildRequires:  libsodium-devel
BuildRequires:  libsecret-devel
BuildRequires:  sdbus-cpp-devel
BuildRequires:  wireplumber-devel
BuildRequires:  libsndfile-devel
BuildRequires:  libjxl-devel
BuildRequires:  md4c-devel
BuildRequires:  tomlplusplus-devel
BuildRequires:  libical-devel
BuildRequires:  nlohmann-json-devel
BuildRequires:  stb_image_resize2-devel
BuildRequires:  stb_image_write-devel

# Noctalia greeter (kineticwe-greeter subpackage; built from Source8)
BuildRequires:  wlroots-devel

Requires:       plasma-milou
# The desktopchangeosd effect's QML (src/plugins/desktopchangeosd) imports
# org.kde.plasma.core, provided by libplasma — not pulled by anything else
# below, so without this the "switch desktop" on-screen overlay silently
# fails to load its UI.
Requires:       libplasma
# The window decoration is the first-party org.kineticwe.decoration plugin
# (built in-tree from src/plugins/kineticdecoration); neither Breeze nor the
# distro kdecoration package is required.
Requires:       breeze-icons
Requires:       kineticwe-noctalia = %{version}-%{release}
Requires:       xorg-x11-server-Xwayland
Requires:       hwdata
Requires:       xdg-desktop-portal
Requires:       xdg-desktop-portal-kwe = %{version}-%{release}
Requires:       bash
Requires:       systemd
Requires:       procps-ng
Requires:       psmisc
Recommends:     xdg-user-dirs
Recommends:     qt6ct
Recommends:     spectacle
Recommends:     kf6-qqc2-desktop-style
Requires:       adw-gtk3-theme
# KineticWE installs beside KWin instead of replacing it. There are deliberately
# no Provides/Obsoletes for kwin*, kdecoration, or kglobalacceld: those would
# force DNF to remove the stock KDE packages.

%description
KineticWE is a fork of KWin that adds native tiling support for Wayland.

%{name} is a daily rolling build tracking the tip of the upstream
kineticwe-2.0 branch (version encodes the commit date and short SHA, e.g.
20260926.gitabcdef12). It installs the compositor, runtime plugins,
helpers, and a Wayland session entry, plus the private kglobalacceld and
kdecoration runtime libraries (built from pinned KDE master commits) that
KineticWE links against. The Noctalia fork shell ships in-tree as the
kineticwe-noctalia subpackage (noctalia-kwe binary).

%package -n xdg-desktop-portal-kwe
Summary:        KineticWE portal backend (rebranded xdg-desktop-portal-kde)
License:        LGPL-2.0-or-later

%description -n xdg-desktop-portal-kwe
The xdg-desktop-portal backend for KineticWE sessions: a fork of KDE's
xdg-desktop-portal-kde (v6.7.4) rebranded to export the desktop as KineticWE.
Registers the org.freedesktop.impl.portal.desktop.kwe D-Bus service and is
selected by the freedesktop frontend via kineticwe-portals.conf
([preferred] default=kwe) when XDG_CURRENT_DESKTOP=KineticWE. All stock
interfaces are kept — FileChooser (KDE file dialog), Screenshot, ScreenCast,
Notification, Settings, GlobalShortcuts, etc. The KDE backend is never
started in a KineticWE session.

%package -n kineticwe-noctalia
Summary:        Noctalia fork shell for KineticWE (noctalia-kwe)
License:        MIT AND BSD-3-Clause AND CC0-1.0
# qdbus-qt6 (from qt6-qttools) is used at runtime by the Noctalia
# kineticwe-layouts plugin to read/switch the compositor's /Tiling layouts.
Requires:       qt6-qttools

%description -n kineticwe-noctalia
The Noctalia v5 shell fork for KineticWE, vendored at shell/noctalia and
built in-tree. The binary is renamed to noctalia-kwe so it can coexist with
an upstream noctalia install. Provides the bar, dock, launcher, control
center, notification daemon, lock screen, and settings UI; paired with the
compositor it renders the KineticWE desktop. Session identity is KineticWE
(the shell treats it like KDE for its compositor backends).

%package -n kineticwe-greeter
Summary:        Noctalia greeter for KineticWE (greetd)
License:        MIT
Requires:       %{name} = %{version}-%{release}
Requires:       greetd

%description -n kineticwe-greeter
The Noctalia greeter for KineticWE, providing a login screen via greetd.
After installing, run kineticwe-setup-greeter to configure greetd as your
display manager.

%prep
%autosetup -n %{name}-%{version}

rm -rf ../kglobalacceld
mkdir -p ../kglobalacceld
tar xf %{SOURCE1} -C ../kglobalacceld --strip-components=1

rm -rf ../kdecoration
mkdir -p ../kdecoration
tar xf %{SOURCE6} -C ../kdecoration --strip-components=1

# Rebrand kdecoration translations so they coexist with Fedora's package.
sed -i \
    's/TRANSLATION_DOMAIN=\\"kdecoration\\"/TRANSLATION_DOMAIN=\\"kineticwe-decoration\\"/' \
    ../kdecoration/src/CMakeLists.txt

for po_file in ../kdecoration/po/*/kdecoration.po; do
    [[ -e "${po_file}" ]] || continue
    mv "${po_file}" "${po_file%/kdecoration.po}/kineticwe-decoration.po"
done

for po_file in ../kdecoration/po/*/kineticwe-decoration.po; do
    [[ -e "${po_file}" ]] || continue
    sed -i \
        's/Project-Id-Version: kdecoration/Project-Id-Version: kineticwe-decoration/' \
        "${po_file}"
done

rm -rf ../kconfig
mkdir -p ../kconfig
tar xf %{SOURCE5} -C ../kconfig --strip-components=1

rm -rf ../noctalia-greeter
mkdir -p ../noctalia-greeter
tar xf %{SOURCE8} -C ../noctalia-greeter --strip-components=1

# Packaging-time patch: keep the portal translation domain separate from the
# stock KDE portal so both packages can be installed without locale-file
# ownership conflicts. This intentionally does not modify the upstream source
# tree; the correction is reapplied from the spec on every RPM build.
PORTAL_SRC=%{_builddir}/%{name}-%{version}/portal/xdg-desktop-portal-kwe
sed -i \
    's/TRANSLATION_DOMAIN="xdg-desktop-portal-kde"/TRANSLATION_DOMAIN="xdg-desktop-portal-kwe"/' \
    "${PORTAL_SRC}/src/CMakeLists.txt"
sed -i \
    's/xdg-desktop-portal-kde\.pot/xdg-desktop-portal-kwe.pot/' \
    "${PORTAL_SRC}/Messages.sh"
sed -i \
    's/FILE xdp-kde\.categories/FILE xdp-kwe.categories/' \
    "${PORTAL_SRC}/src/CMakeLists.txt"
for po_file in "${PORTAL_SRC}"/po/*/xdg-desktop-portal-kde.po; do
    [[ -e "${po_file}" ]] || continue
    mv "${po_file}" "${po_file%/xdg-desktop-portal-kde.po}/xdg-desktop-portal-kwe.po"
done
for po_file in "${PORTAL_SRC}"/po/*/xdg-desktop-portal-kwe.po; do
    [[ -e "${po_file}" ]] || continue
    sed -i 's/Project-Id-Version: xdg-desktop-portal-kde/Project-Id-Version: xdg-desktop-portal-kwe/' "${po_file}"
done

# KineticWE coexistence: the vendored runtime libraries must not install under
# the stock KDE sonames (libkdecorations3 / libKGlobalAccelD) or they would
# collide with Fedora's kdecoration/kglobalacceld packages. Append an
# OUTPUT_NAME override; the CMake target names (and thus our link lines) are
# unchanged. The override is applied at the end of each top-level CMakeLists so
# the targets already exist (both projects add_subdirectory(src)).
cat >> %{_builddir}/kdecoration/CMakeLists.txt <<'KWE_KDECO'

# KineticWE: private soname so a stock kdecoration can stay installed.
set_target_properties(kdecorations3 PROPERTIES OUTPUT_NAME kineticwe-decoration)
set_target_properties(kdecorations3private PROPERTIES OUTPUT_NAME kineticwe-decoration-private)
KWE_KDECO

cat >> %{_builddir}/kglobalacceld/CMakeLists.txt <<'KWE_KGA'

# KineticWE: private soname so a stock kglobalacceld can stay installed.
set_target_properties(KGlobalAccelD PROPERTIES OUTPUT_NAME kineticwe-globalacceld)
KWE_KGA

%build
KGA_SRC=%{_builddir}/kglobalacceld
KGA_BUILD=%{_builddir}/kglobalacceld-build
KGA_TMP_PREFIX=%{_builddir}/kga-install

cmake -S "${KGA_SRC}" \
    -B "${KGA_BUILD}" \
    -GNinja \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_SKIP_RPATH=ON \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DBUILD_TESTING=OFF
cmake --build "${KGA_BUILD}"

mkdir -p "${KGA_TMP_PREFIX}"
DESTDIR="${KGA_TMP_PREFIX}" cmake --install "${KGA_BUILD}" --prefix %{_prefix}

# Build kdecoration (pinned KDE master commit) and stage it next to
# kglobalacceld. kinetic-we uses KDecoration3::Style (server-side drop shadows
# for CSD windows), which does not exist in the buildroot's kdecoration 6.7.x.
KDECO_SRC=%{_builddir}/kdecoration
KDECO_BUILD=%{_builddir}/kdecoration-build

cmake -S "${KDECO_SRC}" \
    -B "${KDECO_BUILD}" \
    -GNinja \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_SKIP_RPATH=ON \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DBUILD_TESTING=OFF
cmake --build "${KDECO_BUILD}"

DESTDIR="${KGA_TMP_PREFIX}" cmake --install "${KDECO_BUILD}" --prefix %{_prefix}

# Build the fixed kconfig_compiler (build-time tool only, nothing is installed)
KCFG_BUILD=%{_builddir}/kconfig-build
cmake -S %{_builddir}/kconfig \
    -B "${KCFG_BUILD}" \
    -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_TESTING=OFF
cmake --build "${KCFG_BUILD}" --target kconfig_compiler

%cmake \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_PREFIX_PATH="${KGA_TMP_PREFIX}%{_prefix}" \
    -DCMAKE_SKIP_RPATH=ON \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DBUILD_TESTING=OFF \
    -DKWIN_KCONFIG_COMPILER=${KCFG_BUILD}/bin/kconfig_compiler_kf6 \
    -DKWIN_BUILD_GLOBALSHORTCUTS=ON \
    -DKWIN_BUILD_KCMS=OFF \
    -DKWIN_BUILD_ACTIVITIES=OFF \
    -DCMAKE_DISABLE_FIND_PACKAGE_PlasmaActivities=ON \
    -DCMAKE_DISABLE_FIND_PACKAGE_KF6DocTools=ON
%cmake_build

# --- Phase 4: Build the KineticWE portal backend (rebranded xdg-desktop-portal-kde) ---
PORTAL_SRC=%{_builddir}/%{name}-%{version}/portal/xdg-desktop-portal-kwe
PORTAL_BUILD=%{_builddir}/portal-build

cmake -S "${PORTAL_SRC}" \
    -B "${PORTAL_BUILD}" \
    -GNinja \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_SKIP_RPATH=ON \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DBUILD_TESTING=OFF
cmake --build "${PORTAL_BUILD}"

# --- Phase 5: Build the Noctalia fork shell (noctalia-kwe) ---
SHELL_SRC=%{_builddir}/%{name}-%{version}/shell/noctalia
SHELL_BUILD=%{_builddir}/shell-build

meson setup "${SHELL_BUILD}" "${SHELL_SRC}" \
    --prefix %{_prefix} \
    --buildtype=release \
    -Dtests=disabled
meson compile -C "${SHELL_BUILD}"

# --- Phase 6: Build the Noctalia greeter (kineticwe-greeter) ---
GREETER_SRC=%{_builddir}/noctalia-greeter
GREETER_BUILD=%{_builddir}/greeter-build

meson setup "${GREETER_BUILD}" "${GREETER_SRC}" \
    --prefix %{_prefix} \
    --buildtype=plain \
    -Dcpp_args=-fPIE -Dc_args=-fPIE
meson compile -C "${GREETER_BUILD}"

%install
KGA_BUILD=%{_builddir}/kglobalacceld-build
DESTDIR=%{buildroot} cmake --install "${KGA_BUILD}" --prefix %{_prefix}
DESTDIR=%{buildroot} cmake --install %{_builddir}/kdecoration-build --prefix %{_prefix}
%cmake_install
DESTDIR=%{buildroot} cmake --install %{_builddir}/portal-build --prefix %{_prefix}
sed -i '/^Exec=/a SystemdService=plasma-xdg-desktop-portal-kwe.service' \
    %{buildroot}%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.kwe.service
DESTDIR=%{buildroot} meson install -C %{_builddir}/shell-build
DESTDIR=%{buildroot} meson install -C %{_builddir}/greeter-build
install -Dpm 0755 %{SOURCE9} %{buildroot}%{_bindir}/kineticwe-setup-greeter

# Fedora's greetd package creates the greeter session account as "greetd".
# The upstream tmpfiles entry uses a generic "greeter" account, which makes
# installation emit an unknown-user error before the interactive setup runs.
sed -i \
    -e 's/ greeter greeter / greetd greetd /' \
    -e 's/hardcodes greeter:greeter/hardcodes greetd:greetd/' \
    %{buildroot}%{_tmpfilesdir}/noctalia-greeter.conf

# Install the packaging-local session launcher. This intentionally overrides
# the copy in the source archive so packaging fixes do not modify upstream.
sed -e 's|@INSTALL_PREFIX@|%{_prefix}|g' \
    %{SOURCE10} \
    > %{buildroot}%{_bindir}/start-kineticwe
chmod 0755 %{buildroot}%{_bindir}/start-kineticwe
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_datadir}/wayland-sessions/kineticwe.desktop
install -Dpm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/systemd/user/plasma-kglobalaccel.service.d/kineticwe-mask.conf
install -Dpm 0644 %{_builddir}/%{name}-%{version}/scripts/kineticwe-workspace.target %{buildroot}%{_userunitdir}/kineticwe-workspace.target
install -Dpm 0644 %{_builddir}/%{name}-%{version}/scripts/kineticwe-session.target %{buildroot}%{_userunitdir}/kineticwe-session.target

# Drop development files. This COPR package intentionally ships runtime only.
rm -rf %{buildroot}%{_includedir}/KGlobalAccelD
rm -rf %{buildroot}%{_includedir}/KDecoration3
rm -f %{buildroot}%{_includedir}/KF6/kdecoration3_version.h
rm -rf %{buildroot}%{_includedir}/kwin
rm -rf %{buildroot}%{_libdir}/cmake/KGlobalAccelD
rm -rf %{buildroot}%{_libdir}/cmake/KDecoration3
rm -rf %{buildroot}%{_libdir}/cmake/KWin
rm -rf %{buildroot}%{_libdir}/cmake/KWinDBusInterface
rm -f %{buildroot}%{_libdir}/libkineticwe-globalacceld.so
rm -f %{buildroot}%{_libdir}/libkineticwe-decoration.so
rm -f %{buildroot}%{_libdir}/libkineticwe-decoration-private.so
rm -f %{buildroot}%{_libdir}/libkineticwe.so

# Avoid owning files that conflict with Fedora's stock KWin notification data.
rm -f %{buildroot}%{_datadir}/knotifications6/*.notifyrc
rm -rf %{buildroot}%{_datadir}/dbus-1/interfaces

# Kinetic Settings owns all settings; drop every KDE System Settings module.
rm -rf %{buildroot}%{_qt6_plugindir}/org.kde.kdecoration3.kcm
rm -f %{buildroot}%{_datadir}/applications/kcm_*.desktop

%post
systemctl daemon-reload 2>/dev/null || true

%posttrans
echo
echo "KineticWE installed. Select 'KineticWE' at your display manager to start."
if [ ! -x %{_bindir}/kineticwe-setup-greeter ]; then
    echo "To install the Noctalia greeter, run: sudo dnf install kineticwe-greeter"
fi
echo

%postun
systemctl daemon-reload 2>/dev/null || true

%posttrans -n kineticwe-greeter
echo
echo "Run kineticwe-setup-greeter to configure the Noctalia greeter as your display manager."
echo

%files
%license LICENSES/* ../kglobalacceld/LICENSES/* ../kdecoration/LICENSES/* data/icon-themes/LICENSE
%doc README.md CONTRIBUTING.md
%{_bindir}/kinetic-we
%{_bindir}/kineticwe_windowprop
%{_bindir}/kinetic-we_wayland_wrapper
%{_bindir}/start-kineticwe
%{_userunitdir}/kineticwe-workspace.target
%{_userunitdir}/kineticwe-session.target
%{_libdir}/libkineticwe-globalacceld.so.*
%{_libdir}/libkineticwe-decoration.so.*
%{_libdir}/libkineticwe-decoration-private.so.*
%{_libdir}/libkineticwe.so.*
%{_qt6_plugindir}/kineticwe/
%{_qt6_plugindir}/kf6/packagestructure/kineticwe/
%{_qt6_plugindir}/org.kineticwe.decoration/
%{_qt6_qmldir}/org/kineticwe/
%{_libdir}/libexec/kineticwe*
%{_datadir}/applications/org.kineticwe.*.desktop
%{_datadir}/icons/hicolor/*/apps/kineticwe.*
%{_datadir}/wayland-sessions/kineticwe.desktop
%dir %{_datadir}/knotifications6/
%{_datadir}/qlogging-categories6/
%exclude %{_datadir}/qlogging-categories6/xdp-kwe.categories
%{_datadir}/kineticwe-wayland/
%{_datadir}/icons/Breeze-Round-Chameleon*
%{_datadir}/krunner/
%{_datadir}/locale/
%exclude %{_datadir}/locale/*/LC_MESSAGES/xdg-desktop-portal-kwe.mo
%{_userunitdir}/kineticwe.service
%dir %{_sysconfdir}/systemd/user/plasma-kglobalaccel.service.d/
%{_sysconfdir}/systemd/user/plasma-kglobalaccel.service.d/kineticwe-mask.conf

%files -n xdg-desktop-portal-kwe
%license portal/xdg-desktop-portal-kwe/LICENSES/*
%{_libdir}/libexec/xdg-desktop-portal-kwe
%{_datadir}/xdg-desktop-portal/portals/kwe.portal
%{_datadir}/xdg-desktop-portal/kineticwe-portals.conf
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.kwe.service
%{_datadir}/applications/org.freedesktop.impl.portal.desktop.kwe.desktop
%{_userunitdir}/plasma-xdg-desktop-portal-kwe.service
%{_datadir}/locale/*/LC_MESSAGES/xdg-desktop-portal-kwe.mo
%{_datadir}/qlogging-categories6/xdp-kwe.categories

%files -n kineticwe-noctalia
%license shell/noctalia/LICENSE
%{_bindir}/noctalia-kwe
%{_datadir}/noctalia/
%{_datadir}/applications/dev.noctalia.Noctalia.desktop
%{_datadir}/applications/dev.kineticwe.Settings.desktop
%{_datadir}/icons/hicolor/scalable/apps/noctalia.svg
%{_datadir}/icons/hicolor/512x512/apps/kineticwe-logo.png

%files -n kineticwe-greeter
%license ../noctalia-greeter/LICENSE
%{_bindir}/noctalia-greeter
%{_bindir}/noctalia-greeter-session
%{_bindir}/noctalia-greeter-apply-appearance
%{_bindir}/noctalia-greeter-compositor
%{_bindir}/noctalia-greeter-print-greetd-config
%{_bindir}/kineticwe-setup-greeter
%{_tmpfilesdir}/noctalia-greeter.conf
%{_datadir}/noctalia-greeter/
%{_datadir}/polkit-1/actions/org.noctalia.greeter.apply-appearance.policy

%changelog
* Sat Sep 26 2026 tofan79 <tofan79@users.noreply.github.com> - %{pkg_version}-1
- Deep source audit against docs/kineticwe-2.0.md's own "cut the cord to
  KDE" plan turned up one real regression: BuildRequires had
  plasma-activities-devel still in it, and %cmake never passed
  -DKWIN_BUILD_ACTIVITIES=OFF, so this package was silently building
  WITH Activities support (a hard runtime need on kactivitymanagerd) —
  exactly what Phase 6 of that doc says to drop. Removed the
  BuildRequires and added -DKWIN_BUILD_ACTIVITIES=OFF plus
  -DCMAKE_DISABLE_FIND_PACKAGE_PlasmaActivities=ON so this can't
  silently flip back on depending on what's in the buildroot.
- Added a missing Requires: libplasma — the desktopchangeosd effect's
  QML imports org.kde.plasma.core and nothing else in the dependency
  chain was pulling it in.
- Everything else audited (org.kde.plasmashell / org.kde.krunner /
  org.kde.kappmenu D-Bus calls scattered across effects and plugins,
  kglobalaccel calls) are optional best-effort integrations that
  degrade gracefully with no service present — consistent with the
  2.0 plan's "accepted drops" and not a hard dependency, so left as-is.
- Rename package kineticwe -> kineticwe-git to make clear this COPR build
  tracks upstream kineticwe-2.0 git HEAD daily, not a tagged release.
  Updated the self-referencing kineticwe-greeter Requires to match
  (now Requires: %{name} instead of a hardcoded old package name).
- Fixed the fetched Source3 (kineticwe.desktop): the workflow was pulling a
  stale pre-2.0 copy (DesktopNames=KDE) instead of the canonical
  scripts/kineticwe.desktop.in (DesktopNames=KineticWE), which is what the
  2.0 "hard cut" session identity in docs/kineticwe-2.0.md actually requires.
  Workflow now fetches the canonical .in template and substitutes
  @INSTALL_PREFIX@ itself before staging it as Source3.
- Workflow now also fetches start-kineticwe.sh from the canonical
  scripts/start-kineticwe.sh (KWE_REAL_CONFIG_HOME-based, matches
  docs/kineticwe-2.0.md Part 6) instead of the lgl-kineticwe-copr/ copy.

* Fri Sep 25 2026 tofan79 <tofan79@users.noreply.github.com> - %{pkg_version}-1
- Initial Mindset-Apps COPR build of the kineticwe-2.0 branch; version
  resolves to the latest upstream commit (date.git<short-SHA>) each day.

* Wed Sep 23 2026 LGL <lgl@localhost> - 0.0.1-10
- Search both KineticWE and KWin data namespaces when discovering desktop effects.
- Add json-devel as a build dependency for Kinetic Settings.
- Recommend kf6-qqc2-desktop-style for the KineticWE desktop session.

* Mon Sep 21 2026 LGL <lgl@localhost> - 0.0.1-7
- Remove nested rpm queries from posttrans scriptlets to avoid RPM database lock errors.
- Require matching main, Noctalia, portal, and installed greeter package releases.
- Rebuild from kineticwe-2.0 commit e010d44f81 (Preparing for kwe2 copr).
- Move Alacritty, qt5ct, qt6ct, and Spectacle to weak recommendations.
- Fix Noctalia greeter tmpfiles ownership to use greetd:greetd.
- Apply a packaging-time locale-domain patch so portal translations use
  xdg-desktop-portal-kwe without modifying the upstream source tree.
- Prevent the portal locale and logging-category files from being claimed by
  the main package or conflicting with stock KDE portal files.
- Include recent Kinetic Settings and default-keybind fixes.

* Sat Aug 15 2026 TheBlackDon <theblackdon@gitlab.com> - 6.7.80-17
- New subpackage: kineticwe-noctalia — the Noctalia fork shell, built
  in-tree from shell/noctalia (Phase 5 meson build, -Dtests=disabled) and
  shipped as the noctalia-kwe binary so it can coexist with an upstream
  noctalia install. Main package now Requires kineticwe-noctalia instead of
  Recommending noctalia-git / noctalia-shell-v5.
- Shell compositor detection treats the KineticWE desktop identity as KDE,
  so the workspace backend (org_kde_plasma_virtual_desktop) activates and
  the bar shows the virtual desktops.

* Sat Aug 15 2026 TheBlackDon <theblackdon@gitlab.com> - 6.7.80-16
- New subpackage: xdg-desktop-portal-kwe — rebranded fork of
  xdg-desktop-portal-kde (v6.7.4) exporting the session as KineticWE
  (org.freedesktop.impl.portal.desktop.kwe, UseIn=KineticWE,
  kineticwe-portals.conf [preferred] default=kwe). All stock interfaces
  kept (FileChooser, Screenshot, ScreenCast, Settings, GlobalShortcuts...).
  Main package now Requires xdg-desktop-portal-kwe instead of
  xdg-desktop-portal-kde; the KDE backend is never selected in KineticWE
  sessions.

* Sat Aug 08 2026 LGL <lgl@localhost> - 6.7.80-15
- Rebuild from latest master to pick up:
  - Expose live tiling layout state on the session bus at org.kde.KWin.Tiling
    /Tiling, so the Noctalia kineticwe-layouts bar plugin and other external
    consumers can read the active output's current layout, list enabled
    layouts, and request layout switches (setLayout/cycleLayout)

* Fri Aug 07 2026 LGL <lgl@localhost> - 6.7.80-14
- Rebuild from latest master to pick up:
  - Show current tiling layout in the desktop-switch on-screen display and
    in System Settings > Desktop Effects/Virtual Desktops

* Sat Aug 01 2026 LGL <lgl@localhost> - 6.7.80-13
- Rebuild from latest master to pick up:
  - kde-output-device-v2.xml cvt event fixed to since=24 (matching the
    interface version and the client-side plasma-wayland-protocols copy);
    the previous since=23 mismatch shifted event opcodes on the wire and
    crashed System Settings > Display & Monitor on open
  - KineticWE default global shortcuts for fresh installs (Window Close:
    Meta+Q, Overview: Meta+O, Tiling Toggle Floating: Meta+V, Swap Tiled
    Window: Meta+Shift+arrows, Switch to Desktop: Meta+N, NoctaliaWindow
    Switcher: Alt+Tab, several stale upstream defaults removed); registered
    via KGlobalAccel autoloading so existing user keybind configs are
    untouched
  - Fix wallpaper showing through in the Overview effect

* Wed Jul 29 2026 TheBlackDon <theblackdon@gitlab.com> - 6.7.80-12
- Work around a kconfig_compiler bug (KF6 <= 6.28, i.e. every released
  Fedora/Arch build) that misgenerates the RuleSettings mutator for the
  decorationpolicy window rule and fails to compile: store the setting as
  Int with explicit casts instead of the KWin::DecorationPolicy enum class;
  the Rules object API stays fully typed, only the KConfigXT storage layer
  changes. Revert once the buildroot's KConfig is >= 6.29.

* Wed Jul 29 2026 TheBlackDon <theblackdon@gitlab.com> - 6.7.80-11
- Ship the canonical scripts/start-kineticwe.sh from the source tree as the
  session launcher instead of the forked SOURCES/ copy: it runs kinetic-we
  in the background and waits on it instead of exec'ing with
  --exit-with-session, fixing logout stalling on a black screen instead of
  returning to the greeter (noctalia logout -> loginctl terminate-session)
- Session desktop entry now declares DesktopNames=KDE, matching the
  environment the launcher exports

- Rebuild from testing merge: ship the border color source fixes (live
  updates, ActiveOnly floating windows, system-surface skip) that the
  previous source snapshot predated, and exclude fullscreen/maximized
  windows from borders and corner radius

- Bundle kdecoration built from pinned KDE master commit d1304925: kwin-we
  now uses KDecoration3::Style (server-side drop shadows for CSD windows),
  which is not in the buildroot's kdecoration 6.7.x; Provides/Obsoletes
  kdecoration and kdecoration-devel like the bundled kglobalacceld runtime
- Pin kglobalacceld to master commit 5cc88399 instead of floating master so
  SRPM builds are reproducible

- Fix system surfaces (app launcher, logout menu, and other popup/overlay
  windows) incorrectly receiving a tiling border in ActiveOnly border mode
  when focused

* Wed Jul 22 2026 LGL <lgl@localhost> - 6.7.80-10
- Supervise noctalia in the session launcher: the shell is restarted after
  a crash or manual kill instead of tearing down the whole session, which
  now ends only when the login session itself is terminated
- Fix D-Bus/systemd-activated apps (e.g. Spectacle's shortcut) crashing on
  startup by exporting WAYLAND_DISPLAY and running
  dbus-update-activation-environment --systemd --all in the payload
- Export KDE_FULL_SESSION=true so System Settings resolves its dock icon
  instead of falling back to a generic one
- Add the "Columns" layout to the per-monitor/per-desktop override
  dropdowns, where it was missing since the layout was introduced

* Mon Jul 20 2026 LGL <lgl@localhost> - 6.7.80-9
- Fix New Columns layout window spawning and resizing issues
- Add gap-aware column width rebalancing to ColumnsLayoutEngine
- Sync start-kineticwe session launcher with upstream power management fix:
  look up upowerd/org_kde_powerdevil across Fedora/Arch/Debian libexec
  paths instead of a hardcoded Fedora-only path, export a WAYLAND_DISPLAY
  fallback so powerdevil doesn't abort at startup, and log their output to
  files instead of discarding it

* Wed Jul 15 2026 LGL <lgl@localhost> - 6.7.80-8
- Rebuild from latest master: adds the Columns tiling layout, the AutoGrid
  layout engine, and KCM shortcuts for swapping the focused window
  up/down/left/right
- Fix ghost window left behind on masterstack when a window is moved to a
  different monitor
- Fix autogrid layout windows floating when moved with the mouse
- Sync start-kineticwe session launcher with upstream start-kineticwe.sh
  fixes: correct QT_PLUGIN_PATH to include the qt6/plugins subdirectory
  (was missing it, so KWin's own plugins could fail to load on Fedora's
  Qt6 layout), export XDG_MENU_PREFIX=plasma- (fixes kbuildsycoca6/
  Application Picker breakage), stop clobbering LD_LIBRARY_PATH with a
  stale inherited value, and pass --exit-with-session to kinetic-we with
  noctalia running in the foreground so the session ends cleanly when
  noctalia exits instead of leaving kinetic-we running detached

* Mon Jul 06 2026 LGL <lgl@localhost> - 6.7.80-7
- Start upowerd and org_kde_powerdevil from the RPM session launcher so power
  management controls are available in KineticWE sessions
- Rebuild with the latest Noctalia/KDE settings integration, including
  Noctalia shortcut registration and Noctalia color source options in the
  Tiling System Settings module

* Mon Jul 06 2026 LGL <lgl@localhost> - 6.7.80-6
- Rebuild from latest master after README/COPR/AUR docs and Arch packaging
  metadata updates

* Sat Jul 04 2026 LGL <lgl@localhost> - 6.7.80-5
- Rebuild to pick up the latest KineticWE changes from master

* Fri Jul 03 2026 LGL <lgl@localhost> - 6.7.80-4
- Rebuild to pick up the Meta+Scroll / Meta+Alt+Scroll swap option
  (InvertScrollDesktopSwitch), which was already merged before build 3 but
  missing from it because lgl-kineticwe-copr/results/kineticwe-6.7.80.tar.gz
  was stale: the Makefile only regenerates that tarball when the file is
  absent, so builds 2 and 3 silently reused the June 28 source snapshot

* Thu Jul 02 2026 LGL <lgl@localhost> - 6.7.80-3
- Fix crash in CenterTileLayoutEngine::cancelMoveWindow: removing a leaf from
  its column list without removing the matching entry from the parallel
  weight list desynced the two, causing an out-of-bounds/empty-list read in
  reflow() on a later addWindow() (segfault in kwin_wayland, kicking the
  session back to the login screen)

* Tue Jun 30 2026 LGL <lgl@localhost> - 6.7.80-2
- Fix xdg-desktop-portal-kde launch: override XDG_CURRENT_DESKTOP=KDE for
  that process so ScreenCast/Screenshot/RemoteDesktop/Clipboard/
  GlobalShortcuts/InputCapture/Background/Wallpaper portals register
  (xdg-desktop-portal-kde requires an exact "KDE" match, not a colon list)
- Obsolete kglobalacceld-devel: it requires the exact-matching system
  kglobalacceld runtime, which kineticwe already replaces, so leaving it
  installed blocks the kineticwe transaction with an unresolvable conflict

* Sun Jun 28 2026 LGL <lgl@localhost> - 6.7.80-1
- Initial COPR package: KineticWE compositor with bundled kglobalacceld runtime
- Install RPM-safe session launcher and Wayland session desktop file
- Require Noctalia v5 from the lionheartp/Hyprland COPR package set
- Keep development outputs out of the runtime package
