# Serein sudah diterbitkan upstream sebagai RPM Fedora 44 di setiap rilis
# nightly. Membangun dari sumber di COPR itu rapuh dan lambat: workspace butuh
# Rust 1.99.1, empat dependensi git, dan BoringSSL yang dikompilasi dari source.
# workflow mengunduh RPM upstream, memverifikasi SHA256, lalu membongkar payload
# dan memasang ulang file yang sama persis.
#
# Versi memakai `~nightly` (bukan `-nightly`) karena tanda hubung ilegal di
# field Version RPM. Tag v1.0.0-nightly.20261123.102 → 1.0.0~nightly.20261123.102.
# RPM upstream juga memakai konvensi ini.
#
# Aktivitas MPL-2.0 untuk hpke-rs terpenuhi karena direktori licenses/ dari RPM
# upstream ikut dipasang (berisi source dependency), tidak dibuang.

Name:           serein
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Ambient AI desktop companion with local-first memory

License:        MIT OR Apache-2.0
URL:            https://github.com/ViceVerse-cz/Serein
Source0:        serein-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils

%description
Serein is an ambient desktop companion that keeps a local-first memory of your
work and can act on it through inline suggestions, a chat panel, and optional
connectors. The upstream binary ships GTK4/WebKitGTK6 UI, GStreamer and
PulseAudio voice support, and Wayland/X11 backends.

This package repacks the upstream x86_64 Fedora RPM; nothing is recompiled
locally.

%prep
%setup -q -n serein-%{version}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a usr %{buildroot}/

# %license menyalin file ke /usr/share/licenses/<nama>/, jadi salinan asli
# di doc/ harus dipindah supaya tidak tercatat sebagai file unpackaged.
install -d %{buildroot}%{_licensedir}/%{name}
mv %{buildroot}%{_datadir}/doc/serein/LICENSE-* %{buildroot}%{_licensedir}/%{name}/

desktop-file-validate %{buildroot}%{_datadir}/applications/cz.viceverse.serein.desktop

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
%license %{_licensedir}/%{name}/LICENSE-*
%doc usr/share/doc/serein/README.md usr/share/doc/serein/THIRD_PARTY_NOTICES.md usr/share/doc/serein/licenses
%{_bindir}/serein
%{_datadir}/applications/cz.viceverse.serein.desktop
%{_datadir}/icons/hicolor/*/apps/serein*

%changelog
* Wed Nov 25 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Paket awal: repack RPM Fedora 44 upstream dari rilis nightly.
- Versiangka nightly memakai tilde agar valid di field Version RPM.
- Hak MPL-2.0 dipenuhi lewat direktori licenses/ bawaan RPM upstream.
