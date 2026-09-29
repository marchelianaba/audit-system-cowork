#!/usr/bin/env python3
"""
build_dashboard.py — Generate dashboard.html dari data sumber:
1. Pemantauan ISU/Risiko: parse wiki/wiki/pemantauan-isu-risiko-trello.md
   + (opsional) penugasan/_RISK-REGISTER/issues.json
2. TLHP: parse wiki/wiki/tlhp-index.md
3. Audit Trail: aggregat dari penugasan/*/_AUDIT-TRAIL/events.jsonl
4. Hasil Pengawasan KKP+LHP: dari penugasan/*/_KKP/temuan.json

Output sinkron ke:
- audit-system-v4/dashboard.html   (sistem)
- audit-system-v4/wiki/wiki/dashboard.html (wiki — replace lama)

Pemakaian:
    python3 scripts/build_dashboard.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "wiki" / "wiki"
PENUGASAN_DIR = ROOT / "penugasan"
RISK_REGISTER = PENUGASAN_DIR / "_RISK-REGISTER" / "issues.json"

OUT_SYSTEM = ROOT / "dashboard.html"
OUT_WIKI = WIKI_DIR / "dashboard.html"

WIB = timezone(timedelta(hours=7))


def _now() -> str:
    return datetime.now(WIB).strftime("%Y-%m-%d %H:%M WIB")


# ---------------- Data collection ----------------

def parse_isu_risiko_wiki() -> list[dict]:
    """Parse cards dari wiki/wiki/pemantauan-isu-risiko-trello.md.
    Cards adalah baris tabel di dalam section '### Kelompok X' dengan kolom:
    | # | Entitas | Prioritas | Item Dipantau |"""
    p = WIKI_DIR / "pemantauan-isu-risiko-trello.md"
    if not p.exists():
        return []
    txt = p.read_text(encoding="utf-8")
    out = []
    # Find each "### Kelompok ..." section
    for m in re.finditer(r"###\s+(Kelompok\s+[^\n]+)", txt):
        kelompok = m.group(1).strip()
        # ambil teks sampai heading berikutnya
        rest = txt[m.end():]
        nxt = re.search(r"\n###\s+", rest)
        section = rest[:nxt.start()] if nxt else rest
        # Parse baris tabel: | N | **Nama** | Priority | Item ... |
        for row in re.finditer(
                r"^\|\s*\d+\s*\|\s*\*?\*?([^*|]+?)\*?\*?\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
                section, re.MULTILINE):
            entitas = row.group(1).strip()
            prio_raw = row.group(2).strip()
            item = row.group(3).strip()
            # Skip header row
            if entitas.lower() == "entitas":
                continue
            priority = "?"
            if re.search(r"Tinggi|🔴", prio_raw, re.IGNORECASE): priority = "Tinggi"
            elif re.search(r"Sedang|🟡", prio_raw, re.IGNORECASE): priority = "Sedang"
            elif re.search(r"Rendah|⚪", prio_raw, re.IGNORECASE): priority = "Rendah"
            out.append({
                "title": entitas,
                "priority": priority,
                "status": f"[{kelompok}] {item[:100]}",
                "source": "wiki",
            })
    return out


def parse_isu_risiko_json() -> list[dict]:
    """Optional override / tambahan dari penugasan/_RISK-REGISTER/issues.json."""
    if not RISK_REGISTER.exists():
        return []
    try:
        data = json.loads(RISK_REGISTER.read_text(encoding="utf-8"))
        out = []
        for item in data.get("issues", []):
            out.append({
                "title": item.get("title", "?"),
                "priority": item.get("priority", "?"),
                "status": item.get("status", ""),
                "source": "json",
            })
        return out
    except Exception:
        return []


def collect_isu_risiko() -> list[dict]:
    """Gabung wiki + JSON (JSON override duplikasi by title)."""
    wiki_items = parse_isu_risiko_wiki()
    json_items = parse_isu_risiko_json()
    by_title = {x["title"].lower(): x for x in wiki_items}
    for j in json_items:
        by_title[j["title"].lower()] = j  # override
    return list(by_title.values())


