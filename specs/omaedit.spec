# OmaEdit adalah proyek qmake/Qt6 yang dibangun di Omarchy/Arch, menarik FFmpeg
# 9.1 pin saat build, dan memakai Qt 6.12. Build dari sumber di COPR tidak
# praktis (makepkg/pacman, git fetch FFmpeg, path hardcode /usr/lib/...).
# Tiap rilis beta menyediakan paket Arch .pkg.tar.zst berisi binary + bundel
# FFmpeg/OpenAPV/library pihak ketiga; workflow mengunduhnya, memverifikasi
# SHA256, lalu spec ini memasang ulang payload-nya sebagai RPM.
#
# Semua rilis upstream berstatus prerelease, jadi workflow memakai /releases,
# bukan /releases/latest. Versi RPM = <pkgver>.<pkgrel> dari nama asset, mis.
# 0.2.6.1, supaya pkgrel baru pada tag yang sama tetap memicu build.
#
# Perubahan spec tanpa ganti upstream versi menaikkan Release (-1 → -2 ...),
# supaya NEVRA unik dan klien tidak memakai RPM lama dari cache repo.
#
# Binary membutuhkan GLIBC_2.44 dan RUNPATH absolut
# /usr/lib/omaedit/{ffmpeg/lib,lib} — paket ini ditujukan untuk Fedora 45+.
#
# Dua penyesuaian yang sama seperti omabroadcast:
#   1. libavformat dan libminizip-ng bundel meminta libbz2.so.1.0 (soname
#      Arch); Fedora memakai libbz2.so.1, jadi DT_NEEDED diganti patchelf.
#   2. Binary bertanda qt_version_tag@Qt_6.12 (Arch rolling); Fedora 45 punya
#      Qt 6.11. String versi diganti ke Qt_6.11 DAN hash .gnu.version_r
#      dihitung ulang, kalau tidak dynamic linker menolak versi tersebut.
#
# Qt 6.12 juga menambah overload by-value (&&) untuk QVariant/QJsonDocument/
# QFile::copy, dan API baru QObject::disconnect(Connection&) serta
# QReadWriteLock::destroyRecursiveHelper(void*). Shim di bawah meneruskan
# semuanya ke API const& / lama yang ada di Qt 6.11.
#
# Binary juga meminta versi Qt_6_PRIVATE_API untuk 11 simbol QRhi; Fedora
# menyediakan Qt_6.11_PRIVATE_API. Requirement dipetakan ke Qt_6 dan shim
# meneruskan simbol-simbol itu ke implementasi aslinya via dlvsym.

Name:           omaedit
Version:        %{pkg_version}
Release:        3%{?dist}
Summary:        Video editor with media, edit, colour, audio and delivery workspaces

License:        GPL-3.0-or-later AND GPL-2.0-or-later AND BSD-2-Clause AND BSD-3-Clause AND Apache-2.0 AND MIT AND Zlib AND ISC AND OFL-1.1 AND LicenseRef-AOMPL-1.0 AND LicenseRef-Intel-Simplified-Software-License
URL:            https://github.com/28allday/omaedit
Source0:        %{name}-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  patchelf
BuildRequires:  python3
BuildRequires:  shared-mime-info

Requires:       qt6-qtbase
Requires:       qt6-qtdeclarative
Requires:       qt6-qtmultimedia
Requires:       qt6-qtsvg
Requires:       qt6-qtwayland
Requires:       qt6-qtimageformats
Requires:       hicolor-icon-theme
Requires:       xdg-desktop-portal
Requires:       glslang
Requires:       spirv-tools
Requires:       vulkan-loader
Requires:       ffmpeg-free >= 9
Requires:       udisks2
Requires:       blas
Requires:       lapack
Requires:       tbb
Requires:       bzip2-libs
Requires:       xz-libs
Requires:       lame-libs
Requires:       opus
Requires:       snappy
Requires:       libva
Requires:       libdrm
Requires:       libvorbis
Requires:       zlib-ng-compat
Requires:       lz4-libs
Recommends:     jetbrains-mono-fonts
Recommends:     google-noto-fonts

