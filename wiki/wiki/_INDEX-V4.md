# Index Wiki — Sistem Audit v4

**Summary**: Wiki ini melayani dua tujuan: (1) **basis pengetahuan** Inspektorat II (knowledge base seperti Karpathy LLM Wiki), (2) **memori operasional sistem audit-system-v4** — referensi pattern temuan, audit trail, database KP/PKP, dan TLHP. Setiap penugasan v4 yang selesai (LHP_FINALIZED + INTEGRAL_EXPORT) di-ingest otomatis ke wiki via `scripts/ingest_to_wiki.py`.

**Last updated**: 2026-05-02 (Patch v4.0.2 — auto-ingest pipeline)

---

## Halaman Operasional Sistem v4

Halaman-halaman ini di-maintain otomatis oleh `scripts/ingest_to_wiki.py` setiap penugasan baru di-ingest:

| Halaman | Isi | Auto-update? |
|---|---|---|
| [[pattern-temuan]] | Aggregate pattern temuan dari semua `_KKP/temuan.json` v4 + integrasi `pattern-library/` lama | ✅ tiap ingest |
| [[audit-trail-overview]] | Penjelasan format audit trail v4 + summary aggregat dari semua penugasan | ✅ tiap ingest |
| [[database-kp]] | Database Kartu Penugasan — di-extract dari `00-input/KP-*.{pdf,docx}` tiap penugasan | ✅ tiap ingest |
| [[database-pkp]] | Database Program Kerja Pengawasan — di-extract dari `00-input/PKP-*.{pdf,docx}` | ✅ tiap ingest |
| [[tlhp-index]] | Index Tindak Lanjut Hasil Pengawasan dari semua LHP final | ✅ tiap ingest |
| [[references-index]] | Index seluruh kriteria/regulasi yang dipakai sistem audit | ✅ tiap ingest |

Halaman per-penugasan: `lhp-{slug-penugasan}.md` (di-create tiap selesai pengawasan).

---

## Halaman Knowledge Base Lama

Untuk index lengkap halaman wiki existing (LHR/LHE/LHA/regulasi/profil unit/dll.) lihat [[index]] — index utama wiki yang sudah ada sejak Apr 2026.

Sumber dokumen mentah: `wiki/raw/` (jangan dimodifikasi langsung).

---

## Cara Kerja Ingest Otomatis (v4)

```
[Task 04] LHP final → Ketua tim catat INTEGRAL_EXPORT event
                    ↓
       Auto trigger: scripts/ingest_to_wiki.py --penugasan [path]
                    ↓
   1. Buat wiki/wiki/lhp-{slug}.md (snapshot temuan + LHP metadata)
   2. Re-aggregate wiki/wiki/pattern-temuan.md
   3. Append ke wiki/wiki/database-kp.md & database-pkp.md
   4. Append ke wiki/wiki/tlhp-index.md (rekomendasi → tracking)
   5. Update wiki/wiki/audit-trail-overview.md (summary)
   6. Append entry ke wiki/wiki/log.md
   7. Tulis 1 event INGEST_TO_WIKI ke audit trail penugasan
```

Bila auditor ingin re-ingest manual:
```bash
python3 scripts/ingest_to_wiki.py --penugasan penugasan/[nama]
```

---

## Cross-link

- [[index]] — index wiki utama (knowledge base umum)
- [[wiki-info-yang-perlu-ditambahkan]] — backlog ingest manual yang sudah ada
- [[log]] — append-only log operasi wiki
