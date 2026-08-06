%global debug_package %{nil}

Name:           software-center
Version:        1.0.0
Release:        1%{?dist}
Summary:        Software Center — install and manage apps, Flatpaks, and system updates

License:        GPL-3.0
# TODO: set the real project homepage before publishing
URL:            https://example.invalid/software-center
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  dbus-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel

Requires:       qt6-qtbase
Requires:       qt6-qtdeclarative
Requires:       qt6-qtwayland
Requires:       flatpak
Requires:       dnf5
Requires:       polkit
Requires:       rpm
Requires:       appstream
Requires:       appstream-data

%description
Software Center is a modern app store for Fedora and derivatives. It lets you
browse and install Flatpaks from Flathub, manage native RPM packages, install
AppImages, and keep your system up to date. A background tray daemon checks for
updates and shows update counts in the system tray.

%prep
%autosetup -n %{name}-%{version}

%build
cargo build --release --locked

%install
# Binaries
install -Dm755 target/release/software-center %{buildroot}%{_bindir}/software-center
install -Dm755 target/release/software-center-tray %{buildroot}%{_bindir}/software-center-tray

# QML frontend
install -dm755 %{buildroot}%{_datadir}/software-center/qml
cp -r crates/ui-qt/qml/* %{buildroot}%{_datadir}/software-center/qml/

# AppStream overrides + bundled appdata
install -dm755 %{buildroot}%{_datadir}/software-center/appstream/data
install -m644 resources/appstream/appstream-overrides.json \
    %{buildroot}%{_datadir}/software-center/appstream/
install -m644 resources/appstream/flatpak-to-rpm.json \
    %{buildroot}%{_datadir}/software-center/appstream/
install -m644 resources/appstream/data/*.xml \
    %{buildroot}%{_datadir}/software-center/appstream/data/
install -dm755 %{buildroot}%{_datadir}/software-center/appstream/icons
install -m644 resources/appstream/icons/*.png \
    %{buildroot}%{_datadir}/software-center/appstream/icons/

# Icon + desktop entries
install -Dm644 resources/software-center.png \
    %{buildroot}%{_datadir}/pixmaps/software-center.png
install -Dm644 resources/software-center.desktop \
    %{buildroot}%{_datadir}/applications/software-center.desktop
install -Dm644 resources/software-center-tray.desktop \
    %{buildroot}%{_sysconfdir}/xdg/autostart/software-center-tray.desktop

%files
%license LICENSE
%doc README.md
%{_bindir}/software-center
%{_bindir}/software-center-tray
%{_datadir}/software-center/qml/
%{_datadir}/software-center/appstream/
%{_datadir}/pixmaps/software-center.png
%{_datadir}/applications/software-center.desktop
%{_sysconfdir}/xdg/autostart/software-center-tray.desktop

%changelog
* Wed Aug 05 2026 mindset <mindset@users.noreply.github.com> - 1.0.0-1
- Initial Software Center package: Qt6/QML frontend + tray daemon.
- Replaces the legacy rakuos-software package (webapps, KNS add-ons, and
  the GTK/COSMIC frontends are removed).
