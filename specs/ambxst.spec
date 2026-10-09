# Ambxst: shell desktop Wayland berbasis Quickshell (daemon Go + pohon QML).
# Backend murni Go dengan seluruh dependency sudah di-vendor upstream
# (backend/vendor, ter-commit di git), jadi `go build -mod=vendor` jalan
# offline, tanpa CGO, tanpa library C.
#
# Menemukan pohon shell: daemon mencari via $AMBXST_SHELL dulu, lalu dir
# binary, lalu ~/.local/share/ambxst/shell_repo (installer), dst — urutan
# lengkap di backend/pkg/paths/shell_source.go (FindBaseShellSource).
# Karena RPM menaruh binary di /usr/libexec dan data di /usr/share/ambxst,
# pasangan wrapper di /usr/bin mengekspor AMBXST_SHELL ke datadir.
#
# Versi: file `version` di source tidak terpakai oleh binary RPM
# (readVersion() membaca dua level di atas executable, bukan datadir),
# jadi main.version di-tanam lewat ldflags -X, pola sama dengan Nix
# (backend.nix).

Name:           ambxst
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Axtremely customizable Quickshell desktop shell with Go daemon

License:        AGPL-3.0-or-later
URL:            https://github.com/Axenide/Ambxst
Source0:        %{name}-%{version}.tar.gz

# Backend Go. go.mod menuntut "go 1.26.0"; kalau chroot lawas (fc44/fc45)
# masih punya golang < 1.26, build bakal menolak direktif itu di awal —
# beri tahu via log COPR, lalu opsi: turunkan direktif di %prep (kalau
# kodenya kompatibel) atau jalankan chroot yang golang-nya cukup.
BuildRequires:  golang

# Module QML org.kde.syntaxhighlighting (dipakai CodeBlock.qml di sidebar AI)
# harus ada di runtime, kalau tidak `qs` gagal load shell.qml dengan
# "module org.kde.syntaxhighlighting is not installed". Berbeda dari
# quickshell/axctl/wl-clipboard yang sengaja manual (lihat konteks runtime
# bawah), modul ini WAJIB untuk shell bisa tampil, jadi dijadikan Requires.
Requires:       kf6-syntax-highlighting

# Tanpa baris ini `find-debuginfo` snap: binary daemon di-strip (-s -w, pola
# sama backend.nix upstream) tanpa DWARF sama sekali, dan datadir ikut membawa
# ELF helper lockscreen ambxst-auth (commit upstream) yang menyulap build jadi
# "Empty %files file debugsourcefiles.list". Tidak ada debug yang hilang —
# paket sengaja dibangun stripped.
%global debug_package %{nil}

%description
Ambxst is a highly customizable Wayland shell built on Quickshell: a unified
panel (bar, dock, notch), dashboard, lockscreen, desktop widgets,
notifications, and a reactive JSON configuration system — all driven by a
single Go daemon that supervises Quickshell, axctl and wl-paste.

# --- Konteks runtime; sengaja BUKAN Requires (pola sama caelestia-shell
# --- supaya `rum install ambxst` tidak menarik apa pun):
#   - quickshell (qs): dipasang manual, COPR errornointernet/quickshell,
#     tidak ada di Fedora.
#   - axctl (CLI compositor punya Axenide): dipakai daemon untuk brightness,
#     screen dan IPC compositor; tanpa itu fitur-fitur tersebut error ramah.
#   - wl-clipboard (wl-paste/wl-copy): clipboard watcher yang dibimbing daemon.
#   - Alat fitur opsional (nmcli, tesseract, ffmpeg, gpu-screen-recorder,
#     systemctl/loginctl, notify-send, gsettings, dbus-send, sqlite3, git)
#     hanya dipanggil saat fiturnya dipakai.
# Ambxst sendiri butuh compositor Hyprland di level lingkungan (axctl = abstraksi
# IPC Hyprland), bukan dependensi paket.
# Pengecualian: kf6-syntax-highlighting adalah Requires di atas karena modul
# QML-nya wajib untuk shell dapat dimuat (error "module not installed").

%prep
%setup -q -n Ambxst-%{version}

%build
cd backend
go build -mod=vendor -trimpath \
    -ldflags "-s -w -X main.version=%{version}" \
    -o %{_builddir}/ambxst-bin ./cmd/ambxst

%install
mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{_libexecdir} \
         %{buildroot}%{_datadir}/ambxst
install -m0755 %{_builddir}/ambxst-bin %{buildroot}%{_libexecdir}/ambxst

cat > %{buildroot}%{_bindir}/ambxst <<'EOF'
#!/bin/sh
export AMBXST_SHELL=%{_datadir}/ambxst
exec %{_libexecdir}/ambxst "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/ambxst

# Pohon shell yang dilempar ke qs: shell.qml, modules/, config/
# (defaults/*.js), assets/ (termasuk preset "Ambxst Default"),
# translations/ (json), scripts/ (google_lens.sh dipanggil Screenshot.qml),
# dan file `version` (dibaca ValidateModGeneration + preset).
cp -a shell.qml modules config assets translations scripts version \
       %{buildroot}%{_datadir}/ambxst/

%files
%license LICENSE
%doc README.md
%{_bindir}/ambxst
%{_libexecdir}/ambxst
%{_datadir}/ambxst/

%changelog
* Fri Oct 09 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial COPR packaging of ambxst.
- Backend Go dibangun dari source tag upstream dengan -mod=vendor (deps
  ter-vendor in-tree) dan main.version ditanam via ldflags; shell QML,
  config, assets, translations, scripts dan version dipasang ke
  %{_datadir}/ambxst.
- Wrapper /usr/bin/ambxst mengekspor AMBXST_SHELL ke datadir; binary asli
  di /usr/libexec/ambxst. Runtime quickshell/axctl/wl-clipboard sengaja
  manual, tidak dijadikan Requires.
- Tambah Requires: kf6-syntax-highlighting — module QML org.kde.
  syntaxhighlighting wajib agar qs dapat memuat shell.qml (CodeBlock.qml);
  tanpa itu shell mogok total (bukan opsi seperti runtime manual lain).