# Verifikasi v4.0 — Hasil Smoke Test

**Tanggal:** 2 Mei 2026
**Penguji:** Claude (cowork session inspektorat2.kominfo.2)
**Sumber:** `audit-system v3` (27 April 2026, dengan exclusion `.git`)
**Folder hasil:** `audit-system-v4/`
**Folder uji coba:** `audit-system-v4/penugasan/CONTOH-2026-05-001-reviu-pengadaan-bakti/` — **dipertahankan** sebagai contoh hidup struktur folder & output (lihat `README-CONTOH.md` di dalamnya)

## Komponen yang Diuji

| # | Komponen | Hasil |
|---|---|---|
| 1 | `role_check.py` AT → Task 03 | ✅ OK (exit 0) |
| 2 | `role_check.py` AT → Task 04 | ✅ DENIED (exit 2) — sesuai spek |
| 3 | `validate_kkp_json.py` schema deteksi `temuan.json` | ✅ valid |
| 4 | `validate_kkp_json.py` schema deteksi `sasaran-assignment.json` | ✅ valid |
| 5 | `sasaran_completeness.py` semua sasaran BELUM_DIKERJAKAN | ✅ BLOKIR (exit 2) + reminder dicetak |
| 6 | `audit_trail.py log-event` ROLE_LOGIN, TASK_STARTED, KKP_TEMUAN_ADDED, SASARAN_COMPLETED | ✅ semua tertulis ke `events.jsonl` (4 baris) |
| 7 | `sasaran_completeness.py` setelah update semua status SELESAI_KKP | ✅ PASS (exit 0) — LHP boleh dimulai |
| 8 | `validate_kkp_json.py` JSON dengan judul "TERPENUHI" + dokumen_sumber kosong | ✅ FAILED (exit 2) — 2 error terdeteksi (judul too short pattern, dokumen_sumber empty) |
| 9 | `role_check.py` tanpa `_ROLE.md` | ✅ DENIED (exit 2) — minta jalankan Task 00 |
| 10 | `role_check.py` KT → Task 04 OK, KT → Task 03 DENIED | ✅ sesuai matriks role |
| 11 | Format `_AUDIT-TRAIL/events.jsonl` JSON Lines valid (parse via `json.tool`) | ✅ ya |

## Catatan

- **Auto-detect schema** di `validate_kkp_json.py` berdasarkan substring nama file (`temuan` atau `sasaran`). File dengan nama random butuh `--schema` explicit. Sudah didokumentasikan di docstring script.
- **`jsonschema` library** terdeteksi dan dipakai. Fallback manual checker juga jalan kalau lib tidak tersedia.
- **Audit trail** ditulis di timezone WIB (+07:00). Log event-nya terbukti append-only & idempotent (tiap call bikin event_id baru).
- **Reminder ke ketua tim** menampilkan: nomor sasaran, deskripsi, status, anggota tim assignee — siap di-copy ke chat untuk visibility.

## Status

✅ v4.0 **siap dipakai** untuk penugasan baru. Penugasan v3 yang sedang berjalan tetap di v3 (tidak perlu migrasi paksa).

## Backlog yang ditandai

- v4.1: upgrade `dashboard_penugasan.py` untuk include kolom Role & Sasaran Completion (saat ini dashboard masih format v3).
- v4.2: integrator INTEGRAL CLI yang men-POST `temuan.json` ke endpoint INTEGRAL (saat API tersedia).
- v4.3: artifact HTML untuk visualisasi audit trail per penugasan.

---

## Patch v4.0.1 — QC Kepatuhan SAIPI (2 Mei 2026, sore)

**Komponen baru:**
- Skill `kepatuhan-saipi/` (SKILL.md + 5 references SAIPI 1100/1200/2200/2300/2400 + checklist mapping JSON)
- Script `scripts/qc_saipi.py` (auto-check, --stage kkp|lhp)
- PDF SAIPI di `wiki/raw/SAIPI-PER-01-AAIPI-DPN-2021.pdf`
- Inject auto-call di Task 03 (langkah 6a.2) & Task 04 (sebelum gate KT)
- `audit_trail.py` KNOWN_ACTIONS tambah `SAIPI_CHECK`

**Smoke test (6 skenario):**

| # | Skenario | Hasil |
|---|---|---|
| 1 | Penugasan minimal (kosong), stage=kkp | ✅ 4 KRITIS terdeteksi (KP/PKP missing, context.md missing, file ref missing), exit 2 |
| 2 | Penugasan minimal, stage=lhp | ✅ 10 KRITIS (semua heading LHP missing + statement SAIPI 2430), exit 2 |
| 3 | Happy path lengkap, stage=kkp | ✅ 16 OK / 0 KRITIS / 3 NEEDS_REVIEW (manual saja), exit 0 |
| 4 | Happy path lengkap, stage=lhp | ✅ 25 OK / 0 KRITIS / 5 NEEDS_REVIEW, exit 0 |
| 5 | Inject placeholder bocor `{{TANGGAPAN_TBD}}` di LHP | ✅ KOM-005 KRITIS terdeteksi (whitelist `[DIISI AUDITOR]` tetap pass), exit 2 |
| 6 | Audit trail VALIDATION_PASSED/FAILED ter-log | ✅ 3 event SAIPI ter-record (kkp pass, lhp pass, lhp fail) |

**Contoh hidup:** `penugasan/CONTOH-HAPPY-PATH-saipi/` — referensi struktur lengkap yang lulus QC SAIPI penuh.

**Catatan implementasi:**
- LHP docx parsing tanpa external lib (parse `word/document.xml` via stdlib zipfile + ElementTree).
- 30 rules total: 19 untuk stage=kkp, 30 untuk stage=lhp (yang lhp termasuk semua kkp + 10 KOM rules).
- Whitelist placeholder `[DIISI AUDITOR]` dihormati di KOM-005 (cek case-insensitive substring).
