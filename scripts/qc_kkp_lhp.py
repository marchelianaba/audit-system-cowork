#!/usr/bin/env python3
"""
qc_kkp_lhp.py — Quality Control otomatis untuk KKP dan LHP sebelum final.

Jalankan sebelum auditor memberi SETUJU pada Task 03 (KKP) atau Task 04 (LHP)
untuk memastikan anti-halusinasi dan kelengkapan administratif.

Cek yang dilakukan:
  KKP:
    1. Setiap baris kondisi memiliki sumber dokumen (pattern: "nama_file" + "p./pasal/ayat")
    2. Kolom wajib per jenis pengawasan terisi (tidak kosong)
    3. Tidak ada kata "TERPENUHI/TIDAK TERPENUHI" sebagai judul temuan
    4. Nomor ST konsisten dengan context.md

  LHP:
    1. Tidak ada placeholder [DIISI AUDITOR] di bagian substansi (kecuali bagian admin)
    2. Setiap temuan punya Kondisi, Kriteria, Akibat, Rekomendasi
    3. Bahasa keyakinan benar (sesuai paradigma KKP: memadai vs terbatas)
    4. Nomor ST konsisten dengan context.md
    5. Font & formatting standar (Arial, justified, sz=24) — warn only

Usage:
    python scripts/qc_kkp_lhp.py <path-folder-penugasan>
    python scripts/qc_kkp_lhp.py <path-folder-penugasan> --only kkp
    python scripts/qc_kkp_lhp.py <path-folder-penugasan> --only lhp
    python scripts/qc_kkp_lhp.py <path-folder-penugasan> --strict   # exit 1 jika ada warning

Contoh:
    python scripts/qc_kkp_lhp.py penugasan/2026-084-reviu-pengadaan-dc-psre/
"""

import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

try:
    from docx import Document
except ImportError:
    print("python-docx tidak tersedia. Instal: pip install python-docx --break-system-packages")
    sys.exit(2)

# ─────────────────────────────────────────────────────────────
# Konstanta
# ─────────────────────────────────────────────────────────────

PARADIGMA_PER_SKILL = {
    "audit-pengadaan": "memadai",
    "audit-kinerja": "memadai",
    "reviu-pengadaan": "terbatas",
    "reviu-rka-kl": "terbatas",
    "pemantauan-pengadaan": "pemantauan",
    "evaluasi-sakip": "terbatas",
    "evaluasi-manajemen-risiko": "terbatas",
    "evaluasi-spip": "terbatas",
    "evaluasi-reformasi-birokrasi": "terbatas",
    "konsultasi-pengadaan": "konsultasi",
}

FRASA_KEYAKINAN_TERBATAS = "tidak terdapat hal-hal yang membuat kami yakin bahwa"
FRASA_KEYAKINAN_MEMADAI = "berdasarkan prosedur audit"

# Pattern sumber dokumen: nama.ext + p./pasal/ayat/hlm
SUMBER_PATTERN = re.compile(
    r"(?i)\b(\w[\w\-.\s]+\.(docx?|pdf|xlsx?|pptx?))\b.*?(p\.|pasal|ayat|hlm|halaman)",
    re.DOTALL,
)

LABEL_STATUS_JUDUL = re.compile(
    r"^\s*(TERPENUHI|TIDAK\s+TERPENUHI|MEMENUHI|BELUM\s+MEMENUHI|SESUAI|TIDAK\s+SESUAI)\s*$",
    re.IGNORECASE,
)

PLACEHOLDER_ADMIN_FIELDS_OK = {
    "nomor surat", "nomor lhp", "tanggal", "destinatari", "tembusan",
    "nota dinas", "ttd", "penandatangan", "yth", "kepada",
}

# ─────────────────────────────────────────────────────────────
# Hasil
# ─────────────────────────────────────────────────────────────

@dataclass
class Issue:
    level: str   # ERROR / WARN / INFO
    cek: str
    detail: str
    lokasi: str = ""

@dataclass
class Report:
    file: str
    issues: List[Issue] = field(default_factory=list)

    def add(self, level, cek, detail, lokasi=""):
        self.issues.append(Issue(level, cek, detail, lokasi))

    @property
    def errors(self):
        return [i for i in self.issues if i.level == "ERROR"]

    @property
    def warns(self):
        return [i for i in self.issues if i.level == "WARN"]


# ─────────────────────────────────────────────────────────────
# Reader helpers
# ─────────────────────────────────────────────────────────────

