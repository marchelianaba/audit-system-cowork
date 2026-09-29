#!/usr/bin/env python3
"""
prepare_lhp.py — Persiapkan template LHP untuk penugasan.
# ⚠ DEPRECATED (sejak v4.0.4): gunakan scripts/render_lhp.py untuk LHP placeholder-driven.
#    Script ini dipertahankan untuk kompatibilitas penugasan v4.0.0..v4.0.3 yang sedang berjalan.


Fungsi:
1. Baca context.md → ekstrak Nomor ST, Tanggal ST, Jenis Pengawasan
2. Pilih template yang sesuai dari folder templates/
3. Salin template ke _LHP/ dengan nama LHP-[nomor-ST-safe].docx
4. Ganti [NOMOR_ST] dan [TANGGAL_ST] di dokumen dengan nilai asli

Format template yang didukung:
  - .docx  → disalin langsung, placeholder diganti di file
  - .gdoc  → baca doc_id dari JSON, output instruksi untuk Claude fetch via Google Drive MCP

Usage:
    python scripts/prepare_lhp.py <path-folder-penugasan>
    python scripts/prepare_lhp.py <path-folder-penugasan> --template "Laporan Hasil Reviu Pengadaan"

Contoh:
    python scripts/prepare_lhp.py penugasan/2026-084-reviu-pengadaan-dc-psre/
"""

import json
import re
import shutil
import sys
from pathlib import Path

# ─── Mapping: Jenis Pengawasan → nama file template (tanpa ekstensi) ──────────
# Script otomatis mencari .docx dulu, lalu fallback ke .gdoc
TEMPLATE_MAP = {
    # Urutan: kunci lebih panjang dulu agar tidak salah match
    "survei pendahuluan audit kinerja": "Laporan Hasil Survei Pendahuluan Audit Kinerja",
    "survei pendahuluan":               "Laporan Hasil Survei Pendahuluan Audit Kinerja",
    "audit pengadaan":                  "Laporan Hasil Audit",
    "audit kinerja":                    "Laporan Hasil Audit",
    "audit":                            "Laporan Hasil Audit",

    "penjaminan kualitas atas penilaian mandiri": "Laporan Hasil Penjaminan Kualitas atas Penilaian Mandiri Pelaksanaan SPIP",
    "penilaian mandiri spip":                     "Laporan Hasil Penjaminan Kualitas atas Penilaian Mandiri Pelaksanaan SPIP",
    "penjaminan kualitas spip":                   "Laporan Hasil Penjaminan Kualitas Pelaksanaan SPIP",
    "evaluasi spip":                              "Laporan Hasil Penjaminan Kualitas Pelaksanaan SPIP",
    "evaluasi maturitas spip":                    "Laporan Hasil Penjaminan Kualitas Pelaksanaan SPIP",

    "evaluasi reformasi birokrasi":  "Laporan Hasil Evaluasi RB",
    "evaluasi rb":                   "Laporan Hasil Evaluasi RB",
    "evaluasi manajemen risiko":     "Laporan Hasil Evaluasi Manajemen Risiko",
    "evaluasi mr":                   "Laporan Hasil Evaluasi Manajemen Risiko",
    "evaluasi sakip":                "Laporan Hasil Evaluasi SAKIP",
    "evaluasi akip":                 "Laporan Hasil Evaluasi SAKIP",
    "evaluasi akuntabilitas":        "Laporan Hasil Evaluasi SAKIP",

    "reviu dokumen alokasi anggaran": "Laporan Hasil Reviu Dokumen Alokasi Anggaran untuk Pemenuhan Prioritas Direktif",
    "reviu alokasi anggaran":         "Laporan Hasil Reviu Dokumen Alokasi Anggaran untuk Pemenuhan Prioritas Direktif",
    "reviu direktif":                 "Laporan Hasil Reviu Dokumen Alokasi Anggaran untuk Pemenuhan Prioritas Direktif",
    "reviu dokumen kontrak":          "Laporan Hasil Reviu Dokumen Kontrak",
    "reviu kontrak":                  "Laporan Hasil Reviu Dokumen Kontrak",
    "reviu laporan kinerja":          "Laporan Hasil Reviu Laporan Kinerja",
    "reviu revisi rencana kerja":     "Laporan Hasil Reviu Revisi Rencana Kerja",
    "reviu revisi rk":                "Laporan Hasil Reviu Revisi Rencana Kerja",
    "reviu rencana kerja dan anggaran": "Laporan Hasil Reviu Rencana Kerja dan Anggaran",
    "reviu rka-kl":                   "Laporan Hasil Reviu Rencana Kerja dan Anggaran",
    "reviu rka":                      "Laporan Hasil Reviu Rencana Kerja dan Anggaran",
    "reviu anggaran":                 "Laporan Hasil Reviu Rencana Kerja dan Anggaran",
    "reviu rencana kerja":            "Laporan Hasil Reviu Rencana Kerja dan Anggaran",
    "reviu pengadaan":                "Laporan Hasil Reviu Pengadaan",

    "pemantauan tindak lanjut":   "Laporan Hasil Pemantauan TLHP",
    "pemantauan tlhp":            "Laporan Hasil Pemantauan TLHP",
    "pemantauan pengadaan":       "Laporan Hasil Pemantauan",
    "pemantauan":                 "Laporan Hasil Pemantauan",

    "pendampingan akuntabilitas pengadaan": "Laporan Hasil Pendampingan Akuntabilitas Pengadaan Barang Jasa",
    "pendampingan akuntabilitas":          "Laporan Hasil Pendampingan Akuntabilitas Pengadaan Barang Jasa",
    "pendampingan pbj":                    "Laporan Hasil Pendampingan Akuntabilitas Pengadaan Barang Jasa",
    "pendampingan":                        "Laporan Hasil Pendampingan Akuntabilitas Pengadaan Barang Jasa",
}


