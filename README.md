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
sudo dnf install zen-browser
```

## Available packages

| Package | Upstream source | Update schedule |
|---------|-----------------|-----------------|
| `zen-browser` | [zen-browser/desktop](https://github.com/zen-browser/desktop) | every 3 days |
| `zed` | [zed-industries/zed](https://github.com/zed-industries/zed) | every 3 days |
| `intellij-idea` | [JetBrains](https://www.jetbrains.com/idea/) (API) | weekly (Mon) |
| `localsend` | [localsend/localsend](https://github.com/localsend/localsend) | weekly (Tue) |
| `android-studio` | [Android Studio](https://developer.android.com/studio) | weekly (Wed) |
| `ab-download-manager` | [amir1376/ab-download-manager](https://github.com/amir1376/ab-download-manager) | weekly (Thu) |
| `onlyoffice-desktopeditors` | [ONLYOFFICE/DesktopEditors](https://github.com/ONLYOFFICE/DesktopEditors) | weekly (Fri) |
| `zoom` | [Zoom](https://zoom.us/download) | weekly (Sun) |
| `software-center` | [tofan79/software-center](https://github.com/tofan79/software-center) | daily (auto) |

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

## Repository layout

```
Mindset-Apps/
├── .github/workflows/   # one workflow per package
│   ├── zen-browser.yml
│   ├── zed.yml
│   ├── intellij-idea.yml
│   ├── localsend.yml
│   ├── android-studio.yml
│   ├── ab-download-manager.yml
│   ├── onlyoffice-desktopeditors.yml
│   ├── zoom.yml
│   └── software-center.yml
├── specs/               # one RPM spec per package
│   ├── zen-browser.spec
│   ├── zed.spec
│   ├── intellij-idea.spec
│   ├── localsend.spec
│   ├── android-studio.spec
│   ├── ab-download-manager.spec
│   ├── onlyoffice-desktopeditors.spec
│   ├── zoom.spec
│   └── software-center.spec
└── README.md
```

## Development

- **Add a package:** create `specs/<name>.spec` and
  `.github/workflows/<name>.yml`, mirroring the structure of an existing entry.
- **Run a build manually:** open
  [Actions](https://github.com/tofan79/Mindset-Apps/actions), select the
  workflow, and press *Run workflow*.
- **Skipped runs** complete in under a minute; real builds take 5–10 minutes.

## License

Individual packages carry their own upstream licenses (see each `.spec`).
Workflows and specs in this repository are provided as-is for personal use.
