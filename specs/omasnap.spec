Name:           omasnap
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Native Wayland screenshot and annotation editor

# Hindari kegagalan debugsourcefiles.list kosong di COPR.
%global debug_package %{nil}

License:        MIT
URL:            https://github.com/omacom/omasnap
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cmake >= 3.24
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  qt6-qtbase-devel
BuildRequires:  layer-shell-qt-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  libdeflate-devel

# Omnipresent (binary via exec / runtime).
Requires:       layer-shell-qt
Requires:       qt6-qtbase-gui
Requires:       hicolor-icon-theme
Requires:       wl-clipboard
Requires:       tesseract
# OCR bahasa Inggris sebagai default; tesseract-data-eng.
Recommends:     tesseract-langpack-eng
Recommends:     xdg-utils

%description
Omasnap is a native Wayland screenshot and annotation overlay: smart selection
(region, window, fullscreen, scroll), vector annotation, layer recrop, OCR, a
recents shelf, floating pins, and native-pixel export on fractional scales. It
targets Hyprland and captures the monitor in-process before mapping its layer.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -G Ninja
%cmake_build

%install
%cmake_install

%post
update-desktop-database -q >/dev/null 2>&1 || :

%postun
update-desktop-database -q >/dev/null 2>&1 || :

%files
%license %{_datadir}/licenses/omasnap/*.txt
%{_bindir}/omasnap
%{_datadir}/applications/omasnap.desktop

%changelog
* Tue Nov 10 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR build from upstream release tag
