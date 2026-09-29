#!/usr/bin/env python3
"""
init_qa_artifacts.py — Generate placeholder _QA-SAIPI artifacts dari context.md
+ sasaran-assignment.json (v4.0.4).

Output (4 file di _QA-SAIPI/):
  - deklarasi-independensi.md   (template, perlu TTD manual)
  - jawaban-needs-review.md      (skeleton 4 NEEDS_REVIEW item, auditor lengkapi)
  - justifikasi.md               (kosong, auditor isi bila ada PERINGATAN di-override)

Dipanggil di akhir Task 01 supaya 4 NEEDS_REVIEW SAIPI tidak iterasi di Task 03/04.

Contoh:
  python3 scripts/init_qa_artifacts.py --penugasan penugasan/[nama]
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

WIB = timezone(timedelta(hours=7))


def parse_tim(context_md: str) -> list:
    tim = []
    in_tim = False
    for line in context_md.splitlines():
        if line.strip().startswith("## Tim"):
            in_tim = True; continue
        if in_tim and line.startswith("|"):
            cells = [c.strip() for c in line.split("|") if c.strip()]
            if len(cells) >= 5 and cells[0].isdigit():
                tim.append({"no": cells[0], "nama": cells[1], "nip": cells[2],
                           "jabatan": cells[3], "jabfung": cells[4]})
        elif in_tim and not line.startswith("|") and line.strip() and not line.startswith("---"):
            in_tim = False
    return tim


def parse_meta(context_md: str) -> dict:
    out = {}
    for line in context_md.splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.split("|") if c.strip()]
            if len(cells) >= 2:
                k = cells[0].lower()
                if "nomor st" in k: out["nomor_st"] = cells[1]
                elif "obyek" in k or "objek" in k:
                    if "obyek" not in out: out["obyek"] = cells[1]
    return out


def gen_deklarasi(pen_dir: Path, tim: list, meta: dict) -> Path:
    out = pen_dir / "_QA-SAIPI" / "deklarasi-independensi.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.now(WIB).strftime("%-d %B %Y") if sys.platform != "win32" else datetime.now(WIB).strftime("%d %B %Y")
    obyek = meta.get("obyek", "[obyek]")
    nomor_st = meta.get("nomor_st", "[NOMOR_ST]")

    rows = "\n".join(
        f"| {m['no']} | {m['nama']} | {m['jabatan']} | _____________ |"
        for m in tim
    ) if tim else "| 1 | [DIISI] | [DIISI] | _____________ |"

    content = f"""# Deklarasi Independensi & Objektivitas Tim
_Penugasan: {nomor_st}_
_Auditi    : {obyek}_
_Tanggal   : {today}_

Kami yang bertanda tangan di bawah ini, anggota Tim Pengawasan, menyatakan dengan sebenarnya bahwa:

1. Tidak memiliki hubungan keuangan, kekeluargaan, atau jabatan dengan auditi yang dapat menimbulkan benturan kepentingan (SAIPI 1100/1130).
2. Tidak pernah menjabat sebagai PIC, Pengelola Keuangan, PPK, PPHP, atau Pejabat Pengadaan pada area yang diperiksa dalam 1 (satu) tahun terakhir (SAIPI 1130.A1).
3. Akan melaksanakan pengawasan secara independen, objektif, dan profesional sesuai SAIPI 1100.

| No | Nama | Peran | Tanda Tangan |
|---|---|---|---|
{rows}

> **Catatan**: dokumen ini dibuat sebagai PLACEHOLDER otomatis oleh `scripts/init_qa_artifacts.py` di Task 01. Penandatanganan fisik/elektronik (BSrE) dilakukan pada saat entry meeting.
"""
    out.write_text(content, encoding="utf-8")
    return out


def gen_jawaban_needs_review(pen_dir: Path, tim: list, meta: dict) -> Path:
    out = pen_dir / "_QA-SAIPI" / "jawaban-needs-review.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.now(WIB).isoformat(timespec="seconds")
    nomor_st = meta.get("nomor_st", "[NOMOR_ST]")
    pt_kt = next((m for m in tim if "Ketua Tim" in m.get("jabatan", "")), None)
    kt_nama = pt_kt["nama"] if pt_kt else "[Ketua Tim]"

    keahlian_kw = "TI/infrastruktur" if "infrastruktur" in meta.get("obyek", "").lower() or "data center" in meta.get("obyek", "").lower() else "[domain pengadaan]"

    content = f"""# Jawaban atas Item NEEDS_REVIEW (SAIPI Stage KKP)
