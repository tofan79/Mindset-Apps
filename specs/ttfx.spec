Name:           ttfx
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Terminal text effects, a Rust port of terminaltexteffects

License:        MIT
URL:            https://github.com/omacom/ttfx
Source0:        %{name}-%{version}.tar.gz

# The x86-64 assembly engine in asm/ is assembled by build.rs with NASM, but
# those hand-written objects use absolute addressing and are not position
# independent, so they cannot be linked into the PIE executable that Fedora
# builds by default. Upstream build.rs falls back to the parity-exact pure
# Rust engine with a warning when NASM is absent, and that is what we build
# here. Enable the asm engine only once upstream assembles it as PIC.
ExclusiveArch:   x86_64
# Nonaktif secara default. Objek NASM di asm/ memakai alamat absolut sehingga
# tidak Position Independent dan tidak bisa di-link ke executable PIE. dulu
# ditulis bcond_without asm, yang justru mengaktifkan asm secara default,
# jadi build.rs tetap memanggil nasm dan link PIE tetap gagal.
# Tetap bisa diaktifkan eksplisit dengan --with asm kalau upstream nanti
# memperbaiki Position Independent Code-nya.
%bcond_with asm
%if %{with asm}
BuildRequires:  nasm
%endif

BuildRequires:  cargo
BuildRequires:  rust

# rpm di Fedora 44 otomatis membuat subpaket debuginfo sekaligus debugsource.
# Untuk aplikasi pihak ketiga yang dibangun dari tarball tidak ada file sumber
# yang bisa dikumpulkan ke debugsource, sehingga rpm berhenti dengan
# "Empty files file .../debugsourcefiles.list". Matikan keduanya.
%global debug_package %{nil}

%description
A fast, parity-exact Rust port of terminaltexteffects (TTE). Applies
animated text effects such as fireworks, beams, burn, crumble, matrix
and decrypt to text piped on stdin, rendered in the terminal with ANSI
escapes.

Effects are available as subcommands, for example:

  echo RakuOS | ttfx fireworks
  ttfx --random-effect

%prep
%autosetup -n %{name}-%{version}

%build
export CARGO_NET_OFFLINE=false
%if %{with asm}
cargo build --release --locked
%else
# Fitur "asm" dinonaktifkan secara eksplisit, bukan dengan mengandalkan NASM
# yang kebetulan ada atau tidak di chroot. Objek NASM di asm/ memakai alamat
# absolut sehingga tidak Position Independent, dan karena itu tidak bisa
# di-link ke executable PIE yang dibangun Fedora secara default.
# build.rs lalu memakai engine Rust murni yang hasil visualnya identik.
cargo build --release --locked --no-default-features
%endif

%install
install -Dpm0755 target/release/ttfx %{buildroot}%{_bindir}/ttfx

# clap_complete generates these; only bash and zsh are wired upstream.
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions
target/release/ttfx --print-completion bash > %{buildroot}%{_datadir}/bash-completion/completions/ttfx
target/release/ttfx --print-completion zsh > %{buildroot}%{_datadir}/zsh/site-functions/_ttfx

install -Dpm0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
install -Dpm0644 NOTICE %{buildroot}%{_datadir}/licenses/%{name}/NOTICE

%files
%license %{_datadir}/licenses/%{name}/LICENSE
%license %{_datadir}/licenses/%{name}/NOTICE
%{_bindir}/ttfx
%{_datadir}/bash-completion/completions/ttfx
%{_datadir}/zsh/site-functions/_ttfx

%changelog
* Sun Sep 27 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR build from upstream release tag
