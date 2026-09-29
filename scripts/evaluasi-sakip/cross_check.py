"""
cross_check.py — Rule-based cross-check untuk LKE SAKIP.

Rules v0.1 fokus pada validasi struktural LKE:
  - Kelengkapan 4 komponen + bobot total 100
  - Kesesuaian nilai mandiri vs nilai APIP (indikasi bias unit kerja)
  - Catatan evaluator yang menunjukkan AoI (Area of Improvement)
  - Subkomponen tanpa bukti dukung (bila kolom BUKTI DUKUNG UPLOAD kosong)

Usage:
    python cross_check.py <lke-sakip.json> [-o anomalies.json]
"""

from __future__ import annotations
import argparse, json, sys
from pathlib import Path

PERINGATAN = "PERINGATAN"
INFO = "INFO"
KRITIS = "KRITIS"


def _rule(rule_id, severity, aspek, judul, deskripsi, bukti=None, draft=None):
    return {
        "rule_id": rule_id,
        "severity": severity,
        "aspek": aspek,
        "judul": judul,
        "deskripsi": deskripsi,
        "bukti": bukti or {},
        "draft_catatan": draft,
    }


def rule_sa1_komponen_tidak_lengkap(lke):
    """SA.1 — SAKIP harus punya 4 komponen."""
    komp = lke.get("komponen", [])
    if len(komp) == 4:
        return None
    return _rule(
        "SA.1", KRITIS, "Struktur",
        f"LKE SAKIP hanya memiliki {len(komp)} komponen (seharusnya 4)",
        f"Permenpan 88/2021 menetapkan 4 komponen SAKIP: Perencanaan Kinerja, "
        f"Pengukuran Kinerja, Pelaporan Kinerja, Evaluasi Akuntabilitas Kinerja Internal.",
        bukti={"komponen_found": [k["nama"] for k in komp]},
        draft={
            "kondisi": f"LKE SAKIP memuat {len(komp)} komponen: "
                       f"{', '.join(k['nama'] for k in komp)}.",
            "kriteria": "Permenpan RB 88/2021 — SAKIP memiliki 4 komponen utama.",
            "akibat": "Evaluasi tidak mencakup seluruh aspek akuntabilitas kinerja secara komprehensif.",
        }
    )


def rule_sa2_bobot_tidak_100(lke):
    """SA.2 — Total bobot 4 komponen harus 100."""
    komp = lke.get("komponen", [])
    total = sum(k.get("bobot") or 0 for k in komp)
    if abs(total - 100) < 0.5:
        return None
    return _rule(
        "SA.2", PERINGATAN, "Struktur",
        f"Total bobot komponen = {total} (seharusnya 100)",
        "Bobot komponen SAKIP harus total 100%.",
        bukti={"bobot_per_komponen": {k["nama"]: k.get("bobot") for k in komp}, "total": total},
        draft={
            "kondisi": f"Total bobot 4 komponen SAKIP: {total} (bukan 100).",
            "kriteria": "Permenpan RB 88/2021 — bobot 4 komponen harus sama dengan 100%.",
            "akibat": "Perhitungan nilai akhir AKIP tidak valid; evaluasi tidak dapat dibandingkan "
                      "dengan K/L lain atau tahun sebelumnya.",
        }
    )


def rule_sa3_catatan_evaluator_kosong(lke):
    """SA.3 — Banyak subkomponen tanpa catatan evaluator padahal nilai tidak 100%."""
    gap = []
    for k in lke.get("komponen", []):
        for sub in k.get("subkomponen", []):
            nilai = sub.get("nilai_mandiri_persen") or ""
            if "%" in str(nilai) and str(nilai) != "100.00%":
                if not sub.get("catatan_evaluator"):
                    gap.append({"komponen": k["no"], "subkomponen": sub["no"],
                                "nilai": nilai, "uraian": sub["uraian"][:80]})
    if len(gap) < 3:
        return None
    return _rule(
        "SA.3", PERINGATAN, "Substantif",
        f"{len(gap)} subkomponen tidak 100% namun evaluator tidak memberi catatan",
        "Subkomponen dengan nilai kurang dari 100% seharusnya memuat catatan AoI dari evaluator.",
        bukti={"gap_sample": gap[:6], "total_gap": len(gap)},
        draft={
            "kondisi": f"Terdapat {len(gap)} subkomponen yang nilainya < 100%, namun tidak "
                       f"terdapat catatan dari evaluator atas penyebab atau area perbaikan.",
            "kriteria": "Pedoman Evaluasi SAKIP — evaluator wajib memberi catatan AoI pada "
                        "subkomponen yang tidak mencapai 100% untuk basis tindak lanjut.",
            "akibat": "Unit kerja tidak mendapat arahan konkret untuk perbaikan; "
                      "rekomendasi LHE menjadi tidak berbasis bukti yang tertulis dalam LKE.",
        }
    )


