Name:           hyprfm
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        HyprFM — A fast, keyboard-friendly file manager for Hyprland
License:        MIT
URL:            https://github.com/soyeb-jim285/hyprfm
Source0:        hyprfm-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

Requires:       qt6-qtbase
Requires:       qt6-qtdeclarative
Requires:       qt6-qtsvg
Requires:       qt6-qtwayland
Requires:       glib2
Requires:       gvfs

%description
HyprFM is a Qt6/QML file manager designed to feel native on Hyprland.
Lightweight, themeable, and built around fast keyboard navigation with
Miller columns, kinetic scrolling, drag & drop, async operations,
rich previews, and a TOML-based theme system.

%prep
%setup -q -n squashfs-root

%install
install -d %{buildroot}/opt/hyprfm
cp -r * %{buildroot}/opt/hyprfm/

install -d %{buildroot}%{_bindir}
ln -s /opt/hyprfm/AppRun %{buildroot}%{_bindir}/hyprfm

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/hyprfm.desktop << 'EOF'
[Desktop Entry]
Name=HyprFM
GenericName=File Manager
Comment=Fast, keyboard-friendly file manager for Hyprland
Exec=/opt/hyprfm/AppRun %U
Icon=hyprfm
Terminal=false
Type=Application
Categories=System;FileTools;FileManager;
MimeType=inode/directory;
StartupNotify=true
EOF

%files
/opt/hyprfm/
%{_bindir}/hyprfm
%{_datadir}/applications/hyprfm.desktop

%changelog
* Wed Aug 26 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package from upstream AppImage
