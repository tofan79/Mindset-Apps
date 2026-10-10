# Phosphor Icons — font ikon yang dipakai shell Ambxst (modules/theme/
# Icons.qml menggambar glyph-nya dari keluarga "Phosphor"). Tidak ada di
# Fedora (ttf-phosphor-icons adalah paket AUR/Arch), jadi dibangun di sini
# dari semua weight yang dikirim upstream.
#
# Mengirim semua grayscale weight (Bold, Duotone, Fill, Light, Regular,
# Thin) dari direktori src/<weight>/*.ttf. Nama keluarga font diambil dari
# name-table TTF, jadi fontconfig mengenalinya otomatis begitu file mendarat
# di /usr/share/fonts — tanpa file konfigurasi.

Name:           phosphor-icons-fonts
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Phosphor icon family fonts

License:        MIT
URL:            https://github.com/phosphor-icons/web
Source0:        web-%{version}.zip

BuildArch:      noarch
# unzip untuk %prep (arsip ini adalah .zip, bukan tarball).
BuildRequires:  unzip
Requires:       fonts-filesystem

%description
Phosphor adalah set ikon garis yang fleksibel untuk tampilan antarmuka dan
diagram, dengan berat mulai dari regular hingga duotone. Font inilah yang
dipakai shell desktop Ambxst untuk menggambar seluruh glyph-nya (bar,
dashboard, launcher): tanpa keluarga font ini, setiap ikon shell tampil
sebagai kotak glyph-hilang.

Paket ini mengirim enam weight grayscale (Thin, Light, Regular,
Bold, Fill, Duotone) dari repository phosphor-icons/web.

%prep
# %setup zip tidak diandalkan; ekstrak manual pakai unzip (BuildRequires).
%setup -q -c -T
unzip -q %{SOURCE0}
# Nama direktori hasil unzip dari web-2.1.2.zip = web-2.1.2
cd web-%{version}

%build
# Tidak ada yang perlu dibangun: font dikirim apa adanya.

%install
install -d %{buildroot}%{_datadir}/fonts/%{name}
find src -name "*.ttf" \
    -exec install -pm 0644 {} %{buildroot}%{_datadir}/fonts/%{name}/ \;
install -d %{buildroot}%{_licensedir}/%{name}
install -pm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE

%files
%license %{_licensedir}/%{name}/LICENSE
%{_datadir}/fonts/%{name}/*.ttf

%changelog
* Fri Oct 09 2026 tofan79 <tofan79@users.noreply.github.com> - %{pkg_version}-1
- Paket baru: Phosphor icon fonts (web repo tag v2.1.2) dari
  phosphor-icons/web, buat menutup font ikon Ambxst yang tidak ada di Fedora.
- Mengirim enam weight (Thin/Light/Regular/Bold/Fill/Duotone) ke
  %{_datadir}/fonts/phosphor-icons-fonts; fc-cache ditangani file-trigger
  fontconfig, jadi tanpa scriptlet apa pun.