Name:           stirling-pdf
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Stirling PDF — Locally hosted web app for PDF operations
License:        MIT
URL:            https://docs.stirlingpdf.com
Source0:        Stirling-PDF-linux-x86_64.rpm

# Binary repackage from upstream RPM, skip debuginfo and RPATH checks
%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

Requires:       glib2
Requires:       gtk3
Requires:       webkit2gtk4.1

%description
Stirling PDF is a powerful, locally hosted web-based PDF manipulation tool.
It lets you perform various operations on PDF files (merge, split, sign,
redact, convert, OCR, compress, and more) without sending documents to
external services. Runs entirely on your machine via a bundled local backend.

%prep
rpm2cpio %{SOURCE0} | cpio -idmv

%install
install -d %{buildroot}/usr/bin
install -d %{buildroot}/usr/lib/"Stirling PDF"/libs
install -d %{buildroot}/usr/lib/"Stirling PDF"/runtime
install -d %{buildroot}%{_datadir}/applications
install -d %{buildroot}%{_datadir}/icons/hicolor

install -pm0755 "usr/bin/Stirling-PDF" %{buildroot}/usr/bin/Stirling-PDF
cp -r "usr/lib/Stirling PDF"/libs/* %{buildroot}/usr/lib/"Stirling PDF"/libs/
cp -r "usr/lib/Stirling PDF"/runtime/* %{buildroot}/usr/lib/"Stirling PDF"/runtime/

install -pm0644 "usr/share/applications/Stirling PDF.desktop" %{buildroot}%{_datadir}/applications/
for size in 16 32 64 128 192 512; do
  install -d %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
  install -pm0644 "usr/share/icons/hicolor/${size}x${size}/apps/Stirling-PDF.png" \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/
done

%files
/usr/bin/Stirling-PDF
/usr/lib/Stirling\ PDF/
%{_datadir}/applications/Stirling\ PDF.desktop
%{_datadir}/icons/hicolor/

%changelog
* Wed Aug 12 2026 mindset <mindset@copr> - %{pkg_version}-1
- Auto-updated from upstream GitHub Releases
