%global debug_package %{nil}
%global _lto_cflags %{nil}
%global __provides_exclude_from ^(%{_libdir}/singularity/|%{_datadir}/singularity/gestures/runtime/).*\.so.*$
%global __requires_exclude ^lib(fprint-2-tod\.so\.1|gusb\.so\.2).*$

Name:           singularity-desktop
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Singularity Desktop and bundled applications
License:        GPL-3.0-only
URL:            https://github.com/singularityos-lab/singularity-desktop
Source0:        singularity-desktop-0.1.0.tar.zst
Source1:        rpm-files.py
Source2:        native-build.sh
Source3:        native-install.sh
Source4:        source-manifest.json
Source5:        vetro-vendor.tar.zst
Source6:        write-accessibility-test.vala
Source7:        native-check.sh
Source8:        write-accessibility-bridge.c
Source9:        runtime-notices.tar.zst
Source10:       check-keyring-service.sh
Source11:       keyring-dialog-test.vala
Source12:       keyring-service-test.vala
Source13:       check-keyring-regression.sh
Patch0:         native-gtk-drag-icon.patch
Patch1:         native-gtk-accessible-text.patch
Patch2:         native-runtime-compat.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  golang >= 1.24
BuildRequires:  meson >= 1.3
BuildRequires:  ninja-build
BuildRequires:  vala
BuildRequires:  vala-cups
BuildRequires:  gettext
BuildRequires:  gobject-introspection-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3
BuildRequires:  sassc
BuildRequires:  scdoc
BuildRequires:  chrpath
BuildRequires:  python3-cryptography
BuildRequires:  abattis-cantarell-vf-fonts
# Codec plugins are runtime requirements supplied by RPM Fusion; they are not
# needed to compile the desktop sources.
BuildRequires:  dejavu-sans-fonts
BuildRequires:  dejavu-serif-fonts
BuildRequires:  rsms-inter-fonts
BuildRequires:  gnu-free-sans-fonts
BuildRequires:  texlive-stix2-otf
BuildRequires:  gstreamer1-plugin-libav
BuildRequires:  pam-devel
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  dbus-daemon

