# Phosphor Icons — font ikon yang dipakai shell Ambxst (modules/theme/
# Icons.qml menggambar glyph-nya dari keluarga "Phosphor"). Tidak ada di
# Fedora (ttf-phosphor-icons adalah paket AUR/Arch), jadi dibangun di sini
# dari semua weight yang dikirim upstream.

Name:           phosphor-icons-fonts
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Phosphor icon family fonts

License:        MIT
URL:            https://github.com/phosphor-icons/web
Source0:        web-%{version}.zip

BuildArch:      noarch
BuildRequires:  unzip
Requires:       fonts-filesystem

%description
Phosphor adalah set ikon garis yang fleksibel untuk tampilan antarmuka dan
diagram, dengan berat mulai dari regular hingga duotone.

%prep
%setup -q -c -T
unzip -q %{SOURCE0}

%build

%install
install -d %{buildroot}%{_datadir}/fonts/%{name}
find web-%{version}/src -name "*.ttf" \
    -exec install -pm 0644 {} %{buildroot}%{_datadir}/fonts/%{name}/ \;
install -d %{buildroot}%{_licensedir}/%{name}
install -pm 0644 web-%{version}/LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE

%files
%license %{_licensedir}/%{name}/LICENSE
%{_datadir}/fonts/%{name}/*.ttf

%changelog
* Fri Oct 09 2026 tofan79 <tofan79@users.noreply.github.com> - %{pkg_version}-1
- Initial packaging of Phosphor Icons fonts.
