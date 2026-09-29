# ⛔ PROTOKOL WAJIB — BACA INI SEBELUM APAPUN

> **Claude: sebelum mengerjakan penugasan apapun, wajib selesaikan dua gate ini terlebih dahulu. Tidak ada pengecualian.**
>
> **GATE 0 — Identifikasi Role:** Tanya nama, role, dan NIP user via `AskUserQuestion`. Tulis `_ROLE.md`. Log ke `_AUDIT-TRAIL/events.jsonl`. → Panduan lengkap: `tasks/00-identifikasi-role.md`
>
> **GATE 1 — Inisiasi:** Cek `00-input/` (ST + KP + PKP), tentukan skill, tulis `context.md` + `sasaran-assignment.json`, buat semua folder standar (`_PKP`, `_KKP`, `_LHP`, `_AUDIT-TRAIL`, `_BUKTI-AI`, `_SUBMIT`). → Panduan lengkap: `tasks/01-start-audit.md`
>
> Lihat juga: `/CLAUDE.md` di root workspace untuk checklist lengkap.

---

# Sistem AI Audit Intern Otomatis — v4
### Powered by Claude Sonnet 4.6 + Haiku 4.5 + Cowork + Skill Architecture

**Versi:** 4.0 — Mei 2026 (Role-based access, KP+PKP manual di INTEGRAL, JSON KKP, Audit Trail, Wiki terintegrasi)
**Platform:** Claude Desktop (Cowork) + File System Lokal + INTEGRAL
**Instansi:** Inspektorat II — Inspektorat Jenderal Kementerian Komunikasi dan Digital RI

> 📋 **Lihat juga:** [STATUS.md](STATUS.md) — project status & roadmap | [AUDIT-REPORT.md](AUDIT-REPORT.md) — laporan audit sistem 6 Mei 2026

---

## 🆕 Update Terbaru — Mei 2026

### v4.4 — Kodefikasi PermenPAN 42/2011 (1 Juni 2026)

**Auto-generate kode atribut temuan dan rekomendasi** sesuai PermenPAN dan RB No. 42 Tahun 2011 (Lampiran 2.1 dan 2.2). Hilangkan langkah manual auditor mencari kode di PDF saat menyusun KKP.

- File baru: `references/permenpan-42-2011-kode.json` — 89 kode temuan + 14 kode rekomendasi (di-generate dari PDF resmi PermenPAN)
- Task 03 step 6E BARU: Claude baca reference, pilih kode berdasarkan semantik isi Kondisi, tulis reasoning, validasi alt-rekomendasi, konfirmasi via HITL
- 4 field baru di schema temuan: `kodefikasi_temuan`, `kodefikasi_temuan_reasoning`, `kodefikasi_rekomendasi`, `kodefikasi_sebab` (sebab pending klarifikasi)
- `integral_inject.py` sekarang kirim kodefikasi ke SIMWAS
- 18 SKILL.md di-update dengan note kodefikasi

### v4.3 — Anti-Kontaminasi Lintas-Sesi (11 Mei 2026)

**Patch keamanan kritis** untuk mencegah Claude membawa data/fakta dari penugasan lain, sesi sebelumnya, atau memori percakapan ke dalam temuan KKP/LHP. 5 lapis defense:

1. **Aturan eksplisit di skill** — file baru `skills/ATURAN-ISOLASI-SUMBER.md` di-referensikan oleh semua 18 SKILL.md
2. **4 cek wajib per temuan** — Task 03 sekarang memaksa Claude verifikasi sumber, atribusi, isolasi sesi, bukan asumsi sebelum tulis tiap kalimat
3. **Session Manifest** — file baru `_SESSION-MANIFEST.json` di-generate di Task 01 dengan SHA-256 hash semua file `00-input/`. Lock-in whitelist sumber fakta
4. **Wiki whitelist** — wiki & pattern-library DIBOLEHKAN untuk pattern temuan + kriteria regulasi, DILARANG untuk fakta/data spesifik
5. **Pre-flight check** — script baru `scripts/check_isolation.py` verifikasi setiap temuan punya `dokumen_sumber.file` yang ADA di manifest. Block auto-inject INTEGRAL kalau ada kontaminasi

Tambahan:
- File baru: `scripts/generate_session_manifest.py`, `scripts/check_isolation.py`, `skills/ATURAN-ISOLASI-SUMBER.md`
- Task 01 step 4 BARU: generate manifest
- Task 03 pre-check ke-3 BARU: cek manifest, 4 cek wajib per temuan, pre-flight isolation
- Task 04 pre-check ke-4 BARU: cek isolasi sebelum konsumsi temuan.json
- Semua 18 SKILL.md tambah section "Aturan Isolasi Sumber"

### v4.2 — Auto-Inject KKP ke INTEGRAL (10 Mei 2026)

