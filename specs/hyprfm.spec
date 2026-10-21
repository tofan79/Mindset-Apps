Name:           hyprfm
Version:        %{pkg_version}
Release:        2%{?dist}
Summary:        Fast keyboard-friendly file manager for Hyprland
License:        MIT
URL:            https://github.com/soyeb-jim285/hyprfm
Source0:        %{name}-%{version}.tar.gz

# Sumber sekarang build dari tag upstream (CMake/Qt6), bukan repack AppImage.
# Quill dan quill-icons sudah disalin ke tarball oleh workflow pada commit
# submodule yang di-pin tag, jadi build tidak mengambil apa pun dari jaringan.
BuildRequires:  cmake >= 3.20
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtsvg-devel

BuildArch:      x86_64
AutoReqProv:    no

Requires:       qt6-qtbase
Requires:       qt6-qtdeclarative
Requires:       qt6-qtsvg
Requires:       qt6-qtwayland
Requires:       glib2%{?_isa}
Requires:       gvfs

%description
HyprFM is a Qt6/QML file manager designed to feel native on Hyprland.
Lightweight and built around fast keyboard navigation with Miller columns,
kinetic scrolling, drag and drop, async operations, rich previews, and a
TOML-based theme system.

Built from the upstream source tag; no AppImage or vendor binary is bundled.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_TESTS=OFF \
    -DHYPRFM_DATA_DIR=%{_datadir}/hyprfm
%cmake_build

%install
%cmake_install

# Salinan LICENSE submodule Quill identik dengan LICENSE utama; simpan satu
# saja supaya rpmlint tidak melaporkan file duplikat.
rm -f %{buildroot}%{_datadir}/hyprfm/src/qml/Quill/LICENSE

%files
%license LICENSE
%doc README.md
%{_bindir}/hyprfm
%{_datadir}/hyprfm/
%{_datadir}/applications/io.github.soyeb_jim285.HyprFM.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.soyeb_jim285.HyprFM.svg
%{_datadir}/metainfo/io.github.soyeb_jim285.HyprFM.metainfo.xml

%changelog
* Wed Oct 21 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-2
- Ganti repack AppImage dengan build source tag upstream: CMake + Qt6,
  Quill dan quill-icons dari commit submodule yang di-pin tag.
- Binary di /usr/bin, tema dan modul QML di /usr/share/hyprfm; desktop,
  ikon, dan metainfo dari dist/ upstream. Runtime manual tetap sama
  (qt6-qtbase/declarative/svg/wayland, glib2, gvfs).

* Wed Aug 26 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package from upstream AppImage
