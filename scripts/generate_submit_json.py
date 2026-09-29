"""
generate_submit_json.py — Generator paket submit JSON untuk Integral.

Setelah pipeline (run_batch.py) selesai, dipanggil untuk mengumpulkan output
penugasan ke dalam satu file JSON terstruktur yang siap ditarik Integral.

Schema mengikuti 8 tahapan Integral (SIMWAS v2 Komdigi):
  1. kartu_penugasan
  2. pkp
  3. kertas_kerja[] (per anggota tim)
  4. lrs_kk (auto-fill dari KKP)
  5. konsep_laporan (LHP draft)
  6. bukti_cek_ai (metadata AI execution)
  7. lrs_lhp (placeholder — diisi PT manual)
  8. laporan_hasil (placeholder — diisi setelah review)

Usage:
    python3 generate_submit_json.py \
        --penugasan PATH_FOLDER_PENUGASAN \
        [--skill SKILL_NAME] \
        [--model MODEL_NAME] \
        [--auditor AUDITOR_ID]

Output:
    <penugasan>/_SUBMIT/submit-{timestamp}.json
    <penugasan>/_SUBMIT/submit-latest.json (symlink/copy)

Idempotent: submit_id berbasis SHA-256 hash of all input file hashes — submit
dengan paket identik menghasilkan submit_id sama.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"
WIB = timezone(timedelta(hours=7))


def _self_check_ast() -> None:
    try:
        ast.parse(Path(__file__).read_text(encoding="utf-8"))
    except SyntaxError as e:
        print(f"[FATAL] Self-check AST gagal di {__file__}: {e}", file=sys.stderr)
        sys.exit(2)


# ---------- helpers ----------

def sha256_file(path: Path) -> str:
    """Compute SHA-256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def file_meta(path: Path, role: str, **extras) -> dict:
    """Build file metadata dict."""
    if not path.exists():
        return {"role": role, "path": str(path), "exists": False, **extras}
    stat = path.stat()
    return {
        "role": role,
        "path": str(path),
        "filename": path.name,
        "sha256": sha256_file(path),
        "size_bytes": stat.st_size,
        "mtime": datetime.fromtimestamp(stat.st_mtime, WIB).isoformat(),
        **extras,
    }


