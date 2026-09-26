# Mindset-Apps COPR

Personal COPR repository that tracks upstream releases and rebuilds them as RPMs,
so Fedora users can install current versions of these apps with plain `dnf`.

[![COPR](https://img.shields.io/badge/COPR-mindset%2FMindset--Apps-brightgreen)](https://copr.fedorainfracloud.org/coprs/mindset/Mindset-Apps/)

## Enable the repository

```bash
sudo dnf copr enable mindset/Mindset-Apps
sudo dnf update
```

After that, install any app from the table below, e.g.:

```bash
sudo dnf install zoom
```

## Available packages

| Package | Upstream source |
|---------|-----------------|
| `software-center` | [tofan79/software-center](https://github.com/tofan79/software-center) |
| `hyprfm` | [soyeb-jim285/hyprfm](https://github.com/soyeb-jim285/hyprfm) |
| `obscura` | [h4ckf0r0day/obscura](https://github.com/h4ckf0r0day/obscura) |
| `hyprland-preview-share-picker` | [WhySoBad/hyprland-preview-share-picker](https://github.com/WhySoBad/hyprland-preview-share-picker) |
| `gloview-git` | [fedsfarm/gloview](https://github.com/fedsfarm/gloview) (daily git build) |
| `swash` | [ItsLemmy/swash](https://github.com/ItsLemmy/swash) |
| `kineticwe-git` | [theblackdon/kineticwe](https://gitlab.com/theblackdon/kineticwe) (`kineticwe-2.0` branch) |
| `colloid-theme` | [Colloid GTK](https://github.com/vinceliuice/Colloid-gtk-theme) + [Colloid icons](https://github.com/vinceliuice/Colloid-icon-theme) (git `main` snapshots, all variants) |
| `stirling-pdf` | [Stirling-Tools/Stirling-PDF](https://github.com/Stirling-Tools/Stirling-PDF) |
| `orca-ide` | [stablyai/orca](https://github.com/stablyai/orca) |
| `intellij-idea` | [JetBrains](https://www.jetbrains.com/idea/) (API) |
| `android-studio` | [Android Studio](https://developer.android.com/studio) |
| `localsend` | [localsend/localsend](https://github.com/localsend/localsend) |
| `ab-download-manager` | [amir1376/ab-download-manager](https://github.com/amir1376/ab-download-manager) |
| `onlyoffice` | [ONLYOFFICE/DesktopEditors](https://github.com/ONLYOFFICE/DesktopEditors) |
| `zoom` | [Zoom](https://zoom.us/download) |

## How it works

Each app has a dedicated workflow that:

1. **Reads the upstream version** — from the latest GitHub release, the vendor
   API, or the vendor's download page.
2. **Reads the current COPR version** — from the last *succeeded* build.
3. **Smart Skip** — if the versions match, the workflow exits immediately
   (no build). Only when upstream publishes something new does it rebuild and
   submit a fresh SRPM to COPR.
4. **Builds & submits** — downloads the upstream artifact, renders the spec,
   builds an SRPM, and pushes it to COPR via `copr-cli`.

The `software-center` package is special-cased: its source lives in its own
repository and is rebuilt automatically (daily) whenever a new release tag
appears there.

## Development

- **Add a package:** create `specs/<name>.spec` and
  `.github/workflows/<name>.yml`, mirroring the structure of an existing entry.
- **Run a build manually:** open
  [Actions](https://github.com/tofan79/Mindset-Apps/actions), select the
  workflow, and press *Run workflow*.
- **Skipped runs** complete in under a minute; most real builds take 5–10 minutes, while KineticWE can take longer because it builds several subpackages.

## License

Individual packages carry their own upstream licenses (see each `.spec`).
Workflows and specs in this repository are provided as-is for personal use.
