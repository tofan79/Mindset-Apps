Name:           caelestia-cli
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Command line tool for the Caelestia desktop shell

License:        GPL-3.0-only
URL:            https://github.com/caelestia-dots/cli
Source0:        caelestia-%{version}-py3-none-any.whl

BuildArch:      noarch

# Paket memakai wheel resmi rilis, bukan sdist: versi sdist dihitung dari
# git (hatch-vcs, pyproject.toml dynamic = ["version"]), jadi tidak bisa
# dibangun dari tarball SRPM yang tidak punya .git.
BuildRequires:  python3-devel
BuildRequires:  python3-pip

# dependencies di pyproject.toml: pillow, materialyoucolor. Keduanya ada
# di Fedora (python3-pillow, python3-materialyoucolor).
Requires:       python3-pillow
Requires:       python3-materialyoucolor

%description
Command line interface for the Caelestia desktop shell: start/stop/reload
the shell, change settings, screenshots, recording, clipboard, wallpaper
and colour-scheme control.

Dipaketkan dari wheel resmi rilis upstream. Shell-nya sendiri ada di
paket terpisah caelestia-shell.

%prep
mkdir -p dist
cp %{SOURCE0} dist/

# Lisensi ikut di dalam wheel (caelestia-<v>.dist-info/licenses/LICENSE);
# tarik keluar supaya bisa dijadikan file lisensi paket. Nama file wheel
# memakai "caelestia-", bukan %{name} (caelestia-cli).
%{__python3} -m zipfile -e dist/caelestia-%{version}-py3-none-any.whl wheeldir/
cp wheeldir/caelestia-%{version}.dist-info/licenses/LICENSE LICENSE

%build

%install
%py3_install_wheel caelestia-%{version}-py3-none-any.whl

%files
%license LICENSE
%{_bindir}/caelestia
%{python3_sitelib}/caelestia/
%{python3_sitelib}/caelestia-%{version}.dist-info/

%changelog
* Thu Oct 08 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial COPR packaging of caelestia-cli, built from the official
  release wheel (the sdist derives its version via hatch-vcs and cannot
  build from an SRPM tarball).
