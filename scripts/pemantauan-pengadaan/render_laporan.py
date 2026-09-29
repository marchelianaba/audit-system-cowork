"""
render_laporan.py — Render anomalies + context.md → draft Laporan Hasil Pemantauan.

Laporan Pemantauan lebih ringkas dari LHA — bersifat observasi, tanpa
analisis Sebab atau Rekomendasi formal. Struktur:
  - Nota Dinas Pengantar
  - Cover Laporan
  - Ringkasan Observasi
  - Dasar Hukum, Tujuan, Ruang Lingkup
  - Hasil Pemantauan (per aspek: Pelaksanaan, Kontrak)
  - Kesimpulan

Usage:
    python render_laporan.py <anomalies.json> <context.md> [-o Laporan.docx]
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
try:
    from docx import Document
    from docx.shared import Pt, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    sys.exit("ERROR: python-docx not installed.")


def _parse_context_md(path):
    if not path.exists(): return {}
    out = {}
    for m in re.finditer(r"^([A-Z][A-Za-z\s]+?)\s*:\s*(.+?)$",
                          path.read_text(encoding="utf-8"), re.M):
        out[m.group(1).strip()] = m.group(2).strip()
    return out


def _h(doc, text, size=12, align=None):
    p = doc.add_paragraph()
    r = p.add_run(text); r.bold = True; r.font.size = Pt(size)
    if align: p.alignment = align


def _p(doc, text, bold=False, italic=False, size=11, align=None, indent=None, justify=False):
    p = doc.add_paragraph()
    if indent: p.paragraph_format.left_indent = Cm(indent)
    if justify: p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if align: p.alignment = align
    r = p.add_run(text); r.bold = bold; r.italic = italic; r.font.size = Pt(size)


def render_laporan(anomalies_path, context_path, output_path):
    anom = json.loads(Path(anomalies_path).read_text(encoding="utf-8"))
    ctx = _parse_context_md(Path(context_path))
    anomalies = [a for a in anom.get("anomalies", []) if a.get("severity") != "ERROR"]

    doc = Document()
    for s in doc.sections:
        s.page_height = Cm(29.7); s.page_width = Cm(21.0)
        s.top_margin = s.bottom_margin = Cm(2.2)
        s.left_margin = s.right_margin = Cm(2.5)
    doc.styles["Normal"].font.name = "Times New Roman"
    doc.styles["Normal"].font.size = Pt(11)

    obyek = ctx.get("Obyek", "[Obyek Pengadaan]")
    unit = ctx.get("Unit yang Diawasi", "[Unit]")
    nomor_st = ctx.get("Nomor ST", "[Nomor ST]")
    tgl_st = ctx.get("Tanggal ST", "[Tanggal ST]")
    penerima = ctx.get("Penerima Laporan", "[Penerima]")

    # Nota Dinas
    for l in ["KEMENTERIAN KOMUNIKASI DAN DIGITAL RI", "INSPEKTORAT JENDERAL", "INSPEKTORAT II"]:
        _p(doc, l, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=12)
    _p(doc, "Jl. Medan Merdeka Barat No. 9, Jakarta 10110",
       align=WD_ALIGN_PARAGRAPH.CENTER, size=9, italic=True)
    doc.add_paragraph()
    _h(doc, "NOTA DINAS", size=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    _p(doc, "Nomor: [DIISI AUDITOR]/IJ.3/PW.04.06/[bulan]/[tahun]",
       align=WD_ALIGN_PARAGRAPH.CENTER, size=10)
    doc.add_paragraph()

    fields = [
        ("Kepada Yth.", penerima),
        ("Dari", "Inspektur II"),
        ("Hal", f"Laporan Hasil Pemantauan Pengadaan — {obyek}"),
        ("Klasifikasi", "Terbatas"),
        ("Lampiran", "Satu laporan"),
        ("Tanggal", "[DIISI AUDITOR]"),
    ]
    t = doc.add_table(rows=len(fields), cols=3); t.autofit = False
    for row in t.rows:
        row.cells[0].width = Cm(3.0); row.cells[1].width = Cm(0.5); row.cells[2].width = Cm(13.0)
    for i, (k, v) in enumerate(fields):
        for j, val in enumerate([k, ":", v]):
            c = t.rows[i].cells[j]; c.text = ""
            r = c.paragraphs[0].add_run(val); r.font.size = Pt(11)
            if j == 0: r.bold = True
    doc.add_paragraph()
    _p(doc,
       f"Menindaklanjuti Surat Tugas Inspektur II Nomor {nomor_st} tanggal {tgl_st} "
       f"perihal pemantauan pengadaan atas {obyek} di {unit}, bersama ini kami sampaikan "
       f"Laporan Hasil Pemantauan sebagaimana terlampir. Sebagai catatan, pemantauan "
       f"bersifat observasi atas progres pengadaan yang sedang berjalan; rekomendasi "
       f"tindak lanjut akan dirumuskan bersama auditan dalam forum tersendiri.",
       justify=True)
    doc.add_paragraph()
    _p(doc, "[TTD — DIISI AUDITOR]", align=WD_ALIGN_PARAGRAPH.RIGHT, size=10, italic=True)
    _p(doc, "Muhammad Arief", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    _p(doc, "Inspektur II", align=WD_ALIGN_PARAGRAPH.RIGHT, size=10)
    doc.add_page_break()

    # Cover
    for l in ["KEMENTERIAN KOMUNIKASI DAN DIGITAL RI", "INSPEKTORAT JENDERAL"]:
        _p(doc, l, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=12)
    doc.add_paragraph()
    _p(doc, "LAPORAN HASIL PEMANTAUAN", bold=True,
       align=WD_ALIGN_PARAGRAPH.CENTER, size=14)
    _p(doc, "PENGADAAN BARANG/JASA", bold=True,
       align=WD_ALIGN_PARAGRAPH.CENTER, size=14)
    doc.add_paragraph()
    _p(doc, obyek.upper(), bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=13)
    _p(doc, unit.upper(), bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=12)
    doc.add_page_break()

    # 1. Ringkasan Observasi
    _h(doc, "1. RINGKASAN OBSERVASI", size=12)
    n = len(anomalies)
    _p(doc,
       f"Inspektorat II telah melakukan pemantauan atas pelaksanaan pengadaan {obyek} di "
       f"{unit}. Pemantauan bersifat observasi — memotret kondisi aktual tanpa analisis "
       f"akar masalah. Teridentifikasi {n} catatan observasi yang perlu diperhatikan oleh "
       f"unit kerja dalam mengawal sisa pelaksanaan kontrak.",
       justify=True)

    # 2. Dasar Hukum
    doc.add_paragraph()
    _h(doc, "2. DASAR HUKUM", size=12)
    for item in [
        "a. Peraturan Pemerintah Nomor 60 Tahun 2008 tentang Sistem Pengendalian Intern Pemerintah;",
        "b. Peraturan Presiden Nomor 16 Tahun 2018 jo. Perpres 12/2021 dan Perpres 46/2025 tentang Pengadaan Barang/Jasa Pemerintah;",
        "c. Peraturan Menteri Keuangan Nomor 190/PMK.05/2012 tentang Tata Cara Pembayaran atas Beban APBN;",
        f"d. Surat Tugas Inspektur II Nomor {nomor_st} tanggal {tgl_st}.",
    ]:
        _p(doc, item, indent=0.5, justify=True)

    # 3. Tujuan
    doc.add_paragraph()
    _h(doc, "3. TUJUAN PEMANTAUAN", size=12)
    _p(doc,
       "Tujuan pemantauan adalah memotret progres pelaksanaan pengadaan sebagai deteksi "
       "dini atas potensi permasalahan, tanpa memberi keyakinan formal atas kepatuhan "
       "penuh. Hasil pemantauan menjadi basis pertimbangan bagi auditor internal dan "
       "unit kerja untuk melakukan tindak lanjut sebelum audit penuh.",
       justify=True)

    # 4. Ruang Lingkup
    doc.add_paragraph()
    _h(doc, "4. RUANG LINGKUP", size=12)
    _p(doc,
       f"Pemantauan mencakup dokumen kontrak, laporan bulanan, BAST/BA Rekonsiliasi, dan "
       f"bukti pembayaran pengadaan {obyek} yang berada di folder penugasan sampai "
       f"tanggal pemantauan. Pemantauan tidak mencakup pengujian kepatuhan menyeluruh "
       f"atau perhitungan kerugian negara.",
       justify=True)

    # 5. Hasil Pemantauan
    doc.add_paragraph()
    _h(doc, "5. HASIL PEMANTAUAN", size=12)
    per_aspek = {}
    for a in anomalies:
        per_aspek.setdefault(a.get("aspek", "?"), []).append(a)
    for aspek, items in per_aspek.items():
        _h(doc, f"5.{aspek[0]}. Aspek {aspek}", size=11)
        for a in items:
            _p(doc, f"{a.get('rule_id','?')}. {a.get('judul','?')}", bold=True, size=11)
            draft = a.get("draft_catatan") or {}
            for label, key in [("Kondisi", "kondisi"), ("Kriteria", "kriteria")]:
                val = draft.get(key)
                if val:
                    p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(0.5)
                    r = p.add_run(f"{label}: "); r.bold = True; r.font.size = Pt(10)
                    r2 = p.add_run(val); r2.font.size = Pt(10)

    # 6. Kesimpulan
    doc.add_paragraph()
    _h(doc, "6. KESIMPULAN", size=12)
    _p(doc,
       f"Terdapat {n} catatan observasi yang perlu diperhatikan unit kerja dalam mengawal "
       f"sisa pelaksanaan pengadaan. Pemantauan ini bukan audit — hasilnya tidak memberikan "
       f"keyakinan formal atas kepatuhan. Catatan observasi ini dapat menjadi bahan "
       f"pertimbangan bagi unit kerja untuk tindak lanjut mandiri dan bagi auditor internal "
       f"apabila audit penuh dilaksanakan pada pengadaan ini.",
       justify=True)

    doc.add_paragraph()
    _p(doc, "[TTD — DIISI AUDITOR]", align=WD_ALIGN_PARAGRAPH.RIGHT, size=10, italic=True)
    _p(doc, "Inspektur II,", align=WD_ALIGN_PARAGRAPH.RIGHT, size=10)
    _p(doc, "Muhammad Arief", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path, len(anomalies)


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
    ap.add_argument("anomalies")
    ap.add_argument("context")
    ap.add_argument("-o", "--output", default="Laporan-Pemantauan-DRAFT.docx")
    args = ap.parse_args(argv)
    out, n = render_laporan(Path(args.anomalies), Path(args.context), Path(args.output))
    print(f"OK — written: {out}")
    print(f"   Catatan observasi ter-render: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
