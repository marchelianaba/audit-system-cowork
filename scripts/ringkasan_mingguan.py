#!/usr/bin/env python3
"""
ringkasan_mingguan.py -- Ringkasan mingguan hasil pengawasan yang LHP-nya
final dalam minggu berjalan.

Scan folder penugasan/, deteksi LHP docx/pdf dengan mtime dalam minggu
target (Senin-Minggu), lalu ekstrak nomor ST, judul, temuan, rekomendasi
-- diprioritaskan dari AoI-*.md (lebih terstruktur) dengan fallback ke
LHP docx (via python-docx jika tersedia, else catat tanpa detail).

Output: audit-system-v4/ringkasan-mingguan/YYYY-MM-DD.md
        (tanggal Senin minggu tsb)

Usage:
    python scripts/ringkasan_mingguan.py
    python scripts/ringkasan_mingguan.py --minggu 2026-04-13
    python scripts/ringkasan_mingguan.py --all-time
    python scripts/ringkasan_mingguan.py --root penugasan/ --out-dir custom/
"""

import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path


def monday_of(d):
    return d - timedelta(days=d.weekday())


def week_window(anchor):
    mon = monday_of(anchor).replace(hour=0, minute=0, second=0, microsecond=0)
    sun = mon + timedelta(days=6, hours=23, minutes=59, seconds=59)
    return mon, sun


def read_context(folder):
    ctx = {"nomor_st": "", "jenis": "", "obyek": "", "periode": "", "tim": ""}
    ctx_path = folder / "context.md"
    if not ctx_path.exists():
        return ctx
    text = ctx_path.read_text(encoding="utf-8", errors="ignore")
    for key, pat in [
        ("nomor_st", r"(?i)Nomor\s+ST\s*[:\-]\s*(.+)"),
        ("jenis", r"(?i)Jenis\s+Pengawasan\s*[:\-]\s*(.+)"),
        ("obyek", r"(?i)Obyek\s*[:\-]\s*(.+)"),
        ("periode", r"(?i)Periode\s*[:\-]\s*(.+)"),
        ("tim", r"(?i)Ketua\s+Tim\s*[:\-]\s*(.+)"),
    ]:
        m = re.search(pat, text)
        if m:
            ctx[key] = m.group(1).strip().split("\n")[0][:120]
    return ctx


def guess_judul(folder, ctx):
    if ctx["jenis"] and ctx["obyek"]:
        return f"{ctx['jenis']} {ctx['obyek']}"
    if ctx["obyek"]:
        return ctx["obyek"]
    return folder.name.replace("-", " ").replace("_", " ").title()


def guess_nomor_st(folder, ctx):
    if ctx["nomor_st"]:
        return ctx["nomor_st"]
    st_dir = folder / "00-surat-tugas"
    if st_dir.exists():
        for f in st_dir.iterdir():
            if f.is_file() and f.suffix.lower() in (".pdf", ".docx"):
                m = re.search(r"(ST[-/_][\w\-\./]+)", f.stem, re.IGNORECASE)
                if m:
                    return m.group(1)
                return f.stem[:80]
    return "(belum diisi)"


def find_lhp_files(folder):
    out = []
    lhp_dir = folder / "_LHP"
    if not lhp_dir.exists():
        return out
    for f in lhp_dir.iterdir():
        if f.is_file() and f.suffix.lower() in (".docx", ".pdf"):
            if f.name.startswith("~$"):
                continue
            if "draft" in f.stem.lower():
                continue
            out.append(f)
    return out


def lhp_in_window(folder, start, end):
    hits = []
    for f in find_lhp_files(folder):
        try:
            m = datetime.fromtimestamp(f.stat().st_mtime)
            if start <= m <= end:
                hits.append(f)
        except OSError:
            pass
    return hits


AOI_HEADING_RE = re.compile(
    r"^#{2,4}\s+(AoI-[A-Z]+(?:-[A-Z]+)?-\d+)[\s:\-\u2013\u2014]+(.+?)\s*$"
)
REKOMENDASI_RE = re.compile(r"^\*\*Rekomendasi[^\*]*\*\*\s*:?\s*(.*)$", re.IGNORECASE)


