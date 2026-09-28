Name:           omashow-git
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Keyboard-first presentation editor and presenter
License:        GPL-3.0-or-later
URL:            https://github.com/28allday/omashow
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  x86_64

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig

# omashow.pro: QT += core gui qml quick quickcontrols2 dbus multimedia
#              concurrent printsupport svg
# core/gui/dbus/concurrent/printsupport semuanya ikut qt6-qtbase-devel.
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtmultimedia-devel

# omashow.pro baris 109: PKGCONFIG += libavformat libavcodec libavutil
# libswscale — jadi build ini ME-LINK ke library FFmpeg, bukan memanggil
# CLI-nya seperti omacut.
#
# Yang tersedia di repo Fedora hanya "ffmpeg-free-devel". Paket "ffmpeg-devel"
# (build GPL penuh) memang ada di mesin ini, tapi berasal dari repo pihak
# ketiga "rakuos", bukan Fedora — chroot COPR tidak punya repo itu, jadi
# menyebutkannya sebagai BuildRequires akan menggagalkan build dengan
# "No match for argument: ffmpeg-devel".
#
# ffmpeg-free adalah build LGPL (tanpa codec non-free) dan menyediakan keempat
# .pc yang dibutuhkan. Omashow sendiri GPL-3.0-or-later, jadi menautkan library
# LGPL ke dalam GPL-3.0 tetap GPL-3.0-or-later — tidak ada masalah lisensi.
# Codec non-free (H.264/AAC streaming dari kamera, sebagian VP9) tidak akan
# tersedia, yang itu konsekuensi wajar dari memilih repo Fedora murni.
BuildRequires:  ffmpeg-free-devel

# omashow.pro baris 110: PKGCONFIG += hunspell
BuildRequires:  hunspell-devel

# omashow.pro baris 179: PKGCONFIG += libetonyek-0.1 librevenge-0.0
# librevenge-stream-0.0 (impor .odp/.odt). Nama .pc-nya diimpor apa adanya
# dari LibreOffice/libetonyek upstream, bukan ditulis ulang, jadi BuildRequires
# memakai nama paket Fedora yang menelize .pc tersebut.
BuildRequires:  libetonyek-devel
BuildRequires:  librevenge-devel

# shared library FFmpeg (bukan CLI) — nama paket runtime-nya mengikuti
# -devel di atas. Bandingkan omacut, yang hanya Requires: ffmpeg-free karena
# ia menjalankan ffmpeg lewat QProcess.
Requires:       ffmpeg-free
# Pustaka kamus; paket kamus bahasa (hunspell-en-US dsb.) sengaja tidak
# dipaksa karena PKGBUILD upstream memperlakukannya sebagai optdepends dan
# ./bin/install miliknya menawarkannya secara terpisah.
Requires:       hunspell
Requires:       xdg-desktop-portal
Requires:       hicolor-icon-theme
Recommends:     hunspell-en-US
Recommends:     hunspell-en-GB

# rpm di Fedora 44 otomatis membuat subpaket debuginfo sekaligus debugsource.
# Build/instalasi sudah berhasil, tetapi debugsource tidak punya satu pun file
# sumber yang bisa dikumpulkan sehingga rpm berhenti dengan
# "Empty files file .../debugsourcefiles.list". Aplikasi pihak ketiga yang
# dibangun dari tarball tidak punya layout debugsource yang bisa dietakan, jadi
# kedua subpaket itu dimatikan altogether.
%global debug_package %{nil}

%description
OmaShow is a keyboard-first presentation editor and presenter. It opens
existing ODP/ODT bundles (through libetonyek and librevenge), renders slides
on a 3D timeline, and can drive a projector over the XDG desktop portal.
Spelling is checked with hunspell against a user-chosen dictionary.

%{name} is a daily rolling build tracking the tip of upstream's main branch.
28allday/omashow has not tagged any releases at the time this spec was
written, so there is no stable version to pin to. %{version} encodes the
commit date and short SHA, e.g. 20260928.gitabcdef1.

