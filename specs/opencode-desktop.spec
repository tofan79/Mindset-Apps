Name:           opencode-desktop
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        opencode Desktop — GUI companion for the opencode AI coding agent
License:        Proprietary
URL:            https://opencode.ai
Source0:        opencode-desktop-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

Requires:       gtk3
Requires:       nss
Requires:       alsa-lib

%description
opencode Desktop is the graphical companion to the opencode CLI: a chat-first
developer tool that reads and edits files, runs commands, and searches the web
inside a desktop app.

%prep
%setup -q -n squashfs-root

%install
install -d %{buildroot}/opt/opencode-desktop
cp -r * %{buildroot}/opt/opencode-desktop/

install -d %{buildroot}%{_bindir}
ln -s /opt/opencode-desktop/AppRun %{buildroot}%{_bindir}/opencode-desktop

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/opencode-desktop.desktop << 'EOF'
[Desktop Entry]
Name=opencode Desktop
GenericName=AI Coding Agent
Comment=GUI for the opencode AI coding agent
Exec=/opt/opencode-desktop/AppRun
Icon=opencode-desktop
Terminal=false
Type=Application
Categories=Development;IDE;Utility;
StartupWMClass=opencode-desktop
EOF

%files
/opt/opencode-desktop/
%{_bindir}/opencode-desktop
%{_datadir}/applications/opencode-desktop.desktop

%changelog
* Thu Sep 17 2026 mindset <mindset@copr> - %{pkg_version}-1
- Auto-updated from upstream GitHub Releases