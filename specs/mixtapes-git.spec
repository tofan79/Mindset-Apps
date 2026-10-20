# mixtapes-git: YouTube Music player GTK4/libadwaita (GPL-3.0).
#
# Upstream belum menerbitkan tag maupun release (masih alpha, versi Cargo.toml
# 0.1.0), jadi paket ini dibangun harian dari commit terbaru branch main —
# pola yang sama dengan gloview-git dan kineticwe-git. Versi paket memakai
# bentuk <versi-cargo>.<YYYYMMDD>.git<sha> supaya COPR bisa membedakan build
# antar commit tanpa menunggu upstream menaikkan versi.

Name:           mixtapes-git
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Modern, Linux-first YouTube Music player (daily git build)

License:        GPL-3.0-or-later
URL:            https://github.com/m-obeid/Mixtapes
Source0:        %{name}-%{version}.tar.gz

%global debug_package %{nil}

ExclusiveArch:  x86_64

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  glib2-devel
# Salah satu crate (lewat ytmusicapi) masih memakai openssl-sys, bukan rustls
# murni; tanpa header openssl build berhenti di pkg-config.
BuildRequires:  openssl-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils

Requires:       gtk4
Requires:       libadwaita
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
Requires:       gstreamer1-plugins-bad-free
Requires:       (gstreamer1-plugin-libav or gstreamer-plugins-libav)
Requires:       hicolor-icon-theme

%description
Mixtapes is a modern, Linux-first YouTube Music client built with GTK4,
libadwaita, and GStreamer. It streams, searches, and keeps a local library,
and follows the GNOME look instead of shipping its own toolkit.

Because upstream publishes neither tags nor releases, this package is rebuilt
from the latest commit on the main branch.

%prep
%autosetup -n %{name}-%{version}

%build
cargo build --release --locked

%install
install -Dpm0755 target/release/mixtapes %{buildroot}%{_bindir}/mixtapes

install -Dpm0644 com.pocoguy.Muse.desktop \
    %{buildroot}%{_datadir}/applications/com.pocoguy.Muse.desktop
install -Dpm0644 com.pocoguy.Muse.metainfo.xml \
    %{buildroot}%{_metainfodir}/com.pocoguy.Muse.metainfo.xml
install -Dpm0644 assets/icons/hicolor/scalable/apps/com.pocoguy.Muse.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/com.pocoguy.Muse.svg

# Upstream menamai perintah desktop "muse" (warisan Flatpak); binary Cargo
# bernama "mixtapes", jadi Exec disesuaikan dengan yang benar-benar dipasang.
sed -i 's/^Exec=muse /Exec=mixtapes /' \
    %{buildroot}%{_datadir}/applications/com.pocoguy.Muse.desktop

%files
%license COPYING
%{_bindir}/mixtapes
%{_datadir}/applications/com.pocoguy.Muse.desktop
%{_metainfodir}/com.pocoguy.Muse.metainfo.xml
%{_datadir}/icons/hicolor/scalable/apps/com.pocoguy.Muse.svg

%changelog
* Tue Oct 20 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package, built from the main branch