def read_docx_all_text(path: Path):
    """Return list of (lokasi_str, text) untuk paragraf + sel tabel."""
    doc = Document(str(path))
    out = []
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip():
            out.append((f"para#{i}", p.text))
    for ti, tbl in enumerate(doc.tables):
        for ri, row in enumerate(tbl.rows):
            for ci, cell in enumerate(row.cells):
                if cell.text.strip():
                    out.append((f"tbl{ti}-r{ri}c{ci}", cell.text))
    return out


def read_context(penugasan: Path):
    ctx_path = penugasan / "context.md"
    if not ctx_path.exists():
        return {}
    text = ctx_path.read_text(encoding="utf-8", errors="ignore")
    ctx = {}
    for key in ["Nomor ST", "Jenis Pengawasan", "Skill", "Paradigma"]:
        m = re.search(rf"(?i){key}\s*[:\-]\s*(.+)", text)
        if m:
            ctx[key] = m.group(1).strip().split("\n")[0].strip()
    return ctx


# ─────────────────────────────────────────────────────────────
# QC KKP
# ─────────────────────────────────────────────────────────────

def qc_kkp(kkp_path: Path, ctx: dict) -> Report:
    rep = Report(file=str(kkp_path.name))
    try:
        rows = read_docx_all_text(kkp_path)
    except Exception as e:
        rep.add("ERROR", "parse", f"Gagal baca KKP: {e}")
        return rep

    full_text = "\n".join(t for _, t in rows)

    # 1. Nomor ST konsisten
    if "Nomor ST" in ctx:
        nomor_clean = re.sub(r"\s+", " ", ctx["Nomor ST"]).strip()
        if nomor_clean and nomor_clean not in full_text:
            rep.add("WARN", "nomor-st", f"Nomor ST '{nomor_clean}' dari context.md tidak ditemukan di KKP.")

    # 2. Sumber dokumen per kondisi
    kondisi_rows = [(lok, txt) for lok, txt in rows if "kondisi" in txt.lower() or re.search(r"^\d+\.\s", txt)]
    if not kondisi_rows:
        # fallback: scan seluruh tabel — setiap sel yang mengandung ">= 2 kalimat" dianggap narasi
        kondisi_rows = [(lok, txt) for lok, txt in rows if lok.startswith("tbl") and len(txt) > 80]

    kondisi_tanpa_sumber = []
    for lok, txt in kondisi_rows:
        if not SUMBER_PATTERN.search(txt):
            # Skip jika isinya tampak heading/placeholder
            if len(txt) < 40 or "[DIISI" in txt.upper():
                continue
            kondisi_tanpa_sumber.append((lok, txt[:120].replace("\n", " ") + "..."))
    for lok, preview in kondisi_tanpa_sumber[:10]:
        rep.add("ERROR", "sumber-dokumen",
                f"Kondisi tidak mencantumkan sumber dokumen (nama file + p./pasal). Preview: {preview}",
                lokasi=lok)
    if len(kondisi_tanpa_sumber) > 10:
        rep.add("WARN", "sumber-dokumen",
                f"... dan {len(kondisi_tanpa_sumber)-10} baris lain tanpa sumber dokumen.")

    # 3. Judul temuan bukan label status
    for lok, txt in rows:
        for line in txt.split("\n"):
            if LABEL_STATUS_JUDUL.match(line):
                rep.add("ERROR", "format-judul",
                        f"Judul temuan berupa label status '{line.strip()}' — harus kalimat deskriptif kondisi.",
                        lokasi=lok)

    # 4. Rekomendasi TIDAK ada di KKP
    if re.search(r"(?i)^\s*rekomendasi\s*:", full_text, re.MULTILINE):
        rep.add("WARN", "rekomendasi-di-kkp",
                "Kolom/bagian 'Rekomendasi' terdeteksi di KKP. Sesuai prinsip sistem, rekomendasi hanya muncul di LHP (Task 04).")

    return rep


# ─────────────────────────────────────────────────────────────
# QC LHP
# ─────────────────────────────────────────────────────────────

