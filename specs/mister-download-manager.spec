# Build dari tag hulu, bukan repack biner rilis. Fedora 45 membawa Rust 1.99
# (Cargo.toml MDM butuh >= 1.98), jadi cargo/rust dari distro cukup.
# Empat biner dibangun: GUI, native-messaging host, CLI, dan server MCP.
# Extension browser dan manifest native-messaging dibuat di sini supaya tidak
# bergantung pada PowerShell (pack.ps1) atau artefak biner rilis.

Name:           mister-download-manager
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Free download manager with torrent, video grabber and browser integration
License:        GPL-3.0-or-later
URL:            https://github.com/anefzaoui/misterdownloadmanager
Source0:        https://github.com/anefzaoui/misterdownloadmanager/archive/v%{version}/misterdownloadmanager-%{version}.tar.gz
ExclusiveArch:  x86_64

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildRequires:  cargo
BuildRequires:  rust >= 1.98
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  pkgconfig
BuildRequires:  gtk3-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libX11-devel
BuildRequires:  python3-pillow
BuildRequires:  zip
BuildRequires:  desktop-file-utils

Requires:       ca-certificates
Requires:       gtk3
Requires:       libxkbcommon
Requires:       libxkbcommon-x11
Requires:       mesa-libEGL
Requires:       mesa-libGL

%description
Mister Download Manager (MDM) speeds files up with parallel connections,
resumes broken downloads, catches browser downloads, and also handles
torrents, videos, galleries and debrid links. This package builds the four
upstream binaries from the release tag and ships the Chromium/Firefox
extension plus the native-messaging manifests for browser integration.

%prep
%autosetup -n misterdownloadmanager-%{version}

%build
cargo build --release --locked -p mdm-app -p mdm-nmhost -p mdm-cli -p mdm-mcp

%install
rm -rf %{buildroot}

install -Dpm755 target/release/misterdownloadmanager        %{buildroot}%{_bindir}/misterdownloadmanager
install -Dpm755 target/release/misterdownloadmanager-nmhost %{buildroot}%{_bindir}/misterdownloadmanager-nmhost
install -Dpm755 target/release/misterdownloadmanager-cli    %{buildroot}%{_bindir}/misterdownloadmanager-cli
install -Dpm755 target/release/misterdownloadmanager-mcp    %{buildroot}%{_bindir}/misterdownloadmanager-mcp

# Menu entry (sama dengan yang dipakai upstream di .rpm/.deb).
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/misterdownloadmanager.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=Mister Download Manager
Comment=Download manager
Exec=misterdownloadmanager %U
Icon=misterdownloadmanager
Terminal=false
Categories=Network;FileTransfer;
StartupWMClass=misterdownloadmanager
MimeType=x-scheme-handler/magnet;application/x-bittorrent;
EOF
desktop-file-validate %{buildroot}%{_datadir}/applications/misterdownloadmanager.desktop

# Ikon 256x256, sama seperti hasil build-linux.sh upstream.
install -d %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
python3 -c 'from PIL import Image; import sys; Image.open(sys.argv[1]).convert("RGBA").resize((256, 256), Image.LANCZOS).save(sys.argv[2])' \
    'art/Mister Download Manager.png' \
    %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/misterdownloadmanager.png

# Extension Chromium: salin sumber extension/ dan isi versi dari tag (pack.ps1
# melakukan hal yang sama, tanpa PowerShell di sini).
EXT=%{buildroot}%{_datadir}/%{name}/extension-chromium
install -d "$EXT"
for f in background.js video.js page.js popup.html popup.css popup.js; do
    install -pm644 "extension/$f" "$EXT/$f"
done
cp -a extension/icons "$EXT/icons"
cp -a extension/_locales "$EXT/_locales"
sed -E 's/("version"[[:space:]]*:[[:space:]]*)"[^"]*"/\1"%{version}"/' \
    extension/manifest.json > "$EXT/manifest.json"

# Firefox .xpi dari manifest.firefox.json (Firefox memakai locale "nb").
FX=$(mktemp -d)
for f in background.js video.js page.js popup.html popup.css popup.js; do
    install -pm644 "extension/$f" "$FX/$f"
done
cp -a extension/icons "$FX/icons"
cp -a extension/_locales "$FX/_locales"
[ -d "$FX/_locales/no" ] && cp -a "$FX/_locales/no" "$FX/_locales/nb"
sed -E 's/("version"[[:space:]]*:[[:space:]]*)"[^"]*"/\1"%{version}"/' \
    extension/manifest.firefox.json > "$FX/manifest.json"
install -d %{buildroot}%{_datadir}/%{name}
(cd "$FX" && zip -q -r "%{buildroot}%{_datadir}/%{name}/mdm-firefox.xpi" .)
rm -rf "$FX"

# Manifest native messaging untuk Chrome/Chromium/Edge/Firefox. Binary yang
# baru saja dibangun akan menuliskan path absolut /usr/bin/...-nmhost.
%{buildroot}%{_bindir}/misterdownloadmanager-nmhost --package-manifests %{buildroot}

%files
%license LICENSE
%doc ATTRIBUTION.md
%{_bindir}/misterdownloadmanager
%{_bindir}/misterdownloadmanager-nmhost
%{_bindir}/misterdownloadmanager-cli
%{_bindir}/misterdownloadmanager-mcp
%{_datadir}/applications/misterdownloadmanager.desktop
%{_datadir}/icons/hicolor/256x256/apps/misterdownloadmanager.png
%{_datadir}/%{name}/

%dir /etc/opt/chrome/native-messaging-hosts
/etc/opt/chrome/native-messaging-hosts/com.misterdownloadmanager.host.json
%dir /etc/chromium/native-messaging-hosts
/etc/chromium/native-messaging-hosts/com.misterdownloadmanager.host.json
%dir /etc/opt/edge/native-messaging-hosts
/etc/opt/edge/native-messaging-hosts/com.misterdownloadmanager.host.json
%dir %{_prefix}/lib/mozilla/native-messaging-hosts
%{_prefix}/lib/mozilla/native-messaging-hosts/com.misterdownloadmanager.host.json
%dir %{_prefix}/lib64/mozilla/native-messaging-hosts
%{_prefix}/lib64/mozilla/native-messaging-hosts/com.misterdownloadmanager.host.json

%changelog
* Tue Nov 17 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial COPR package: build dari tag v%{version} dengan cargo/rust Fedora.
- Bangun GUI, CLI, MCP, dan native-messaging host dari sumber.
- Hasilkan extension Chromium/Firefox dan manifest browser tanpa PowerShell.
