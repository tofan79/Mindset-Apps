# omafont: manajer font untuk Omarchy/rakuOS (Qt6/QML). Dibangun dari sumber
# karena upstream tidak menerbitkan artifact biner maupun RPM.

Name:           omafont
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Font manager for Omarchy: browse, preview, install and remove fonts
License:        MIT
URL:            https://github.com/28allday/omafont-app
Source0:        omafont-%{version}.tar.gz

%global debug_package %{nil}

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  fontconfig-devel
BuildRequires:  libarchive-devel

%description
OmaFont is a font manager for Omarchy: browse, preview, install and remove
fonts. On RakuOS the "send monospace font to terminal" button expects
omarchy-font-set, which is unavailable; every other feature (install, preview,
collections, disable) works normally with the default Qt theme.

%prep
%autosetup -n omafont-%{version}

%build
mkdir -p build
cd build
qmake6 ../omafont.pro PREFIX=%{_prefix}
make %{?_smp_mflags}

%install
install -Dpm0755 build/omafont %{buildroot}%{_bindir}/omafont
install -Dpm0644 pkgbuild/omafont.desktop %{buildroot}%{_datadir}/applications/omafont.desktop
install -Dpm0644 pkgbuild/omafont.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/omafont.svg
install -Dpm0644 LICENSE %{buildroot}%{_licensedir}/omafont/LICENSE
install -Dpm0644 src/ui/icons/LICENSE.lucide %{buildroot}%{_licensedir}/omafont/LICENSE.lucide

%files
%license LICENSE
%license src/ui/icons/LICENSE.lucide
%{_bindir}/omafont
%{_datadir}/applications/omafont.desktop
%{_datadir}/icons/hicolor/scalable/apps/omafont.svg

%changelog
* Fri Nov 06 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package, built from the upstream release tag.