**Hilangkan langkah manual copy-paste** auditor ke modul Temuan INTEGRAL. Setelah anggota tim klik SETUJU di Task 03, sistem otomatis POST `_KKP/temuan.json` ke endpoint INTEGRAL `/kertas-kerja` via `scripts/integral_inject.py`.

- File baru: `scripts/integral_inject.py` (~285 baris, pakai REST API SIMWAS v2)
- Task 00 sekarang minta **NIP 18 digit** (disimpan di `_ROLE.md` field `nip:`) — wajib untuk auth ke INTEGRAL
- Task 03 trigger auto-inject otomatis di akhir setelah HITL SETUJU
- Schema `kkp-temuan.schema.json` field `integral` tambah `nomor_kkp` (response.kertas_kerja.nomor)
- Status temuan setelah inject sukses: `DIINJECT_INTEGRAL`
- Audit trail catat event `INTEGRAL_EXPORT`
- **Skip-list** (tetap manual upload): konsultasi-pengadaan, evaluasi-spip, evaluasi-reformasi-birokrasi, pemantauan-tindak-lanjut (output format khusus, bukan tabel KKP)
- Env var wajib (org-level Cowork): `INTEGRAL_API_BASE_URL`, `INTEGRAL_SERVICE_TOKEN`, `COWORK_USER_EMAIL`
- Workflow approval: KKP masuk status `ai_draft` → auditor login INTEGRAL klik Approve → status berubah → muncul di dashboard pimpinan

### v4.1 — Pipeline Reviu RKA-K/L Production-Grade (6 Mei 2026)

**reviu-rka-kl v3.0** — pipeline 39 rules deterministik (21 + 18 alt-rules), auto-execute via SKILL.md, parallel 4 workers, render LHR multi-RO.

- 12 RO end-to-end: **14,1 detik** (107x lebih cepat dari workflow manual)
- 66 anomali ter-deteksi otomatis (vs 24 pre-v3 = 2,75x)
- 1 perintah saja: `python3 audit-system-v4/scripts/reviu-rka-kl/run_batch.py --penugasan <FOLDER>`

### 5 Skill Umum Criteria-Driven

`audit-umum`, `reviu-umum`, `pemantauan-umum`, `evaluasi-umum`, `konsultansi-umum` — untuk objek pengawasan tanpa skill spesifik. Auditor unggah kriteria di `input/kriteria/` (bebas-format), skill auto-extract & klasifikasi.

### Meta-skill Graduasi

`graduasi-skill-spesifik` — auto-generate skill spesifik baru dari pola penugasan dengan skill umum. Manual trigger, mode batch Jumat sore. Output draft di `skills/_draft/<nama>/`.

### 3 Template Reviu RKA-K/L Siap Pakai

PKP-Reviu-RKA-KL-template.xlsx, KKR-Reviu-RKA-KL-template.xlsx, LHR-Reviu-RKA-KL-skeleton.docx — di `templates/`.

### AST Preflight Protection

`_self_check_ast()` di 8 script untuk proteksi dari OneDrive sync corruption.

> **Perubahan utama v4** (Mei 2026 — major release, source-cloned dari v3 27 Apr 2026):
>
> 1. **KP + PKP dihapus dari alur otomasi**. Kartu Penugasan dan Program Kerja Pengawasan dikerjakan **manual oleh auditor di sistem INTEGRAL**. Anggota tim mengunduh ST + KP + PKP final dari INTEGRAL dan menaruhnya di `00-input/`. Task 02b (Generate KP+PKP) diarsipkan.
> 2. **Role-based access**. Setiap sesi dimulai dengan **Task 00 — Identifikasi Role**: Claude tanya nama lengkap & peran (Anggota Tim / Ketua Tim / Pengendali Teknis / Pengendali Mutu). Anggota Tim hanya boleh menjalankan Task 01 & 03 (KKP). Ketua Tim hanya boleh menjalankan Task 04 (LHP). Aturan dipaksakan oleh `scripts/role_check.py`.
> 3. **Pembagian sasaran ke anggota**. Task 01 mengekstrak `_PKP/sasaran-assignment.json` dari PKP. Saat Task 03, anggota tim **hanya boleh** mengisi KKP untuk sasaran yang `assigned_to`-nya mencantumkan namanya.
> 4. **LHP completeness gate**. Task 04 menjalankan `scripts/sasaran_completeness.py` lebih dulu. Jika ada sasaran belum SELESAI_KKP, LHP **diblokir** dan ketua tim mendapat reminder berisi nama anggota & sasaran yang belum dikerjakan.
> 5. **JSON KKP untuk INTEGRAL**. KKP sekarang punya **dua format**: `_KKP/temuan.json` (sumber kebenaran, valid terhadap `schemas/kkp-temuan.schema.json`, dipakai untuk inject ke INTEGRAL) + `_KKP/KKP-[nama-anggota].docx` (view auditor).
> 6. **Audit trail JSON Lines**. Setiap aksi (login, gate, file generate, temuan added, reminder) ditulis sebagai 1 baris JSON di `_AUDIT-TRAIL/events.jsonl`. Append-only, mudah di-query.
> 7. **Wiki terintegrasi**. Folder `wiki/` (eks `llm-wiki`) sekarang bagian dari sistem pengawasan. Skill bisa lookup regulasi/best-practice dari sini.
> 8. **(Patch v4.0.1) QC kepatuhan SAIPI** otomatis. Skill `kepatuhan-saipi/` + script `qc_saipi.py` dipanggil otomatis di akhir Task 03 (stage=kkp) dan Task 04 (stage=lhp). Cek standar SAIPI 1100, 1200, 2200, 2300, 2400. Output `_QA-SAIPI/checklist-{stage}.json` + `laporan-qa-{stage}.md`. Gap KRITIS memblokir gate auditor sebelum submit ke INTEGRAL.
> 9. **(Patch v4.0.2) Auto-ingest ke wiki** setelah `LHP_FINALIZED + INTEGRAL_EXPORT`. Setiap penugasan v4 yang selesai disubmit ke INTEGRAL → otomatis ingest ke `wiki/wiki/`: halaman per-penugasan (`lhp-{slug}.md`), aggregator pattern temuan, database KP & PKP, index TLHP, references-index, audit-trail-overview. Wiki growing sebagai memori organisasi.

