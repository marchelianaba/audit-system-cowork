# CHANGELOG v4.0 — Role-Based Workflow + INTEGRAL JSON + Audit Trail

**Tanggal rilis:** 2 Mei 2026
**Baseline:** v3 (folder `audit-system v3/` per 27 April 2026)
**Tipe rilis:** **major** (alur task berubah, ada deny rule baru, output format berubah)

---

## v4.4 — Kodefikasi PermenPAN 42/2011 (1 Juni 2026)

**Tanggal rilis:** 1 Juni 2026
**Tipe:** patch — feature addition, backward-compatible (kodefikasi nullable di schema, temuan lama tanpa kodefikasi tetap valid)
**Tujuan:** Auto-generate kode atribut temuan dan rekomendasi sesuai PermenPAN dan RB No. 42 Tahun 2011 (Lampiran 2.1 dan 2.2). Hilangkan langkah manual auditor mencari kode di PDF saat menyusun KKP.

### Tambahan File

- **`references/permenpan-42-2011-kode.json`** (BARU, 89 kode temuan + 14 kode rekomendasi dalam JSON terstruktur). Di-generate dari PDF `Kode_Atribut_Temuan_PermenPAN_42_2011.pdf`. Struktur: 3 kelompok temuan dengan sub-kategori, setiap kode temuan punya `alt_rekomendasi` (list kode rekomendasi yang valid). Whitelisted di `ATURAN-ISOLASI-SUMBER.md` sebagai sumber kodefikasi.

### Update Schema

- **`schemas/kkp-temuan.schema.json`** — tambah 4 field baru di `Temuan`:
  - `kodefikasi_temuan` — regex `^[123]\.0[1-9]\.[0-9]{2}$` (format X.YY.ZZ)
  - `kodefikasi_temuan_reasoning` — string justifikasi pilihan kode (untuk audit trail)
  - `kodefikasi_rekomendasi` — array of string, regex `^(0[1-9]|1[0-4])$` per item
  - `kodefikasi_sebab` — pending klarifikasi enum dari tim SIMWAS, sementara nullable

### Update Task

- **`tasks/03-generate-kkp.md`** — Step 6E BARU "Auto-Pilih Kodefikasi PermenPAN 42/2011". Claude baca reference JSON, cocokkan Kondisi temuan ke deskripsi kode (semantic matching, Pendekatan A), tulis reasoning, validasi alt-rekomendasi, lalu konfirmasi via HITL.

### Update Aturan Isolasi

- **`skills/ATURAN-ISOLASI-SUMBER.md`** — folder `references/` (terutama `permenpan-42-2011-kode.json`) ditambahkan ke whitelist kategori "Kriteria/regulasi". Boleh dipakai untuk kodefikasi, tetap dilarang untuk fakta Kondisi/Sebab/Akibat.

### Update Skill (18 file)

Semua 18 SKILL.md di `skills/*/` tambah section "Kodefikasi PermenPAN 42/2011 (v4.4)" yang merujuk ke Task 03 Step 6E. Catatan khusus: konsultasi-pengadaan tidak kodefikasi (bukan temuan formal), pemantauan-tindak-lanjut mengacu kode LHP awal.

### Update Script

- **`scripts/integral_inject.py`** — `_map_temuan()` sekarang kirim `kodefikasi_temuan`, `kodefikasi_rekomendasi`, `kodefikasi_sebab` ke endpoint SIMWAS (sebelumnya selalu null). Field di-baca dari temuan.json yang sudah diisi Claude di Step 6E.

### Konsekuensi

- KKP yang masuk via auto-inject ke SIMWAS sekarang punya kodefikasi resmi PermenPAN — siap konsumsi untuk Ikhtisar LHP APIP.
- Auditor tidak perlu lagi membuka PDF PermenPAN dan mencari kode manual.
- Reasoning kode tersimpan di temuan.json untuk audit trail dan keperluan review oleh ketua tim.

---

## v4.3 — Anti-Kontaminasi Lintas-Sesi (11 Mei 2026)

**Tanggal rilis:** 11 Mei 2026
**Tipe:** patch keamanan kritis — backward-compatible (manifest auto-generate kalau belum ada di Task 01)
**Tujuan:** Mencegah Claude membawa data/fakta dari penugasan lain, sesi sebelumnya, wiki, atau pattern library ke dalam temuan KKP/LHP. Akar masalah ditemukan saat uji coba RKA-KL: Claude tidak punya aturan eksplisit yang melarang ambil fakta dari sumber selain `00-input/` folder sesi aktif.

### 5 Lapis Defense

