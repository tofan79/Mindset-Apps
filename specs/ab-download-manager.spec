Name:           ab-download-manager
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        AB Download Manager — Fast & powerful download manager
License:        Apache-2.0
URL:            https://abdownloadmanager.com
Source0:        ABDownloadManager_%{pkg_version}_linux_x64.tar.gz

# Pre-built binary, skip RPATH and debuginfo checks
%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

Requires:       glibc
Requires:       libX11
Requires:       libxcb
Requires:       gtk3

%description
AB Download Manager (ABDM) is a fast and powerful download manager
with advanced features like video downloading from websites and
browser integration.

%prep
%setup -q -c -n ABDownloadManager

%install
install -d %{buildroot}/opt/ab-download-manager
cp -r * %{buildroot}/opt/ab-download-manager/

install -d %{buildroot}%{_bindir}
ln -s /opt/ab-download-manager/bin/ABDownloadManager %{buildroot}%{_bindir}/abdownloadmanager

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/ab-download-manager.desktop << 'EOF'
[Desktop Entry]
Name=AB Download Manager
GenericName=Download Manager
Comment=Fast & powerful download manager
Exec=/opt/ab-download-manager/bin/ABDownloadManager %U
Icon=/opt/ab-download-manager/lib/ABDownloadManager.png
Terminal=false
Type=Application
Categories=Network;FileTransfer;
StartupNotify=true
EOF

%files
/opt/ab-download-manager/
%{_bindir}/abdownloadmanager
%{_datadir}/applications/ab-download-manager.desktop

%changelog
* Tue Aug 05 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package