def find_audit_system_root(start: Path) -> Path:
    """Cari root audit-system-v4 ke atas dari start."""
    p = start.resolve()
    for _ in range(10):
        if (p / "README.md").exists() and (p / "templates").exists():
            return p
        p = p.parent
    raise FileNotFoundError(
        f"Tidak menemukan root audit-system-v4 (folder berisi README.md + templates/)\n"
        f"dari: {start}"
    )


def read_context(penugasan_dir: Path) -> dict:
    """Baca context.md dan ekstrak field yang diperlukan."""
    ctx_file = penugasan_dir / "context.md"
    if not ctx_file.exists():
        raise FileNotFoundError(
            f"context.md tidak ditemukan di: {penugasan_dir}\n"
            "Jalankan Task 01 terlebih dahulu untuk membuat context.md"
        )

    text = ctx_file.read_text(encoding="utf-8")
    fields = {
        "nomor_st":   r"Nomor ST\s*:\s*(.+)",
        "tanggal_st": r"Tanggal ST\s*:\s*(.+)",
        "jenis":      r"Jenis Pengawasan\s*:\s*(.+)",
        "obyek":      r"Obyek\s*:\s*(.+)",
        "template":   r"Template LHP\s*:\s*(.+)",
    }
    result = {}
    for key, pat in fields.items():
        m = re.search(pat, text, re.IGNORECASE)
        val = m.group(1).strip() if m else ""
        if val in ("[DIISI AUDITOR]", "-", "—"):
            val = ""
        result[key] = val

    missing = [k for k in ("nomor_st", "tanggal_st", "jenis") if not result.get(k)]
    if missing:
        raise ValueError(
            f"Field berikut kosong di context.md: {', '.join(missing)}\n"
            "Isi terlebih dahulu sebelum menjalankan script ini."
        )
    return result


def read_gdoc_id(gdoc_path: Path) -> str:
    """Baca Google Doc ID dari file .gdoc."""
    try:
        data = json.loads(gdoc_path.read_text(encoding="utf-8"))
        return data.get("doc_id", "")
    except (json.JSONDecodeError, KeyError):
        return ""


