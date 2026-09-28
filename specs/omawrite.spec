Name:           omawrite
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Dead-simple Markdown writing app built with Qt Quick
License:        MIT
URL:            https://github.com/omacom/omawrite
Source0:        %{name}-%{version}.tar.gz
ExclusiveArch:  x86_64

BuildRequires:  gcc-c++
BuildRequires:  make

# omawrite.pro: QT += core gui widgets printsupport qml quick
#              quickcontrols2 quickdialogs2 dbus
# core/gui/widgets/printsupport/dbus ikut qt6-qtbase-devel. qml/quick/
# quickcontrols2/quickdialogs2 ikut qt6-qtdeclarative-devel (modul
# QtQuickDialogs2 memang bagian dari qtdeclarative, bukan paket terpisah).
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel

# Di Fedora libQt6Quick.so dimiliki paket qt6-qtdeclarative — tidak ada
# paket "qt6-qtbase-quick". Verified against the F44 repo list.
#
# QT += widgets tidak butuh paket terpisah: Fedora memecah qtbase menjadi
# sub-paket (common/devel/gui/ibase/mysql/odbc/postgresql/static) tapi TIDAK
# punya qt6-qtbase-widgets. libQt6Widgets.so.6() di-provide oleh
# qt6-qtbase-gui:
#   $ rpm -q --provides qt6-qtbase-gui | grep libQt6Widgets
#   libQt6Widgets.so.6()(64bit)  libQt6Widgets.so.6(Qt_6)(64bit)  ...
# Jadi cukup Requires: qt6-qtbase-gui — sudah ada di bawah.
Requires:       qt6-qtbase-gui
Requires:       qt6-qtdeclarative
Requires:       xdg-desktop-portal
Requires:       hicolor-icon-theme

# Font iA Writer Mono (Regular/Italic/Bold/BoldItalic) TIDAK dipasang ke
# %{_datadir}/fonts. Src memakainya lewat Qt resource system:
#   src/resources.qrc  → <file alias="fonts/...">../fonts/...</file>
#   src/main.cpp       → QFontDatabase::addApplicationFont(":/fonts/...")
# jadi font-nya tertanam di dalam biner dan dimuat lewat ":". Menyalinnya
# ke /usr/share/fonts hanya akan menduplikasi 4 file tanpa efek apa pun.
# OFL.txt tetap ikut (kewajiban atribusi font yang tertanam), sedangkan 4
# .ttf-nya tidak — sama persis dengan apa yang dilakukan PKGBUILD upstream.

%global debug_package %{nil}

%description
Omawrite is a dead-simple Markdown writing app built with Qt Quick and C++.
It opens a folder of Markdown files, renders them with live preview, and
follows the system dark/light mode automatically. The bundled iA Writer Mono
font is compiled into the binary as a Qt resource, so no font needs to be
installed system-wide.

%prep
%autosetup -n %{name}-%{version}

%build
# .pro tidak mendukung build shadow di luar pohon, jadi tidak bisa memakai
# %make_build dengan BUILDDIR terpisah. PKGBUILD upstream juga membangun
# di dalam pohon (mkdir build && cd build && qmake6 ../omawrite.pro).
mkdir -p build
pushd build
qmake6 ../omawrite.pro
%make_build
popd

%install
install -Dm755 build/omawrite %{buildroot}%{_bindir}/omawrite
install -Dm644 pkgbuild/omawrite.desktop \
  %{buildroot}%{_datadir}/applications/omawrite.desktop
install -Dm644 pkgbuild/omawrite.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/omawrite.svg

%post
for cmd in "gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor" \
           "update-desktop-database -q"; do
  $cmd >/dev/null 2>&1 || :
done

%postun
for cmd in "gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor" \
           "update-desktop-database -q"; do
  $cmd >/dev/null 2>&1 || :
done

%files
%license LICENSE
%license fonts/OFL.txt
%doc README.md
%{_bindir}/omawrite
%{_datadir}/applications/omawrite.desktop
%{_datadir}/icons/hicolor/scalable/apps/omawrite.svg

%changelog
* Mon Sep 28 2026 Mindset Apps <mindset@example.com> - 0.5.0-1
- Initial packaging, tracking upstream tag v0.5.0.
- Bundled iA Writer Mono is embedded via Qt resources (:/fonts/...), so it
  is not installed into %{_datadir}/fonts; only fonts/OFL.txt ships.
