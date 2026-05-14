Name:           zen-browser
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Zen Browser — A calmer, privacy-focused browser
License:        MPL-2.0
URL:            https://zen-browser.app
Source0:        zen.linux-x86_64.tar.xz

# Pre-built binary, skip RPATH and debuginfo checks
%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

Requires:       gtk3
Requires:       dbus-glib
Requires:       libXt
Requires:       nss
Requires:       alsa-lib

%description
Zen Browser is a privacy-focused browser built on Firefox.
It offers a calmer browsing experience with a clean interface.

%prep
%setup -q -c -n zen

%install
install -d %{buildroot}/opt/zen-browser
cp -r . %{buildroot}/opt/zen-browser/

install -d %{buildroot}%{_bindir}
ln -s /opt/zen-browser/zen %{buildroot}%{_bindir}/zen-browser

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/zen-browser.desktop << 'EOF'
[Desktop Entry]
Name=Zen Browser
GenericName=Web Browser
Comment=A calmer, privacy-focused browser
Exec=/opt/zen-browser/zen %u
Icon=/opt/zen-browser/browser/chrome/icons/default/default128.png
Terminal=false
Type=Application
Categories=Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml+xml;x-scheme-handler/http;x-scheme-handler/https;
StartupNotify=true
StartupWMClass=zen-browser
EOF

%files
/opt/zen-browser/
%{_bindir}/zen-browser
%{_datadir}/applications/zen-browser.desktop

%changelog
* Wed May 14 2026 mindset <mindset@copr> - %{pkg_version}-1
- Auto-updated from upstream GitHub Releases
