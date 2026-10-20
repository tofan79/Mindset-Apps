# sysc-greet: greeter TUI untuk greetd (Go + Bubble Tea, GPL-3.0).
#
# Varian yang dipakai di image Hyprland adalah **cagebreak**, bukan varian
# Hyprland: upstream men-deprecate varian Hyprland dan menggantinya dengan
# cagebreak yang lebih stabil. Sesi login tetap Hyprland — cagebreak hanya
# compositor kecil tempat layar login digambar, lalu keluar setelah login.
#
# Upstream menginstal binary ke /usr/local/bin dan dua config yang menunjuk ke
# path itu. RPM tidak boleh menulis ke /usr/local, jadi spec ini memindahkan
# binary ke /usr/bin dan menyesuaikan config yang ikut dipasang. Config
# compositor lain (niri, sway, mango, hyprland-legacy) tidak dipasang: yang
# dipakai image ini hanya cagebreak.
#
# Lisensi: kode GPL-3.0-only, tetapi binary menyertakan aset model AK-47
# berlisensi CC-BY-NC-4.0 (lihat THIRD_PARTY_NOTICES.md). Karena itu License
# menulis keduanya.
#
# Yang sengaja TIDAK dilakukan paket ini: menyentuh /etc/greetd/config.toml.
# Itu tugas `rakuos-hyprland greeter sysc-greet`, yang menyimpan backup dan
# menulis baris command sebelum greetd diarahkan ke sini.

%global debug_package %{nil}

Name:           sysc-greet
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Greeter TUI untuk greetd di atas cagebreak

License:        GPL-3.0-only AND CC-BY-NC-4.0
URL:            https://github.com/Nomadcxx/sysc-greet
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  golang
BuildRequires:  systemd-rpm-macros

# cagebreak: compositor layar login (varian yang dipertahankan upstream).
# socat: menutup cagebreak lewat IPC socket setelah login, tanpa itu greetd
#        menunggu selamanya dan layar terlihat "stuck".
# ghostty: terminal tempat TUI digambar. Image ini sudah memakainya, jadi tidak
#        perlu menarik kitty (beserta xterm/libXaw/ripgrep) hanya untuk layar
#        login. Semua keybind dimatikan (`--keybind=clear`) supaya tidak ada
#        jalan pintas keluar dari greeter.
Requires:       greetd
Requires:       cagebreak
Requires:       socat
Requires:       ghostty

%description
sysc-greet menggambar layar login greetd sebagai antarmuka teks: ASCII art,
tema, jam, dan daftar sesi, semuanya di dalam terminal yang berjalan di
compositor kecil (cagebreak). Dipakai sebagai opsi keempat di
`rakuos-hyprland greeter`, untuk mesin yang stack grafisnya sedang bermasalah.

Alur runtime:

  greetd      -> cagebreak -e -c /etc/greetd/cagebreak-greeter-config
  cagebreak   -> ghostty --keybind=clear -e sysc-greet
  sysc-greet  -> (login) -> socat menutup cagebreak -> greetd memulai sesi

Paket ini tidak mengubah /etc/greetd/config.toml. Setelah memasangnya, arahkan
greetd dengan `rakuos-hyprland greeter sysc-greet` (atau edit config.toml
sendiri dan reboot).

%prep
%setup -q -n %{name}-%{version}

%build
go build -mod=mod -trimpath -buildvcs=false \
    -ldflags "-s -w -X main.Version=%{version}" \
    -o sysc-greet ./cmd/sysc-greet/

%install
install -Dm0755 sysc-greet %{buildroot}%{_bindir}/sysc-greet

install -d %{buildroot}%{_datadir}/sysc-greet
# themes/ baru ada setelah tag v1.1.11 (ditambahkan di master), jadi daftar ini
# ditulis sebagai loop: tema tambahan ikut terpasang begitu versi berikutnya
# membawanya, tanpa perlu mengubah spec.
for dir in ascii_configs themes wallpapers fonts; do
    [ -d "$dir" ] && cp -r "$dir" %{buildroot}%{_datadir}/sysc-greet/
done
if [ -f THIRD_PARTY_NOTICES.md ]; then
    install -m0644 THIRD_PARTY_NOTICES.md %{buildroot}%{_datadir}/sysc-greet/
fi

install -d %{buildroot}%{_sysconfdir}/greetd
# Dua penyesuaian pada config compositor bawaan:
#  - binary ada di /usr/bin, bukan /usr/local/bin;
#  - kitty diganti ghostty (tanpa keybind sama sekali) karena image tidak
#    memasang kitty. File kitty.conf bawaan tidak ikut dipasang.
sed -e 's|/usr/local/bin/sysc-greet|%{_bindir}/sysc-greet|g' \
    -e 's|kitty --start-as=fullscreen --config=/etc/greetd/kitty.conf %{_bindir}/sysc-greet|ghostty --gtk-single-instance=false --keybind=clear --fullscreen=true --window-decoration=none --font-family="JetBrainsMono Nerd Font" --font-size=11 -e %{_bindir}/sysc-greet|' \
    config/cagebreak-greeter-config \
    > %{buildroot}%{_sysconfdir}/greetd/cagebreak-greeter-config

install -Dm0644 config/85-greeter.rules \
    %{buildroot}%{_datadir}/polkit-1/rules.d/85-greeter.rules

# Direktori yang dibutuhkan greeter saat login. Dibuat lewat tmpfiles, bukan
# %post, supaya ikut dibuat ulang kalau /var di-reset.
install -d %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/sysc-greet.conf <<'EOF'
d /var/cache/sysc-greet 0755 greeter greeter -
d /var/lib/greeter 0755 greeter greeter -
d /var/lib/greeter/.cache 0755 greeter greeter -
d /var/lib/greeter/.config 0755 greeter greeter -
d /var/lib/greeter/.local 0755 greeter greeter -
d /var/lib/greeter/.local/state 0755 greeter greeter -
d /var/lib/greeter/Pictures 0755 greeter greeter -
d /var/lib/greeter/Pictures/wallpapers 0755 greeter greeter -
EOF

%post
%tmpfiles_create %{_tmpfilesdir}/sysc-greet.conf

%files
%license LICENSE
%doc README.md
%{_bindir}/sysc-greet
%{_datadir}/sysc-greet
%{_datadir}/polkit-1/rules.d/85-greeter.rules
%{_tmpfilesdir}/sysc-greet.conf
%config(noreplace) %{_sysconfdir}/greetd/cagebreak-greeter-config

%changelog
* Tue Oct 20 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Paket COPR pertama sysc-greet, varian cagebreak.
- Binary dipindah dari /usr/local/bin ke %{_bindir}; dua config yang menunjuk
  ke path lama ikut disesuaikan.
- Wallpaper, tema, ascii_configs, dan fonts ikut dipasang di
  /usr/share/sysc-greet (dibaca binary lewat dataDir yang di-hardcode).
- /etc/greetd/config.toml TIDAK disentuh: pengarahan greetd dilakukan oleh
  rakuos-hyprland greeter, yang juga menyimpan backup.
