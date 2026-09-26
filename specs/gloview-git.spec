Name:           gloview-git
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        macOS Mission Control-style overview plugin for Hyprland (daily git build)

License:        GPL-3.0-or-later
URL:            https://github.com/fedsfarm/gloview
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cmake >= 3.19
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(hyprland)
BuildRequires:  pkgconfig(glesv2)
# Lua's pkg-config module name varies by distro/build (lua, lua5.4, or the
# luajit Hyprland itself links against) — mirror upstream's own
# pkg_search_module() fallback list with an RPM boolean dependency.
BuildRequires:  (pkgconfig(lua) or pkgconfig(lua5.4) or pkgconfig(luajit))

Requires:       hyprland-git

%description
GloView is a macOS Mission Control-style overview/expo plugin for the
Hyprland Wayland compositor: a workspace strip, window previews,
keyboard navigation, and configurable layouts (rows / grid / natural).

%{name} is a daily rolling build tracking the tip of upstream's main
branch — fedsfarm/gloview has not tagged any releases at the time this
spec was written, so there is no stable version to pin to. %{version}
encodes the commit date and short SHA, e.g. 20260926.gitabcdef1.

IMPORTANT — Hyprland plugin ABI hazard: a Hyprland plugin's ABI must
match the *exact* Hyprland build it is loaded into (this is called out
in upstream's own README and PKGBUILD, not something this packaging
adds). This RPM is rebuilt daily against whatever hyprland-devel is
available in the COPR chroot at build time — the accompanying workflow
(.github/workflows/gloview-git.yml) points that chroot at the
lionheartp/Hyprland COPR project (copr://lionheartp/Hyprland, itself a
fork of solopasha/hyprland tracking git HEAD) so `pkgconfig(hyprland)`
resolves against a `hyprland-git` build that is current within the same
day as this package, not a stale pinned release. If the `hyprland-git`
package on a user's system is rebuilt/updated between two daily runs of
this workflow, %{name} can still refuse to load or crash Hyprland on
load until the next matching daily build lands — there is no spec-level
fix for that residual window; users should `dnf reinstall %{name}` any
time they update `hyprland-git` itself.

Load it from hyprland.conf:
    plugin = %{_libdir}/gloview.so
then bind a dispatcher, e.g.:
    bind = SUPER, TAB, gloview:toggle

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install
# CMakeLists.txt sets PREFIX "" on the target, so this installs a bare
# gloview.so (not libgloview.so) straight into %{_libdir} — nothing
# else to stage.

%files
%license LICENSE
%doc README.md
%{_libdir}/gloview.so

%changelog
* Sat Sep 26 2026 tofan79 <tofan79@users.noreply.github.com> - %{pkg_version}-1
- Initial Mindset-Apps COPR build of fedsfarm/gloview, tracking git HEAD
  on the main branch daily since upstream has not tagged any releases.
