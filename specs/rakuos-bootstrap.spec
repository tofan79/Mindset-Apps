# rakuos-bootstrap: Wizard pasca-install untuk RakuOS minimal.
#
# Wizard menambah desktop, login manager, terminal, browser, dan file manager
# ke image minimal tanpa mengganti installer OS. Paket ini sengaja tidak
# menyalakan unit `rakuos-bootstrap.service`; derived image yang enable.

%global debug_package        %{nil}

Name:           rakuos-bootstrap
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Wizard pasca-install untuk RakuOS minimal
License:        MIT
URL:            https://github.com/tofan79/rakuos-bootstrap
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  systemd-rpm-macros
BuildRequires:  gcc
BuildRequires:  pkgconf-pkg-config

%description
Wizard terminal (TUI) untuk menambahkan terminal, browser, file manager,
desktop Wayland, dan login manager ke image RakuOS minimal. Perubahan host
ditulis ke /etc dan $HOME user, paket dipasang lewat rum.

%prep
%autosetup -n %{name}-%{version}

%build
cargo build --release --locked

%install
install -Dpm0755 target/release/%{name} \
    %{buildroot}%{_bindir}/%{name}

install -d %{buildroot}%{_datadir}/rakuos/bootstrap
cp -a data/catalog.toml %{buildroot}%{_datadir}/rakuos/bootstrap/catalog.toml
cp -a data/skel %{buildroot}%{_datadir}/rakuos/bootstrap/
cp -a data/sessions %{buildroot}%{_datadir}/rakuos/bootstrap/
install -Dpm0644 data/rakuos-bootstrap.service \
    %{buildroot}/usr/lib/systemd/system/rakuos-bootstrap.service

%post
%systemd_post rakuos-bootstrap.service

%preun
%systemd_preun rakuos-bootstrap.service

%postun
%systemd_postun_with_restart rakuos-bootstrap.service

%files
%{_bindir}/rakuos-bootstrap
%dir %{_datadir}/rakuos
%dir %{_datadir}/rakuos/bootstrap
%{_datadir}/rakuos/bootstrap/catalog.toml
%{_datadir}/rakuos/bootstrap/skel/
%{_datadir}/rakuos/bootstrap/sessions/
/usr/lib/systemd/system/rakuos-bootstrap.service

%changelog
* Sat Oct 31 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial packaging for rakuos-bootstrap from GitHub release tag.