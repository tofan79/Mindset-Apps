#!/bin/bash
set -euo pipefail
STAGE="$1"
cp -p subprojects/libsingularity/LICENSE libsingularity-LICENSE
meson install -C build --destdir "$STAGE" --no-rebuild
install -Dm644 subprojects/libsingularity/src/vapi/upower-glib.vapi "$STAGE/usr/share/vala/vapi/upower-glib.vapi"
for binary in singularity-leafs singularity-atelier singularity-keyframe singularity-browser; do
    chrpath -d "$STAGE/usr/bin/$binary"
done

install -Dm755 compositor-build/labwc "$STAGE/usr/libexec/singularity/labwc"
install -d "$STAGE/usr/lib64/singularity" "$STAGE/usr/share/singularity/libinput"
cp -a input-build/libinput.so.10* "$STAGE/usr/lib64/singularity/"
cp -a subprojects/libinput/quirks/*.quirks "$STAGE/usr/share/singularity/libinput/"
install -d "$STAGE/usr/lib64/singularity/fprint"
meson install -C fprint-build --destdir "$PWD/fprint-stage" --no-rebuild
find fprint-stage/usr/lib64/singularity/fprint -name 'libfprint*.so.*' \( -type f -o -type l \) \
    -exec cp -a '{}' "$STAGE/usr/lib64/singularity/fprint/" \;
cp -a gusb-stage/lib/libgusb.so.2* "$STAGE/usr/lib64/singularity/fprint/"
install -Dm755 data/fprint/singularity-fprint-driver "$STAGE/usr/libexec/singularity-fprint-driver"
install -d "$STAGE/usr/share/polkit-1/actions"
sed 's|@LIBEXECDIR@|/usr/libexec|g' data/fprint/dev.sinty.fprint-driver.policy \
    > "$STAGE/usr/share/polkit-1/actions/dev.sinty.fprint-driver.policy"
install -d "$STAGE/usr/lib/systemd/system/fprintd.service.d"
cat > "$STAGE/usr/lib/systemd/system/fprintd.service.d/singularity-fprint.conf" <<'EOF'
[Service]
Environment=LD_LIBRARY_PATH=/usr/lib64/singularity/fprint
ExtensionDirectories=-/var/lib/singularity/fprint/singularity-fprint-drivers
EOF
for launcher in singularity-labwc-session singularity-desktop-session; do
    sed -i 's|export PATH="$BIN:$PATH"|export PATH="/usr/libexec/singularity:$BIN:$PATH"|' "$STAGE/usr/bin/$launcher"
done
sed -i 's|LIB="$PREFIX/lib"|LIB="$PREFIX/lib64"|' "$STAGE/usr/bin/singularity-desktop-session"
sed -i 's|LD_LIBRARY_PATH="$PREFIX/lib${|LD_LIBRARY_PATH="$PREFIX/lib64/singularity${|' "$STAGE/usr/bin/singularity-labwc-session"
bash -n "$STAGE/usr/bin/singularity-labwc-session" "$STAGE/usr/bin/singularity-desktop-session"
sed 's/^Name=org.freedesktop.secrets$/Name=dev.sinty.keyring/' \
    "$STAGE/usr/share/dbus-1/services/org.freedesktop.secrets.service" \
    > "$STAGE/usr/share/dbus-1/services/dev.sinty.keyring.service"
python3 - "$STAGE" <<'PYINSTALL'
from pathlib import Path
import sys
stage = Path(sys.argv[1])
(stage / 'usr/share/dbus-1/services/org.freedesktop.secrets.service').unlink()
launcher = stage / 'usr/bin/singularity-desktop-session'
text = launcher.read_text()
needle = '_polkit_agent="$(singularity_helper singularity-polkit-agent)"'
assert text.count(needle) == 1
text = text.replace(needle, '''_keyring="$(singularity_helper singularity-keyring)"
nohup "$_keyring" >> "$_STATE/keyring.log" 2>&1 &
record_helper "$!" "$_keyring"
''' + needle)
launcher.write_text(text)
PYINSTALL
bash -n "$STAGE/usr/bin/singularity-desktop-session"
install -d "$STAGE/usr/share/wayland-sessions"
cat > "$STAGE/usr/share/wayland-sessions/singularity.desktop" <<'EOF'
[Desktop Entry]
Name=Singularity
Comment=Singularity Desktop
Exec=env SINGULARITY_LABWC_BINARY=/usr/libexec/singularity/labwc singularity-labwc-session
Type=Application
DesktopNames=Singularity
EOF
sed -i 's|^ExecStart=.*|ExecStart=/usr/libexec/xdg-desktop-portal-singularity|' \
    "$STAGE/usr/lib/systemd/user/xdg-desktop-portal-singularity.service"
install -d "$STAGE/usr/lib/systemd/user/singularity-session.target.wants"
ln -s ../xdg-desktop-portal-singularity.service \
    "$STAGE/usr/lib/systemd/user/singularity-session.target.wants/xdg-desktop-portal-singularity.service"
python3 "$2" build "$STAGE" "$3"