1. **Aturan Eksplisit di Skill (Lapis 1)** — file baru `skills/ATURAN-ISOLASI-SUMBER.md` jadi referensi global. Section "Aturan Isolasi Sumber" ditambahkan ke seluruh **18 SKILL.md** (audit-pengadaan, audit-kinerja, reviu-pengadaan, reviu-rka-kl, evaluasi-sakip/-spip/-rb/-mr, pemantauan-pengadaan/-tindak-lanjut, konsultasi-pengadaan, kepatuhan-saipi, 5 skill umum, graduasi-skill-spesifik).

2. **4 Cek Wajib Per Temuan (Lapis 2)** — Task 03 sekarang memaksa Claude lakukan 4 cek sebelum tulis tiap kalimat Kondisi/Sebab/Akibat: (a) cek sumber fakta, (b) cek atribusi dokumen, (c) cek isolasi sesi, (d) cek bukan asumsi. Kalau ragu → HAPUS atau flag sebagai "kesimpulan analitik".

3. **Session Manifest (Lapis 3)** — file baru `_SESSION-MANIFEST.json` di-generate di awal Task 01 oleh script baru `scripts/generate_session_manifest.py`. Manifest mencatat semua file `00-input/` + hash SHA-256. Jadi whitelist sumber fakta untuk seluruh sesi.

4. **Wiki Whitelist (Lapis 4)** — wiki (`wiki/`) dan pattern library (`pattern-library/`) **boleh** dipakai untuk: (a) pattern temuan historis sebagai referensi metodologi, (b) lookup nomor regulasi/Perpres/PMK sebagai Kriteria. **Dilarang** untuk fakta/data/angka/nama di Kondisi.

5. **Pre-Flight Isolation Check (Lapis 5)** — script baru `scripts/check_isolation.py` dipanggil di akhir Task 03 (sebelum auto-inject) dan di awal Task 04 (sebelum konsumsi temuan). Verifikasi: (a) manifest ada dan hash file masih match, (b) setiap temuan punya `dokumen_sumber.file` non-kosong, (c) file yang dirujuk ADA di whitelist manifest. Exit code 3 = kontaminasi → block auto-inject ke INTEGRAL.

### Tambahan File

- **`skills/ATURAN-ISOLASI-SUMBER.md`** — referensi global, 7 section: prinsip inti, sumber yang boleh, 4 cek wajib, penanganan multi-dokumen, penanganan kriteria, pre/post-flight, konsekuensi pelanggaran.
- **`scripts/generate_session_manifest.py`** (~95 baris) — SHA-256 hash semua file di `00-input/`, tulis `_SESSION-MANIFEST.json` dengan whitelist_rules eksplisit.
- **`scripts/check_isolation.py`** (~130 baris) — 2 cek (hash + temuan sources), exit code 0/1/2/3.

### Update Task

- **`tasks/01-start-audit.md`** — Pre-Check step 4 BARU: generate_session_manifest.py. Section baru "Aturan Isolasi Sumber" referencing ATURAN-ISOLASI-SUMBER.md.
- **`tasks/03-generate-kkp.md`** — Pre-Check step 3 BARU: cek `_SESSION-MANIFEST.json` ada. Section baru "ATURAN ISOLASI SUMBER" dengan 4 cek wajib + wiki whitelist. Section baru "Pre-Flight Isolation Check" sebelum auto-inject.
- **`tasks/04-generate-lhp.md`** — Pre-Check step 4 BARU: panggil check_isolation.py. Catatan isolasi v4.3 di prasyarat.

### Update Skill (18 file)

Semua SKILL.md di `skills/*/` tambah section "Aturan Isolasi Sumber (v4.3)" yang refer ke `ATURAN-ISOLASI-SUMBER.md`.

### Konsekuensi

- Setiap penugasan baru WAJIB mulai dengan Task 01 lengkap (termasuk generate manifest)
- Penugasan lama tanpa `_SESSION-MANIFEST.json` perlu generate manual via `python3 scripts/generate_session_manifest.py --penugasan ...` sebelum bisa lanjut Task 03/04
- Auto-inject ke INTEGRAL BLOK kalau ada kontaminasi temuan (sumber bukan dari 00-input/)
- Akuntabilitas auditor terjamin: setiap temuan traceable ke file spesifik di sesi yang sama

---

## v4.2 — Auto-Inject KKP ke INTEGRAL (10 Mei 2026)