---

## Sejarah versi sebelumnya (referensi historis)

> **Perubahan utama v2.7** (16 April 2026):
>
> - **Task 05 (Administrasi) dihapus**. Pembuatan Nota Dinas, pengisian nomor surat (SIMWAS), tanggal, destinatari, tembusan, dan TTD **dikerjakan auditor secara manual** di Word setelah Task 04 selesai. Task 04 tetap menulis placeholder `[DIISI AUDITOR]` untuk semua field administratif. Alasan: nomor surat selalu dari SIMWAS, TTD wajib manusia, dan Nota Dinas adalah template singkat yang lebih cepat ditulis sendiri. Hemat token + waktu eksekusi. File lama disimpan sebagai `_ARSIP-05-generate-administrasi.md`.
> - **KP + PKP 6 jenis terstandar** (reviu-rka-kl, pemantauan-pengadaan, evaluasi-sakip, evaluasi-spip, evaluasi-reformasi-birokrasi, evaluasi-manajemen-risiko): Task 02b kini bercabang Jalur A (bespoke untuk audit-kinerja/audit-pengadaan/reviu-pengadaan/konsultasi-pengadaan) dan Jalur B (find-replace template di `templates/kp-pkp/[jenis]/`). Konvensi placeholder di `templates/kp-pkp/TEMPLATE-INDEX-KP-PKP.md`.
>
> **Perubahan v2.5** (16 April 2026):
>
> - **Task 02 (Validasi Dokumen) dihapus** untuk hemat token. File listing + ringkasan isi dokumen dilakukan inline di Task 03 Langkah 1 & 2. File `tasks/_ARSIP-02-analisis-dokumen.md` tetap ada sebagai referensi historis.
> - **Kasus folder kosong total**: Task 03 berhenti dan minta auditor upload dokumen (tidak membuat KKP dengan analisis halu).
> - **Audit Kinerja Survey Pendahuluan — Research Online**: WebSearch + WebFetch untuk 4 jenis research (benchmark K/L, best practice internasional OECD/WB/INTOSAI, regulasi pembina terbaru, hasil audit BPK/BPKP + riset akademis). Sitasi URL + tanggal akses wajib. Research hanya konteks pembanding — bukan kriteria utama temuan.
>
> **Perubahan v2.3** (8 April 2026 — dari uji coba Reviu Pengadaan DC/DRC PSrE Induk 2026):
>
> **Efisiensi Token (~40–43% penghematan potensial):**
> - Scope reviu perencanaan tidak lagi memeriksa RUP/SiRUP dan SPPBJ — kedua aspek ini lebih relevan untuk scope pemilihan/pelaksanaan (~20% hemat)
> - File listing skip folder `04-pelaksanaan/` dan `05-keuangan/` untuk penugasan perencanaan
>
> **Scope Switch untuk reviu-pengadaan:** Skill kini mendukung dua scope eksplisit — **Perencanaan** (default: KAK, HPS, metode pemilihan) dan **Pemilihan** (opsional: SPPBJ, BAHP, dokumen pemilihan). Auditor memilih scope di awal.
>
> **Checklist Baru — Dua Isu yang Sebelumnya Terlewat:**
> - Konsistensi internal KAK: nilai SLA di Latar Belakang vs Persyaratan Teknis wajib diperiksa
> - Komponen biaya migrasi: jika KAK mencantumkan klausul migrasi/transisi, biaya wajib ada di HPS
>
> **Standar Format LHP (DOCX):** Font Arial, `jc=both` (justified), sz=24. Template wajib diduplikasi (bukan dibuat dari nol). Lihat Task 04 untuk fungsi Python siap pakai.
>
> **Perubahan v2.2:** Model tiering — Task administrasi (01, 02, 02b, 05) menggunakan Haiku; task analisis (03, 04) menggunakan Sonnet.
>
> **Perubahan v2.1:** Ditambahkan KP + PKP sebagai dokumen formal sebelum KKP.

