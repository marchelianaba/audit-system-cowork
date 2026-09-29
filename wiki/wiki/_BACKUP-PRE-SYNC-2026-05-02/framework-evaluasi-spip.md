# Framework Evaluasi SPIP (Penjaminan Kualitas)

**Summary**: Kerangka Penjaminan Kualitas (PK) atas Penilaian Mandiri (PM) Maturitas Penyelenggaraan SPIP Terintegrasi; dilakukan APIP berdasarkan Peraturan BPKP 5/2021 dan diimplementasikan dalam skill `evaluasi-spip` v1.4 di `audit-system-v2/` dengan alur 9 gate.

**Sources**: audit-system-v2/skills/evaluasi-spip/SKILL.md (v1.4), tasks/evaluasi-spip-bertahap.md, references/02-parameter-bobot-spip.md, PROJECT-STATUS.md.

**Last updated**: 2026-04-24

---

## Dasar Hukum

- **Peraturan BPKP 5/2021** — Penilaian Maturitas Penyelenggaraan SPIP Terintegrasi (kriteria primer).
- **PP 60/2008** — SPIP (landasan regulasi).

## Peran Inspektorat II dalam SPIP

APIP tidak melakukan PM sendiri; APIP melakukan **Penjaminan Kualitas (PK)** atas hasil PM yang disusun manajemen. Artinya:

- Kolom **Nilai PM** → diisi asesor manajemen.
- Kolom **Nilai PK** → diisi oleh APIP (Inspektorat II) secara mandiri.
- Selisih PM–PK menjadi dasar catatan dan Area of Improvement (AoI).

Aturan umum (default skill): jika bukti parsial satker, **turunkan 1 level** dari nilai PM.

## Struktur Unsur SPIP (5 Unsur)

| Unsur | Nama | Bobot (indikatif) |
|---|---|---|
| I | Lingkungan Pengendalian (1.1–1.8) | tertimbang |
| II | Penilaian Risiko (2.1–2.2) | tertimbang |
| III | Kegiatan Pengendalian (3.1–3.11) | tertimbang |
| IV | Informasi & Komunikasi (4.1, 4.2) | tertimbang |
| V | Pemantauan (5.1, 5.2) | tertimbang |

Tiga dimensi skoring: **Penetapan Tujuan (40%)**, **Struktur & Proses (30%)**, **Pencapaian Tujuan (30%)**.

## Skala Level Maturitas

| Level | Nama |
|---|---|
| 1 | Rintisan |
| 2 | Berkembang |
| 3 | Terdefinisi |
| 4 | Terkelola dan Terukur |
| 5 | Optimum |

## 9 Gate Evaluasi (Alur Bertahap)

Skill `evaluasi-spip` memecah penugasan menjadi 9 gate — setiap gate berhenti dan menunggu **LANJUT / KOREKSI / ULANG** dari auditor sebelum lanjut:

```
Gate 0 — Konfirmasi Awal (4 pertanyaan wajib):
          (1) Status Nilai PM
          (2) Cakupan satker + aturan bukti parsial
          (3) Penanganan subunsur tanpa bukti dukung
          (4) Ada/tidaknya kasus korupsi untuk KK4_PENALTI
Gate 1  — Penetapan Tujuan (split 1A KKE 1.1, 1B KKE 1.2, 1C KKE 2.1, 1D KK 2.2 RO)
Gate 2  — Struktur Proses Unsur I (Lingkungan Pengendalian 1.1–1.8)
Gate 3  — Struktur Proses Unsur II (Penilaian Risiko 2.1–2.2)
Gate 4A — Struktur Proses Unsur III-A (Kegiatan Pengendalian 3.1–3.4)
Gate 4B — Struktur Proses Unsur III-B (Kegiatan Pengendalian 3.5–3.11)
Gate 5  — Struktur Proses Unsur IV & V
Gate 6  — Pencapaian Tujuan SPIP
Gate 7  — Veto Penalti + Verifikasi Agregator
Gate 8  — AoI Final + Ringkasan Eksekutif
```

Setiap gate selesai → AoI terakumulasi ke `penugasan/SPIP/AoI-SPIP-[tahun].md` dan progress tersimpan di `penilaian-progress.json` (resume-able bila sesi terputus).

## Format AoI Standar

```
AoI-[KODE]-[NO] — [Nama Kelemahan]
Komponen / Cakupan / Nilai PK / Nilai PM / Kondisi / Dampak /
Rekomendasi / Prioritas / PIC / Target selesai
```

Kode per komponen: **PT** (Penetapan Tujuan), **LP** (Lingkungan Pengendalian), **PR** (Penilaian Risiko), **KP** (Kegiatan Pengendalian), **IK** (Informasi–Komunikasi), **PM** (Pemantauan), **PC** (Pencapaian Tujuan), **VP** (Veto Penalti).

## Hasil Pilot di Wiki

Pilot penjaminan kualitas SPIP Kemkomdigi periode Jul 2025 – Jun 2026 sedang berjalan (status per 15 April 2026 dalam PROJECT-STATUS.md):

| Gate | Sheet | Skor PM | Skor PK | Level PM → PK |
|---|---|---:|---:|---|
| 1A | KKE 1.1 SASTRA PEMDA | 97% | 60% | 5 Optimum → **2 Berkembang** |
| 1B | KKE 1.2 SASARAN OPD | 100% | 70% | 5 Optimum → **3 Terdefinisi** |

7 AoI Penetapan Tujuan sudah terbit (AoI-PT-01 sampai AoI-PT-07).

## Guard Teknis (anti-rusak formula LKE)

LKE SPIP Kementerian memuat **24 sheet** dengan **1.179 cell formula**. Skill memakai class `LKEWriter` di `fill_lke_safely.py` dengan 3 lapis guard: (1) blokir sheet agregator; (2) blokir cell per cell-map JSON; (3) blokir runtime formula. Jangan pernah isi nilai ke cell yang seharusnya formula.

## Related pages

- [[lhe-manajemen-risiko-2026]] (dokumen berdekatan — evaluasi MR yang merekomendasikan SIMR *early warning* terkait SPIP)
- [[framework-evaluasi-mr]]
- [[framework-evaluasi-sakip]]
- [[framework-evaluasi-rb]]
- [[pedoman-pengawasan-buku-i]]
- [[integrasi-audit-system]]
