# arroxy: video downloader Electron (GPL-3.0), upstream only publishes AppImage and tar.gz.
#
# Repack AppImage: unpack squashfs-root into /opt/arroxy. The wrapper loads
# the bundled X11 libs shipped under usr/lib, just like AppRun does.

Name:           arroxy
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Free video downloader for YouTube and 2000+ other sites

License:        GPL-3.0-or-later
URL:            https://github.com/antonio-orionus/Arroxy
Source0:        arroxy-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

# Upstream only ships an x86_64 AppImage.
ExclusiveArch:  x86_64

# The bundle ships part of its own dependency set under /opt/arroxy/usr/lib,
# so automatic soname detection is not reliable.
AutoReqProv:    no

Requires:       gtk3
Requires:       nss
Requires:       (xdg-utils or xdg-desktop-portal)

%description
Arroxy is a free, open-source video downloader for YouTube and 2000+ other
sites, with a built-in browser for sites that need a sign-in. Features include
a queue with pause / resume / cancel, playlists, subtitles, and a built-in
media converter driven by ffmpeg.

This package repacks the upstream x86_64 AppImage; nothing is rebuilt locally.

%prep
%setup -q -n squashfs-root

%install
install -d %{buildroot}/opt/arroxy
cp -a . %{buildroot}/opt/arroxy/

install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/arroxy << 'EOF'
#!/bin/sh
# Prefer the libraries bundled with the AppImage, just like AppRun.
LD_LIBRARY_PATH="/opt/arroxy/usr/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec /opt/arroxy/arroxy "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/arroxy

install -Dpm0644 usr/share/icons/hicolor/1123x1123/apps/arroxy.png \
    %{buildroot}%{_datadir}/icons/hicolor/1123x1123/apps/arroxy.png

# Install upstream desktop entry with a corrected Exec line and keep the
# Arroxy icon name used in hicolor above.
install -d %{buildroot}%{_datadir}/applications
sed -e 's|^Exec=.*|Exec=/usr/bin/arroxy %U|' arroxy.desktop \
    > %{buildroot}%{_datadir}/applications/arroxy.desktop

install -Dpm0644 resources/THIRD_PARTY_NOTICES.txt \
    %{buildroot}%{_licensedir}/arroxy/THIRD_PARTY_NOTICES.txt

%files
%license %{_licensedir}/arroxy/THIRD_PARTY_NOTICES.txt
/opt/arroxy/
%{_bindir}/arroxy
%{_datadir}/applications/arroxy.desktop
%{_datadir}/icons/hicolor/1123x1123/apps/arroxy.png

%changelog
* Tue Nov 03 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package from the upstream AppImage