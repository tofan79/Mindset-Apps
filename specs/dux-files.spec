# dux-files: File manager berbasis Go + Quickshell (Wayland, GNOME/GTK/Qt integration).

%global debug_package %{nil}

Name:           dux-files
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        A fast, keyboard-first file manager for Wayland
License:        MIT
URL:            https://github.com/duxlabs-dev/dux-files
Source0:        dux-files-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  golang

# Runtime optional yang sangat disarankan tetap di Require supaya fitur dasar
# (mini thumbnail, navigator, trash/device/network) bekerja tanpa fallback.
Requires:       quickshell
Requires:       gvfs
Requires:       poppler
Requires:       ffmpegthumbnailer
Requires:       udisks2

%description
Dux Files adalah file manager Wayland berbasis Go daemon + Quickshell, dengan
tab, dual pane, pencarian, bookmark, trash, mount device, arsip, network
share, reveal-in-file-manager, dan integrasi desktop portal. Paket ini
menggunakan tarball release tagged upstream.

%prep
%autosetup -n dux-files-%{version}

%build
%make_build

%install
%make_install PREFIX=%{_prefix}

%files
%license LICENSE
%doc README.md
%{_bindir}/dfiles
%{_datadir}/applications/dev.duxlabs.files.desktop
%{_datadir}/dbus-1/services/dev.duxlabs.files.FileManager1.service
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.dfiles.service
%{_datadir}/icons/hicolor/scalable/apps/dev.duxlabs.files.svg
%{_datadir}/metainfo/dev.duxlabs.files.metainfo.xml
%{_datadir}/polkit-1/actions/dev.duxlabs.files.policy
%{_datadir}/xdg-desktop-portal/portals/dfiles.portal

%changelog
* Sat Oct 31 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial packaging of dux-files from upstream tagged release.