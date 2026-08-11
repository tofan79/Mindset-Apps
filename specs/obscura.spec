Name:           obscura
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Fast embeddable browser automation engine with native rendering

License:        Apache-2.0
URL:            https://github.com/h4ckf0r0day/obscura
Source0:        %{name}-%{version}.tar.gz

# Build render variant (--features render). Rendering uses rustls so it does
# NOT need OpenSSL/CMake for BoringSSL; V8/deno_core still need clang, perl,
# python3 and ninja to compile from source.
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  clang
BuildRequires:  clang-libs
BuildRequires:  cmake
BuildRequires:  glibc-devel
BuildRequires:  ninja-build
BuildRequires:  perl
BuildRequires:  python3

%description
Obscura is a fast, embeddable, pure-Rust browser automation engine. It can
render and capture modern web pages directly without bundling or launching
Chromium: native rendering, screenshots, scrolling, screencasting, and PDF
export through the CLI, MCP, Puppeteer, and Playwright.

%prep
%setup -q -n %{name}-%{version}

%build
export CARGO_NET_OFFLINE=false
cargo build --release -p obscura-cli --bins --features render

%install
install -Dpm0755 target/release/obscura        %{buildroot}%{_bindir}/obscura
install -Dpm0755 target/release/obscura-worker %{buildroot}%{_bindir}/obscura-worker

%files
%{_bindir}/obscura
%{_bindir}/obscura-worker
%license LICENSE

%changelog
* Tue Aug 11 2026 tofan79 <tofan79@users.noreply.github.com> - 0.1.0-1
- Initial build: git snapshot from upstream main