**Tanggal rilis:** 10 Mei 2026
**Tipe:** patch — feature addition, backward-compatible
**Tujuan:** Hilangkan langkah manual auditor copy-paste temuan KKP ke modul Temuan INTEGRAL. Setelah anggota tim klik SETUJU di Task 03, sistem otomatis POST `_KKP/temuan.json` ke endpoint REST API SIMWAS v2 (INTEGRAL).

### Tambahan Script

- **`scripts/integral_inject.py`** (~285 baris) — HTTP client untuk POST ke endpoint `/kertas-kerja` SIMWAS v2. Membaca `_KKP/temuan.json`, filter temuan milik anggota saat ini yang berstatus DISETUJUI, map ke schema SIMWAS, POST dengan token bearer + 3 headers wajib (Authorization, X-Source, X-Cowork-User-Email). Update `temuan.json` field `integral` dengan ID dan nomor KKP dari response. Log event `INTEGRAL_EXPORT` ke audit trail.

### Skema Payload SIMWAS v2 (sesuai konfirmasi tim SIMWAS 29 April 2026)

- Identifikasi auditor pakai DUA field terpisah: `disusun_oleh` (nama) + `nip` (18 digit), bukan satu field gabungan
- Field opsional `id_sasaran` (integer) per temuan
- Field `uraian_rekomendasi` boleh `null` (rekomendasi di v4 ada di LHP, bukan KKP)
- Response struktur: `{success, message, kertas_kerja{id, nomor, internal_id, id_penugasan, status}, temuan_count}`
- Status awal `ai_draft` (string), response return `status: 0` (integer enum)

### Skip-List (Tetap Manual Upload)

Auto-inject tidak aktif untuk 4 jenis pengawasan dengan output format khusus:

- `konsultasi-pengadaan` — struktur kolom beda total (Pertanyaan/Analisis/Dasar Hukum/Rekomendasi)
- `evaluasi-spip` — output LKE Excel, bukan tabel KKP
- `evaluasi-reformasi-birokrasi` — output LKE per triwulan
- `pemantauan-tindak-lanjut` — output TLHP skeleton

Untuk 4 jenis ini, script otomatis print pesan agar auditor upload manual.

### Update Schema

- **`schemas/kkp-temuan.schema.json`** — field `integral` tambah property `nomor_kkp` (string formatted, mis. `KKP-1/82/IJ.3/PW.02.06/04/2026`). Field `id_integral` sekarang berisi numeric ID dari response.

### Update Task

- **`tasks/00-identifikasi-role.md`** — Pertanyaan 3 BARU: tanya NIP 18 digit. Field `nip:` ditambahkan ke frontmatter `_ROLE.md`. NIP wajib untuk auth ke INTEGRAL.
- **`tasks/03-generate-kkp.md`** — Section BARU "Auto-Inject ke INTEGRAL" setelah HITL SETUJU. Penjelasan skip-list, error handling 403/404/422, pesan ke auditor, mapping field.

### Status Workflow

KKP yang masuk via auto-inject tidak langsung final. Alur:
- POST sukses → status `ai_draft` (status code 0)
- Auditor login INTEGRAL → review → klik **Approve** → status berubah
- Pimpinan baru bisa lihat di dashboard setelah auditor approve
- Rejected: klik **Tolak & Laporkan** untuk eskalasi ke admin

### Environment Variables (Cowork Org-Level)

- `INTEGRAL_API_BASE_URL` — contoh: `https://simwasv2.komdigi.go.id/api/v1`
- `INTEGRAL_SERVICE_TOKEN` — Bearer token dari tim SIMWAS/INTEGRAL
- `COWORK_USER_EMAIL` — otomatis dari Cowork
- `COWORK_USER_NIP` — opsional, fallback kalau `_ROLE.md` tidak punya field `nip:`

### Error Handling

| Exit code | Arti |
|---|---|
| 0 | Sukses inject (HTTP 200/201) atau skip jenis manual-only |
| 1 | Error konfigurasi (env var tidak lengkap, _ROLE.md tidak ada) |
| 2 | Error validasi (temuan.json invalid, NIP tidak ditemukan/format salah) |
| 3 | Error HTTP dari SIMWAS (403/404/422/5xx) |

### Pending Klarifikasi dari Tim SIMWAS

Lihat `Pertanyaan-Tim-SIMWAS.docx` (di folder Audit AI IR2_V6). 10 pertanyaan klasifikasi KRITIS/PENTING/NICE — terutama: enum status, response GET schema, format error, url_view link, mapping id_sasaran.

---

## v4.0.4 — Optimisasi Durasi Eksekusi (3 Mei 2026)

