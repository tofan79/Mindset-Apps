#!/bin/bash
set -euo pipefail
CHECK_DIR="$(mktemp -d "${TMPDIR:?}/c.XXXXXX")"
cleanup() {
    for attempt in 1 2 3; do
        if rm -rf -- "$CHECK_DIR"; then return; fi
        sleep 1
    done
}
trap cleanup EXIT
export TMPDIR="$CHECK_DIR" TMP="$CHECK_DIR" TEMP="$CHECK_DIR"
export GTK_A11Y=none TZ=UTC
mkdir -p "$CHECK_DIR/runtime" "$CHECK_DIR/cache" "$CHECK_DIR/data" "$CHECK_DIR/config"
chmod 700 "$CHECK_DIR/runtime"
export XDG_RUNTIME_DIR="$CHECK_DIR/runtime" XDG_CACHE_HOME="$CHECK_DIR/cache"
export XDG_DATA_HOME="$CHECK_DIR/data" XDG_CONFIG_HOME="$CHECK_DIR/config"
unset XDG_DATA_DIRS
xvfb-run -a dbus-run-session -- bash -c '
    export SLIDES_UI_TEST_DISPLAY="$DISPLAY" PUBLISH_UI_TEST_DISPLAY="$DISPLAY"
    exec "$@"
' rpm-check meson test -C build --print-errorlogs --num-processes 2 --timeout-multiplier 3 --wrapper="env TMPDIR=$TMPDIR TMP=$TMP TEMP=$TEMP XDG_CACHE_HOME=$XDG_CACHE_HOME XDG_DATA_HOME=$XDG_DATA_HOME XDG_CONFIG_HOME=$XDG_CONFIG_HOME"
mkdir -p .rpm-check
python3 - "$1" "$2" <<'PY'
from pathlib import Path
import re
import subprocess
import sys
source = Path('subprojects/singularity-write')
meson = (source / 'meson.build').read_text()
engine = re.search(r'engine = files\((.*?)\n\)', meson, re.S).group(1)
sources = [str(source / name) for name in re.findall(r"'([^']+\.vala)'", engine)]
sources += [str(source / 'src/ui/doc_view.vala'), str(source / 'tests/harness.vala'), sys.argv[1], sys.argv[2]]
lib = Path('build/subprojects/libsingularity').resolve()
command = ['valac', '--vapidir=' + str(lib), '-o', '.rpm-check/write-accessibility-test']
packages = ['gtk4', 'gee-0.8', 'gio-2.0', 'libxml-2.0', 'zlib', 'pangocairo', 'json-glib-1.0', 'sqlite3', 'singularity-1.0']
packages += Path('subprojects/libsingularity/singularity-1.0.deps').read_text().split()
for package in dict.fromkeys(packages):
    command += ['--pkg', package]
for flag in ['-DGETTEXT_PACKAGE="singularity-write"', '-I' + str(lib), '-L' + str(lib), '-lsingularity', '-lm', '-lz', '-Wl,-rpath,' + str(lib)]:
    command += ['--Xcc=' + flag]
subprocess.run(command + sources, check=True)
PY
xvfb-run -a dbus-run-session -- .rpm-check/write-accessibility-test
