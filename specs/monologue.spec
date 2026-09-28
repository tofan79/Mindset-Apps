Name:           monologue
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Theme-synced webcam recorder with a built-in trim editor
License:        MIT
URL:            https://github.com/omacom/monologue
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  x86_64

BuildRequires:  gcc-c++
BuildRequires:  make

# monologue.pro: QT += core gui qml quick quickcontrols2 multimedia dbus
# concurrent
# core/gui/dbus/concurrent ikut qt6-qtbase-devel; qml/quick/quickcontrols2
# ikut qt6-qtdeclarative-devel; multimedia → qt6-qtmultimedia-devel.
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  pulseaudio-libs-devel

# README upstream: "Install ... libpulse" — perekaman mikrofon lewat
# PulseAudio-compatible server (PipeWire-Pulse pada sistem modern).
# Di Fedora pustaka client-nya ada di pulseaudio-libs.
Requires:       pulseaudio-libs
# Yang dipanggil lewat QProcess saat menyimpan hasil rekaman. Arch
# depend-nya 'ffmpeg'; padanannya di repo Fedora adalah ffmpeg-free
# (build LGPL). Bandingkan omashow-git yang menautkan libav* secara
# langsung — Monologue tidak butuh devel, hanya biner CLI.
Requires:       ffmpeg-free
Requires:       qt6-qtbase-gui
Requires:       qt6-qtdeclarative
Requires:       qt6-qtmultimedia
Requires:       xdg-desktop-portal
Requires:       hicolor-icon-theme

# Kamera tidak butuh paket RPM — diambil lewat /dev/video* + V4L2 yang
# sudah ada di kernel. Tidak ada Recommends untuk device kamera karena
# tidak ada cara mendeteksinya dari dep.

%global debug_package %{nil}

%description
Monologue is a simple webcam recorder. Choose a camera and microphone once,
then press Space to record; press again to pause or resume the same take.
Stopping opens the recording in a built-in editor where you can trim either
end or cut ranges out of the middle, then save. The interface is theme-synced
with the system dark/light mode.

%prep
%autosetup -n %{name}-%{version}

%build
# .pro tidak mendukung build shadow di luar pohon, jadi tidak bisa memakai
# %make_build dengan BUILDDIR terpisah; PKGBUILD upstream juga di dalam pohon.
mkdir -p build
pushd build
qmake6 ../monologue.pro
%make_build
popd

%install
install -Dm755 build/monologue %{buildroot}%{_bindir}/monologue
install -Dm644 pkgbuild/monologue.desktop \
  %{buildroot}%{_datadir}/applications/monologue.desktop
install -Dm644 pkgbuild/monologue.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/monologue.svg

%post
for cmd in "gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor" \
           "update-desktop-database -q"; do
  $cmd >/dev/null 2>&1 || :
done

%postun
for cmd in "gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor" \
           "update-desktop-database -q"; do
  $cmd >/dev/null 2>&1 || :
done

%files
%license LICENSE
%doc README.md
%{_bindir}/monologue
%{_datadir}/applications/monologue.desktop
%{_datadir}/icons/hicolor/scalable/apps/monologue.svg

%changelog
* Mon Sep 28 2026 Mindset Apps <mindset@example.com> - 0.3.0-1
- Initial packaging, tracking upstream tag v0.3.0.
- Requires pulseaudio-libs (upstream "libpulse") and ffmpeg-free (upstream
  "ffmpeg"); Monologue drives the ffmpeg CLI, so no -devel package is needed.
