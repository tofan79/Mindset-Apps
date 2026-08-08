Name:           heroic-launcher
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        An Open Source Launcher for GOG, Epic Games and Amazon Games
License:        GPL-3.0-only
URL:            https://heroicgameslauncher.com/
Source0:        Heroic-%{pkg_version}-linux-x86_64.rpm

# Pre-built binary repack (official RPM), skip RPATH and debuginfo checks
%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

BuildRequires:  cpio

Requires:       at-spi2-core
Requires:       gtk3
Requires:       libXScrnSaver
Requires:       libXtst
Requires:       libnotify
Requires:       libuuid
Requires:       nss
Requires:       xdg-utils

%description
Heroic Games Launcher is an open source launcher for GOG, Epic Games and
Amazon Games, based on legendary and gogdl. It lets you download, play and
manage games from your Epic, GOG and Amazon Prime Gaming libraries on Linux.

This package is a repack of the official Heroic Games Launcher binary RPM.

%prep

%build

%install
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot} > /dev/null 2>&1
rm -rf %{buildroot}/usr/lib/.build-id

%files
%defattr(-,root,root,-)
/opt/Heroic/
/usr/share/applications/heroic.desktop
/usr/share/icons/hicolor/*/apps/heroic.png

%changelog
* Sat Aug 08 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package (binary repack of official RPM)
