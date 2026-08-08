# Mindset-Apps COPR

Personal COPR repository — auto-build dari GitHub Releases resmi + source build.

## Cara Pakai

```bash
sudo dnf copr enable mindset/Mindset-Apps
sudo dnf update
```

## Apps yang Tersedia

| App | Source | Update |
|-----|--------|--------|
| zen-browser | [zen-browser/desktop](https://github.com/zen-browser/desktop) | tiap 3 hari |
| zed | [zed-industries/zed](https://github.com/zed-industries/zed) | tiap 3 hari |
| intellij-idea | [JetBrains API](https://www.jetbrains.com/idea/) | tiap 7 hari (Senin) |
| localsend | [localsend/localsend](https://github.com/localsend/localsend) | tiap 7 hari (Selasa) |
| android-studio | [developer.android.com](https://developer.android.com/studio) | tiap 7 hari (Rabu) |
| ab-download-manager | [amir1376/ab-download-manager](https://github.com/amir1376/ab-download-manager) | tiap 7 hari (Kamis) |
| onlyoffice-desktopeditors | [ONLYOFFICE/DesktopEditors](https://github.com/ONLYOFFICE/DesktopEditors) | tiap 7 hari (Jumat) |
| software-center | [tofan79/software-center](https://github.com/tofan79/software-center) | manual |

## Struktur Repo

```
Mindset-Apps/
├── .github/workflows/
│   ├── zen-browser.yml
│   ├── localsend.yml
│   ├── zed.yml
│   ├── intellij-idea.yml
│   ├── android-studio.yml
│   ├── ab-download-manager.yml
│   ├── onlyoffice-desktopeditors.yml
│   └── software-center.yml
├── specs/
│   ├── zen-browser.spec
│   ├── localsend.spec
│   ├── zed.spec
│   ├── intellij-idea.spec
│   ├── android-studio.spec
│   ├── ab-download-manager.spec
│   ├── onlyoffice-desktopeditors.spec
│   └── software-center.spec
└── README.md
```

## Smart Skip

Tiap workflow cek versi upstream vs COPR sebelum build. Kalau sama → stop (<1 menit). Kalau beda → build + push (~5-10 menit).
