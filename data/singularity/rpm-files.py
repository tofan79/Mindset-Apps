import argparse
import json
import posixpath
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('build')
parser.add_argument('stage')
parser.add_argument('manifest')
args = parser.parse_args()
build = Path(args.build)
stage = Path(args.stage)
manifest = json.loads(Path(args.manifest).read_text())
components = set(manifest['expected_installed_components'])
plan = json.loads((build / 'meson-info/intro-install_plan.json').read_text())
installed = json.loads((build / 'meson-info/intro-installed.json').read_text())
source_owners = {source: item.get('subproject') or 'singularity-common'
                 for group in plan.values() for source, item in group.items()}
owners = {}
subdirs = []
for source, destination in installed.items():
    owner = source_owners.get(source)
    if owner is None:
        parts = Path(source).parts
        if 'subprojects' in parts:
            owner = parts[parts.index('subprojects') + 1]
        elif '/' in source:
            owner = 'singularity-common'
    if owner is not None:
        if owner not in components | {'singularity-common'}:
            raise ValueError(f'Unexpected component: {owner}')
        owners[destination] = owner
        if Path(source).is_dir():
            subdirs.append((destination.rstrip('/') + '/', owner))
subdirs.sort(key=lambda item: len(item[0]), reverse=True)
extra = {
    '/usr/share/vala/vapi/upower-glib.vapi': 'libsingularity',
    '/usr/share/icons/Singularity': 'singularity-themes',
    '/usr/share/themes/Singularity/': 'singularity-themes',
    '/usr/libexec/singularity/labwc': 'singularity-labwc',
    '/usr/lib64/singularity/libinput': 'singularity-libinput',
    '/usr/share/singularity/libinput/': 'singularity-libinput',
    '/usr/lib64/singularity/fprint/': 'singularity-fprint',
    '/usr/libexec/singularity-fprint-driver': 'singularity-fprint',
    '/usr/share/polkit-1/actions/dev.sinty.fprint-driver.policy': 'singularity-fprint',
    '/usr/lib/systemd/system/fprintd.service.d/': 'singularity-fprint',
    '/usr/share/wayland-sessions/singularity.desktop': 'singularity-session',
    '/usr/share/dbus-1/services/dev.sinty.keyring.service': 'singularity-keyring',
}
files = [p for p in stage.rglob('*') if p.is_file() or p.is_symlink()]
for path in files:
    name = '/' + str(path.relative_to(stage))
    for prefix, owner in extra.items():
        if name.startswith(prefix):
            owners[name] = owner
    if name not in owners:
        for prefix, owner in subdirs:
            if name.startswith(prefix):
                owners[name] = owner
                break
for path in files:
    name = '/' + str(path.relative_to(stage))
    if name not in owners and path.is_symlink():
        target = path.readlink().as_posix()
        target = posixpath.normpath(target if target.startswith('/') else posixpath.dirname(name) + '/' + target)
        if target in owners:
            owners[name] = owners[target]
missing = ['/' + str(p.relative_to(stage)) for p in files if '/' + str(p.relative_to(stage)) not in owners]
if missing:
    raise ValueError('Unassigned installed files: ' + ', '.join(missing))
groups = {}
for path in files:
    name = '/' + str(path.relative_to(stage))
    owner = owners[name]
    if name.endswith(('.h', '.vapi', '.deps', '.pc', '.gir', '.a')) or (name.endswith('.so') and path.is_symlink()):
        owner += '-devel'
    line = ('%config(noreplace) ' if name.startswith('/etc/') else '') + '"' + name.replace('%', '%%') + '"'
    groups.setdefault(owner, []).append(line)
directories = {}
for name, owner in owners.items():
    if not (stage / name.lstrip('/')).exists() and not (stage / name.lstrip('/')).is_symlink():
        continue
    for parent in Path(name).parents:
        directory = parent.as_posix()
        if 'singularity' in directory.lower() or directory.startswith('/usr/share/themes/Kids'):
            directories.setdefault(directory, set()).add(owner)
for directory, assigned in directories.items():
    owner = next(iter(assigned)) if len(assigned) == 1 else 'singularity-common'
    groups.setdefault(owner, []).append('%dir "' + directory.replace('%', '%%') + '"')
for name in components | {'singularity-common', 'singularity-labwc', 'singularity-libinput', 'singularity-fprint'}:
    groups.setdefault(name, [])
for owner, entries in groups.items():
    Path(owner + '.files').write_text('\n'.join(sorted(entries)) + '\n')
Path('rpm-file-coverage.json').write_text(json.dumps({
    'installed_files': len(files),
    'owned_directories': len(directories),
    'packages': {owner: len(entries) for owner, entries in sorted(groups.items())},
    'unassigned_files': missing,
}, indent=2) + '\n')
print(f'{len(files)} installed files assigned to {len(groups)} packages')
