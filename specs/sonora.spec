# sonora: client streaming musik native (Rust + GPUI, GPL-3.0).
#
# Upstream tidak menerbitkan RPM; yang tersedia adalah AppImage x86_64, binary
# mentah, dan flatpak. GPUI butuh toolchain GPU saat build, jadi spec ini
# mengemas ulang AppImage: seluruh isi squashfs-root dipasang ke /opt/sonora
# dan sebuah wrapper kecil mengarahkan LD_LIBRARY_PATH ke lib bawaan bundle,
# sama seperti yang dilakukan AppRun.

Name:           sonora
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Native music streaming client built with Rust and GPUI

License:        GPL-3.0-or-later
URL:            https://github.com/sonorahq/sonora
Source0:        sonora-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

# Rilis upstream hanya menyediakan AppImage x86_64.
ExclusiveArch:  x86_64

# Bundle membawa sebagian library-nya sendiri di /opt/sonora/lib, jadi deteksi
# soname otomatis tidak akurat: rpm akan meminta soname yang justru sudah
# disertakan di dalam paket ini. Dependensi sistem ditulis manual.
AutoReqProv:    no

Requires:       alsa-lib
Requires:       libXau
Requires:       libxcb
Requires:       libxkbcommon
Requires:       libxkbcommon-x11
Requires:       sqlite-libs
Requires:       libstdc++

%description
Sonora is a native music streaming client written in Rust with GPUI. It
streams from Spotify, keeps a local library, and integrates with the desktop
through MPRIS and the media keys.

This package repacks the upstream x86_64 AppImage.

%prep
%setup -q -n squashfs-root

%install
install -d %{buildroot}/opt/sonora
cp -r usr/bin usr/lib %{buildroot}/opt/sonora/

install -Dpm0644 sonora.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/sonora.svg
install -Dpm0644 sonora.desktop \
    %{buildroot}%{_datadir}/applications/sonora.desktop
install -Dpm0644 usr/share/doc/sonora/LICENSE \
    %{buildroot}%{_licensedir}/sonora/LICENSE

install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/sonora << 'EOF'
#!/bin/sh
# Pakai library bawaan bundle lebih dulu, persis seperti AppRun.
LD_LIBRARY_PATH="/opt/sonora/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec /opt/sonora/bin/sonora "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/sonora

%files
%license %{_licensedir}/sonora/LICENSE
/opt/sonora/
%{_bindir}/sonora
%{_datadir}/applications/sonora.desktop
%{_datadir}/icons/hicolor/scalable/apps/sonora.svg

%changelog
* Tue Oct 20 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package from the upstream AppImage