BuildRequires:  pkgconfig(atspi-2)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(cairo-gobject)
BuildRequires:  pkgconfig(cups)
BuildRequires:  pkgconfig(dbusmenu-glib-0.4)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(enchant-2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freerdp-client3)
BuildRequires:  pkgconfig(freerdp3)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fuse3)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gst-editing-services-1.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gstreamer-tag-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk4) >= 4.22
BuildRequires:  pkgconfig(gtk4-layer-shell-0) >= 0.7
BuildRequires:  pkgconfig(gtk4-unix-print)
BuildRequires:  pkgconfig(gtk4-wayland)
BuildRequires:  pkgconfig(gtksourceview-5)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(gusb)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(harfbuzz-subset)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(libdrm) >= 2.4.129
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libfido2)
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(libgphoto2)
BuildRequires:  pkgconfig(libgphoto2_port)
BuildRequires:  pkgconfig(libinput) >= 1.26
BuildRequires:  pkgconfig(libliftoff)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libnm)
BuildRequires:  pkgconfig(libpeas-2)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpulse-mainloop-glib)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libsfdo-basedir) >= 0.1.3
BuildRequires:  pkgconfig(libsfdo-desktop) >= 0.1.3
BuildRequires:  pkgconfig(libsfdo-icon) >= 0.1.3
BuildRequires:  pkgconfig(libsodium)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libwacom)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libwebpmux)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(mtdev)
BuildRequires:  pkgconfig(nettle)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pangoft2)
BuildRequires:  pkgconfig(pixman-1) >= 0.46.0
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  pkgconfig(sane-backends)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(tracker-sparql-3.0)
BuildRequires:  pkgconfig(udev)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(vte-2.91-gtk4)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.39
BuildRequires:  pkgconfig(wayland-server) >= 1.22.90
BuildRequires:  pkgconfig(webkitgtk-6.0)
BuildRequires:  pkgconfig(winpr3)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-xinput)
BuildRequires:  pkgconfig(xkbcommon) >= 1.8.0
BuildRequires:  pkgconfig(xwayland)
BuildRequires:  pkgconfig(zbar)
BuildRequires:  pkgconfig(zlib)
Requires:       libsingularity = %{version}-%{release}
Requires:       singularity-accounts = %{version}-%{release}
Requires:       singularity-atelier = %{version}-%{release}
Requires:       singularity-authenticator = %{version}-%{release}
Requires:       singularity-backups = %{version}-%{release}
Requires:       singularity-browser = %{version}-%{release}
Requires:       singularity-calculator = %{version}-%{release}
Requires:       singularity-calendar = %{version}-%{release}
Requires:       singularity-camera = %{version}-%{release}
Requires:       singularity-characters = %{version}-%{release}
Requires:       singularity-clock = %{version}-%{release}
Requires:       singularity-colorpicker = %{version}-%{release}
Requires:       singularity-connections = %{version}-%{release}
Requires:       singularity-contacts = %{version}-%{release}
Requires:       singularity-database = %{version}-%{release}
Requires:       singularity-demo = %{version}-%{release}
Requires:       singularity-disks = %{version}-%{release}
Requires:       singularity-draw = %{version}-%{release}
Requires:       singularity-drivewriter = %{version}-%{release}
Requires:       singularity-edit = %{version}-%{release}
Requires:       singularity-fediverse = %{version}-%{release}
Requires:       singularity-files = %{version}-%{release}
Requires:       singularity-fonts = %{version}-%{release}
Requires:       singularity-formula = %{version}-%{release}
Requires:       singularity-gestures = %{version}-%{release}
Requires:       singularity-git = %{version}-%{release}
Requires:       singularity-greeter = %{version}-%{release}
Requires:       singularity-help = %{version}-%{release}
Requires:       singularity-keyframe = %{version}-%{release}
Requires:       singularity-keyring = %{version}-%{release}
Requires:       singularity-leafs = %{version}-%{release}
Requires:       singularity-lettere = %{version}-%{release}
Requires:       singularity-loginui = %{version}-%{release}
Requires:       singularity-logs = %{version}-%{release}
Requires:       singularity-machines = %{version}-%{release}
Requires:       singularity-maps = %{version}-%{release}
Requires:       singularity-media-plugins = %{version}-%{release}
Requires:       singularity-monitor = %{version}-%{release}
Requires:       singularity-montage = %{version}-%{release}
Requires:       singularity-music = %{version}-%{release}
Requires:       singularity-nearby = %{version}-%{release}
Requires:       singularity-nearby-app = %{version}-%{release}
Requires:       singularity-news = %{version}-%{release}
Requires:       singularity-notes = %{version}-%{release}
Requires:       singularity-passwords = %{version}-%{release}
Requires:       singularity-photos = %{version}-%{release}
Requires:       singularity-plugins = %{version}-%{release}
Requires:       singularity-podcasts = %{version}-%{release}
Requires:       singularity-polkit-agent = %{version}-%{release}
Requires:       singularity-printers = %{version}-%{release}
Requires:       singularity-publish = %{version}-%{release}
Requires:       singularity-qrcodes = %{version}-%{release}
Requires:       singularity-radio = %{version}-%{release}
Requires:       singularity-reader = %{version}-%{release}
Requires:       singularity-scanner = %{version}-%{release}
Requires:       singularity-session = %{version}-%{release}
Requires:       singularity-sharing = %{version}-%{release}
Requires:       singularity-shell = %{version}-%{release}
Requires:       singularity-slides = %{version}-%{release}
Requires:       singularity-splash = %{version}-%{release}
Requires:       singularity-spreadsheet = %{version}-%{release}
Requires:       singularity-store = %{version}-%{release}
Requires:       singularity-tasks = %{version}-%{release}
Requires:       singularity-themes = %{version}-%{release}
Requires:       singularity-tour = %{version}-%{release}
Requires:       singularity-translate = %{version}-%{release}
Requires:       singularity-usage = %{version}-%{release}
Requires:       singularity-vector = %{version}-%{release}
Requires:       singularity-videos = %{version}-%{release}
Requires:       singularity-voice = %{version}-%{release}
Requires:       singularity-wallpapers = %{version}-%{release}
Requires:       singularity-wave = %{version}-%{release}
Requires:       singularity-weather = %{version}-%{release}
Requires:       singularity-widgets = %{version}-%{release}
Requires:       singularity-write = %{version}-%{release}
Requires:       xdg-desktop-portal-singularity = %{version}-%{release}
Requires:       singularity-common = %{version}-%{release}
Requires:       singularity-labwc = %{version}-%{release}
Requires:       singularity-libinput = %{version}-%{release}
Requires:       singularity-fprint = %{version}-%{release}

