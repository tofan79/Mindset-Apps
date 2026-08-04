Name:           intellij-idea-community
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        IntelliJ IDEA Community Edition — Leading Java and Kotlin IDE
License:        Apache-2.0
URL:            https://www.jetbrains.com/idea/
Source0:        ideaIC-%{pkg_version}.tar.gz

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
The Community Edition is the open source version of IntelliJ IDEA,
a premier IDE for Java, Kotlin, and other languages.

%prep
%setup -q -c -T
%{__tar} -xf %{SOURCE0} -C . --strip-components=1

%install
install -d %{buildroot}/opt/intellij-idea-community
cp -r . %{buildroot}/opt/intellij-idea-community/

install -d %{buildroot}%{_bindir}
ln -s /opt/intellij-idea-community/bin/idea %{buildroot}%{_bindir}/idea

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/intellij-idea-community.desktop << 'EOF'
[Desktop Entry]
Name=IntelliJ IDEA Community
Comment=IntelliJ IDEA Community Edition — Java and Kotlin IDE
Exec=/opt/intellij-idea-community/bin/idea %f
Icon=/opt/intellij-idea-community/bin/idea.png
Terminal=false
Type=Application
Categories=Development;IDE;
StartupNotify=true
StartupWMClass=jetbrains-idea-ce
EOF

install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp bin/idea.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/intellij-idea-community.svg 2>/dev/null || true

%files
/opt/intellij-idea-community/
%{_bindir}/idea
%{_datadir}/applications/intellij-idea-community.desktop
%{_datadir}/icons/hicolor/scalable/apps/intellij-idea-community.svg

%changelog
* Tue Aug 05 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package
