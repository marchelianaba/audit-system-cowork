# Pipeline Evaluasi SPIP — v0.2 (production-ready)

Pipeline untuk skill `evaluasi-spip`. **Status: production-ready v0.2** — di-tune dari sample LKE SPIP Kementerian nyata.

## Arsitektur

```
LKE SPIP.xlsx ─► digest_lke.py (dari evaluasi-sakip) ─► lke.json ─► cross_check.py ─► anomalies.json
(Multi-sheet: KKLEAD_SPIP rekap, 24 sheet detail per unsur)
```

## Reuse dari evaluasi-sakip

`digest_lke.py` sama file — auto-detect LKE SAKIP vs SPIP berdasarkan keberadaan sheet `KKLEAD_SPIP`. Extraction untuk SPIP menghasilkan:
- 3 komponen utama (Penetapan Tujuan 0.4, Struktur 0.3, Hasil 0.3)
- Subunsur per komponen (Penetapan: 2; Struktur: 25; Hasil: 7 kategori)
- Skor PM (Penilaian Mandiri) + PK (Penilaian Kualitas APIP) per subunsur

## 4 Rules v0.1

| ID | Aspek | Severity | Rule |
|---|---|---|---|
| SP.1 | Struktur | PERINGATAN | Total bobot 3 komponen ≠ 1.0 |
| SP.2 | Substantif | KRITIS/PERINGATAN | Subunsur dengan skor PK < 2 (Rintisan/Awal) |
| SP.3 | Substantif | PERINGATAN | Gap > 1 poin antara PM dan PK |
| SP.4 | Hasil | KRITIS | Nilai maturitas total < Level 3 |

## Hasil Demo pada `LKE SPIP KEMENTERIAN.xlsx`

**Parser**: 3 komponen + 25 subunsur Struktur + 2 subunsur Penetapan + bobot correct (0.4+0.3+0.3=1.0).
**Cross-check**: 1 anomali ter-deteksi:
- SP.3 — 5 subunsur memiliki gap > 1 poin antara PM (unit kerja) dan PK (APIP)

Real finding: unit kerja cenderung over-estimate maturitas dibandingkan evaluasi APIP pada beberapa subunsur.

## 4 Konfirmasi Wajib Auditor (dari feedback_evaluasi_spip memory)

Saat menjalankan skill ini via Task workflow, 4 konfirmasi wajib dilakukan (jangan diabaikan):
1. Konfirmasi kelengkapan LKE dari 8 satker
2. Konfirmasi status bukti dukung (lengkap vs parsial)
3. Konfirmasi selisih PM vs PK (untuk tiap subunsur yang flag)
4. Konfirmasi rekomendasi AoI lintas unsur

## Cara Pakai

```bash
# Digest (pakai script dari evaluasi-sakip karena auto-detect)
python3 scripts/evaluasi-sakip/digest_lke.py \
  "penugasan/SPIP/_KKP/LKE SPIP KEMENTERIAN.xlsx" \
  -o "penugasan/SPIP/_KKP/lke.json"

# Cross-check SPIP (rules khusus SPIP)
python3 scripts/evaluasi-spip/cross_check.py \
  "penugasan/SPIP/_KKP/lke.json" \
  -o "penugasan/SPIP/_KKP/anomalies.json"
```

## Roadmap v0.3

- Parser KK Lead II (tabular multi-dimensi) untuk extract parameter detail
- Bukti dukung tracking per subunsur (flag parsial < 80%)
- Rule tambahan: Loss Event Database referenced, Aplikasi MR K/L terkelola
- Renderer LHE SPIP lengkap dengan peta jalan maturitas
