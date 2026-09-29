"""
render_lhe.py — Render anomalies + lke.json + context.md → draft LHE SPIP.

Struktur LHE SPIP (sesuai PerBPKP 5/2021 + Template Laporan Hasil Penjaminan
Kualitas Pelaksanaan SPIP):
  - Nota Dinas Pengantar
  - Cover LHE
  - Ringkasan Eksekutif (nilai maturitas + kategori level 1-5)
  - Dasar Hukum (PP 60/2008, PerBPKP 5/2021)
  - Tujuan, Ruang Lingkup, Metodologi
  - Hasil Evaluasi per 3 Komponen (Penetapan Tujuan, Struktur, Pencapaian)
  - Area of Improvement per Unsur SPIP
  - Kesimpulan & Peta Jalan Peningkatan Maturitas

Usage:
    python render_lhe.py <anomalies.json> <context.md> --lke <lke.json> [-o LHE.docx]
"""

from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    sys.exit("ERROR: python-docx not installed. Run: pip install python-docx")


LEVEL_MATURITAS = [
    (4.5, 5, "Optimum"),
    (3.5, 4, "Terdefinisi"),
    (2.5, 3, "Terintegrasi"),
    (1.5, 2, "Berkembang"),
    (0,   1, "Rintisan"),
]


def _kategori_maturitas(nilai):
    if nilai is None:
        return ("—", "—")
    for threshold, level, label in LEVEL_MATURITAS:
        if nilai >= threshold:
            return (f"Level {level}", label)
    return ("Level 1", "Rintisan")


def _parse_context_md(path):
    if not path.exists():
        return {}
    out = {}
    for m in re.finditer(r"^([A-Z][A-Za-z\s]+?)\s*:\s*(.+?)$",
                         path.read_text(encoding="utf-8"), re.M):
        out[m.group(1).strip()] = m.group(2).strip()
    return out


def _h(doc, text, size=12, align=None):
    p = doc.add_paragraph()
    r = p.add_run(text); r.bold = True; r.font.size = Pt(size)
    if align: p.alignment = align
    return p


def _p(doc, text, bold=False, italic=False, size=11, align=None, indent=None, justify=False):
    p = doc.add_paragraph()
    if indent: p.paragraph_format.left_indent = Cm(indent)
    if justify: p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if align: p.alignment = align
    r = p.add_run(text); r.bold = bold; r.italic = italic; r.font.size = Pt(size)
    return p


