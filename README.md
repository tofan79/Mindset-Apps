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
| mangowm | [mangowm/mango](https://github.com/mangowm/mango) | tiap 3 hari |
| zen-browser | [zen-browser/desktop](https://github.com/zen-browser/desktop) | tiap 3 hari |
| localsend | [localsend/localsend](https://github.com/localsend/localsend) | tiap 3 hari |
| zed | [zed-industries/zed](https://github.com/zed-industries/zed) | tiap 3 hari |
| jetbrains-toolbox | [jetbrains.com/toolbox](https://jetbrains.com/toolbox) | tiap 3 hari |

## Struktur Repo

```
Mindset-Apps/
├── .github/workflows/
│   ├── mangowm.yml
│   ├── zen-browser.yml
│   ├── localsend.yml
│   ├── zed.yml
│   └── jetbrains-toolbox.yml
├── specs/
│   ├── mangowm.spec
│   ├── zen-browser.spec
│   ├── localsend.spec
│   ├── zed.spec
│   └── jetbrains-toolbox.spec
└── README.md
```

## Smart Skip

Tiap workflow cek versi upstream vs COPR sebelum build. Kalau sama → stop (<1 menit). Kalau beda → build + push (~5-10 menit).
