#!/usr/bin/env python3
"""integral_inject.py — Auto-inject KKP temuan ke INTEGRAL via API.

Format payload sesuai contoh dari tim SIMWAS (29 April 2026):
  - Pakai dua field terpisah: 'disusun_oleh' (nama) + 'nip' (18 digit)
  - Field opsional 'id_sasaran' (integer) per temuan
  - Response struktur: {success, message, kertas_kerja{id, nomor, internal_id, ...}, temuan_count}

Env vars wajib:
  INTEGRAL_API_BASE_URL, INTEGRAL_SERVICE_TOKEN, COWORK_USER_EMAIL

Skip-list (tetap manual):
  konsultasi-pengadaan, evaluasi-spip, evaluasi-reformasi-birokrasi, pemantauan-tindak-lanjut
"""
from __future__ import annotations
import argparse, json, os, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    sys.stderr.write("ERROR: pip install requests\n")
    sys.exit(1)

WIB = timezone(timedelta(hours=7))

SKIP_LIST = {
    "konsultasi-pengadaan",
    "evaluasi-spip",
    "evaluasi-reformasi-birokrasi",
    "pemantauan-tindak-lanjut",
}

REQUIRED_ENV_VARS = ["INTEGRAL_API_BASE_URL", "INTEGRAL_SERVICE_TOKEN", "COWORK_USER_EMAIL"]


def _now_iso():
    return datetime.now(WIB).isoformat(timespec="seconds")


def _read_role(penugasan_dir):
    p = penugasan_dir / "_ROLE.md"
    if not p.exists():
        sys.stderr.write(f"ERROR: _ROLE.md tidak ditemukan di {penugasan_dir}\n")
        sys.exit(1)
    out = {"nama": None, "role": None, "role_kode": None, "nip": None}
    in_fm = False
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip() == "---":
            in_fm = not in_fm
            continue
        if in_fm and ":" in line:
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip()
            if k == "nama_lengkap": out["nama"] = v
            elif k == "role": out["role"] = v
            elif k == "role_kode": out["role_kode"] = v.upper()
            elif k == "nip": out["nip"] = v
    return out


def _resolve_nip(role):
    return role.get("nip") or os.environ.get("COWORK_USER_NIP")


def _validate_env():
    missing = [v for v in REQUIRED_ENV_VARS if not os.environ.get(v)]
    if missing:
        sys.stderr.write("ERROR: env var belum ter-set: " + ", ".join(missing) + "\n")
        sys.exit(1)
    return {
        "base_url": os.environ["INTEGRAL_API_BASE_URL"].rstrip("/"),
        "token": os.environ["INTEGRAL_SERVICE_TOKEN"],
        "email": os.environ["COWORK_USER_EMAIL"],
    }


def _read_temuan_json(penugasan_dir):
    p = penugasan_dir / "_KKP" / "temuan.json"
    if not p.exists():
        sys.stderr.write(f"ERROR: temuan.json tidak ditemukan di {p}\n")
        sys.exit(2)
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.stderr.write(f"ERROR: temuan.json tidak valid: {e}\n")
        sys.exit(2)
    if "penugasan" not in d or "temuan" not in d:
        sys.stderr.write("ERROR: temuan.json tidak punya field 'penugasan' atau 'temuan'\n")
        sys.exit(2)
    return d


def _filter_by_anggota(temuan, nama):
    return [t for t in temuan
            if t.get("anggota_tim", {}).get("nama_lengkap") == nama
            and t.get("status") in ("DISETUJUI", "DIREVIU_KETUA_TIM")
            and not (t.get("integral") or {}).get("id_integral")]


def _map_temuan(temuan_list):
    """Konversi temuan v4 ke format payload INTEGRAL.

    v4.4 update: kirim kodefikasi_temuan dan kodefikasi_rekomendasi dari
    PermenPAN 42/2011 (sebelumnya null). Lihat references/permenpan-42-2011-kode.json.
    """
    out = []
    for i, t in enumerate(temuan_list, start=1):
        item = {
            "no": i,
            "judul_temuan": t.get("judul_temuan", "")[:200],
            "kondisi": t.get("kondisi", ""),
            "kriteria": t.get("kriteria", ""),
            "sebab": t.get("sebab"),
            "akibat": t.get("akibat"),
            "uraian_rekomendasi": None,
            "kodefikasi_temuan": t.get("kodefikasi_temuan"),
            "kodefikasi_rekomendasi": t.get("kodefikasi_rekomendasi"),
            "kodefikasi_sebab": t.get("kodefikasi_sebab"),
        }
        sid = t.get("sasaran_id")
        if sid and isinstance(sid, str) and sid.startswith("S-"):
            item["id_sasaran"] = sid
        out.append(item)
    return out


def _post_to_integral(env, payload):
    url = f"{env['base_url']}/kertas-kerja"
    headers = {
        "Authorization": f"Bearer {env['token']}",
        "Content-Type": "application/json",
        "X-Source": "audit-system-v4",
        "X-Cowork-User-Email": env["email"],
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=15)
    except requests.exceptions.RequestException as e:
        sys.stderr.write(f"ERROR: gagal hubungi INTEGRAL: {e}\n")
        sys.exit(3)
    if r.status_code in (200, 201):
        try:
            d = r.json()
        except ValueError:
            sys.stderr.write(f"ERROR: response bukan JSON: {r.text[:300]}\n")
            sys.exit(3)
        if not d.get("success", True):
            sys.stderr.write(f"ERROR: SIMWAS tolak request. {d.get('message', '')}\n")
            sys.exit(3)
        return d
    if r.status_code == 403:
        sys.stderr.write("ERROR 403: akses ditolak. Hubungi Admin Inspektorat II.\n")
        sys.exit(3)
    if r.status_code == 404:
        sys.stderr.write("ERROR 404: id_penugasan tidak ditemukan.\n")
        sys.exit(3)
    if r.status_code == 422:
        sys.stderr.write(f"ERROR 422: validasi gagal. {r.text[:500]}\n")
        sys.exit(3)
    sys.stderr.write(f"ERROR {r.status_code}: {r.text[:500]}\n")
    sys.exit(3)