%description
OmaEdit is a native video editor for Omarchy/Hyprland with separate media,
edit, colour, audio and delivery workspaces. It ships its own FFmpeg 9.1,
OpenAPV encoder and third-party libraries under /usr/lib/omaedit.

This package repacks the upstream x86_64 Arch binary package; nothing is
recompiled locally.

%prep
%setup -q -n %{name}-%{version}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a usr %{buildroot}/

# Bundel Arch meminta libbz2.so.1.0; Fedora menyediakan libbz2.so.1.
find %{buildroot}%{_prefix}/lib/%{name} -type f -name '*.so*' | while read -r f; do
    if patchelf --print-needed "$f" 2>/dev/null | grep -qx 'libbz2.so.1.0'; then
        patchelf --replace-needed libbz2.so.1.0 libbz2.so.1 "$f"
    fi
done

# qt_version_tag@Qt_6.12 -> Qt_6.11. Selain string, hash entri .gnu.version_r
# harus dihitung ulang supaya dynamic linker menerima versi baru.
f=%{buildroot}%{_bindir}/%{name}
if grep -q 'Qt_6.12' "$f"; then
    python3 - "$f" <<'PY'
import struct
import sys

path = sys.argv[1]
data = bytearray(open(path, "rb").read())
data = bytearray(data.replace(b"Qt_6.12", b"Qt_6.11"))
# Qt 6.12 memakai versi "Qt_6_PRIVATE_API"; Fedora 6.11 memakai
# "Qt_6.11_PRIVATE_API" yang lebih panjang, jadi tidak bisa ditimpa in-place.
# Requirement dipetakan ke "Qt_6" yang tersedia di semua pustaka Qt; simbol
# private-nya disediakan shim di bawah. Penimpaan ini tetap sama panjangnya.
old = b"Qt_6_PRIVATE_API\0"
if data.count(old) != 1:
    raise SystemExit("unexpected Qt_6_PRIVATE_API count")
pos = data.index(old)
data[pos:pos + len(old)] = b"Qt_6\0" + b"\0" * (len(old) - 5)

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
        name = string_at(dynstr, vna_name)
        if name in ("Qt_6.11", "Qt_6"):
            wanted = elf_hash(name)
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

# Shim ABI Qt 6.12 -> 6.11. Tidak perlu link ke libQt6Core: simbol tujuan
# di-resolve dari DT_NEEDED binary utama saat runtime.
mkdir -p %{buildroot}%{_libdir}
cat > %{_builddir}/%{name}-qtcompat.c <<'EOF'
/* Kompatibilitas ABI Qt 6.12 -> 6.11 untuk biner omaedit upstream Arch. */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdint.h>

static void *priv_handle(void)
{
    static void *h;
    if (!h) {
        h = dlopen("libQt6Gui.so.6", RTLD_NOW | RTLD_NOLOAD);
        if (!h) h = dlopen("libQt6Gui.so.6", RTLD_NOW);
    }
    return h;
}

extern void t_qstringlist(void *, const void *) __asm__("_ZN8QVariantC1ERK5QListI7QStringE");
void s_qstringlist(void *self, const void *v) __asm__("_ZN8QVariantC1EO5QListI7QStringE");
void s_qstringlist(void *self, const void *v) { t_qstringlist(self, v); }

extern void t_qstring(void *, const void *) __asm__("_ZN8QVariantC1ERK7QString");
void s_qstring(void *self, const void *v) __asm__("_ZN8QVariantC1EO7QString");
void s_qstring(void *self, const void *v) { t_qstring(self, v); }

extern void t_qlist(void *, const void *) __asm__("_ZN8QVariantC1ERK5QListIS_E");
void s_qlist(void *self, const void *v) __asm__("_ZN8QVariantC1EO5QListIS_E");
void s_qlist(void *self, const void *v) { t_qlist(self, v); }

