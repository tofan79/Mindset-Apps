Name:           zed
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Zed — A high-performance, multiplayer code editor
License:        GPL-3.0
URL:            https://zed.dev
Source0:        zed-linux-x86_64.tar.gz

# Pre-built binary
%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

Requires:       libxcb
Requires:       libX11
Requires:       libXcursor
Requires:       libXfixes

%description
Zed is a high-performance, multiplayer code editor.

%prep
%setup -q -c -n zed

%install
install -d %{buildroot}/opt/zed
cp -r zed/* %{buildroot}/opt/zed/

install -d %{buildroot}%{_bindir}
ln -s /opt/zed/bin/zed %{buildroot}%{_bindir}/zed

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/zed.desktop << 'EOF'
[Desktop Entry]
Name=Zed
Comment=High-performance, multiplayer code editor
Exec=/opt/zed/bin/zed %F
Icon=zed
Terminal=false
Type=Application
Categories=Development;IDE;
StartupNotify=true
StartupWMClass=zed
MimeType=text/plain;
EOF

%files
/opt/zed/
%{_bindir}/zed
%{_datadir}/applications/zed.desktop

%changelog
* Thu May 14 2026 mindset <mindset@copr> - %{pkg_version}-1
- Auto-updated from upstream GitHub Releases
