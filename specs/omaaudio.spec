# OmaAudio adalah proyek qmake6 + meson yang dikembangkan di Omarchy/Arch.
# Artefak rilis berupa paket Arch .pkg.tar.zst berisi binary Qt 6.12, plugin
# LV2, helper VST3 scanner, dan skrip import Python. Build dari sumber juga
# memungkinkan di Fedora 45 (Qt 6.11 memenuhi syarat >=6.8), tetapi repack
# dipilih supaya konsisten dengan omabroadcast/omaedit dan menghindari
# keraguan nama paket -devel (pipewire, lilv, lv2, rnnoise, dll.).
#
# Semua rilis upstream berstatus prerelease, jadi workflow memakai /releases,
# bukan /releases/latest. Versi RPM = <pkgver>.<pkgrel> dari nama asset,
# dengan "beta" dinormalisasi ke "~beta" supaya rilis final 0.2.0 nanti tidak
# dianggap lebih tua. Contoh: 0.2.0beta1-1 → 0.2.0~beta1.1.
#
# Perubahan spec tanpa ganti upstream versi menaikkan Release (-1 → -2 ...),
# supaya NEVRA unik dan klien tidak memakai RPM lama dari cache repo.
#
# Binary meminta sampai GLIBC_2.43, jadi aman di Fedora 45 (glibc 2.44),
# tetapi tidak di Fedora 44.
#
# Penyesuaian yang sama seperti omabroadcast/omaedit: qt_version_tag@Qt_6.12
# diganti ke Qt_6.11 dengan hash .gnu.version_r dihitung ulang, dan shim
# meneruskan overload by-value (&&) Qt 6.12 ke overload const& milik Qt 6.11.
# Termasuk dua varian QFile::copy(std::optional<QFlags<Permission>>) yang
# hanya dipakai omaaudio. Tidak ada bundel FFmpeg, jadi tidak ada patchelf
# libbz2 seperti di omabroadcast/omaedit.
#
# Binary juga meminta versi Qt_6_PRIVATE_API (QVulkanFunctions /
# QVulkanDeviceFunctions); Fedora menyediakan Qt_6.11_PRIVATE_API. Karena
# string lama lebih pendek, requirement dipetakan ke Qt_6 dan shim meneruskan
# simbol private tersebut ke implementasi Qt_6.11_PRIVATE_API via dlvsym.

Name:           omaaudio
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Audio editor, arranger, mixer and mastering tool for the desktop

License:        MIT AND ISC AND BSD-3-Clause
URL:            https://github.com/28allday/omaaudio
Source0:        %{name}-%{version}.tar.gz

%global debug_package %{nil}
%global __brp_check_rpaths %{nil}

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  patchelf
BuildRequires:  python3

Requires:       qt6-qtbase
Requires:       qt6-qtdeclarative
Requires:       qt6-qtsvg
Requires:       qt6-qtwayland
Requires:       hicolor-icon-theme
Requires:       xdg-desktop-portal
Requires:       pipewire
Requires:       libsndfile >= 1.1.0
Requires:       lilv
Requires:       tomlplusplus
Requires:       rnnoise
Requires:       libxcb
Requires:       xcb-util-wm
Requires:       python3
Requires:       ffmpeg-free
Recommends:     lv2-calf-plugins
Recommends:     lsp-plugins-lv2
Recommends:     lv2-x42-plugins
Suggests:       pipewire-jack
Suggests:       xorg-xwayland

%description
OmaAudio is a native audio editor for Omarchy/Hyprland: edit, arrange, repair,
mix and deliver sound. It records and monitors through PipeWire, ships LV2
plugins and a VST3 scanner, and can run headless through its JSON CLI.

This package repacks the upstream x86_64 Arch binary package; nothing is
recompiled locally.

%prep
%setup -q -n %{name}-%{version}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a usr %{buildroot}/

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
/* Kompatibilitas ABI Qt 6.12 -> 6.11 untuk biner omaaudio upstream Arch. */
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
/* Simbol private API: biner meminta versi Qt_6_PRIVATE_API yang tidak ada
   di Qt 6.11 Fedora. Shim menyediakannya tanpa versi dan meneruskan ke
   implementasi Qt_6.11_PRIVATE_API asli. Semua argumen adalah pointer/int
   (tidak ada float), jadi uintptr_t aman untuk x86_64 SysV. */
