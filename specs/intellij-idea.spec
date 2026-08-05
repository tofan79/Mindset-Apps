Name:           intellij-idea
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        IntelliJ IDEA — Leading Java and Kotlin IDE (unified)
License:        Apache-2.0
URL:            https://www.jetbrains.com/idea/
Source0:        idea-%{pkg_version}.tar.gz

# Pre-built binary
%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

Requires:       java-25-openjdk
Requires:       glib2
Requires:       libXtst
Requires:       libxcb
Requires:       libX11

%description
Unified IntelliJ IDEA — replaces the separate Community Edition and
Ultimate distributions since 2025.3. Core Java/Kotlin features are free
for everyone; extended tooling is unlocked via an Ultimate subscription.

%prep
%setup -q -c -T
%{__tar} -xf %{SOURCE0} -C . --strip-components=1

%install
install -d %{buildroot}/opt/intellij-idea
cp -r . %{buildroot}/opt/intellij-idea/

install -d %{buildroot}%{_bindir}
ln -s /opt/intellij-idea/bin/idea %{buildroot}%{_bindir}/idea

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/intellij-idea.desktop << 'EOF'
[Desktop Entry]
Name=IntelliJ IDEA
Comment=IntelliJ IDEA — Java and Kotlin IDE
Exec=/opt/intellij-idea/bin/idea %f
Icon=/opt/intellij-idea/bin/idea.png
Terminal=false
Type=Application
Categories=Development;IDE;
StartupNotify=true
StartupWMClass=jetbrains-idea
EOF

install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp bin/idea.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/intellij-idea.svg 2>/dev/null || true

%files
/opt/intellij-idea/
%{_bindir}/idea
%{_datadir}/applications/intellij-idea.desktop
%{_datadir}/icons/hicolor/scalable/apps/intellij-idea.svg

%changelog
* Wed Aug 05 2026 mindset <mindset@copr> - %{pkg_version}-1
- Rename to unified IntelliJ IDEA (Community Edition discontinued since 2025.3)
