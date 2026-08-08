Name:           android-studio
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Android Studio — The official Android IDE
License:        Apache-2.0
URL:            https://developer.android.com/studio
Source0:        android-studio-%{pkg_version}-linux.tar.gz

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
Android Studio is the official IDE for Android application development,
based on IntelliJ IDEA.

%prep
%setup -q -c -T
%{__tar} -xf %{SOURCE0} -C . --strip-components=1

%install
install -d %{buildroot}/opt/android-studio
cp -r . %{buildroot}/opt/android-studio/

install -d %{buildroot}%{_bindir}
ln -s /opt/android-studio/bin/studio %{buildroot}%{_bindir}/android-studio

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/android-studio.desktop << 'EOF'
[Desktop Entry]
Name=Android Studio
Comment=Android Studio — The official Android IDE
Exec=/opt/android-studio/bin/studio %f
Icon=/opt/android-studio/bin/studio.png
Terminal=false
Type=Application
Categories=Development;IDE;
StartupNotify=true
StartupWMClass=jetbrains-studio
EOF

install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
cp bin/studio.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/android-studio.svg 2>/dev/null || true

%files
/opt/android-studio/
%{_bindir}/android-studio
%{_datadir}/applications/android-studio.desktop
%{_datadir}/icons/hicolor/scalable/apps/android-studio.svg

%changelog
* Tue Aug 05 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package
