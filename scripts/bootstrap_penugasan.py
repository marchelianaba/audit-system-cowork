#!/usr/bin/env python3
"""
bootstrap_penugasan.py — Initialize folder penugasan dengan standar v4.0.4 dalam 1 call.

Yang dilakukan:
  1. Buat folder standar: _PKP/, _KKP/, _LHP/, _AUDIT-TRAIL/, _QA-SAIPI/, 00-input/
  2. Tulis _ROLE.md dari --nama, --role-kode (default: AT)
  3. Log ROLE_LOGIN ke audit trail
  4. (Opsional) clean output sebelum mulai dengan --clean
  5. (Opsional setelah context.md ada) auto-gen QA placeholder + run preflight

Tujuan: ganti 5-6 langkah manual jadi 1 call. Aman dipanggil ulang (idempotent).

Contoh:
  # Bootstrap baru, role default AT
  python3 scripts/bootstrap_penugasan.py --penugasan penugasan/[nama] --nama "Sarah Aulia"

  # Bootstrap dengan role KT
  python3 scripts/bootstrap_penugasan.py --penugasan penugasan/[nama] --nama "Andi Pratama" --role-kode KT

  # Clean output sebelum mulai (KKP, LHP, audit trail)
  python3 scripts/bootstrap_penugasan.py --penugasan penugasan/[nama] --nama "Sarah Aulia" --clean

  # Setelah Task 01 jalan dan context.md ada, jalankan post-init
  python3 scripts/bootstrap_penugasan.py --penugasan penugasan/[nama] --post-task01
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

WIB = timezone(timedelta(hours=7))

ROLE_NAMES = {
    "AT": "Anggota Tim",
    "KT": "Ketua Tim",
    "PT": "Pengendali Teknis",
    "PM": "Pengendali Mutu",
}

STANDARD_DIRS = ["_PKP", "_KKP", "_LHP", "_AUDIT-TRAIL", "_QA-SAIPI", "00-input"]


def now_iso() -> str:
    return datetime.now(WIB).isoformat(timespec="seconds")


def write_role(pen_dir: Path, nama: str, role_kode: str, validated: bool = False) -> Path:
    role_kode = role_kode.upper()
    if role_kode not in ROLE_NAMES:
        raise ValueError(f"role_kode '{role_kode}' tidak dikenal — pakai AT/KT/PT/PM")
    role_label = ROLE_NAMES[role_kode]
    out = pen_dir / "_ROLE.md"
    content = f"""---
nama_lengkap: {nama}
role: {role_label}
role_kode: {role_kode}
role_validated_against_pkp: {str(validated).lower()}
session_start: {now_iso()}
---

# Sesi Aktif — {nama} ({role_label})

Penugasan: {pen_dir.name}
"""
    out.write_text(content, encoding="utf-8")
    return out


def clean_outputs(pen_dir: Path) -> int:
    """Bersihkan folder output (kecuali 00-input). Return jumlah file dihapus."""
    deleted = 0
    targets = ["_KKP", "_LHP", "_AUDIT-TRAIL", "_QA-SAIPI", "_PKP"]
    for d in targets:
        target_dir = pen_dir / d
        if target_dir.exists():
            for f in target_dir.iterdir():
                if f.is_file():
                    try:
                        f.unlink()
                        deleted += 1
                    except OSError as e:
                        sys.stderr.write(f"WARN: gagal hapus {f}: {e}\n")
    # juga hapus context.md
    ctx = pen_dir / "context.md"
    if ctx.exists():
        try:
            ctx.unlink(); deleted += 1
        except OSError:
            pass
    role = pen_dir / "_ROLE.md"
    if role.exists():
        try:
            role.unlink(); deleted += 1
        except OSError:
            pass
    return deleted


def run_audit_log(pen_dir: Path, action: str, target: str, task: str, payload: dict) -> bool:
    import json
    script_dir = Path(__file__).resolve().parent
    cmd = [sys.executable, str(script_dir / "audit_trail.py"), "log-event",
           "--penugasan", str(pen_dir),
           "--action", action,
           "--target", target,
           "--task", task,
           "--payload", json.dumps(payload, ensure_ascii=False)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(f"WARN: audit_trail log-event gagal: {r.stderr}\n")
        return False
    return True


def run_init_qa(pen_dir: Path) -> bool:
    script_dir = Path(__file__).resolve().parent
    cmd = [sys.executable, str(script_dir / "init_qa_artifacts.py"),
           "--penugasan", str(pen_dir)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout, end="")
    if r.returncode != 0:
        sys.stderr.write(f"WARN: init_qa_artifacts gagal: {r.stderr}\n")
        return False
    return True


def run_preflight(pen_dir: Path) -> int:
    script_dir = Path(__file__).resolve().parent
    cmd = [sys.executable, str(script_dir / "qc_saipi.py"),
           "--penugasan", str(pen_dir),
           "--preflight-context"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout, end="")
    if r.stderr:
        sys.stderr.write(r.stderr)
    return r.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description="Bootstrap folder penugasan v4.0.4 dalam 1 call.")
    ap.add_argument("--penugasan", required=True)
    ap.add_argument("--nama", help="Nama lengkap user (untuk _ROLE.md)")
    ap.add_argument("--role-kode", default="AT", help="AT/KT/PT/PM (default: AT)")
    ap.add_argument("--clean", action="store_true",
                    help="Bersihkan output (KKP/LHP/audit trail/context) sebelum mulai")
    ap.add_argument("--post-task01", action="store_true",
                    help="Setelah Task 01 jalan & context.md ada — jalankan init_qa_artifacts + preflight")
    args = ap.parse_args()

    pen_dir = Path(args.penugasan)
    if not pen_dir.exists():
        sys.stderr.write(f"ERROR: folder penugasan tidak ada: {pen_dir}\n"); return 1

    # 1. Standar dir
    for d in STANDARD_DIRS:
        (pen_dir / d).mkdir(parents=True, exist_ok=True)
    print(f"OK: 6 standard dirs di {pen_dir.name}/")

    # 2. Clean (opsional)
    if args.clean:
        n = clean_outputs(pen_dir)
        print(f"OK: clean — {n} file dihapus")

    # 3. _ROLE.md (kalau --nama diberikan)
    if args.nama:
        role_path = write_role(pen_dir, args.nama, args.role_kode)
        print(f"OK: _ROLE.md → {args.nama} ({args.role_kode})")
        run_audit_log(pen_dir, "ROLE_LOGIN", "_ROLE.md", "00",
                      {"nama": args.nama, "role_kode": args.role_kode.upper(),
                       "source": "bootstrap_penugasan"})
        print(f"OK: audit trail ROLE_LOGIN logged")

    # 4. Post-Task01 mode
    if args.post_task01:
        ctx = pen_dir / "context.md"
        sa = pen_dir / "_PKP" / "sasaran-assignment.json"
        if not ctx.exists():
            sys.stderr.write("WARN: context.md belum ada — skip post-task01 step\n")
            return 0
        if not sa.exists():
            sys.stderr.write("WARN: _PKP/sasaran-assignment.json belum ada — skip post-task01 step\n")
            return 0
        print("\n--- post-task01: init QA artifacts ---")
        run_init_qa(pen_dir)
        print("\n--- post-task01: preflight QC SAIPI ---")
        rc = run_preflight(pen_dir)
        if rc == 2:
            sys.stderr.write("\n⛔ Preflight FAIL — perbaiki context.md sebelum lanjut Task 03.\n")
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