def render_lhe_spip(anomalies_path, context_path, lke_path, output_path):
    anom = json.loads(Path(anomalies_path).read_text(encoding="utf-8"))
    ctx = _parse_context_md(Path(context_path))
    lke = json.loads(Path(lke_path).read_text(encoding="utf-8")) if lke_path and Path(lke_path).exists() else {}
    anomalies = [a for a in anom.get("anomalies", []) if a.get("severity") != "ERROR"]

    doc = Document()
    for s in doc.sections:
        s.page_height = Cm(29.7); s.page_width = Cm(21.0)
        s.top_margin = s.bottom_margin = Cm(2.2)
        s.left_margin = s.right_margin = Cm(2.5)
    doc.styles["Normal"].font.name = "Times New Roman"
    doc.styles["Normal"].font.size = Pt(11)

    obyek = ctx.get("Obyek") or "Kementerian Komunikasi dan Digital"
    unit = ctx.get("Unit yang Diawasi") or "Kementerian Komunikasi dan Digital"
    nomor_st = ctx.get("Nomor ST", "[Nomor ST]")
    tgl_st = ctx.get("Tanggal ST", "[Tanggal ST]")
    penerima = ctx.get("Penerima Laporan", "Sekretaris Jenderal")
    tahun = None
    m = re.search(r"\b(202\d)\b", str(lke.get("metadata", {}).get("source_file") or "") + obyek)
    tahun = m.group(1) if m else "[TAHUN]"

    # nilai maturitas — hitung dari unsur komponen × bobot
    total_maturitas = 0
    valid = True
    for k in lke.get("unsur", []) or []:
        nilai_k = k.get("sub_jumlah_nilai")
        bobot_k = k.get("bobot_komponen")
        if nilai_k is not None and bobot_k is not None:
            total_maturitas += nilai_k * bobot_k
        else:
            valid = False
    if not valid:
        total_maturitas = None
    level_kode, level_label = _kategori_maturitas(total_maturitas)

    # ========== Nota Dinas ==========
    for l in ["KEMENTERIAN KOMUNIKASI DAN DIGITAL RI", "INSPEKTORAT JENDERAL"]:
        _p(doc, l, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=12)
    _p(doc, "Jl. Medan Merdeka Barat No. 9, Jakarta 10110",
       align=WD_ALIGN_PARAGRAPH.CENTER, size=9, italic=True)
    doc.add_paragraph()
    _h(doc, "NOTA DINAS", size=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    _p(doc, "Nomor: [DIISI AUDITOR]/IJ/PW.04.05/[bulan]/[tahun]",
       align=WD_ALIGN_PARAGRAPH.CENTER, size=10)
    doc.add_paragraph()

    fields = [
        ("Kepada Yth.", penerima),
        ("Dari", "Inspektur Jenderal"),
        ("Hal", f"Penyampaian Laporan Hasil Penjaminan Kualitas Pelaksanaan SPIP {unit} Tahun {tahun}"),
        ("Klasifikasi", "Terbatas"),
        ("Lampiran", "Satu laporan"),
        ("Tanggal", "[DIISI AUDITOR]"),
    ]
    t = doc.add_table(rows=len(fields), cols=3)
    t.autofit = False
    for row in t.rows:
        row.cells[0].width = Cm(3.0); row.cells[1].width = Cm(0.5); row.cells[2].width = Cm(13.0)
    for i, (k, v) in enumerate(fields):
        for j, val in enumerate([k, ":", v]):
            c = t.rows[i].cells[j]; c.text = ""
            r = c.paragraphs[0].add_run(val); r.font.size = Pt(11)
            if j == 0: r.bold = True
    doc.add_paragraph()

    if total_maturitas is not None:
        _p(doc,
           f"Sesuai Peraturan Badan Pengawasan Keuangan dan Pembangunan Nomor 5 Tahun 2021 "
           f"tentang Penilaian Maturitas Penyelenggaraan SPIP, Inspektorat Jenderal telah "
           f"melaksanakan penjaminan kualitas (quality assurance) atas hasil penilaian mandiri "
           f"maturitas SPIP {unit} Tahun {tahun}.",
           justify=True)
        _p(doc,
           f"Berdasarkan hasil penjaminan kualitas, nilai maturitas SPIP {unit} adalah "
           f"**{total_maturitas:.2f}** — {level_kode} ({level_label}). "
           f"Terdapat {len(anomalies)} Area of Improvement (AoI) yang perlu ditindaklanjuti "
           f"untuk peningkatan maturitas pada periode berikutnya.",
           justify=True)
    else:
        _p(doc,
           f"Inspektorat Jenderal telah melaksanakan penjaminan kualitas atas penilaian mandiri "
           f"maturitas SPIP {unit} Tahun {tahun}. Terdapat {len(anomalies)} AoI yang disampaikan "
           f"pada laporan terlampir.",
           justify=True)
    doc.add_paragraph()
    _p(doc, "[TTD — DIISI AUDITOR]", align=WD_ALIGN_PARAGRAPH.RIGHT, size=10, italic=True)
    _p(doc, "Arief Tri Hardiyanto", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    _p(doc, "Inspektur Jenderal", align=WD_ALIGN_PARAGRAPH.RIGHT, size=10)
    doc.add_page_break()

    # ========== Cover LHE SPIP ==========
    for l in ["KEMENTERIAN KOMUNIKASI DAN DIGITAL RI", "INSPEKTORAT JENDERAL"]:
        _p(doc, l, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=12)
    doc.add_paragraph()
    _p(doc, "LAPORAN HASIL PENJAMINAN KUALITAS", bold=True,
       align=WD_ALIGN_PARAGRAPH.CENTER, size=14)
    _p(doc, "PELAKSANAAN SISTEM PENGENDALIAN INTERN PEMERINTAH (SPIP)", bold=True,
       align=WD_ALIGN_PARAGRAPH.CENTER, size=14)
    doc.add_paragraph()
    _p(doc, unit.upper(), bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=13)
    _p(doc, f"TAHUN {tahun}", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=13)
    doc.add_paragraph()
    _p(doc, "Nomor: B-[DIISI AUDITOR]/IJ/PW.04.05/[bulan]/[tahun]",
       align=WD_ALIGN_PARAGRAPH.CENTER, size=10)
    _p(doc, "Tanggal: [DIISI AUDITOR]", align=WD_ALIGN_PARAGRAPH.CENTER, size=10)
    doc.add_page_break()

    # ========== 1. Ringkasan Eksekutif ==========
    _h(doc, "1. RINGKASAN EKSEKUTIF", size=12)
    if total_maturitas is not None:
        _p(doc,
           f"Inspektorat Jenderal Kementerian Komunikasi dan Digital telah melaksanakan "
           f"penjaminan kualitas atas penilaian mandiri maturitas SPIP pada {unit} Tahun {tahun}. "
           f"Penilaian dilakukan terhadap 3 komponen SPIP (Penetapan Tujuan bobot 0,4; "
           f"Struktur dan Proses bobot 0,3; Pencapaian Tujuan SPIP bobot 0,3) mengikuti "
           f"Peraturan BPKP 5/2021.",
           justify=True)
        _p(doc,
           f"Berdasarkan penjaminan kualitas, {unit} memperoleh nilai maturitas SPIP "
           f"{total_maturitas:.2f} — {level_kode} ({level_label}). "
           f"Target K/L untuk maturitas minimal Level 3 (Terintegrasi).",
           justify=True)
    # rincian per komponen
    _p(doc, ""); _p(doc, "Rincian nilai per komponen:", bold=True)
    for k in lke.get("unsur", []) or []:
        nilai_k = k.get("sub_jumlah_nilai") or 0
        bobot_k = k.get("bobot_komponen") or 0
        _p(doc, f"  • {k['nama_komponen']}: nilai {nilai_k:.2f} × bobot {bobot_k} = "
           f"{(nilai_k * bobot_k):.3f}", indent=0.3)
    _p(doc, "")
    _p(doc,
       f"Terdapat {len(anomalies)} Area of Improvement (AoI) yang perlu ditindaklanjuti "
       f"untuk peningkatan maturitas periode berikutnya.",
       justify=True)

    # ========== 2. Dasar Hukum ==========
    doc.add_paragraph()
    _h(doc, "2. DASAR HUKUM", size=12)
    for item in [
        "a. Peraturan Pemerintah Nomor 60 Tahun 2008 tentang Sistem Pengendalian Intern Pemerintah;",
        "b. Peraturan Badan Pengawasan Keuangan dan Pembangunan Nomor 5 Tahun 2021 tentang Penilaian Maturitas Penyelenggaraan Sistem Pengendalian Intern Pemerintah Terintegrasi pada Kementerian/Lembaga dan Pemerintah Daerah;",
        f"c. Surat Tugas Inspektur Jenderal Nomor {nomor_st} tanggal {tgl_st}.",
    ]:
        _p(doc, item, indent=0.5, justify=True)

    # ========== 3. Tujuan ==========
    doc.add_paragraph()
    _h(doc, "3. TUJUAN PENJAMINAN KUALITAS", size=12)
    _p(doc,
       "Tujuan penjaminan kualitas adalah: (a) memvalidasi hasil penilaian mandiri maturitas "
       "SPIP yang disusun oleh unit kerja; (b) memberikan keyakinan atas reliabilitas nilai "
       "maturitas untuk pelaporan ke BPKP; (c) mengidentifikasi Area of Improvement per unsur "
       "SPIP untuk peta jalan peningkatan maturitas.",
       justify=True)

    # ========== 4. Ruang Lingkup ==========
    doc.add_paragraph()
    _h(doc, "4. RUANG LINGKUP", size=12)
    _p(doc,
       f"Penjaminan kualitas mencakup 3 komponen SPIP pada {unit} Tahun {tahun}: "
       f"(1) Penetapan Tujuan — 2 subunsur (Kualitas Sasaran Strategis, Kualitas Strategi "
       f"Pencapaian Sasaran); (2) Struktur dan Proses — 25 subunsur mencakup 5 unsur utama "
       f"(Lingkungan Pengendalian, Penilaian Risiko, Kegiatan Pengendalian, Informasi dan "
       f"Komunikasi, Pemantauan); (3) Pencapaian Tujuan SPIP — 4E (Efektivitas/Efisiensi, "
       f"Keandalan Laporan Keuangan, Pengamanan Aset, Ketaatan Peraturan).",
       justify=True)

    # ========== 5. Metodologi ==========
    doc.add_paragraph()
    _h(doc, "5. METODOLOGI", size=12)
    _p(doc,
       "Penjaminan kualitas dilaksanakan dengan: (a) pre-digest LKE Excel menggunakan "
       "pipeline deterministik — ekstraksi 3 komponen dan 27+ subunsur; (b) cross-check "
       "rule-based atas kelengkapan bobot, gap Penilaian Mandiri (PM) vs Penilaian Kualitas "
       "(PK), subunsur bernilai rendah, dan maturitas total; (c) verifikasi bukti dukung "
       "pada subunsur yang di-flag; (d) konfirmasi kepada unit kerja atas AoI yang "
       "teridentifikasi.",
       justify=True)

    # ========== 6. Hasil Evaluasi per Komponen ==========
    doc.add_paragraph()
    _h(doc, "6. HASIL EVALUASI PER KOMPONEN", size=12)
    for k in lke.get("unsur", []) or []:
        komp_nama = k["nama_komponen"]
        nilai_k = k.get("sub_jumlah_nilai") or 0
        bobot_k = k.get("bobot_komponen") or 0
        subs = k.get("unsur", []) or []
        _h(doc, f"6.{komp_nama[:30]}. {komp_nama} (Bobot {bobot_k}, Nilai {nilai_k:.2f})", size=11)
        if subs:
            t = doc.add_table(rows=len(subs)+1, cols=4)
            t.autofit = False
            for j, h in enumerate(["No", "Subunsur", "Skor PK", "Bobot Unsur"]):
                c = t.rows[0].cells[j]; c.text = ""
                r = c.paragraphs[0].add_run(h); r.bold = True; r.font.size = Pt(10)
            for i, sub in enumerate(subs, start=1):
                vals = [str(i), sub.get("nama", "")[:80],
                        f"{sub.get('skor_pk') or 0:.2f}" if sub.get("skor_pk") is not None else "—",
                        str(sub.get("bobot_unsur") or "—")]
                for j, v in enumerate(vals):
                    c = t.rows[i].cells[j]; c.text = ""
                    r = c.paragraphs[0].add_run(v); r.font.size = Pt(9)

    # ========== 7. AoI per Unsur ==========
    doc.add_paragraph()
    _h(doc, "7. AREA OF IMPROVEMENT (AoI)", size=12)
    if anomalies:
        _p(doc, f"Terdapat {len(anomalies)} AoI yang teridentifikasi dari hasil penjaminan kualitas:",
           justify=True)
        for a in anomalies:
            _p(doc, f"{a.get('rule_id','?')}. {a.get('judul','?')}", bold=True)
            draft = a.get("draft_catatan") or {}
            for label, key in [("Kondisi", "kondisi"), ("Kriteria", "kriteria"),
                                ("Akibat", "akibat")]:
                val = draft.get(key)
                if val:
                    p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(0.5)
                    r = p.add_run(f"{label}: "); r.bold = True; r.font.size = Pt(10)
                    r2 = p.add_run(val); r2.font.size = Pt(10)
    else:
        _p(doc, "Tidak terdapat AoI yang memerlukan tindak lanjut khusus.", justify=True)

    # ========== 8. Kesimpulan ==========
    doc.add_paragraph()
    _h(doc, "8. KESIMPULAN DAN PETA JALAN PENINGKATAN", size=12)
    if total_maturitas is not None:
        _p(doc,
           f"Nilai maturitas SPIP {unit} Tahun {tahun} adalah {total_maturitas:.2f} — "
           f"{level_kode} ({level_label}). "
           f"Untuk mencapai level {'optimum' if total_maturitas >= 3.5 else 'terdefinisi' if total_maturitas >= 2.5 else 'terintegrasi'}, "
           f"unit kerja perlu menindaklanjuti {len(anomalies)} AoI di atas dengan "
           f"memprioritaskan perbaikan pada subunsur dengan skor terendah.",
           justify=True)
    _p(doc,
       "Peta jalan peningkatan maturitas direkomendasikan dikonsolidasikan dalam dokumen "
       "tersendiri dengan memperhatikan prioritas dan sumber daya yang tersedia. "
       "[Rumusan peta jalan final — DIISI AUDITOR]",
       justify=True, italic=True)

    doc.add_paragraph()
    _p(doc, "[TTD — DIISI AUDITOR]", align=WD_ALIGN_PARAGRAPH.RIGHT, size=10, italic=True)
    _p(doc, "Inspektur Jenderal,", align=WD_ALIGN_PARAGRAPH.RIGHT, size=10)
    _p(doc, "Arief Tri Hardiyanto", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path, len(anomalies), total_maturitas, level_kode


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
    ap.add_argument("--lke", default=None)
    ap.add_argument("-o", "--output", default="LHE-SPIP-DRAFT.docx")
    args = ap.parse_args(argv)
    out, n, nilai, level = render_lhe_spip(
        Path(args.anomalies), Path(args.context),
        Path(args.lke) if args.lke else None, Path(args.output)
    )
    print(f"OK — written: {out}")
    print(f"   AoI ter-render: {n}")
    if nilai is not None:
        print(f"   Maturitas: {nilai:.2f} ({level})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
