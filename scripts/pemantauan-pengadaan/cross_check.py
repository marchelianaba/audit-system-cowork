"""
cross_check.py — Rules pemantauan-pengadaan (reuse digest dari audit-pengadaan).

Pemantauan fokus pada pengadaan yang sedang BERJALAN — cek progres fisik vs
keuangan, keterlambatan timeline, dan amandemen compliance.

Kolom KKP pemantauan: No, Judul, Kondisi, Kriteria (tanpa Sebab/Akibat/Rekomendasi
— pemantauan bersifat observasi, bukan analisis akar masalah).

Usage:
    python cross_check.py <pengadaan-digest.json> [-o anomalies.json]
"""

from __future__ import annotations
import argparse, json, re, sys
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


def _first(d, t):
    items = d.get("dokumen", {}).get(t, [])
    return items[0] if items else None


def _parsed(entry):
    return (entry or {}).get("parsed") or {}


def rule_pm1_progres_fisik_vs_keuangan(digest):
    """PM.1 — Jumlah BAST/BA Rekonsiliasi vs jumlah LS/SPTB (periode tertinggal)."""
    n_bast = len(digest.get("dokumen", {}).get("ba_rekonsiliasi", []))
    n_ls = len(digest.get("dokumen", {}).get("pembayaran_ls", []))
    n_sptb = len(digest.get("dokumen", {}).get("sptb", []))
    n_pembayaran = n_ls + n_sptb
    if n_pembayaran == 0 or n_bast == 0:
        return None
    if n_bast >= n_pembayaran:
        return None
    gap = n_pembayaran - n_bast
    return _rule(
        "PM.1", PERINGATAN, "Pelaksanaan",
        f"Jumlah pembayaran ({n_pembayaran}) melebihi jumlah BAST ({n_bast})",
        f"Indikasi progres keuangan lebih cepat dari progres fisik (gap {gap} periode).",
        bukti={"bast_count": n_bast, "pembayaran_count": n_pembayaran, "gap": gap},
        draft={
            "kondisi": f"Berdasarkan file listing folder penugasan, terdapat {n_pembayaran} "
                       f"dokumen pembayaran namun hanya {n_bast} BAST/BA Rekonsiliasi — selisih "
                       f"{gap} periode.",
            "kriteria": "PMK 190/2012 tentang Pembayaran APBN — setiap pembayaran atas jasa harus "
                        "didukung BAST sebagai bukti penyelesaian pekerjaan.",
        }
    )


def rule_pm2_laporan_bulanan_tidak_lengkap(digest):
    """PM.2 — Jumlah laporan bulanan < jumlah bulan yang lewat dalam periode kontrak."""
    n_laporan = len(digest.get("dokumen", {}).get("laporan_bulanan", []))
    kontrak = _parsed(_first(digest, "kontrak"))
    if not kontrak:
        return None
    # heuristik: cek periode kontrak dari parse_kontrak (belum diimplementasi —
    # fallback: flag jika n_laporan < 3 pada pengadaan berjangka waktu panjang)
    if n_laporan == 0:
        return _rule(
            "PM.2", PERINGATAN, "Pelaksanaan",
            "Laporan bulanan tidak ditemukan di folder penugasan",
            "Pengadaan jasa berjangka waktu seharusnya memiliki laporan bulanan.",
            bukti={"n_laporan": 0, "kontrak": kontrak.get("nomor")},
            draft={
                "kondisi": "Tim pemantauan tidak menemukan laporan bulanan penyedia di folder "
                           "penugasan. Kontrak jasa berjangka waktu seharusnya disertai laporan "
                           "bulanan sebagai bahan pemantauan progres.",
                "kriteria": "Perpres 16/2018 Pasal 50 — kewajiban pelaporan progres oleh penyedia; "
                            "SSUKSSKK klausul pelaporan bulanan.",
            }
        )
    return None