%description
Installs the complete Singularity desktop, services, and bundled applications.

%package -n libsingularity
Summary:        Singularity libsingularity
Requires:       singularity-common = %{version}-%{release}
License:        LGPL-2.1-only
Requires:       gstreamer1-plugins-good
Requires:       gstreamer1-plugin-libav
Requires:       tesseract
Requires:       tesseract-langpack-eng

%description -n libsingularity
Libsingularity component of Singularity Desktop.

%package -n singularity-accounts
Summary:        Singularity accounts
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-accounts
Accounts component of Singularity Desktop.

%package -n singularity-atelier
Summary:        Singularity atelier
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-atelier
Atelier component of Singularity Desktop.

%package -n singularity-authenticator
Summary:        Singularity authenticator
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-authenticator
Authenticator component of Singularity Desktop.

%package -n singularity-backups
Summary:        Singularity backups
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       flatpak

%description -n singularity-backups
Backups component of Singularity Desktop.

%package -n singularity-browser
Summary:        Singularity browser
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-browser
Browser component of Singularity Desktop.

%package -n singularity-calculator
Summary:        Singularity calculator
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-calculator
Calculator component of Singularity Desktop.

%package -n singularity-calendar
Summary:        Singularity calendar
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       xdg-utils

%description -n singularity-calendar
Calendar component of Singularity Desktop.

%package -n singularity-camera
Summary:        Singularity camera
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-camera
Camera component of Singularity Desktop.

%package -n singularity-characters
Summary:        Singularity characters
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-characters
Characters component of Singularity Desktop.

%package -n singularity-clock
Summary:        Singularity clock
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-clock
Clock component of Singularity Desktop.

%package -n singularity-colorpicker
Summary:        Singularity colorpicker
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-colorpicker
Colorpicker component of Singularity Desktop.

%package -n singularity-connections
Summary:        Singularity connections
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-connections
Connections component of Singularity Desktop.

%package -n singularity-contacts
Summary:        Singularity contacts
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-contacts
Contacts component of Singularity Desktop.

%package -n singularity-database
Summary:        Singularity database
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-database
Database component of Singularity Desktop.

%package -n singularity-demo
Summary:        Singularity demo
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-demo
Demo component of Singularity Desktop.

%package -n singularity-disks
Summary:        Singularity disks
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-disks
Disks component of Singularity Desktop.

%package -n singularity-draw
Summary:        Singularity draw
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-draw
Draw component of Singularity Desktop.

%package -n singularity-drivewriter
Summary:        Singularity drivewriter
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-drivewriter
Drivewriter component of Singularity Desktop.

%package -n singularity-edit
Summary:        Singularity edit
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-edit
Edit component of Singularity Desktop.

%package -n singularity-fediverse
Summary:        Singularity fediverse
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-fediverse
Fediverse component of Singularity Desktop.

%package -n singularity-files
Summary:        Singularity files
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-files
Files component of Singularity Desktop.

%package -n singularity-fonts
Summary:        Singularity fonts
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       fontconfig

%description -n singularity-fonts
Fonts component of Singularity Desktop.

%package -n singularity-formula
Summary:        Singularity formula
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       abattis-cantarell-vf-fonts
Requires:       texlive-stix2-otf
Requires:       texlive-lm-math
Requires:       espeak-ng

%description -n singularity-formula
Formula component of Singularity Desktop.

%package -n singularity-gestures
Summary:        Singularity gestures
Requires:       singularity-common = %{version}-%{release}
License:        LGPL-2.1-only AND Apache-2.0 AND MIT
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-gestures
Gestures component of Singularity Desktop.

%package -n singularity-git
Summary:        Singularity git
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       git

%description -n singularity-git
Git component of Singularity Desktop.

%package -n singularity-greeter
Summary:        Singularity greeter
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-greeter
Greeter component of Singularity Desktop.

%package -n singularity-help
Summary:        Singularity help
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       man-db