**Tanggal rilis:** 3 Mei 2026
**Tipe:** patch — backward-compatible, tidak ada breaking change
**Tujuan:** Memangkas durasi eksekusi end-to-end tanpa menurunkan kualitas output.

**Patch berdasarkan diagnosa sesi uji coba pertama** (penugasan ST-156, ~30+ menit interaktif). Perubahan ini menargetkan ~50% pengurangan waktu untuk skill `reviu-pengadaan` dengan output substansi setara.

### Tambahan Script

- **`scripts/render_kkp.py`** — renderer KKP DOCX dari `_KKP/temuan.json` + `context.md`. Filter per anggota, kolom otomatis sesuai jenis (audit pakai Sebab; reviu/evaluasi tanpa Sebab; pemantauan tanpa Akibat). Mengganti scripted python-docx custom di tiap Task 03.
- **`scripts/render_lhp.py`** — renderer LHP DOCX placeholder-driven dari template skeleton + temuan.json + context.md + rekomendasi.json. Find-replace `{{...}}` + expand-loop untuk `{{HASIL_REVIU_LOOP}}`, `{{DASAR_HUKUM_LIST}}`, `{{SASARAN_LIST}}`, `{{TEMBUSAN_LIST}}`. Mengganti scripted python-docx custom di tiap Task 04.
- **`scripts/init_qa_artifacts.py`** — auto-generate placeholder `_QA-SAIPI/deklarasi-independensi.md`, `jawaban-needs-review.md`, `justifikasi.md` dari `context.md`. Dipanggil di Task 01 untuk mencegah iterasi 4 NEEDS_REVIEW SAIPI di Task 03.

### Tambahan Sub-command Script Lama

- **`audit_trail.py log-batch`** — terima JSON array of events (atau file/stdin), tulis dalam 1 subprocess call. Hemat ~3-5 detik per task dibanding chain `log-event` x N.
- **`qc_saipi.py --preflight-context`** — mode lightweight cek hanya rules `REN-001..REN-007` (KP/PKP ada di 00-input/, Tujuan terisi, Ruang Lingkup terisi, ≥1 sasaran). Tidak menulis checklist.json, tidak log audit-trail. Exit 2 kalau ada KRITIS. Dipanggil di akhir Task 01 sebelum gate, mencegah KRITIS context.md baru ketahuan saat Task 03 (mahal di-iterasi karena temuan sudah disusun).

### Tambahan Template

- **`templates/_skeleton-lhp/template-lhp-[jenis].docx`** — 10 template skeleton placeholder-driven untuk semua 10 jenis pengawasan (reviu-pengadaan, audit-pengadaan, audit-kinerja, reviu-rka-kl, evaluasi-sakip/-spip/-rb/-mr, pemantauan-pengadaan, pemantauan-tindak-lanjut). Struktur: Nota Dinas placeholder + halaman judul + Bab A–I substansi standar. Placeholder kunci: `{{NOMOR_ST}}`, `{{TANGGAL_ST}}`, `{{OBYEK}}`, `{{PENERIMA_LHP}}`, `{{HASIL_REVIU_LOOP}}`, `{{SIMPULAN_REVIU}}`, dll. Kompatibel dengan `render_lhp.py`.

### Update Dokumentasi

- **`tasks/01-start-audit.md`** — tambah Langkah 7b (`init_qa_artifacts.py`), 7c (`qc_saipi --preflight-context`), dan format `log-batch` untuk audit trail.
- **`tasks/03-generate-kkp.md`** — Langkah 6 mengarahkan ke `render_kkp.py` daripada generate scripted python-docx.
- **`tasks/04-generate-lhp.md`** — Langkah 2 mengarahkan ke `render_lhp.py` placeholder-driven daripada duplikasi template + edit manual.
- **`skills/reviu-pengadaan/SKILL.md`** — direktif eksplisit: jangan re-read full PDF setelah pre-digest jalan; pakai field `parsed.*` di digest, kecuali untuk verifikasi halaman spesifik yang akan dikutip.

### Verifikasi Smoke Test

Penugasan ST-156-2026 (Reviu Pengadaan DC/DRC PSrE Induk 2026, 5 temuan, 3 sasaran) di-rerun dengan pipeline v4.0.4 — output substansi identik dengan run pertama:
- 5 temuan, semua judul/Kondisi/Kriteria/Akibat tertuang lengkap di LHP
- 5 rekomendasi tertuang per temuan
- KKP DOCX per anggota: 10 paragraphs, 1 tabel, kolom sesuai paradigma reviu (tanpa Sebab)
- LHP DOCX: 175 paragraphs, semua 13 placeholder kelas filled (zero `{{...}}` bocor)
- QC SAIPI stage=kkp: KRITIS=0 di run pertama (sebelumnya butuh 2 iterasi)
- QC SAIPI stage=lhp: KRITIS=0 di run pertama (sebelumnya butuh 1 iterasi)
- Audit trail: 31 events (vs 37 sebelumnya — lebih ringkas tanpa kehilangan jejak action critical)

