# Material Symbols (Rounded) — font ikon yang dipakai shell Caelestia untuk
# menggambar seluruh glyph-nya (bar, launcher, control centre). Tidak ada repo
# yang menyediakannya, jadi dibangun di sini langsung dari variable font di
# repository upstream.
#
# Hanya gaya Rounded yang dikirim: itulah satu-satunya yang di-hardcode
# Caelestia ("Material Symbols Rounded", dibaca dari libcaelestia-config.so).
# Kerabat Outlined dan Sharp di repository yang sama masing-masing ~15 MB dan
# tidak ada paket kita yang memintanya.
#
# Nama keluarga font ini berasal dari name-table di dalam TTF, jadi tidak perlu
# file fontconfig sendiri: fontconfig mengenalinya begitu file mendarat di
# /usr/share/fonts.

Name:           material-symbols-fonts
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Material Symbols Rounded variable icon font (Google)

License:        Apache-2.0
URL:            https://github.com/google/material-design-icons
Source0:        MaterialSymbolsRounded-VF.ttf
Source1:        LICENSE

BuildArch:      noarch
Requires:       fonts-filesystem

%description
Material Symbols Rounded adalah font ikon variable dari Google, generasi
terbaru dari set ikon Material Design. Di dalamnya ada glyph ikon yang dipakai
shell desktop Caelestia untuk menggambar bar, launcher, dan control
centre-nya, dan font ini wajib ada supaya shell itu bisa tampil: tanpa
keluarga font-nya, setiap ikon keluar sebagai kotak glyph-hilang.

Paket ini hanya mengirim gaya Rounded, diambil dari direktori variablefont/ di
google/material-design-icons.

%prep
# Tidak ada yang perlu di-unpack: sourcenya adalah file font itu sendiri.

%build
# Tidak ada yang perlu dibangun: font dikirim apa adanya.

%install
# /usr/share/fonts diawasi file trigger milik fontconfig (transfiletriggerin),
# jadi fc-cache jalan sendiri saat paket dipasang maupun dilepas — tidak perlu
# scriptlet apa pun di sini.
install -d %{buildroot}%{_datadir}/fonts/material-symbols
install -pm 0644 %{SOURCE0} \
    %{buildroot}%{_datadir}/fonts/material-symbols/MaterialSymbolsRounded-VF.ttf
# Lisensi dipasang eksplisit: tidak ada %prep yang meng-unpack, jadi tidak ada
# file di direktori build yang bisa ditunjuk %license LICENSE.
install -d %{buildroot}%{_licensedir}/%{name}
install -pm 0644 %{SOURCE1} %{buildroot}%{_licensedir}/%{name}/LICENSE

%files
%license %{_licensedir}/%{name}/LICENSE
%{_datadir}/fonts/material-symbols/MaterialSymbolsRounded-VF.ttf

%changelog
* Fri Oct 09 2026 tofan79 <tofan79@users.noreply.github.com> - %{pkg_version}-1
- Paket baru: Material Symbols Rounded (variable) dari
  google/material-design-icons, buat menutup font yang hilang di RakuOS —
  tanpa ini semua ikon shell Caelestia tampil sebagai kotak.