extern void t_qmap(void *, const void *) __asm__("_ZN8QVariantC1ERK4QMapI7QStringS_E");
void s_qmap(void *self, const void *v) __asm__("_ZN8QVariantC1EO4QMapI7QStringS_E");
void s_qmap(void *self, const void *v) { t_qmap(self, v); }

extern void t_qbytearray(void *, const void *) __asm__("_ZN8QVariantC1ERK10QByteArray");
void s_qbytearray(void *self, const void *v) __asm__("_ZN8QVariantC1EO10QByteArray");
void s_qbytearray(void *self, const void *v) { t_qbytearray(self, v); }

extern void t_qurl(void *, const void *) __asm__("_ZN8QVariantC1ERK4QUrl");
void s_qurl(void *self, const void *v) __asm__("_ZN8QVariantC1EO4QUrl");
void s_qurl(void *self, const void *v) { t_qurl(self, v); }

extern void t_jsonarray(void *, const void *) __asm__("_ZN13QJsonDocumentC1ERK10QJsonArray");
void s_jsonarray(void *self, const void *v) __asm__("_ZN13QJsonDocumentC1EO10QJsonArray");
void s_jsonarray(void *self, const void *v) { t_jsonarray(self, v); }

extern void t_jsonobject(void *, const void *) __asm__("_ZN13QJsonDocumentC1ERK11QJsonObject");
void s_jsonobject(void *self, const void *v) __asm__("_ZN13QJsonDocumentC1EO11QJsonObject");
void s_jsonobject(void *self, const void *v) { t_jsonobject(self, v); }

extern unsigned char t_qfile_copy(void *, const void *, const void *) __asm__("_ZN5QFile4copyERK7QStringS2_");
unsigned char s_qfile_copy(void *self, const void *a, const void *b, const void *opt)
    __asm__("_ZN5QFile4copyERK7QStringS2_St8optionalI6QFlagsIN11QFileDevice10PermissionEEE");
unsigned char s_qfile_copy(void *self, const void *a, const void *b, const void *opt)
{
    (void)opt;
    return t_qfile_copy(self, a, b);
}

extern unsigned char t_qfile_copy1(void *, const void *) __asm__("_ZN5QFile4copyERK7QString");
unsigned char s_qfile_copy1(void *self, const void *a, const void *opt)
    __asm__("_ZN5QFile4copyERK7QStringSt8optionalI6QFlagsIN11QFileDevice10PermissionEEE");
unsigned char s_qfile_copy1(void *self, const void *a, const void *opt)
{
    (void)opt;
    return t_qfile_copy1(self, a);
}

extern unsigned char t_qobject_disconnect(void *, const void *) __asm__("_ZN7QObject10disconnectERKN11QMetaObject10ConnectionE");
unsigned char s_qobject_disconnect(void *self, void *connection)
    __asm__("_ZN7QObject10disconnectERN11QMetaObject10ConnectionE");
unsigned char s_qobject_disconnect(void *self, void *connection)
{
    return t_qobject_disconnect(self, connection);
}

extern void t_lock_destroy(void *) __asm__("_ZN14QReadWriteLock16destroyRecursiveEP21QReadWriteLockPrivate");
void s_lock_destroy(void *d) __asm__("_ZN14QReadWriteLock22destroyRecursiveHelperEPv");
void s_lock_destroy(void *d) { t_lock_destroy(d); }
/* Simbol private API: biner meminta versi Qt_6_PRIVATE_API yang tidak ada
   di Qt 6.11 Fedora. Shim menyediakannya tanpa versi dan meneruskan ke
   implementasi Qt_6.11_PRIVATE_API asli. Semua argumen adalah pointer/int
   (tidak ada float), jadi uintptr_t aman untuk x86_64 SysV. */
void wpriv0(uintptr_t a0, uintptr_t a1) __asm__("_ZN17QRhiCommandBuffer14resourceUpdateEP23QRhiResourceUpdateBatch");
void wpriv0(uintptr_t a0, uintptr_t a1) {
    static void (*fn)(uintptr_t a0, uintptr_t a1);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0, uintptr_t a1))dlvsym(h, "_ZN17QRhiCommandBuffer14resourceUpdateEP23QRhiResourceUpdateBatch", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0, a1);
}

