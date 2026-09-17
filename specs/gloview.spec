Name:           gloview
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Minimal macOS-style window overview plugin for Hyprland
License:        GPL-3.0-or-later
URL:            https://github.com/fedsfarm/gloview
Source0:        gloview-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

Requires:       hyprland
Requires:       mesa-libGL
Requires:       lua-libs

%description
GloView is a macOS Mission Control-style window overview plugin for Hyprland.
Super+Tab toggles the overview, with a fully configurable keyboard layout and
styling via the plugin:gloview:* keys.

The plugin is pre-built in CI inside a Fedora 44 container with the
lionheartp/Hyprland COPR enabled, so the chroot only packages the binary.

%prep
%setup -q -n gloview-%{version}

%build
# Pre-built in the GitHub Actions workflow (gloview.so shipped in Source0)

%install
install -d %{buildroot}%{_libdir}
install -m 0755 gloview.so %{buildroot}%{_libdir}/gloview.so

%files
%{_libdir}/gloview.so

%changelog
* Thu Sep 17 2026 mindset <mindset@copr> - %{pkg_version}-1
- Pre-built binary package (built in CI, packaged in COPR chroot)