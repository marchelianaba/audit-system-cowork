"""
build_dashboard_v2.py — Generate dashboard HTML self-contained dengan
data agregasi dari semua penugasan + pipeline AI metrics + submit status.

Scan:
  - penugasan/*/_KKP/_pipeline_meta.json  (per skill timing + anomali)
  - penugasan/*/_SUBMIT/submit-latest.json (status 8 tahapan Integral)
  - penugasan/*/_AUDIT-TRAIL/events.jsonl (event log)

Output: dashboard-v2.html — single file siap di-open di browser, no server needed.

Usage:
    python3 build_dashboard_v2.py [--root PATH_AUDIT_SYSTEM]

Default root: parent of this script's parent.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


WIB = timezone(timedelta(hours=7))


def _self_check_ast() -> None:
    try:
        ast.parse(Path(__file__).read_text(encoding="utf-8"))
    except SyntaxError as e:
        print(f"[FATAL] Self-check AST gagal: {e}", file=sys.stderr)
        sys.exit(2)


def load_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def scan_penugasan(root: Path) -> list[dict]:
    """Scan semua folder penugasan, kumpulkan metrics."""
    pen_root = root / "penugasan"
    out: list[dict] = []
    if not pen_root.exists():
        return out

    for pen_dir in sorted(pen_root.iterdir()):
        if not pen_dir.is_dir():
            continue
        pipeline_meta = load_json(pen_dir / "_KKP" / "_pipeline_meta.json") or {}
        submit_latest = load_json(pen_dir / "_SUBMIT" / "submit-latest.json") or {}

        # Count files
        kkp_dir = pen_dir / "_KKP"
        lhp_dir = pen_dir / "_LHP"
        bukti_dir = pen_dir / "_BUKTI-AI"
        n_kkp = len(list(kkp_dir.glob("KKP-*.docx"))) if kkp_dir.exists() else 0
        n_lhp_draft = len(list(lhp_dir.glob("*-DRAFT.docx"))) if lhp_dir.exists() else 0
        n_bukti = len(list(bukti_dir.glob("Bukti-Cek-AI-*.docx"))) if bukti_dir.exists() else 0

        # Tahapan complete count (untuk progress 0-8)
        tahapan_done = 0
        if submit_latest:
            if submit_latest.get("kartu_penugasan", {}).get("nomor_st", "TBD") != "TBD":
                tahapan_done += 1
            if submit_latest.get("pkp", {}).get("langkah_kerja"):
                tahapan_done += 1
            if submit_latest.get("kertas_kerja"):
                tahapan_done += 1
            if submit_latest.get("lrs_kk"):
                tahapan_done += 1  # placeholder, usually 4
            if submit_latest.get("konsep_laporan", {}).get("filename"):
                tahapan_done += 1
            if submit_latest.get("bukti_cek_ai", {}).get("filename"):
                tahapan_done += 1
            if submit_latest.get("lrs_lhp"):
                tahapan_done += 1
            if submit_latest.get("laporan_hasil", {}).get("filename"):
                tahapan_done += 1

        out.append({
            "name": pen_dir.name,
            "skill": pipeline_meta.get("skill", "?"),
            "tanggal_pipeline": pipeline_meta.get("tanggal", "—"),
            "wall_clock_seconds": pipeline_meta.get("wall_clock_seconds", 0),
            "total_anomali": pipeline_meta.get("total_anomali", pipeline_meta.get("total_observasi", 0)),
            "per_severity": pipeline_meta.get("per_severity", {}),
            "n_kkp": n_kkp,
            "n_lhp_draft": n_lhp_draft,
            "n_bukti_ai": n_bukti,
            "submit_id": submit_latest.get("submit_metadata", {}).get("submit_id", "—"),
            "submit_timestamp": submit_latest.get("submit_metadata", {}).get("submit_timestamp"),
            "tahapan_done": tahapan_done,
            "has_pipeline_meta": bool(pipeline_meta),
            "has_submit": bool(submit_latest),
        })
    return out


def aggregate_metrics(penugasan_list: list[dict]) -> dict:
    """Agregasi total metrics."""
    has_pipeline = [p for p in penugasan_list if p["has_pipeline_meta"]]
    total_anomali = sum(p["total_anomali"] for p in has_pipeline)
    total_wall_clock = sum(p["wall_clock_seconds"] for p in has_pipeline)
    skills = {}
    for p in has_pipeline:
        s = p["skill"]
        if s not in skills:
            skills[s] = {"count": 0, "total_anomali": 0, "total_wall": 0}
        skills[s]["count"] += 1
        skills[s]["total_anomali"] += p["total_anomali"]
        skills[s]["total_wall"] += p["wall_clock_seconds"]

    sev_total = {}
    for p in has_pipeline:
        for sev, count in (p.get("per_severity") or {}).items():
            sev_total[sev] = sev_total.get(sev, 0) + count

    n_with_submit = len([p for p in penugasan_list if p["has_submit"]])

    return {
        "total_penugasan": len(penugasan_list),
        "with_pipeline": len(has_pipeline),
        "with_submit_to_integral": n_with_submit,
        "total_anomali_terdeteksi": total_anomali,
        "total_wall_clock_seconds": round(total_wall_clock, 2),
        "avg_wall_clock_seconds": round(total_wall_clock / len(has_pipeline), 2) if has_pipeline else 0,
        "per_skill": skills,
        "per_severity_total": sev_total,
    }


# ---------- HTML rendering ----------

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
       background: #f0f2f5; color: #1a1a2e; font-size: 14px; line-height: 1.5; }
.header { background: linear-gradient(135deg,#1a1a2e 0%,#16213e 60%,#0f3460 100%);
          color: white; padding: 28px 32px 24px; }
.header h1 { font-size: 22px; font-weight: 700; }
.header .sub { font-size: 12px; opacity: 0.7; margin-top: 4px; }
.container { max-width: 1400px; margin: 0 auto; padding: 24px 32px; }
.tabs { display: flex; gap: 4px; margin-bottom: 24px; border-bottom: 2px solid #cbd5e1; flex-wrap: wrap; }
.tab { padding: 10px 18px; cursor: pointer; background: #e2e8f0; border-radius: 8px 8px 0 0;
       font-weight: 500; color: #475569; border: none; font-size: 13px; }
.tab.active { background: #0f3460; color: white; }
.tab:hover:not(.active) { background: #cbd5e1; }
.panel { display: none; }
.panel.active { display: block; }
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(180px,1fr));
            gap: 16px; margin-bottom: 24px; }
.kpi { background: white; padding: 18px; border-radius: 8px;
       box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-left: 4px solid #0f3460; }
.kpi .label { font-size: 11px; color: #64748b; text-transform: uppercase;
              letter-spacing: 0.5px; margin-bottom: 4px; }
.kpi .value { font-size: 28px; font-weight: 700; color: #0f3460; }
.kpi.tinggi { border-left-color: #dc2626; }
.kpi.tinggi .value { color: #dc2626; }
.kpi.sedang { border-left-color: #f59e0b; }
.kpi.sedang .value { color: #f59e0b; }
.kpi.done { border-left-color: #16a34a; }
.kpi.done .value { color: #16a34a; }
.kpi.ai { border-left-color: #7c3aed; }
.kpi.ai .value { color: #7c3aed; }
.kpi.unit { font-size: 14px; color: #64748b; font-weight: normal; margin-left: 4px; }
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 16px; overflow: hidden; }
.card-header { padding: 14px 18px; background: #f8fafc; border-bottom: 1px solid #e2e8f0;
               font-weight: 600; color: #0f3460; }
.card-body { padding: 16px 18px; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th { background: #0f3460; color: white; text-align: left; padding: 10px 12px; font-weight: 600; }
td { padding: 8px 12px; border-bottom: 1px solid #e2e8f0; vertical-align: top; }
tr:hover td { background: #f8fafc; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px;
         font-weight: 600; text-transform: uppercase; }
.badge-tinggi { background: #fee2e2; color: #dc2626; }
.badge-sedang { background: #fef3c7; color: #d97706; }
.badge-rendah { background: #dbeafe; color: #2563eb; }
.badge-done { background: #dcfce7; color: #16a34a; }
.badge-active { background: #fef3c7; color: #d97706; }
.badge-belum { background: #fee2e2; color: #dc2626; }
.badge-ai { background: #ede9fe; color: #7c3aed; }
.empty { color: #94a3b8; font-style: italic; padding: 16px; text-align: center; }
.muted { color: #64748b; font-size: 12px; }
.timestamp { color: #94a3b8; font-size: 11px; }
.search-box { width: 100%; padding: 8px 12px; border: 1px solid #cbd5e1;
              border-radius: 6px; font-size: 13px; margin-bottom: 12px; }
.bar-container { width: 100%; background: #e2e8f0; border-radius: 4px; overflow: hidden; height: 22px; position: relative; }
.bar { background: linear-gradient(90deg, #7c3aed, #a78bfa); height: 100%; transition: width 0.3s; }
.bar-label { position: absolute; left: 8px; top: 2px; font-size: 11px; color: white; font-weight: 600; }
.progress-pill { display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px; border-radius: 12px; background: #f1f5f9; font-size: 11px; }
.progress-pill .dot { width: 8px; height: 8px; border-radius: 50%; background: #cbd5e1; }
.progress-pill .dot.done { background: #16a34a; }
.tahapan-grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 4px; margin-top: 4px; }
.tahapan-cell { background: #f1f5f9; padding: 4px; text-align: center; border-radius: 3px; font-size: 10px; color: #64748b; }
.tahapan-cell.done { background: #dcfce7; color: #16a34a; font-weight: 600; }
.skill-bar-row { display: grid; grid-template-columns: 200px 1fr 60px; gap: 12px; align-items: center; padding: 8px 0; border-bottom: 1px solid #f1f5f9; }
.skill-bar-row:last-child { border-bottom: none; }
.skill-name { font-weight: 500; color: #1a1a2e; font-size: 13px; }
.severity-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; }
.severity-tile { background: white; padding: 14px; border-radius: 6px; border-left: 4px solid #cbd5e1; }
.severity-tile.KRITIS { border-left-color: #dc2626; }
.severity-tile.PERINGATAN { border-left-color: #f59e0b; }
.severity-tile.INFO { border-left-color: #3b82f6; }
.severity-tile .num { font-size: 24px; font-weight: 700; }
.severity-tile.KRITIS .num { color: #dc2626; }
.severity-tile.PERINGATAN .num { color: #f59e0b; }
.severity-tile.INFO .num { color: #3b82f6; }
"""


