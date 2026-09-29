# Audit Trail — Overview Sistem Audit v4

**Summary**: Penjelasan format audit trail v4 (JSON Lines, append-only) + summary aggregat dari seluruh penugasan v4. Setiap aksi yang relevan (login role, gate konfirmasi, file generate, temuan added, reminder, validation) tercatat sebagai 1 baris JSON di `penugasan/[nama]/_AUDIT-TRAIL/events.jsonl`.

**Sources**: `scripts/audit_trail.py` (helper) + `_AUDIT-TRAIL/events.jsonl` per penugasan.

**Last updated**: _(akan di-update otomatis oleh `scripts/ingest_to_wiki.py`)_

---

## Format Event

```json
{
  "event_id": "evt_<uuid12>",
  "timestamp": "2026-05-02T14:30:00+07:00",
  "actor": {"nama": "Sarah Aulia", "role": "Anggota Tim", "role_kode": "AT"},
  "action": "ROLE_LOGIN",
  "target": "_ROLE.md",
  "payload": {...},
  "task": "00",
  "penugasan": "2026-05-001-reviu-pengadaan-bakti"
}
```

## Action Types yang Dikenal

| Action | Pemicu | Task |
|---|---|---|
| `ROLE_LOGIN` | Task 00 berhasil tulis `_ROLE.md` | 00 |
| `TASK_STARTED` | Task 01/03/04 mulai jalan | 01/03/04 |
| `TASK_COMPLETED` | Task 01/03/04 selesai | 01/03/04 |
| `GATE_PASSED` | Auditor LANJUT setelah review | varies |
| `GATE_REJECTED` | Auditor KOREKSI/ULANG | varies |
| `FILE_GENERATED` | File baru ditulis | varies |
| `FILE_UPDATED` | File existing dimodifikasi | varies |
| `KKP_TEMUAN_ADDED` | 1 temuan baru di-append ke temuan.json | 03 |
| `KKP_TEMUAN_UPDATED` | Temuan existing diedit | 03/04 |
| `SASARAN_COMPLETED` | Status sasaran berubah jadi SELESAI_KKP | 03 |
| `LHP_FINALIZED` | Ketua tim SETUJU LHP | 04 |
| `REMINDER_SENT` | Completeness check menemukan gap | 04 |
| `ROLE_DENIED` | role_check.py menolak akses | varies |
| `VALIDATION_PASSED` / `VALIDATION_FAILED` | Validator JSON KKP / qc_saipi | 03/04 |
| `INTEGRAL_EXPORT` | Auditor catat ekspor temuan.json ke INTEGRAL | 04 (post-LHP) |
| `SAIPI_CHECK` | (alias generic) qc_saipi run | 03/04 |
| `INGEST_TO_WIKI` | Penugasan di-ingest ke wiki | 04 (post-LHP) |

## Cara Lihat Trail per Penugasan

```bash
# Tampilkan semua event
python3 scripts/audit_trail.py show --penugasan penugasan/[nama]

# Hanya 10 event terakhir
python3 scripts/audit_trail.py show --penugasan penugasan/[nama] --last 10
```

---

## Summary Aggregat (auto-update)

> _Tabel di bawah ini di-regenerate oleh `scripts/ingest_to_wiki.py` setiap penugasan baru di-ingest._

### Total Events per Action

| Action | Total Events |
|---|---:|
| `VALIDATION_FAILED` | 3 |
| `VALIDATION_PASSED` | 2 |
| `INGEST_TO_WIKI` | 2 |
| `ROLE_LOGIN` | 1 |
| `TASK_STARTED` | 1 |
| `KKP_TEMUAN_ADDED` | 1 |
| `SASARAN_COMPLETED` | 1 |
| `GATE_PASSED` | 1 |
| `LHP_FINALIZED` | 1 |
| `INTEGRAL_EXPORT` | 1 |


### Penugasan Aktif & Selesai

| Penugasan | Stage | Total Events | Last Event | Status |
|---|---|---:|---|---|
| CONTOH-2026-05-001-reviu-pengadaan-bakti | KKP | 6 | 2026-05-02T19:07:55+07:00 | ACTIVE |
| CONTOH-HAPPY-PATH-saipi | LHP_FINAL | 8 | 2026-05-02T19:37:51+07:00 | DONE |

_(updated 2026-05-02)_


---

## Compliance Insight

Audit trail dipakai oleh `scripts/qc_saipi.py` untuk mengecek standar SAIPI 2340 (Supervisi Penugasan): apakah ada `GATE_PASSED` task=03 oleh role KT/PT/PM? Jika ya → bukti supervisi ada.

## Cross-link

- [[_INDEX-V4]]
- [[pattern-temuan]]
- `scripts/audit_trail.py`, `scripts/qc_saipi.py`