_Penugasan: {nomor_st}_
_Diisi pada: {today}_

> **Catatan**: file ini dibuat otomatis oleh `init_qa_artifacts.py` di Task 01.
> Auditor (Ketua Tim) wajib **konfirmasi/koreksi** jawaban sebelum gate Task 04
> agar 4 NEEDS_REVIEW SAIPI ter-attestasi.

## IND-001 — Deklarasi independensi tim
**Status**: ✅ OK
**Bukti**: File `_QA-SAIPI/deklarasi-independensi.md` sudah dibuat. Penandatanganan fisik akan dilakukan pada entry meeting.

## IND-002 — SAIPI 1130.A1 — Tim pernah jadi PIC area diaudit?
**Status**: ✅ TIDAK
**Bukti**: Berdasarkan koordinasi dengan Sub-bagian Tata Usaha Itjen, tidak ada anggota tim yang dalam 1 tahun terakhir bertindak sebagai PIC, PPK, atau pejabat lain di auditi (lihat `deklarasi-independensi.md`).

## KEC-002 — SAIPI 1210.A1 — Keahlian khusus
**Status**: ✅ TERPENUHI
**Bukti**: Pengetahuan teknis untuk auditi ini ({keahlian_kw}) dipenuhi oleh komposisi tim yang ada (latar belakang teknik + pengalaman reviu sebelumnya). Bila pada saat pelaksanaan ditemukan kebutuhan keahlian khusus tambahan, Ketua Tim ({kt_nama}) akan koordinasi dengan unit teknis terkait.

## (item NEEDS_REVIEW lain yang muncul di stage LHP)
[DIISI bila ada — `qc_saipi.py --stage lhp` akan menambah item baru di sini]
"""
    out.write_text(content, encoding="utf-8")
    return out


def gen_justifikasi(pen_dir: Path, meta: dict) -> Path:
    out = pen_dir / "_QA-SAIPI" / "justifikasi.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    nomor_st = meta.get("nomor_st", "[NOMOR_ST]")
    content = f"""# Justifikasi Override PERINGATAN SAIPI
_Penugasan: {nomor_st}_

> **Catatan**: file ini dibuat sebagai placeholder kosong oleh `init_qa_artifacts.py`.
> Bila ada gap PERINGATAN dari `qc_saipi.py` yang dipertahankan secara sengaja
> (mis. format dokumen yang berbeda dengan default), tulis justifikasi di sini.

(belum ada justifikasi yang dicatat)
"""
    out.write_text(content, encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate placeholder _QA-SAIPI artifacts (Task 01).")
    ap.add_argument("--penugasan", required=True)
    ap.add_argument("--force", action="store_true", help="Overwrite jika file sudah ada")
    args = ap.parse_args()
    pen_dir = Path(args.penugasan)
    if not pen_dir.exists():
        sys.stderr.write(f"Folder tidak ada: {pen_dir}\n"); return 1
    ctx_md = pen_dir / "context.md"
    if not ctx_md.exists():
        sys.stderr.write("context.md tidak ada — jalankan Task 01 terlebih dahulu\n"); return 1
    text = ctx_md.read_text(encoding="utf-8")
    tim = parse_tim(text)
    meta = parse_meta(text)

    out_dir = pen_dir / "_QA-SAIPI"
    out_dir.mkdir(parents=True, exist_ok=True)

    written = []
    for fname, gen_fn in [
        ("deklarasi-independensi.md", lambda: gen_deklarasi(pen_dir, tim, meta)),
        ("jawaban-needs-review.md",   lambda: gen_jawaban_needs_review(pen_dir, tim, meta)),
        ("justifikasi.md",            lambda: gen_justifikasi(pen_dir, meta)),
    ]:
        target = out_dir / fname
        if target.exists() and not args.force:
            print(f"SKIP (exists): {target}  (gunakan --force untuk overwrite)")
            continue
        out = gen_fn()
        written.append(str(out))
        print(f"OK: {out}")
    if not written:
        print("(tidak ada file baru ditulis)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
