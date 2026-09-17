Name:           orca-desktop
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Orca — Multimodal AI-native code editor
License:        Proprietary
URL:            https://github.com/stablyai/orca
Source0:        orca-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

Requires:       gtk3
Requires:       nss
Requires:       alsa-lib

%description
Orca is an AI-native code editor built on multimodal perception. It takes
project context into account and makes edits across files, with support for
terminal, browser, and app UIs.

%prep
%setup -q -n squashfs-root

%install
install -d %{buildroot}/opt/orca-desktop
cp -r * %{buildroot}/opt/orca-desktop/

install -d %{buildroot}%{_bindir}
ln -s /opt/orca-desktop/AppRun %{buildroot}%{_bindir}/orca-desktop

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/orca-desktop.desktop << 'EOF'
[Desktop Entry]
Name=Orca Desktop
GenericName=AI Code Editor
Comment=Multimodal AI-native code editor
Exec=/opt/orca-desktop/AppRun %U
Icon=orca-desktop
Terminal=false
Type=Application
Categories=Development;IDE;
StartupWMClass=orca-desktop
EOF

%files
/opt/orca-desktop/
%{_bindir}/orca-desktop
%{_datadir}/applications/orca-desktop.desktop

%changelog
* Thu Sep 17 2026 mindset <mindset@copr> - %{pkg_version}-1
- Renamed to orca-desktop to avoid clashing with Fedora's orca (screen reader)