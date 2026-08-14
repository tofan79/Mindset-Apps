%global debug_package %{nil}

Name:           software-center
Version:        1.1.0
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
# AppImage support — archive extraction, AppImage runtime, desktop-file refresh
Requires:       unzip
Requires:       7zip
Requires:       tar
Requires:       coreutils
# AppImage delta updates (.zsync). Falls back to full download when absent.
Requires:       zsync
# Backend helpers — dnf process detection, desktop-file cache update
Requires:       procps-ng
Requires:       desktop-file-utils

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
* Thu Aug 14 2026 mindset <mindset@users.noreply.github.com> - 1.1.0-1
- Source update otomatis untuk AppImage populer (#5): RPCS3, Eden, DuckStation,
  PCSX2, Youwee terdeteksi otomatis (badge 'auto source'). Perbandingan rilis
  memakai tanggal untuk repo yang tag-nya bukan versi (DuckStation 'latest',
  RPCS3 'build-hash'). AppImage lain tetap bisa ikut auto-update via Detail →
  Update: pilih source (github/gitlab/codeberg/forgejo/url), isi owner/repo +
  pattern, Save Settings.
- Verifikasi checksum SHA256 sebelum install/update AppImage (#6): diambil dari
  release body (termasuk format 'hash;size') atau sidecar (.sha256/.sha256sum);
  update dibatalkan jika tidak cocok, berjalan normal jika tidak tersedia.
- Rollback AppImage ke versi sebelumnya (#7): backup versi lama disimpan setelah
  update; tombol 'Kembali ke versi sebelumnya' di halaman detail mengembalikannya
  (bisa bolak-balik). Backup dibersihkan saat uninstall/cleanup.

* Thu Aug 13 2026 mindset <mindset@users.noreply.github.com> - 1.0.13-1
- AppImage update kini berfungsi penuh di UI: check updates manual menyertakan
  AppImage (sebelumnya `appimages: []` hardcoded), tombol Update per-item /
  Update all / Update section memanggil updateAppImage() yang benar (sebelumnya
  jatuh ke dnf upgrade dan gagal), dan versi setelah update benar (fallback ke
  new_version hasil check saat binary baru tanpa X-AppImage-Version).
- Uninstall AppImage kini menghapus juga preview icon cache local-icons —
  tidak ada sisa file. Re-install mempertahankan update settings (update source/
  URL/pattern) yang sudah diatur pengguna.
- Filter warning log QML QQuickImage (404 ikon Flathub, issue #1) via
  is_noise()/NoiseFilter — log bersih.
- Requires baru untuk AppImage: unzip, 7zip, tar, coreutils, procps-ng,
  desktop-file-utils.
- Clippy bersih seluruh workspace.

* Wed Aug 12 2026 mindset <mindset@users.noreply.github.com> - 1.0.12-1
- Fix tab Flatpak Repositories di Settings selalu kosong ("No Flatpak remotes
  configured") padahal backend benar: assignment hasil parse ditulis sebagai
  `remotes = ...` (bukan `flatpakTab.remotes = ...`) di dalam Timer.onTriggered,
  sehingga QML men-resolve ke global property dan error "Invalid write to global
  property" — data tidak pernah tersimpan. Semua assignment kini di-prefiks
  eksplisit dengan `flatpakTab.` (remotes, hasFlathub, hasFlathubSystem/User,
  hasCosmic*).
- Log aktivitas baru: setiap aksi di-log ke /tmp/software-center/activity.log
  ber-timestamp (navigasi halaman, install/remove/upgrade, repo & remote DNF/
  Flatpak, clean cache, search, detail, local file install) + error QML/Qt
  kini ikut tertangkap ke /tmp/software-center/software-center.log (env_logger
  dialihkan ke file + stderr), jadi masalah bisa didiagnosis tanpa terminal.

* Tue Aug 11 2026 mindset <mindset@users.noreply.github.com> - 1.0.11-1
- Fix freeze UI startup: repoquery --unneeded (dnf5) yang berjalan sinkron saat
  app dibuka (SettingsPage Component.onCompleted) diubah jadi async — tidak
  lagi mengunci UI. Load Installed (runtimes), repositori, dan unused packages
  semua dipindah ke pola async load/poll/read (backend load/poll/read + timer QML).
- Fix deadlock native install/remove: run_scenter_stream (pkexec dnf5 install/remove)
  kini men-drain stderr di thread terpisah — dnf5 yang menulis >64KB ke stderr
  tidak lagi menghentikan proses selamanya saat instal .rpm lokal.
- Optimasi search/browse: get_installed_packages kini pakai SATU `rpm -qa`
  (bukan satu proses rpm per paket) + batch `rpm -q --whatprovides` untuk
  virtual provides — pencarian jauh lebih cepat.
- Optimasi cache repoquery: hapus clear_repo_cache() dari check-update; cache
  hanya invalidasi saat metadata repo benar-benar berubah (repomd.xml lebih baru
  dari cache). Logika freshness repo_cache_fresh diperbaiki (sebelumnya terbalik:
  metadata baru ≥60s justru dianggap fresh).
- Fix unused packages list: repoquery --unneeded kini pakai --qf "%{name}"
  — sebelumnya parsing menampilkan version-release.arch, bukan nama paket.
- Fix icon 404: fallback icon Flathub CDN hanya dipakai untuk app yang benar
  berasal dari remote flathub — app remote lain (cosmic, dst) tidak lagi
  menunjuk URL yang tidak ada.
- Screenshot detail page kini pakai cache:true (tidak re-download tiap buka).
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
