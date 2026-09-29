# Konfigurasi Model AI — Audit System v2

Dokumen ini adalah **master reference** assignment model Claude per task dan skill.
Tujuan: efisiensi token tanpa mengorbankan kualitas output pengawasan.

---

## Prinsip Assignment

| Model | String | Digunakan untuk |
|---|---|---|
| **Haiku** | `claude-haiku-4-5-20251001` | Routing, checklist, validasi administratif, pengisian form, template sederhana |
| **Sonnet** | `claude-sonnet-4-6` | Analisis dokumen, generate KKP/LHP, evaluasi, reviu, narasi temuan |

> **Aturan dasar**: Jika ragu, gunakan Sonnet. Haiku hanya untuk tugas yang hasilnya bisa diprediksi dan tidak memerlukan penalaran mendalam.

---

## Assignment per Task

| File | Task | Model | Alasan |
|---|---|---|---|
| `01-start-audit.md` | Inisiasi Penugasan | **Haiku** | Baca ST, isi form context.md, routing ke skill yang tepat |
| `02b-generate-kp-pkp.md` | Generate KP & PKP | **Haiku** | Mengisi template Word dengan data dari context.md, tidak analitik. **Khusus audit-kinerja**: Sonnet karena SP butuh penajaman sasaran + research online benchmarking |
| `_ARSIP-02-analisis-dokumen.md` | (ARSIP) Validasi Dokumen | — | Dihilangkan dari alur v2.5 untuk hemat token. File listing + ringkasan kini inline di Task 03 |
| `03-generate-kkp.md` | Generate KKP | **Sonnet** | Analisis mendalam dokumen, sintesis KKSA, temuan kompleks |
| `04-generate-lhp.md` | Generate LHP Substansi (tahap akhir otomasi) | **Sonnet** | Narasi analitik, menulis temuan, rekomendasi, simpulan berkualitas |
| `_ARSIP-05-generate-administrasi.md` | (ARSIP) Administrasi & Nota Dinas | — | Dihilangkan dari alur v2.7 — dikerjakan auditor manual di Word (nomor surat dari SIMWAS, TTD wajib manusia). Hemat token + waktu |
| `_ARSIP-monthly-summary.md` | Rekapitulasi Bulanan | **Sonnet** | Agregasi data lintas penugasan, statistik, laporan bulanan |
| `_ARSIP-reviu-temuan-interaktif.md` | Reviu Temuan Interaktif | **Sonnet** | Dialog iteratif review temuan, perlu pemahaman konteks mendalam |

---

## Assignment per Skill (audit-system-v2/skills/)

| Skill | Model | Alasan |
|---|---|---|
| `audit-kinerja` | **Sonnet** | Analisis 3E, temuan kompleks, akar masalah, rekomendasi strategis |
| `audit-pengadaan` | **Sonnet** | Analisis multi-tahap, perhitungan kerugian, analisis CCSAA lengkap |
| `evaluasi-manajemen-risiko` | **Sonnet** | Evaluasi governance, analisis ISO 31000, identifikasi AoI |
| `evaluasi-reformasi-birokrasi` | **Sonnet** | Evaluasi 4 dimensi × komponen RB, narasi dampak |
| `evaluasi-sakip` | **Sonnet** | Skoring 12 sub-komponen tertimbang, LKE + LHE AKIP |
| `evaluasi-spip` | **Sonnet** | Penilaian maturitas SPIP/MRI/IEPK, identifikasi penalti korupsi |
| `konsultasi-pengadaan` | **Haiku** | Advisory ringan, penjelasan regulasi, saran prosedur |
| `pemantauan-pengadaan` | **Haiku** | Pelaporan status real-time, early warning, tidak ada analisis mendalam |
| `reviu-pengadaan` | **Sonnet** | Validasi multi-aspek pengadaan, catatan KKSA (tanpa sebab) |
| `reviu-rka-kl` | **Sonnet** | Validasi 6 aspek RKA, checklist anggaran vs standar biaya |

---

## Assignment Skill Support (.claude/skills/)

| Skill | Model | Alasan |
|---|---|---|
| `isi-laporan` | **Sonnet** | Ekstraksi temuan KKP, isi substansi laporan, adaptasi narasi |
| `reviu-dokumen-auditor` | **Sonnet** | Analisis KKSA dokumen, generasi KKA Excel |
| `docx` | **Haiku** | Operasi file teknis, tidak analitik |
| `pdf` | **Haiku** | Operasi file teknis, tidak analitik |
| `xlsx` | **Haiku** | Operasi file teknis, tidak analitik |
| `pptx` | **Haiku** | Operasi file teknis, tidak analitik |
| `schedule` | **Haiku** | Setup teknis, bukan analitik |
| `skill-creator` | **Sonnet** | Development skill baru, perlu pemahaman konteks sistem |

---

## Panduan Implementasi

Setiap file task dan SKILL.md sudah ditambahkan header:
```
> **Model**: `claude-haiku-4-5-20251001`
```
atau
```
> **Model**: `claude-sonnet-4-6`
```

Auditor atau Claude yang men-dispatch tugas harus membaca header ini sebelum menjalankan task.

---

## Estimasi Penghematan

Berdasarkan distribusi penugasan tipikal:
- Task 01, 02b → ~20% volume percakapan → dialihkan ke Haiku
- Konsultasi + Pemantauan → ~15% volume → dialihkan ke Haiku
- Task 05 (eks-administrasi) → ~10% volume → **dihilangkan** (manual di Word sejak v2.7)
- Sisa (analisis berat: Task 03, Task 04) → ~55% tetap di Sonnet

**Estimasi penghematan token gabungan: ~50–65%** dari baseline pre-v2.5, dengan kualitas output analitik tidak terdegradasi.
