# Mindset-Apps COPR

Personal COPR repository — auto-build & mirror dari GitHub Releases resmi.

## Cara Pakai

```bash
# Enable repo
sudo dnf copr enable mindset/Mindset-Apps

# Install apps
sudo dnf install zen-browser
sudo dnf install localsend

# Update semua otomatis
sudo dnf update
```

## Apps yang Tersedia

| App | Source | Strategi | Jadwal Update |
|-----|--------|----------|---------------|
| zen-browser | [zen-browser/desktop](https://github.com/zen-browser/desktop) | tar.xz → RPM | tiap 3 hari |
| localsend | [localsend/localsend](https://github.com/localsend/localsend) | tar.gz → RPM | tiap 3 hari |

## Struktur Repo

```
Mindset-Apps/
├── .github/
│   └── workflows/
│       ├── zen-browser.yml           ← auto-build tiap 3 hari
│       ├── localsend.yml             ← auto-build tiap 3 hari
│       ├── _template-tar-build.yml   ← template app tanpa RPM
│       └── _template-rpm-mirror.yml  ← template app yang punya RPM
├── specs/
│   ├── zen-browser.spec
│   └── localsend.spec
└── README.md
```

## Menambah App Baru

### App yang sudah punya RPM
1. Duplikat `_template-rpm-mirror.yml`
2. Ganti bagian `env:` — `APP_NAME`, `GITHUB_REPO`, `RPM_PATTERN`
3. Commit — selesai!

### App yang tidak punya RPM (tar.gz / tar.xz)
1. Duplikat `_template-tar-build.yml`
2. Ganti bagian `env:`
3. Buat `specs/namaapp.spec` (duplikat dari spec yang ada)
4. Commit — selesai!

## Smart Skip

Setiap workflow cek versi upstream vs COPR sebelum build.
Kalau sama → stop otomatis (< 1 menit).
Kalau beda → build + push ke COPR (~5-10 menit).
