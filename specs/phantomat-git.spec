Name:           phantomat-git
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Zoomable infinite-canvas overview plugin for Hyprland (daily git build)

License:        BSD-3-Clause
URL:            https://github.com/djeddi-yacine/phantomat
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  x86_64

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(hyprland)
BuildRequires:  pkgconfig(hyprgraphics)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(xkbcommon)
# Makefile: PKGS = ... lua5.4, falling back to "lua"; CMakeLists.txt does the
# same via pkg_search_module(). Fedora only ships pkgconfig(lua) (5.4.x), but
# the module name varies by distro/build, so mirror upstream's fallback list
# with an RPM boolean dependency.
BuildRequires:  (pkgconfig(lua) or pkgconfig(lua5.4) or pkgconfig(luajit))

# Hyprland plugin: a .so is dlopen()ed into whichever compositor is present, so
# bind to the one already installed instead of pulling a second, conflicting
# build. hyprland-git hard-Conflicts: hyprland, so a flat "Requires: hyprland"
# would make any image that ships the git build unresolvable.
# (A if A else B) = "if A is installed, A must stay; otherwise B is required".
Requires:       (hyprland-git if hyprland-git else hyprland)

%description
Phantomat (formerly "Spatial Overview") is a Hyprland plugin that turns the
compositor into a zoomable, infinite canvas: every window gets a place in 2D
space, and SUPER+CTRL+G zooms out to see, navigate, and rearrange them all,
with live previews, drag and drop, and window rules.

%{name} is a daily rolling build tracking the tip of upstream's master branch —
kaolti/phantomat has not tagged any releases (hyprpm.toml only defines a
"make all" build), so there is no stable version to pin to. %{version} encodes
the commit date and short SHA, e.g. 20261008.gita1e8a08.

IMPORTANT — Hyprland plugin ABI hazard: a Hyprland plugin's ABI must match the
*exact* Hyprland build it is loaded into, and Hyprland refuses plugins whose
PLUGIN_API_VERSION differs from its own ("API version mismatch"). This RPM is
rebuilt daily against whatever hyprland-devel the COPR chroot provides; the
project carries the external repository copr://lionheartp/Hyprland
(a solopasha/hyprland fork tracking git HEAD) precisely so that
pkgconfig(hyprland) resolves to a current hyprland-git build rather than a
stale pinned release. If hyprland-git on your system is rebuilt between two
daily runs of this workflow, the plugin can still refuse to load until the
next matching build lands — there is no spec-level fix for that window; run
`dnf reinstall %{name}` any time you update hyprland-git itself.

Load it from hyprland.conf:
    plugin = %{_libdir}/spatialoverview.so
Copy the example settings shipped in %{_docdir}/%{name}/spatialoverview.lua to
~/.config/hypr/spatialoverview.lua before the first launch.

%prep
%autosetup -n %{name}-%{version}

%build
# hyprpm.toml builds this plugin with "make all", and the Makefile adds
# -fno-gnu-unique for g++ so Hyprland can unload the module safely; the
# bundled CMakeLists.txt does not set that flag. Build the way upstream does.
#
# SCROLLOVERVIEW_BUILD_VERSION is what `hyprctl plugin list` reports. Without
# it scripts/generate-plugin-version.sh falls back to `git rev-parse`, which
# yields "unknown" inside a release tarball.
export SCROLLOVERVIEW_BUILD_VERSION=%{version}
%make_build CXX=g++ OUT=spatialoverview.so

%install
# The Makefile has no install target (the .so normally lives in
# ~/.local/share/spatial-overview/ for hyprpm), so stage it by hand.
install -Dpm0755 spatialoverview.so %{buildroot}%{_libdir}/spatialoverview.so

%files
%license LICENSE
%doc README.md
%doc examples/spatialoverview.lua
%{_libdir}/spatialoverview.so

%changelog
* Fri Nov 06 2026 tofan79 <tofan79@users.noreply.github.com> - %{pkg_version}-1
- Initial Mindset-Apps COPR build of kaolti/phantomat, tracking git HEAD on
  the master branch daily since upstream has not tagged any releases.
- Build against pkgconfig(hyprland) from the project's external
  copr://lionheartp/Hyprland repository; Fedora itself does not ship Hyprland.
