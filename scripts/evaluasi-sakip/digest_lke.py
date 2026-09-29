"""
digest_lke.py — Parser LKE SAKIP/AKIP Excel (v0.2).

Struktur LKE SAKIP yang diparse (berdasarkan LKE DJED 2025 APIP Komdigi):
  - Sheet "LKE" dengan header di row 6-7
  - Hierarki: Komponen (1) → Subkomponen (1.a) → Kriteria (1), 2), ...)
  - Kolom: NAMA (A-D), BOBOT (E), NILAI MANDIRI (F,G), NILAI AKIP (J),
           EVALUASI APIP (M-R), CATATAN EVALUATOR (T), REKOMENDASI EVALUATOR (U)

Output:
  {
    "metadata": {...},
    "komponen": [
      { "no": "1", "nama": "Perencanaan Kinerja", "bobot": 30,
        "subkomponen": [
          { "no": "1.a", "nama": "...", "bobot": 6,
            "nilai_mandiri_persen": "100.00%",
            "nilai_mandiri_nilai": 6, "jawaban_akhir": "BB",
            "kriteria": [
              { "no": "1)", "uraian": "...", "jawaban": "Ya", "nilai": 100, ... }
            ]
          }
        ]
      }
    ],
    "total_nilai_akip": <float>,
    "kategori_akip": <str>,  # A/BB/B/CC/C
    "rekap_apip_notes": [...],
  }

Usage:
    python digest_lke.py <LKE.xlsx> [-o lke.json]
"""

from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

try:
    from openpyxl import load_workbook
except ImportError:
    sys.exit("ERROR: openpyxl not installed. Run: pip install openpyxl")


def _clean(v):
    if v is None:
        return None
    s = str(v).strip()
    return s if s else None


