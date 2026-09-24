Name:           hyprland-preview-share-picker
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Alternative share picker for Hyprland with window and monitor previews

License:        MIT
URL:            https://github.com/WhySoBad/hyprland-preview-share-picker
# Tarball dibuat workflow (git clone --recurse-submodules, submodule lib/hyprland-protocols
# diwajibkan saat compile oleh wayland_scanner::generate_interfaces!)
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  gtk4-devel
BuildRequires:  gtk4-layer-shell-devel

Requires:       gtk4
Requires:       gtk4-layer-shell
Requires:       xdg-desktop-portal-hyprland
Requires:       hyprland

%description
An alternative share picker for xdg-desktop-portal-hyprland, written in
Rust. Shows live previews of monitors and windows so the user can pick
what to share (used by OBS, screenshots, screen recording, video calls)
instead of the plain Qt list from the portal default. Wired in Omarchy
through the xdph.conf screencopy.custom_picker_binary setting.

%prep
%setup -q -n %{name}-%{version}

%build
export CARGO_NET_OFFLINE=false
cargo build --release --locked

%install
install -Dpm0755 target/release/hyprland-preview-share-picker \
    %{buildroot}%{_bindir}/hyprland-preview-share-picker

./target/release/hyprland-preview-share-picker schema > schema.json
install -Dpm0644 schema.json \
    %{buildroot}%{_datadir}/hyprland-preview-share-picker/schema.json

%files
%{_bindir}/hyprland-preview-share-picker
%{_datadir}/hyprland-preview-share-picker/schema.json
%license LICENSE

%changelog
* Thu Sep 24 2026 mindset <mindset@copr> - 0.1.0-1
- Initial COPR build from upstream master