void wpriv0(uintptr_t a0, uintptr_t a1) __asm__("_ZN16QVulkanFunctions29vkGetPhysicalDevicePropertiesEP18VkPhysicalDevice_TP26VkPhysicalDeviceProperties");
void wpriv0(uintptr_t a0, uintptr_t a1) {
    static void (*fn)(uintptr_t a0, uintptr_t a1);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0, uintptr_t a1))dlvsym(h, "_ZN16QVulkanFunctions29vkGetPhysicalDevicePropertiesEP18VkPhysicalDevice_TP26VkPhysicalDeviceProperties", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0, a1);
}

void wpriv1(uintptr_t a0, uintptr_t a1, uintptr_t a2) __asm__("_ZN16QVulkanFunctions40vkGetPhysicalDeviceQueueFamilyPropertiesEP18VkPhysicalDevice_TPjP23VkQueueFamilyProperties");
void wpriv1(uintptr_t a0, uintptr_t a1, uintptr_t a2) {
    static void (*fn)(uintptr_t a0, uintptr_t a1, uintptr_t a2);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0, uintptr_t a1, uintptr_t a2))dlvsym(h, "_ZN16QVulkanFunctions40vkGetPhysicalDeviceQueueFamilyPropertiesEP18VkPhysicalDevice_TPjP23VkQueueFamilyProperties", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0, a1, a2);
}

void wpriv2(uintptr_t a0, uintptr_t a1, uintptr_t a2) __asm__("_ZN16QVulkanFunctions26vkEnumeratePhysicalDevicesEP12VkInstance_TPjPP18VkPhysicalDevice_T");
void wpriv2(uintptr_t a0, uintptr_t a1, uintptr_t a2) {
    static void (*fn)(uintptr_t a0, uintptr_t a1, uintptr_t a2);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0, uintptr_t a1, uintptr_t a2))dlvsym(h, "_ZN16QVulkanFunctions26vkEnumeratePhysicalDevicesEP12VkInstance_TPjPP18VkPhysicalDevice_T", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0, a1, a2);
}

void wpriv3(uintptr_t a0, uintptr_t a1, uintptr_t a2, uintptr_t a3) __asm__("_ZN16QVulkanFunctions14vkCreateDeviceEP18VkPhysicalDevice_TPK18VkDeviceCreateInfoPK21VkAllocationCallbacksPP10VkDevice_T");
void wpriv3(uintptr_t a0, uintptr_t a1, uintptr_t a2, uintptr_t a3) {
    static void (*fn)(uintptr_t a0, uintptr_t a1, uintptr_t a2, uintptr_t a3);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0, uintptr_t a1, uintptr_t a2, uintptr_t a3))dlvsym(h, "_ZN16QVulkanFunctions14vkCreateDeviceEP18VkPhysicalDevice_TPK18VkDeviceCreateInfoPK21VkAllocationCallbacksPP10VkDevice_T", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0, a1, a2, a3);
}

void wpriv4(uintptr_t a0, uintptr_t a1) __asm__("_ZN22QVulkanDeviceFunctions15vkDestroyDeviceEP10VkDevice_TPK21VkAllocationCallbacks");
void wpriv4(uintptr_t a0, uintptr_t a1) {
    static void (*fn)(uintptr_t a0, uintptr_t a1);
    if (!fn) { void *h = priv_handle(); if (h) fn = (void (*)(uintptr_t a0, uintptr_t a1))dlvsym(h, "_ZN22QVulkanDeviceFunctions15vkDestroyDeviceEP10VkDevice_TPK21VkAllocationCallbacks", "Qt_6.11_PRIVATE_API"); }
    if (fn) fn(a0, a1);
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
%{_bindir}/%{name}
%{_libdir}/lib%{name}-qtcompat.so
%{_prefix}/lib/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/doc/%{name}/
%{_datadir}/%{name}/

%changelog
* Wed Nov 25 2026 Mindset Apps <mindset@example.com> - %{pkg_version}-1
- Paket awal: repack paket Arch x86_64 upstream v0.2.0-beta.1.
- Versi memakai pkgver.pkgrel dengan normalisasi beta -> ~beta.
- qt_version_tag@Qt_6.12 diganti ke Qt_6.11 dengan hash .gnu.version_r
  dihitung ulang.
- Shim kompatibilitas overload by-value (&&) Qt 6.12, termasuk kedua
  varian QFile::copy(std::optional<QFlags<Permission>>).
