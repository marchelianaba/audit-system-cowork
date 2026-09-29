# Framework Evaluasi SAKIP

**Summary**: Kerangka evaluasi Sistem Akuntabilitas Kinerja Instansi Pemerintah (SAKIP/AKIP) yang dipakai Inspektorat II; mengacu PermenPAN-RB 88/2021 dan diimplementasikan dalam skill `evaluasi-sakip` v5.0 di `audit-system-v4/`.

**Sources**: audit-system-v4/skills/evaluasi-sakip/SKILL.md (v5.0); PermenPAN-RB 88/2021.

**Last updated**: 2026-04-24

---

## Dasar Hukum

- **PermenPAN-RB 88/2021** — Pedoman Evaluasi AKIP (kriteria primer).
- **Perpres 29/2014** — SAKIP.
- **PP 8/2006** — Pelaporan Keuangan dan Kinerja Instansi Pemerintah.

## Struktur Penilaian

Penilaian dibagi ke dalam **4 komponen** dengan total bobot 100:

| # | Komponen | Keberadaan | Kualitas | Pemanfaatan | **Total** |
|---|---|---:|---:|---:|---:|
| 1 | Perencanaan Kinerja | 6 | 9 | 15 | **30** |
| 2 | Pengukuran Kinerja | 6 | 9 | 15 | **30** |
| 3 | Pelaporan Kinerja | 3 | 4,5 | 7,5 | **15** |
| 4 | Evaluasi AKIP Internal | 5 | 7,5 | 12,5 | **25** |

Sub-komponen "Keberadaan" menjawab *apakah dokumen ada*; "Kualitas" menjawab *apakah isinya baik*; "Pemanfaatan" menjawab *apakah benar-benar dipakai*. Total ada **79 kriteria**.

## Skala Predikat APIP

| Predikat | Nilai |
|---|---:|
| AA | 100 |
| A | 90 |
| BB | 80 |
| B | 70 |
| CC | 60 |
| C | 50 |
| D | 30 |
| E | 0 |

**Formula**: Nilai Sub-Komponen = (Predikat ÷ 100) × Bobot.

## Paradigma Evaluasi (skill v5.0)

- Setiap predikat APIP harus didukung **kutipan/observasi spesifik** dari dokumen, bukan nilai evaluator sebelumnya (tidak *copy-paste* nilai PM).
- Folder bukti dukung dikelola per kode sub-komponen: `1_a/`, `1_b/`, `2_a/`, dst.
- Skrip `read_local_bukti.py` mengekstrak teks PDF/xlsx dari folder dan menambahkannya ke JSON agar Claude bisa membaca ratusan halaman dalam menit.

## Output Standar

- **LKE Excel** (APIP) — kolom predikat dan catatan terisi.
- **LHE AKIP** (.docx) — laporan akhir sesuai template Inspektorat II.
- **KKP Markdown** — kertas kerja pengawasan.

## Hasil Historis di Wiki

Belum ada LHE SAKIP mandiri yang terekam; yang ada adalah reviu LKj (sub-set dari SAKIP):
- [[lhr-lkj-kemkomdigi-2025]] — CHR LKj Kemkomdigi TA 2025; 2 catatan.
- [[lhr-lkj-ekosistem-digital-2025]] — skor penuh.
- [[lhr-lkj-wasdig-2025]] — skor penuh; IKSP 1.2 = 93,025% (target 74%).

## Kapan Pakai Skill Ini

- Saat APIP melakukan evaluasi AKIP tahunan (biasanya Jan–Mar).
- Input: Folder bukti dukung per sub-komponen + LKE Excel.
- Output: Nilai per sub-komponen + predikat + catatan + rekomendasi.

## Catatan

- Rumus LKE tidak boleh ditimpa — gunakan pola yang sama dengan `evaluasi-spip` (lapisan guard anti-timpa formula).
- Untuk skor lintas tahun, rujuk dokumen evaluasi AKIP sebelumnya agar tren terlihat.

## Related pages

- [[pedoman-pengawasan-buku-i]]
- [[framework-evaluasi-spip]]
- [[framework-evaluasi-rb]]
- [[framework-evaluasi-mr]]
- [[integrasi-audit-system]]
- [[lhr-lkj-kemkomdigi-2025]]
- [[lhr-lkj-wasdig-2025]]
- [[lhr-lkj-ekosistem-digital-2025]]
