Name:           singularity-greeter-setup
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        greetd session setup for Singularity Desktop
License:        MIT
URL:            https://github.com/singularityos-lab/packaging
BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
Source0:        singularity-greeter-session
Source1:        config.toml
Source2:        labwc-locked-rc.xml
Source3:        labwc-locked-menu.xml
Source4:        singularity-greeter.sysusers
Source5:        singularity-greeter.tmpfiles
Source6:        LICENSE
Requires:       greetd
Requires:       singularity-greeter
Requires:       singularity-labwc
Requires:       dbus-daemon

%description
Installs the greetd session wrapper and locked labwc configuration for the
Singularity greeter. It does not enable greetd or replace another display
manager; activation is left to the administrator or RakuOS bootstrap.

%prep
%setup -q -c -T

%build

%install
install -Dpm0755 %{SOURCE0} %{buildroot}%{_libexecdir}/singularity-greeter/session
install -Dpm0644 %{SOURCE1} %{buildroot}%{_datadir}/greetd/singularity-greeter.toml
install -Dpm0644 %{SOURCE2} %{buildroot}%{_datadir}/singularity/greeter/labwc-locked/rc.xml
install -Dpm0644 %{SOURCE3} %{buildroot}%{_datadir}/singularity/greeter/labwc-locked/menu.xml
install -Dpm0644 %{SOURCE4} %{buildroot}%{_sysusersdir}/singularity-greeter.conf
install -Dpm0644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/singularity-greeter.conf
install -Dpm0644 %{SOURCE6} %{buildroot}%{_licensedir}/%{name}/LICENSE

%files
%license %{_licensedir}/%{name}/LICENSE
%{_libexecdir}/singularity-greeter/session
%{_datadir}/greetd/singularity-greeter.toml
%{_datadir}/singularity/greeter/labwc-locked/rc.xml
%{_datadir}/singularity/greeter/labwc-locked/menu.xml
%{_sysusersdir}/singularity-greeter.conf
%{_tmpfilesdir}/singularity-greeter.conf

%changelog
* Fri Oct 30 2026 Tofan79 <nanasmuda.404@outlook.co.id> - %{version}-1
- Initial Mindset-Apps package for the Singularity greetd session glue.
