%global pkg_version 0
%global gtk_ref 0000000000000000000000000000000000000000
%global icon_ref 0000000000000000000000000000000000000000

Name:           colloid-theme
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Colloid GTK and icon themes
License:        GPL-3.0-only
URL:            https://github.com/vinceliuice/Colloid-gtk-theme
Source0:        colloid-gtk-theme-%{gtk_ref}.tar.gz
Source1:        colloid-icon-theme-%{icon_ref}.tar.gz

BuildArch:      noarch
BuildRequires:  sassc
BuildRequires:  gtk-update-icon-cache
Requires:       gtk3
Requires:       hicolor-icon-theme

%description
Colloid is a modern GTK theme and icon theme for Linux desktops. This package
installs the complete GTK 3 and GTK 4 named variant matrix together with the
complete Colloid icon variant matrix. All assets are installed system-wide and
can be selected by their variant names.

%prep
%setup -q -n colloid-gtk-theme-%{gtk_ref}

mkdir -p ../colloid-icon-theme-%{icon_ref}
tar -xf %{SOURCE1} -C ../colloid-icon-theme-%{icon_ref} --strip-components=1

%build

%install
install -d %{buildroot}%{_datadir}/themes
install -d %{buildroot}%{_datadir}/icons
install -d %{buildroot}%{_datadir}/colloid-build-home
install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/gtk-update-icon-cache <<'EOF'
#!/bin/sh
exit 0
EOF
chmod 0755 %{buildroot}%{_bindir}/gtk-update-icon-cache

PATH="%{buildroot}%{_bindir}:$PATH" \
HOME=%{buildroot}%{_datadir}/colloid-build-home \
XDG_DATA_HOME=%{buildroot}%{_datadir} \
  ./install.sh \
    --dest %{buildroot}%{_datadir}/themes \
    --theme all \
    --color standard light dark \
    --size standard compact \
    --tweaks all

for theme in %{buildroot}%{_datadir}/themes/Colloid*; do
  [ -d "$theme" ] || continue
  case "${theme##*/}" in
    *-hdpi|*-xhdpi) rm -rf "$theme"; continue ;;
  esac
  for component in "$theme"/*; do
    case "${component##*/}" in
      gtk-3.0|gtk-4.0|index.theme) ;;
      *) rm -rf "$component" ;;
    esac
  done
done

PATH="%{buildroot}%{_bindir}:$PATH" \
HOME=%{buildroot}%{_datadir}/colloid-build-home \
XDG_DATA_HOME=%{buildroot}%{_datadir} \
  ../colloid-icon-theme-%{icon_ref}/install.sh \
    --dest %{buildroot}%{_datadir}/icons \
    --theme all \
    --scheme all \
    --alternative \
    --kde-plasma \
    --bold

rm -f %{buildroot}%{_bindir}/gtk-update-icon-cache
rm -rf %{buildroot}%{_datadir}/colloid-build-home

for theme in %{buildroot}%{_datadir}/icons/Colloid*; do
  [ -d "$theme" ] || continue
  rm -f "$theme/icon-theme.cache"
done

install -Dpm0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE.GTK
install -Dpm0644 ../colloid-icon-theme-%{icon_ref}/LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE.icons

%post
for theme in %{_datadir}/icons/Colloid*; do
  [ -d "$theme" ] || continue
  gtk-update-icon-cache -q -t -f "$theme" || :
done

%postun
if [ "$1" -eq 0 ]; then
  for theme in %{_datadir}/icons/Colloid*; do
    [ -d "$theme" ] || continue
    gtk-update-icon-cache -q -t -f "$theme" || :
  done
fi

%files
%{_datadir}/themes/Colloid*
%{_datadir}/icons/Colloid*
%license %{_datadir}/licenses/%{name}/LICENSE.GTK
%license %{_datadir}/licenses/%{name}/LICENSE.icons

%changelog
* Fri Sep 25 2026 mindset <mindset@copr> - %{pkg_version}-1
- Initial combined package with all Colloid GTK and icon variants