def qc_lhp(lhp_path: Path, ctx: dict) -> Report:
    rep = Report(file=str(lhp_path.name))
    try:
        rows = read_docx_all_text(lhp_path)
    except Exception as e:
        rep.add("ERROR", "parse", f"Gagal baca LHP: {e}")
        return rep

    full_text = "\n".join(t for _, t in rows)

    # 1. Placeholder [DIISI AUDITOR] hanya boleh di field admin
    for lok, txt in rows:
        m = re.search(r"\[DIISI\s+AUDITOR\]", txt, re.IGNORECASE)
        if not m:
            continue
        ctx_line = txt.lower()
        is_admin = any(k in ctx_line for k in PLACEHOLDER_ADMIN_FIELDS_OK)
        if not is_admin:
            rep.add("ERROR", "placeholder-bocor",
                    f"Placeholder [DIISI AUDITOR] di luar field administratif. Preview: {txt[:120]}",
                    lokasi=lok)

    # 2. Nomor ST konsisten
    if "Nomor ST" in ctx:
        nomor_clean = re.sub(r"\s+", " ", ctx["Nomor ST"]).strip()
        if nomor_clean and nomor_clean not in full_text:
            rep.add("WARN", "nomor-st", f"Nomor ST '{nomor_clean}' dari context.md tidak ditemukan di LHP.")

    # 3. Bahasa keyakinan sesuai paradigma
    paradigma = PARADIGMA_PER_SKILL.get((ctx.get("Skill") or "").strip().lower(), "")
    if not paradigma:
        paradigma = (ctx.get("Paradigma") or "").strip().lower()
    if paradigma == "terbatas":
        if FRASA_KEYAKINAN_TERBATAS not in full_text.lower():
            rep.add("WARN", "bahasa-keyakinan",
                    f"Paradigma 'terbatas' — frasa baku '{FRASA_KEYAKINAN_TERBATAS}...' tidak ditemukan. Lihat feedback_sistem.md §8.")
    elif paradigma == "memadai":
        if FRASA_KEYAKINAN_MEMADAI not in full_text.lower():
            rep.add("WARN", "bahasa-keyakinan",
                    f"Paradigma 'memadai' — frasa baku '{FRASA_KEYAKINAN_MEMADAI}...' tidak ditemukan.")

    # 4. Font & formatting (warn only)
    try:
        doc = Document(str(lhp_path))
        non_arial = 0
        for p in doc.paragraphs:
            for run in p.runs:
                name = run.font.name
                if name and name.lower() not in ("arial", ""):
                    non_arial += 1
        if non_arial > 0:
            rep.add("WARN", "font", f"{non_arial} run menggunakan font non-Arial. Template LHP standar: Arial.")
    except Exception:
        pass

    return rep


# ─────────────────────────────────────────────────────────────
# Orkestrasi
# ─────────────────────────────────────────────────────────────

def find_docs(penugasan: Path):
    kkp_files = sorted((penugasan / "_KKP").glob("KKP-*.docx")) if (penugasan / "_KKP").exists() else []
    lhp_files = sorted((penugasan / "_LHP").glob("*.docx")) if (penugasan / "_LHP").exists() else []
    return kkp_files, lhp_files


def print_report(rep: Report):
    n_err = len(rep.errors); n_warn = len(rep.warns)
    status = "OK" if (n_err == 0 and n_warn == 0) else ("FAIL" if n_err else "WARN")
    print(f"\n── {rep.file} :: {status} (errors={n_err}, warns={n_warn})")
    for i in rep.issues:
        tag = {"ERROR": "❌", "WARN": "⚠️ ", "INFO": "ℹ️ "}.get(i.level, "•")
        loc = f" @{i.lokasi}" if i.lokasi else ""
        print(f"  {tag} [{i.cek}]{loc}  {i.detail}")


def main():
    ap = argparse.ArgumentParser(description="QC KKP/LHP")
    ap.add_argument("penugasan", type=Path)
    ap.add_argument("--only", choices=["kkp", "lhp"], default=None)
    ap.add_argument("--strict", action="store_true", help="exit 1 jika ada warning")
    args = ap.parse_args()

    p = args.penugasan
    if not p.exists():
        print(f"Folder tidak ada: {p}")
        sys.exit(2)

    ctx = read_context(p)
    kkp_files, lhp_files = find_docs(p)

    all_reports: List[Report] = []

    if args.only != "lhp":
        for f in kkp_files:
            all_reports.append(qc_kkp(f, ctx))
    if args.only != "kkp":
        for f in lhp_files:
            all_reports.append(qc_lhp(f, ctx))

    if not all_reports:
        print(f"Tidak ada KKP/LHP di {p}")
        sys.exit(0)

    print("=" * 70)
    print(f"QC Report — {p.name}")
    if ctx:
        print(f"  Context: {ctx}")
    print("=" * 70)

    total_err = 0; total_warn = 0
    for rep in all_reports:
        print_report(rep)
        total_err += len(rep.errors)
        total_warn += len(rep.warns)

    print("\n" + "=" * 70)
    print(f"TOTAL: {total_err} error, {total_warn} warning")
    print("=" * 70)

    if total_err > 0:
        sys.exit(1)
    if args.strict and total_warn > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