def render_html(metrics: dict, penugasan_list: list[dict], generated_at: str) -> str:
    """Render full HTML self-contained."""
    # KPI top
    kpi_html = f"""
    <div class="kpi-grid">
        <div class="kpi"><div class="label">Total Penugasan</div><div class="value">{metrics['total_penugasan']}</div></div>
        <div class="kpi ai"><div class="label">Pipeline AI Dijalankan</div><div class="value">{metrics['with_pipeline']}<span class="unit">penugasan</span></div></div>
        <div class="kpi tinggi"><div class="label">Total Anomali Terdeteksi AI</div><div class="value">{metrics['total_anomali_terdeteksi']}</div></div>
        <div class="kpi done"><div class="label">Submit Siap ke Integral</div><div class="value">{metrics['with_submit_to_integral']}</div></div>
        <div class="kpi"><div class="label">Avg Wall Clock Pipeline</div><div class="value">{metrics['avg_wall_clock_seconds']:.1f}<span class="unit">detik</span></div></div>
        <div class="kpi"><div class="label">Total Wall Clock</div><div class="value">{metrics['total_wall_clock_seconds']:.0f}<span class="unit">detik</span></div></div>
    </div>
    """

    # Severity breakdown
    severity_html = '<div class="severity-grid">'
    for sev in ["KRITIS", "PERINGATAN", "INFO"]:
        count = metrics["per_severity_total"].get(sev, 0)
        severity_html += f'<div class="severity-tile {sev}"><div class="muted">{sev}</div><div class="num">{count}</div></div>'
    severity_html += "</div>"

    # Per-skill bars
    max_anomali = max((s.get("total_anomali", 0) for s in metrics["per_skill"].values()), default=1) or 1
    skill_bars = ""
    for skill, data in sorted(metrics["per_skill"].items(), key=lambda x: -x[1]["total_anomali"]):
        pct = (data["total_anomali"] / max_anomali) * 100 if max_anomali > 0 else 0
        skill_bars += f"""
        <div class="skill-bar-row">
            <div class="skill-name">{skill}</div>
            <div class="bar-container">
                <div class="bar" style="width: {pct:.0f}%"></div>
                <div class="bar-label">{data['count']} penugasan · avg {data['total_wall']/data['count']:.1f}s</div>
            </div>
            <div style="text-align:right;font-weight:600;color:#7c3aed">{data['total_anomali']}</div>
        </div>
        """

    # Penugasan table (Pipeline AI tab)
    pipeline_table_rows = ""
    for p in sorted(penugasan_list, key=lambda x: x.get("tanggal_pipeline", ""), reverse=True):
        if not p["has_pipeline_meta"]:
            continue
        sev_html = ""
        for sev, count in (p.get("per_severity") or {}).items():
            cls = "tinggi" if sev == "KRITIS" else ("sedang" if sev == "PERINGATAN" else "rendah")
            sev_html += f'<span class="badge badge-{cls}">{sev}: {count}</span> '
        pipeline_table_rows += f"""
        <tr>
            <td><strong>{p['name']}</strong></td>
            <td><span class="badge badge-ai">{p['skill']}</span></td>
            <td>{p['wall_clock_seconds']:.1f} s</td>
            <td><strong style="color:#7c3aed">{p['total_anomali']}</strong></td>
            <td>{sev_html or '<span class="muted">—</span>'}</td>
            <td><span class="muted">{p['tanggal_pipeline'][:16] if p['tanggal_pipeline'] else '—'}</span></td>
        </tr>
        """

    # Submit Integral tab
    submit_table_rows = ""
    for p in sorted(penugasan_list, key=lambda x: x.get("submit_timestamp") or "", reverse=True):
        if not p["has_submit"]:
            continue
        # Tahapan grid 1-8
        tahapan_cells = ""
        for i in range(1, 9):
            done = i <= p["tahapan_done"]
            cls = "done" if done else ""
            tahapan_cells += f'<div class="tahapan-cell {cls}">{i}</div>'
        sid = p["submit_id"][:24] if p["submit_id"] else "—"
        ts = p["submit_timestamp"][:16] if p["submit_timestamp"] else "—"
        submit_table_rows += f"""
        <tr>
            <td><strong>{p['name']}</strong></td>
            <td><span class="badge badge-ai">{p['skill']}</span></td>
            <td>{p['n_kkp']} KKP, {p['n_lhp_draft']} LHP, {p['n_bukti_ai']} Bukti AI</td>
            <td><div class="tahapan-grid">{tahapan_cells}</div><div class="muted" style="margin-top:4px">{p['tahapan_done']}/8 tahapan</div></td>
            <td><code style="font-size:10px">{sid}…</code></td>
            <td><span class="muted">{ts}</span></td>
        </tr>
        """

    if not pipeline_table_rows:
        pipeline_table_rows = '<tr><td colspan="6" class="empty">Belum ada penugasan dengan _pipeline_meta.json. Jalankan run_batch.py di salah satu skill.</td></tr>'
    if not submit_table_rows:
        submit_table_rows = '<tr><td colspan="6" class="empty">Belum ada penugasan dengan submit-latest.json.</td></tr>'

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard Audit-System v4.1 — Inspektorat II</title>
<style>{CSS}</style>
</head>
<body>
<div class="header">
    <h1>📊 Dashboard Audit-System v4.1 — Inspektorat II</h1>
    <div class="sub">Pipeline AI · Submit Integral · Pemantauan ISU/Risiko · TLHP — generated {generated_at}</div>
