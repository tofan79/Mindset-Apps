Name:           gliff
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Hyprland remote desktop over SSH (GPU H.264, 4:4:4)

%global debug_package %{nil}

License:        MIT AND BSD-2-Clause
URL:            https://github.com/omacom/gliff
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  nasm
BuildRequires:  pkgconfig
BuildRequires:  dbus-devel
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  libdrm-devel
BuildRequires:  libva-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  vulkan-devel
BuildRequires:  wayland-devel

Requires:       gtk4
Requires:       libadwaita
Requires:       hicolor-icon-theme

%description
Gliff shows a Hyprland session from another machine in a window on yours, over
SSH only: no open ports, no accounts, no relay. Text stays sharp (4:4:4
through hardware H.264), video runs on the GPU on both ends with CPU
fallback, and keyboard layout, clipboard, and reconnection follow.

%prep
%autosetup -n %{name}-%{version}

%build
./bin/build

%install
install -Dpm0755 target/release/gliff %{buildroot}%{_bindir}/gliff
install -Dpm0755 target/release/gliff-server %{buildroot}%{_bindir}/gliff-server
install -Dpm0755 target/release/gliff-probe %{buildroot}%{_bindir}/gliff-probe 2>/dev/null || true
install -Dpm0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
install -Dpm0644 NOTICE %{buildroot}%{_datadir}/licenses/%{name}/NOTICE 2>/dev/null || true
install -Dpm0644 pkgbuild/gliff.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/gliff.svg
install -Dpm0644 pkgbuild/gliff.desktop %{buildroot}%{_datadir}/applications/gliff.desktop

%post
update-desktop-database -q >/dev/null 2>&1 || :

%postun
update-desktop-database -q >/dev/null 2>&1 || :

%files
%license %{_datadir}/licenses/%{name}/LICENSE
%license %{_datadir}/licenses/%{name}/NOTICE
%{_bindir}/gliff
%{_bindir}/gliff-server
%{_bindir}/gliff-probe
%{_datadir}/applications/gliff.desktop
%{_datadir}/icons/hicolor/scalable/apps/gliff.svg

%changelog
* Tue Nov 10 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR build from upstream release tag
