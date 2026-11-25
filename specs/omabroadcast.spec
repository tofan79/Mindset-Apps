# OmaBroadcast adalah proyek qmake/Qt6 yang dibangun di Omarchy/Arch dan
# mengikat FFmpeg 9.1 versi pin yang diunduh saat build. Build dari sumber di
# COPR tidak praktis (pacman, makepkg, git fetch FFmpeg, path hardcode). Tiap
# rilis menyediakan paket Arch .pkg.tar.zst berisi binary + FFmpeg bundle;
# workflow mengunduhnya, memverifikasi SHA256, lalu di-repack sebagai RPM.
#
# Versi = <pkgver>.<pkgrel> dari nama asset, mis. 0.1.0.62. Ini membuat pkgrel
# baru dengan tag yang sama tetap memicu build.
#
# Binary membutuhkan glibc sampai 2.44 dan RUNPATH absolut
# /usr/lib/omabroadcast/ffmpeg/lib, jadi paket ini ditujukan untuk Fedora 45+
# ( Fedora 45 memakai glibc 2.44 ).
#
# FFmpeg bundle upstream menautkan libbz2.so.1.0 (nama soname Arch); Fedora
# menyediakan libbz2.so.1. Di %install DT_NEEDED diganti memakai patchelf
# supaya dependency RPM bisa.resolve dan runtime tidak mencari file yang
# tidak ada di Fedora.

Name:           omabroadcast
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Live production, recording and streaming studio for the desktop

License:        MIT AND GPL-3.0-or-later AND GPL-2.0-or-later AND BSD-3-Clause AND MPL-2.0 AND ISC AND Apache-2.0 AND LicenseRef-AOMPL-1.0
URL:            https://github.com/28allday/omabroadcast
Source0:        omabroadcast-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  patchelf

%description
OmaBroadcast is a Qt6/QML live-production app for recording, replaying and
streaming the desktop. It bundles its own FFmpeg 9.1 libraries under
/usr/lib/omabroadcast/ffmpeg/lib and ships a WebEngine helper browser.

This package repacks the upstream x86_64 Arch binary package; nothing is
recompiled locally.

%prep
%setup -q -n omabroadcast-%{version}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a usr %{buildroot}/

# libavformat bundle upstream (Arch) meminta libbz2.so.1.0; Fedora memakai
# libbz2.so.1. Ganti DT_NEEDED-nya supaya dependency RPM bisa resolve.
find %{buildroot}%{_prefix}/lib/%{name}/ffmpeg/lib -type f -name '*.so.*' | while read -r f; do
    if patchelf --print-needed "$f" | grep -qx 'libbz2.so.1.0'; then
        patchelf --replace-needed libbz2.so.1.0 libbz2.so.1 "$f"
    fi
done

desktop-file-validate %{buildroot}%{_datadir}/applications/omabroadcast.desktop

%post
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q %{_datadir}/applications || :
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -qt %{_datadir}/icons/hicolor || :
fi

%postun
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q %{_datadir}/applications || :
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -qt %{_datadir}/icons/hicolor || :
fi

%files
%license %{_datadir}/licenses/%{name}/
%{_bindir}/omabroadcast
%{_prefix}/lib/%{name}/
%{_datadir}/applications/omabroadcast.desktop
%{_datadir}/icons/hicolor/scalable/apps/omabroadcast.svg

%changelog
* Wed Nov 25 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Paket awal: repack paket Arch x86_64 upstream v0.1.0-62.
- Versi memakai pkgver.pkgrel agar rebuild pkgrel memicu workflow.
- FFmpeg bundle, helper WebEngine, dan lisensi pihak ketiga ikut dipasang.
- Perbaikan: DT_NEEDED libbz2.so.1.0 diganti ke libbz2.so.1 (nama soname Fedora).
