%global debug_package %{nil}

Name:           software-center
Version:        1.0.11
Release:        1%{?dist}
Summary:        Software Center — install and manage apps, Flatpaks, and system updates

License:        GPL-3.0-or-later
URL:            https://github.com/tofan79/software-center
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
* Tue Aug 11 2026 mindset <mindset@users.noreply.github.com> - 1.0.11-1
- Fix freeze UI startup: repoquery --unneeded (dnf5) yang berjalan sinkron saat
  app dibuka (SettingsPage Component.onCompleted) diubah jadi async — tidak
  lagi mengunci UI. Load Installed (runtimes), repositori, dan unused packages
  semua dipindah ke pola async load/poll/read.
- Fix deadlock native install/remove: run_scenter_stream (pkexec dnf5) kini
  men-drain stderr di thread terpisah — dnf5 yang menulis >64KB ke stderr tidak
  lagi menggantung saat instal .rpm lokal.
- Optimasi search/browse: get_installed_packages kini pakai SATU `rpm -qa`
  (bukan satu proses rpm per paket) + batch --whatprovides untuk virtual
  provides — pencarian jauh lebih cepat.
- Optimasi cache repoquery: clear_repo_cache() dihapus dari check-update; cache
  hanya invalidasi saat metadata repo benar-benar berubah. Logika freshness
  diperbaiki (sebelumnya terbalik).
- Fix unused packages: repoquery --unneeded pakai --qf "%{name}" (sebelumnya
  menampilkan version-release.arch, bukan nama).
- Fix icon 404: fallback Flathub CDN hanya untuk app dari remote flathub.
- Screenshot detail page cache:true (tidak re-download tiap buka).
- Hapus dead code: install_stream (packages), install_ref_stream (flatpak).

* Sat Aug 08 2026 mindset <mindset@users.noreply.github.com> - 1.0.10-1
- Detail page: dropdown pilihan sumber (Fedora (DNF) / Flathub System/User)
  kini disembunyikan saat aplikasi sudah terinstall — cukup tombol Remove.
  Sebelumnya dropdown tetap muncul walau app sudah terinstall.

* Sat Aug 08 2026 mindset <mindset@users.noreply.github.com> - 1.0.9-1
- Label sumber native di dropdown install kini "Fedora (DNF)" agar jelas
  membedakannya dari "Flathub (System)" / "Flathub (User)".

* Sat Aug 08 2026 mindset <mindset@users.noreply.github.com> - 1.0.8-1
- Fix: opsi sumber native (Fedora) untuk paket yang tidak ada di repo
  manapun kini disembunyikan — sebelumnya muncul lalu install gagal
  "package not found" (kasus: Spotify mapping ke spotify-client yang
  tidak tersedia; kini dipetakan ke spotify-launcher dari Terra).
- Safety net: opsi native hanya ditampilkan bila paket terinstall ATAU
  tersedia di salah satu repo aktif (build_sources + enrich_sources).

* Sat Aug 08 2026 mindset <mindset@users.noreply.github.com> - 1.0.7-1
- Cache search repoquery kini otomatis basi saat metadata repo dnf5 berubah
  (misal COPR selesai build), tidak lagi menunggu TTL 4 jam.
- "Check for updates" menghapus cache repoquery sekalian, jadi hasil search
  langsung memuat paket baru (contoh: paket COPR yang baru rilis).
- Hapus cache manual via rm tidak lagi diperlukan.

* Sat Aug 08 2026 mindset <mindset@users.noreply.github.com> - 1.0.6-1
- Perbaiki sinkronisasi CLI/GUI: semua query dnf5 read-only
  (check-update, list --installed, repoquery, repo list) kini pakai
  --skip-file-locks sehingga tidak lagi berebut /var/lib/dnf/system-repo.lock
  dengan `dnf upgrade` dari terminal.
- Perbaiki tray beku: update check daemon dijalankan di task terpisah,
  message loop tetap responsif untuk Open/Quit; trigger refresh UI ditulis
  setelah cache selesai.
- Tambah timeout 20s pada pengecekan GNOME extension (sebelumnya bisa
  menggantung tanpa batas).
- Daemon kini memverifikasi PID UI via cmdline (bukan hanya /proc), jadi
  pid file basi tidak lagi membuat "Open Software Center" diam saja.

* Sat Aug 08 2026 mindset <mindset@users.noreply.github.com> - 1.0.5-1
- Perbaiki deteksi installed (desktop file + mapping flatpak-to-rpm):
  Telegram & Zed kini akurat di Installed/Home/detail.
- Grid/List toggle + sort (nama, terbaru update, installed first) di
  halaman kategori dan halaman sumber DNF/Flatpak.
- Halaman sidebar baru DNF & Flatpak; picker install sumber dikontekstualisasi
  (DNF page -> native saja, Flatpak page -> flatpak System/User).
- Field "updated" (tanggal rilis AppStream) diisi dari atribut date/timestamp.
- Search dirapikan: tab DNF | Flatpak (AppImage tab dihapus).

* Fri Aug 07 2026 mindset <mindset@users.noreply.github.com> - 1.0.4-1
- Search lintas repo (DNF/COPR/Terra/RPM Fusion/Brave) + badge Installed.
- Hasil search dikelompokkan DNF/Flatpak/AppImage (gaya Shelly), sumber
  yang diklik langsung dipakai untuk install.
- Installed hanya menampilkan aplikasi GUI nyata (filter component_type).
- AppImage: update atomik dengan backup+rollback, verifikasi ELF/arsitektur,
  provider Codeberg/Forgejo, dan opsi allow-prerelease per aplikasi.

* Wed Aug 05 2026 mindset <mindset@users.noreply.github.com> - 1.0.0-1
- Initial Software Center package: Qt6/QML frontend + tray daemon.
- Replaces the legacy rakuos-software package (webapps, KNS add-ons, and
  the GTK/COSMIC frontends are removed).