---

## Alur Kerja v4 (Semua Jenis Pengawasan)

```
[INTEGRAL — manual oleh auditor]
    Auditor entry penugasan + bagi sasaran → unduh ST + KP + PKP
    Letakkan ke: penugasan/[nama]/00-input/
        │
        ▼
Task 00 ─── Identifikasi Role: tanya nama lengkap + peran + NIP    [HAIKU]
    │         Tulis _ROLE.md (incl. NIP 18 digit), log ROLE_LOGIN
    │         ⏸ (default flow: anggota tim login dulu)
    ▼
Task 01 ─── Inisiasi: baca ST + KP + PKP → context.md +            [HAIKU]
    │         _PKP/sasaran-assignment.json (pembagian sasaran)
    │         ⏸ Anggota konfirmasi LANJUT
    │         (Hanya boleh oleh: Anggota Tim)
    ▼
Task 03 ─── KKP: file listing + analisis + generate                 [SONNET]
    │         _KKP/temuan.json + _KKP/KKP-[nama].docx
    │         FILTER: hanya sasaran yang assigned ke user
    │         ⏸ Anggota review draft, koreksi sampai SETUJU
    │         (Hanya boleh oleh: Anggota Tim)
    │         🆕 v4.2: AUTO-INJECT ke INTEGRAL setelah SETUJU
    │             → POST /kertas-kerja (status: ai_draft)
    │             → Update temuan.status = DIINJECT_INTEGRAL
    │             → Log INTEGRAL_EXPORT ke audit trail
    │             → SKIP untuk: konsultasi-pengadaan, evaluasi-spip,
    │                evaluasi-RB, pemantauan-tindak-lanjut (manual)
    ▼
   [Anggota lain ulangi Task 00 → 03 untuk sasaran masing-masing]
    │         _KKP/temuan.json di-append (bersama)
    │         _PKP/sasaran-assignment.json status di-update
    ▼
Task 04 ─── LHP: completeness check → konsumsi temuan.json         [SONNET]
    │         → tulis LHP-SUBSTANSI.docx
    │         ⛔ DIBLOKIR jika ada sasaran belum SELESAI_KKP
    │             → Reminder otomatis ke ketua tim (siapa belum)
    │         ⏸ Ketua Tim review, iterasi sampai SETUJU
    │         (Hanya boleh oleh: Ketua Tim / PT / PM)
    │
    ═══ OTOMASI BERAKHIR ═══
    ▼
[Manual oleh auditor]
    1. Login INTEGRAL → review KKP draft (yang sudah auto-inject)
       → klik "Approve" agar status berubah → muncul di pimpinan
    2. Isi nomor surat (SIMWAS), tanggal, destinatari, tembusan,
       Nota Dinas pengantar, TTD di Word → kirim ke auditan ✅
```

> **Audit trail**: setiap event di alur di atas (gate passed, file generated, reminder sent, dll.) tercatat di `penugasan/[nama]/_AUDIT-TRAIL/events.jsonl`.

---

## Kolom KKP per Jenis Pengawasan

| Jenis | Kolom KKP | Paradigma |
|-------|-----------|-----------|
| Audit Pengadaan | No \| Judul \| Kondisi \| Kriteria \| **Sebab** \| Akibat | Keyakinan Memadai |
| Audit Kinerja | No \| Judul \| Kondisi \| Kriteria \| **Sebab** \| Akibat | Keyakinan Memadai |
| Reviu Pengadaan | No \| Judul \| Kondisi \| Kriteria \| Akibat | Keyakinan Terbatas |
| Reviu RKA/KL | No \| Judul \| Kondisi \| Kriteria \| Akibat | Keyakinan Terbatas |
| Pemantauan Pengadaan | No \| Judul \| Kondisi \| Kriteria | Pemantauan |
| Evaluasi SAKIP | No \| Judul \| Kondisi \| Kriteria \| Akibat | Keyakinan Terbatas |
| Evaluasi Manajemen Risiko | No \| Judul \| Kondisi \| Kriteria \| Akibat | Keyakinan Terbatas |
| Evaluasi SPIP | *Gunakan LKE Excel (bukan tabel KKP)* | Keyakinan Terbatas |
| Evaluasi RB | *Gunakan LKE per triwulan (bukan tabel KKP)* | Keyakinan Terbatas |
| Konsultasi Pengadaan | No \| Pertanyaan \| Analisis \| Dasar Hukum \| Rekomendasi | Konsultasi |

