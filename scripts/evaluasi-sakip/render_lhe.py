"""
render_lhe.py — Render anomalies + lke.json + context.md → draft LHE SAKIP.

Struktur mengikuti LHE benchmark (LHE SAKIP Kementerian Komdigi 2025):
  - Nota Dinas Pengantar
  - Cover LHE
  - Ringkasan Eksekutif (nilai AKIP + kategori + rekomendasi ringkas)
  - Dasar Hukum (PP 60/2008, Permenpan 88/2021, Pedoman Irjen 2/2022, ST)
  - Tujuan, Ruang Lingkup, Metodologi Evaluasi
  - Gambaran Umum
  - Hasil Evaluasi per 4 Komponen SAKIP + AoI
  - Kesimpulan & Rekomendasi

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


KOMP_LABELS = {
    "1": "Perencanaan Kinerja",
    "2": "Pengukuran Kinerja",
    "3": "Pelaporan Kinerja",
    "4": "Evaluasi Akuntabilitas Kinerja Internal",
}

KATEGORI_AKIP = [
    (90, "AA", "Sangat Memuaskan"),
    (80, "A",  "Memuaskan"),
    (70, "BB", "Sangat Baik"),
    (60, "B",  "Baik"),
    (50, "CC", "Cukup (Memadai)"),
    (30, "C",  "Kurang"),
    (0,  "D",  "Sangat Kurang"),
]


def _kategori_from_score(nilai: float) -> tuple[str, str]:
    for threshold, kode, label in KATEGORI_AKIP:
        if nilai >= threshold:
            return kode, label
    return "D", "Sangat Kurang"


def _parse_context_md(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"^([A-Z][A-Za-z\s]+?)\s*:\s*(.+?)$", text, re.M):
        out[m.group(1).strip()] = m.group(2).strip()
    return out


def _h(doc, text, size=12, align=None):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(size)
    if align:
        p.alignment = align
    return p


def _p(doc, text, bold=False, italic=False, size=11, align=None, indent=None, justify=False):
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    if justify:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if align:
        p.alignment = align
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.size = Pt(size)
    return p


def render_lhe(anomalies_path, context_path, lke_path, output_path):
    anom = json.loads(Path(anomalies_path).read_text(encoding="utf-8"))
    ctx = _parse_context_md(Path(context_path))
    lke = {}
    if lke_path and Path(lke_path).exists():
        lke = json.loads(Path(lke_path).read_text(encoding="utf-8"))
    anomalies = [a for a in anom.get("anomalies", []) if a.get("severity") != "ERROR"]

    doc = Document()
    for s in doc.sections:
        s.page_height = Cm(29.7); s.page_width = Cm(21.0)
        s.top_margin = s.bottom_margin = Cm(2.2)
        s.left_margin = s.right_margin = Cm(2.5)
    doc.styles["Normal"].font.name = "Times New Roman"
    doc.styles["Normal"].font.size = Pt(11)

    obyek = ctx.get("Obyek") or ctx.get("Unit yang Diawasi") or "[Unit Kerja]"
    unit = ctx.get("Unit yang Diawasi") or obyek
    nomor_st = ctx.get("Nomor ST", "[Nomor ST]")
    tgl_st = ctx.get("Tanggal ST", "[Tanggal ST]")
    penerima = ctx.get("Penerima Laporan", "[Penerima Laporan]")
    tahun = None
    m = re.search(r"\b(202\d)\b", str(lke.get("metadata", {}).get("source_file") or "") + obyek)
    if m:
        tahun = m.group(1)
    if not tahun:
        tahun = "[TAHUN]"

    # hitung total nilai (sum subkomponen nilai_mandiri_nilai × 1 — karena sudah ter-bobot)
    total_nilai = 0
    valid = True
    for k in lke.get("komponen", []) or []:
        for sub in k.get("subkomponen", []) or []:
            n = sub.get("nilai_mandiri_nilai")
            if n is not None:
                total_nilai += n
            else:
                valid = False
    if not valid:
        total_nilai = None
    kategori_kode, kategori_label = ("—", "—")
    if total_nilai is not None:
        kategori_kode, kategori_label = _kategori_from_score(total_nilai)

    # ========== Nota Dinas ==========
    for l in ["KEMENTERIAN KOMUNIKASI DAN DIGITAL RI", "INSPEKTORAT JENDERAL"]:
        _p(doc, l, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=12)
    _p(doc, "Jl. Medan Merdeka Barat No. 9, Jakarta 10110",
       align=WD_ALIGN_PARAGRAPH.CENTER, size=9, italic=True)
    doc.add_paragraph()
    _h(doc, "NOTA DINAS", size=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    _p(doc, "Nomor: [DIISI AUDITOR — dari SIMWAS]/IJ/PW.04.05/[bulan]/[tahun]",
       align=WD_ALIGN_PARAGRAPH.CENTER, size=10)
    doc.add_paragraph()

    fields = [
        ("Kepada Yth.", penerima),
        ("Dari", "Inspektur Jenderal"),
        ("Hal", f"Penyampaian Laporan Hasil Evaluasi Internal atas AKIP {unit} Tahun {tahun}"),
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

    if total_nilai is not None:
        _p(doc,
           f"Sesuai Peraturan Menteri Pendayagunaan Aparatur Negara dan Reformasi Birokrasi "
           f"Nomor 88 Tahun 2021, Inspektorat Jenderal telah melaksanakan evaluasi "
           f"Akuntabilitas Kinerja Instansi Pemerintah (AKIP) pada {unit} Tahun {tahun}.",
           justify=True)
        _p(doc,
           f"Berdasarkan hasil evaluasi, AKIP {unit} memperoleh nilai {total_nilai:.2f} "
           f"dengan predikat \"{kategori_kode}\" ({kategori_label}). Hasil evaluasi "
           f"beserta {len(anomalies)} catatan perbaikan disampaikan pada laporan terlampir.",
           justify=True)
    else:
        _p(doc,
           f"Sesuai Permenpan RB 88/2021, Inspektorat Jenderal telah melaksanakan evaluasi "
           f"AKIP pada {unit} Tahun {tahun}. {len(anomalies)} catatan perbaikan disampaikan "
           f"pada laporan terlampir.",
           justify=True)

    doc.add_paragraph()
    _p(doc, "[TTD — DIISI AUDITOR]", align=WD_ALIGN_PARAGRAPH.RIGHT, size=10, italic=True)
    _p(doc, "Arief Tri Hardiyanto", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)
    _p(doc, "Inspektur Jenderal", align=WD_ALIGN_PARAGRAPH.RIGHT, size=10)
    doc.add_page_break()

    # ========== Cover LHE ==========
    for l in ["KEMENTERIAN KOMUNIKASI DAN DIGITAL RI", "INSPEKTORAT JENDERAL"]:
        _p(doc, l, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=12)
    doc.add_paragraph()
    _p(doc, "LAPORAN HASIL EVALUASI INTERNAL", bold=True,
       align=WD_ALIGN_PARAGRAPH.CENTER, size=14)
    _p(doc, "ATAS AKUNTABILITAS KINERJA INSTANSI PEMERINTAH (AKIP)",
       bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=14)
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
    if total_nilai is not None:
        _p(doc,
           f"Inspektorat Jenderal Kementerian Komunikasi dan Digital telah melaksanakan "
           f"evaluasi atas Akuntabilitas Kinerja Instansi Pemerintah (AKIP) pada {unit} "
           f"Tahun {tahun}. Berdasarkan Lembar Kerja Evaluasi (LKE) yang disusun dengan "
           f"4 komponen utama (Perencanaan Kinerja, Pengukuran Kinerja, Pelaporan Kinerja, "
           f"Evaluasi Akuntabilitas Kinerja Internal), {unit} memperoleh nilai AKIP "
           f"{total_nilai:.2f} dengan predikat \"{kategori_kode}\" ({kategori_label}).",
           justify=True)

    # rincian per komponen
    _p(doc, "")
    _p(doc, "Rincian nilai per komponen:", bold=True)
    for k in lke.get("komponen", []) or []:
        nilai_k = sum(sub.get("nilai_mandiri_nilai") or 0 for sub in k.get("subkomponen", []) or [])
        bobot = k.get("bobot") or 0
        _p(doc, f"  • {k['no']}. {k['nama']}: nilai {nilai_k:.2f} dari bobot {bobot}",
           indent=0.3)

    doc.add_paragraph()
    _p(doc,
       f"Dari hasil evaluasi, terdapat {len(anomalies)} area perbaikan (Area of Improvement / AoI) "
       f"yang perlu ditindaklanjuti untuk meningkatkan implementasi AKIP pada periode berikutnya.",
       justify=True)

    # ========== 2. Dasar Hukum ==========
    doc.add_paragraph()
    _h(doc, "2. DASAR HUKUM", size=12)
    for item in [
        "a. Peraturan Pemerintah Nomor 60 Tahun 2008 tentang Sistem Pengendalian Intern Pemerintah;",
        "b. Peraturan Menteri Pendayagunaan Aparatur Negara dan Reformasi Birokrasi Nomor 88 Tahun 2021 tentang Evaluasi Akuntabilitas Kinerja Instansi Pemerintah;",
        "c. Pedoman Inspektur Jenderal Nomor 2 Tahun 2022 tentang Pedoman Evaluasi Akuntabilitas Kinerja Instansi Pemerintah di lingkup Kementerian Komunikasi dan Digital;",
        f"d. Surat Tugas Inspektur Jenderal Nomor {nomor_st} tanggal {tgl_st}.",
    ]:
        _p(doc, item, indent=0.5, justify=True)

    # ========== 3–5. Tujuan, Ruang Lingkup, Metodologi ==========
    doc.add_paragraph()
    _h(doc, "3. TUJUAN EVALUASI", size=12)
    _p(doc,
       "Tujuan evaluasi adalah: (a) memberikan penilaian atas implementasi Akuntabilitas "
       "Kinerja Instansi Pemerintah sebagai bagian dari Sistem AKIP; (b) memberikan saran "
       "perbaikan yang dapat ditindaklanjuti untuk mendorong peningkatan nilai AKIP "
       "pada periode evaluasi berikutnya.",
       justify=True)

    doc.add_paragraph()
    _h(doc, "4. RUANG LINGKUP EVALUASI", size=12)
    _p(doc,
       f"Evaluasi mencakup seluruh 4 komponen SAKIP pada {unit}: (1) Perencanaan Kinerja, "
       f"(2) Pengukuran Kinerja, (3) Pelaporan Kinerja, dan (4) Evaluasi Akuntabilitas "
       f"Kinerja Internal. Penilaian dilakukan terhadap bukti dukung Tahun {tahun} sesuai "
       f"Lembar Kerja Evaluasi (LKE) yang ditetapkan Permenpan RB 88/2021.",
       justify=True)

    doc.add_paragraph()
    _h(doc, "5. METODOLOGI EVALUASI", size=12)
    _p(doc,
       "Evaluasi dilaksanakan sesuai Standar Audit Intern Pemerintah dengan tahapan: "
       "(a) pre-digest LKE Excel menggunakan pipeline deterministik untuk ekstraksi "
       "struktur komponen-subkomponen-kriteria; (b) cross-check rule-based atas kelengkapan "
       "bobot, catatan evaluator, dan konsistensi PM vs APIP; (c) verifikasi substantif "
       "atas bukti dukung pada subkomponen yang di-flag; (d) konfirmasi kepada unit kerja "
       "atas AoI yang teridentifikasi.",
       justify=True)

    # ========== 6. Hasil Evaluasi per Komponen ==========
    doc.add_paragraph()
    _h(doc, "6. HASIL EVALUASI PER KOMPONEN", size=12)

    for k in lke.get("komponen", []) or []:
        no = k.get("no")
        nama = k.get("nama", "—")
        bobot = k.get("bobot")
        nilai_k = sum(sub.get("nilai_mandiri_nilai") or 0 for sub in k.get("subkomponen", []) or [])
        _h(doc, f"6.{no}. {nama} (Bobot {bobot}, Nilai {nilai_k:.2f})", size=11)
        subs = k.get("subkomponen", []) or []
        if subs:
            # tabel subkomponen
            t = doc.add_table(rows=len(subs)+1, cols=5)
            t.autofit = False
            headers = ["No", "Subkomponen", "Bobot", "Nilai", "Pred."]
            for j, h in enumerate(headers):
                c = t.rows[0].cells[j]
                c.text = ""
                r = c.paragraphs[0].add_run(h)
                r.bold = True; r.font.size = Pt(10)
            for i, sub in enumerate(subs, start=1):
                vals = [
                    sub.get("no", ""),
                    sub.get("uraian", "")[:80],
                    str(sub.get("bobot") or ""),
                    f"{sub.get('nilai_mandiri_nilai') or 0:.2f}",
                    sub.get("jawaban_akhir_mandiri") or "—",
                ]
                for j, v in enumerate(vals):
                    c = t.rows[i].cells[j]; c.text = ""
                    r = c.paragraphs[0].add_run(str(v)); r.font.size = Pt(9)

    # ========== 7. Area of Improvement ==========
    doc.add_paragraph()
    _h(doc, "7. AREA OF IMPROVEMENT (AoI)", size=12)
    if anomalies:
        _p(doc, f"Berdasarkan hasil evaluasi, terdapat {len(anomalies)} area perbaikan berikut:",
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
        _p(doc,
           "Tidak terdapat area perbaikan yang memerlukan tindak lanjut khusus. "
           "Unit kerja telah menerapkan SAKIP sesuai standar.",
           justify=True)

    # ========== 8. Kesimpulan & Rekomendasi ==========
    doc.add_paragraph()
    _h(doc, "8. KESIMPULAN DAN REKOMENDASI", size=12)
    if total_nilai is not None:
        _p(doc,
           f"Berdasarkan hasil evaluasi, AKIP {unit} Tahun {tahun} memperoleh nilai "
           f"{total_nilai:.2f} dengan predikat \"{kategori_kode}\" ({kategori_label}). "
           f"Implementasi AKIP pada {unit} telah {kategori_label.lower()} dan perlu ditingkatkan "
           f"melalui tindak lanjut atas {len(anomalies)} AoI yang diuraikan di bagian 7.",
           justify=True)
    _p(doc,
       "Rekomendasi konkret untuk setiap AoI dirumuskan oleh tim evaluator pada lampiran "
       "LKE dan dapat diklarifikasi lebih lanjut pada forum tindak lanjut evaluasi. "
       "[Rumusan rekomendasi final dilakukan setelah gate auditor — DIISI AUDITOR]",
       justify=True, italic=True)

    doc.add_paragraph()
    _p(doc, "[TTD — DIISI AUDITOR]", align=WD_ALIGN_PARAGRAPH.RIGHT, size=10, italic=True)
    _p(doc, "Inspektur Jenderal,", align=WD_ALIGN_PARAGRAPH.RIGHT, size=10)
    _p(doc, "Arief Tri Hardiyanto", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path, len(anomalies), total_nilai, kategori_kode


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
    ap.add_argument("--lke", default=None, help="path lke.json (untuk metadata komponen + nilai)")
    ap.add_argument("-o", "--output", default="LHE-DRAFT.docx")
    args = ap.parse_args(argv)
    out, n, nilai, kategori = render_lhe(
        Path(args.anomalies), Path(args.context),
        Path(args.lke) if args.lke else None,
        Path(args.output)
    )
    print(f"OK — written: {out}")
    print(f"   AoI ter-render: {n}")
    if nilai is not None:
        print(f"   Nilai AKIP: {nilai:.2f} ({kategori})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