def select_template(jenis: str, templates_dir: Path, hint: str = "") -> dict:
    """
    Pilih template berdasarkan Jenis Pengawasan.
    Return dict: {
        "type": "docx" | "gdoc",
        "path": Path,       # path ke file template
        "name": str,        # nama template tanpa ekstensi
        "doc_id": str       # Google Doc ID (kosong jika .docx)
    }
    """
    # 1. Cek hint dari context.md (bisa dengan atau tanpa ekstensi)
    if hint and hint not in ("", "-", "—", "[DIISI AUDITOR]"):
        hint_stem = hint.replace(".docx", "").replace(".gdoc", "").strip()
        # Coba .docx dulu
        for ext in (".docx", ".gdoc"):
            t = templates_dir / (hint_stem + ext)
            if t.exists():
                doc_id = read_gdoc_id(t) if ext == ".gdoc" else ""
                return {"type": ext[1:], "path": t, "name": hint_stem, "doc_id": doc_id}

    # 2. Match berdasarkan TEMPLATE_MAP
    jenis_lower = jenis.lower().strip()
    best_key, best_name = "", ""
    for key, name in TEMPLATE_MAP.items():
        if key in jenis_lower and len(key) > len(best_key):
            best_key, best_name = key, name

    if best_name:
        # Coba .docx dulu (lebih cepat, tidak perlu fetch)
        for ext in (".docx", ".gdoc"):
            t = templates_dir / (best_name + ext)
            if t.exists():
                doc_id = read_gdoc_id(t) if ext == ".gdoc" else ""
                return {"type": ext[1:], "path": t, "name": best_name, "doc_id": doc_id}
        # Template ada di map tapi file tidak ada — coba fuzzy match
        for f in list(templates_dir.glob("*.docx")) + list(templates_dir.glob("*.gdoc")):
            if best_name.lower()[:20] in f.stem.lower():
                ext = f.suffix[1:]
                doc_id = read_gdoc_id(f) if ext == "gdoc" else ""
                return {"type": ext, "path": f, "name": f.stem, "doc_id": doc_id}

    # 3. Tidak ketemu
    available_docx = sorted(f.stem for f in templates_dir.glob("*.docx"))
    available_gdoc = sorted(f.stem for f in templates_dir.glob("*.gdoc"))
    all_available = "\n".join(
        [f"  - {n} (.docx)" for n in available_docx] +
        [f"  - {n} (.gdoc)" for n in available_gdoc]
    )
    raise ValueError(
        f"Template untuk jenis '{jenis}' tidak bisa ditentukan otomatis.\n"
        f"Template tersedia di {templates_dir}:\n{all_available}\n\n"
        "Tentukan secara manual dengan mengisi 'Template LHP' di context.md"
    )


def safe_filename(text: str) -> str:
    """Buat nama file aman."""
    safe = re.sub(r'[<>:"/\\|?*\s]', '-', text)
    safe = re.sub(r'-+', '-', safe).strip('-')
    return safe


def replace_in_docx(docx_path: Path, nomor_st: str, tanggal_st: str) -> tuple:
    """
    Ganti [NOMOR_ST] dan [TANGGAL_ST] langsung di ZIP (docx).
    Return (n_nomor_replaced, n_tanggal_replaced).
    """
    import io
    import zipfile as zf

    buf = io.BytesIO(docx_path.read_bytes())
    out_buf = io.BytesIO()
    n_nomor_total = 0
    n_tanggal_total = 0

    with zf.ZipFile(buf, 'r') as zin, zf.ZipFile(out_buf, 'w', zf.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)

            if item.filename.endswith('.xml') or item.filename.endswith('.rels'):
                try:
                    text = data.decode('utf-8')
                    new_text, n1 = re.subn(r'\[NOMOR_ST\]', nomor_st, text)
                    new_text, n2 = re.subn(r'\[TANGGAL_ST\]', tanggal_st, new_text)
                    n_nomor_total += n1
                    n_tanggal_total += n2
                    data = new_text.encode('utf-8')
                except UnicodeDecodeError:
                    pass

            zout.writestr(item, data)

    docx_path.write_bytes(out_buf.getvalue())
    return n_nomor_total, n_tanggal_total


