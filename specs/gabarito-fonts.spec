# Gabarito — font variabel (wght 400–900) yang iNiR (shell Quickshell untuk
# Niri) hitung sebagai font "important": tanpa keluarga ini doctor-nya gagal di
# langkah "Checking fonts" dengan "Important fonts missing: Gabarito". Tidak ada
# repo Fedora maupun RakuOS yang menyediakannya — upstream-nya sendiri yang
# mengunduh file ini per-user ke ~/.local/share/fonts saat doctor dijalankan
# (sdata/lib/doctor.sh, cabang "Gabarito"). Karena itu dibangun di sini dari file
# yang sama, supaya font-nya mendarat system-wide lewat paket: ikut terpasang
# dan terlepas bersama shell, tanpa unduhan per-user di tiap mesin.
#
# Nama keluarga font berasal dari name-table di dalam TTF ("Gabarito", id 1),
# jadi tidak perlu file fontconfig sendiri: fontconfig mengenalinya begitu file
# mendarat di /usr/share/fonts, dan file trigger miliknya (transfiletriggerin)
# menjalankan fc-cache sendiri saat paket dipasang maupun dilepas — tidak ada
# scriptlet yang perlu ditulis di sini.

Name:           gabarito-fonts
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Gabarito variable display font (Google Fonts)

License:        OFL-1.1
URL:            https://fonts.google.com/specimen/Gabarito
Source0:        Gabarito-VF.ttf
Source1:        OFL.txt

BuildArch:      noarch
Requires:       fonts-filesystem

%description
Gabarito adalah font variabel bergaya geometric sans dari Google Fonts: satu
file untuk seluruh rentang berat 400–900. iNiR memakai keluarga ini di sebagian
antarmukanya dan doctor-nya menganggapnya wajib, jadi tanpa paket ini teks
shell memakai font pengganti dan laporan doctor gagal di langkah pemeriksaan
font.

Paket ini mengirim file variabel apa adanya dari google/fonts (ofl/gabarito).

%prep
# Tidak ada yang perlu di-unpack: sourcenya adalah file font + lisensinya.

%build
# Tidak ada yang perlu dibangun: font dikirim apa adanya.

%install
install -d %{buildroot}%{_datadir}/fonts/%{name}
install -pm 0644 %{SOURCE0} %{buildroot}%{_datadir}/fonts/%{name}/Gabarito-VF.ttf
# Lisensi dipasang eksplisit: tidak ada %prep yang meng-unpack, jadi tidak ada
# file di direktori build yang bisa ditunjuk %license.
install -d %{buildroot}%{_licensedir}/%{name}
install -pm 0644 %{SOURCE1} %{buildroot}%{_licensedir}/%{name}/OFL.txt

%files
%license %{_licensedir}/%{name}/OFL.txt
%{_datadir}/fonts/%{name}/Gabarito-VF.ttf

%changelog
* Mon Oct 19 2026 tofan79 <tofan79@users.noreply.github.com> - %{pkg_version}-1
- Paket baru: Gabarito (variabel, wght 400–900) dari google/fonts, menutup
  font "important" iNiR yang tidak ada di repo RakuOS/Fedora — tanpa keluarga
  ini doctor iNiR gagal di "Checking fonts".
