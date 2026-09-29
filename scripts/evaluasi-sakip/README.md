# Pipeline Evaluasi SAKIP — v0.2 (production-ready)

Pipeline untuk skill `evaluasi-sakip`. **Status: production-ready v0.2** — di-tune dari sample LKE DJED 2025 APIP nyata.

## Arsitektur

```
LKE.xlsx ─► digest_lke.py ─► lke.json ─► cross_check.py ─► anomalies.json
(Sheet LKE dengan header di R6-R7, hierarki Komponen/Subkomponen/Kriteria)
```

## Komponen

| Script | Fungsi | Status |
|---|---|---|
| `digest_lke.py` | Parser LKE SAKIP (auto-detect vs SPIP) — ekstrak 4 komponen SAKIP + subkomponen + kriteria + nilai mandiri + nilai APIP + catatan/rekomendasi evaluator | ✅ v0.2 |
| `cross_check.py` | 5 rules deterministik (struktur + substansi) | ✅ v0.1 |

## 5 Rules v0.1

| ID | Aspek | Severity | Rule |
|---|---|---|---|
| SA.1 | Struktur | KRITIS | LKE SAKIP tidak memiliki 4 komponen |
| SA.2 | Struktur | PERINGATAN | Total bobot komponen ≠ 100 |
| SA.3 | Substansi | PERINGATAN | Subkomponen < 100% tanpa catatan evaluator (≥3) |
| SA.4 | Substansi | PERINGATAN | Subkomponen < 90% tanpa rekomendasi evaluator |
| SA.5 | Dokumentasi | PERINGATAN | LKE APIP belum diisi kolom Evaluasi APIP |

## Hasil Demo pada `LKE_DJED_2025_APIP.xlsx`

**Parser**: 4 komponen terekstrak dengan bobot benar (30+30+15+25 = 100).
**Cross-check**: 1 anomali ter-deteksi:
- SA.5 — 4 komponen di LKE APIP belum diisi kolom Evaluasi APIP (ini finding riil: LKE ini masih menunggu pengisian evaluasi independen oleh APIP)

## Cara Pakai

```bash
python3 scripts/evaluasi-sakip/digest_lke.py \
  "penugasan/SAKIP/_KKP/LKE_DJED_2025_APIP.xlsx" \
  -o "penugasan/SAKIP/_KKP/lke.json"

python3 scripts/evaluasi-sakip/cross_check.py \
  "penugasan/SAKIP/_KKP/lke.json" \
  -o "penugasan/SAKIP/_KKP/anomalies.json"
```

## Roadmap v0.3

- Extract subkomponen detail (level 1.a, 1.b, dst.) untuk SA.3/SA.4 coverage
- Renderer LHE SAKIP dari anomalies.json
- Mapping ke template LHE standar Inspektorat II
- Rule tambahan: gap PM vs APIP > 10%, catatan AoI belum ditindaklanjuti periode lalu
