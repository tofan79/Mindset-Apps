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
| localsend | [localsend/localsend](https://github.com/localsend/localsend) | tiap 3 hari |
| zed | [zed-industries/zed](https://github.com/zed-industries/zed) | tiap 3 hari |
| intellij-idea-community | [JetBrains API](https://www.jetbrains.com/idea/) | tiap 3 hari |
| android-studio | [developer.android.com](https://developer.android.com/studio) | tiap 3 hari |

## Struktur Repo

```
Mindset-Apps/
├── .github/workflows/
│   ├── zen-browser.yml
│   ├── localsend.yml
│   ├── zed.yml
│   ├── intellij-idea-community.yml
│   └── android-studio.yml
├── specs/
│   ├── zen-browser.spec
│   ├── localsend.spec
│   ├── zed.spec
│   ├── intellij-idea-community.spec
│   └── android-studio.spec
└── README.md
```

## Smart Skip

Tiap workflow cek versi upstream vs COPR sebelum build. Kalau sama → stop (<1 menit). Kalau beda → build + push (~5-10 menit).