def parse_tlhp_index() -> list[dict]:
    """Parse table dari wiki/wiki/tlhp-index.md."""
    p = WIKI_DIR / "tlhp-index.md"
    if not p.exists():
        return []
    txt = p.read_text(encoding="utf-8")
    out = []
    for line in txt.splitlines():
        m = re.match(r"\|\s*`?(REK-[\w-]+)`?\s*\|\s*(\[\[lhp-[\w-]+\]\]|[^|]+)\s*\|"
                     r"\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*(\w+)\s*\|\s*([^|]+)\s*\|", line)
        if m:
            out.append({
                "rek_id": m.group(1),
                "penugasan": m.group(2).strip().strip("[]"),
                "auditi": m.group(3).strip(),
                "rekomendasi": m.group(4).strip(),
                "status": m.group(5).strip(),
                "deadline": m.group(6).strip(),
            })
    return out


def collect_audit_trail() -> tuple[Counter, list[dict]]:
    """Aggregate events + per-penugasan summary."""
    actions = Counter()
    pen_summary = []
    if not PENUGASAN_DIR.exists():
        return actions, pen_summary
    for pen in sorted(PENUGASAN_DIR.iterdir()):
        if not pen.is_dir() or pen.name.startswith("_"):
            continue
        log = pen / "_AUDIT-TRAIL" / "events.jsonl"
        if not log.exists():
            continue
        events = []
        for line in log.read_text(encoding="utf-8").splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        for e in events:
            actions[e.get("action", "?")] += 1
        last = events[-1] if events else {}
        has_export = any(e.get("action") == "INTEGRAL_EXPORT" for e in events)
        has_lhp = any(e.get("action") == "LHP_FINALIZED" for e in events)
        stage = "DONE" if has_export else ("LHP_FINAL" if has_lhp else
                ("KKP" if any(e.get("action") == "KKP_TEMUAN_ADDED" for e in events) else "INISIASI"))
        pen_summary.append({
            "penugasan": pen.name,
            "stage": stage,
            "n_events": len(events),
            "last_ts": last.get("timestamp", "?"),
            "last_action": last.get("action", "?"),
            "last_actor": last.get("actor", {}).get("nama", "?"),
        })
    return actions, pen_summary


