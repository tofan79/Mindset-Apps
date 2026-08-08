Name:           zoom
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Zoom Workplace — video conferencing, team chat and collaboration
License:        Proprietary
URL:            https://zoom.us/
Source0:        zoom_x86_64.rpm

# Pre-built binary repack (official RPM), skip RPATH and debuginfo checks
%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

BuildRequires:  cpio

Requires:       freetype >= 2.6
Requires:       glibc
Requires:       gtk3
Requires:       ibus
Requires:       ibus-m17n
Requires:       libX11
Requires:       libXScrnSaver
Requires:       libXcomposite
Requires:       libXfixes
Requires:       libXrender
Requires:       libXtst
Requires:       libxcb
Requires:       libxkbcommon-x11
Requires:       libxslt
Requires:       mesa-dri-drivers
Requires:       mesa-libEGL
Requires:       mesa-libGL
Requires:       mesa-libgbm
Requires:       nss >= 3.22
Requires:       pulseaudio-libs
Requires:       sqlite-libs
Requires:       alsa-lib
Requires:       libdrm
Requires:       dbus-libs

%description
Zoom Workplace is an AI-first, open collaboration platform that combines team
chat, meetings, phone, whiteboard, calendar, mail, docs, and more. Use Zoom
Workplace for Linux with any free or paid Zoom license.

This package is a repack of the official Zoom binary RPM.

%prep

%build

%install
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot} > /dev/null 2>&1
rm -rf %{buildroot}/usr/lib/.build-id

%files
%defattr(-,root,root,-)
/opt/zoom/
/usr/bin/zoom
/usr/share/applications/Zoom.desktop
/usr/share/doc/zoom
/usr/share/mime/packages/zoom.xml
/usr/share/pixmaps/Zoom.png
/usr/share/pixmaps/application-x-zoom.png

%changelog
* Sat Aug 08 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package (binary repack of official RPM)
