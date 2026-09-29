# CHANGELOG v2.8 — Paket Transformasi Efektivitas, Efisiensi, & Power

**Tanggal rilis:** 19 April 2026
**Baseline:** v2.7 (16 April 2026)
**Skope:** audit-system-v2/
**Tipe rilis:** major-feature (non-breaking)

---

## TL;DR

v2.8 menambahkan 4 pilar baru ke sistem audit tanpa mengubah alur 4-task yang sudah stabil:

1. **Quality Control otomatis** — script validator KKP/LHP anti-halusinasi + anti-placeholder-bocor.
2. **Observability** — dashboard penugasan yang me-rangkum status semua penugasan aktif dalam 1 tabel markdown.
3. **Propagasi gate-based** — template 7-gate SAKIP dan 9-gate RB, mengikuti pola SPIP yang sudah terbukti.
4. **Foundation untuk growth** — skill TLHP skeleton, references 3 skill kosong terseed, pattern library untuk temuan berulang.

Tidak ada perubahan pada `tasks/01-04`, `README.md`, `MODEL-CONFIG.md`, atau alur eksekusi existing. Sistem tetap compatible penuh dengan penugasan SPIP Kemkomdigi 2026 yang sedang berjalan.

---

## Perubahan (per file)

### Baru

| File | Tipe | Tujuan |
|------|------|--------|
| `SECURITY.md` | security advisories | Dokumentasi SEC-01 GitHub token plaintext, SEC-02 klasifikasi dokumen penugasan, SEC-03 proteksi sistem |
| `scripts/qc_kkp_lhp.py` | script QC | Validator KKP (sumber dokumen, format judul, tidak ada rek) dan LHP (placeholder bocor, bahasa keyakinan, font) |
| `scripts/dashboard_penugasan.py` | script observability | Dashboard markdown status semua penugasan: gate, tim, AoI, age indicator |
| `scripts/ringkasan_mingguan.py` | script observability | Ringkasan mingguan LHP final: nomor ST, judul, temuan, rekomendasi (auto-extract dari AoI-*.md / LHP docx) |
| `tasks/evaluasi-sakip-bertahap.md` | template gate-based | 7 gate untuk evaluasi SAKIP, pola SPIP bertahap |
| `tasks/evaluasi-rb-bertahap.md` | template gate-based | 9 gate untuk evaluasi RB, pola SPIP bertahap |
| `skills/pemantauan-tindak-lanjut/SKILL.md` | skill baru (skeleton) | Pemantauan TLHP BPK/BPKP/APIP dengan aging analysis |
| `checklists/pemantauan-tindak-lanjut.md` | checklist skill baru | Daftar dokumen yang diminta untuk pemantauan TLHP |
| `skills/audit-kinerja/references/README.md` | seed references | Kerangka 8 file regulasi + metodologi yang perlu diisi |
| `skills/audit-kinerja/references/08-checklist-survey-pendahuluan.md` | seed references | Checklist lengkap Survey Pendahuluan (AAIPI 3100) |
| `skills/konsultasi-pengadaan/references/README.md` | seed references | Kerangka 5 file rujukan + format output konsultasi |
| `skills/evaluasi-manajemen-risiko/references/README.md` | seed references | Kerangka 7 file: ISO/COSO/BPKP MRI + integrasi dengan SPIP |
| `pattern-library/README.md` | folder baru | Dokumentasi mekanisme pattern library + template |
| `pattern-library/_index.md` | index | Daftar pattern aktif/draft/deprecated |
| `pattern-library/reviu-pengadaan/P-RP-001-*.md` | pattern seed | KAK tidak konsisten SLA (dari feedback pilot Apr 2026) |
| `pattern-library/reviu-pengadaan/P-RP-002-*.md` | pattern seed | HPS kurang komponen migrasi (dari feedback pilot Apr 2026) |
| `CHANGELOG-v2.8.md` | dokumentasi | File ini |

### Dimodifikasi

Tidak ada — v2.8 additive-only. Prinsip "jangan modifikasi `tasks/`, `skills/`, `checklists/`, `README.md` saat penugasan berjalan" dihormati.

**Catatan:** README.md belum di-update. Setelah auditor SETUJU seluruh v2.8, auditor (atau Claude di luar mode penugasan) perlu menambahkan:
- Section "v2.8" di perubahan utama
- Penyebutan `scripts/qc_kkp_lhp.py`, `dashboard_penugasan.py`, dan `ringkasan_mingguan.py` di bagian "Tooling"
- Penambahan `pemantauan-tindak-lanjut` ke daftar skill aktif

---

## Cara Pakai Tooling Baru

### QC Validator

```bash
cd audit-system-v2/

# Cek KKP + LHP
python3 scripts/qc_kkp_lhp.py penugasan/SPIP/

# Hanya LHP
python3 scripts/qc_kkp_lhp.py penugasan/SPIP/ --only lhp

# Strict mode (exit 1 jika ada warning)
python3 scripts/qc_kkp_lhp.py penugasan/SPIP/ --strict
```

