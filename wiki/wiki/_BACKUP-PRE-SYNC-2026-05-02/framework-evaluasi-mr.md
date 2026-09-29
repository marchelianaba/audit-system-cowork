# Framework Evaluasi Manajemen Risiko

**Summary**: Kerangka evaluasi efektivitas Manajemen Risiko di lingkungan Kemkomdigi; kriteria primer adalah Pedoman Menkomdigi 6/2017 (perlu revisi — lihat [[lhe-manajemen-risiko-2026]]) dengan ISO 31000:2018 sebagai pendukung. Diimplementasikan dalam skill `evaluasi-manajemen-risiko` v2.0.

**Sources**: audit-system-v2/skills/evaluasi-manajemen-risiko/SKILL.md (v2.0); references/01-pedoman-menkomdigi-6-2017.md; [[lhe-manajemen-risiko-2026]].

**Last updated**: 2026-04-24

---

## Dasar Hukum

- **Pedoman Menkomdigi 6/2017** — kriteria primer evaluasi MR di Komdigi (masih nomenklatur Kominfo lama — sudah ditandai usang di [[lhe-manajemen-risiko-2026]]).
- **ISO 31000:2018** — referensi pendukung bila pedoman internal belum mengatur.

## Struktur MR (Kriteria Organisasi)

- **KMR** — Komite Manajemen Risiko (eselon I).
- **UPR** — Unit Pemilik Risiko (per unit kerja).
- **Peran Itjen** — APIP sebagai *assurance & consulting* MR.

## 6 Kategori Risiko (Pedoman Menkomdigi 6/2017)

Dijabarkan dalam Pedoman; digunakan untuk klasifikasi register risiko. *(Daftar kategori lengkap di `references/01-pedoman-menkomdigi-6-2017.md`; ingest penuh ke wiki bila perlu.)*

## Skala Penilaian

- **Kemungkinan**: 5 level.
- **Dampak**: 6 area × 5 level.
- **Matriks Analisis Risiko**: 5×5 → level risiko.
- **Selera Risiko**: sedang ke atas **wajib ditangani**.

## 5 Proses MR

1. **Komunikasi & Konsultasi**
2. **Penetapan Konteks**
3. **Penilaian Risiko** (identifikasi → analisis → evaluasi)
4. **Penanganan Risiko**
5. **Pemantauan & Tinjauan**

## 5 Opsi Penanganan Risiko

Avoid — Reduce — Share (transfer) — Accept — Exploit (bila risiko juga peluang).

## Model Kematangan TKPMR (5 Level)

| Level | Nama |
|---|---|
| 1 | Risk Naive |
| 2 | Risk Aware |
| 3 | Risk Defined |
| 4 | Risk Managed |
| 5 | Risk Enable |

## Struktur Laporan Khusus

Laporan evaluasi MR berbeda dengan audit/reviu:

- **F. Hasil Evaluasi** — berisi **catatan naratif bernomor** format **KKSA** (Kondisi–Kriteria–Sebab–Akibat).
- **G. Rekomendasi** — dikompilasi **terpisah** (bukan bagian dari tiap catatan F).
- **H. Apresiasi** — penutup.

Tiap catatan F memuat: Judul → Kondisi (fakta dari dokumen) → Kriteria (Pedoman Menkomdigi 6/2017, ISO 31000 bila perlu) → Sebab → Akibat.

## Dokumen yang Diperlukan (urutan prioritas)

1. **Piagam Manajemen Risiko** + Formulir 1 (Konteks), Formulir 2 (Profil & Peta Risiko), Formulir 3 (Penanganan Risiko).
2. **Laporan Pemantauan Triwulan** (Formulir 4) seluruh TW periode evaluasi.
3. **Laporan Pemantauan Tahunan** (Formulir 5) bila tersedia.
4. **LED** (Loss Event Database) — catatan risiko yang benar-benar terjadi.
5. **SK/struktur** Komite MR dan penetapan UPR.
6. **Dokumen SPIP** — AoI dari penilaian BPKP bila ada (cross-referenced dengan [[framework-evaluasi-spip]]).

## Kode Surat

PW.04.05.

## Hasil Historis di Wiki

- [[lhe-manajemen-risiko-2026]] — LHE MR Kemkomdigi, B-70, Feb 2026. **6 catatan**:
  1. Pedoman MR usang (masih Permenkominfo 6/2017 — perlu revisi ke Permenkomdigi).
  2. Three Lines Model belum optimal.
  3. Belum ada standar kompetensi SDM MR.
  4. SIMR belum ada *early warning*.
  5. SIMR belum terintegrasi lintas unit.
  6. Belum ada prosedur insiden.

Pola: kriteria evaluasi itu sendiri (Pedoman 6/2017) sudah menua — revisi pedoman adalah prasyarat agar evaluasi MR ke depan lebih relevan.

## Kaitan dengan Framework Lain

- [[framework-evaluasi-spip]] — SPIP mencakup MR sebagai unsur Penilaian Risiko; LHE MR bisa jadi input AoI SPIP.
- [[pedoman-pengawasan-buku-i]] — 7 jenis risiko (Error, Fraud, Theft, Regulatory, Disclosure, Disruption, Value for Money) = taksonomi yang berbeda dari kategori MR 6/2017; bisa digunakan saling melengkapi.

## Related pages

- [[lhe-manajemen-risiko-2026]]
- [[framework-evaluasi-spip]]
- [[framework-evaluasi-sakip]]
- [[framework-evaluasi-rb]]
- [[pedoman-pengawasan-buku-i]]
- [[integrasi-audit-system]]
