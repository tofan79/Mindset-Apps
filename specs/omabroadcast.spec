# OmaBroadcast adalah proyek qmake/Qt6 yang dibangun di Omarchy/Arch dan
# mengikat FFmpeg 9.1 versi pin yang diunduh saat build. Build dari sumber di
# COPR tidak praktis (pacman, makepkg, git fetch FFmpeg, path hardcode). Tiap
# rilis menyediakan paket Arch .pkg.tar.zst berisi binary + FFmpeg bundle;
# workflow mengunduhnya, memverifikasi SHA256, lalu di-repack sebagai RPM.
#
# Versi = <pkgver>.<pkgrel> dari nama asset, mis. 0.1.0.62. Ini membuat pkgrel
# baru dengan tag yang sama tetap memicu build.
#
# Perubahan spec tanpa ganti upstream versi menaikkan Release (-1 → -2 ...),
# supaya NEVRA unik dan klien tidak memakai RPM lama dari cache repo.
#
# Binary membutuhkan glibc sampai 2.44 dan RUNPATH absolut
# /usr/lib/omabroadcast/ffmpeg/lib, jadi paket ini ditujukan untuk Fedora 45+
# ( Fedora 45 memakai glibc 2.44 ).
#
# FFmpeg bundle upstream menautkan libbz2.so.1.0 (nama soname Arch); Fedora
# menyediakan libbz2.so.1. Di %install DT_NEEDED diganti memakai patchelf
# supaya dependency RPM bisa.resolve dan runtime tidak mencari file yang
# tidak ada di Fedora.
#
# Binary juga membawa qt_version_tag@Qt_6.12 (Arch rolling); Fedora 45 punya
# Qt 6.11. Tag versinya diganti ke Qt_6.11 di %install. Selain string, hash
# entri .gnu.version_r juga harus dihitung ulang; kalau tidak, dynamic linker
# menolak dengan "version `Qt_6.11' not found" walaupun stringnya sudah benar.

Name:           omabroadcast
Version:        %{pkg_version}
Release:        4%{?dist}
Summary:        Live production, recording and streaming studio for the desktop

License:        MIT AND GPL-3.0-or-later AND GPL-2.0-or-later AND BSD-3-Clause AND MPL-2.0 AND ISC AND Apache-2.0 AND LicenseRef-AOMPL-1.0
URL:            https://github.com/28allday/omabroadcast
Source0:        omabroadcast-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  patchelf
BuildRequires:  python3

%description
OmaBroadcast is a Qt6/QML live-production app for recording, replaying and
streaming the desktop. It bundles its own FFmpeg 9.1 libraries under
/usr/lib/omabroadcast/ffmpeg/lib and ships a WebEngine helper browser.

This package repacks the upstream x86_64 Arch binary package; nothing is
recompiled locally.

%prep
%setup -q -n omabroadcast-%{version}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a usr %{buildroot}/

# libavformat bundle upstream (Arch) meminta libbz2.so.1.0; Fedora memakai
# libbz2.so.1. Ganti DT_NEEDED-nya supaya dependency RPM bisa resolve.
find %{buildroot}%{_prefix}/lib/%{name}/ffmpeg/lib -type f -name '*.so.*' | while read -r f; do
    if patchelf --print-needed "$f" | grep -qx 'libbz2.so.1.0'; then
        patchelf --replace-needed libbz2.so.1.0 libbz2.so.1 "$f"
    fi
done

# Arch menandai qt_version_tag dengan Qt_6.12; Fedora 45 menyediakan Qt_6.11.
# Ganti string versi dan hitung ulang hash di .gnu.version_r supaya dynamic
# linker menerima versi yang baru.
for f in %{buildroot}%{_bindir}/omabroadcast \
         %{buildroot}%{_prefix}/lib/%{name}/omabroadcast-browser; do
    [ -f "$f" ] || continue
    if grep -q 'Qt_6.12' "$f"; then
        python3 - "$f" <<'PY'
import struct
import sys

path = sys.argv[1]
data = bytearray(open(path, "rb").read())
data = bytearray(data.replace(b"Qt_6.12", b"Qt_6.11"))

e_shoff = struct.unpack_from("<Q", data, 0x28)[0]
e_shentsize = struct.unpack_from("<H", data, 0x3a)[0]
e_shnum = struct.unpack_from("<H", data, 0x3c)[0]
e_shstrndx = struct.unpack_from("<H", data, 0x3e)[0]


def get_section(index):
    values = struct.unpack_from("<IIQQQQIIQQ", data, e_shoff + index * e_shentsize)
    return {"name": values[0], "off": values[4], "size": values[5], "link": values[6]}


def string_at(section, offset):
    start = section["off"] + offset
    end = data.index(0, start)
    return data[start:end].decode("ascii", "replace")


shstr = get_section(e_shstrndx)
sections = {}
for index in range(e_shnum):
    section = get_section(index)
    sections[string_at(shstr, section["name"])] = section

version_r = sections[".gnu.version_r"]
dynstr = sections[".dynstr"]


def elf_hash(value):
    result = 0
    for char in value.encode():
        result = (result << 4) + char
        high = result & 0xF0000000
        if high:
            result ^= high >> 24
        result &= ~high
    return result & 0xFFFFFFFF


offset = version_r["off"]
end = offset + version_r["size"]
while offset < end:
    vn_version, vn_count, vn_file, vn_aux, vn_next = struct.unpack_from("<HHIII", data, offset)
    aux = offset + vn_aux
    for _ in range(vn_count):
        vna_hash, vna_flags, vna_other, vna_name, vna_next = struct.unpack_from("<IHHII", data, aux)
        if string_at(dynstr, vna_name) == "Qt_6.11":
            wanted = elf_hash("Qt_6.11")
            if vna_hash != wanted:
                struct.pack_into("<I", data, aux, wanted)
        if vna_next == 0:
            break
        aux += vna_next
    if vn_next == 0:
        break
    offset += vn_next

open(path, "wb").write(data)
PY
    fi
done

desktop-file-validate %{buildroot}%{_datadir}/applications/omabroadcast.desktop

%post
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q %{_datadir}/applications || :
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -qt %{_datadir}/icons/hicolor || :
fi

%postun
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q %{_datadir}/applications || :
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -qt %{_datadir}/icons/hicolor || :
fi

%files
%license %{_datadir}/licenses/%{name}/
%{_bindir}/omabroadcast
%{_prefix}/lib/%{name}/
%{_datadir}/applications/omabroadcast.desktop
%{_datadir}/icons/hicolor/scalable/apps/omabroadcast.svg

%changelog
* Wed Nov 25 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-4
- Perbaikan: hash .gnu.version_r ikut dihitung ulang setelah qt_version_tag
  diganti ke Qt_6.11, supaya dynamic linker tidak menolak versi tersebut.

* Wed Nov 25 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-3
- Perbaikan: qt_version_tag@Qt_6.12 diganti ke Qt_6.11 (versi Fedora 45).

* Wed Nov 25 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-2
- Perbaikan: DT_NEEDED libbz2.so.1.0 diganti ke libbz2.so.1 (nama soname Fedora).
- Release dinaikkan supaya RPM lama tidak dipakai ulang dari cache repo.

* Wed Nov 25 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Paket awal: repack paket Arch x86_64 upstream v0.1.0-62.
- Versi memakai pkgver.pkgrel agar rebuild pkgrel memicu workflow.
- FFmpeg bundle, helper WebEngine, dan lisensi pihak ketiga ikut dipasang.