def rule_pm3_addendum_tidak_dokumentatif(digest):
    """PM.3 — Terdapat amandemen/addendum kontrak tapi dokumen adendum tidak lengkap."""
    # heuristik: cek raw_first_chars dari kontrak untuk kata "addendum" / "amandemen"
    kontrak_entry = _first(digest, "kontrak")
    if not kontrak_entry:
        return None
    raw = (kontrak_entry.get("parsed") or {}).get("_raw_first_chars", "") or ""
    if not re.search(r"addendum|amandemen", raw, re.I):
        return None
    # cek ada dokumen terpisah addendum di folder
    unc = digest.get("unclassified_files", []) or []
    has_addendum_file = any("addendum" in f.lower() or "amandemen" in f.lower() for f in unc)
    if has_addendum_file:
        return None
    return _rule(
        "PM.3", PERINGATAN, "Kontrak",
        "Kontrak menyebut addendum/amandemen namun dokumen addendum terpisah tidak ditemukan",
        "Addendum kontrak harus didokumentasikan secara terpisah.",
        bukti={"kontrak": kontrak_entry.get("filename")},
        draft={
            "kondisi": "Teks kontrak menyebut keberadaan addendum/amandemen, namun dokumen "
                       "addendum terpisah dan terdokumentasi tidak ditemukan di folder penugasan.",
            "kriteria": "Perpres 16/2018 Pasal 54 — amandemen kontrak harus dituangkan dalam "
                        "dokumen tertulis yang ditandatangani para pihak.",
        }
    )


def rule_pm4_kontrak_tanpa_laporan(digest):
    """PM.4 — Kontrak + pembayaran berjalan tapi tidak ada laporan pemantauan apapun."""
    kontrak = _first(digest, "kontrak")
    pembayaran = _first(digest, "pembayaran_ls") or _first(digest, "sptb")
    bast = _first(digest, "ba_rekonsiliasi")
    if not (kontrak and pembayaran):
        return None
    # sudah ada BAST/rekonsiliasi?
    if bast:
        return None
    return _rule(
        "PM.4", KRITIS, "Pelaksanaan",
        "Pembayaran dilakukan namun BAST/BA Rekonsiliasi belum diterbitkan",
        "Pembayaran tanpa BAST adalah red flag untuk pemantauan pengadaan.",
        bukti={"pembayaran": pembayaran.get("filename"), "kontrak": kontrak.get("filename")},
        draft={
            "kondisi": "Pembayaran atas jasa telah dilakukan, namun BAST atau BA Rekonsiliasi "
                       "sebagai bukti penyelesaian pekerjaan periode tidak ditemukan.",
            "kriteria": "PMK 190/2012 — pembayaran atas jasa wajib didukung BAST; SSUKSSKK "
                        "klausul serah terima pekerjaan.",
        }
    )


def rule_pm5_kontrak_tanpa_sla_monitoring(digest):
    """PM.5 — Kontrak ada klausul SLA tapi tidak ada BA Rekonsiliasi SLA."""
    kontrak = _parsed(_first(digest, "kontrak"))
    bast = _parsed(_first(digest, "ba_rekonsiliasi"))
    if not kontrak or not kontrak.get("sla_clause"):
        return None
    if bast and bast.get("sla_reported"):
        return None
    return _rule(
        "PM.5", PERINGATAN, "Pelaksanaan",
        "Kontrak memuat klausul SLA namun tidak ada laporan SLA aktual dari BA Rekonsiliasi",
        "SLA monitoring tidak dapat dilakukan tanpa laporan aktual.",
        bukti={"sla_kontrak": kontrak.get("sla_value"), "sla_reported": bast.get("sla_reported") if bast else None},
        draft={
            "kondisi": f"Kontrak mencantumkan SLA {kontrak.get('sla_value') or '—'}, namun "
                       f"BA Rekonsiliasi tidak memuat laporan SLA aktual yang dapat dibandingkan "
                       f"dengan komitmen.",
            "kriteria": "Perpres 16/2018 Pasal 52 — kinerja penyedia harus dimonitor dan "
                        "diukur terhadap klausul SLA dalam kontrak.",
        }
    )


ALL_RULES = [
    rule_pm1_progres_fisik_vs_keuangan,
    rule_pm2_laporan_bulanan_tidak_lengkap,
    rule_pm3_addendum_tidak_dokumentatif,
    rule_pm4_kontrak_tanpa_laporan,
    rule_pm5_kontrak_tanpa_sla_monitoring,
]


def run_checks(digest):
    out = []
    for fn in ALL_RULES:
        try:
            r = fn(digest)
            if r: out.append(r)
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
    ap.add_argument("digest_json")
    ap.add_argument("-o", "--output", default="anomalies.json")
    args = ap.parse_args(argv)
    digest = json.loads(Path(args.digest_json).read_text(encoding="utf-8"))
    anomalies = run_checks(digest)
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
    print(f"=== PEMANTAUAN-PENGADAAN ===")
    print(f"Tested {len(ALL_RULES)} rules; Found {len(anomalies)} anomalies")
    for a in anomalies:
        print(f"  [{a.get('severity','?'):11s}] {a.get('rule_id','?'):6s} -- {a.get('judul','?')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
