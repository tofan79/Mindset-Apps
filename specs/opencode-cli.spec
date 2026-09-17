Name:           opencode-cli
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        opencode CLI — Open-source AI coding agent for your terminal
License:        Proprietary
URL:            https://opencode.ai
Source0:        opencode-cli-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildArch:      x86_64
AutoReqProv:    no

%description
opencode is an open-source AI coding agent that runs in your terminal.
Bring your own model, or use a hosted variant, and drive code edits, TUI,
and local tools across your projects.

%prep
%setup -q -n opencode-cli-%{version}

%install
rm -rf %{buildroot}
install -d %{buildroot}/opt/opencode-cli
cp -r . %{buildroot}/opt/opencode-cli/

BINDIR=%{buildroot}/opt/opencode-cli
BIN=$(find "$BINDIR" -maxdepth 3 -type f -name opencode | head -1)
[ -n "$BIN" ] || { echo "error: opencode binary not found"; exit 1; }

install -d %{buildroot}%{_bindir}
ln -s "${BIN#$BINDIR}" %{buildroot}%{_bindir}/opencode

%files
/opt/opencode-cli/
%{_bindir}/opencode

%changelog
* Thu Sep 17 2026 mindset <mindset@copr> - %{pkg_version}-1
- Auto-updated from upstream GitHub Releases