%description -n singularity-help
Help component of Singularity Desktop.

%package -n singularity-keyframe
Summary:        Singularity keyframe
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       gstreamer1-plugins-ugly
Requires:       gstreamer1-plugins-bad-freeworld
Requires:       gstreamer1-plugin-voaacenc
Requires:       /usr/bin/ffmpeg
Requires:       /usr/bin/ffprobe

%description -n singularity-keyframe
Keyframe component of Singularity Desktop.

%package -n singularity-keyring
Summary:        Singularity keyring
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-keyring
Keyring component of Singularity Desktop.

%package -n singularity-leafs
Summary:        Singularity leafs
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-leafs
Leafs component of Singularity Desktop.

%package -n singularity-lettere
Summary:        Singularity lettere
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-lettere
Lettere component of Singularity Desktop.

%package -n singularity-loginui
Summary:        Singularity loginui
Requires:       singularity-common = %{version}-%{release}
License:        LGPL-2.1-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-loginui
Loginui component of Singularity Desktop.

%package -n singularity-logs
Summary:        Singularity logs
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-logs
Logs component of Singularity Desktop.

%package -n singularity-machines
Summary:        Singularity machines
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       qemu-system-x86-core
Requires:       qemu-img
Requires:       edk2-ovmf
Requires:       virtiofsd
Requires:       osinfo-db

%description -n singularity-machines
Machines component of Singularity Desktop.

%package -n singularity-maps
Summary:        Singularity maps
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-maps
Maps component of Singularity Desktop.

%package -n singularity-media-plugins
Summary:        Singularity media plugins
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       librespot

%description -n singularity-media-plugins
Media plugins component of Singularity Desktop.

%package -n singularity-monitor
Summary:        Singularity monitor
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-monitor
Monitor component of Singularity Desktop.

%package -n singularity-montage
Summary:        Singularity montage
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       gstreamer1-plugins-ugly
Requires:       gstreamer1-plugins-bad-freeworld
Requires:       gstreamer1-plugin-voaacenc
Requires:       /usr/bin/ffmpeg
Requires:       /usr/bin/ffprobe

%description -n singularity-montage
Montage component of Singularity Desktop.

%package -n singularity-music
Summary:        Singularity music
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-music
Music component of Singularity Desktop.

%package -n singularity-nearby
Summary:        Singularity nearby
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-nearby
Nearby component of Singularity Desktop.

%package -n singularity-nearby-app
Summary:        Singularity nearby app
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-nearby-app
Nearby app component of Singularity Desktop.

%package -n singularity-news
Summary:        Singularity news
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-news
News component of Singularity Desktop.

%package -n singularity-notes
Summary:        Singularity notes
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-notes
Notes component of Singularity Desktop.

%package -n singularity-passwords
Summary:        Singularity passwords
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-passwords
Passwords component of Singularity Desktop.

%package -n singularity-photos
Summary:        Singularity photos
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       gstreamer1-plugins-ugly
Requires:       gstreamer1-plugins-bad-freeworld
Requires:       gstreamer1-plugin-voaacenc
Requires:       /usr/bin/ffmpeg
Requires:       /usr/bin/ffprobe

%description -n singularity-photos
Photos component of Singularity Desktop.

%package -n singularity-plugins
Summary:        Singularity plugins
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       tailscale

%description -n singularity-plugins
Plugins component of Singularity Desktop.

%package -n singularity-podcasts
Summary:        Singularity podcasts
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-podcasts
Podcasts component of Singularity Desktop.

%package -n singularity-polkit-agent
Summary:        Singularity polkit agent
Requires:       singularity-common = %{version}-%{release}
License:        LGPL-2.1-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-polkit-agent
Polkit agent component of Singularity Desktop.

%package -n singularity-printers
Summary:        Singularity printers
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-printers
Printers component of Singularity Desktop.

%package -n singularity-publish
Summary:        Singularity publish
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       dejavu-serif-fonts
Requires:       rsms-inter-fonts

%description -n singularity-publish
Publish component of Singularity Desktop.

%package -n singularity-qrcodes
Summary:        Singularity qrcodes
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-qrcodes
Qrcodes component of Singularity Desktop.

