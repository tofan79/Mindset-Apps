#!/bin/bash
set -euo pipefail

mkdir -p .rpm-tmp
export TMPDIR="$PWD/.rpm-tmp" TMP="$PWD/.rpm-tmp" TEMP="$PWD/.rpm-tmp"
export GOTMPDIR="$TMPDIR" GOCACHE="$PWD/.go-cache" GOPROXY=off
JOBS="${RPM_BUILD_NCPUS:-4}"

cp -p subprojects/labwc/LICENSE labwc-LICENSE
cp -p subprojects/labwc/subprojects/wlroots/LICENSE wlroots-LICENSE
cp -p subprojects/labwc/subprojects/scenefx/LICENSE scenefx-LICENSE
cp -p subprojects/libfprint/COPYING libfprint-COPYING
cp -p subprojects/libgusb/COPYING libgusb-COPYING
cp -p subprojects/singularity-sharing/LICENSE sharing-LICENSE

meson setup input-build subprojects/libinput --prefix=/usr --libdir=lib64/singularity \
    --datadir=share/singularity --sysconfdir=/etc --buildtype=release \
    -Ddocumentation=false -Ddebug-gui=false -Dtests=false -Dlibwacom=false -Dlua-plugins=disabled
meson compile -C input-build -j "$JOBS"

meson setup compositor-build subprojects/labwc --prefix=/usr --libdir=lib64 \
    --buildtype=release -Dxwayland=enabled \
    --force-fallback-for=wlroots-0.20,scenefx-0.5 \
    -Dwlroots:default_library=static -Dwlroots:examples=false \
    -Dscenefx:default_library=static -Dscenefx:examples=false \
    '-Dc_link_args=-Wl,-rpath,$ORIGIN/../../lib64/singularity'
meson compile -C compositor-build -j "$JOBS"

meson setup gusb-build subprojects/libgusb --prefix="$PWD/gusb-stage" --libdir=lib \
    --buildtype=release -Dtests=false -Dvapi=false -Ddocs=false \
    -Dintrospection=false -Dumockdev=disabled
meson compile -C gusb-build -j "$JOBS"
meson install -C gusb-build
meson setup fprint-build subprojects/libfprint --prefix=/usr --libdir=lib64/singularity/fprint \
    --buildtype=release --pkg-config-path="$PWD/gusb-stage/lib/pkgconfig" \
    -Ddrivers=default -Dtod=true -Dintrospection=false -Ddoc=false \
    -Dgtk-examples=false -Dinstalled-tests=false -Dudev_rules=disabled \
    -Dudev_hwdb=disabled -Dtod_extra_drivers_dir=/var/lib/singularity/fprint/tod-1
meson compile -C fprint-build -j "$JOBS"

if [ -f build/build.ninja ]; then
    meson configure build -Dsingularity-media-plugins:librespot=disabled
fi
meson setup build --prefix=/usr --libdir=lib64 --libexecdir=/usr/libexec \
    --sysconfdir=/etc --localstatedir=/var --buildtype=release \
    -Dapps=all -Dgestures=enabled -Dinstaller=false -Dsingularity-media-plugins:librespot=disabled
meson compile -C build -j "$JOBS"
