Name:           jetbrains-toolbox
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Manage all your JetBrains Projects and Tools
License:        custom
URL:            https://www.jetbrains.com/toolbox/
Source0:        jetbrains-toolbox-%{pkg_version}.tar.gz

# Pre-built binary
%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

Requires:       fuse
Requires:       glib2
Requires:       libxslt
Requires:       libXScrnSaver
Requires:       nss
Requires:       xcb-util-keysyms

%description
Manage all your JetBrains Projects and Tools.

%prep
%setup -q -c -n jetbrains-toolbox

%install
install -d %{buildroot}/opt/jetbrains-toolbox
cp -r jetbrains-toolbox-*/. %{buildroot}/opt/jetbrains-toolbox/

install -d %{buildroot}%{_bindir}
ln -s /opt/jetbrains-toolbox/jetbrains-toolbox %{buildroot}%{_bindir}/jetbrains-toolbox

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/jetbrains-toolbox.desktop << 'EOF'
[Desktop Entry]
Name=JetBrains Toolbox
Comment=Manage all your JetBrains Projects and Tools
Exec=/opt/jetbrains-toolbox/jetbrains-toolbox
Icon=jetbrains-toolbox
Terminal=false
Type=Application
Categories=Development;IDE;
StartupNotify=true
StartupWMClass=jetbrains-toolbox
EOF

%files
/opt/jetbrains-toolbox/
%{_bindir}/jetbrains-toolbox
%{_datadir}/applications/jetbrains-toolbox.desktop

%changelog
* Thu May 14 2026 mindset <mindset@copr> - %{pkg_version}-1
- Auto-updated from upstream