def _parse_number(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return v
    s = str(v).strip()
    if not s:
        return None
    # percent
    if s.endswith("%"):
        try:
            return float(s.rstrip("%").replace(",", "."))
        except ValueError:
            return None
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return None


def digest_sakip_lke(xlsx_path: Path) -> dict:
    wb = load_workbook(xlsx_path, data_only=True)
    if "LKE" not in wb.sheetnames:
        # fallback: pakai sheet pertama
        ws = wb[wb.sheetnames[0]]
    else:
        ws = wb["LKE"]

    out = {
        "metadata": {
            "source_file": xlsx_path.name,
            "parser_version": "v0.2",
            "sheet": ws.title,
            "dimensions": f"{ws.max_row}x{ws.max_column}",
        },
        "komponen": [],
        "rekap": {
            "total_nilai_akip": None,
            "kategori_akip": None,
            "total_nilai_mandiri": None,
        },
    }

    current_komponen = None
    current_subkomponen = None

    # Cari baris "NILAI AKUNTABILITAS KINERJA" untuk total
    for i in range(1, ws.max_row + 1):
        col_a = _clean(ws.cell(row=i, column=1).value)
        col_b = _clean(ws.cell(row=i, column=2).value)
        col_c = _clean(ws.cell(row=i, column=3).value)
        col_d = _clean(ws.cell(row=i, column=4).value)
        col_e = _clean(ws.cell(row=i, column=5).value)  # BOBOT
        col_f = _clean(ws.cell(row=i, column=6).value)  # % Nilai Mandiri
        col_g = _clean(ws.cell(row=i, column=7).value)  # Nilai
        col_h = _clean(ws.cell(row=i, column=8).value)  # Jawaban Akhir
        col_j = _clean(ws.cell(row=i, column=10).value)  # NILAI AKIP Mandiri
        col_m = _clean(ws.cell(row=i, column=13).value)  # Evaluasi APIP %
        col_n = _clean(ws.cell(row=i, column=14).value)  # Evaluasi APIP Nilai
        col_t = _clean(ws.cell(row=i, column=20).value)  # Catatan Evaluator
        col_u = _clean(ws.cell(row=i, column=21).value)  # Rekomendasi Evaluator

        # Total nilai akip
        if col_a and "NILAI AKUNTABILITAS" in col_a.upper():
            out["rekap"]["total_bobot"] = _parse_number(col_e)
            out["rekap"]["total_nilai_mandiri"] = _parse_number(col_g) or _parse_number(col_n)
            # kategori = col_h biasanya
            if col_h:
                out["rekap"]["kategori_akip"] = col_h
            continue

        # Komponen: col_a = digit murni "1", "2", ... col_b = nama komponen
        if col_a and re.fullmatch(r"\d{1,2}", col_a) and col_b:
            komp = {
                "no": col_a,
                "nama": col_b,
                "bobot": _parse_number(col_e),
                "nilai_mandiri_persen": col_f,
                "nilai_mandiri_nilai": _parse_number(col_g),
                "jawaban_akhir_mandiri": col_h,
                "nilai_apip_persen": col_m,
                "nilai_apip_nilai": _parse_number(col_n),
                "catatan_evaluator": col_t,
                "rekomendasi_evaluator": col_u,
                "subkomponen": [],
            }
            out["komponen"].append(komp)
            current_komponen = komp
            current_subkomponen = None
            continue

        # Subkomponen: col_b = "1.a", "1.b", ...
        if col_b and re.fullmatch(r"\d+\.[a-z]", col_b):
            uraian = col_d or col_c or col_b
            sub = {
                "no": col_b,
                "uraian": uraian,
                "bobot": _parse_number(col_e),
                "nilai_mandiri_persen": col_f,
                "nilai_mandiri_nilai": _parse_number(col_g),
                "jawaban_akhir_mandiri": col_h,
                "nilai_apip_persen": col_m,
                "nilai_apip_nilai": _parse_number(col_n),
                "catatan_evaluator": col_t,
                "rekomendasi_evaluator": col_u,
                "kriteria": [],
            }
            if current_komponen:
                current_komponen["subkomponen"].append(sub)
            current_subkomponen = sub
            continue

        # Kriteria: col_c = "1)", "2)", ...
        if col_c and re.fullmatch(r"\d+\)", col_c):
            uraian = col_d or ""
            krit = {
                "no": col_c,
                "uraian": uraian,
                "jawaban_mandiri": col_f,
                "nilai_mandiri": _parse_number(col_g),
                "jawaban_apip": col_m,
                "nilai_apip": _parse_number(col_n),
                "catatan_evaluator": col_t,
            }
            if current_subkomponen:
                current_subkomponen["kriteria"].append(krit)

    return out


def digest_spip_lke(xlsx_path: Path) -> dict:
    """Parser LKE SPIP — multi-sheet, rekap di KKLEAD_SPIP."""
    wb = load_workbook(xlsx_path, data_only=True)
    out = {
        "metadata": {
            "source_file": xlsx_path.name,
            "parser_version": "v0.2",
            "sheets": wb.sheetnames,
        },
        "unsur": [],
        "rekap": {
            "nilai_maturitas_total": None,
            "kategori_maturitas": None,
            "bobot_perencanaan": None,
            "bobot_struktur": None,
            "bobot_hasil": None,
        },
    }

    if "KKLEAD_SPIP" not in wb.sheetnames:
        return out

    ws = wb["KKLEAD_SPIP"]

    current_komponen = None
    for i in range(1, ws.max_row + 1):
        col_c = _clean(ws.cell(row=i, column=3).value)  # Uraian
        col_d = _clean(ws.cell(row=i, column=4).value)  # Skor PM
        col_e = _clean(ws.cell(row=i, column=5).value)  # Skor PK
        col_f = _clean(ws.cell(row=i, column=6).value)  # Bobot Unsur
        col_g = _clean(ws.cell(row=i, column=7).value)  # Bobot Komponen
        col_h = _clean(ws.cell(row=i, column=8).value)  # Nilai Unsur

        if not col_c:
            continue
        upper = col_c.upper()

        # Komponen utama
        seen = [x["nama_komponen"] for x in out["unsur"]]
        if upper in ("PENETAPAN TUJUAN", "STRUKTUR DAN PROSES", "PENCAPAIAN TUJUAN SPIP") and col_c not in seen:
            current_komponen = {
                "nama_komponen": col_c,
                "bobot_komponen": None,
                "unsur": [],
            }
            out["unsur"].append(current_komponen)
            continue

        # Bobot komponen
        if upper.startswith("BOBOT "):
            if current_komponen and _parse_number(col_g):
                current_komponen["bobot_komponen"] = _parse_number(col_g)
            # juga simpan ke rekap
            if "PERENCANAAN" in upper:
                out["rekap"]["bobot_perencanaan"] = _parse_number(col_g)
            elif "STRUKTUR" in upper:
                out["rekap"]["bobot_struktur"] = _parse_number(col_g)
            elif "HASIL" in upper:
                out["rekap"]["bobot_hasil"] = _parse_number(col_g)
            continue

        # Sub jumlah
        if "SUB JUMLAH" in upper:
            if current_komponen:
                current_komponen["sub_jumlah_nilai"] = _parse_number(col_h)
            continue

        # Unsur / subunsur (kalau kedua col_d atau col_e punya nilai)
        if _parse_number(col_e) is not None or _parse_number(col_d) is not None:
            unsur = {
                "nama": col_c,
                "skor_pm": _parse_number(col_d),
                "skor_pk": _parse_number(col_e),
                "bobot_unsur": _parse_number(col_f),
                "nilai_unsur": _parse_number(col_h),
            }
            if current_komponen:
                current_komponen["unsur"].append(unsur)

    # Total nilai maturitas — cari di sheet "Uraian NIlai Setiap Unsur"
    if "Uraian NIlai Setiap Unsur" in wb.sheetnames:
        ws2 = wb["Uraian NIlai Setiap Unsur"]
        subunsur_scores = []
        for i in range(2, ws2.max_row + 1):
            kode = _clean(ws2.cell(row=i, column=1).value)
            nama = _clean(ws2.cell(row=i, column=2).value)
            nilai_2e = _parse_number(ws2.cell(row=i, column=5).value)
            if kode and re.fullmatch(r"\d+\.\d+", kode) and nama and nilai_2e is not None:
                subunsur_scores.append({"kode": kode, "nama": nama[:80],
                                         "nilai_2e": nilai_2e})
        out["subunsur_detail"] = subunsur_scores

    # estimasi total dari rekap (nilai komponen × bobot komponen)
    total = 0
    valid = True
    for k in out["unsur"]:
        nilai = k.get("sub_jumlah_nilai")
        bobot = k.get("bobot_komponen")
        if nilai is not None and bobot is not None:
            total += nilai * bobot
        else:
            valid = False
    if valid and out["unsur"]:
        out["rekap"]["nilai_maturitas_total"] = round(total, 4)
        if total >= 4.5:
            out["rekap"]["kategori_maturitas"] = "Optimum (Level 5)"
        elif total >= 3.5:
            out["rekap"]["kategori_maturitas"] = "Terdefinisi (Level 4)"
        elif total >= 2.5:
            out["rekap"]["kategori_maturitas"] = "Terintegrasi (Level 3)"
        elif total >= 1.5:
            out["rekap"]["kategori_maturitas"] = "Berkembang (Level 2)"
        else:
            out["rekap"]["kategori_maturitas"] = "Rintisan (Level 1)"
    return out


def digest_lke(xlsx_path: Path, jenis: str = "auto") -> dict:
    """Auto-detect SAKIP vs SPIP based on sheet names."""
    wb = load_workbook(xlsx_path, data_only=True)
    if jenis == "auto":
        if "KKLEAD_SPIP" in wb.sheetnames:
            jenis = "spip"
        elif "LKE" in wb.sheetnames:
            jenis = "sakip"
        else:
            jenis = "unknown"
    if jenis == "sakip":
        out = digest_sakip_lke(xlsx_path)
        out["metadata"]["jenis_lke"] = "SAKIP"
    elif jenis == "spip":
        out = digest_spip_lke(xlsx_path)
        out["metadata"]["jenis_lke"] = "SPIP"
    else:
        out = {"metadata": {"source_file": xlsx_path.name, "jenis_lke": "unknown",
                            "sheets": wb.sheetnames}}
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
    ap.add_argument("xlsx")
    ap.add_argument("-o", "--output", default=None)
    ap.add_argument("--jenis", default="auto", choices=["auto", "sakip", "spip"])
    args = ap.parse_args(argv)

    out = digest_lke(Path(args.xlsx), jenis=args.jenis)
    out_path = args.output or str(Path(args.xlsx).with_suffix(".json"))
    Path(out_path).write_text(
        json.dumps(out, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8"
    )
    print(f"OK — written: {out_path}")
    print(f"   Jenis: {out['metadata'].get('jenis_lke')}")
    if out['metadata'].get('jenis_lke') == "SAKIP":
        print(f"   Komponen: {len(out.get('komponen', []))}")
        for k in out.get("komponen", []):
            print(f"     - {k['no']}. {k['nama'][:50]} (bobot={k.get('bobot')}, "
                  f"nilai_mandiri={k.get('nilai_mandiri_nilai')}, nilai_apip={k.get('nilai_apip_nilai')})")
        r = out.get("rekap", {})
        print(f"   Total Nilai AKIP: {r.get('total_nilai_mandiri')} — {r.get('kategori_akip', '—')}")
    elif out['metadata'].get('jenis_lke') == "SPIP":
        print(f"   Komponen: {len(out.get('unsur', []))}")
        for k in out.get("unsur", []):
            print(f"     - {k['nama_komponen']} (bobot={k.get('bobot_komponen')}, "
                  f"sub_jumlah={k.get('sub_jumlah_nilai')}, unsur_count={len(k.get('unsur', []))})")
        r = out.get("rekap", {})
        print(f"   Nilai Maturitas: {r.get('nilai_maturitas_total')} — {r.get('kategori_maturitas', '—')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
