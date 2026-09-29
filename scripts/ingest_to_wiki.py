#!/usr/bin/env python3
"""
ingest_to_wiki.py — Auto-ingest hasil penugasan ke wiki.

Dipanggil otomatis setelah event `LHP_FINALIZED` + `INTEGRAL_EXPORT` ada di
audit trail penugasan. Tugas:

1. Buat `wiki/wiki/lhp-{slug-penugasan}.md` (snapshot penugasan + temuan)
2. Re-aggregate `wiki/wiki/pattern-temuan.md` (gabungan v4 temuan + pattern-library/ lama)
3. Append ke `wiki/wiki/database-kp.md` (extract dari 00-input/KP-*)
4. Append ke `wiki/wiki/database-pkp.md` (extract dari 00-input/PKP-* + sasaran-assignment)
5. Append rekomendasi ke `wiki/wiki/tlhp-index.md`
6. Update kriteria yg dirujuk di `wiki/wiki/references-index.md`
7. Update aggregat di `wiki/wiki/audit-trail-overview.md`
8. Append entry ke `wiki/wiki/log.md`
9. Tulis 1 event INGEST_TO_WIKI ke audit trail penugasan

Pemakaian:
    python3 scripts/ingest_to_wiki.py --penugasan penugasan/2026-05-001-xxx
    python3 scripts/ingest_to_wiki.py --penugasan penugasan/2026-05-001-xxx --force  # bypass gate
    python3 scripts/ingest_to_wiki.py --re-aggregate-only                            # rebuild aggregator pages saja
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "wiki" / "wiki"
PATTERN_LIB_DIR = ROOT / "pattern-library"
PENUGASAN_DIR = ROOT / "penugasan"

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))
from audit_trail import log_event  # noqa: E402

WIB = timezone(timedelta(hours=7))


def _now_iso() -> str:
    return datetime.now(WIB).isoformat(timespec="seconds")


def _today() -> str:
    return datetime.now(WIB).strftime("%Y-%m-%d")


def _load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


def _slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", s.lower()).strip("-")


def _read_docx_text(path: Path) -> str:
    """Ekstraksi teks docx tanpa external lib."""
    import zipfile
    from xml.etree import ElementTree as ET
    try:
        with zipfile.ZipFile(path) as z:
            with z.open("word/document.xml") as f:
                tree = ET.parse(f)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        texts = [t.text or "" for t in tree.iter(f"{{{ns['w']}}}t")]
        return "\n".join(texts)
    except Exception:
        return ""


def _check_gate(pen_dir: Path, force: bool) -> tuple[bool, str]:
    """Cek apakah penugasan sudah LHP_FINALIZED + INTEGRAL_EXPORT."""
    events = _load_jsonl(pen_dir / "_AUDIT-TRAIL" / "events.jsonl")
    has_lhp = any(e.get("action") == "LHP_FINALIZED" for e in events)
    has_export = any(e.get("action") == "INTEGRAL_EXPORT" for e in events)
    if force:
        return True, "force=True (gate bypassed)"
    if has_lhp and has_export:
        return True, "LHP_FINALIZED + INTEGRAL_EXPORT terdeteksi"
    missing = []
    if not has_lhp: missing.append("LHP_FINALIZED")
    if not has_export: missing.append("INTEGRAL_EXPORT")
    return False, f"belum ada: {', '.join(missing)}"


# ---------------- ingest functions ----------------

def write_lhp_wiki_page(pen_dir: Path) -> Path:
    """Tulis wiki/wiki/lhp-{slug}.md untuk penugasan ini."""
    temuan_doc = _load_json(pen_dir / "_KKP" / "temuan.json") or {"temuan": [], "penugasan": {}}
    sasaran_doc = _load_json(pen_dir / "_PKP" / "sasaran-assignment.json") or {"sasaran": []}
    pinfo = temuan_doc.get("penugasan", {})

    slug = _slugify(pinfo.get("id", pen_dir.name))
    page_path = WIKI_DIR / f"lhp-{slug}.md"

    # Cari LHP docx
    lhp_files = list((pen_dir / "_LHP").glob("LHP*.docx")) if (pen_dir / "_LHP").exists() else []
    lhp_filename = lhp_files[0].name if lhp_files else "(tidak ada)"

    md = [
        f"# LHP — {pinfo.get('obyek', pen_dir.name)}",
        "",
        f"**Summary**: Snapshot penugasan **{pen_dir.name}** ({pinfo.get('jenis_pengawasan', '?')}). "
        f"LHP final tersusun dengan {len(temuan_doc.get('temuan', []))} temuan dari "
        f"{len(sasaran_doc.get('sasaran', []))} sasaran. Sudah disubmit ke INTEGRAL.",
        "",
        f"**Sources**: `penugasan/{pen_dir.name}/_KKP/temuan.json`, `_LHP/{lhp_filename}`, "
        f"`_PKP/sasaran-assignment.json`",
        "",
        f"**Last updated**: {_today()} (auto-ingested)",
        "",
        "---",
        "",
        "## Identitas Penugasan",
        "",
        "| Field | Nilai |",
        "|---|---|",
        f"| Nomor ST | {pinfo.get('nomor_st', '?')} |",
        f"| Tanggal ST | {pinfo.get('tanggal_st', '?')} |",
        f"| Obyek | {pinfo.get('obyek', '?')} |",
        f"| Jenis Pengawasan | {pinfo.get('jenis_pengawasan', '?')} |",
        f"| Folder Penugasan | `penugasan/{pen_dir.name}/` |",
        "",
    ]

    # Sasaran
    md += ["## Sasaran (dari PKP)", ""]
    if sasaran_doc.get("sasaran"):
        md += ["| Sasaran | Status | Anggota Tim | # Temuan |",
               "|---|---|---|---:|"]
        for s in sasaran_doc["sasaran"]:
            assignees = ", ".join(a["nama_lengkap"] for a in s.get("assigned_to", []))
            md.append(f"| **{s['sasaran_id']}** {s.get('deskripsi', '')[:60]} | "
                      f"{s.get('status', '?')} | {assignees} | "
                      f"{len(s.get('id_temuan_terkait', []))} |")
    else:
        md.append("_(sasaran tidak tercatat)_")
    md.append("")

    # Temuan
    md += ["## Temuan", ""]
    if temuan_doc.get("temuan"):
        for t in temuan_doc["temuan"]:
            md += [
                f"### {t['id_temuan']} — {t.get('judul_temuan', '?')}",
                "",
                f"**Sasaran terkait**: {t.get('sasaran_id', '?')}",
                f"**Anggota tim**: {t.get('anggota_tim', {}).get('nama_lengkap', '?')}",
                "",
                f"**Kondisi**: {t.get('kondisi', '?')}",
                "",
                f"**Kriteria**: {t.get('kriteria', '?')}",
                "",
            ]
            if t.get("sebab"):
                md += [f"**Sebab**: {t['sebab']}", ""]
            md += [
                f"**Akibat**: {t.get('akibat', '?')}",
                "",
                "**Dokumen Sumber**:",
            ]
            for d in t.get("dokumen_sumber", []):
                hal = f" hal. {d['halaman']}" if d.get("halaman") else ""
                md.append(f"- `{d.get('file', '?')}`{hal}")
            md.append("")
    else:
        md.append("_(tidak ada temuan)_")

    # Cross-link
    md += [
        "---",
        "## Cross-link",
        "",
        "- [[_INDEX-V4]]",
        "- [[pattern-temuan]]",
        "- [[database-kp]] · [[database-pkp]]",
        "- [[tlhp-index]]",
    ]

    page_path.write_text("\n".join(md), encoding="utf-8")
    return page_path


def collect_all_temuan() -> list[tuple[str, dict]]:
    """Iterasi semua penugasan v4 yang punya _KKP/temuan.json."""
    out = []
    if not PENUGASAN_DIR.exists():
        return out
    for pen in sorted(PENUGASAN_DIR.iterdir()):
        if not pen.is_dir():
            continue
        td = _load_json(pen / "_KKP" / "temuan.json")
        if not td:
            continue
        for t in td.get("temuan", []):
            out.append((pen.name, t))
    return out


def collect_pattern_lib() -> list[tuple[str, str, str]]:
    """Iterasi pattern-library/ lama. Return [(skill, file, judul)].
    Prioritas judul: frontmatter `judul:` -> first heading -> stem."""
    out = []
    if not PATTERN_LIB_DIR.exists():
        return out
    for skill_dir in PATTERN_LIB_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        for f in skill_dir.glob("P-*.md"):
            judul = f.stem
            try:
                lines = f.read_text(encoding="utf-8").splitlines()
                in_fm = False
                fm_judul = None
                heading = None
                for i, line in enumerate(lines):
                    if i == 0 and line.strip() == "---":
                        in_fm = True
                        continue
                    if in_fm and line.strip() == "---":
                        in_fm = False
                        continue
                    if in_fm:
                        if line.lower().startswith("judul:"):
                            fm_judul = line.split(":", 1)[1].strip()
                        continue
                    if heading is None and line.startswith("#"):
                        heading = line.lstrip("# ").strip()
                judul = fm_judul or heading or judul
            except Exception:
                pass
            out.append((skill_dir.name, f.name, judul))
    return out


def regenerate_pattern_temuan() -> Path:
    page = WIKI_DIR / "pattern-temuan.md"
    pattern_lib = collect_pattern_lib()
    all_temuan = collect_all_temuan()

    # Aggregate by judul similarity (simple: first 6 words lowercase)
    def keyish(judul: str) -> str:
        words = re.findall(r"\w+", judul.lower())[:6]
        return " ".join(words)

    grouped = defaultdict(list)
    for pen, t in all_temuan:
        grouped[keyish(t.get("judul_temuan", ""))].append((pen, t))

    md = [
        "# Pattern Temuan — Aggregator Otomatis",
        "",
        f"**Summary**: Aggregat pattern temuan dari {len(all_temuan)} temuan di seluruh penugasan v4 + "
        f"{len(pattern_lib)} pattern dari `pattern-library/` (manual curated).",
        "",
        "**Sources**: di-aggregate dari `penugasan/*/_KKP/temuan.json` + `pattern-library/`.",
        "",
        f"**Last updated**: {_today()} (auto-aggregated)",
        "",
        "---",
        "",
        "## Pattern dari pattern-library/ (manual curated)",
        "",
    ]
    if pattern_lib:
        md += ["| Pattern ID | Skill | Judul |", "|---|---|---|"]
        for skill, fname, judul in pattern_lib:
            pid = fname.replace(".md", "")
            md.append(f"| `{pid}` | {skill} | {judul} |")
    else:
        md.append("_(belum ada pattern di pattern-library/)_")
    md.append("")

    md += ["", "## Pattern dari Penugasan v4 (auto-aggregated)", ""]

    # Top patterns (freq >= 2)
    md += ["### Top Pattern (frekuensi ≥ 2)", "",
           "| Auto-ID | Frekuensi | Standar/Kriteria | Judul Representatif | Penugasan |",
           "|---|---:|---|---|---|"]
    top_count = 0
    for i, (key, items) in enumerate(sorted(grouped.items(), key=lambda kv: -len(kv[1])), 1):
        if len(items) < 2:
            continue
        repr_temuan = items[0][1]
        sample_pen = ", ".join(p for p, _ in items[:3]) + (" ..." if len(items) > 3 else "")
        md.append(f"| AUTO-{i:03d} | {len(items)} | {repr_temuan.get('kriteria','')[:60]}... | "
                  f"{repr_temuan.get('judul_temuan','')[:80]} | {sample_pen} |")
        top_count += 1
    if top_count == 0:
        md.append("| _(belum ada pattern berulang)_ | | | | |")
    md.append("")

    # Single patterns
    md += ["### Pattern Tunggal (frekuensi = 1)", "",
           "| Penugasan | id_temuan | Judul | Kriteria | Anggota |",
           "|---|---|---|---|---|"]
    single_count = 0
    for key, items in grouped.items():
        if len(items) != 1:
            continue
        pen, t = items[0]
        md.append(f"| {pen} | {t.get('id_temuan','?')} | {t.get('judul_temuan','')[:80]} | "
                  f"{t.get('kriteria','')[:60]}... | "
                  f"{t.get('anggota_tim',{}).get('nama_lengkap','?')} |")
        single_count += 1
    if single_count == 0:
        md.append("| _(belum ada)_ | | | | |")

    md += ["", "---", "", "## Cara Pakai",
           "",
           "1. **Sebelum mulai analisis KKP** (Task 03), lihat halaman ini untuk pola yang sering muncul.",
           "2. **Saat menemukan kasus mirip**, kutip pattern di field `dokumen_sumber.kutipan`.",
           "3. **Pattern yang stable** (≥ 3 penugasan) bisa di-promote ke `pattern-library/[skill]/`.",
           "",
           "## Cross-link",
           "",
           "- [[_INDEX-V4]] · [[references-index]] · [[audit-trail-overview]]"]

    page.write_text("\n".join(md), encoding="utf-8")
    return page


def collect_pkp_kp_per_penugasan() -> list[dict]:
    """Iterasi penugasan: extract metadata KP/PKP + sasaran-assignment ringkas."""
    rows = []
    if not PENUGASAN_DIR.exists():
        return rows
    for pen in sorted(PENUGASAN_DIR.iterdir()):
        if not pen.is_dir():
            continue
        input_dir = pen / "00-input"
        kp_files = sorted(input_dir.glob("KP-*.*")) if input_dir.exists() else []
        pkp_files = sorted(input_dir.glob("PKP-*.*")) if input_dir.exists() else []
        sasaran_doc = _load_json(pen / "_PKP" / "sasaran-assignment.json")
        temuan_doc = _load_json(pen / "_KKP" / "temuan.json")
        pinfo = (temuan_doc or {}).get("penugasan", {})

        sasaran = (sasaran_doc or {}).get("sasaran", [])
        anggota_set = set()
        for s in sasaran:
            for a in s.get("assigned_to", []):
                anggota_set.add(a.get("nama_lengkap", "?"))

        rows.append({
            "penugasan": pen.name,
            "jenis_pengawasan": pinfo.get("jenis_pengawasan", "?"),
            "nomor_st": pinfo.get("nomor_st", "?"),
            "tanggal_st": pinfo.get("tanggal_st", "?"),
            "obyek": pinfo.get("obyek", "?"),
            "kp_files": [f.name for f in kp_files],
            "pkp_files": [f.name for f in pkp_files],
            "n_sasaran": len(sasaran),
            "n_anggota": len(anggota_set),
            "sample_sasaran": sasaran[0].get("deskripsi", "")[:80] if sasaran else "",
        })
    return rows


def regenerate_database_kp() -> Path:
    page = WIKI_DIR / "database-kp.md"
    rows = collect_pkp_kp_per_penugasan()

    md = [
        "# Database Kartu Penugasan (KP)",
        "",
        f"**Summary**: Database KP yang sudah pernah dipakai di sistem audit-system-v4 "
        f"({len(rows)} penugasan ter-ingest).",
        "",
        "**Sources**: di-extract dari `penugasan/*/00-input/KP-*` oleh `scripts/ingest_to_wiki.py`.",
        "",
        f"**Last updated**: {_today()} (auto-aggregated)",
        "",
        "---",
        "",
        "## Konteks v4",
        "",
        "Sejak v4 (Mei 2026), KP dikerjakan manual oleh ketua tim di sistem INTEGRAL. "
        "Auditor mengunduh KP final dari INTEGRAL dan meletakkannya di `00-input/`. "
        "Sistem v4 hanya membaca dan mengarsipkan KP — tidak generate.",
        "",
        "Database ini berfungsi sebagai library KP terpakai — siapa saja boleh referensi saat "
        "menyusun KP baru di INTEGRAL.",
        "",
        "---",
        "",
        "## Index KP per Jenis Pengawasan",
        "",
    ]

    by_jenis = defaultdict(list)
    for r in rows:
        by_jenis[r["jenis_pengawasan"]].append(r)

    JENIS_ORDER = [
        "audit-pengadaan", "audit-kinerja", "reviu-pengadaan", "reviu-rka-kl",
        "pemantauan-pengadaan", "pemantauan-tindak-lanjut",
        "evaluasi-sakip", "evaluasi-spip", "evaluasi-reformasi-birokrasi",
        "evaluasi-manajemen-risiko", "konsultasi-pengadaan", "?",
    ]
    for jenis in JENIS_ORDER:
        items = by_jenis.get(jenis, [])
        if not items and jenis == "?":
            continue
        md += [f"### {jenis}", ""]
        if items:
            md += ["| Penugasan | Nomor ST | Tanggal | KP file | Obyek |",
                   "|---|---|---|---|---|"]
            for r in items:
                kp = ", ".join(r["kp_files"]) if r["kp_files"] else "_(belum ada)_"
                md.append(f"| [[lhp-{_slugify(r['penugasan'])}]] | {r['nomor_st']} | "
                          f"{r['tanggal_st']} | `{kp}` | {r['obyek'][:50]} |")
        else:
            md.append("_(belum ada)_")
        md.append("")

    md += [
        "---",
        "",
        "## Statistik Agregat",
        "",
        "| Metrik | Nilai |",
        "|---|---|",
        f"| Total KP terkumpul | {sum(len(r['kp_files']) for r in rows)} |",
        f"| Total penugasan ter-ingest | {len(rows)} |",
        "",
        "## Cross-link",
        "",
        "- [[database-pkp]] · [[_INDEX-V4]] · [[references-index]]",
    ]
    page.write_text("\n".join(md), encoding="utf-8")
    return page


def regenerate_database_pkp() -> Path:
    page = WIKI_DIR / "database-pkp.md"
    rows = collect_pkp_kp_per_penugasan()

    md = [
        "# Database Program Kerja Pengawasan (PKP)",
        "",
        f"**Summary**: Database PKP dari {len(rows)} penugasan v4. "
        f"Setiap PKP di-extract jadi `_PKP/sasaran-assignment.json` (pembagian sasaran).",
        "",
        "**Sources**: `penugasan/*/00-input/PKP-*` + `_PKP/sasaran-assignment.json`.",
        "",
        f"**Last updated**: {_today()} (auto-aggregated)",
        "",
        "---",
        "",
        "## Index PKP per Jenis Pengawasan",
        "",
    ]

    by_jenis = defaultdict(list)
    for r in rows:
        by_jenis[r["jenis_pengawasan"]].append(r)

    JENIS_ORDER = [
        "audit-pengadaan", "audit-kinerja", "reviu-pengadaan", "reviu-rka-kl",
        "pemantauan-pengadaan", "pemantauan-tindak-lanjut",
        "evaluasi-sakip", "evaluasi-spip", "evaluasi-reformasi-birokrasi",
        "evaluasi-manajemen-risiko", "konsultasi-pengadaan", "?",
    ]
    for jenis in JENIS_ORDER:
        items = by_jenis.get(jenis, [])
        if not items and jenis == "?":
            continue
        md += [f"### {jenis}", ""]
        if items:
            md += ["| Penugasan | PKP file | # Sasaran | # Anggota | Sample sasaran |",
                   "|---|---|---:|---:|---|"]
            for r in items:
                pkp = ", ".join(r["pkp_files"]) if r["pkp_files"] else "_(belum)_"
                md.append(f"| [[lhp-{_slugify(r['penugasan'])}]] | `{pkp}` | "
                          f"{r['n_sasaran']} | {r['n_anggota']} | {r['sample_sasaran']} |")
        else:
            md.append("_(belum ada)_")
        md.append("")

    # Pola pembagian sasaran
    md += ["---", "", "## Pola Pembagian Sasaran", "",
           "| Jenis Pengawasan | Median Sasaran | Median Anggota | n |",
           "|---|---:|---:|---:|"]
    import statistics
    for jenis, items in by_jenis.items():
        if jenis == "?":
            continue
        med_s = int(statistics.median([r["n_sasaran"] for r in items])) if items else 0
        med_a = int(statistics.median([r["n_anggota"] for r in items])) if items else 0
        md.append(f"| {jenis} | {med_s} | {med_a} | {len(items)} |")

    md += ["", "## Cross-link", "", "- [[database-kp]] · [[_INDEX-V4]] · [[pattern-temuan]]"]
    page.write_text("\n".join(md), encoding="utf-8")
    return page


def regenerate_tlhp_index() -> Path:
    """Extract rekomendasi dari LHP docx + temuan.json setiap penugasan."""
    page = WIKI_DIR / "tlhp-index.md"
    rows = []
    if PENUGASAN_DIR.exists():
        for pen in sorted(PENUGASAN_DIR.iterdir()):
            if not pen.is_dir():
                continue
            temuan_doc = _load_json(pen / "_KKP" / "temuan.json")
            pinfo = (temuan_doc or {}).get("penugasan", {})
            # Rekomendasi: extract dari LHP docx (cari section "Rekomendasi")
            lhp_files = list((pen / "_LHP").glob("LHP*.docx")) if (pen / "_LHP").exists() else []
            rekomendasi = []
            if lhp_files:
                txt = _read_docx_text(lhp_files[0])
                # extract paragraf setelah heading "Rekomendasi"
                m = re.search(r"Rekomendasi(.{0,3000})", txt, re.IGNORECASE | re.DOTALL)
                if m:
                    chunk = m.group(1)
                    # cari poin: "1. ...", "2. ..." dan dedupe (LHP dummy bisa berulang)
                    seen = set()
                    for nm in re.finditer(r"^\s*\d+\.\s*([^\n]{20,200})", chunk, re.MULTILINE):
                        rek_text = nm.group(1).strip()
                        norm = rek_text.lower()[:80]
                        if norm not in seen:
                            seen.add(norm)
                            rekomendasi.append(rek_text)
            for i, rek in enumerate(rekomendasi[:10], 1):
                rows.append({
                    "rek_id": f"REK-{_slugify(pen.name)[:20]}-{i:02d}",
                    "penugasan": pen.name,
                    "auditi": pinfo.get("obyek", "?"),
                    "rekomendasi": rek,
                    "status": "BELUM_DITINDAKLANJUTI",
                    "deadline": "(TBD oleh auditor)",
                })

    md = [
        "# Index Tindak Lanjut Hasil Pengawasan (TLHP)",
        "",
        f"**Summary**: {len(rows)} rekomendasi dari LHP penugasan v4 yang sudah final. "
        f"Status TL di-update manual oleh tim Pemantauan TLHP.",
        "",
        "**Sources**: di-extract dari `_LHP/LHP-SUBSTANSI*.docx` + `_KKP/temuan.json`.",
        "",
        f"**Last updated**: {_today()} (auto-aggregated)",
        "",
        "---",
        "",
        "## Status TLHP",
        "",
        "| Status | Arti |",
        "|---|---|",
        "| `BELUM_DITINDAKLANJUTI` | Auditi belum mulai TL |",
        "| `SEDANG_DITINDAKLANJUTI` | Auditi sudah mulai action plan, belum selesai |",
        "| `SELESAI_DITINDAKLANJUTI` | Auditi mengirim bukti TL, di-verifikasi |",
        "| `DITERIMA_KETUA_TIM` | TL dianggap memuaskan |",
        "| `DITUTUP` | TL final, siap dilaporkan ke Itjen / BPK |",
        "",
        "---",
        "",
        "## Index Rekomendasi",
        "",
        "| ID Rek | Penugasan | Auditi | Rekomendasi (singkat) | Status | Deadline |",
        "|---|---|---|---|---|---|",
    ]
    if rows:
        for r in rows:
            md.append(f"| `{r['rek_id']}` | [[lhp-{_slugify(r['penugasan'])}]] | "
                      f"{r['auditi']} | {r['rekomendasi'][:80]} | "
                      f"{r['status']} | {r['deadline']} |")
    else:
        md.append("| _(belum ada — perlu LHP dengan section Rekomendasi)_ | | | | | |")

    md += [
        "",
        "## Statistik",
        "",
        f"- Total rekomendasi: **{len(rows)}**",
        f"- BELUM_DITINDAKLANJUTI: **{sum(1 for r in rows if r['status'] == 'BELUM_DITINDAKLANJUTI')}**",
        "",
        "## Cross-link",
        "",
        "- [[_INDEX-V4]] · [[pattern-temuan]] · [[tlhp-internal-simwas-ir2]] · [[tlhp-eksternal-simwas-ir2]]",
    ]
    page.write_text("\n".join(md), encoding="utf-8")
    return page


def regenerate_references_index() -> Path:
    """Aggregate kriteria dari semua temuan.json."""
    page = WIKI_DIR / "references-index.md"
    all_temuan = collect_all_temuan()
    krit_freq = Counter()
    krit_pen = defaultdict(set)
    for pen, t in all_temuan:
        krit = t.get("kriteria", "").strip()
        # Ambil first 80 char sebagai key
        key = krit[:80]
        if key:
            krit_freq[key] += 1
            krit_pen[key].add(pen)

    # Read existing manual sections (preserve A-F static), regenerate auto section
    existing = ""
    if page.exists():
        existing = page.read_text(encoding="utf-8")

    # Cari section auto
    auto_marker = "## Reference yang Sering Dirujuk di Temuan (auto-aggregated)"

    # Build new auto section
    new_auto = [auto_marker, "",
                "> _Di-regenerate oleh `scripts/ingest_to_wiki.py`. Frekuensi dihitung dari field `kriteria`._",
                "",
                "| Reference (truncated 80) | Frekuensi | Penugasan terkait |",
                "|---|---:|---|"]
    for k, freq in krit_freq.most_common(20):
        pens = ", ".join(sorted(krit_pen[k])[:3])
        if len(krit_pen[k]) > 3:
            pens += f" (+{len(krit_pen[k])-3})"
        new_auto.append(f"| {k} | {freq} | {pens} |")
    if not krit_freq:
        new_auto.append("| _(belum ada)_ | | |")
    new_auto += ["", f"_(updated {_today()})_", ""]

    if auto_marker in existing:
        # replace section auto sampai "---" berikutnya atau EOF
        idx = existing.index(auto_marker)
        # cari "---" setelah marker
        rest = existing[idx:]
        next_sep = rest.find("\n---\n", len(auto_marker))
        if next_sep > 0:
            new_text = existing[:idx] + "\n".join(new_auto) + "\n" + rest[next_sep:]
        else:
            new_text = existing[:idx] + "\n".join(new_auto)
    else:
        new_text = (existing or "# Index Reference yang Dipakai Sistem Audit v4\n\n") + "\n" + "\n".join(new_auto)

    page.write_text(new_text, encoding="utf-8")
    return page


def regenerate_audit_trail_overview() -> Path:
    """Aggregate event dari semua _AUDIT-TRAIL/events.jsonl."""
    page = WIKI_DIR / "audit-trail-overview.md"
    action_counter = Counter()
    pen_summary = []
    if PENUGASAN_DIR.exists():
        for pen in sorted(PENUGASAN_DIR.iterdir()):
            if not pen.is_dir():
                continue
            events = _load_jsonl(pen / "_AUDIT-TRAIL" / "events.jsonl")
            if not events:
                continue
            for e in events:
                action_counter[e.get("action", "?")] += 1
            last = events[-1]
            stage = "LHP_FINAL" if any(e.get("action") == "LHP_FINALIZED" for e in events) else \
                    "KKP" if any(e.get("action") == "KKP_TEMUAN_ADDED" for e in events) else "INISIASI"
            pen_summary.append({
                "penugasan": pen.name,
                "stage": stage,
                "n_events": len(events),
                "last": last.get("timestamp", "?"),
                "status": "DONE" if any(e.get("action") == "INTEGRAL_EXPORT" for e in events) else "ACTIVE",
            })

    existing = page.read_text(encoding="utf-8") if page.exists() else ""

    # Build aggregat sections (dipisah marker)
    auto_action_marker = "### Total Events per Action"
    auto_pen_marker = "### Penugasan Aktif & Selesai"

    new_action_section = [auto_action_marker, "",
                          "| Action | Total Events |", "|---|---:|"]
    for act, n in action_counter.most_common():
        new_action_section.append(f"| `{act}` | {n} |")
    if not action_counter:
        new_action_section.append("| _(belum ada)_ | 0 |")
    new_action_section.append("")

    new_pen_section = [auto_pen_marker, "",
                       "| Penugasan | Stage | Total Events | Last Event | Status |",
                       "|---|---|---:|---|---|"]
    for r in pen_summary:
        new_pen_section.append(f"| {r['penugasan']} | {r['stage']} | {r['n_events']} | "
                               f"{r['last']} | {r['status']} |")
    if not pen_summary:
        new_pen_section.append("| _(belum ada)_ | | | | |")
    new_pen_section += ["", f"_(updated {_today()})_", ""]

    # Replace di existing text
    def replace_section(text: str, marker: str, new_lines: list[str]) -> str:
        if marker not in text:
            return text + "\n" + "\n".join(new_lines)
        idx = text.index(marker)
        rest = text[idx:]
        next_h = re.search(r"\n(?:###|##|---)\s", rest[len(marker):])
        end = idx + len(marker) + (next_h.start() if next_h else len(rest))
        return text[:idx] + "\n".join(new_lines) + "\n" + text[end:]

    new_text = replace_section(existing, auto_action_marker, new_action_section)
    new_text = replace_section(new_text, auto_pen_marker, new_pen_section)
    page.write_text(new_text, encoding="utf-8")
    return page


def append_log(pen_name: str, files_written: list[str]) -> None:
    log = WIKI_DIR / "log.md"
    line = f"- {_today()} **ingest** `{pen_name}` → {len(files_written)} files written/updated\n"
    if log.exists():
        content = log.read_text(encoding="utf-8")
    else:
        content = "# Wiki Operations Log\n\n_Append-only_\n\n"
    log.write_text(content + line, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--penugasan", help="Path folder penugasan untuk di-ingest.")
    ap.add_argument("--force", action="store_true", help="Bypass gate LHP_FINALIZED+INTEGRAL_EXPORT.")
    ap.add_argument("--re-aggregate-only", action="store_true",
                    help="Hanya regenerate halaman aggregator (pattern, db-kp, db-pkp, tlhp, refs, trail).")
    args = ap.parse_args()

    files_written = []

    if args.re_aggregate_only:
        print("[ingest] re-aggregate-only mode")
        files_written += [str(regenerate_pattern_temuan().relative_to(ROOT))]
        files_written += [str(regenerate_database_kp().relative_to(ROOT))]
        files_written += [str(regenerate_database_pkp().relative_to(ROOT))]
        files_written += [str(regenerate_tlhp_index().relative_to(ROOT))]
        files_written += [str(regenerate_references_index().relative_to(ROOT))]
        files_written += [str(regenerate_audit_trail_overview().relative_to(ROOT))]
        for f in files_written:
            print(f"  -> {f}")
        return 0

    if not args.penugasan:
        sys.stderr.write("Wajib --penugasan atau --re-aggregate-only.\n")
        return 1

    pen_dir = Path(args.penugasan)
    if not pen_dir.exists():
        sys.stderr.write(f"Folder tidak ada: {pen_dir}\n")
        return 1

    ok, why = _check_gate(pen_dir, args.force)
    if not ok:
        sys.stderr.write(f"[ingest] DITUNDA — gate belum terpenuhi: {why}\n")
        sys.stderr.write("  Tunggu sampai ada event LHP_FINALIZED + INTEGRAL_EXPORT, atau --force.\n")
        return 2

    print(f"[ingest] gate OK ({why}). Mulai ingest {pen_dir.name}...")

    # 1. Per-penugasan page
    p = write_lhp_wiki_page(pen_dir)
    files_written.append(str(p.relative_to(ROOT)))
    print(f"  -> {p.relative_to(ROOT)}")

    # 2-7. Aggregator pages

    # 2-7. Aggregator pages
    for fn in (regenerate_pattern_temuan, regenerate_database_kp, regenerate_database_pkp,
               regenerate_tlhp_index, regenerate_references_index, regenerate_audit_trail_overview):
        p = fn()
        files_written.append(str(p.relative_to(ROOT)))
        print(f"  -> {p.relative_to(ROOT)}")

    # 8. Log
    append_log(pen_dir.name, files_written)
    print(f"  -> wiki/wiki/log.md (appended)")

    # 9. Audit trail

    # 9. Audit trail (compact form to avoid sync truncation)
    payload = {"files_written": len(files_written)}
    log_event(pen_dir, action="INGEST_TO_WIKI",
              target=f"wiki/wiki/lhp-{_slugify(pen_dir.name)}.md",
              payload=payload, task="04")

    # 10. Auto-rebuild dashboard
    try:
        import build_dashboard
        build_dashboard.main()
        print("  -> dashboard.html (sistem+wiki)")
    except Exception as e:
        print(f"  [warn] dashboard: {e}")

    print(f"[ingest] selesai. {len(files_written)} file ditulis.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