%package -n singularity-radio
Summary:        Singularity radio
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-radio
Radio component of Singularity Desktop.

%package -n singularity-reader
Summary:        Singularity reader
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       espeak-ng

%description -n singularity-reader
Reader component of Singularity Desktop.

%package -n singularity-scanner
Summary:        Singularity scanner
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-scanner
Scanner component of Singularity Desktop.

%package -n singularity-session
Summary:        Singularity session
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       singularity-labwc = %{version}-%{release}
Requires:       singularity-shell = %{version}-%{release}
Requires:       singularity-polkit-agent = %{version}-%{release}
Recommends:     gdm
Requires:       xdg-user-dirs

%description -n singularity-session
Session component of Singularity Desktop.

%package -n singularity-sharing
Summary:        Singularity sharing
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only AND LGPL-2.1-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-sharing
Sharing component of Singularity Desktop.

%package -n singularity-shell
Summary:        Singularity shell
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       accountsservice
Requires:       NetworkManager
Requires:       upower
Requires:       udisks2
Requires:       bluez
Requires:       pipewire
Requires:       wireplumber
Requires:       pipewire-utils
Requires:       grim
Requires:       slurp
Requires:       wl-clipboard

%description -n singularity-shell
Shell component of Singularity Desktop.

%package -n singularity-slides
Summary:        Singularity slides
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-slides
Slides component of Singularity Desktop.

%package -n singularity-splash
Summary:        Singularity splash
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only AND LGPL-2.1-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-splash
Splash component of Singularity Desktop.

%package -n singularity-spreadsheet
Summary:        Singularity spreadsheet
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-spreadsheet
Spreadsheet component of Singularity Desktop.

%package -n singularity-store
Summary:        Singularity store
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       flatpak

%description -n singularity-store
Store component of Singularity Desktop.

%package -n singularity-tasks
Summary:        Singularity tasks
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-tasks
Tasks component of Singularity Desktop.

%package -n singularity-themes
Summary:        Singularity themes
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-themes
Themes component of Singularity Desktop.

%package -n singularity-tour
Summary:        Singularity tour
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-tour
Tour component of Singularity Desktop.

%package -n singularity-translate
Summary:        Singularity translate
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-translate
Translate component of Singularity Desktop.

%package -n singularity-usage
Summary:        Singularity usage
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-usage
Usage component of Singularity Desktop.

%package -n singularity-vector
Summary:        Singularity vector
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       ghostscript

%description -n singularity-vector
Vector component of Singularity Desktop.

%package -n singularity-videos
Summary:        Singularity videos
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-videos
Videos component of Singularity Desktop.

%package -n singularity-voice
Summary:        Singularity voice
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-voice
Voice component of Singularity Desktop.

%package -n singularity-wallpapers
Summary:        Singularity wallpapers
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-wallpapers
Wallpapers component of Singularity Desktop.

%package -n singularity-wave
Summary:        Singularity wave
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-wave
Wave component of Singularity Desktop.

%package -n singularity-weather
Summary:        Singularity weather
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-weather
Weather component of Singularity Desktop.

%package -n singularity-widgets
Summary:        Singularity widgets
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}

%description -n singularity-widgets
Widgets component of Singularity Desktop.

%package -n singularity-write
Summary:        Singularity write
Requires:       singularity-common = %{version}-%{release}
License:        GPL-3.0-only
Requires:       libsingularity = %{version}-%{release}
Requires:       gtk4 >= 4.22
Requires:       espeak-ng

%description -n singularity-write
Write component of Singularity Desktop.

%package -n xdg-desktop-portal-singularity
Summary:        Singularity xdg desktop portal singularity
Requires:       singularity-common = %{version}-%{release}
License:        LGPL-2.1-only
Requires:       libsingularity = %{version}-%{release}

%description -n xdg-desktop-portal-singularity
Xdg desktop portal singularity component of Singularity Desktop.

%package -n singularity-common
Summary:        Singularity common
Requires:       hicolor-icon-theme
Requires:       glib2
Requires:       systemd
Requires:       xdg-desktop-portal
Requires:       desktop-file-utils
Requires:       shared-mime-info

%description -n singularity-common
Common component of Singularity Desktop.