void wpriv1(uintptr_t a0, uintptr_t a1) __asm__("_ZN19QRhiColorAttachmentC1EP11QRhiTexture");
void wpriv1(uintptr_t a0, uintptr_t a1) {
    static void (*fn)(uintptr_t a0, uintptr_t a1);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0, uintptr_t a1))dlvsym(h, "_ZN19QRhiColorAttachmentC1EP11QRhiTexture", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0, a1);
}

void wpriv2(uintptr_t a0, uintptr_t a1) __asm__("_ZN23QRhiReadbackDescriptionC1EP11QRhiTexture");
void wpriv2(uintptr_t a0, uintptr_t a1) {
    static void (*fn)(uintptr_t a0, uintptr_t a1);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0, uintptr_t a1))dlvsym(h, "_ZN23QRhiReadbackDescriptionC1EP11QRhiTexture", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0, a1);
}

void wpriv3(uintptr_t a0, uintptr_t a1, uintptr_t a2) __asm__("_ZN23QRhiResourceUpdateBatch15readBackTextureERK23QRhiReadbackDescriptionP18QRhiReadbackResult");
void wpriv3(uintptr_t a0, uintptr_t a1, uintptr_t a2) {
    static void (*fn)(uintptr_t a0, uintptr_t a1, uintptr_t a2);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0, uintptr_t a1, uintptr_t a2))dlvsym(h, "_ZN23QRhiResourceUpdateBatch15readBackTextureERK23QRhiReadbackDescriptionP18QRhiReadbackResult", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0, a1, a2);
}

void wpriv4(uintptr_t a0, uintptr_t a1) __asm__("_ZN34QRhiTextureRenderTargetDescriptionC1ERK19QRhiColorAttachment");
void wpriv4(uintptr_t a0, uintptr_t a1) {
    static void (*fn)(uintptr_t a0, uintptr_t a1);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0, uintptr_t a1))dlvsym(h, "_ZN34QRhiTextureRenderTargetDescriptionC1ERK19QRhiColorAttachment", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0, a1);
}

void wpriv5(uintptr_t a0, uintptr_t a1, uintptr_t a2, uintptr_t a3, uintptr_t a4) __asm__("_ZN4QRhi10newTextureEN11QRhiTexture6FormatERK5QSizei6QFlagsINS0_4FlagEE");
void wpriv5(uintptr_t a0, uintptr_t a1, uintptr_t a2, uintptr_t a3, uintptr_t a4) {
    static void (*fn)(uintptr_t a0, uintptr_t a1, uintptr_t a2, uintptr_t a3, uintptr_t a4);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0, uintptr_t a1, uintptr_t a2, uintptr_t a3, uintptr_t a4))dlvsym(h, "_ZN4QRhi10newTextureEN11QRhiTexture6FormatERK5QSizei6QFlagsINS0_4FlagEE", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0, a1, a2, a3, a4);
}

void wpriv6(uintptr_t a0, uintptr_t a1, uintptr_t a2, uintptr_t a3, uintptr_t a4, uintptr_t a5) __asm__("_ZN4QRhi15newRenderBufferEN16QRhiRenderBuffer4TypeERK5QSizei6QFlagsINS0_4FlagEEN11QRhiTexture6FormatE");
void wpriv6(uintptr_t a0, uintptr_t a1, uintptr_t a2, uintptr_t a3, uintptr_t a4, uintptr_t a5) {
    static void (*fn)(uintptr_t a0, uintptr_t a1, uintptr_t a2, uintptr_t a3, uintptr_t a4, uintptr_t a5);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0, uintptr_t a1, uintptr_t a2, uintptr_t a3, uintptr_t a4, uintptr_t a5))dlvsym(h, "_ZN4QRhi15newRenderBufferEN16QRhiRenderBuffer4TypeERK5QSizei6QFlagsINS0_4FlagEEN11QRhiTexture6FormatE", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0, a1, a2, a3, a4, a5);
}

