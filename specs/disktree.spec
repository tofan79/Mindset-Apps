Name:           disktree
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        A treemap for finding and removing what fills your disk

%global debug_package %{nil}

License:        MIT
URL:            https://github.com/tobi/disktree
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  vulkan-headers
BuildRequires:  libxkbcommon-devel
BuildRequires:  libxkbcommon-x11-devel
BuildRequires:  libxcb-devel
BuildRequires:  gtk4-devel

%description
Disktree is an interactive disk-usage treemap for Hyprland/Linux: scan a path,
mark tiles with Space, open with Enter, review marked files with c, and prune
what fills your disk. Runs as a Wayland desktop app.

%prep
%autosetup -n %{name}-%{version}

%build
make build

%install
install -Dm755 target/release/disktree %{buildroot}%{_bindir}/disktree
install -Dm644 assets/disktree.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/disktree.svg
mkdir -p %{buildroot}%{_datadir}/applications
VERSION=$(sed -n 's/^version = "\(.*\)"/\1/p' Cargo.toml | head -1)
sed -e 's|@BINDIR@|%{_bindir}|' -e "s|@VERSION@|$VERSION|" \
  packaging/disktree.desktop.in > %{buildroot}%{_datadir}/applications/disktree.desktop
install -Dpm0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%post
update-desktop-database -q %{_datadir}/applications >/dev/null 2>&1 || :

%postun
update-desktop-database -q %{_datadir}/applications >/dev/null 2>&1 || :

%files
%license LICENSE
%{_bindir}/disktree
%{_datadir}/applications/disktree.desktop
%{_datadir}/icons/hicolor/scalable/apps/disktree.svg

%changelog
* Tue Nov 10 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR build from upstream release tag