%package -n singularity-labwc
Summary:        Singularity labwc
Requires:       singularity-common = %{version}-%{release}
License:        GPL-2.0-only AND MIT
Requires:       singularity-libinput = %{version}-%{release}
Requires:       xorg-x11-server-Xwayland

%description -n singularity-labwc
Labwc component of Singularity Desktop.

%package -n singularity-libinput
Summary:        Singularity libinput
Requires:       singularity-common = %{version}-%{release}
License:        MIT

%description -n singularity-libinput
Libinput component of Singularity Desktop.

%package -n singularity-fprint
Summary:        Singularity fprint
Requires:       singularity-common = %{version}-%{release}
License:        LGPL-2.1-or-later AND GPL-3.0-only
Requires:       fprintd
Requires:       polkit
Requires:       binutils
Requires:       curl
Requires:       zstd
Requires:       xz

%description -n singularity-fprint
Fprint component of Singularity Desktop.

%package -n libsingularity-devel
Summary:        Development files for libsingularity
License:        LGPL-2.1-only
Requires:       libsingularity = %{version}-%{release}
Requires:       vala-cups

%description -n libsingularity-devel
Headers and development metadata for libsingularity.

%package -n singularity-loginui-devel
Summary:        Development files for singularity-loginui
License:        LGPL-2.1-only
Requires:       singularity-loginui = %{version}-%{release}

%description -n singularity-loginui-devel
Headers and development metadata for singularity-loginui.

%package -n singularity-gestures-devel
Summary:        Development files for singularity-gestures
License:        LGPL-2.1-only AND Apache-2.0 AND MIT
Requires:       singularity-gestures = %{version}-%{release}

%description -n singularity-gestures-devel
Headers and development metadata for singularity-gestures.

%package -n singularity-atelier-devel
Summary:        Development files for singularity-atelier
License:        GPL-3.0-only
Requires:       singularity-atelier = %{version}-%{release}

%description -n singularity-atelier-devel
Headers and development metadata for singularity-atelier.

%package -n singularity-keyframe-devel
Summary:        Development files for singularity-keyframe
License:        GPL-3.0-only
Requires:       singularity-keyframe = %{version}-%{release}

%description -n singularity-keyframe-devel
Headers and development metadata for singularity-keyframe.

%prep
%setup -q -n singularity-desktop-0.1.0
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
tar --zstd -xf %{SOURCE5} -C subprojects/vetro
tar --zstd -xf %{SOURCE9}

%build
%set_build_flags
export CFLAGS="$(printf '%s' "$CFLAGS" | sed -E 's/(^| )-g([0-9]*)?( |$)/ /g')"
export CXXFLAGS="$(printf '%s' "$CXXFLAGS" | sed -E 's/(^| )-g([0-9]*)?( |$)/ /g')"
bash %{SOURCE2}

%install
bash %{SOURCE3} "%{buildroot}" "%{SOURCE1}" "%{SOURCE4}"

%check
bash %{SOURCE7} "%{SOURCE6}" "%{SOURCE8}"
bash %{SOURCE10} build/subprojects/singularity-keyring/singularity-keyring
valac --pkg gtk4 --pkg gee-0.8 -X '-DGETTEXT_PACKAGE="singularity-keyring"' -o keyring-dialog-check %{SOURCE11} subprojects/singularity-keyring/src/unlock_dialog.vala
GTK_A11Y=none xvfb-run -a dbus-run-session -- ./keyring-dialog-check
bash %{SOURCE13} %{SOURCE12}

%files
%license LICENSE

%files -n libsingularity -f libsingularity.files
%license subprojects/libsingularity/LICENSE

%files -n singularity-accounts -f singularity-accounts.files
%license subprojects/singularity-accounts/LICENSE

%files -n singularity-atelier -f singularity-atelier.files
%license subprojects/singularity-atelier/LICENSE

%files -n singularity-authenticator -f singularity-authenticator.files
%license subprojects/singularity-authenticator/LICENSE

%files -n singularity-backups -f singularity-backups.files
%license subprojects/singularity-backups/LICENSE

%files -n singularity-browser -f singularity-browser.files
%license subprojects/singularity-browser/LICENSE

%files -n singularity-calculator -f singularity-calculator.files
%license subprojects/singularity-calculator/LICENSE