</div>
<div class="container">
    <div class="tabs">
        <button class="tab active" onclick="showTab('overview')">📈 Overview</button>
        <button class="tab" onclick="showTab('pipeline')">🤖 Pipeline AI ({metrics['with_pipeline']})</button>
        <button class="tab" onclick="showTab('integral')">📨 Submit ke Integral ({metrics['with_submit_to_integral']})</button>
    </div>

    <div class="panel active" id="panel-overview">
        {kpi_html}

        <div class="card">
            <div class="card-header">Anomali per Severity (Total Lintas Penugasan)</div>
            <div class="card-body">{severity_html}</div>
        </div>

        <div class="card">
            <div class="card-header">🤖 Aktivitas Pipeline per Skill</div>
            <div class="card-body">{skill_bars or '<div class="empty">Belum ada pipeline AI yang dijalankan.</div>'}</div>
        </div>
    </div>

    <div class="panel" id="panel-pipeline">
        {kpi_html}
        <div class="card">
            <div class="card-header">Detail Eksekusi Pipeline AI per Penugasan</div>
            <div class="card-body">
                <table>
                    <thead><tr>
                        <th>Penugasan</th><th>Skill</th><th>Wall Clock</th>
                        <th>Anomali</th><th>Per Severity</th><th>Tanggal</th>
                    </tr></thead>
                    <tbody>{pipeline_table_rows}</tbody>
                </table>
            </div>
        </div>
    </div>

    <div class="panel" id="panel-integral">
        <div class="card">
            <div class="card-header">📨 Status Submit ke Integral SIMWAS — 8 Tahapan</div>
            <div class="card-body">
                <p class="muted" style="margin-bottom:12px">
                    Setiap penugasan di-submit ke Integral mengikuti 8 tahapan: 1.Kartu Penugasan → 2.PKP → 3.Kertas Kerja → 4.LRS KK → 5.Konsep Laporan → 6.Bukti Cek AI → 7.LRS LHP → 8.Laporan Hasil. File <code>_SUBMIT/submit-latest.json</code> snapshot lengkap untuk Integral menarik.
                </p>
                <table>
                    <thead><tr>
                        <th>Penugasan</th><th>Skill</th><th>Output Files</th>
                        <th>Tahapan Progress</th><th>Submit ID</th><th>Timestamp</th>
                    </tr></thead>
                    <tbody>{submit_table_rows}</tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<script>
