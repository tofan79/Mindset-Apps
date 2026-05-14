Name:           wl-screenrec
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        High-performance screencast recording for Wayland

License:        Apache-2.0
URL:            https://github.com/russelltg/wl-screenrec
Source0:        wl-screenrec-%{version}.tar.gz
Source1:        vendor.tar.gz

ExcludeArch:    %{ix86}

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

BuildRequires:  rust >= 1.85
BuildRequires:  cargo
BuildRequires:  clang
BuildRequires:  llvm
BuildRequires:  pkgconfig(libdrm)

BuildRequires:  ffmpeg-free-devel

Requires:       ffmpeg-free
Requires:       libdrm
Requires:       libva

%description
High-performance screen recording for Wayland compositors.
Supports hardware-accelerated encoding via VA-API (GPU) and
software encoding via FFmpeg.

%prep
%setup -q -n wl-screenrec-%{version}
tar xzf %{SOURCE1}
mkdir -p .cargo
cat > .cargo/config.toml << 'EOF'
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
CARGO_NET_OFFLINE=true cargo build --release --locked

%install
install -D -m 755 target/release/wl-screenrec %{buildroot}%{_bindir}/wl-screenrec

install -d %{buildroot}%{_datadir}/bash-completion/completions
install -d %{buildroot}%{_datadir}/fish/vendor_completions.d
install -d %{buildroot}%{_datadir}/zsh/site-functions

target/release/wl-screenrec --generate-completions bash > %{buildroot}%{_datadir}/bash-completion/completions/wl-screenrec
target/release/wl-screenrec --generate-completions fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/wl-screenrec.fish
target/release/wl-screenrec --generate-completions zsh > %{buildroot}%{_datadir}/zsh/site-functions/_wl-screenrec

%files
%{_bindir}/wl-screenrec
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/wl-screenrec
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/wl-screenrec.fish
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_wl-screenrec

%changelog
* Thu May 14 2026 mindset <mindset@copr> - %{pkg_version}-1
- Auto-updated from upstream GitHub Releases
