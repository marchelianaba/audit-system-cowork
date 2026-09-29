# Index Reference yang Dipakai Sistem Audit v4

**Summary**: Index seluruh kriteria/regulasi/standar yang dipakai sistem audit-system-v4 sebagai dasar judgement temuan. Di-aggregate dari (1) field `kriteria` di `_KKP/temuan.json` semua penugasan, (2) `references/` tiap skill di `skills/`, (3) PDF di `wiki/raw/`.

**Sources**: di-aggregate oleh `scripts/ingest_to_wiki.py`.

**Last updated**: _(akan di-update otomatis)_

---

## A. Standar Profesi

| Reference | Status | Lokasi |
|---|---|---|
| **PER-01/AAIPI/DPN/2021** — Standar Audit Intern Pemerintah Indonesia (SAIPI) | ✅ tersedia | `wiki/raw/SAIPI-PER-01-AAIPI-DPN-2021.pdf` |
| Skill aktif: [[../../skills/kepatuhan-saipi/SKILL]] (auto-check per penugasan) | ✅ | — |

## B. Regulasi Pengadaan

| Reference | Status | Dipakai di |
|---|---|---|
| Perpres 16/2018 — Pengadaan Barang/Jasa Pemerintah | dirujuk di temuan | audit-pengadaan, reviu-pengadaan |
| Perpres 12/2021 — perubahan Perpres 16/2018 | dirujuk | sda |
| Perka LKPP 12/2021 — Pedoman Pelaksanaan PBJ | dirujuk | sda |

## C. Regulasi Akuntabilitas Kinerja

| Reference | Status | Dipakai di |
|---|---|---|
| PermenPAN-RB 88/2021 — Pedoman Evaluasi AKIP | dirujuk | evaluasi-sakip |
| PermenPAN-RB tentang RB | TBD | evaluasi-reformasi-birokrasi |

## D. Regulasi SPIP / MR

| Reference | Status | Dipakai di |
|---|---|---|
| PP 60/2008 — Sistem Pengendalian Intern Pemerintah | dirujuk | evaluasi-spip |
| PerBPKP 5/2021 — Penjaminan Kualitas SPIP | dirujuk | evaluasi-spip |
| Permenkominfo 6/2017 — Pedoman MR (legacy, perlu update) | dirujuk | evaluasi-manajemen-risiko |
| ISO 31000 — Risk Management | dirujuk | evaluasi-manajemen-risiko |

## E. Regulasi RKA-K/L

| Reference | Status | Dipakai di |
|---|---|---|
| PMK tentang Reviu RKA-K/L (versi terbaru — perlu cek) | TBD | reviu-rka-kl |

## F. Reference Internal Inspektorat II

| Reference | Status | Dipakai di |
|---|---|---|
| Pedoman Buku III — Penyusunan KKP | TBD | semua skill assurance |
| Pedoman Umum Bab III — Pelaporan Hasil Pengawasan | TBD | semua skill |
| Renstra Itjen 2025-2029 | TBD | strategis |

---

## Reference yang Sering Dirujuk di Temuan (auto-aggregated)

> _Di-regenerate oleh `scripts/ingest_to_wiki.py`. Frekuensi dihitung dari field `kriteria`._

| Reference (truncated 80) | Frekuensi | Penugasan terkait |
|---|---:|---|
| Perpres 16/2018 Pasal 19 ayat (1) jo. Perka LKPP 12/2021 menyatakan KAK wajib me | 1 | CONTOH-2026-05-001-reviu-pengadaan-bakti |
| Perpres 16/2018 Pasal 19 ayat (1) jo. Perka LKPP 12/2021. | 1 | CONTOH-HAPPY-PATH-saipi |

_(updated 2026-05-02)_


---

## Cross-link

- [[_INDEX-V4]]
- [[pattern-temuan]]
- Skill `skills/kepatuhan-saipi/references/` — kutipan SAIPI verbatim
- `wiki/raw/` — PDF dokumen mentah