### Backward Compatibility

- `log-event` (single) tetap berfungsi — `log-batch` adalah tambahan.
- `qc_saipi --stage kkp|lhp` (lama) tetap berfungsi tanpa perubahan — `--preflight-context` adalah mode tambahan.
- Template lama `templates/Laporan Hasil Reviu Pengadaan.docx` tetap ada — skeleton baru di `templates/_skeleton-lhp/` adalah additive.
- Penugasan v4.0.0..v4.0.3 yang sedang berjalan tidak perlu migrasi — script lama tetap kompatibel.
- `prepare_lhp.py` mendapat banner DEPRECATED tapi masih berfungsi — script disimpan untuk penugasan in-flight.

### Perluasan ke Semua Skill (3 Mei 2026, sore)

Sesudah smoke test sukses untuk `reviu-pengadaan`, optimisasi diperluas ke seluruh keluarga skill:

**SKILL.md di-update** — seksi *Hemat Token & Eksekusi (v4.0.4)* ditambahkan ke 8 skill yang relevan: `audit-pengadaan`, `audit-kinerja`, `evaluasi-manajemen-risiko`, `evaluasi-reformasi-birokrasi`, `evaluasi-sakip`, `evaluasi-spip`, `konsultasi-pengadaan`, `pemantauan-pengadaan`, `pemantauan-tindak-lanjut`. Untuk skill yang punya pre-digest pipeline (`audit-pengadaan`, `reviu-pengadaan`, `reviu-rka-kl`), direktif spesifik: "jangan re-read PDF setelah digest". Untuk skill berbasis LKE/dokumen lain, direktif general: pakai renderer + log-batch + preflight + init_qa_artifacts.

**Tasks bertahap di-update** — `tasks/evaluasi-rb-bertahap.md`, `tasks/evaluasi-sakip-bertahap.md`, `tasks/evaluasi-spip-bertahap.md` mendapat seksi "Tooling v4.0.4 (hemat eksekusi)" yang mengarahkan: `audit_trail.py log-batch` per gate; `render_lhp.py` untuk LHE final dengan template skeleton per jenis; `qc_saipi.py --preflight-context` setelah Gate 0/1; `init_qa_artifacts.py` di Gate 0/1.

**Helper baru `scripts/bootstrap_penugasan.py`** — one-shot initializer: buat 6 standar dir (`_PKP/`, `_KKP/`, `_LHP/`, `_AUDIT-TRAIL/`, `_QA-SAIPI/`, `00-input/`), tulis `_ROLE.md` dari `--nama` + `--role-kode` (default AT), log `ROLE_LOGIN`. Mode `--clean` bersihkan output, mode `--post-task01` jalankan `init_qa_artifacts.py` + `qc_saipi.py --preflight-context` setelah Task 01 selesai. Hemat 5-6 langkah manual jadi 1 call.

**Renderer kompatibilitas** — `render_kkp.py` ter-verify untuk 6 jenis pengawasan (audit-pengadaan, audit-kinerja, reviu-pengadaan, reviu-rka-kl, evaluasi-sakip, pemantauan-pengadaan): kolom KKP otomatis sesuai paradigma (audit pakai Sebab; reviu/evaluasi tanpa Sebab; pemantauan tanpa Akibat). `render_lhp.py` ter-verify untuk 4 jenis (audit-pengadaan, reviu-rka-kl, evaluasi-sakip, pemantauan-pengadaan) dengan placeholder fully filled (`unfilled=NONE`).

**Skeleton template tambahan** — `templates/_skeleton-lhp/template-lhp-konsultasi-pengadaan.docx` ditambahkan untuk format Memo Konsultasi. Total 11 skeleton template tersedia.

**Cleanup** — `scripts/prepare_lhp.py` diberi banner DEPRECATED (gunakan `render_lhp.py`); script disimpan untuk kompatibilitas penugasan v4.0.0..v4.0.3.

---

---

## TL;DR

v4 mengubah **siapa** mengerjakan **apa** dan **bagaimana** hasilnya disimpan:

