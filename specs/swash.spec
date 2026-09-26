Name:           swash
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Fast screenshot annotator and lightweight image editor (GTK4/libadwaita)

License:        GPL-3.0-or-later
URL:            https://github.com/ItsLemmy/swash
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  meson >= 0.59
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  pkgconfig(gtk4) >= 4.10
BuildRequires:  pkgconfig(libadwaita-1) >= 1.6
BuildRequires:  pkgconfig(gio-2.0)

Recommends:     tesseract

%description
Swash is a fast screenshot annotator and lightweight image editor for
Linux, built with GTK 4 and libadwaita: freehand drawing, highlighting,
text, arrows, shapes, numbered markers, cropping, rotation, flipping,
blurring, and undo/redo history. OCR text recognition is available
through Tesseract (spawned as an external `tesseract` binary at
runtime, not linked at build time — hence Recommends rather than
Requires).

%{name} tracks upstream's tagged GitHub Releases, not git HEAD: this
package's %{version} is always some upstream vX.Y.Z release tag with
the leading "v" stripped, never an untagged commit.

%prep
%autosetup -n %{name}-%{version}

%build
%meson
%meson_build

%check
# test-editor-utils is a pure GLib unit test (g_test_init only, no GTK
# window/display is created), safe to run in a headless mock buildroot.
%meson_test

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
* Sat Sep 26 2026 tofan79 <tofan79@users.noreply.github.com> - %{pkg_version}-1
- Initial Mindset-Apps COPR build of ItsLemmy/swash, tracking upstream's
  tagged GitHub Releases (workflow polls releases/latest daily and
  builds only when a new tag appears; %{pkg_version} is filled in by
  the workflow from that tag, e.g. 1.5.1 for tag v1.5.1).