> **Rekomendasi tidak ada di KKP** — dirumuskan di LHP setelah feedback auditor.

---

## Skill yang Tersedia (19 aktif)

```
ASSURANCE — Keyakinan Memadai (Audit):
├─ audit-pengadaan/         → Seluruh siklus PBJ, termasuk pembayaran [v2.0]
└─ audit-kinerja/           → Efektivitas & efisiensi program [v2.2]

ASSURANCE — Keyakinan Terbatas (Reviu & Evaluasi):
├─ reviu-pengadaan/         → Perencanaan (default) atau Pemilihan (Scope Switch) [v1.2]
├─ reviu-rka-kl/            → ⚡ Auto-execute pipeline 39 rules — 1 cmd end-to-end [v3.0]
├─ pemantauan-pengadaan/    → Progres pelaksanaan kontrak aktif [v2.0]
├─ pemantauan-tindak-lanjut/→ TLHP (skeleton) [v0.1]
├─ evaluasi-sakip/          → Sistem AKIP (4 komponen, skor 0–100) [v5.0]
├─ evaluasi-spip/           → Maturitas SPIP (LKE Excel, Nilai PK) [v1.4]
├─ evaluasi-reformasi-birokrasi/ → RB on-going per triwulan [v2.0]
└─ evaluasi-manajemen-risiko/    → Evaluasi MR berdasarkan ISO 31000 [v2.0]

CONSULTING (tanpa keyakinan formal):
└─ konsultasi-pengadaan/    → Advisory, pendapat teknis, telaah isu PBJ [v2.0]

QUALITY ASSURANCE:
└─ kepatuhan-saipi/         → QC standar SAIPI 1100/1200/2200/2300/2400 [v1.0]

🆕 SKILL UMUM CRITERIA-DRIVEN (Mei 2026) — auditor unggah kriteria di input/kriteria/:
├─ audit-umum/              → Audit umum, gate-based, KKSA penuh [v1.0]
├─ reviu-umum/              → Reviu administratif, keyakinan terbatas [v1.0]
├─ pemantauan-umum/         → Status hijau/kuning/merah [v1.0]
├─ evaluasi-umum/           → Penilaian substantif, skor + predikat [v1.0]
└─ konsultansi-umum/        → Memo pendapat/saran tanpa keyakinan [v1.0]

🤖 META-SKILL:
└─ graduasi-skill-spesifik/ → Auto-generate skill spesifik dari penugasan umum [v1.0]
                              Mode batch (Jumat sore mingguan)

PANDUAN BERSAMA:
├─ panduan-format-umum/     → Format Nota Dinas, LHR, bahasa laporan
├─ shared-pbj-references/   → Perbandingan 4 skill PBJ (kapan pakai yang mana)
└─ shared-kinerja-references/ → Perbandingan skill kinerja
```

⚡ = Auto-execute pipeline (saat skill dipanggil, Claude otomatis jalankan `run_batch.py`)
🆕 = Skill baru Mei 2026
🤖 = Meta-skill (untuk pengembangan sistem, bukan pengawasan)

---

## Struktur Folder

