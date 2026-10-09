# axctl: daemon CLI kompositor dari Axenide (pengaruh ambxst/Ax-Shell).
# Membaca ~/.config/axctl/config.toml, menghasilkan file konfigurasi kompositor
# (mis. hyprland.lua untuk ambxst), menangani brightness/layar/idle, dan
# subscribe ke event kompositor. Single binary Go, tanpa CGO.
#
# Buru go.mod menuntut "go 1.27.1" sedangkan chroot COPR fc44 maksimum golang
# 1.26.x — direktif diturunkan ke 1.26 di %prep (kode tidak memakai fitur Go
# 1.27; deps fsnotify/go-toml/x-sys semuanya di bawah 1.26). Kalau chroot
# nanti punya golang >= 1.27, sed ini hanya no-op. Sama dengan catatan go
# version di ambxst.spec.
#
# Grup 'input': axctl punya keymon (modifier-alone binds via /dev/input).
# Itu fitur OPTIONAL — daemon tetap jalan tanpa grup itu. Installer upstream
# hanya menambah user ke grup 'input' (bukan menyertakan grup), jadi RPM
# tidak me-nek-kan grup; baca catatan di bawah %description tentang
# usermod manual untuk mengaktifkan fitur tersebut.
#
# Versi: tag upstream pakai prefix "v" (v0.0.29). Source diambil dari arsip
# git tag (release tidak punya tarball source). main.go membaca main.Version
# via -ldflags -X, pola sama backend ambxst.

Name:           axctl
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Axtremely flexible compositor daemon/CLI (config + brightness + IPC)

License:        AGPL-3.0-or-later
URL:            https://github.com/Axenide/axctl
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  golang

# Binary daemon di-strip (-s -w) tanpa DWARF; tidak ada debug info yang
# hilang. Sama alasan dengan ambxst.spec.
%global debug_package %{nil}

%description
axctl is a compositor configuration daemon and CLI: it watches a reactive
TOML config (~/.config/axctl/config.toml), renders compositor config files
(for example hyprland.lua used by ambxst), and exposes IPC for brightness,
screen, idle, darkmode and layout control. It is the companion tool of the
ambxst shell.

Runtime is manual (pola sama ambxst):
  - compositor (Hyprland/KWin/etc): di level lingkungan, bukan dep paket.
  - ambxst: dipasang terpisah; kalau tidak ada, axctl tetap jalan sendiri.
Fitur optional yang diaktifkan saat binary tersedia di PATH: wl-clipboard,
systemctl/loginctl, notify-send, dll (dipanggil hanya saat fiturnya aktif).

Untuk modifier-alone binds (keymon), tambahkan user daemon ke grup "input"
(installer upstream melakukan ini secara manual):
    sudo usermod -aG input $USER
Tanpa itu, axctl tetap berfungsi penuh untuk config/brightness/layar/IPC.

%prep
%setup -q -n %{name}-%{version}
# Turunkan direktif go supaya bisa dibangun dengan golang tersedia di chroot
# fc44 (maks 1.26.x). Perhatikan baris 'go 1.27.1' di go.mod.
sed -i 's/^go 1\.[0-9][0-9]*\.[0-9][0-9]*$/go 1.26/' go.mod

%build
go build -mod=mod -trimpath \
    -ldflags "-s -w -X main.Version=%{version}" \
    -o %{_builddir}/axctl-bin .

%install
install -Dm0755 %{_builddir}/axctl-bin %{buildroot}%{_bindir}/axctl

%files
%license LICENSE
%doc README.md
%{_bindir}/axctl

%changelog
* Fri Oct 09 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial COPR packaging of axctl.
- Single Go binary dibangun dari arsip git tag v0.0.29 dengan -mod=mod
  (deps di-fetch via proxy); main.Version ditanam via ldflags; go.mod
  diturunkan 1.27.1 -> 1.26 di %prep (kode kompatibel).
- Paket hanya binary; config TOML diletakkan user di ~/.config/axctl
  (opsional). Grup 'input' untuk modifier-alone binds TIDAK dibuat otomatis
  oleh RPM — dijelaskan di %description (usermod manual).