**Integrasi alur yang direkomendasikan:**
- **Sebelum auditor SETUJU Task 03**: jalankan `--only kkp`. Jika ERROR, iterasi KKP dulu.
- **Sebelum auditor SETUJU Task 04**: jalankan `--only lhp`. Jika ERROR, iterasi LHP dulu.
- Validasi di-jalankan Claude di akhir Task 03/04 sebelum meminta konfirmasi auditor (upgrade bertahap ke tasks/03,04 di rilis minor berikutnya).

### Dashboard

```bash
python3 scripts/dashboard_penugasan.py
python3 scripts/dashboard_penugasan.py --save   # tulis dashboard.md
```

**Integrasi alur:**
- Jalankan di awal sesi untuk cepat orientasi status penugasan aktif.
- Jalankan weekly untuk laporan ke atasan (PIC monitoring Inspektur II).

### Ringkasan Mingguan

```bash
# Default: minggu berjalan (Senin-Minggu), auto-save ke ringkasan-mingguan/YYYY-MM-DD.md
python3 scripts/ringkasan_mingguan.py

# Minggu tertentu (tanggal apa saja dalam minggu target)
python3 scripts/ringkasan_mingguan.py --minggu 2026-04-13

# Snapshot semua LHP (bukan hanya minggu berjalan)
python3 scripts/ringkasan_mingguan.py --all-time

# Preview ke stdout tanpa menulis file
python3 scripts/ringkasan_mingguan.py --stdout
```

**Yang dihasilkan:** 1 file `ringkasan-mingguan/YYYY-MM-DD.md` (tanggal Senin minggu target) berisi per penugasan: Nomor ST, Judul ST, tabel Temuan + Rekomendasi.

**Sumber ekstraksi (urutan prioritas):**
1. `AoI-*.md` di folder penugasan — paling terstruktur, ambil per `### AoI-XX-NN` + section `**Rekomendasi:**`
2. Fallback: `_LHP/*.docx` (butuh `python-docx`) — ambil paragraf bernomor + "Rekomendasi:"

**Kriteria "final minggu ini":** file .docx/.pdf di `_LHP/` yang bukan `*draft*` dengan mtime di window Senin 00:00 — Minggu 23:59. Untuk week boundary yang berbeda (mis. jadwal lapor Inspektur), pakai `--minggu`.

**Integrasi alur:**
- Jalankan setiap Jumat sore / Senin pagi untuk ringkasan minggu sebelumnya.
- Output .md siap dilampirkan ke Nota Dinas Inspektur atau share ke tim.
- Smoke tested 19 Apr 2026: 2 penugasan terdeteksi (SAKIP, SPIP) — 26 AoI dari SPIP berhasil diekstrak otomatis lengkap dengan rekomendasi.

---

## Status Tiap Pilar

| Pilar | Status | Tindakan Lanjutan |
|-------|--------|-------------------|
| QC otomatis | ✅ script siap, perlu piloting | Jalankan di penugasan SPIP aktif; iterasi kalau false positive tinggi |
| Dashboard | ✅ script siap, sudah tested | Tambah kolom custom (misal: PIC, deadline) saat kebutuhan muncul |
| Gate-based SAKIP | ⬜ template skeleton | Pilot di evaluasi SAKIP 2026 (target Q2 2026) |
| Gate-based RB | ⬜ template skeleton | Pilot di evaluasi PMPRB TW1 2026 (target Q2 2026) |
| Skill TLHP | ⬜ skeleton | Pilot di pemantauan TLHP Semester I 2026 (target Jun 2026) |
| References 3 skill | ⬜ kerangka seed | Auditor isi konten per prioritas yang ditulis di README references |
| Pattern library | ✅ seed + 2 pattern | Tumbuh organik setiap Task 04 selesai; mining LHP historis sebagai bonus |
| Security advisories | ✅ terdokumentasi | Auditor tindaklanjuti SEC-01 (revoke + migrate token) |

---

## Metrik Sukses v2.8 (usulan)

| Metrik | Baseline | Target 3 bulan | Target 6 bulan |
|--------|----------|---------------|----------------|
| References 3 skill terisi | 7/18 file | 12/18 | 18/18 |
| Pattern library aktif | 2 pattern | 5 pattern | 10 pattern |
| Penugasan yang jalan dengan QC pre-gate | 0% | 50% | 100% |
| Penugasan gate-based (SAKIP/RB) | 0 | 1 penugasan pilot | 2+ penugasan |
| Skill TLHP dipakai | skeleton | pilot | rutin semester |
| Latency rata-rata Task 03→auditor review | ? | -20% dari baseline | -30% |

---

## Appendix A — Usulan Fitur Power Baru (roadmap v2.9+)

Berdasarkan arahan auditor untuk menambahkan fitur yang belum ada di roadmap. Ini **belum diimplementasikan di v2.8** — didokumentasikan untuk prioritisasi di rilis berikutnya.