```
audit-system-v4/
├─ README.md                              ← Dokumen ini — baca dulu!
├─ STATUS.md                              ← Project status & roadmap
├─ AUDIT-REPORT.md                        ← Laporan audit sistem (6 Mei 2026)
│
├─ skills/                               ← Panduan per jenis pengawasan (dibaca Claude)
│  ├─ panduan-format-umum/PANDUAN.md
│  ├─ shared-pbj-references/PANDUAN.md
│  ├─ shared-kinerja-references/PANDUAN.md
│  ├─ audit-pengadaan/SKILL.md + references/ (6 file)
│  ├─ audit-kinerja/SKILL.md + references/
│  ├─ reviu-pengadaan/SKILL.md + references/ (4 file)
│  ├─ reviu-rka-kl/SKILL.md + references/ (3 file)
│  ├─ pemantauan-pengadaan/SKILL.md + references/
│  ├─ evaluasi-sakip/SKILL.md + references/
│  ├─ evaluasi-spip/SKILL.md + references/ (2 file)
│  ├─ evaluasi-reformasi-birokrasi/SKILL.md + references/ (3 file)
│  ├─ evaluasi-manajemen-risiko/SKILL.md + references/
│  └─ konsultasi-pengadaan/SKILL.md + references/
│
├─ tasks/                                ← Alur kerja langkah-per-langkah (dibaca Claude)
│  ├─ 01-start-audit.md                  ← SELALU mulai dari sini — routing + context.md
│  ├─ 02b-generate-kp-pkp.md            ← Generate KP + PKP (+ Memo SP untuk audit-kinerja)
│  ├─ 03-generate-kkp.md                ← File listing + ringkasan + tabel temuan KKP (Word)
│  ├─ 04-generate-lhp.md                ← Substansi laporan (temuan/analisis/rekomendasi) — TAHAP AKHIR
│  ├─ _ARSIP-02-analisis-dokumen.md     ← (ARSIP) Validasi dokumen — dihapus dari alur v2.5
│  └─ _ARSIP-05-generate-administrasi.md ← (ARSIP) Administrasi/Nota Dinas — dihapus dari alur v2.7 (manual)
│
├─ templates/                            ← Template LHP per jenis (disediakan auditor)
│  ├─ TARUH-TEMPLATE-LHP-DI-SINI.md
│  └─ [jenis-pengawasan]/template-lhp.docx
│
└─ penugasan/                            ← SATU FOLDER PER PENUGASAN (v4)
   └─ [TAHUN]-[NOMOR]-[jenis]-[obyek]/
      ├─ 00-input/                       ← (v4) Auditor unduh dari INTEGRAL:
      │  ├─ ST-*.pdf                       ST, KP, PKP
      │  ├─ KP-*.docx                      + dokumen pendukung pengawasan
      │  ├─ PKP-*.docx                       (KAK, HPS, kontrak, BAST, dll.)
      │  └─ [dokumen-pendukung-lain]
      ├─ _ROLE.md                        ← (v4 — Task 00) sumber kebenaran role sesi ini
      ├─ context.md                      ← (Task 01) — jangan hapus
      ├─ _PKP/
      │  └─ sasaran-assignment.json      ← (v4 — Task 01) pembagian sasaran
      ├─ _KKP/
      │  ├─ temuan.json                  ← (v4 — Task 03) sumber kebenaran inject INTEGRAL
      │  └─ KKP-[nama-anggota].docx      ← view per anggota
      ├─ _LHP/
      │  └─ LHP-SUBSTANSI-[nomor-ST].docx  ← (Task 04, ketua tim)
      └─ _AUDIT-TRAIL/
         └─ events.jsonl                 ← (v4) JSON Lines append-only event log
```

> **Catatan**: folder lama `00-surat-tugas/`, `01-peraturan-internal/`, ... `05-keuangan/` masih bisa dipakai untuk kompatibilitas dengan penugasan v3 yang berjalan. Untuk penugasan baru v4, gunakan struktur `00-input/` flat (auditor mengelola pengelompokan dokumen di INTEGRAL, bukan di filesystem Claude).

---

## Cara Memulai Penugasan Baru — v4

### Langkah 1 (di INTEGRAL): Auditor entry penugasan & bagi sasaran

Ketua tim entry penugasan di INTEGRAL, mengisi Kartu Penugasan (KP) dan Program Kerja Pengawasan (PKP), termasuk **pembagian sasaran ke anggota tim**. Cetak/unduh ST + KP + PKP.

### Langkah 2 (di filesystem): Buat folder penugasan & taruh input

```
penugasan/[TAHUN]-[BULAN]-[NOMOR]-[jenis]-[obyek-singkat]/
└─ 00-input/
   ├─ ST-*.pdf
   ├─ KP-*.docx
   ├─ PKP-*.docx
   └─ [dokumen-pendukung-pengawasan]
```

### Langkah 3: Anggota tim mulai sesi di Claude Cowork

Sapa Claude (Indonesian/English):
```
"Saya mau mulai penugasan 2026-05-001-reviu-pengadaan-bakti."
```

Claude akan menjalankan:
1. **Task 00** — tanya nama lengkap & role Anda → tulis `_ROLE.md`
2. **Task 01** — baca ST/KP/PKP → tulis `context.md` + `_PKP/sasaran-assignment.json`
3. **Task 03** — analisis dokumen → tulis `_KKP/temuan.json` + `_KKP/KKP-[Nama].docx`
   *(hanya untuk sasaran yang ditugaskan ke Anda)*

Setelah anggota lain juga selesai sesi mereka:

4. **Ketua tim** sapa Claude:
```
"Saya mau lanjut LHP penugasan 2026-05-001-reviu-pengadaan-bakti."
```

Claude akan:
1. **Task 00** — tanya nama & role → tulis `_ROLE.md` baru (kalau ketua tim)
2. **Task 04** — completeness check → kalau lengkap, tulis `_LHP/LHP-SUBSTANSI.docx`
   *(diblokir + reminder kalau ada anggota belum kerjakan KKP)*

### Langkah 4 (di INTEGRAL): Approve KKP draft + finalisasi administrasi