%files -n singularity-calendar -f singularity-calendar.files
%license subprojects/singularity-calendar/LICENSE

%files -n singularity-camera -f singularity-camera.files
%license subprojects/singularity-camera/LICENSE

%files -n singularity-characters -f singularity-characters.files
%license subprojects/singularity-characters/LICENSE

%files -n singularity-clock -f singularity-clock.files
%license subprojects/singularity-clock/LICENSE

%files -n singularity-colorpicker -f singularity-colorpicker.files
%license subprojects/singularity-colorpicker/LICENSE

%files -n singularity-connections -f singularity-connections.files
%license subprojects/singularity-connections/LICENSE

%files -n singularity-contacts -f singularity-contacts.files
%license subprojects/singularity-contacts/LICENSE

%files -n singularity-database -f singularity-database.files
%license subprojects/singularity-database/LICENSE

%files -n singularity-demo -f singularity-demo.files
%license subprojects/singularity-demo/LICENSE

%files -n singularity-disks -f singularity-disks.files
%license subprojects/singularity-disks/LICENSE

%files -n singularity-draw -f singularity-draw.files
%license subprojects/singularity-draw/LICENSE

%files -n singularity-drivewriter -f singularity-drivewriter.files
%license subprojects/singularity-drivewriter/LICENSE

%files -n singularity-edit -f singularity-edit.files
%license subprojects/singularity-edit/LICENSE

%files -n singularity-fediverse -f singularity-fediverse.files
%license subprojects/singularity-fediverse/LICENSE

%files -n singularity-files -f singularity-files.files
%license subprojects/singularity-files/LICENSE

%files -n singularity-fonts -f singularity-fonts.files
%license subprojects/singularity-fonts/LICENSE

%files -n singularity-formula -f singularity-formula.files
%license subprojects/singularity-formula/LICENSE

%files -n singularity-gestures -f singularity-gestures.files
%license subprojects/singularity-gestures/LICENSE runtime-notices

%files -n singularity-git -f singularity-git.files
%license subprojects/singularity-git/LICENSE

%files -n singularity-greeter -f singularity-greeter.files
%license subprojects/singularity-greeter/LICENSE

%files -n singularity-help -f singularity-help.files
%license subprojects/singularity-help/LICENSE

%files -n singularity-keyframe -f singularity-keyframe.files
%license subprojects/singularity-keyframe/LICENSE

%files -n singularity-keyring -f singularity-keyring.files
%license subprojects/singularity-keyring/LICENSE

%files -n singularity-leafs -f singularity-leafs.files
%license subprojects/singularity-leafs/LICENSE

%files -n singularity-lettere -f singularity-lettere.files
%license subprojects/singularity-lettere/LICENSE

%files -n singularity-loginui -f singularity-loginui.files
%license subprojects/singularity-loginui/LICENSE

%files -n singularity-logs -f singularity-logs.files
%license subprojects/singularity-logs/LICENSE

%files -n singularity-machines -f singularity-machines.files
%license subprojects/singularity-machines/LICENSE

%files -n singularity-maps -f singularity-maps.files
%license subprojects/singularity-maps/LICENSE

%files -n singularity-media-plugins -f singularity-media-plugins.files
%license subprojects/singularity-media-plugins/LICENSE

%files -n singularity-monitor -f singularity-monitor.files
%license subprojects/singularity-monitor/LICENSE

%files -n singularity-montage -f singularity-montage.files
%license subprojects/singularity-montage/LICENSE

%files -n singularity-music -f singularity-music.files
%license subprojects/singularity-music/LICENSE

%files -n singularity-nearby -f singularity-nearby.files
%license subprojects/singularity-nearby/LICENSE

%files -n singularity-nearby-app -f singularity-nearby-app.files
%license subprojects/singularity-nearby-app/LICENSE

%files -n singularity-news -f singularity-news.files
%license subprojects/singularity-news/LICENSE

%files -n singularity-notes -f singularity-notes.files
%license subprojects/singularity-notes/LICENSE

%files -n singularity-passwords -f singularity-passwords.files
%license subprojects/singularity-passwords/LICENSE

%files -n singularity-photos -f singularity-photos.files
%license subprojects/singularity-photos/LICENSE

%files -n singularity-plugins -f singularity-plugins.files
%license subprojects/singularity-plugins/LICENSE

