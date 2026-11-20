# Repack RPM x86_64 resmi dari hulu. Build MDM dari source Rust memakan waktu
# lebih lama dari batas waktu chroot COPR (timeout + "build root is locked"),
# jadi paket ini mengambil biner rilis yang sudah dibangun upstream di GitHub
# Actions. RPM hulu tidak punya scriptlet, jadi aman diekstrak langsung ke
# buildroot. Semua path dan isi mengikuti RPM resmi apa adanya.

Name:           mister-download-manager
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Free download manager with torrent, video grabber and browser integration
License:        GPL-3.0-or-later
URL:            https://github.com/anefzaoui/misterdownloadmanager
Source0:        https://github.com/anefzaoui/misterdownloadmanager/releases/download/v%{version}/MisterDownloadManager-%{version}-linux-x86_64.rpm
ExclusiveArch:  x86_64

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

# Requirement berikut disalin dari metadata RPM upstream. AutoReq dimatikan
# supaya tidak ada dependensi tambahan dari hasil scan biner prebuilt.
AutoReqProv:    no

BuildRequires:  cpio
BuildRequires:  rpm-build

Requires:       ca-certificates
Requires:       glibc >= 2.35
Requires:       gtk3
Requires:       libxkbcommon
Requires:       libxkbcommon-x11
Requires:       mesa-libEGL
Requires:       mesa-libGL

%description
Mister Download Manager (MDM) speeds files up with parallel connections,
resumes broken downloads, catches browser downloads, and also handles
torrents, videos, galleries and debrid links. This package repacks the
official upstream x86_64 RPM, including the four binaries (GUI, CLI, MCP and
native-messaging host), the Chromium/Firefox extension and the browser
native-messaging manifests.

%prep

%build

%install
mkdir -p %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot} > /dev/null 2>&1
rm -rf %{buildroot}/usr/lib/.build-id

%files
%license %{_datadir}/doc/misterdownloadmanager/LICENSE
%doc %{_datadir}/doc/misterdownloadmanager/ATTRIBUTION.md
%dir %{_datadir}/doc/misterdownloadmanager
%{_bindir}/misterdownloadmanager
%{_bindir}/misterdownloadmanager-nmhost
%{_bindir}/misterdownloadmanager-cli
%{_bindir}/misterdownloadmanager-mcp
%{_datadir}/applications/misterdownloadmanager.desktop
%{_datadir}/icons/hicolor/256x256/apps/misterdownloadmanager.png
%{_datadir}/misterdownloadmanager/

%dir /etc/chromium
%dir /etc/chromium/native-messaging-hosts
/etc/chromium/native-messaging-hosts/com.misterdownloadmanager.host.json
%dir /etc/opt/chrome
%dir /etc/opt/chrome/native-messaging-hosts
/etc/opt/chrome/native-messaging-hosts/com.misterdownloadmanager.host.json
%dir /etc/opt/edge
%dir /etc/opt/edge/native-messaging-hosts
/etc/opt/edge/native-messaging-hosts/com.misterdownloadmanager.host.json
%dir %{_prefix}/lib/mozilla
%dir %{_prefix}/lib/mozilla/native-messaging-hosts
%{_prefix}/lib/mozilla/native-messaging-hosts/com.misterdownloadmanager.host.json
%dir %{_prefix}/lib64/mozilla
%dir %{_prefix}/lib64/mozilla/native-messaging-hosts
%{_prefix}/lib64/mozilla/native-messaging-hosts/com.misterdownloadmanager.host.json

%changelog
* Fri Nov 20 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Ganti dari build source ke repack RPM upstream: build Rust melewati batas
  waktu COPR dan menyebabkan build root terkunci.
- Isi paket mengikuti RPM resmi v%{version} apa adanya (biner, ekstensi,
  manifest browser, ikon, dan desktop entry).