🆕 **Sejak v4.2 (10 Mei 2026):** KKP otomatis ter-inject ke INTEGRAL di akhir Task 03 via `scripts/integral_inject.py`. Auditor tidak perlu copy-paste manual lagi.

Yang masih manual:
1. Login INTEGRAL → review KKP draft yang sudah auto-inject → klik **Approve** agar status berubah dari `ai_draft` → `auditor_approved` (muncul di dashboard pimpinan).
2. Isi nomor surat (SIMWAS), tanggal, tembusan, Nota Dinas pengantar di Word → TTD & kirim ke auditan.

**Exception (tetap manual upload ke INTEGRAL):** konsultasi-pengadaan, evaluasi-spip, evaluasi-reformasi-birokrasi, pemantauan-tindak-lanjut. Untuk 4 jenis ini, output format khusus (Excel/skeleton) jadi tidak masuk endpoint `/kertas-kerja`.

---

## (Lama, untuk kompatibilitas v3) Cara Memulai Penugasan Baru — v3

### Langkah 1: Buat folder penugasan

```
penugasan/[TAHUN]-[NOMOR]-[jenis]-[obyek-singkat]/
```

Contoh:
```
penugasan/2025-254-audit-kinerja-om-tkppse/
penugasan/2026-031-evaluasi-rb-tw4-djprd/
penugasan/2026-067-reviu-pengadaan-dc-psre/
```

### Langkah 2: Upload Surat Tugas

Simpan ST ke: `penugasan/[nama-folder]/00-surat-tugas/`

Upload dokumen lain sesuai folder:
- `01-peraturan-internal/` → SOP, peraturan internal auditan
- `02-kontrak/` → kontrak, addendum
- `03-perencanaan/` → KAK, HPS, RUP
- `04-pelaksanaan/` → laporan progres, BA, BAST, data kinerja
- `05-keuangan/` → tagihan, bukti bayar, SPM/SP2D

### Langkah 3: Mulai di Claude Cowork

Ketik di Claude:
```
Mulai penugasan baru di folder penugasan/[nama-folder]/
```

Claude akan membaca `tasks/01-start-audit.md` dan memandu langkah berikutnya.

### Langkah 4: Ikuti alur konfirmasi

Setiap gate memerlukan konfirmasi auditor:
1. `LANJUT` → lanjut ke task berikutnya
2. `KOREKSI [apa yang perlu dikoreksi]` → Claude perbaiki dulu
3. `ULANG` → periksa ulang dari awal task ini

---

## Nomor Dokumen

| Dokumen | Format Nomor | Contoh |
|---------|-------------|--------|
| Kartu Penugasan | `KP/[no]/IJ.3/KP.01.06/[bln]/[thn]` | KP/254/IJ.3/KP.01.06/11/2025 |
| Program Kerja | `PKP/[no]/IJ.3/KP.01.06/[bln]/[thn]` | PKP/254/IJ.3/KP.01.06/11/2025 |
| KKP per Sasaran | `KKP-[n]/[no]/IJ.3/KP.01.06/[bln]/[thn]` | KKP-1/254/IJ.3/KP.01.06/11/2025 |
| Laporan Hasil (B-) | `B-[no]/IJ.3/PW.04.04/[bln]/[thn]` | B-67/IJ.3/PW.04.04/02/2026 |

**Kode nomor surat laporan:**
- Audit / Reviu → PW.04.04
- Evaluasi → PW.04.05
- Pemantauan → PW.04.06

---

## Standar Format Dokumen DOCX (LHP)

Saat mengedit template DOCX secara programatik (via XML/python-docx), gunakan standar ini agar konsisten dengan template resmi:

| Elemen | Nilai | Keterangan |
|--------|-------|-----------|
| Font | `Arial` | Bukan Times New Roman |
| Alignment | `jc=both` (justified) | Tambahkan di `w:pPr` sebelum `w:rPr` |
| Font size | `sz=24` (= 12pt) | Untuk isi teks standar |
| Ordering | `jc` harus **sebelum** `rPr` di pPr | Wajib — OOXML schema |

**Wajib**: Duplikasi template yang ada (`cp template.docx output.docx`), jangan buat file DOCX baru dari nol. Ini memastikan header, footer, kop surat, dan gaya halaman tetap konsisten.

Fungsi Python siap pakai tersedia di `tasks/04-generate-lhp.md` (bagian "Panduan Formatting DOCX").

---

## Uji Coba yang Telah Selesai

| Penugasan | Status | Temuan | Catatan |
|-----------|--------|--------|---------|
| 2026-UJI — Reviu Pengadaan DC/DRC PSrE Induk TA 2026 | ✅ SELESAI (8 Apr 2026) | 9 catatan (2 rekomendasi) | Pertama pakai v2.3; ditemukan 2 isu baru (SLA inconsistency + missing migration costs) yang kemudian ditambahkan ke skill |

