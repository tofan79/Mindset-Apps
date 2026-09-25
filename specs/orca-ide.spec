Name:           orca-ide
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Orca IDE — Multimodal AI-native code editor
License:        Proprietary
URL:            https://github.com/stablyai/orca
Source0:        orca-ide-%{version}.x86_64.rpm

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

BuildRequires:  cpio

Requires:       at-spi2-core
Requires:       gtk3
Requires:       libXScrnSaver
Requires:       libnotify
Requires:       libXtst
Requires:       libuuid
Requires:       nss
Requires:       python3
Requires:       python3-gobject
Requires:       xclip
Requires:       xdg-utils
Requires:       xdotool
Requires:       xorg-x11-server-Xvfb

%description
Orca IDE is an AI-native code editor built on multimodal perception. It takes
project context into account and makes edits across files, with support for
terminal, browser, and app UIs.

This package is a repack of the official Orca RPM.

%prep

%build

%install
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot} > /dev/null 2>&1
rm -rf %{buildroot}/usr/lib/.build-id
rm -f %{buildroot}%{_datadir}/applications/orca-ide.desktop

install -d %{buildroot}%{_bindir}
ln -s ../../opt/Orca/resources/bin/orca-ide %{buildroot}%{_bindir}/orca-ide

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/orca-ide.desktop << 'EOF'
[Desktop Entry]
Name=Orca IDE
GenericName=AI Code Editor
Comment=Multimodal AI-native code editor
Exec=/usr/bin/orca-ide %U
Icon=orca-ide
Terminal=false
Type=Application
Categories=Development;IDE;
StartupWMClass=orca
EOF

%post
[ -f /opt/Orca/chrome-sandbox ] && chmod 4755 /opt/Orca/chrome-sandbox || :

%files
%defattr(-,root,root,-)
/opt/Orca/
%{_bindir}/orca-ide
%{_datadir}/applications/orca-ide.desktop
%{_datadir}/icons/hicolor/*/apps/orca-ide.png

%changelog
* Fri Sep 25 2026 mindset <mindset@copr> - %{pkg_version}-1
- Repack the official Orca IDE RPM
