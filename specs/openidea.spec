# openidea: IDE open-source berbasis Tauri (Rust + WebKit, Apache-2.0).
# Upstream menerbitkan RPM x86_64 di setiap rilis, jadi spec ini me-repack RPM
# itu (binary + .desktop + tiga ukuran ikon). Membangun dari sumber tidak
# realistis untuk COPR: repo-nya butuh Node/npm, Vite, dan bundel frontend
# sebelum Tauri dikompilasi.
#
# Pola yang sama dengan `nuclear`, `sonora`, `zapfast`, dan `ario` di repo ini.

Name:           openidea
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Open-source IDE inspired by IntelliJ IDEA
License:        Apache-2.0
URL:            https://github.com/l0ng-ai/openidea
Source0:        openidea-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

# Rilis upstream hanya menyediakan RPM x86_64.
ExclusiveArch:  x86_64

# Binary Tauri ini menautkan WebKitGTK 4.1 dan GTK3; rpmbuild menemukan
# soname-nya sendiri, tapi paket runtime-nya ditulis eksplisit karena
# libwebkit2gtk-4.1.so.0 dimiliki paket bernama lain di Fedora (webkit2gtk4.1)
# dan itu sering jadi sumber "nothing provides" saat di-repack.
Requires:       webkit2gtk4.1

%description
OpenIDEA is an open-source IDE inspired by IntelliJ IDEA, rebuilt in Rust on
top of Tauri and WebKitGTK. It ships a code editor, project tree, plugins, and
a bundled language server.

This package repacks the upstream x86_64 RPM; nothing is rebuilt locally. The
upstream RPM carries no license file, so the Apache-2.0 text is fetched from
the matching upstream tag by the workflow and installed as %license.

%prep
%setup -q -n openidea-%{version}

%install
install -Dpm0755 usr/bin/openidea %{buildroot}%{_bindir}/openidea

install -Dpm0644 usr/share/applications/OpenIDEA.desktop \
    %{buildroot}%{_datadir}/applications/OpenIDEA.desktop

install -Dpm0644 usr/share/icons/hicolor/32x32/apps/openidea.png \
    %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/openidea.png
install -Dpm0644 usr/share/icons/hicolor/128x128/apps/openidea.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/openidea.png
install -Dpm0644 usr/share/icons/hicolor/256x256@2/apps/openidea.png \
    %{buildroot}%{_datadir}/icons/hicolor/256x256@2/apps/openidea.png

# LICENSE tidak di-stage ke %{buildroot}: %license mengambilnya langsung dari
# direktori build lalu memasangnya ke /usr/share/licenses/openidea/.

%files
%license LICENSE
%{_bindir}/openidea
%{_datadir}/applications/OpenIDEA.desktop
%{_datadir}/icons/hicolor/32x32/apps/openidea.png
%{_datadir}/icons/hicolor/128x128/apps/openidea.png
%{_datadir}/icons/hicolor/256x256@2/apps/openidea.png

%changelog
* Fri Nov 06 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package, repacked from the upstream x86_64 RPM.