%files -n singularity-podcasts -f singularity-podcasts.files
%license subprojects/singularity-podcasts/LICENSE

%files -n singularity-polkit-agent -f singularity-polkit-agent.files
%license libsingularity-LICENSE

%files -n singularity-printers -f singularity-printers.files
%license subprojects/singularity-printers/LICENSE

%files -n singularity-publish -f singularity-publish.files
%license subprojects/singularity-publish/LICENSE

%files -n singularity-qrcodes -f singularity-qrcodes.files
%license subprojects/singularity-qrcodes/LICENSE

%files -n singularity-radio -f singularity-radio.files
%license subprojects/singularity-radio/LICENSE

%files -n singularity-reader -f singularity-reader.files
%license subprojects/singularity-reader/LICENSE

%files -n singularity-scanner -f singularity-scanner.files
%license subprojects/singularity-scanner/LICENSE

%files -n singularity-session -f singularity-session.files
%license subprojects/singularity-session/LICENSE

%files -n singularity-sharing -f singularity-sharing.files
%license LICENSE sharing-LICENSE

%files -n singularity-shell -f singularity-shell.files
%license subprojects/singularity-shell/LICENSE

%files -n singularity-slides -f singularity-slides.files
%license subprojects/singularity-slides/LICENSE

%files -n singularity-splash -f singularity-splash.files
%license LICENSE libsingularity-LICENSE

%files -n singularity-spreadsheet -f singularity-spreadsheet.files
%license subprojects/singularity-spreadsheet/LICENSE

%files -n singularity-store -f singularity-store.files
%license subprojects/singularity-store/LICENSE

%files -n singularity-tasks -f singularity-tasks.files
%license subprojects/singularity-tasks/LICENSE

%files -n singularity-themes -f singularity-themes.files
%license subprojects/singularity-themes/LICENSE

%files -n singularity-tour -f singularity-tour.files
%license subprojects/singularity-tour/LICENSE

%files -n singularity-translate -f singularity-translate.files
%license subprojects/singularity-translate/LICENSE

%files -n singularity-usage -f singularity-usage.files
%license subprojects/singularity-usage/LICENSE

%files -n singularity-vector -f singularity-vector.files
%license subprojects/singularity-vector/LICENSE

%files -n singularity-videos -f singularity-videos.files
%license subprojects/singularity-videos/LICENSE

%files -n singularity-voice -f singularity-voice.files
%license subprojects/singularity-voice/LICENSE

%files -n singularity-wallpapers -f singularity-wallpapers.files
%license subprojects/singularity-wallpapers/LICENSE

%files -n singularity-wave -f singularity-wave.files
%license subprojects/singularity-wave/LICENSE

%files -n singularity-weather -f singularity-weather.files
%license subprojects/singularity-weather/LICENSE

%files -n singularity-widgets -f singularity-widgets.files
%license subprojects/singularity-widgets/LICENSE

%files -n singularity-write -f singularity-write.files
%license subprojects/singularity-write/LICENSE

%files -n xdg-desktop-portal-singularity -f xdg-desktop-portal-singularity.files
%license subprojects/xdg-desktop-portal-singularity/LICENSE

%files -n singularity-common -f singularity-common.files
%license LICENSE

%files -n singularity-labwc -f singularity-labwc.files
%license labwc-LICENSE wlroots-LICENSE scenefx-LICENSE

%files -n singularity-libinput -f singularity-libinput.files
%license subprojects/libinput/COPYING

%files -n singularity-fprint -f singularity-fprint.files
%license LICENSE libfprint-COPYING libgusb-COPYING

%files -n libsingularity-devel -f libsingularity-devel.files
%license subprojects/libsingularity/LICENSE

%files -n singularity-loginui-devel -f singularity-loginui-devel.files
%license subprojects/singularity-loginui/LICENSE

%files -n singularity-gestures-devel -f singularity-gestures-devel.files
%license subprojects/singularity-gestures/LICENSE runtime-notices

%files -n singularity-atelier-devel -f singularity-atelier-devel.files
%license subprojects/singularity-atelier/LICENSE

%files -n singularity-keyframe-devel -f singularity-keyframe-devel.files
%license subprojects/singularity-keyframe/LICENSE