def parse_aoi_file(path, max_rekom_lines=8):
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    entries = []
    current = None
    capturing_rekom = False
    rekom_buffer = []

    def flush():
        nonlocal current, rekom_buffer
        if current is None:
            return
        rekom_text = "\n".join(rekom_buffer).strip()
        current["rekomendasi"] = rekom_text or "(belum dirumuskan)"
        entries.append(current)
        current = None
        rekom_buffer = []

    for line in lines:
        heading = AOI_HEADING_RE.match(line)
        if heading:
            flush()
            aoi_id, judul = heading.group(1), heading.group(2).strip()
            judul = re.sub(r"\[(.+?)\]\(#.*?\)", r"\1", judul)
            current = {"id": aoi_id, "judul": judul, "rekomendasi": ""}
            capturing_rekom = False
            rekom_buffer = []
            continue

        if current is None:
            continue

        m_rek = REKOMENDASI_RE.match(line.strip())
        if m_rek:
            capturing_rekom = True
            first = m_rek.group(1).strip()
            if first:
                rekom_buffer.append(first)
            continue

        if capturing_rekom:
            stripped = line.strip()
            if stripped.startswith("#"):
                capturing_rekom = False
                continue
            if stripped.startswith("**") and "opsi" not in stripped.lower() and "rekomendasi" not in stripped.lower():
                capturing_rekom = False
                continue
            if len(rekom_buffer) >= max_rekom_lines:
                capturing_rekom = False
                continue
            if stripped:
                rekom_buffer.append(stripped)

    flush()
    return entries


def collect_aoi_entries(folder):
    all_entries = []
    for f in sorted(folder.glob("AoI-*.md")):
        all_entries.extend(parse_aoi_file(f))
    seen = set()
    unique = []
    for e in all_entries:
        if e["id"] in seen:
            continue
        seen.add(e["id"])
        unique.append(e)
    return unique


def extract_from_docx(path):
    try:
        from docx import Document
    except ImportError:
        return []
    try:
        doc = Document(str(path))
    except Exception:
        return []

    paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    entries = []
    current = None
    capturing_rekom = False
    rekom_buf = []

    judul_re = re.compile(r"^\d+\.\s+\S+")
    rek_re = re.compile(r"^Rekomendasi\s*[:\-]?\s*(.*)", re.IGNORECASE)

    def flush():
        nonlocal current, rekom_buf
        if current is not None:
            current["rekomendasi"] = " ".join(rekom_buf).strip() or "(belum dirumuskan)"
            entries.append(current)
        current = None
        rekom_buf = []

    for p in paras:
        if judul_re.match(p) and len(p) < 200:
            flush()
            current = {"id": "", "judul": p, "rekomendasi": ""}
            capturing_rekom = False
            continue
        m = rek_re.match(p)
        if m and current is not None:
            capturing_rekom = True
            first = m.group(1).strip()
            if first:
                rekom_buf.append(first)
            continue
        if capturing_rekom and current is not None:
            if judul_re.match(p):
                flush()
                current = {"id": "", "judul": p, "rekomendasi": ""}
                capturing_rekom = False
                continue
            rekom_buf.append(p)
            if len(" ".join(rekom_buf)) > 600:
                capturing_rekom = False

    flush()
    return entries[:25]


