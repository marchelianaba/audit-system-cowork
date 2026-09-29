"""
generate_bukti_ai_docx.py — Generator dokumen Bukti Pengecekan AI (.docx).

Tahapan #6 Integral SIMWAS v2 = "Bukti Cek AI" — slot khusus untuk
mendokumentasikan bahwa output pengawasan dihasilkan dengan bantuan AI dan
auditor sudah memvalidasi.

Output dokumen memuat:
  1. Identitas penugasan
  2. Skill, model, tanggal eksekusi pipeline
  3. Rules deterministik yang dijalankan + jumlah anomali per severity
  4. Excerpt audit trail (input file hashes, retrieval RAG)
  5. Pernyataan validasi auditor

Dokumen ini siap diunggah ke slot "Bukti Cek AI" di Integral.

Usage:
    python3 generate_bukti_ai_docx.py \
        --penugasan PATH_FOLDER_PENUGASAN \
        [--skill SKILL_NAME] \
        [--model MODEL_NAME] \
        [--auditor AUDITOR_NAME]

Output:
    <penugasan>/_BUKTI-AI/Bukti-Cek-AI-<judul>-<ts>.docx
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

try:
    from docx import Document
    from docx.shared import Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_ALIGN_VERTICAL
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    sys.exit("ERROR: python-docx not installed. Run: pip install python-docx --break-system-packages")


WIB = timezone(timedelta(hours=7))


def _self_check_ast() -> None:
    try:
        ast.parse(Path(__file__).read_text(encoding="utf-8"))
    except SyntaxError as e:
        print(f"[FATAL] Self-check AST gagal di {__file__}: {e}", file=sys.stderr)
        sys.exit(2)


def load_json_safe(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def load_context_md(penugasan: Path) -> dict[str, str]:
    ctx_path = penugasan / "context.md"
    if not ctx_path.exists():
        return {}
    out: dict[str, str] = {}
    for line in ctx_path.read_text(encoding="utf-8").splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, _, v = line.partition(":")
            k = k.strip().strip("-").strip().lower().replace(" ", "_")
            v = v.strip().strip('"').strip("'")
            if k and v and k not in out:
                out[k] = v
    return out


def slugify(s: str, maxlen: int = 60) -> str:
    s = re.sub(r"[^\w\s-]", "", s).strip()
    s = re.sub(r"[\s_-]+", "-", s)
    return s[:maxlen] or "Penugasan"


# ---------- DOCX building helpers ----------

def add_heading_inline(doc: Document, text: str, size: int = 14, bold: bool = True, center: bool = False) -> None:
    p = doc.add_paragraph()
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = "Arial"


def add_kv_row(table, key: str, value: str) -> None:
    row = table.add_row().cells
    row[0].text = key
    row[1].text = ":"
    row[2].text = value or "—"
    for c in row:
        for p in c.paragraphs:
            for r in p.runs:
                r.font.size = Pt(10)
                r.font.name = "Arial"


def set_table_borders(table) -> None:
    tbl = table._tbl
    tblPr = tbl.find(qn("w:tblPr"))
    if tblPr is None:
        tblPr = OxmlElement("w:tblPr")
        tbl.insert(0, tblPr)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{edge}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "4")
        b.set(qn("w:color"), "000000")
        borders.append(b)
    tblPr.append(borders)


# ---------- main builder ----------

def build_bukti_ai_docx(penugasan: Path, skill: str, model: str, auditor: str) -> Path:
    ctx = load_context_md(penugasan)
    kkp_meta = load_json_safe(penugasan / "_KKP" / "_pipeline_meta.json") or {}
    anomalies_master = load_json_safe(penugasan / "_KKP" / "anomalies-master.json") or load_json_safe(penugasan / "_KKP" / "anomalies.json") or {}
    anomalies = anomalies_master.get("anomalies", []) if isinstance(anomalies_master, dict) else []

    doc = Document()

    # Margins
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.0)

    # Header — Kop Surat ringkas (one-liner kementerian)
    add_heading_inline(doc, "INSPEKTORAT JENDERAL", size=11, bold=True, center=True)
    add_heading_inline(doc, "KEMENTERIAN KOMUNIKASI DAN DIGITAL REPUBLIK INDONESIA", size=11, bold=True, center=True)
    add_heading_inline(doc, "INSPEKTORAT II", size=11, bold=True, center=True)
    doc.add_paragraph("─" * 100).alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()

    # Title
    add_heading_inline(doc, "BUKTI PENGECEKAN PENGGUNAAN AI", size=14, bold=True, center=True)
    add_heading_inline(doc, "Validasi Output Pengawasan Berbasis Artificial Intelligence", size=11, bold=False, center=True)
    doc.add_paragraph()

    # Section 1: Identitas Penugasan
    add_heading_inline(doc, "1. IDENTITAS PENUGASAN", size=12)
    t1 = doc.add_table(rows=0, cols=3)
    t1.columns[0].width = Cm(5)
    t1.columns[1].width = Cm(0.5)
    t1.columns[2].width = Cm(11)
    add_kv_row(t1, "Nomor Surat Tugas", ctx.get("nomor_st") or ctx.get("nomor_surat_tugas", ""))
    add_kv_row(t1, "Judul Pengawasan", ctx.get("judul_pengawasan") or ctx.get("judul", ""))
    add_kv_row(t1, "Tujuan Pengawasan", ctx.get("tujuan_pengawasan") or ctx.get("tujuan", ""))
    add_kv_row(t1, "Periode Pengawasan", f"{ctx.get('tanggal_mulai', '')} s.d. {ctx.get('tanggal_selesai', '')}")
    add_kv_row(t1, "Tim Pengawasan", f"Ketua: {ctx.get('ketua_tim', '—')}, Anggota: {ctx.get('anggota_tim_1', '—')}")
    doc.add_paragraph()

    # Section 2: Identitas Sistem AI
    add_heading_inline(doc, "2. IDENTITAS SISTEM AI", size=12)
    t2 = doc.add_table(rows=0, cols=3)
    add_kv_row(t2, "Sistem", "Claude Cowork — Audit System v4 (Inspektorat II)")
    add_kv_row(t2, "Skill yang Digunakan", skill or kkp_meta.get("skill", "—"))
    add_kv_row(t2, "Model AI", model)
    add_kv_row(t2, "Versi Skill", kkp_meta.get("skill_version", "v1.0"))
    add_kv_row(t2, "Vendor", "Anthropic (tier enterprise, zero data retention)")
    add_kv_row(t2, "Tanggal Eksekusi", kkp_meta.get("tanggal", datetime.now(WIB).strftime("%Y-%m-%d %H:%M")))
    add_kv_row(t2, "Wall Clock Eksekusi", f"{kkp_meta.get('wall_clock_seconds', 0):.1f} detik")
    doc.add_paragraph()

    # Section 3: Rules & Hasil Deteksi
    add_heading_inline(doc, "3. RULES DETERMINISTIK & HASIL DETEKSI", size=12)
    p = doc.add_paragraph()
    p.add_run("Pipeline AI menjalankan rule-based cross-check sebelum analisis substantif Claude. "
              "Rule adalah aturan deterministik yang mendeteksi anomali struktural dokumen secara otomatis. "
              "Hasil deteksi rule WAJIB direviu auditor sebelum menjadi temuan KKP.").font.size = Pt(10)

    t3 = doc.add_table(rows=1, cols=3)
    t3.columns[0].width = Cm(8)
    t3.columns[1].width = Cm(3)
    t3.columns[2].width = Cm(5)
    set_table_borders(t3)
    hdr = t3.rows[0].cells
    hdr[0].text = "Metrik"
    hdr[1].text = "Nilai"
    hdr[2].text = "Keterangan"
    for c in hdr:
        for p in c.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(10)

    n_anom = len(anomalies)
    per_sev: dict[str, int] = kkp_meta.get("per_severity", {})
    if not per_sev and anomalies:
        for a in anomalies:
            sev = a.get("severity", "INFO")
            per_sev[sev] = per_sev.get(sev, 0) + 1

    rules_run = kkp_meta.get("rules_dijalankan") or "—"
    metrics = [
        ("Total rules deterministik dijalankan", str(rules_run), "Rule yang sudah ditetapkan & disetujui auditor senior"),
        ("Total anomali terdeteksi otomatis", str(n_anom), "Sebelum reviu auditor — wajib divalidasi"),
    ]
    for sev, count in sorted(per_sev.items()):
        metrics.append((f"  – Severity {sev}", str(count), ""))
    metrics += [
        ("Wall clock eksekusi", f"{kkp_meta.get('wall_clock_seconds', 0):.1f} detik", "End-to-end pipeline"),
        ("Metode deteksi", "Rule-based + heuristik regex", "Pure deterministik, no LLM dalam fase ini"),
    ]
    for k, v, ket in metrics:
        row = t3.add_row().cells
        row[0].text = k
        row[1].text = v
        row[2].text = ket
        for c in row:
            for pp in c.paragraphs:
                for r in pp.runs:
                    r.font.size = Pt(9)
    doc.add_paragraph()

    # Section 4: Audit Trail Excerpt
    add_heading_inline(doc, "4. AUDIT TRAIL — INPUT DOKUMEN & PROSES", size=12)
    p = doc.add_paragraph()
    p.add_run("Setiap dokumen input dihash SHA-256 sebagai bukti integritas. "
              "Audit trail lengkap tersimpan di file JSONL append-only yang dapat diakses untuk forensik.").font.size = Pt(10)

    audit_trail = penugasan / "_AUDIT-TRAIL" / "events.jsonl"
    if audit_trail.exists():
        # Sample 5 latest events
        lines = audit_trail.read_text(encoding="utf-8").strip().splitlines()[-5:]
        events = []
        for line in lines:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                pass
        if events:
            add_heading_inline(doc, "Sampel 5 event terakhir:", size=10, bold=True)
            for e in events:
                bullet = doc.add_paragraph(style="List Bullet")
                bullet.add_run(f"{e.get('timestamp', '?')} — {e.get('event_type', '?')} "
                               f"oleh {e.get('user', '?')}: {e.get('message', '')[:120]}").font.size = Pt(9)
        else:
            doc.add_paragraph(f"Audit trail tersedia di: {audit_trail.relative_to(penugasan)}").font.size = Pt(9)
    else:
        doc.add_paragraph("File audit trail _AUDIT-TRAIL/events.jsonl belum dibuat di penugasan ini.").italic = True

    # Daftar input docs dengan SHA-256
    input_files: list[tuple[str, str, int]] = []
    for d in [penugasan / "00-input", penugasan]:
        if d.exists():
            for f in d.rglob("*"):
                if f.is_file() and f.suffix.lower() in (".pdf", ".docx", ".xlsx", ".xls"):
                    if "_KKP" not in f.parts and "_LHP" not in f.parts and "_BUKTI-AI" not in f.parts:
                        import hashlib
                        h = hashlib.sha256(f.read_bytes()).hexdigest()
                        input_files.append((str(f.relative_to(penugasan)), h[:16] + "...", f.stat().st_size))
                        if len(input_files) >= 10:
                            break
    if input_files:
        add_heading_inline(doc, "Dokumen Input (10 pertama):", size=10, bold=True)
        t4 = doc.add_table(rows=1, cols=3)
        t4.columns[0].width = Cm(10)
        t4.columns[1].width = Cm(4)
        t4.columns[2].width = Cm(2)
        set_table_borders(t4)
        h = t4.rows[0].cells
        h[0].text = "Path"
        h[1].text = "SHA-256 (16 char)"
        h[2].text = "Size"
        for c in h:
            for pp in c.paragraphs:
                for r in pp.runs:
                    r.font.bold = True
                    r.font.size = Pt(9)
        for path, hash_short, size in input_files:
            row = t4.add_row().cells
            row[0].text = path
            row[1].text = hash_short
            row[2].text = f"{size//1024} KB"
            for c in row:
                for pp in c.paragraphs:
                    for r in pp.runs:
                        r.font.size = Pt(8)
    doc.add_paragraph()

    # Section 5: Pernyataan Validasi
    add_heading_inline(doc, "5. PERNYATAAN VALIDASI AUDITOR", size=12)
    pernyataan = (
        f"Yang bertanda tangan di bawah ini, {auditor}, menyatakan bahwa:\n\n"
        f"1. Output pipeline AI di atas (anomali, draft KKP, draft Konsep Laporan) telah saya reviu di setiap "
        f"gate Cowork sebelum menyetujui kelanjutan ke tahap berikutnya.\n\n"
        f"2. Rules deterministik yang dijalankan sudah disetujui Inspektur Jenderal melalui pengesahan skill "
        f"versi yang tertera di bagian 2.\n\n"
        f"3. Anomali yang terdeteksi otomatis sudah saya validasi terhadap dokumen sumber. False positive "
        f"telah saya filter; temuan substantif baru yang tidak terdeteksi rules telah saya tambahkan secara manual.\n\n"
        f"4. Pertimbangan profesional (professional judgment) tetap menjadi inti pengawasan; AI berperan "
        f"sebagai alat bantu produksi, bukan pengambil keputusan."
    )
    p = doc.add_paragraph(pernyataan)
    for r in p.runs:
        r.font.size = Pt(10)
        r.font.name = "Arial"

    doc.add_paragraph()
    doc.add_paragraph()

    # Tanda tangan
    sig_p = doc.add_paragraph()
    sig_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    sig_p.add_run(f"Jakarta, {datetime.now(WIB).strftime('%d %B %Y')}\n").font.size = Pt(11)
    sig_p.add_run("Auditor Pelaksana,\n\n\n\n").font.size = Pt(11)
    sig_p.add_run(f"{auditor}\n").bold = True

    # Footer note
    doc.add_paragraph()
    note = doc.add_paragraph()
    note_run = note.add_run(
        f"Dokumen ini dihasilkan otomatis oleh generate_bukti_ai_docx.py "
        f"pada {datetime.now(WIB).strftime('%Y-%m-%d %H:%M:%S WIB')}. "
        f"Dokumen ini WAJIB diparaf auditor sebelum diunggah ke slot Bukti Cek AI di Integral."
    )
    note_run.italic = True
    note_run.font.size = Pt(8)
    note_run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)

    # Save
    bukti_dir = penugasan / "_BUKTI-AI"
    bukti_dir.mkdir(parents=True, exist_ok=True)
    judul = ctx.get("judul_pengawasan") or ctx.get("judul") or penugasan.name
    ts = datetime.now(WIB).strftime("%Y%m%d-%H%M%S")
    out_path = bukti_dir / f"Bukti-Cek-AI-{slugify(judul)}-{ts}.docx"
    doc.save(out_path)
    return out_path


def main(argv: list[str] | None = None) -> int:
    _self_check_ast()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--penugasan", required=True)
    ap.add_argument("--skill", default="")
    ap.add_argument("--model", default="claude-sonnet-4-6")
    ap.add_argument("--auditor", default="Auditor Inspektorat II")
    args = ap.parse_args(argv)

    penugasan = Path(args.penugasan).resolve()
    if not penugasan.exists():
        print(f"[FATAL] Folder penugasan tidak ditemukan: {penugasan}", file=sys.stderr)
        return 4

    print(f"Generating Bukti Cek AI .docx for: {penugasan.name}")
    out_path = build_bukti_ai_docx(penugasan, args.skill, args.model, args.auditor)
    print(f"[OK] Saved: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
