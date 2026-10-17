Name:           illogical-impulse
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Quickshell-based Hyprland desktop shell (dots-hyprland snapshot)

# Kode GPL-3.0 (LICENSE); licenses/ berisi teks LGPL-3.0 (bagian yang
# mengambil kode LGPL) dan MIT (bagian vendored). Aset/font upstream yang
# proprietary (Google Sans Flex) tidak ikut ke paket ini.
License:        GPL-3.0-only AND LGPL-3.0-or-later AND MIT
URL:            https://github.com/end-4/dots-hyprland
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

# ---- Requires minimal (pola ambxst/inir-shell) ----
# quickshell-git, matugen, font, dan alat CLI dipasang manual lewat install
# plan rakuos-shell-picker, bukan resolver rpm. Yang tetap Requires hanya
# modul QML yang WAJIB ada supaya shell bisa dimuat: org.kde.kirigami dipakai
# panel/widget dan org.kde.syntaxhighlighting dipakai blok kode — tanpa
# paketnya komponen gagal dimuat dengan "module ... is not installed".
Requires:       kf6-kirigami
Requires:       kf6-syntax-highlighting

# Skrip python payload memakai shebang venv upstream
# `#!/usr/bin/env -S /bin/sh -c "source ..."`. Varian yang di-escape
# (`-S\_`) lolos dari brp-mangle-shebangs, lalu generator dependensi rpm
# membaca seluruh baris shebang sebagai path interpreter dan menulis
# Requires karangan `/usr/bin/-S_/bin/sh_-c_...` yang tidak disediakan
# paket mana pun -> `rum install`/dnf gagal "nothing provides".
# Interpreter sebenarnya sudah dijamin (sh/bash/python3) dan venv dibuat
# install plan rakuos-shell-picker, jadi dependensi palsu itu disaring.
%global __requires_exclude ^/usr/bin/-S_

%description
illogical-impulse (ii) adalah desktop shell berbasis Quickshell untuk
Hyprland dari proyek dots-hyprland: bar, dock, launcher, control center,
notifikasi, lock screen, dan tema Material You (matugen).

Paket ini adalah snapshot master upstream (version 2026MMDD.git<sha>) berisi
salinan induk config ke %{_datadir}/illogical-impulse/ (tree dots/ apa adanya
+ sdata/uv/requirements.txt). Upstream hanya menyediakan installer interaktif
yang menulis $HOME; paket ini sengaja TIDAK menjalankan installer itu —
penyaluran ke ~/.config (hypr, quickshell, matugen, dst) dilakukan oleh skel
rakuos-shell-picker, jadi update dari RPM bisa menimpa salinan induk tanpa
menyentuh config user yang sudah kamu ubah. Advisory upstream: jangan pilih
uwsm saat login dari display manager.

Virtual env Python (materialyoucolor, dll) dibuat oleh picker saat install:
    uv venv --prompt .venv ~/.local/state/quickshell/.venv -p 3.12
    uv pip install -r %{_datadir}/illogical-impulse/sdata/uv/requirements.txt
Env var ILLOGICAL_IMPULSE_VIRTUAL_ENV sudah diatur di
dots/.config/hypr/hyprland/env.lua. Tanpa venv, fitur warna/thumbnail
berbasis Python tidak jalan (shell tetap tampil).

Submodule dots/.config/quickshell/ii/modules/common/widgets/shapes
(end-4/rounded-polygon-qmljs) di-vendor di workflow saat membuat tarball —
git archive tidak membawa isi submodule.

%prep
%autosetup -n %{name}-%{version}

# Submodule shapes harus terisi (di-vendor oleh workflow); kalau kosong,
# shell akan gagal memuat widget bulat dan build ini cacat sejak awal.
find dots/.config/quickshell/ii/modules/common/widgets/shapes -type f | grep -q . \
    || { echo "submodule shapes kosong — workflow tidak mem-vendor"; exit 1; }

%install
mkdir -p %{buildroot}%{_datadir}/illogical-impulse
cp -a dots %{buildroot}%{_datadir}/illogical-impulse/
mkdir -p %{buildroot}%{_datadir}/illogical-impulse/sdata
cp -a sdata/uv %{buildroot}%{_datadir}/illogical-impulse/sdata/

%files
%license LICENSE
%license licenses/LGPL-3.0.txt
%license licenses/MIT.txt
%{_datadir}/illogical-impulse/

%changelog
* Sat Oct 17 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-2
- Filter requires karangan `/usr/bin/-S_...` dari shebang venv upstream
  (dots/.config/quickshell/ii/scripts/hyprland/hyprconfigurator.py dan
  scripts/colors/generate_colors_material.py) via __requires_exclude;
  sebelumnya `rum install illogical-impulse` gagal "nothing provides".
* Sat Oct 17 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Initial COPR packaging of dots-hyprland (illogical-impulse base, RPM 1
  dari pasangan end4-pC): snapshot master + vendor submodule shapes,
  payload ke /usr/share/illogical-impulse (dots/ + sdata/uv).
- Requires minimal (pola ambxst): hanya kf6-kirigami +
  kf6-syntax-highlighting; quickshell-git, matugen, font, dan alat CLI
  dipasang manual lewat install plan rakuos-shell-picker.
- venv Python (uv) dibootstrap picker, bukan scriptlet RPM; installer
  interaktif upstream (setup) tidak ikut dipaketkan.
