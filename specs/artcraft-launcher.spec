# artcraft-launcher: launcher untuk Craft App Suite (Rust, MIT OR Apache-2.0).
#
# Upstream menerbitkan RPM x86_64 di setiap rilis; spec ini tidak membangun
# ulang dari sumber (proyek Rust + wgpu, build-nya berat), melainkan membongkar
# payload RPM itu dan memasang ulang isinya. Aplikasi yang dikelola launcher
# (PhotoCraft, FilmCraft, dst.) diunduh sendiri oleh launcher saat runtime,
# jadi tidak perlu dipaketkan di sini.

Name:           artcraft-launcher
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Install, update and launch the Craft App Suite

License:        MIT OR Apache-2.0
URL:            https://github.com/storytold/craft-launcher
Source0:        artcraft-launcher-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

ExclusiveArch:  x86_64

# Binary hanya menautkan libc/libm/libgcc; X11, Wayland, dan Vulkan dibuka
# lewat dlopen oleh winit/wgpu, jadi soname-nya ditulis manual seperti yang
# dilakukan RPM upstream.
Requires:       libxkbcommon.so.0()(64bit)
Requires:       libxkbcommon-x11.so.0()(64bit)
Requires:       libwayland-client.so.0()(64bit)
Requires:       libX11.so.6()(64bit)
Requires:       libX11-xcb.so.1()(64bit)
Requires:       libxcb.so.1()(64bit)
Requires:       libXcursor.so.1()(64bit)
Requires:       libXi.so.6()(64bit)
Requires:       (libvulkan.so.1()(64bit) or libEGL.so.1()(64bit))

%description
ArtCraft Launcher is a pure-Rust launcher for the Craft App Suite: PhotoCraft,
LightCraft, FilmCraft, DesignCraft, VectorCraft, PdfCraft, EffectCraft,
WordCraft, DeckCraft, GridCraft, CADCraft, SoundCraft and FigCraft.

It picks the right build for the machine, installs and updates it, then opens
it. The apps themselves are downloaded by the launcher at runtime; this package
only provides the launcher.

%prep
%setup -q -n artcraft-launcher-%{version}

%install
install -Dpm0755 usr/bin/artcraft-launcher \
    %{buildroot}%{_bindir}/artcraft-launcher

install -Dpm0644 usr/share/applications/ai.storyteller.artcraft-launcher.desktop \
    %{buildroot}%{_datadir}/applications/ai.storyteller.artcraft-launcher.desktop

for size in 16 24 32 48 64 128 256 512; do
    install -Dpm0644 "usr/share/icons/hicolor/${size}x${size}/apps/ai.storyteller.artcraft-launcher.png" \
        "%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/ai.storyteller.artcraft-launcher.png"
done

install -Dpm0644 usr/share/doc/artcraft-launcher/LICENSE-APACHE \
    %{buildroot}%{_licensedir}/artcraft-launcher/LICENSE-APACHE
install -Dpm0644 usr/share/doc/artcraft-launcher/LICENSE-MIT \
    %{buildroot}%{_licensedir}/artcraft-launcher/LICENSE-MIT
install -Dpm0644 usr/share/doc/artcraft-launcher/NOTICE \
    %{buildroot}%{_docdir}/artcraft-launcher/NOTICE
install -Dpm0644 usr/share/doc/artcraft-launcher/ATTRIBUTION.md \
    %{buildroot}%{_docdir}/artcraft-launcher/ATTRIBUTION.md
install -Dpm0644 usr/share/doc/artcraft-launcher/README.md \
    %{buildroot}%{_docdir}/artcraft-launcher/README.md

%files
%license %{_licensedir}/artcraft-launcher/LICENSE-APACHE
%license %{_licensedir}/artcraft-launcher/LICENSE-MIT
%doc %{_docdir}/artcraft-launcher/NOTICE
%doc %{_docdir}/artcraft-launcher/ATTRIBUTION.md
%doc %{_docdir}/artcraft-launcher/README.md
%{_bindir}/artcraft-launcher
%{_datadir}/applications/ai.storyteller.artcraft-launcher.desktop
%{_datadir}/icons/hicolor/*/apps/ai.storyteller.artcraft-launcher.png

%changelog
* Wed Oct 21 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package from the upstream RPM
