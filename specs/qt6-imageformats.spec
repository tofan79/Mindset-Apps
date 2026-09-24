Name:           qt6-imageformats
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Additional plugins for Qt 6 (WebP, TIFF, MNG image formats)

License:        LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only OR LicenseRef-Qt-Commercial
URL:            https://code.qt.io/cgit/qt/qtimageformats.git/
# Version dipasangkan dengan qt6-qtbase di base image (saat ini 6.11.2)
Source0:        https://github.com/qt/qtimageformats/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  qt6-rpm-macros
BuildRequires:  qt6-qtbase-devel
BuildRequires:  libwebp-devel
BuildRequires:  libtiff-devel
BuildRequires:  libmng-devel

%description
The Qt 6 ImageFormats module provides additional image format plugins for
Qt 6 applications: WebP, TIFF, and MNG. Required by Qt/QML applications
(e.g. Quickshell, Hyprfm) to display OMA-style themes whose wallpaper and
preview assets ship in WebP format.

%prep
%setup -q -n qtimageformats-%{version}

%build
%cmake_qt6
%cmake_build

%install
%cmake_install

%files
%{_libdir}/qt6/plugins/imageformats/*.so
%license LICENSES/LGPL-3.0-only.txt
%license LICENSES/GPL-2.0-only.txt
%license LICENSES/GPL-3.0-only.txt

%changelog
* Thu Sep 24 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR build from Qt 6 imageformats module