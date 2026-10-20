# nuclear: music player Tauri/WebKit (AGPL-3.0), dibangun upstream sebagai RPM.
#
# Upstream sudah menerbitkan RPM x86_64 di setiap rilis (tag "player@X.Y.Z"),
# jadi spec ini tidak membangun Electron/Tauri dari sumber: workflow mengunduh
# RPM itu, membongkar payload-nya, lalu memasang ulang tiga file yang sama
# (binary, .desktop, ikon). Cara ini mengikuti pola yang sama dengan paket
# AppImage lain di repo ini.

Name:           nuclear
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Music player for your desktop built with Tauri and WebKit

License:        AGPL-3.0-only
URL:            https://github.com/nukeop/nuclear
Source0:        nuclear-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

# Rilis upstream hanya menyediakan RPM x86_64.
ExclusiveArch:  x86_64

# libwebkit2gtk-4.1 dan libgtk-3 terdeteksi otomatis dari binary; plugin
# GStreamer tidak pernah muncul sebagai soname, jadi ditulis eksplisit.
Requires:       (gstreamer1-plugin-libav or gstreamer-plugins-libav)

%description
Nuclear is a free music streaming application for the desktop, built with
Tauri (Rust + WebKit) and React. It streams from YouTube, Jamendo, Audius and
other sources, keeps a local library, and can download tracks for offline
playback.

This package repacks the upstream x86_64 RPM; nothing is rebuilt locally.

%prep
%setup -q -n nuclear-%{version}

%install
install -Dpm0755 usr/bin/nuclear-music-player \
    %{buildroot}%{_bindir}/nuclear-music-player

install -Dpm0644 usr/share/applications/Nuclear.desktop \
    %{buildroot}%{_datadir}/applications/Nuclear.desktop

install -Dpm0644 usr/share/icons/hicolor/512x512/apps/nuclear-music-player.png \
    %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/nuclear-music-player.png

%files
%{_bindir}/nuclear-music-player
%{_datadir}/applications/Nuclear.desktop
%{_datadir}/icons/hicolor/512x512/apps/nuclear-music-player.png

%changelog
* Tue Oct 20 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package from the upstream RPM