1. **Kartu Penugasan & Program Kerja Pengawasan dihapus dari otomasi** — dikerjakan manual di INTEGRAL. Anggota tim hanya unduh & taruh di `00-input/`.
2. **Role-based access** (AT vs KT/PT/PM) — `Task 00` baru, `role_check.py` memaksakan deny rule.
3. **Pembagian sasaran ke anggota** dari PKP → `_PKP/sasaran-assignment.json` → filter di Task 03.
4. **LHP completeness gate** — Ketua tim diblokir oleh `sasaran_completeness.py` selama ada sasaran belum SELESAI_KKP, dengan reminder otomatis.
5. **JSON KKP** (`_KKP/temuan.json`) menjadi sumber kebenaran untuk inject ke INTEGRAL. Word KKP jadi view sekunder per anggota.
6. **Audit trail JSON Lines** (`_AUDIT-TRAIL/events.jsonl`) — setiap aksi (login, gate, file generate, temuan added, reminder) ter-log.
7. **Wiki terintegrasi** — `wiki/` (eks `llm-wiki`) menjadi bagian dari sistem pengawasan, dapat diakses skill saat lookup regulasi.

---

## Perubahan File

### Baru

| File / Folder | Tujuan |
|---|---|
| `tasks/00-identifikasi-role.md` | Task baru — wajib pertama tiap sesi. Tanya nama + role, tulis `_ROLE.md`. |
| `scripts/role_check.py` | Validator role-based access. Dipanggil di awal Task 01/03/04. |
| `scripts/audit_trail.py` | Helper append-only event log JSON Lines. |
| `scripts/sasaran_completeness.py` | Cek apakah semua sasaran SELESAI_KKP sebelum LHP boleh dibuat; emit reminder ke ketua tim kalau belum. |
| `scripts/validate_kkp_json.py` | Validator JSON terhadap `schemas/`. |
| `schemas/kkp-temuan.schema.json` | JSON Schema untuk `_KKP/temuan.json`. Field: id_temuan, sasaran_id, anggota_tim, judul, kondisi, kriteria, sebab, akibat, dokumen_sumber. |
| `schemas/sasaran-assignment.schema.json` | JSON Schema untuk pembagian sasaran. |
| `schemas/examples/temuan-sample.json` | Contoh KKP valid. |
| `schemas/examples/sasaran-assignment-sample.json` | Contoh assignment 3 sasaran ke 2 anggota. |
| `wiki/` | Integrasi `llm-wiki` ke dalam audit-system-v4. |
| `CHANGELOG-v4.md` | File ini. |

### Dimodifikasi

| File | Perubahan |
|---|---|
| `tasks/01-start-audit.md` | Re-write: baca ST + KP + PKP yang sudah disediakan auditor (bukan generate). Output `context.md` + `_PKP/sasaran-assignment.json`. Pre-check role. |
| `tasks/03-generate-kkp.md` | Pre-check role + filter sasaran. Output dual: `temuan.json` (master) + `KKP-[nama].docx` (view). Status `sasaran-assignment.json` di-update. |
| `tasks/04-generate-lhp.md` | Pre-check role (KT/PT/PM only). `sasaran_completeness.py` blocker + auto-reminder. Konsumsi `temuan.json`, bukan Word KKP. |
| `README.md` | Header v4, alur baru, struktur folder baru, panduan starter v4. Bagian v3 dipertahankan untuk kompatibilitas. |

### Diarsipkan / dihapus dari alur

| File / Folder | Status |
|---|---|
| `tasks/02b-generate-kp-pkp.md` | → `tasks/_ARSIP-02b-generate-kp-pkp.md` (KP+PKP manual di INTEGRAL) |
| `templates/kp-pkp/` | → `templates/_ARSIP-kp-pkp/` (+ README arsip) |

---

## Role Matrix

| Role | Kode | Boleh menjalankan | Boleh akses skill |
|------|------|-------------------|-------------------|
| Anggota Tim | AT | Task 00, 01, 03 | Semua 10 skill audit + wiki + `qc_kkp_lhp.py --only kkp` |
| Ketua Tim | KT | Task 00, 04 | Skill yang dipakai untuk LHP + wiki + `qc_kkp_lhp.py --only lhp` |
| Pengendali Teknis | PT | Task 00, 04 (default = setara KT) | Sama seperti KT |
| Pengendali Mutu | PM | Task 00, 04 (default = setara KT) | Sama seperti KT |

Override manual dapat dilakukan dengan field `role_override` di `_ROLE.md`.

---

## Cara Pakai Tooling Baru

### Cek role sebelum menjalankan task
```bash
python3 scripts/role_check.py --penugasan penugasan/2026-05-001-xxx --task 03
# exit 0 = OK; exit 2 = DENIED + alasan di stderr
```

