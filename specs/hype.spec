Name:           hype
Version:        %{pkg_version}
Release:        3%{?dist}
Summary:        Simple Markdown presentations with a visual slide editor

# Hindari kegagalan debugsourcefiles.list kosong di COPR.
%global debug_package %{nil}

# GCC 16 (Fedora 45) mengalami ICE — cc1plus segfault saat mengompilasi
# src/apptheme.cpp dengan LTO. Matikan LTO untuk paket ini; CMakeLists juga
# menyalakan INTERPROCEDURAL_OPTIMIZATION per target, jadi baris itu dibuang
# di %prep.
%global _lto_cflags %{nil}

License:        MIT
URL:            https://github.com/omacom/hype
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.21
BuildRequires:  ninja-build
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
# INTERPROCEDURAL_OPTIMIZATION ON menambahkan -flto lagi di atas flag RPM;
# kombinasi itulah yang memicu ICE GCC 16.
sed -i '/INTERPROCEDURAL_OPTIMIZATION ON/d' CMakeLists.txt

%build
# Sejak v0.7.0 upstream pindah dari qmake ke CMake; hype.pro sudah tidak
# ada di tarball rilis. CMakeLists tidak punya install(), jadi biner tetap
# dipasang manual di %install.
%cmake -G Ninja
%cmake_build

%install
install -Dpm0755 %{_vpath_builddir}/hype %{buildroot}%{_bindir}/hype
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