---

## Prinsip Desain Sistem

### 1. Anti-Halusinasi
- Semua data di KP/PKP wajib berasal dari ST — tidak boleh dikarang
- Semua kondisi di KKP wajib mencantumkan sumber dokumen (nama file + halaman/pasal)
- Semua kriteria di KKP wajib menyebut pasal/ketentuan yang tepat dari references/
- Field yang tidak diketahui → tandai `[DIISI AUDITOR]`, jangan menebak

### 2. Gate/Checkpoint yang Ketat
- Claude tidak boleh lanjut ke task berikutnya tanpa konfirmasi eksplisit auditor
- Setiap gate ada pesan jelas: apa yang perlu diperiksa, apa yang masih kosong, apa langkah berikutnya
- Koreksi substansi → selalu di task yang relevan (KKP di Task 03, LHP di Task 04)

### 3. Pemisahan Tanggung Jawab yang Jelas
| Tahap | Yang Dikerjakan Claude | Yang Dikerjakan Auditor |
|-------|----------------------|------------------------|
| KP + PKP | Generate dari ST (atau find-replace template untuk 6 jenis standar) | Review, isi yang kosong, tanda tangan |
| KKP | Analisis + temuan | Baca, koreksi, konfirmasi |
| LHP Substansi | Temuan + rekomendasi + placeholder `[DIISI AUDITOR]` untuk admin | Baca, koreksi, konfirmasi |
| Administrasi | — (tidak dikerjakan Claude sejak v2.7) | Isi nomor surat (SIMWAS), tanggal, destinatari, Nota Dinas, TTD, kirim |

### 4. Satu Penugasan = Satu Folder
- Semua output tersimpan rapi di subfolder `_KP/`, `_PKP/`, `_KKP/`, `_LHP/`
- `context.md` adalah "memory" yang menyimpan status penugasan
- Jika sesi Claude baru: baca `context.md` untuk resume konteks

### 5. Ringkasan Dokumen Inline — Hemat Token (v2.5)
- Task 03 melakukan file listing + ringkasan singkat dokumen di Langkah 1 & 2, lalu menggunakan ringkasan tersebut (di memori conversation) sebagai basis analisis Langkah 3
- Tidak perlu file `index-dokumen.md` — ringkasan cukup di memori conversation saja
- Jika folder kosong total → Task 03 berhenti, minta auditor upload
- Estimasi penghematan: hilangnya Task 02 + model tiering = target ≥40% hemat token

### 6. Scope Switch — Sesuaikan Cakupan dengan Penugasan
- Setiap skill dapat memiliki beberapa scope (contoh: reviu-pengadaan → Perencanaan vs Pemilihan)
- Scope dipilih di Task 01 dan dicatat di `context.md`
- Scope yang lebih sempit = lebih sedikit dokumen yang dibutuhkan = lebih cepat dan hemat
- Jangan periksa aspek di luar scope yang disepakati auditor

---

## Tips Penting

- **Baca dulu** `panduan-format-umum/PANDUAN.md` sebelum menghasilkan laporan apapun
- **Bahasa keyakinan terbatas**: gunakan "tidak terdapat hal-hal yang membuat kami yakin bahwa... tidak terpenuhi"
- **Bahasa keyakinan memadai**: gunakan "berdasarkan prosedur audit... menurut pendapat kami..."
- **Rekomendasi tidak ada di KKP** — hanya di LHP setelah substansi disetujui
- **Evaluasi SPIP dan RB**: output adalah LKE Excel yang diisi (berbeda dari KKP tabel Word)
- **Survei SIMWAS**: jika ada link, cantumkan di Nota Dinas
- **Update references**: perbarui file references/ ketika ada perubahan regulasi

---

## Kondisi Khusus

### Jika dokumen dikirim via chat (bukan folder):
Untuk reviu/konsultasi cepat yang dokumennya dikirim langsung di chat — Task 03 langsung pakai konten chat sebagai basis analisis, tidak perlu file listing folder.

### Jika template LHP tidak tersedia:
Task 04 punya format standar built-in. Namun sangat disarankan membuat template Word dari LHP yang sudah pernah ditandatangani.

### Jika ada koreksi setelah LHP Substansi disetujui:
- Koreksi substansi (temuan/rekomendasi): kembali ke Task 04, buat versi baru (`-v2.docx`)
- Koreksi administratif (nomor/tanggal/nama/destinatari/Nota Dinas): edit langsung di Word oleh auditor — tidak perlu Claude

### Untuk Evaluasi SPIP dan Evaluasi RB:
Task 02b (KP + PKP) tetap dijalankan normal. Task 03 digantikan oleh pengisian LKE Excel sesuai masing-masing SKILL.md.
