Name:           whitesur-gtk-theme
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        A macOS Big Sur/Monterey like theme for GTK based desktops
License:        MIT
URL:            https://github.com/vinceliuice/WhiteSur-gtk-theme
Source0:        whitesur-%{version}.tar.gz

%global pkg_srcver 2026-09-10
%global debug_package %{nil}

BuildArch:      noarch

%description
WhiteSur is a macOS Big Sur/Monterey style theme for GTK based desktop
environments. It ships ready-rendered themes for GTK2/GTK3/GTK4, metacity,
xfwm4, cinnamon, gnome-shell, unity and plank.

Window control buttons follow the macOS layout (close, minimize, maximize)
rendered as traffic lights. An optional libadwaita override is provided by
the upstream project and can be applied per user with the installer.

%prep
%setup -q -n WhiteSur-gtk-theme-%{pkg_srcver}

%install
install -d %{buildroot}%{_datadir}/themes
for variant in Dark Light; do
    tar -xJf "release/WhiteSur-${variant}.tar.xz" -C %{buildroot}%{_datadir}/themes
done

%files
%{_datadir}/themes/WhiteSur-Dark/
%{_datadir}/themes/WhiteSur-Light/

%changelog
* Sat Sep 12 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial COPR package of the WhiteSur GTK theme