### Log event ke audit trail
```bash
python3 scripts/audit_trail.py log-event \
    --penugasan penugasan/2026-05-001-xxx \
    --action KKP_TEMUAN_ADDED --task 03 \
    --target _KKP/temuan.json \
    --payload '{"id_temuan": "T-001", "sasaran_id": "S-01"}'
```

### Lihat audit trail
```bash
python3 scripts/audit_trail.py show --penugasan penugasan/2026-05-001-xxx --last 10
```

### Cek completeness sebelum LHP
```bash
python3 scripts/sasaran_completeness.py \
    --penugasan penugasan/2026-05-001-xxx --emit-reminder
# exit 0 = lengkap; exit 2 = belum + reminder dicetak
```

### Validasi JSON KKP
```bash
python3 scripts/validate_kkp_json.py penugasan/2026-05-001-xxx/_KKP/temuan.json
python3 scripts/validate_kkp_json.py penugasan/2026-05-001-xxx/_PKP/sasaran-assignment.json
```

---

## Migrasi dari v3 ke v4

Penugasan v3 yang **sedang berjalan** boleh tetap di v3 (tidak perlu migrasi paksa). Penugasan baru pakai v4.

Jika perlu migrasi:
1. Salin folder penugasan dari `audit-system v3/penugasan/[nama]` → `audit-system-v4/penugasan/[nama]`.
2. Pindah dokumen pendukung dari `00-surat-tugas/` + `01..05/` ke `00-input/` flat.
3. Jalankan Task 00 (login) → Task 01 (re-extract sasaran-assignment.json dari PKP).
4. Jika KKP sudah ada di Word v3, konversi manual ke `_KKP/temuan.json` mengikuti schema, lalu validate.

---

## Yang TIDAK berubah

- 10 skill di `skills/` — masih sama (audit-pengadaan, reviu-pengadaan, dst.)
- Template LHP di `templates/[jenis]/template-lhp.docx` — tetap dipakai Task 04
- Pipeline pre-digest reviu-rka-kl, audit-pengadaan, reviu-pengadaan
- Pattern library
- Ringkasan mingguan & dashboard penugasan (akan diupgrade di rilis berikutnya untuk include kolom role progress)
- Prinsip anti-halusinasi: setiap kondisi wajib referensi dokumen sumber

---

## Patch v4.0.1 — QC Kepatuhan SAIPI (2 Mei 2026, sore)

Tambahan setelah rilis v4.0:

| File | Tujuan |
|---|---|
| `skills/kepatuhan-saipi/SKILL.md` | Skill QA kepatuhan SAIPI per-penugasan |
| `skills/kepatuhan-saipi/references/SAIPI-{1100,1200,2200,2300,2400}-*.md` | Kutipan verbatim standar |
| `skills/kepatuhan-saipi/references/checklist-saipi-per-penugasan.json` | 30 rule mapping → standar SAIPI |
| `scripts/qc_saipi.py` | Auto-check kepatuhan, `--stage kkp \| lhp` |
| `wiki/raw/SAIPI-PER-01-AAIPI-DPN-2021.pdf` | PDF SAIPI sumber otoritatif |
| `tasks/03-generate-kkp.md` | Tambah Langkah 6a.2 panggil qc_saipi --stage kkp |
| `tasks/04-generate-lhp.md` | Tambah section QC SAIPI sebelum gate ketua tim |
| `scripts/audit_trail.py` | KNOWN_ACTIONS tambah `SAIPI_CHECK` |

**Cakupan**: per-penugasan. Standar 1100, 1200, 2200, 2300, 2400. Standar organisasi-level (1000, 1300, 2000-an, 2100-an, 2500, 2600) di-out of scope.

**Pemicu**: otomatis di akhir Task 03 (stage=kkp) dan Task 04 (stage=lhp), sebelum gate auditor. Tujuan: koreksi gap sebelum submit INTEGRAL.

**Severity**:
- `KRITIS` → exit 2, blokir gate
- `PERINGATAN` → boleh override dengan justifikasi tertulis
- `NEEDS_REVIEW` → konfirmasi manual auditor (mis. independensi pribadi)

## Patch v4.0.2 — Auto-ingest ke Wiki (2 Mei 2026, malam)

Tambahan setelah Patch v4.0.1:

