# whisker-cli: CLI companion for Whisker.
#
# LISENSI: upstream corecathx/whisker-cli belum punya file LICENSE. Spec ini
# disiapkan untuk build lokal/uji, tetapi JANGAN dikirim ke COPR atau
# didistribusikan sampai upstream menambahkan lisensi (gerbang 1.1 plan 2).
#
# Build masih mengambil hxcpp lewat haxelib (butuh jaringan). Untuk COPR,
# hxcpp harus di-vendor atau dipaketkan terpisah supaya build reproducible.

%global debug_package %{nil}

Name:           whisker-cli
Version:        %{pkg_version}
Release:        1.20261015git54b50c7%{?dist}
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

Upstream does not ship a LICENSE file yet; this package is local-test only
until that gate is resolved.

%prep
%autosetup -n %{name}-%{version}

%build
export HAXELIB_PATH=%{_builddir}/haxelib
mkdir -p "$HAXELIB_PATH"
haxelib setup "$HAXELIB_PATH" >/dev/null 2>&1 || true
haxelib install hxcpp --always --quiet
export WHISKER_VERSION="%{version}"
export WHISKER_COMMIT="54b50c7"
haxe release.hxml

%install
install -Dpm0755 target/cpp/whisker %{buildroot}%{_bindir}/whisker

%files
%{_bindir}/whisker

%changelog
* Wed Oct 21 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1.20261015git54b50c7
- Initial local-test packaging of corecathx/whisker-cli.
- hxcpp fetched at build time; licensing gate still open upstream.