function showTab(name) {{
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById('panel-' + name).classList.add('active');
    event.target.classList.add('active');
}}
</script>
</body>
</html>
"""
    return html


def main(argv: list[str] | None = None) -> int:
    _self_check_ast()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=None, help="Path audit-system-v4 root (default: parent of script's parent)")
    ap.add_argument("--out", default=None, help="Output HTML path (default: <root>/dashboard-v2.html)")
    args = ap.parse_args(argv)

    if args.root:
        root = Path(args.root).resolve()
    else:
        root = Path(__file__).resolve().parent.parent  # scripts/.. = audit-system-v4/

    if not root.exists():
        print(f"[FATAL] Root tidak ditemukan: {root}", file=sys.stderr)
        return 4

    out_path = Path(args.out) if args.out else root / "dashboard-v2.html"

    print(f"Scanning penugasan di {root}/penugasan/ ...")
    penugasan_list = scan_penugasan(root)
    print(f"  → {len(penugasan_list)} penugasan ditemukan")

    print("Aggregating metrics ...")
    metrics = aggregate_metrics(penugasan_list)
    print(f"  → {metrics['with_pipeline']} dengan pipeline meta, {metrics['with_submit_to_integral']} dengan submit JSON")
    print(f"  → Total anomali: {metrics['total_anomali_terdeteksi']}, avg wall clock: {metrics['avg_wall_clock_seconds']:.1f}s")

    generated_at = datetime.now(WIB).strftime("%Y-%m-%d %H:%M WIB")
    html = render_html(metrics, penugasan_list, generated_at)
    out_path.write_text(html, encoding="utf-8")

    print(f"\n[OK] Dashboard generated: {out_path}")
    print(f"   Open in browser to view")
    return 0


if __name__ == "__main__":
    sys.exit(main())
