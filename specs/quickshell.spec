%global commit 4b4fca3224ab977dc515ac0bb78d00b3dfa71e00
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global build_timestamp %(date +"20260522")
%global rel_build 6.git.%{build_timestamp}.%{shortcommit}%{?dist}

%bcond_with         asan

Name:               quickshell
Version:            0.3.0
Release:            %{rel_build}
Summary:            Flexible QtQuick based desktop shell toolkit

License:            LGPL-3.0-only AND GPL-3.0-only
URL:                https://github.com/quickshell-mirror/quickshell
Source0:            %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:      cmake
BuildRequires:      cmake(Qt6Core)
BuildRequires:      cmake(Qt6DBus)
BuildRequires:      cmake(Qt6Qml)
BuildRequires:      cmake(Qt6ShaderTools)
BuildRequires:      cmake(Qt6WaylandClient)
BuildRequires:      gcc-c++
BuildRequires:      git
BuildRequires:      ninja-build
BuildRequires:      pkgconfig(CLI11)
BuildRequires:      pkgconfig(gbm)
BuildRequires:      pkgconfig(jemalloc)
BuildRequires:      pkgconfig(libdrm)
BuildRequires:      pkgconfig(libpipewire-0.3)
BuildRequires:      pkgconfig(libunwind-generic)
BuildRequires:      pkgconfig(pam)
BuildRequires:      pkgconfig(polkit-agent-1)
BuildRequires:      pkgconfig(wayland-client)
BuildRequires:      pkgconfig(wayland-protocols)
BuildRequires:      qt6-qtbase-private-devel
BuildRequires:      spirv-tools

%if %{with asan}
BuildRequires:      libasan
%endif

Provides:           desktop-notification-daemon
Provides:           bundled(cpptrace) = 1.0.4
Conflicts:          noctalia-qs
Obsoletes:          quickshell < %{version}-%{release}

%description
Flexible toolkit for making desktop shells with QtQuick, targeting
Wayland and X11.
Built with full features: Network (NetworkManager), Bluetooth, PipeWire, etc.

%prep
%autosetup -n %{name}-%{commit}

%build
%cmake  -GNinja \
%if %{with asan}
        -DASAN=ON \
%endif
        -DBUILD_SHARED_LIBS=ON \
        -DCMAKE_BUILD_TYPE=Release \
        -DDISTRIBUTOR="Mindset-Apps COPR" \
        -DGIT_REVISION=%{commit} \
        -DINSTALL_QML_PREFIX=%{_lib}/qt6/qml \
        -DVENDOR_CPPTRACE=ON \
        -DNETWORK=ON \
        -DBLUETOOTH=ON \
        -DSERVICE_PIPEWIRE=ON \
        -DSERVICE_MPRIS=ON \
        -DSERVICE_POLKIT=ON \
        -DSERVICE_UPOWER=ON \
        -DSERVICE_NOTIFICATIONS=ON \
        -DWAYLAND=ON \
        -DWAYLAND_WLR_LAYERSHELL=ON \
        -DWLR_LAYERSHELL=ON \
        -DX11=ON
%cmake_build

%install
%cmake_install

# VENDOR_CPPTRACE=ON bundles cpptrace + dwarf + zstd
# Remove all bundled dev artifacts — only ship needed shared libs
rm -rf %{buildroot}%{_includedir}/cpptrace
rm -rf %{buildroot}%{_includedir}/ctrace
rm -rf %{buildroot}%{_includedir}/{dwarf.h,libdwarf.h,zstd.h,zdict.h,zstd_errors.h}
rm -rf %{buildroot}%{_libdir}/libdwarf*
rm -rf %{buildroot}%{_libdir}/libzstd*
rm -rf %{buildroot}%{_libdir}/cmake
rm -rf %{buildroot}%{_libdir}/pkgconfig
rm -rf %{buildroot}%{_datadir}/cpptrace
rm -rf %{buildroot}%{_debuginfodir}

%files
%license LICENSE
%license LICENSE-GPL
%doc BUILD.md
%doc CONTRIBUTING.md
%doc README.md
%{_bindir}/qs
%{_bindir}/quickshell
%{_datadir}/applications/org.quickshell.desktop
%{_datadir}/icons/hicolor/scalable/apps/org.quickshell.svg
%{_libdir}/qt6/qml/Quickshell
%{_libdir}/libcpptrace.so*

%changelog
* Sat May 30 2026 mindset <mindset@copr> - %{version}-%{release}
- Initial Mindset-Apps build with full features (NETWORK=ON, BUILD_SHARED_LIBS=ON)
