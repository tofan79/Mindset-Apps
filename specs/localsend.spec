Name:           localsend
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        LocalSend — Share files to nearby devices, no internet needed
License:        MIT
URL:            https://localsend.org
Source0:        LocalSend-%{version}-linux-x86-64.tar.gz

BuildArch:      x86_64
AutoReqProv:    no

Requires:       gtk3
Requires:       libayatana-appindicator3

%description
LocalSend is an open-source cross-platform app to share files
and messages to nearby devices over your local network.
No internet required, no external servers.

%prep
%setup -q -c -n localsend

%install
install -d %{buildroot}/opt/localsend
cp -r * %{buildroot}/opt/localsend/

install -d %{buildroot}%{_bindir}
ln -s /opt/localsend/localsend_app %{buildroot}%{_bindir}/localsend

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/localsend.desktop << 'EOF'
[Desktop Entry]
Name=LocalSend
GenericName=File Sharing
Comment=Share files to nearby devices over local network
Exec=/opt/localsend/localsend_app
Icon=/opt/localsend/data/flutter_assets/assets/img/logo-512.png
Terminal=false
Type=Application
Categories=Network;FileTransfer;
StartupNotify=true
EOF

%files
/opt/localsend/
%{_bindir}/localsend
%{_datadir}/applications/localsend.desktop

%changelog
* Wed May 14 2026 mindset <mindset@copr> - %{pkg_version}-1
- Auto-updated from upstream GitHub Releases
