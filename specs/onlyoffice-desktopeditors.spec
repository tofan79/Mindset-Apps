Name:           onlyoffice-desktopeditors
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        ONLYOFFICE Desktop Editors
License:        AGPL-3.0-only
URL:            https://www.onlyoffice.com/
Source0:        onlyoffice-desktopeditors.x86_64.rpm

# Pre-built binary repack (official RPM), skip RPATH and debuginfo checks
%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

BuildRequires:  cpio

Requires:       glibc
Requires:       gtk3
Requires:       libX11
Requires:       libXScrnSaver
Requires:       libnotify
Requires:       libstdc++ >= 4.8.0
Requires:       libxcb
Requires:       libxkbcommon-x11
Requires:       xcb-util-image
Requires:       xcb-util-keysyms
Requires:       xcb-util-renderutil
Requires:       xcb-util-wm
Requires:       xdg-utils
Requires:       curl
Requires:       atk
Requires:       boost-filesystem
Requires:       dejavu-sans-fonts
Requires:       dejavu-sans-mono-fonts
Requires:       dejavu-serif-fonts
Requires:       liberation-mono-fonts
Requires:       liberation-narrow-fonts
Requires:       liberation-sans-fonts
Requires:       liberation-serif-fonts

%description
ONLYOFFICE Desktop Editors is a free office suite for editing documents,
spreadsheets and presentations. It is compatible with Microsoft Office
formats (docx, xlsx, pptx) and supports collaborative editing.

This package is a repack of the official ONLYOFFICE binary RPM.

%prep

%build

%install
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot} > /dev/null 2>&1
rm -rf %{buildroot}/usr/lib/.build-id

%files
%defattr(-,root,root,-)
/opt/onlyoffice/
/usr/bin/desktopeditors
/usr/bin/onlyoffice-desktopeditors
/usr/share/applications/onlyoffice-desktopeditors.desktop
/usr/share/doc/onlyoffice-desktopeditors
/usr/share/icons/hicolor/*/apps/onlyoffice-desktopeditors.png
/usr/share/licenses/onlyoffice-desktopeditors

%changelog
* Sat Aug 08 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package (binary repack of official RPM)
