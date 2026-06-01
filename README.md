# Mindset-Apps COPR

Personal COPR repository — auto-build dari GitHub Releases resmi + source build.

## Cara Pakai

```bash
sudo dnf copr enable mindset/Mindset-Apps
sudo dnf install mangowm quickshell zen-browser localsend zed jetbrains-toolbox
sudo dnf update
```

## Apps yang Tersedia

| App | Source | Update |
|-----|--------|--------|
| mangowm | [mangowm/mango](https://github.com/mangowm/mango) | tiap 3 hari |
| quickshell | [quickshell-mirror/quickshell](https://github.com/quickshell-mirror/quickshell) | tiap 7 hari |
| zen-browser | [zen-browser/desktop](https://github.com/zen-browser/desktop) | tiap 3 hari |
| localsend | [localsend/localsend](https://github.com/localsend/localsend) | tiap 3 hari |
| zed | [zed-industries/zed](https://github.com/zed-industries/zed) | tiap 3 hari |
| jetbrains-toolbox | [JetBrains/toolbox](https://github.com/JetBrains/toolbox) | tiap 3 hari |

## Struktur Repo

```
Mindset-Apps/
├── .github/workflows/
│   ├── mangowm.yml
│   ├── quickshell.yml
│   ├── zen-browser.yml
│   ├── localsend.yml
│   ├── zed.yml
│   └── jetbrains-toolbox.yml
├── specs/
│   ├── mangowm.spec
│   ├── quickshell.spec
│   ├── zen-browser.spec
│   ├── localsend.spec
│   ├── zed.spec
│   └── jetbrains-toolbox.spec
└── README.md
```

## Smart Skip

Tiap workflow cek versi upstream vs COPR sebelum build. Kalau sama → stop (<1 menit). Kalau beda → build + push (~5-10 menit).