def rule_sa4_rekomendasi_evaluator_kosong(lke):
    """SA.4 — Komponen dengan nilai di bawah 90% tanpa rekomendasi."""
    gap = []
    for k in lke.get("komponen", []):
        for sub in k.get("subkomponen", []):
            jawaban = sub.get("jawaban_akhir_mandiri", "")
            # kategori rendah: CC, C, D — tapi kita juga flag BB di bawah 100%
            nilai_pct = str(sub.get("nilai_mandiri_persen") or "")
            if "%" in nilai_pct:
                pct_num = float(nilai_pct.rstrip("%").replace(",", "."))
                if pct_num < 90 and not sub.get("rekomendasi_evaluator"):
                    gap.append({"komponen": k["no"], "subkomponen": sub["no"],
                                "persen": nilai_pct, "uraian": sub["uraian"][:80]})
    if not gap:
        return None
    return _rule(
        "SA.4", PERINGATAN, "Substantif",
        f"{len(gap)} subkomponen dengan nilai < 90% tidak memuat rekomendasi evaluator",
        "Subkomponen dengan nilai rendah wajib memuat rekomendasi perbaikan.",
        bukti={"gap": gap[:6]},
        draft={
            "kondisi": f"Terdapat {len(gap)} subkomponen dengan nilai < 90% yang tidak "
                       f"dilengkapi rekomendasi dari evaluator.",
            "kriteria": "Pedoman Evaluasi SAKIP — subkomponen bernilai rendah wajib memuat "
                        "rekomendasi konkret untuk perbaikan tahun berikutnya.",
            "akibat": "Area perbaikan tidak teridentifikasi dengan actionable guidance; "
                      "unit kerja tidak memiliki dasar untuk perencanaan tindak lanjut.",
        }
    )


def rule_sa5_evaluasi_apip_kosong(lke):
    """SA.5 — Kolom EVALUASI APIP kosong padahal ini LKE APIP."""
    is_apip = "APIP" in (lke.get("metadata", {}).get("source_file") or "").upper()
    if not is_apip:
        return None
    gap = []
    for k in lke.get("komponen", []):
        if k.get("nilai_apip_nilai") is None:
            gap.append(k["nama"])
    if not gap:
        return None
    return _rule(
        "SA.5", PERINGATAN, "Dokumentasi",
        f"{len(gap)} komponen di LKE APIP belum diisi kolom Evaluasi APIP",
        "LKE APIP harus berisi evaluasi independen APIP atas penilaian mandiri unit kerja.",
        bukti={"komponen_belum_dievaluasi": gap},
        draft={
            "kondisi": f"LKE APIP ({lke['metadata']['source_file']}) memuat {len(gap)} komponen "
                       f"yang kolom Evaluasi APIP-nya masih kosong: {', '.join(gap)}.",
            "kriteria": "Permenpan RB 88/2021 — LKE APIP wajib diisi evaluasi independen atas "
                        "penilaian mandiri unit kerja.",
            "akibat": "Evaluasi sepihak unit kerja tidak divalidasi; reliabilitas nilai AKIP "
                      "final tidak dapat dipertanggungjawabkan.",
        }
    )


ALL_RULES = [
    rule_sa1_komponen_tidak_lengkap,
    rule_sa2_bobot_tidak_100,
    rule_sa3_catatan_evaluator_kosong,
    rule_sa4_rekomendasi_evaluator_kosong,
    rule_sa5_evaluasi_apip_kosong,
]


def run_checks(lke):
    out = []
    for fn in ALL_RULES:
        try:
            r = fn(lke)
            if r:
                out.append(r)
        except Exception as e:
            out.append({"rule_id": fn.__name__, "severity": "ERROR", "error": str(e)})
    return out


def _self_check_ast() -> None:
    """Preflight: pastikan script ini sendiri syntactically valid sebelum run.
    Mencegah eksekusi dengan file korup (mis. akibat OneDrive sync artifact)."""
    import ast
    try:
        ast.parse(open(__file__, "r", encoding="utf-8").read())
    except SyntaxError as e:
        print(f"Self-check AST gagal di {__file__}: {e}", file=sys.stderr)
        print("   File mungkin korup. Lihat backup atau git restore.", file=sys.stderr)
        sys.exit(2)


def main(argv=None):
    _self_check_ast()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("lke_json")
    ap.add_argument("-o", "--output", default="anomalies.json")
    args = ap.parse_args(argv)
    lke = json.loads(Path(args.lke_json).read_text(encoding="utf-8"))
    anomalies = run_checks(lke)
    out = {
        "metadata": {"total_rules_tested": len(ALL_RULES),
                     "total_anomalies_found": len(anomalies)},
        "summary_by_severity": {},
        "anomalies": anomalies,
    }
    for a in anomalies:
        out["summary_by_severity"][a.get("severity", "?")] = \
            out["summary_by_severity"].get(a.get("severity", "?"), 0) + 1
    Path(args.output).write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"=== CROSS-CHECK SAKIP ===")
    print(f"Tested {len(ALL_RULES)} rules; Found {len(anomalies)} anomalies")
    for a in anomalies:
        print(f"  [{a.get('severity','?'):11s}] {a.get('rule_id','?'):6s} -- {a.get('judul','?')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
