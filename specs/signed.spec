Name:           signed
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Sign PDFs and fill them in with text and dates

# Hindari kegagalan debugsourcefiles.list kosong di COPR.
%global debug_package %{nil}

License:        MIT
URL:            https://github.com/omacom/signed
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  poppler-qt6-devel
BuildRequires:  qpdf-devel

# Modul QML dan platform Wayland dimuat saat runtime, tidak terdeteksi otomatis.
Requires:       qt6-qtdeclarative
Requires:       qt6-qtwayland
Requires:       xdg-desktop-portal
# Dipakai untuk database sertifikat saat PDF disegel.
Requires:       nss
# Font yang dipakai untuk menata teks di halaman PDF.
Recommends:     google-noto-sans-fonts

%description
Signed is a native PDF signer built with Qt Quick: open a PDF, drop a
signature, a line of text, or today's date anywhere on a page, move and size
it, and save a signed copy. The copy can optionally be sealed with a digital
certificate so any later change to it shows. The original PDF is never
modified. On Omarchy the interface follows the theme's accent color.

%prep
%autosetup -n %{name}-%{version}

%build
mkdir -p build
cd build
qmake6 ../signed.pro
make %{?_smp_mflags}

%install
install -Dpm0755 build/signed %{buildroot}%{_bindir}/signed
install -Dpm0644 pkgbuild/signed.desktop %{buildroot}%{_datadir}/applications/signed.desktop
install -Dpm0644 pkgbuild/signed.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/signed.svg
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
%{_bindir}/signed
%{_datadir}/applications/signed.desktop
%{_datadir}/icons/hicolor/scalable/apps/signed.svg

%changelog
* Tue Nov 10 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR build from upstream release tag
