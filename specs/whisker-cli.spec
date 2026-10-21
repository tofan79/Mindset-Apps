# whisker-cli: CLI companion for Whisker.
#
# License follows whisker-shell (same author/project): GPL-3.0-only. Upstream
# still has no standalone LICENSE file, so the license is declared here and
# in the package metadata rather than installed as a file.
#
# Build takes hxcpp through haxelib; the COPR workflow enables network for
# this package because hxcpp is not packaged in Fedora.

%global debug_package %{nil}

Name:           whisker-cli
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        CLI helper for the Whisker Quickshell shell
License:        GPL-3.0-only
URL:            https://github.com/corecathx/whisker-cli
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  x86_64

BuildRequires:  haxe
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  zlib-devel

%description
whisker-cli is the command-line companion for Whisker: it starts and restarts
the shell, stores preferences, exposes IPC commands, and lists wallpapers.

%prep
%autosetup -n %{name}-%{version}

%build
export HAXELIB_PATH=%{_builddir}/haxelib
mkdir -p "$HAXELIB_PATH"
haxelib setup "$HAXELIB_PATH" >/dev/null 2>&1 || true
haxelib install hxcpp --always --quiet

# Version snapshots look like 0.6.20261015.git54b50c7. Macro.hx wants the
# upstream base version and the short commit separately, not the RPM version.
WHISKER_BASE=$(echo "%{version}" | cut -d. -f1-2)
WHISKER_SHA=$(echo "%{version}" | sed -n 's/.*\.git\([0-9a-f]*\)$/\1/p')
export WHISKER_VERSION="$WHISKER_BASE"
export WHISKER_COMMIT="${WHISKER_SHA:-unknown}"
haxe release.hxml

%install
install -Dpm0755 target/cpp/whisker %{buildroot}%{_bindir}/whisker

%files
%{_bindir}/whisker

%changelog
* Wed Oct 21 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial packaging of corecathx/whisker-cli.
- License declared GPL-3.0-only, matching whisker-shell.
- hxcpp fetched through haxelib at build time; COPR enables network for it.
