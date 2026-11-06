# ario: terminal download manager berbasis aria2 (Rust, MIT). Upstream
# menerbitkan RPM x86_64 di setiap rilis, jadi spec ini me-repack RPM itu
# (binary `ario` + daemon `ario_daemon`) alih-alih mengompilasi workspace
# Cargo-nya di chroot COPR.
#
# Pola yang sama dengan `nuclear`, `sonora`, dan `zapfast` di repo ini.

Name:           ario
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Terminal download manager powered by aria2
License:        MIT
URL:            https://github.com/peymanAzad/ario
Source0:        ario-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

# Rilis upstream hanya menyediakan RPM x86_64.
ExclusiveArch:  x86_64

# aria2 tidak di-link, tapi dijalankan sebagai proses terpisah (RPC JSON);
# ca-certificates dipakai untuk unduhan HTTPS. Keduanya ditulis eksplisit
# karena tidak akan muncul sebagai soname.
Requires:       aria2
Requires:       ca-certificates

%description
Ario is a batteries-included terminal download manager built on aria2. It
combines a TUI (ratatui) with a managed daemon, so downloads and scheduled
queues keep running after the interface is closed, and supports HTTP/HTTPS,
magnet links, and .torrent files in one workflow.

This package repacks the upstream x86_64 RPM; nothing is rebuilt locally.

%prep
%setup -q -n ario-%{version}

%install
install -Dpm0755 usr/bin/ario %{buildroot}%{_bindir}/ario
install -Dpm0755 usr/bin/ario_daemon %{buildroot}%{_bindir}/ario_daemon

# LICENSE dan README.md tidak di-stage ke %{buildroot} di sini: %license dan
# %doc mengambil berkasnya langsung dari direktori build lalu memasangnya ke
# /usr/share/licenses/ario/ dan /usr/share/doc/ario/.

%files
%license LICENSE
%doc README.md
%{_bindir}/ario
%{_bindir}/ario_daemon

%changelog
* Fri Nov 06 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package, repacked from the upstream x86_64 RPM.