def render(items, start, end):
    iso_year, iso_week, _ = start.isocalendar()
    lines = [
        "# Ringkasan Mingguan Hasil Pengawasan",
        "",
        f"**Minggu:** {iso_year}-W{iso_week:02d} ({start.strftime('%d %b %Y')} s.d. {end.strftime('%d %b %Y')})",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
    ]
    if not items:
        lines.append("_Tidak ada LHP yang final dalam minggu ini._")
        lines.append("")
        return "\n".join(lines)

    lines.append(f"Total: **{len(items)} penugasan** dengan LHP final minggu ini.")
    lines.append("")

    for idx, it in enumerate(items, 1):
        lines.append(f"## {idx}. {it['judul_st']}")
        lines.append("")
        lines.append(f"- **Nomor ST:** {it['nomor_st']}")
        lines.append(f"- **Folder:** `{it['folder']}`")
        lines.append(f"- **File LHP:** `{it['lhp_file']}`")
        lines.append(f"- **Tanggal final (mtime):** {it['lhp_mtime']}")
        lines.append("")

        if it["entries"]:
            lines.append(f"### Temuan & Rekomendasi ({len(it['entries'])})")
            lines.append("")
            lines.append("| No | Temuan | Rekomendasi |")
            lines.append("|----|--------|-------------|")
            for j, e in enumerate(it["entries"], 1):
                judul = e.get("judul", "").replace("|", "\\|").replace("\n", " ")
                if e.get("id"):
                    judul = f"**{e['id']}** -- {judul}"
                rekom = e.get("rekomendasi", "").replace("|", "\\|").replace("\n", " ")
                if len(rekom) > 400:
                    rekom = rekom[:400].rsplit(" ", 1)[0] + " ..."
                lines.append(f"| {j} | {judul} | {rekom} |")
            lines.append("")
        else:
            lines.append("_Tidak berhasil mengekstrak temuan otomatis -- silakan isi manual dari LHP._")
            lines.append("")

    lines.append("---")
    lines.append("_Generated by `scripts/ringkasan_mingguan.py` -- cek & edit sebelum dikirim._")
    lines.append("")
    return "\n".join(lines)


def collect(root, start, end, all_time):
    items = []
    for sub in sorted(root.iterdir()):
        if not sub.is_dir():
            continue
        if sub.name.startswith(".") or sub.name.startswith("_"):
            continue
        lhps = find_lhp_files(sub) if all_time else lhp_in_window(sub, start, end)
        if not lhps:
            continue
        ctx = read_context(sub)
        entries = collect_aoi_entries(sub)
        if not entries:
            docx_files = [p for p in lhps if p.suffix.lower() == ".docx"]
            if docx_files:
                entries = extract_from_docx(docx_files[0])
        lhp = sorted(lhps, key=lambda p: p.stat().st_mtime, reverse=True)[0]
        items.append({
            "folder": sub.name,
            "nomor_st": guess_nomor_st(sub, ctx),
            "judul_st": guess_judul(sub, ctx),
            "lhp_file": lhp.name,
            "lhp_mtime": datetime.fromtimestamp(lhp.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
            "entries": entries,
        })
    return items


def main():
    ap = argparse.ArgumentParser(description="Ringkasan mingguan hasil pengawasan")
    ap.add_argument("--root", type=Path, default=Path("penugasan"))
    ap.add_argument("--minggu", type=str, default="")
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--all-time", action="store_true")
    ap.add_argument("--stdout", action="store_true")
    args = ap.parse_args()

    root = args.root
    if not root.exists():
        script_dir = Path(__file__).resolve().parent.parent
        cand = script_dir / "penugasan"
        if cand.exists():
            root = cand
    if not root.exists():
        print(f"[error] folder penugasan tidak ditemukan: {args.root}")
        return

    anchor = datetime.strptime(args.minggu, "%Y-%m-%d") if args.minggu else datetime.now()
    start, end = week_window(anchor)

    items = collect(root, start, end, args.all_time)
    md = render(items, start, end)

    if args.stdout:
        print(md)
        return

    out_dir = args.out_dir
    if out_dir is None:
        out_dir = Path(__file__).resolve().parent.parent / "ringkasan-mingguan"
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = f"{start.strftime('%Y-%m-%d')}{'-all' if args.all_time else ''}.md"
    out_path = out_dir / fname
    out_path.write_text(md, encoding="utf-8")
    print(f"[saved] {out_path}")
    print(f"  minggu   : {start.strftime('%Y-%m-%d')} s.d. {end.strftime('%Y-%m-%d')}")
    print(f"  penugasan: {len(items)}")


if __name__ == "__main__":
    main()
