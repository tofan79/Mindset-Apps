Name:           hype
Version:        %{pkg_version}
Release:        3%{?dist}
Summary:        Simple Markdown presentations with a visual slide editor

# Hindari kegagalan debugsourcefiles.list kosong di COPR.
%global debug_package %{nil}

License:        MIT
URL:            https://github.com/omacom/hype
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  zlib-devel
BuildRequires:  libwebp-devel

%description
Hype is a native Markdown presentation editor with a visual slide editor,
support for images and video, PDF/PowerPoint export, and Omarchy theme
integration.

%prep
%autosetup -n %{name}-%{version}

%build
mkdir -p build
cd build
qmake6 ../hype.pro
make %{?_smp_mflags}

%install
install -Dpm0755 build/hype %{buildroot}%{_bindir}/hype
install -Dpm0644 pkgbuild/hype.desktop %{buildroot}%{_datadir}/applications/hype.desktop
install -Dpm0644 pkgbuild/hype.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/hype.svg
install -Dpm0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%post
if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database -q %{_datadir}/applications || :
fi

%postun
if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database -q %{_datadir}/applications || :
fi

%files
%license %{_datadir}/licenses/%{name}/LICENSE
%{_bindir}/hype
%{_datadir}/applications/hype.desktop
%{_datadir}/icons/hicolor/scalable/apps/hype.svg

%changelog
* Mon Nov 09 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR build from upstream release tag