def collect_kkp_lhp() -> list[dict]:
    """Untuk tiap penugasan: ambil ringkasan dari temuan.json + detail KKSA per temuan."""
    out = []
    if not PENUGASAN_DIR.exists():
        return out
    for pen in sorted(PENUGASAN_DIR.iterdir()):
        if not pen.is_dir() or pen.name.startswith("_"):
            continue
        tj = pen / "_KKP" / "temuan.json"
        if not tj.exists():
            continue
        try:
            doc = json.loads(tj.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        pinfo = doc.get("penugasan", {})
        temuan = doc.get("temuan", [])
        lhp_files = []
        if (pen / "_LHP").exists():
            lhp_files = [f.name for f in (pen / "_LHP").glob("LHP*.docx")]
        anggota = Counter()
        for t in temuan:
            anggota[t.get("anggota_tim", {}).get("nama_lengkap", "?")] += 1
        # Detail temuan: KKSA full
        temuan_detail = []
        for t in temuan:
            sumber = []
            for d in t.get("dokumen_sumber", []):
                hal = f" hal. {d['halaman']}" if d.get("halaman") else ""
                sumber.append(f"{d.get('file', '?')}{hal}")
            temuan_detail.append({
                "id": t.get("id_temuan", "?"),
                "sasaran_id": t.get("sasaran_id", "?"),
                "anggota": t.get("anggota_tim", {}).get("nama_lengkap", "?"),
                "judul": t.get("judul_temuan", "?"),
                "kondisi": t.get("kondisi", ""),
                "kriteria": t.get("kriteria", ""),
                "sebab": t.get("sebab"),
                "akibat": t.get("akibat", ""),
                "dokumen_sumber": sumber,
                "status": t.get("status", "DRAFT"),
            })
        out.append({
            "penugasan": pen.name,
            "obyek": pinfo.get("obyek", "?"),
            "jenis_pengawasan": pinfo.get("jenis_pengawasan", "?"),
            "nomor_st": pinfo.get("nomor_st", "?"),
            "n_temuan": len(temuan),
            "lhp_file": lhp_files[0] if lhp_files else "(belum ada)",
            "anggota_dist": dict(anggota),
            "temuan_detail": temuan_detail,
        })
    return out


# ---------------- HTML rendering ----------------

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
       background: #f0f2f5; color: #1a1a2e; font-size: 14px; line-height: 1.5; }
.header { background: linear-gradient(135deg,#1a1a2e 0%,#16213e 60%,#0f3460 100%);
          color: white; padding: 28px 32px 24px; }
.header h1 { font-size: 22px; font-weight: 700; }
.header .sub { font-size: 12px; opacity: 0.7; margin-top: 4px; }
.container { max-width: 1400px; margin: 0 auto; padding: 24px 32px; }
.tabs { display: flex; gap: 4px; margin-bottom: 24px; border-bottom: 2px solid #cbd5e1; }
.tab { padding: 10px 20px; cursor: pointer; background: #e2e8f0; border-radius: 8px 8px 0 0;
       font-weight: 500; color: #475569; border: none; font-size: 14px; }
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
.badge-sedang-tl { background: #fed7aa; color: #ea580c; }
.badge-selesai { background: #dcfce7; color: #16a34a; }
.empty { color: #94a3b8; font-style: italic; padding: 16px; text-align: center; }
.muted { color: #64748b; font-size: 12px; }
.timestamp { color: #94a3b8; font-size: 11px; }
.search-box { width: 100%; padding: 8px 12px; border: 1px solid #cbd5e1;
              border-radius: 6px; font-size: 13px; margin-bottom: 12px; }
.dist-badge { display: inline-block; padding: 1px 6px; background: #e0e7ff; color: #4338ca;
              border-radius: 3px; font-size: 11px; margin-right: 4px; }
.temuan-card { background: #f8fafc; border-left: 3px solid #0f3460; padding: 12px 14px;
               margin: 10px 0; border-radius: 4px; font-size: 13px; }
.temuan-head { color: #475569; font-size: 12px; margin-bottom: 6px; }
.temuan-judul { font-weight: 600; color: #0f3460; margin-bottom: 10px; font-size: 14px; }
.kksa-row { display: grid; grid-template-columns: 110px 1fr; gap: 12px; margin: 6px 0;
            padding: 4px 0; border-bottom: 1px dashed #e2e8f0; }
.kksa-row:last-child { border-bottom: none; }
.kksa-label { font-weight: 600; color: #475569; text-transform: uppercase;
              font-size: 11px; padding-top: 2px; }
.kksa-val { color: #1a1a2e; line-height: 1.5; }
details { padding: 8px 0; }
summary { cursor: pointer; padding: 6px 0; font-weight: 500; }
summary:hover { color: #0f3460; }
"""

JS = """
function showTab(name) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  document.getElementById('panel-' + name).classList.add('active');
}
function filterTable(inputId, tableId) {
  var q = document.getElementById(inputId).value.toLowerCase();
  document.querySelectorAll('#' + tableId + ' tbody tr').forEach(tr => {
    tr.style.display = tr.textContent.toLowerCase().includes(q) ? '' : 'none';
  });
}
"""


def _badge_priority(p: str) -> str:
    cls = {"Tinggi": "badge-tinggi", "Sedang": "badge-sedang", "Rendah": "badge-rendah"}.get(p, "")
    return f'<span class="badge {cls}">{escape(p)}</span>'


def _badge_status(s: str) -> str:
    s_up = s.upper()
    if "BELUM" in s_up: cls = "badge-belum"
    elif "SEDANG" in s_up or "ACTIVE" in s_up: cls = "badge-sedang-tl"
    elif "SELESAI" in s_up or "DITERIMA" in s_up or "DONE" in s_up or "DITUTUP" in s_up: cls = "badge-selesai"
    else: cls = ""
    return f'<span class="badge {cls}">{escape(s)}</span>'


def render_panel_isu_risiko(items: list[dict]) -> str:
    if not items:
        return '<div class="empty">Belum ada data ISU/Risiko terdaftar.</div>'
    n_tinggi = sum(1 for i in items if i["priority"] == "Tinggi")
    n_sedang = sum(1 for i in items if i["priority"] == "Sedang")
    rows = []
    for it in items:
        rows.append(f"""<tr>
            <td><strong>{escape(it['title'])}</strong></td>
            <td>{_badge_priority(it['priority'])}</td>
            <td>{escape(it['status']) or '<span class="muted">—</span>'}</td>
            <td><span class="muted">{escape(it['source'])}</span></td>
        </tr>""")
    return f"""
    <div class="kpi-grid">
      <div class="kpi tinggi"><div class="label">Prioritas Tinggi</div><div class="value">{n_tinggi}</div></div>
      <div class="kpi sedang"><div class="label">Prioritas Sedang</div><div class="value">{n_sedang}</div></div>
      <div class="kpi"><div class="label">Total ISU/Risiko</div><div class="value">{len(items)}</div></div>
    </div>
    <div class="card">
      <div class="card-header">Daftar Card Pemantauan ISU & Risiko</div>
      <div class="card-body">
        <input class="search-box" id="search-isu" placeholder="Filter..." onkeyup="filterTable('search-isu','tbl-isu')">
        <table id="tbl-isu">
          <thead><tr><th>Card / Entitas</th><th>Prioritas</th><th>Status / Progres</th><th>Sumber</th></tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
      </div>
    </div>
    """


def render_panel_tlhp(items: list[dict]) -> str:
    if not items:
        return '<div class="empty">Belum ada rekomendasi TLHP. Selesaikan satu penugasan dulu (ingest_to_wiki).</div>'
    by_status = Counter(i["status"] for i in items)
    rows = []
    for it in items:
        rows.append(f"""<tr>
            <td><code>{escape(it['rek_id'])}</code></td>
            <td>{escape(it['penugasan'])}</td>
            <td>{escape(it['auditi'])}</td>
            <td>{escape(it['rekomendasi'])}</td>
            <td>{_badge_status(it['status'])}</td>
            <td><span class="muted">{escape(it['deadline'])}</span></td>
        </tr>""")
    return f"""
    <div class="kpi-grid">
      <div class="kpi belum"><div class="label">Belum Ditindaklanjuti</div><div class="value">{by_status.get('BELUM_DITINDAKLANJUTI',0)}</div></div>
      <div class="kpi sedang"><div class="label">Sedang Ditindaklanjuti</div><div class="value">{by_status.get('SEDANG_DITINDAKLANJUTI',0)}</div></div>
      <div class="kpi done"><div class="label">Selesai/Ditutup</div><div class="value">{by_status.get('SELESAI_DITINDAKLANJUTI',0)+by_status.get('DITUTUP',0)}</div></div>
      <div class="kpi"><div class="label">Total Rekomendasi</div><div class="value">{len(items)}</div></div>
    </div>
    <div class="card">
      <div class="card-header">Index Rekomendasi TLHP</div>
      <div class="card-body">
        <input class="search-box" id="search-tlhp" placeholder="Filter..." onkeyup="filterTable('search-tlhp','tbl-tlhp')">
        <table id="tbl-tlhp">
          <thead><tr><th>ID Rek</th><th>Penugasan</th><th>Auditi</th><th>Rekomendasi</th><th>Status</th><th>Deadline</th></tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
      </div>
    </div>
    """


def render_panel_audit_trail(actions: Counter, pen_summary: list[dict]) -> str:
    if not pen_summary:
        return '<div class="empty">Belum ada audit trail dari penugasan v4.</div>'
    n_done = sum(1 for p in pen_summary if p["stage"] == "DONE")
    n_active = len(pen_summary) - n_done
    total_events = sum(actions.values())
    action_rows = "".join(
        f"<tr><td><code>{escape(a)}</code></td><td>{n}</td></tr>"
        for a, n in actions.most_common()
    )
    pen_rows = "".join(
        f"""<tr>
            <td>{escape(p['penugasan'])}</td>
            <td>{_badge_status(p['stage'])}</td>
            <td>{p['n_events']}</td>
            <td>{escape(p['last_action'])}</td>
            <td>{escape(p['last_actor'])}</td>
            <td><span class="timestamp">{escape(p['last_ts'])}</span></td>
        </tr>"""
        for p in pen_summary
    )
    return f"""
    <div class="kpi-grid">
      <div class="kpi done"><div class="label">Penugasan SELESAI</div><div class="value">{n_done}</div></div>
      <div class="kpi"><div class="label">Penugasan Aktif</div><div class="value">{n_active}</div></div>
      <div class="kpi"><div class="label">Total Events</div><div class="value">{total_events}</div></div>
    </div>
    <div class="card">
      <div class="card-header">Penugasan v4 — Status Terkini</div>
      <div class="card-body">
        <input class="search-box" id="search-pen" placeholder="Filter..." onkeyup="filterTable('search-pen','tbl-pen')">
        <table id="tbl-pen">
          <thead><tr><th>Penugasan</th><th>Stage</th><th>Events</th><th>Last Action</th><th>Last Actor</th><th>Last Timestamp</th></tr></thead>
          <tbody>{pen_rows}</tbody>
        </table>
      </div>
    </div>
    <div class="card">
      <div class="card-header">Total Events per Action (semua penugasan)</div>
      <div class="card-body">
        <table>
          <thead><tr><th>Action</th><th>Total</th></tr></thead>
          <tbody>{action_rows}</tbody>
        </table>
      </div>
    </div>
    """


def render_panel_pengawasan(items: list[dict]) -> str:
    if not items:
        return '<div class="empty">Belum ada KKP/LHP dari penugasan v4.</div>'
    total_temuan = sum(i["n_temuan"] for i in items)
    n_lhp_ready = sum(1 for i in items if i["lhp_file"] != "(belum ada)")
    rows = []
    for it in items:
        anggota_html = " ".join(
            f'<span class="dist-badge">{escape(n)}: {c}</span>'
            for n, c in it["anggota_dist"].items()
        ) or '<span class="muted">—</span>'
        # Render detail KKSA per temuan (collapsible)
        if it["temuan_detail"]:
            temuan_blocks = []
            for t in it["temuan_detail"]:
                sumber_html = ", ".join(f"<code>{escape(s)}</code>" for s in t["dokumen_sumber"]) or '<span class="muted">—</span>'
                sebab_block = (f'<div class="kksa-row"><span class="kksa-label">Sebab</span>'
                               f'<div class="kksa-val">{escape(t["sebab"])}</div></div>') if t.get("sebab") else ""
                temuan_blocks.append(f"""
                <div class="temuan-card">
                  <div class="temuan-head">
                    <code>{escape(t['id'])}</code> · sasaran <code>{escape(t['sasaran_id'])}</code> ·
                    {escape(t['anggota'])}
                    <span class="badge badge-active" style="float:right">{escape(t['status'])}</span>
                  </div>
                  <div class="temuan-judul">{escape(t['judul'])}</div>
                  <div class="kksa-row"><span class="kksa-label">Kondisi</span>
                    <div class="kksa-val">{escape(t['kondisi'])}</div></div>
                  <div class="kksa-row"><span class="kksa-label">Kriteria</span>
                    <div class="kksa-val">{escape(t['kriteria'])}</div></div>
                  {sebab_block}
                  <div class="kksa-row"><span class="kksa-label">Akibat</span>
                    <div class="kksa-val">{escape(t['akibat'])}</div></div>
                  <div class="kksa-row"><span class="kksa-label">Dokumen sumber</span>
                    <div class="kksa-val">{sumber_html}</div></div>
                </div>""")
            detail_html = "".join(temuan_blocks)
        else:
            detail_html = '<p class="muted" style="padding:8px 0">(tidak ada temuan)</p>'

        rows.append(
            "<tr>"
            f"<td><strong>{escape(it['penugasan'])}</strong><br>"
            f"<span class='muted'>{escape(it['nomor_st'])}</span></td>"
            f"<td>{escape(it['jenis_pengawasan'])}</td>"
            f"<td>{escape(it['obyek'])}</td>"
            f"<td>{it['n_temuan']}</td>"
            f"<td>{anggota_html}</td>"
            f"<td><code>{escape(it['lhp_file'])}</code></td>"
            "</tr>"
            "<tr><td colspan='6' style='padding:0 12px 16px'><details>"
            f"<summary class='muted'>Lihat detail temuan ({it['n_temuan']}) — kondisi, kriteria, sebab, akibat</summary>"
            f"{detail_html}"
            "</details></td></tr>"
        )
    return (
        '<div class="kpi-grid">'
        f'<div class="kpi"><div class="label">Total Penugasan dengan KKP</div><div class="value">{len(items)}</div></div>'
        f'<div class="kpi"><div class="label">Total Temuan</div><div class="value">{total_temuan}</div></div>'
        f'<div class="kpi done"><div class="label">LHP Final Tersedia</div><div class="value">{n_lhp_ready}</div></div>'
        '</div>'
        '<div class="card">'
        '<div class="card-header">Hasil Pengawasan — KKP &amp; LHP per Penugasan</div>'
        '<div class="card-body">'
        '<input class="search-box" id="search-pgw" placeholder="Filter..." onkeyup="filterTable(\'search-pgw\',\'tbl-pgw\')">'
        '<table id="tbl-pgw">'
        '<thead><tr><th>Penugasan / ST</th><th>Jenis</th><th>Obyek</th><th># Temuan</th><th>Distribusi Anggota</th><th>LHP File</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody>'
        '</table>'
        '</div></div>'
    )


def render_html() -> str:
    isu = collect_isu_risiko()
    tlhp = parse_tlhp_index()
    actions, pen_summary = collect_audit_trail()
    pengawasan = collect_kkp_lhp()
    body = (
        f'<div class="header"><h1>Dashboard Audit-System v4 — Inspektorat II</h1>'
        f'<div class="sub">Pemantauan ISU/Risiko · TLHP · Audit Trail · Hasil Pengawasan KKP &amp; LHP — generated {_now()}</div></div>'
        f'<div class="container">'
        f'<div class="tabs">'
        f'<button class="tab active" id="tab-isu" onclick="showTab(\'isu\')">📋 Pemantauan ISU &amp; Risiko ({len(isu)})</button>'
        f'<button class="tab" id="tab-tlhp" onclick="showTab(\'tlhp\')">📌 TLHP ({len(tlhp)})</button>'
        f'<button class="tab" id="tab-trail" onclick="showTab(\'trail\')">🔍 Audit Trail ({sum(actions.values())})</button>'
        f'<button class="tab" id="tab-pgw" onclick="showTab(\'pgw\')">📊 Hasil Pengawasan ({len(pengawasan)})</button>'
        f'</div>'
        f'<div class="panel active" id="panel-isu">{render_panel_isu_risiko(isu)}</div>'
        f'<div class="panel" id="panel-tlhp">{render_panel_tlhp(tlhp)}</div>'
        f'<div class="panel" id="panel-trail">{render_panel_audit_trail(actions, pen_summary)}</div>'
        f'<div class="panel" id="panel-pgw">{render_panel_pengawasan(pengawasan)}</div>'
        f'<div style="margin-top:32px;text-align:center" class="muted">'
        f'Sumber: pemantauan-isu-risiko-trello.md · tlhp-index.md · _AUDIT-TRAIL/*.jsonl · _KKP/temuan.json<br>'
        f'Auto-rebuild oleh scripts/build_dashboard.py — sinkron antara dashboard.html sistem &amp; wiki.'
        f'</div></div>'
    )
    return (
        '<!DOCTYPE html><html lang="id"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        '<title>Dashboard Audit-System v4 — Inspektorat II</title>'
        f'<style>{CSS}</style></head><body>'
        f'{body}'
        f'<script>{JS}</script></body></html>'
    )


def main() -> int:
    html = render_html()
    OUT_SYSTEM.write_text(html, encoding="utf-8")
    OUT_WIKI.write_text(html, encoding="utf-8")
    print(f"[build_dashboard] OK ({len(html)} chars).")
    print(f"  -> {OUT_SYSTEM.relative_to(ROOT)}")
    print(f"  -> {OUT_WIKI.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