void wpriv7(uintptr_t a0, uintptr_t a1, uintptr_t a2) __asm__("_ZN4QRhi22newTextureRenderTargetERK34QRhiTextureRenderTargetDescription6QFlagsIN23QRhiTextureRenderTarget4FlagEE");
void wpriv7(uintptr_t a0, uintptr_t a1, uintptr_t a2) {
    static void (*fn)(uintptr_t a0, uintptr_t a1, uintptr_t a2);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0, uintptr_t a1, uintptr_t a2))dlvsym(h, "_ZN4QRhi22newTextureRenderTargetERK34QRhiTextureRenderTargetDescription6QFlagsIN23QRhiTextureRenderTarget4FlagEE", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0, a1, a2);
}

void wpriv8(uintptr_t a0) __asm__("_ZN4QRhi23nextResourceUpdateBatchEv");
void wpriv8(uintptr_t a0) {
    static void (*fn)(uintptr_t a0);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0))dlvsym(h, "_ZN4QRhi23nextResourceUpdateBatchEv", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0);
}

void wpriv9(uintptr_t a0) __asm__("_ZNK4QRhi10driverInfoEv");
void wpriv9(uintptr_t a0) {
    static void (*fn)(uintptr_t a0);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0))dlvsym(h, "_ZNK4QRhi10driverInfoEv", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0);
}

void wpriv10(uintptr_t a0) __asm__("_ZNK4QRhi18isYUpInFramebufferEv");
void wpriv10(uintptr_t a0) {
    static void (*fn)(uintptr_t a0);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0))dlvsym(h, "_ZNK4QRhi18isYUpInFramebufferEv", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0);
}
EOF
gcc -shared -fPIC -O2 -Wl,-soname,lib%{name}-qtcompat.so \
    %{_builddir}/%{name}-qtcompat.c \
    -o %{buildroot}%{_libdir}/lib%{name}-qtcompat.so -ldl

# Muat shim sebelum libQt6Core resolve simbol-simbol tersebut.
patchelf --add-needed lib%{name}-qtcompat.so %{buildroot}%{_bindir}/%{name}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q %{_datadir}/applications || :
fi
if command -v update-mime-database >/dev/null 2>&1; then
    update-mime-database %{_datadir}/mime >/dev/null 2>&1 || :
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -qt %{_datadir}/icons/hicolor || :
fi

%postun
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database -q %{_datadir}/applications || :
fi
if command -v update-mime-database >/dev/null 2>&1; then
    update-mime-database %{_datadir}/mime >/dev/null 2>&1 || :
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -qt %{_datadir}/icons/hicolor || :
fi

%files
%license %{_datadir}/licenses/%{name}/
%{_bindir}/%{name}
%{_libdir}/lib%{name}-qtcompat.so
%{_prefix}/lib/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/metainfo/org.omatools.%{name}.metainfo.xml
%{_datadir}/mime/packages/%{name}-project.xml
%{_datadir}/%{name}/

%changelog
* Wed Nov 25 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Paket awal: repack paket Arch x86_64 upstream v0.2.6-1.
- Versi memakai pkgver.pkgrel agar rebuild pkgrel memicu workflow.
- DT_NEEDED libbz2.so.1.0 diganti ke libbz2.so.1 (soname Fedora).
- qt_version_tag@Qt_6.12 diganti ke Qt_6.11 dengan hash .gnu.version_r
  dihitung ulang.
- Shim kompatibilitas overload by-value (&&) Qt 6.12, QObject::disconnect,
  dan QReadWriteLock::destroyRecursiveHelper.
* Wed Nov 25 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-2
- Ganti nama dependensi Arch ke nama paket Fedora/RakuOS: opus-libs -> opus,
  snappy-libs -> snappy, zlib -> zlib-ng-compat.
* Wed Nov 25 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-3
- Hapus Requires: whisper-cpp; tidak dipakai binary/library apa pun dan
  menarik seluruh stack ROCm (~5.9 GiB) lewat hipblas/rocblas.
