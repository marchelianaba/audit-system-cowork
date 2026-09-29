"""
cross_check.py — Rule-based cross-check untuk LKE SPIP.

Rules v0.1:
  - SP.1 Bobot 3 komponen tidak 1.0 (harus 0.4+0.3+0.3)
  - SP.2 Subunsur dengan skor PK < 2 (Rintisan/Berkembang awal)
  - SP.3 Gap besar antara PM dan PK (unit over-claim maturitas)
  - SP.4 Unsur tanpa nilai sub-jumlah
  - SP.5 Nilai maturitas final < Level 3 (perlu attention)
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


def rule_sp1_bobot_komponen(lke):
    """SP.1 — Bobot 3 komponen harus total 1.0."""
    rekap = lke.get("rekap", {})
    bp = rekap.get("bobot_perencanaan")
    bs = rekap.get("bobot_struktur")
    bh = rekap.get("bobot_hasil")
    if not all(x is not None for x in [bp, bs, bh]):
        return None
    total = bp + bs + bh
    if abs(total - 1.0) < 0.01:
        return None
    return _rule(
        "SP.1", PERINGATAN, "Struktur",
        f"Total bobot komponen SPIP = {total} (seharusnya 1.0)",
        "Bobot 3 komponen SPIP: Perencanaan (0.4), Struktur (0.3), Hasil (0.3).",
        bukti={"bobot_perencanaan": bp, "bobot_struktur": bs, "bobot_hasil": bh, "total": total},
        draft={
            "kondisi": f"Total bobot 3 komponen SPIP tidak sama dengan 1.0 "
                       f"(Perencanaan={bp}, Struktur={bs}, Hasil={bh}, total={total}).",
            "kriteria": "Peraturan BPKP 5/2021 — bobot 3 komponen SPIP total harus 1.0.",
            "akibat": "Nilai maturitas akhir tidak valid; tidak dapat dibandingkan lintas K/L.",
        }
    )


def rule_sp2_subunsur_skor_rendah(lke):
    """SP.2 — Subunsur dengan skor PK < 2 (butuh perhatian serius)."""
    low = []
    for k in lke.get("unsur", []):
        for u in k.get("unsur", []):
            skor = u.get("skor_pk")
            if skor is not None and skor < 2:
                low.append({"komponen": k["nama_komponen"],
                            "subunsur": u["nama"], "skor_pk": skor})
    if not low:
        return None
    return _rule(
        "SP.2", KRITIS if len(low) >= 3 else PERINGATAN, "Substantif",
        f"{len(low)} subunsur SPIP bernilai di bawah Level 2 (Rintisan/Awal Berkembang)",
        "Subunsur dengan skor < 2 menunjukkan penyelenggaraan SPIP masih rintisan.",
        bukti={"subunsur_rendah": low},
        draft={
            "kondisi": f"Terdapat {len(low)} subunsur SPIP dengan skor PK < 2 "
                       f"(kategori Rintisan/Awal Berkembang): "
                       f"{', '.join(x['subunsur'][:50] for x in low[:3])}.",
            "kriteria": "Peraturan BPKP 5/2021 — subunsur SPIP diharapkan mencapai minimal "
                        "Level 3 (Terintegrasi) untuk K/L matang.",
            "akibat": "Sistem pengendalian intern pada subunsur terkait belum memadai untuk "
                      "mencegah risiko operasional dan keuangan; berpotensi temuan BPK/BPKP.",
        }
    )


def rule_sp3_gap_pm_pk(lke):
    """SP.3 — Gap > 1 poin antara Penilaian Mandiri (PM) dan Penilaian Kualitas (PK)."""
    gap = []
    for k in lke.get("unsur", []):
        for u in k.get("unsur", []):
            pm = u.get("skor_pm")
            pk = u.get("skor_pk")
            if pm is None or pk is None:
                continue
            if abs(pm - pk) >= 1.0:
                gap.append({
                    "komponen": k["nama_komponen"], "subunsur": u["nama"],
                    "skor_pm": pm, "skor_pk": pk, "selisih": round(pm - pk, 2),
                })
    if not gap:
        return None
    return _rule(
        "SP.3", PERINGATAN, "Substantif",
        f"{len(gap)} subunsur memiliki gap > 1 poin antara PM (unit kerja) dan PK (APIP)",
        "Gap besar PM vs PK menunjukkan over-estimate/under-estimate unit kerja.",
        bukti={"gap": gap[:8]},
        draft={
            "kondisi": f"Terdapat {len(gap)} subunsur SPIP dengan perbedaan skor Penilaian Mandiri "
                       f"(PM) vs Penilaian Kualitas (PK) APIP ≥ 1 poin.",
            "kriteria": "Peraturan BPKP 5/2021 — PM dan PK diharapkan selaras; gap besar "
                        "mengindikasikan perlunya re-evaluasi bukti dukung.",
            "akibat": "Unit kerja berpotensi over-claim/under-claim maturitas; kredibilitas "
                      "penilaian mandiri menurun dan memerlukan pembahasan ulang.",
        }
    )


def rule_sp4_maturitas_di_bawah_level_3(lke):
    """SP.4 — Nilai maturitas total di bawah Level 3 (Terintegrasi)."""
    nilai = lke.get("rekap", {}).get("nilai_maturitas_total")
    if nilai is None:
        return None
    if nilai >= 3.0:
        return None
    return _rule(
        "SP.4", KRITIS, "Hasil",
        f"Nilai maturitas SPIP total = {nilai} (di bawah Level 3 Terintegrasi)",
        "K/L tingkat Kementerian diharapkan minimal Level 3.",
        bukti={"nilai": nilai, "kategori": lke.get("rekap", {}).get("kategori_maturitas")},
        draft={
            "kondisi": f"Nilai maturitas SPIP final: {nilai} "
                       f"({lke.get('rekap', {}).get('kategori_maturitas', '—')}) — "
                       f"di bawah Level 3 (Terintegrasi).",
            "kriteria": "Peraturan BPKP 5/2021 — K/L diharapkan mencapai Level 3 (Terintegrasi) "
                        "sebagai standar minimum maturitas SPIP.",
            "akibat": "Penyelenggaraan SPIP belum memadai untuk mencegah risiko menyeluruh; "
                      "perlu peta jalan peningkatan maturitas untuk tahun berikutnya.",
        }
    )


ALL_RULES = [
    rule_sp1_bobot_komponen,
    rule_sp2_subunsur_skor_rendah,
    rule_sp3_gap_pm_pk,
    rule_sp4_maturitas_di_bawah_level_3,
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
    Path(args.output).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"=== CROSS-CHECK SPIP ===")
    print(f"Tested {len(ALL_RULES)} rules; Found {len(anomalies)} anomalies")
    for a in anomalies:
        print(f"  [{a.get('severity','?'):11s}] {a.get('rule_id','?'):6s} -- {a.get('judul','?')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