def load_json_safe(path: Path) -> dict | list | None:
    """Load JSON file or return None if missing/invalid."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"[WARN] Failed to load {path}: {e}", file=sys.stderr)
        return None


def load_context_md(penugasan: Path) -> dict[str, str]:
    """Parse context.md as YAML-like key:value pairs.

    Format toleran: each line `Key: value`, headers ditolerir.
    """
    ctx_path = penugasan / "context.md"
    if not ctx_path.exists():
        return {}
    out: dict[str, str] = {}
    in_frontmatter = False
    fm_lines: list[str] = []
    body_lines: list[str] = []
    for line in ctx_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            fm_lines.append(line)
        else:
            body_lines.append(line)
    # Parse frontmatter or whole body for `key: value` patterns
    for line in fm_lines + body_lines:
        if ":" in line and not line.lstrip().startswith("#"):
            k, _, v = line.partition(":")
            k = k.strip().strip("-").strip().lower().replace(" ", "_")
            v = v.strip().strip('"').strip("'")
            if k and v and k not in out:
                out[k] = v
    return out


def parse_komposisi_tim(ctx: dict[str, str]) -> dict:
    """Extract komposisi tim dari context.md."""
    def _person(key: str) -> dict | None:
        val = ctx.get(key) or ctx.get(key.replace("_", "-"))
        if not val:
            return None
        # format: "Nama (NIP: 123456)" atau cuma "Nama"
        if "(" in val and "NIP" in val:
            nama, _, rest = val.partition("(")
            nip = rest.split("NIP")[1].strip(": )").strip()
            return {"nama": nama.strip(), "nip": nip}
        return {"nama": val, "nip": None}

    return {
        "penanggung_jawab": _person("penanggung_jawab") or _person("inspektur"),
        "pengendali_mutu": _person("pengendali_mutu") or _person("dalwas"),
        "pengendali_teknis": _person("pengendali_teknis"),
        "ketua_tim": _person("ketua_tim"),
        "anggota_tim": [
            _person(k) for k in ("anggota_tim_1", "anggota_tim_2", "anggota_tim_3", "anggota_tim_4")
            if _person(k)
        ],
    }


# ---------- per-tahapan builders ----------

def build_kartu_penugasan(penugasan: Path, ctx: dict, meta: dict) -> dict:
    """Tahapan 1: Kartu Penugasan."""
    nomor_st = ctx.get("nomor_st") or ctx.get("nomor_surat_tugas") or "TBD"
    return {
        "nomor_kp": f"KP/{nomor_st}",
        "nomor_st": nomor_st,
        "judul_pengawasan": ctx.get("judul_pengawasan") or ctx.get("judul") or "",
        "dasar_pengawasan": ctx.get("dasar_pengawasan") or ctx.get("dasar") or "",
        "tingkat_risiko": ctx.get("tingkat_risiko") or "Sedang",
        "tujuan_pengawasan": ctx.get("tujuan_pengawasan") or ctx.get("tujuan") or "",
        "sasaran_pengawasan": [
            ctx[k] for k in sorted(ctx.keys()) if k.startswith("sasaran") and ctx[k]
        ] or [ctx.get("sasaran", "")],
        "ruang_lingkup": ctx.get("ruang_lingkup") or "",
        "komposisi_tim": parse_komposisi_tim(ctx),
        "tanggal_mulai": ctx.get("tanggal_mulai") or meta.get("tanggal_mulai"),
        "tanggal_selesai": ctx.get("tanggal_selesai") or meta.get("tanggal_selesai"),
        "lampiran": _find_lampiran(penugasan, ["kartu-penugasan", "ST", "surat-tugas"], ext_priority=[".docx", ".pdf"]),
    }


def build_pkp(penugasan: Path, ctx: dict, meta: dict) -> dict:
    """Tahapan 2: PKP (Program Kerja Pengawasan)."""
    pkp_dir = penugasan / "_PKP"
    nomor_st = ctx.get("nomor_st") or "TBD"
    sasaran_assignment = load_json_safe(pkp_dir / "sasaran-assignment.json") or {}

    langkah_kerja: list[dict] = []
    if isinstance(sasaran_assignment, dict) and "sasaran" in sasaran_assignment:
        for sas in sasaran_assignment.get("sasaran", []):
            langkah_kerja.append({
                "fase": "II. Pelaksanaan",
                "sasaran_id": sas.get("id"),
                "sasaran_text": sas.get("text", ""),
                "langkah_detail": sas.get("langkah_kerja", []),
                "dilaksanakan_oleh": sas.get("auditor"),
                "waktu": sas.get("tanggal"),
                "kkp_ref": sas.get("kkp_ref"),
            })

    return {
        "nomor_pkp": f"PKP/{nomor_st}",
        "judul_pengawasan": ctx.get("judul_pengawasan", ""),
        "tujuan_pengawasan": ctx.get("tujuan_pengawasan", ""),
        "langkah_kerja": langkah_kerja or [{"fase": "I. Perencanaan",
                                              "langkah": "Menyusun PKP",
                                              "dilaksanakan_oleh": "Ketua Tim",
                                              "waktu": ctx.get("tanggal_mulai")}],
        "lampiran": _find_lampiran(penugasan, ["pkp", "PKP"], ext_priority=[".docx"], folder="_PKP"),
    }


def build_kertas_kerja(penugasan: Path, ctx: dict, meta: dict) -> list[dict]:
    """Tahapan 3: Kertas Kerja per anggota tim."""
    kkp_dir = penugasan / "_KKP"
    nomor_st = ctx.get("nomor_st") or "TBD"

    # Cari semua file temuan/anomalies sebagai sumber temuan_rekomendasi
    anomalies_master = load_json_safe(kkp_dir / "anomalies-master.json") or load_json_safe(kkp_dir / "anomalies.json") or {}
    anomalies = anomalies_master.get("anomalies", []) if isinstance(anomalies_master, dict) else []

    # Cari KKP per anggota — convention: render_kkp.py menghasilkan KKP-{N}-{nama}.docx
    kkp_files = sorted(kkp_dir.glob("KKP-*.docx")) if kkp_dir.exists() else []

    # Komposisi tim untuk mapping anggota
    komposisi = parse_komposisi_tim(ctx)
    anggota_list = komposisi.get("anggota_tim", [])
    if not anggota_list and komposisi.get("ketua_tim"):
        anggota_list = [komposisi["ketua_tim"]]

    # Kalau tidak ada KKP file fisik tapi ada anomalies, buat 1 KKP gabungan
    if not kkp_files and anomalies:
        return [{
            "nomor_kkp": f"KKP-1/{nomor_st}",
            "disusun_oleh": (anggota_list[0] or {}).get("nama") if anggota_list else "Tim",
            "tanggal": datetime.now(WIB).date().isoformat(),
            "sasaran": [{"id": i+1, "text": s, "status": "selesai"}
                        for i, s in enumerate(ctx.get("sasaran_pengawasan_list", [ctx.get("sasaran", "")]))],
            "langkah_kerja": [],
            "temuan_rekomendasi": _anomalies_to_temuan(anomalies),
            "status_kkp": "ditutup" if anomalies else "draft",
            "lampiran": [],
        }]

    # Kalau ada KKP file, mapping per file
    out: list[dict] = []
    for i, kkp_path in enumerate(kkp_files):
        anggota = anggota_list[i] if i < len(anggota_list) else {"nama": "Anggota Tim"}
        out.append({
            "nomor_kkp": f"KKP-{i+1}/{nomor_st}",
            "disusun_oleh": anggota.get("nama"),
            "nip_anggota": anggota.get("nip"),
            "tanggal": datetime.fromtimestamp(kkp_path.stat().st_mtime, WIB).date().isoformat(),
            "sasaran": [{"id": i+1, "text": s, "status": "selesai"}
                        for i, s in enumerate(ctx.get("sasaran_pengawasan_list", []))],
            "langkah_kerja": [],
            "temuan_rekomendasi": _anomalies_to_temuan(anomalies, filter_by_anggota=anggota.get("nama")),
            "status_kkp": "ditutup",
            "tanggal_tutup": datetime.fromtimestamp(kkp_path.stat().st_mtime, WIB).isoformat(),
            "lampiran": [file_meta(kkp_path, role=f"kkp-{i+1}")],
        })
    return out


def _anomalies_to_temuan(anomalies: list[dict], filter_by_anggota: str | None = None) -> list[dict]:
    """Convert pipeline anomalies ke schema temuan Integral."""
    out: list[dict] = []
    for i, anom in enumerate(anomalies, 1):
        if filter_by_anggota and anom.get("anggota") and anom.get("anggota") != filter_by_anggota:
            continue
        out.append({
            "no": i,
            "referensi_sasaran": anom.get("aspek") or anom.get("kategori") or "—",
            "judul_temuan": anom.get("judul") or anom.get("rule_id", "Temuan"),
            "kodefikasi_temuan": anom.get("rule_id", "—"),
            "kondisi": anom.get("deskripsi") or anom.get("kondisi", "—"),
            "kriteria": anom.get("kriteria", "—"),
            "kodefikasi_penyebab": "—",
            "penyebab": anom.get("sebab") or anom.get("penyebab", "—"),
            "akibat": anom.get("akibat", "—"),
            "kodefikasi_rekomendasi": "—",
            "uraian_rekomendasi": anom.get("rekomendasi") or anom.get("draft_catatan", "—"),
            "severity": anom.get("severity", "INFO"),
        })
    return out


def build_konsep_laporan(penugasan: Path, ctx: dict, meta: dict) -> dict:
    """Tahapan 5: Konsep Laporan (LHP/LHA/LHE/LHR draft)."""
    lhp_dir = penugasan / "_LHP"
    # cari draft yang dihasilkan run_batch.py
    candidates = []
    if lhp_dir.exists():
        for pattern in ["LHA-DRAFT.docx", "LHR-DRAFT.docx", "LHE-DRAFT.docx", "Laporan-Pemantauan-DRAFT.docx", "*-DRAFT.docx"]:
            candidates.extend(lhp_dir.glob(pattern))
    candidates = list(dict.fromkeys(candidates))  # dedup

    lampiran = [file_meta(p, role="konsep-laporan") for p in candidates]
    return {
        "filename": candidates[0].name if candidates else None,
        "url_drive": None,
        "tanggal_unggah": datetime.fromtimestamp(candidates[0].stat().st_mtime, WIB).isoformat() if candidates else None,
        "lampiran": lampiran,
    }


def build_bukti_cek_ai(penugasan: Path, ctx: dict, meta: dict, skill: str, model: str) -> dict:
    """Tahapan 6: Bukti Cek AI — metadata pipeline + dokumen bukti."""
    audit_trail_dir = penugasan / "_AUDIT-TRAIL"
    bukti_dir = penugasan / "_BUKTI-AI"
    bukti_dir.mkdir(parents=True, exist_ok=True)

    # cari dokumen bukti yang sudah dihasilkan generate_bukti_ai_docx.py
    bukti_docx = list(bukti_dir.glob("Bukti-Cek-AI-*.docx"))
    bukti_docx.sort(key=lambda p: p.stat().st_mtime, reverse=True)

    return {
        "filename": bukti_docx[0].name if bukti_docx else None,
        "tanggal_unggah": datetime.fromtimestamp(bukti_docx[0].stat().st_mtime, WIB).isoformat() if bukti_docx else None,
        "lampiran": [file_meta(p, role="bukti-cek-ai") for p in bukti_docx[:1]],
        "metadata_ai": {
            "skill": f"{skill}@{meta.get('skill_version', 'v1.0')}" if skill else (meta.get("skill", "?")),
            "model": model or meta.get("model", "claude-sonnet-4-6"),
            "session_id": meta.get("session_id") or meta.get("penugasan", penugasan.name),
            "tanggal_eksekusi": meta.get("tanggal", datetime.now(WIB).isoformat()),
            "wall_clock_seconds": meta.get("wall_clock_seconds", 0.0),
            "rules_dijalankan": meta.get("rules_dijalankan"),
            "anomali_terdeteksi": meta.get("total_anomali") or meta.get("total_observasi") or 0,
            "per_severity": meta.get("per_severity", {}),
            "audit_trail_excerpt_path": str((audit_trail_dir / "events.jsonl").relative_to(penugasan)) if (audit_trail_dir / "events.jsonl").exists() else None,
        },
    }


def build_lrs_kk(ctx: dict, kertas_kerja: list[dict]) -> dict:
    """Tahapan 4: LRS KK — auto-fill dari KKP, status default placeholder."""
    nomor_st = ctx.get("nomor_st") or "TBD"
    return {
        "nomor_lrs_kk": f"LKS-KK-1/{nomor_st}",
        "judul_pengawasan": ctx.get("judul_pengawasan", ""),
        "no_pkp": f"PKP/{nomor_st}",
        "tanggal": None,
        "progres": {"checklist_done": 0, "checklist_total": len(kertas_kerja) * 4, "completed_pct": 0.0},
        "kkp_list": [k["nomor_kkp"] for k in kertas_kerja],
        "reviu_ketua_tim": [
            {"no": "A", "permasalahan": "Kecukupan Informasi dalam Kertas Kerja (On Scope)", "status": "Menunggu Reviu", "paraf": None},
            {"no": "B", "permasalahan": "Kodefikasi Temuan", "status": "Menunggu Reviu", "paraf": None},
            {"no": "C", "permasalahan": "Kesesuaian Informasi dengan Standard (On Standard)", "status": "Menunggu Reviu", "paraf": None},
            {"no": "D", "permasalahan": "Ketepatan Waktu", "status": "Menunggu Reviu", "paraf": None},
        ],
        "lampiran": [],
    }


def build_lrs_lhp(ctx: dict) -> dict:
    """Tahapan 7: LRS LHP — placeholder (diisi PT manual saat reviu Konsep Laporan)."""
    nomor_st = ctx.get("nomor_st") or "TBD"
    return {
        "nomor_lrs_lhp": f"LKS-LHP-1/{nomor_st}",
        "judul_pengawasan": ctx.get("judul_pengawasan", ""),
        "no_pkp": f"PKP/{nomor_st}",
        "tanggal": None,
        "progres": {"checklist_done": 0, "checklist_total": 4, "completed_pct": 0.0},
        "reviu_pengendali_teknis": [
            {"no": "A", "permasalahan": "Tata Bahasa atau Penyajian (On Standard)", "penyelesaian": None, "status": "Menunggu Reviu", "paraf": None},
            {"no": "B", "permasalahan": "Kecukupan Substansi", "penyelesaian": None, "status": "Menunggu Reviu", "paraf": None},
            {"no": "C", "permasalahan": "Kesesuaian Ruang Lingkup (On Scope)", "penyelesaian": None, "status": "Menunggu Reviu", "paraf": None},
            {"no": "D", "permasalahan": "Ketepatan Waktu", "penyelesaian": None, "status": "Menunggu Reviu", "paraf": None},
        ],
        "lampiran": [],
    }


def build_laporan_hasil(penugasan: Path) -> dict:
    """Tahapan 8: Laporan Hasil — placeholder (final, diisi setelah disetujui)."""
    lhp_dir = penugasan / "_LHP"
    final = list(lhp_dir.glob("*FINAL*.docx")) if lhp_dir.exists() else []
    return {
        "pengajuan_id": None,
        "filename": final[0].name if final else None,
        "tanggal_final": datetime.fromtimestamp(final[0].stat().st_mtime, WIB).isoformat() if final else None,
        "status": "draft_pending_pt_review" if not final else "submitted",
        "lampiran": [file_meta(p, role="laporan-hasil-final") for p in final[:1]],
    }


def _find_lampiran(penugasan: Path, name_keywords: list[str], ext_priority: list[str], folder: str = None) -> list[dict]:
    """Cari file lampiran berdasarkan keyword + ext priority."""
    search_dirs = [penugasan / folder] if folder else [penugasan, penugasan / "_KKP", penugasan / "_LHP", penugasan / "_PKP"]
    out: list[dict] = []
    seen = set()
    for d in search_dirs:
        if not d.exists():
            continue
        for ext in ext_priority:
            for p in d.glob(f"*{ext}"):
                if any(kw.lower() in p.name.lower() for kw in name_keywords):
                    if p not in seen:
                        out.append(file_meta(p, role=name_keywords[0].lower()))
                        seen.add(p)
    return out[:3]


# ---------- compute submit_id ----------

def compute_submit_id(payload: dict) -> str:
    """SHA-256 of all sha256 hashes in payload — idempotent."""
    h = hashlib.sha256()
    for sec in payload.values():
        if isinstance(sec, dict):
            for lampir in sec.get("lampiran", []) if isinstance(sec.get("lampiran"), list) else []:
                if "sha256" in lampir:
                    h.update(lampir["sha256"].encode("utf-8"))
        elif isinstance(sec, list):
            for item in sec:
                if isinstance(item, dict):
                    for lampir in item.get("lampiran", []) if isinstance(item.get("lampiran"), list) else []:
                        if "sha256" in lampir:
                            h.update(lampir["sha256"].encode("utf-8"))
    return f"sha256:{h.hexdigest()}"


# ---------- main ----------

def main(argv: list[str] | None = None) -> int:
    _self_check_ast()

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--penugasan", required=True, help="Path folder penugasan")
    ap.add_argument("--skill", default="", help="Skill name (e.g. reviu-rka-kl)")
    ap.add_argument("--model", default="claude-sonnet-4-6", help="Model name")
    ap.add_argument("--auditor", default=os.environ.get("USER", "auditor"), help="Auditor ID")
    ap.add_argument("--out", default=None, help="Custom output path (default: <penugasan>/_SUBMIT/submit-<ts>.json)")
    args = ap.parse_args(argv)

    penugasan = Path(args.penugasan).resolve()
    if not penugasan.exists():
        print(f"[FATAL] Folder penugasan tidak ditemukan: {penugasan}", file=sys.stderr)
        return 4

    submit_dir = penugasan / "_SUBMIT"
    submit_dir.mkdir(parents=True, exist_ok=True)

    # Load context + meta dari pipeline
    ctx = load_context_md(penugasan)
    kkp_meta = load_json_safe(penugasan / "_KKP" / "_pipeline_meta.json") or {}

    print("=" * 72)
    print("GENERATE SUBMIT JSON — Integral SIMWAS v2 schema v" + SCHEMA_VERSION)
    print("=" * 72)
    print(f"  Penugasan : {penugasan}")
    print(f"  Skill     : {args.skill or kkp_meta.get('skill', '?')}")
    print(f"  Auditor   : {args.auditor}")
    print()

    # Build payload per tahapan
    print("[1/8] Building Kartu Penugasan ...")
    kp = build_kartu_penugasan(penugasan, ctx, kkp_meta)
    print("[2/8] Building PKP ...")
    pkp = build_pkp(penugasan, ctx, kkp_meta)
    print("[3/8] Building Kertas Kerja (per anggota) ...")
    kk = build_kertas_kerja(penugasan, ctx, kkp_meta)
    print(f"      → {len(kk)} KKP, total temuan: {sum(len(k.get('temuan_rekomendasi', [])) for k in kk)}")
    print("[4/8] Building LRS KK (placeholder) ...")
    lrs_kk = build_lrs_kk(ctx, kk)
    print("[5/8] Building Konsep Laporan ...")
    konsep = build_konsep_laporan(penugasan, ctx, kkp_meta)
    print(f"      → {konsep.get('filename') or '(no draft)'}")
    print("[6/8] Building Bukti Cek AI metadata ...")
    bukti_ai = build_bukti_cek_ai(penugasan, ctx, kkp_meta, args.skill, args.model)
    print("[7/8] Building LRS LHP (placeholder) ...")
    lrs_lhp = build_lrs_lhp(ctx)
    print("[8/8] Building Laporan Hasil (placeholder) ...")
    lhp = build_laporan_hasil(penugasan)

    payload: dict[str, Any] = {
        "submit_metadata": {
            "submit_id": "PLACEHOLDER",  # filled below
            "submit_timestamp": datetime.now(WIB).isoformat(),
            "schema_version": SCHEMA_VERSION,
            "skill": args.skill or kkp_meta.get("skill", "?"),
            "model": args.model,
            "auditor": args.auditor,
            "penugasan_folder": str(penugasan),
            "audit_trail_path": str((penugasan / "_AUDIT-TRAIL" / "events.jsonl").relative_to(penugasan)),
        },
        "kartu_penugasan": kp,
        "pkp": pkp,
        "kertas_kerja": kk,
        "lrs_kk": lrs_kk,
        "konsep_laporan": konsep,
        "bukti_cek_ai": bukti_ai,
        "lrs_lhp": lrs_lhp,
        "laporan_hasil": lhp,
    }

    # Compute idempotent submit_id
    payload["submit_metadata"]["submit_id"] = compute_submit_id(payload)

    # Write
    ts = datetime.now(WIB).strftime("%Y%m%d-%H%M%S")
    out_path = Path(args.out) if args.out else submit_dir / f"submit-{ts}.json"
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Update latest pointer
    latest = submit_dir / "submit-latest.json"
    latest.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print()
    print("=" * 72)
    print(f"[OK] Submit package generated")
    print(f"   submit_id : {payload['submit_metadata']['submit_id'][:32]}...")
    print(f"   Output    : {out_path}")
    print(f"   Latest    : {latest}")
    print(f"   KKP       : {len(kk)} dokumen, {sum(len(k.get('temuan_rekomendasi', [])) for k in kk)} temuan")
    print(f"   Konsep LHP: {konsep.get('filename') or '(belum ada)'}")
    print(f"   Bukti AI  : {bukti_ai.get('filename') or '(jalankan generate_bukti_ai_docx.py)'}")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