%prep
%autosetup -n %{name}-%{version}

%build
# .pro tidak mendukung build shadow di luar pohon, jadi tidak bisa memakai
# %make_build dengan BUILDDIR terpisah. upstream PKGBUILD juga membangun
# di dalam pohon (mkdir build && cd build && qmake6 ../omashow.pro), jadi
# ikuti pola itu agar berkas objek tetap terpisah dari source.
mkdir -p build
pushd build
%{__qmake6} ../omashow.pro
%make_build
popd

%install
install -Dm755 build/omashow %{buildroot}%{_bindir}/omashow
install -Dm644 pkgbuild/omashow.desktop \
  %{buildroot}%{_datadir}/applications/omashow.desktop
install -Dm644 pkgbuild/omashow.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/omashow.svg
install -Dm644 pkgbuild/omashow.xml \
  %{buildroot}%{_datadir}/mime/packages/omashow.xml

# Contoh deck milik upstream, dibaca lewat File > Open Examples. Nama
# berkasnya berisi spasi ("A tour of OmaShow.omashow") jadi loop + quoting
# dipakai, bukan install per-nama.
install -d %{buildroot}%{_datadir}/omashow/examples
for f in examples/*.omashow; do
  [[ -e "$f" ]] || continue
  install -m644 "$f" "%{buildroot}%{_datadir}/omashow/examples/$(basename "$f")"
done

# SKILL.md memberi tahu coding agent bahwa CLI omashow ada. Upstream
# menautkannya ke ~/.agents/skills dan sejenisnya dari scriptlet
# post-install; %post di rpm berjalan sebagai root sehingga tidak bisa
# menautkan milik user, jadi berkas SKILL.md-nya tetap diinstal dan
# %post hanya meng printing perintahnya.
install -Dm644 skills/omashow/SKILL.md \
  %{buildroot}%{_datadir}/omashow/skills/omashow

# Lisensi wajib: GPL-3.0-or-later + daftar pihak ketiga yang memang
# dipisah upstream jadi berkas sendiri.
%license LICENSE
%license THIRD-PARTY-NOTICES.md
%license src/ui/icons/LICENSE.lucide

%post
# thrice: ikon hicolor, database MIME (omashow mendaftarkan tipe
# application/x-omashow untuk glob *.omashow), dan database desktop.
for cmd in "gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor" \
           "update-mime-database %{_datadir}/mime" \
           "update-desktop-database -q"; do
  $cmd >/dev/null 2>&1 || :
done
echo "OmaShow mengirim skill untuk coding agent: omashow skill --link"

%postun
for cmd in "gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor" \
           "update-mime-database %{_datadir}/mime" \
           "update-desktop-database -q"; do
  $cmd >/dev/null 2>&1 || :
done

# Pustaka runtime (libav*, hunspell, libetonyek, librevenge) semuanya
# bereits tertangani oleh rpmfindRequires otomatis; tidak ada .so yang
# perlu-installed di luar location rpm.

%files
%license LICENSE
%license THIRD-PARTY-NOTICES.md
%license src/ui/icons/LICENSE.lucide
%doc README.md
%{_bindir}/omashow
%{_datadir}/applications/omashow.desktop
%{_datadir}/icons/hicolor/scalable/apps/omashow.svg
%{_datadir}/mime/packages/omashow.xml
%{_datadir}/omashow/examples/
%{_datadir}/omashow/skills/omashow

%changelog
* Mon Sep 28 2026 Mindset Apps <mindset@example.com> - 20260928.git0000000-1
- Initial packaging of omashow-git (upstream has no tagged releases).
- BuildRequires ffmpeg-free-devel, not ffmpeg-devel: the latter is only
  present in the third-party "rakuos" repo, which COPR chroots do not have.
- Spell dictionaries kept as Recommends, mirroring upstream's optdepends.