### A.1. Semantic Search KKP & LHP Historis
Indeks FTS (full-text search) lokal untuk seluruh KKP/LHP yang sudah closing. Query "temuan serupa soal HPS kemahalan di 2024" → Claude mem-pull preseden untuk konteks. Implementasi: SQLite FTS5 + embedding kecil. Keuntungan: konsistensi lintas penugasan, precedent-aware.

### A.2. Auto-benchmark via WebSearch (audit-kinerja saja)
Extend Task 02b audit-kinerja untuk otomatis cari 3–5 benchmark terbaru (OECD/WB/INTOSAI + BPK/BPKP) relevan dengan obyek, sitasi URL+tanggal akses otomatis dilekatkan ke Memo SP. Hemat 30 menit per penugasan.

### A.3. Auto-draft Usulan PKPT
Dari hasil dashboard + pattern library + aging TLHP, generate draft usulan PKPT tahun berikutnya (paket mana yang perlu di-audit, mana di-reviu, mana di-pantau). Auditor tinggal kurasi + rapatkan di sidang PKPT.

### A.4. Pre-commit Hook untuk Proteksi Sistem
Git hook lokal yang mencegah commit perubahan ke `tasks/`, `skills/`, `checklists/`, `README.md` kecuali commit message memuat tag `[MAINT]` (mode pemeliharaan). Menegakkan SEC-03 secara teknis, bukan hanya aturan tertulis.

### A.5. Standar Red-Team Self-Review
Tambah fase opsional "Red Team" setelah Task 03 dan sebelum auditor review: Claude kedua di-prompt sebagai "auditor BPK yang skeptis" untuk menyerang temuan. Hasil: list tantangan yang harus dijawab sebelum LHP. Implementasi murah via Agent tool di sesi yang sama.

### A.6. Integrasi Read-Only SIMWAS
Jika SIMWAS punya API/export, buat connector untuk fetch daftar ST aktif + status nomor surat. Claude tetap tidak menulis ke SIMWAS (per feedback_sistem.md), tapi mengurangi manual copy-paste.

### A.7. Auto-seed Folder Penugasan Baru
Script `init_penugasan.py <nomor-ST> <jenis>` yang otomatis: buat folder 00-05, copy template LHP yang benar ke `_LHP/`, copy KP+PKP template (Jalur B) kalau applicable, tulis context.md awal. Hemat 5 menit × setiap penugasan baru.

### A.8. Knowledge Graph Temuan
Graph yang menghubungkan temuan ↔ obyek/satker ↔ regulasi ↔ PIC ↔ rekomendasi. Berguna untuk query: "Semua rekomendasi yang belum selesai dari BPK & Itjen untuk Ditjen Infradigi" — saat ini manual lookup, bisa instant. Implementasi: Neo4j lokal atau cukup networkx + export Mermaid.

Prioritas usulan (berdasarkan biaya/benefit):
1. **A.7** (auto-seed) — quick win, pakai di setiap penugasan baru
2. **A.4** (pre-commit hook) — keamanan sistem
3. **A.1** (semantic search) — return besar untuk konsistensi
4. **A.5** (red-team) — peningkatan kualitas tanpa major refactor
5. **A.2, A.3, A.6, A.8** — tergantung roadmap strategis

---

## Catatan Migration

v2.8 non-breaking — tidak perlu migrasi data. Penugasan SPIP aktif bisa lanjut tanpa ada gangguan.

Jika auditor ingin mulai memakai QC validator di penugasan yang sudah berjalan:
1. Pastikan python-docx sudah terinstal: `pip install python-docx --break-system-packages`
2. Jalankan `python3 scripts/qc_kkp_lhp.py penugasan/[nama]/ --only kkp` sebelum konfirmasi SETUJU Task 03.
3. Sama untuk Task 04 dengan `--only lhp`.

---

## Who Tested What (traceability) — verified 19 Apr 2026

- `dashboard_penugasan.py` ✅ **smoke tested** di `penugasan/` live. 3 penugasan terdeteksi: CONTOH-Dinkes (MERAH, tidak aktif), SAKIP (HIJAU), SPIP (HIJAU, 26 AoI di gate_4_penyimpulan_akhir:PENDING_REVIEW). Output Markdown ter-save di `audit-system-v2/dashboard.md`.
- `qc_kkp_lhp.py` ✅ **smoke tested** di `penugasan/SPIP/LHP-SUBSTANSI-SPIP-2026.docx`. Exit 0, 0 error + 1 warning (5 run font non-Arial) — menunjukkan validator berfungsi: memang benar template LHP standar adalah Arial.
- Template gate-based SAKIP/RB → belum di-pilot. Struktur mengikuti pola `evaluasi-spip-bertahap.md` yang sudah terbukti.
- Skill TLHP → skeleton, belum dipilot.
- Pattern library → di-seed dari feedback historis yang sudah terbukti di Reviu DC/DRC PSrE 2026.
- References 3 skill → kerangka seed (README + 1 file substantif `08-checklist-survey-pendahuluan.md` untuk audit-kinerja). Konten full regulasi/metodologi menunggu pengisian auditor per prioritas di masing-masing README.
