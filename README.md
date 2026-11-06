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

52 packages total, all with successful COPR builds.

Packages are listed alphabetically.

| Package | Upstream source | Deskripsi (fungsi app) | Catatan kemasan |
|---------|----------------|------------------------|-----------------|
| `ab-download-manager` | [amir1376/ab-download-manager](https://github.com/amir1376/ab-download-manager) | AB Download Manager — Fast & powerful download manager | — |
| `ambxst` | [Axenide/Ambxst](https://github.com/Axenide/Ambxst) | Axtremely customizable Quickshell desktop shell with Go daemon | Go daemon + Quickshell shell; runtime quickshell/axctl/wl-clipboard manual |
| `android-studio` | [Android Studio](https://developer.android.com/studio) | Android Studio — The official Android IDE | — |
| `ario` | [peymanAzad/ario](https://github.com/peymanAzad/ario) | Terminal download manager powered by aria2 | repack RPM x86_64 upstream; TUI + daemon, butuh `aria2` |
| `aura` | [antwny/aura](https://github.com/antwny/aura) | Live wallpaper manager for COSMIC, GNOME, KDE, and Wayland | repack tarball x86_64 upstream; live wallpaper Rust + mpvpaper, GNOME/KDE/COSMIC |
| `arroxy` | [antonio-orionus/Arroxy](https://github.com/antonio-orionus/Arroxy) | Free video downloader for YouTube and 2000+ other sites | — |
| `artcraft-launcher` | [storytold/craft-launcher](https://github.com/storytold/craft-launcher) | Install, update and launch the Craft App Suite | launcher Rust; aplikasi Craft diunduh sendiri saat runtime |
| `axctl` | [Axenide/axctl](https://github.com/Axenide/axctl) | Axtremely flexible compositor daemon/CLI (config + brightness + IPC) | Go compositor daemon/CLI: config, brightness, IPC — dipakai ambxst |
| `caelestia-cli` | [caelestia-dots/cli](https://github.com/caelestia-dots/cli) | Command line tool for the Caelestia desktop shell | — |
| `caelestia-shell` | [caelestia-dots/shell](https://github.com/caelestia-dots/shell) | Caelestia desktop shell for Wayland compositors (Quickshell) | bundles libcava + m3shapes |
| `colloid-theme` | [Colloid GTK](https://github.com/vinceliuice/Colloid-gtk-theme) | Colloid GTK and icon themes | https://github.com/vinceliuice/Colloid-icon-theme) (git `main` snapshots, all variants |
| `end4-pc` | [pctrade/end4-pC](https://github.com/pctrade/end4-pC) | end4-pC Quickshell shell config (fork of dots-hyprland ii) | config Quickshell fork dots-hyprland untuk Hyprland; base: `illogical-impulse` |
| `gabarito-fonts` | [google/fonts](https://github.com/google/fonts) | Gabarito variable display font (Google Fonts) | font variabel, font "important" iNiR |
| `gloview-git` | [fedsfarm/gloview](https://github.com/fedsfarm/gloview) | macOS Mission Control-style overview plugin for Hyprland (daily git build) | daily git build |
| `hyprfm` | [soyeb-jim285/hyprfm](https://github.com/soyeb-jim285/hyprfm) | Fast keyboard-friendly file manager for Hyprland | build source tag CMake/Qt6 + submodule Quill/quill-icons |
| `hyprland-preview-share-picker` | [WhySoBad/hyprland-preview-share-picker](https://github.com/WhySoBad/hyprland-preview-share-picker) | Alternative share picker for Hyprland with window and monitor previews | — |
| `illogical-impulse` | [end-4/dots-hyprland](https://github.com/end-4/dots-hyprland) | Quickshell-based Hyprland desktop shell (dots-hyprland snapshot) | snapshot master shell Quickshell "ii" untuk Hyprland; base untuk `end4-pc` |
| `impasto-shell` | [andreumassanet/impasto](https://github.com/andreumassanet/impasto) | Impasto Quickshell desktop shell for Hyprland | payload Quickshell untuk Hyprland; runtime quickshell/awww manual |
| `inir-shell` | [snowarch/iNiR](https://github.com/snowarch/iNiR) | iNiR desktop shell payload, launcher, and user service (Niri/Quickshell) | payload shell Quickshell untuk Niri + launcher dan unit systemd user |
| `intellij-idea` | [JetBrains](https://www.jetbrains.com/idea/) | IntelliJ IDEA — Leading Java and Kotlin IDE (unified) | API |
| `localsend` | [localsend/localsend](https://github.com/localsend/localsend) | LocalSend — Share files to nearby devices, no internet needed | — |
| `material-symbols-fonts` | [google/material-design-icons](https://github.com/google/material-design-icons) | Material Symbols Rounded variable icon font (Google) | variable Rounded icon font |
| `mixtapes-git` | [m-obeid/Mixtapes](https://github.com/m-obeid/Mixtapes) | Modern, Linux-first YouTube Music player (daily git build) | daily git build; upstream belum punya tag/release |
| `monologue` | [omacom/monologue](https://github.com/omacom/monologue) | Theme-synced webcam recorder with a built-in trim editor | — |
| `nandoroid-shell` | [na-ive/nandoroid-shell](https://github.com/na-ive/nandoroid-shell) | NAnDoroid Quickshell desktop shell for Hyprland | payload Quickshell Material 3 untuk Hyprland; runtime quickshell/matugen manual |
| `nautilus-open-any-terminal-git` | [Stunkymonkey/nautilus-open-any-terminal](https://github.com/Stunkymonkey/nautilus-open-any-terminal) | Nautilus extension adding a context menu entry for other terminal emulators | daily git build |
| `nuclear` | [nukeop/nuclear](https://github.com/nukeop/nuclear) | Music player for your desktop built with Tauri and WebKit | repack RPM x86_64 upstream |
| `obscura` | [h4ckf0r0day/obscura](https://github.com/h4ckf0r0day/obscura) | Fast embeddable browser automation engine with native rendering | — |
| `omacut` | [omacom/omacut](https://github.com/omacom/omacut) | Dead-simple video length trimmer built with Qt Quick and ffmpeg | — |
| `omanta` | [28allday/omanta](https://github.com/28allday/omanta) | Native file manager for Omarchy (Qt Quick + GIO) | — |
| `omareel-git` | [omacom/omareel](https://github.com/omacom/omareel) | Minimal, keyboard-driven video cutter for Wayland compositors | daily git build |
| `omashow-git` | [28allday/omashow](https://github.com/28allday/omashow) | Keyboard-first presentation editor and presenter | daily git build |
| `omawrite` | [omacom/omawrite](https://github.com/omacom/omawrite) | Dead-simple Markdown writing app built with Qt Quick | — |
| `onlyoffice` | [ONLYOFFICE/DesktopEditors](https://github.com/ONLYOFFICE/DesktopEditors) | ONLYOFFICE Desktop Editors | — |
| `openidea` | [l0ng-ai/openidea](https://github.com/l0ng-ai/openidea) | Open-source IDE inspired by IntelliJ IDEA | repack RPM x86_64 upstream; IDE Tauri/WebKit |
| `orca-ide` | [stablyai/orca](https://github.com/stablyai/orca) | Orca IDE — Multimodal AI-native code editor | — |
| `oxanium-fonts` | [google/fonts](https://github.com/google/fonts) | Oxanium variable display font (Google Fonts) | font variabel, font "important" iNiR |
| `phosphor-icons-fonts` | [phosphor-icons/web](https://github.com/phosphor-icons/web) | Phosphor icon family fonts | 6 weight ikon, dipakai ambxst |
| `rakuos-bootstrap` | [tofan79/rakuos-bootstrap](https://github.com/tofan79/rakuos-bootstrap) | Wizard pasca-install untuk RakuOS minimal | wizard pasca-install RakuOS minimal, release tag |
| `rakuos-shell-picker` | [tofan79/rakuos-shell-picker](https://github.com/tofan79/rakuos-shell-picker) | Pick the desktop shell (Noctalia/DMS/Caelestia/Ambxst) on Hyprland | Rust + GTK4; pilih desktop shell di atas Hyprland |
| `sekaipop-shell` | [Blapples/SekaiPop](https://github.com/Blapples/SekaiPop) | SekaiPop Quickshell desktop shell for Hyprland | payload Quickshell Project Sekai untuk Hyprland; daily git build |
| `software-center` | [tofan79/software-center](https://github.com/tofan79/software-center) | Software Center — install and manage apps, Flatpaks, and system updates | — |
| `sonora` | [sonorahq/sonora](https://github.com/sonorahq/sonora) | Native music streaming client built with Rust and GPUI | repack AppImage x86_64 upstream |
| `stirling-pdf` | [Stirling-Tools/Stirling-PDF](https://github.com/Stirling-Tools/Stirling-PDF) | Stirling PDF — Locally hosted web app for PDF operations | — |
| `swash` | [ItsLemmy/swash](https://github.com/ItsLemmy/swash) | Fast screenshot annotator and lightweight image editor (GTK4/libadwaita) | — |
| `sysc-greet` | [Nomadcxx/sysc-greet](https://github.com/Nomadcxx/sysc-greet) | Greeter TUI untuk greetd di atas cagebreak | greeter TUI untuk greetd, varian cagebreak |
| `ttfx` | [omacom/ttfx](https://github.com/omacom/ttfx) | Terminal text effects, a Rust port of terminaltexteffects | — |
| `umbriel-git` | [noctalia-dev/umbriel](https://github.com/noctalia-dev/umbriel) | Wayland compositor built on wlroots (daily build) | Wayland compositor wlroots; daily git build, paket `umbriel` + session `umbriel.desktop` |
| `whisker-cli` | [corecathx/whisker-cli](https://github.com/corecathx/whisker-cli) | CLI helper for the Whisker Quickshell shell | CLI pendamping Whisker; daily git build |
| `whisker-shell` | [corecathx/whisker](https://github.com/corecathx/whisker) | Whisker Quickshell desktop shell for Hyprland | payload Quickshell Material 3 untuk Hyprland; daily git build |
| `zapfast` | [crmne/zapfast](https://github.com/crmne/zapfast) | Fast native WhatsApp client built with Rust and egui | repack RPM x86_64 upstream; klien WhatsApp native Rust + egui |
| `zoom` | [Zoom](https://zoom.us/download) | Zoom Workplace — video conferencing, team chat and collaboration | — |
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

`nuclear`, `sonora`, `zapfast`, `ario`, `openidea`, and `aura` do not compile
anything in COPR. Upstream already publishes an x86_64 artifact (an RPM,
an AppImage for `sonora`, or a tarball for `aura`), so the workflow downloads
it, unpacks the payload, and repacks the same files into an RPM. Builds finish
in seconds and cannot break on a dependency change, at the cost of shipping
upstream's binary rather than one compiled on Fedora.

For upstream projects without tags, `whisker-shell`, `whisker-cli`, and
`sekaipop-shell` use the latest commit on `main`. Their RPM version is
`<base>.<commit-date>.git<short-sha>`; a new commit produces a new version, and
a commit that already has a successful COPR build is skipped by the same Smart
Skip logic. `nandoroid-shell` and `impasto-shell` use the latest release tag,
falling back to the highest numeric tag when no GitHub release exists.
`impasto-shell` uploads only the shell files to COPR instead of the upstream
desktop archive.

Packages with a `-git` suffix in their name are rolling: they re-evaluate on
every run (smart-skip by commit SHA), and there is no release-to-release
migration step for them. Release-tracking and repack packages never move
automatically unless a new tag or release asset appears upstream.

## Development

- **Add a package:** create `specs/<name>.spec` and
  `.github/workflows/<name>.yml`, mirroring the structure of an existing entry.
- **Run a build manually:** open
  [Actions](https://github.com/tofan79/Mindset-Apps/actions), select the
  workflow, and press *Run workflow*.
- **Skipped runs** complete in under a minute; most real builds take 5–10 minutes, 

## License

Individual packages carry their own upstream licenses (see each `.spec`).
Workflows and specs in this repository are provided as-is for personal use.