def prepare_template(penugasan_dir_arg: str, template_hint_override: str = "") -> dict:
    """Proses utama."""
    penugasan_dir = Path(penugasan_dir_arg).resolve()
    if not penugasan_dir.exists():
        raise FileNotFoundError(f"Folder penugasan tidak ada: {penugasan_dir}")

    audit_root = find_audit_system_root(penugasan_dir)
    templates_dir = audit_root / "templates"

    ctx = read_context(penugasan_dir)
    nomor_st   = ctx["nomor_st"]
    tanggal_st = ctx["tanggal_st"]
    jenis      = ctx["jenis"]
    obyek      = ctx["obyek"]

    print(f"Penugasan   : {penugasan_dir.name}")
    print(f"Nomor ST    : {nomor_st}")
    print(f"Tanggal ST  : {tanggal_st}")
    print(f"Jenis       : {jenis}")
    print(f"Obyek       : {obyek}")
    print()

    hint = template_hint_override or ctx.get("template", "")
    tmpl = select_template(jenis, templates_dir, hint)

    lhp_dir = penugasan_dir / "_LHP"
    lhp_dir.mkdir(exist_ok=True)
    safe_nomor = safe_filename(nomor_st)

    # ── Jalur A: Template .docx (lokal) ──────────────────────────────────────
    if tmpl["type"] == "docx":
        print(f"Template    : {tmpl['name']}.docx  [lokal]")
        output_filename = f"LHP-{safe_nomor}.docx"
        output_path = lhp_dir / output_filename

        shutil.copy2(str(tmpl["path"]), str(output_path))
        print(f"Disalin ke  : {output_path.relative_to(penugasan_dir.parent)}")

        n_nomor, n_tanggal = replace_in_docx(output_path, nomor_st, tanggal_st)

        print()
        print("Placeholder diganti:")
        print(f"  [NOMOR_ST]   → '{nomor_st}'  ({n_nomor}x)")
        print(f"  [TANGGAL_ST] → '{tanggal_st}'  ({n_tanggal}x)")
        print()
        print(f"✓ File siap  : {output_path}")

        return {
            "mode": "docx",
            "output_path": str(output_path),
            "template_used": tmpl["name"],
            "nomor_st": nomor_st,
            "tanggal_st": tanggal_st,
            "n_nomor": n_nomor,
            "n_tanggal": n_tanggal,
        }

    # ── Jalur B: Template .gdoc (Google Drive) ────────────────────────────────
    else:
        doc_id  = tmpl["doc_id"]
        doc_url = f"https://docs.google.com/document/d/{doc_id}/edit" if doc_id else ""
        stub_path = lhp_dir / f"LHP-{safe_nomor}.gdoc.txt"

        info = (
            f"# Template LHP — Instruksi Fetch Google Drive\n\n"
            f"Penugasan   : {penugasan_dir.name}\n"
            f"Nomor ST    : {nomor_st}\n"
            f"Tanggal ST  : {tanggal_st}\n"
            f"Jenis       : {jenis}\n"
            f"Template    : {tmpl['name']}\n"
            f"Google Doc  : {doc_url}\n"
            f"Doc ID      : {doc_id}\n\n"
            f"## Langkah selanjutnya untuk Claude\n\n"
            f"1. Fetch konten template via Google Drive MCP:\n"
            f"   Tool: google_drive_fetch\n"
            f"   document_ids: [\"{doc_id}\"]\n\n"
            f"2. Buat file LHP-{safe_nomor}.docx di folder _LHP/ menggunakan skill docx\n"
            f"   dengan struktur dari template di atas\n\n"
            f"3. Ganti placeholder:\n"
            f"   [NOMOR_ST]   → {nomor_st}\n"
            f"   [TANGGAL_ST] → {tanggal_st}\n"
        )

        stub_path.write_text(info, encoding="utf-8")

        print(f"Template    : {tmpl['name']}.gdoc  [Google Drive]")
        print(f"Google Doc  : {doc_url}")
        print(f"Doc ID      : {doc_id}")
        print()
        print("⚠️  Template tersimpan di Google Drive, bukan file lokal .docx")
        print(f"   Instruksi fetch disimpan di: {stub_path}")
        print()
        print("Langkah selanjutnya (untuk Claude):")
        print(f"  1. Fetch template via Google Drive MCP: document_ids=[\"{doc_id}\"]")
        print(f"  2. Buat file _LHP/LHP-{safe_nomor}.docx menggunakan konten template tersebut")
        print(f"  3. Ganti [NOMOR_ST] → {nomor_st}  dan  [TANGGAL_ST] → {tanggal_st}")

        return {
            "mode": "gdoc",
            "doc_id": doc_id,
            "doc_url": doc_url,
            "template_name": tmpl["name"],
            "stub_path": str(stub_path),
            "nomor_st": nomor_st,
            "tanggal_st": tanggal_st,
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    # Parse argumen opsional: --template "nama template"
    penugasan_arg = sys.argv[1]
    hint_arg = ""
    if "--template" in sys.argv:
        idx = sys.argv.index("--template")
        if idx + 1 < len(sys.argv):
            hint_arg = sys.argv[idx + 1]

    try:
        prepare_template(penugasan_arg, hint_arg)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