def _update_status(penugasan_dir, nama, response):
    p = penugasan_dir / "_KKP" / "temuan.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    kk = response.get("kertas_kerja", {})
    id_int = str(kk.get("id", "")) or str(kk.get("internal_id", ""))
    nomor = kk.get("nomor", "")
    ts = _now_iso()
    for t in d.get("temuan", []):
        if t.get("anggota_tim", {}).get("nama_lengkap") == nama \
                and t.get("status") in ("DISETUJUI", "DIREVIU_KETUA_TIM") \
                and not (t.get("integral") or {}).get("id_integral"):
            t["status"] = "DIINJECT_INTEGRAL"
            t["integral"] = {"id_integral": id_int, "nomor_kkp": nomor, "tanggal_inject": ts}
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


def _log_trail(penugasan_dir, action, payload):
    import subprocess
    sp = Path(__file__).parent / "audit_trail.py"
    if not sp.exists():
        return
    try:
        subprocess.run(["python3", str(sp), "log-event",
                        "--penugasan", str(penugasan_dir),
                        "--action", action, "--task", "03",
                        "--target", "_KKP/temuan.json",
                        "--payload", json.dumps(payload, ensure_ascii=False)],
                       check=False, capture_output=True)
    except Exception:
        pass


def main():
    ap = argparse.ArgumentParser(description="Inject KKP ke INTEGRAL via API.")
    ap.add_argument("--penugasan", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    pdir = Path(args.penugasan).resolve()
    if not pdir.is_dir():
        sys.stderr.write(f"ERROR: folder tidak ditemukan: {pdir}\n")
        sys.exit(1)

    env = _validate_env() if not args.dry_run else {"base_url": "(dry)", "token": "(dry)", "email": "(dry)"}
    role = _read_role(pdir)
    if role.get("role_kode") != "AT":
        sys.stderr.write(f"ERROR: hanya Anggota Tim yang boleh inject. User: {role.get('role')}\n")
        sys.exit(1)

    nip = _resolve_nip(role)
    if not nip and not args.dry_run:
        sys.stderr.write("ERROR: NIP tidak ada di _ROLE.md / env COWORK_USER_NIP\n")
        sys.exit(2)
    if nip and (not nip.isdigit() or len(nip) != 18):
        sys.stderr.write(f"ERROR: NIP harus 18 digit angka. Saat ini: {nip}\n")
        sys.exit(2)

    data = _read_temuan_json(pdir)
    jenis = data["penugasan"].get("jenis_pengawasan", "")
    id_pen = data["penugasan"].get("id", "")

    if jenis in SKIP_LIST:
        print(f"INFO: jenis '{jenis}' tidak di-auto-inject (output format khusus).")
        print(f"      Silakan inject manual ke INTEGRAL menggunakan output di _KKP/.")
        sys.exit(0)

    temuan_anggota = _filter_by_anggota(data["temuan"], role["nama"])
    if not temuan_anggota:
        print(f"INFO: tidak ada temuan baru untuk '{role['nama']}' yang siap diinject.")
        sys.exit(0)

    payload = {
        "id_penugasan": id_pen,
        "disusun_oleh": role["nama"],
        "nip": nip,
        "tanggal": datetime.now(WIB).strftime("%Y-%m-%d"),
        "temuan": _map_temuan(temuan_anggota),
        "status": "ai_draft",
        "sumber": "audit-system-v4",
        "ai_metadata": {
            "model": "claude-via-cowork",
            "generated_at": _now_iso(),
            "jenis_pengawasan": jenis,
            "anggota_tim": role["nama"],
            "jumlah_temuan": len(temuan_anggota),
        },
    }

    if args.dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        sys.exit(0)

    print(f"Mengirim {len(temuan_anggota)} temuan ke INTEGRAL...")
    response = _post_to_integral(env, payload)
    _update_status(pdir, role["nama"], response)
    kk = response.get("kertas_kerja", {})
    _log_trail(pdir, "INTEGRAL_EXPORT", {
        "id_kkp": kk.get("id"),
        "internal_id": kk.get("internal_id"),
        "nomor_kkp": kk.get("nomor"),
        "status_code": kk.get("status"),
        "temuan_count": response.get("temuan_count", len(temuan_anggota)),
        "anggota_tim": role["nama"],
        "jenis_pengawasan": jenis,
    })

    print()
    print("=" * 60)
    print("KKP berhasil dikirim ke INTEGRAL dengan status DRAFT.")
    print("=" * 60)
    print(f"ID KKP       : {kk.get('id', '(?)')}")
    print(f"Nomor KKP    : {kk.get('nomor', '(?)')}")
    print(f"Internal ID  : {kk.get('internal_id', '(?)')}")
    print(f"Jumlah temuan: {response.get('temuan_count', len(temuan_anggota))}")
    print()
    print("PENTING: KKP belum final. Login ke INTEGRAL,")
    print("         buka KKP nomor di atas, review, lalu klik 'Approve'")
    print("         agar muncul di dashboard ketua tim/pimpinan.")
    print()
    sys.exit(0)


if __name__ == "__main__":
    main()
