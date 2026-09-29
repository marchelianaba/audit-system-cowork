# Pipeline Pemantauan Pengadaan — v0.1 (production)

Pipeline untuk skill `pemantauan-pengadaan`. **Status: v0.1 production** — reuse digest dari audit-pengadaan dengan 5 rules khusus.

## Arsitektur

```
folder penugasan ─► scripts/audit-pengadaan/digest_pengadaan.py ─► pengadaan-digest.json
                                                                           │
                                                                           ▼
                                      scripts/pemantauan-pengadaan/cross_check.py (5 rules)
                                                                           │
                                                                           ▼
                                                                   anomalies.json
```

## Cara Pakai

```bash
cd audit-system-v4
PENUGASAN=penugasan/[nama]

# 1. Digest (reuse audit-pengadaan)
python3 scripts/audit-pengadaan/digest_pengadaan.py "$PENUGASAN" \
  -o "$PENUGASAN/_KKP/pengadaan-digest.json"

# 2. Cross-check pemantauan
python3 scripts/pemantauan-pengadaan/cross_check.py \
  "$PENUGASAN/_KKP/pengadaan-digest.json" \
  -o "$PENUGASAN/_KKP/anomalies.json"
```

## 5 Rules v0.1

| ID | Aspek | Severity | Rule |
|---|---|---|---|
| PM.1 | Pelaksanaan | PERINGATAN | Jumlah pembayaran > jumlah BAST (progres keuangan > fisik) |
| PM.2 | Pelaksanaan | PERINGATAN | Laporan bulanan tidak ditemukan di folder |
| PM.3 | Kontrak | PERINGATAN | Kontrak menyebut addendum, dokumen addendum terpisah tidak ada |
| PM.4 | Pelaksanaan | KRITIS | Pembayaran dilakukan namun BAST tidak ada |
| PM.5 | Pelaksanaan | PERINGATAN | Kontrak punya SLA tapi BA Rekonsiliasi tidak laporkan SLA aktual |

## Hasil Demo di Sample DCDRC PSrE

- 14 dokumen dikenali oleh digest
- **2 anomali terdeteksi**:
  - PM.2 — Laporan bulanan tidak ditemukan
  - PM.5 — Kontrak memuat klausul SLA namun BA Rekonsiliasi tidak laporkan SLA aktual

## Perbedaan dari audit-pengadaan

| Aspek | audit-pengadaan | pemantauan-pengadaan |
|---|---|---|
| Waktu | Post-pengadaan | Saat pengadaan berjalan |
| Kolom KKP | No, Judul, Kondisi, Kriteria, Sebab, Akibat | No, Judul, Kondisi, Kriteria |
| Jumlah rules | 11 | 5 |
| Fokus | Kepatuhan + kerugian | Progres + deteksi dini |
