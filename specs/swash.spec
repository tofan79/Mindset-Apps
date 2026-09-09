Name:           swash
Version:        %{pkg_version}
Release:        2%{?dist}
Summary:        Fast screenshot annotator and lightweight image editor

License:        GPL-3.0-or-later
URL:            https://github.com/ItsLemmy/swash
Source0:        swash-v%{version}.tar.gz
Patch0:         swash-savedir.patch

BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  pkgconfig(gtk4) >= 4.10
BuildRequires:  pkgconfig(libadwaita-1) >= 1.6

Requires:       gtk4
Requires:       libadwaita
Requires:       tesseract

%description
Swash is a fast screenshot annotator and lightweight image editor for Linux,
built with GTK 4 and libadwaita. It supports freehand drawing, highlighting,
text, arrows, shapes and numbered markers, cropping, rotation, flipping,
blurring and annotation erasing, moveable annotations, undo/redo history,
OCR text recognition through Tesseract, and copy-to-clipboard or save-to-file.
Images can be opened directly or read from standard input.

%prep
%autosetup -n swash-%{version}
%patch -P 0 -p1

%build
%meson --buildtype=release
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_bindir}/swash
%{_datadir}/applications/dev.lemmy.swash.desktop
%{_datadir}/icons/hicolor/128x128/apps/dev.lemmy.swash.png
%{_datadir}/icons/hicolor/256x256/apps/dev.lemmy.swash.png
%{_datadir}/icons/hicolor/512x512/apps/dev.lemmy.swash.png

%changelog
* Wed Sep 09 2026 mindset <mindset@copr> - %{pkg_version}-2
- Patch: honor SWASH_SAVE_DIR env as initial save folder in save dialog
- Auto-updated from upstream GitHub Releases