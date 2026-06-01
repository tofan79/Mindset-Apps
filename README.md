# Mindset-Apps COPR

Personal COPR repository — auto-build & mirror dari GitHub Releases resmi.

## Cara Pakai

```bash
sudo dnf copr enable mindset/Mindset-Apps
sudo dnf install zen-browser localsend quickshell
sudo dnf update
```

## Apps yang Tersedia

| App | Source | Strategi | Update |
|-----|--------|----------|--------|
| zen-browser | [zen-browser/desktop](https://github.com/zen-browser/desktop) | tar.xz → RPM | tiap 3 hari |
| localsend | [localsend/localsend](https://github.com/localsend/localsend) | tar.gz → RPM | tiap 3 hari |
| quickshell | [Qutheory/quickshell](https://github.com/Qutheory/quickshell) | git checkout → RPM | manual |

## Struktur Repo

```
Mindset-Apps/
├── .github/
│   └── workflows/
│       ├── zen-browser.yml
│       ├── localsend.yml
│       ├── _template-tar-build.yml
│       └── _template-rpm-mirror.yml
├── specs/
│   ├── zen-browser.spec
│   ├── localsend.spec
│   └── quickshell.spec
└── README.md
```

## Smart Skip

Workflow cek versi upstream vs COPR sebelum build. Kalau sama → stop (<1 menit). Kalau beda → build + push (~5-10 menit).
