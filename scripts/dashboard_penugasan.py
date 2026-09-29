#!/usr/bin/env python3
"""
dashboard_penugasan.py — Ringkasan status semua penugasan aktif.

Scan folder penugasan/ dan rangkum status tiap penugasan:
  - Jenis pengawasan, nomor ST, tim
  - Progress gate (jika ada penilaian-progress.json)
  - Jumlah file KKP / LHP / AoI
  - Outstanding AoI (dari AoI-*.md)
  - Last-activity date (mtime dokumen terbaru)

Output: tabel markdown ke stdout + optional file dashboard.md di root audit-system-v4.

Usage:
    python scripts/dashboard_penugasan.py
    python scripts/dashboard_penugasan.py --save      # tulis dashboard.md
    python scripts/dashboard_penugasan.py --root penugasan/
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


def read_context(folder: Path) -> dict:
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
            ctx[key] = m.group(1).strip().split("\n")[0][:80]
    return ctx


def read_progress(folder: Path) -> dict:
    prog_path = folder / "penilaian-progress.json"
    if not prog_path.exists():
        return {}
    try:
        return json.loads(prog_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def current_gate(progress: dict) -> str:
    if not progress:
        return "-"
    gates = [k for k in progress if k.startswith("gate_")]
    if not gates:
        return "-"
    gates.sort()
    for g in reversed(gates):
        if isinstance(progress[g], dict) and progress[g].get("status"):
            return f"{g}:{progress[g]['status']}"
    return gates[-1]


def count_files(folder: Path, subdir: str, ext: str):
    d = folder / subdir
    if not d.exists():
        return 0
    return len([f for f in d.iterdir() if f.suffix.lower() == ext])


def count_aoi(folder: Path):
    """Hitung AoI unik dari file AoI-*.md.

    Match ID AoI di mana saja dalam teks, pakai set untuk de-dup
    (AoI sering muncul berkali-kali di daftar isi, heading, referensi).
    """
    ids = set()
    for aoi_file in folder.glob("AoI-*.md"):
        text = aoi_file.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"\bAoI-[A-Z]+(?:-[A-Z]+)?-\d+\b", text):
            ids.add(m.group(0))
    return len(ids)


def last_activity(folder: Path) -> str:
    latest = 0
    for f in folder.rglob("*"):
        if f.is_file() and not f.name.endswith(("desktop.ini",)):
            try:
                m = f.stat().st_mtime
                if m > latest:
                    latest = m
            except Exception:
                pass
    if latest == 0:
        return "-"
    return datetime.fromtimestamp(latest).strftime("%Y-%m-%d")


def age_indicator(last_str: str) -> str:
    if last_str == "-":
        return "?"
    try:
        last = datetime.strptime(last_str, "%Y-%m-%d")
        age = (datetime.now() - last).days
        if age <= 3:
            return "HIJAU"
        if age <= 10:
            return "KUNING"
        return "MERAH"
    except Exception:
        return "?"


def collect_penugasan(root: Path):
    items = []
    for sub in sorted(root.iterdir()):
        if not sub.is_dir():
            continue
        if sub.name.startswith(".") or sub.name.startswith("_"):
            continue
        ctx = read_context(sub)
        progress = read_progress(sub)
        last = last_activity(sub)
        items.append({
            "nama": sub.name,
            "jenis": ctx["jenis"] or "?",
            "nomor_st": ctx["nomor_st"] or "?",
            "obyek": ctx["obyek"] or "?",
            "ketua_tim": ctx["tim"] or "?",
            "gate": current_gate(progress),
            "kkp": count_files(sub, "_KKP", ".docx"),
            "lhp": count_files(sub, "_LHP", ".docx"),
            "aoi": count_aoi(sub),
            "last": last,
            "age": age_indicator(last),
        })
    return items


def render_markdown(items, root: Path) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# Dashboard Penugasan Aktif",
        f"_Generated: {now} -- root: `{root}`_",
        "",
        f"Total: **{len(items)} penugasan** | HIJAU <=3 hari / KUNING <=10 / MERAH >10",
        "",
        "| # | Penugasan | Jenis | Nomor ST | Gate/Status | KKP | LHP | AoI | Last | Age |",
        "|---|-----------|-------|----------|-------------|----:|----:|----:|------|:---:|",
    ]
    for i, it in enumerate(items, 1):
        lines.append(
            f"| {i} | {it['nama']} | {it['jenis']} | {it['nomor_st']} | {it['gate']} | "
            f"{it['kkp']} | {it['lhp']} | {it['aoi']} | {it['last']} | {it['age']} |"
        )
    lines.append("")
    lines.append("## Aksi yang disarankan")
    for it in items:
        actions = []
        if it["age"] == "MERAH":
            actions.append("last activity >10 hari - cek progress dengan tim")
        if it["kkp"] == 0 and it["lhp"] == 0:
            actions.append("belum ada output - lanjut Task 01/02b/03")
        if it["kkp"] > 0 and it["lhp"] == 0:
            actions.append("KKP siap - jalankan Task 04 untuk LHP")
        if it["aoi"] > 0 and it["lhp"] == 0:
            actions.append(f"{it['aoi']} AoI belum dituang ke LHP")
        if actions:
            lines.append(f"- **{it['nama']}**: " + "; ".join(actions))
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Dashboard penugasan aktif")
    ap.add_argument("--root", type=Path, default=Path("penugasan"))
    ap.add_argument("--save", action="store_true", help="tulis dashboard.md di audit-system-v4/")
    args = ap.parse_args()

    root = args.root
    if not root.exists():
        script_dir = Path(__file__).resolve().parent.parent
        root = script_dir / "penugasan"
    if not root.exists():
        print(f"Folder penugasan tidak ditemukan: {args.root}")
        return

    items = collect_penugasan(root)
    md = render_markdown(items, root)
    print(md)

    if args.save:
        out = Path(__file__).resolve().parent.parent / "dashboard.md"
        out.write_text(md, encoding="utf-8")
        print(f"\n[saved] {out}")


if __name__ == "__main__":
    main()