| File | Tujuan |
|---|---|
| `scripts/ingest_to_wiki.py` | Auto-ingest hasil penugasan ke wiki — dipanggil setelah `LHP_FINALIZED + INTEGRAL_EXPORT` |
| `wiki/wiki/_INDEX-V4.md` | Index utama wiki sistem v4 (hub navigasi halaman operasional) |
| `wiki/wiki/pattern-temuan.md` | Aggregator pattern temuan (auto + integrasi `pattern-library/` lama) |
| `wiki/wiki/audit-trail-overview.md` | Format audit trail + summary aggregat semua penugasan |
| `wiki/wiki/database-kp.md` | Database KP yang sudah terpakai (auto-extract dari `00-input/`) |
| `wiki/wiki/database-pkp.md` | Database PKP + pola pembagian sasaran |
| `wiki/wiki/tlhp-index.md` | Index rekomendasi LHP final (auto-extract) |
| `wiki/wiki/references-index.md` | Aggregat kriteria yang dirujuk di temuan |
| `tasks/04-generate-lhp.md` | Section auto-ingest setelah `INTEGRAL_EXPORT` |
| `scripts/audit_trail.py` | KNOWN_ACTIONS tambah `INGEST_TO_WIKI` |
| `wiki/wiki/_BACKUP-PRE-SYNC-2026-05-02/` | Backup wiki lama (176 file) sebelum sync mnt/wiki overwrite |

**Sync wiki**: 188 file dari folder mnt/wiki/ (sumber kebenaran user) di-sync ke v4/wiki/wiki/. 12 file beda di-overwrite, file baru disalin.

**Pemicu ingest**: otomatis di akhir Task 04 setelah ketua tim catat `INTEGRAL_EXPORT`. Output tertulis ke 7 halaman wiki + 1 entry log + 1 event audit trail.

**Idempotent**: setiap ingest re-aggregate halaman aggregator dari awal — aman di-jalankan berulang.

**Mode tambahan**:
- `--force` bypass gate
- `--re-aggregate-only` rebuild halaman aggregator tanpa ingest penugasan baru

## Patch v4.0.3 — Dashboard HTML sinkron sistem + wiki (2 Mei 2026, malam)

| File | Tujuan |
|---|---|
| `scripts/build_dashboard.py` | Generate dashboard.html dengan 4 panel: ISU/Risiko, TLHP, Audit Trail, Hasil Pengawasan KKP+LHP |
| `audit-system-v4/dashboard.html` | Output sistem (replace `dashboard.md` v3 yang tinggal placeholder) |
| `wiki/wiki/dashboard.html` | Output wiki (replace dashboard.html lama, backup di `_BACKUP-PRE-SYNC-2026-05-02/dashboard-old.html`) |
| `scripts/ingest_to_wiki.py` | Tambah panggilan auto-rebuild dashboard di langkah 10 finalisasi |

**Sumber data:**
- ISU/Risiko: parse `wiki/wiki/pemantauan-isu-risiko-trello.md` (tabel cards di section "Kelompok Wasdig/Ekosdig/Kementerian") + opsional override `penugasan/_RISK-REGISTER/issues.json`
- TLHP: parse `wiki/wiki/tlhp-index.md` (auto-aggregated v4.0.2)
- Audit Trail: aggregat dari `penugasan/*/_AUDIT-TRAIL/events.jsonl`
- Hasil Pengawasan: dari `penugasan/*/_KKP/temuan.json` (sumber kebenaran inject INTEGRAL)

**Sinkron**: kedua file dashboard.html identik (md5 sama). Setiap rebuild dipanggil otomatis setelah `ingest_to_wiki.py` selesai (yang sendiri dipicu oleh `LHP_FINALIZED + INTEGRAL_EXPORT`).

**Manual trigger**:
```bash
python3 scripts/build_dashboard.py
```

### Patch v4.0.3a — Detail KKSA di tab Hasil Pengawasan

Tab "Hasil Pengawasan" sekarang menampilkan **detail KKSA lengkap** per temuan (collapsible), tidak hanya judul:
- Kondisi (fakta yang ditemukan)
- Kriteria (regulasi yang dilanggar/dipenuhi)
- Sebab (kalau audit-pengadaan/audit-kinerja)
- Akibat (konsekuensi/risiko)
- Dokumen sumber (file + halaman)

Plus header tiap card: id_temuan · sasaran_id · anggota tim · status badge.

## Backlog v4.x

- v4.1: dashboard.md di-upgrade tampilkan kolom role + completeness per sasaran.
- v4.2: integrator INTEGRAL — script CLI yang men-POST `temuan.json` ke endpoint INTEGRAL (saat API tersedia).
- v4.3: portal sederhana (artifact HTML) untuk lihat audit trail per penugasan secara visual.
