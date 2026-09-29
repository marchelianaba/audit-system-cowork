# Task 00 — Identifikasi Role (WAJIB tiap sesi)

> **Model**: `claude-haiku-4-5-20251001` — Tanya jawab singkat, tidak perlu penalaran berat.

## Tujuan
Memastikan Claude tahu **siapa** yang sedang bekerja dan **peran**nya di tim audit, sebelum task lain dijalankan. Role ini menentukan task & sasaran apa yang boleh diakses.

> Task ini **WAJIB dijalankan paling awal di setiap sesi** sebelum Task 01/03/04. Tanpa `_ROLE.md` valid, semua task lain akan menolak eksekusi.

---

## Aturan Role

| Role | Boleh Akses Task | Boleh Akses Skill |
|------|------------------|-------------------|
| **Anggota Tim** | Task 00, Task 01, Task 03 (KKP) | Semua 10 skill audit + skill pendukung wiki + script QC `qc_kkp_lhp.py --only kkp` |
| **Ketua Tim** | Task 00, Task 04 (LHP) | Semua skill yang dipakai untuk LHP + wiki + QC `--only lhp` |

Anggota tim **tidak boleh** menjalankan Task 04 (LHP). Ketua tim **tidak boleh** menjalankan Task 03 (KKP) — KKP adalah hasil kerja anggota tim sesuai pembagian sasaran di PKP.

> **Pengendali Mutu (PM)** dan **Pengendali Teknis (PT)** secara default disetarakan dengan Ketua Tim untuk akses sistem (boleh Task 04). Override manual bila diperlukan dengan field `role_override` di `_ROLE.md`.

---

## ⚠️ ATURAN ANTI-ASUMSI IDENTITAS (v4.5 — WAJIB)

**Claude DILARANG mengasumsikan identitas user dari `_ROLE.md` yang sudah ada.**

Setiap kali Task 00 dipanggil (= setiap sesi chat baru), Claude WAJIB:

1. **SELALU TANYA** Pertanyaan 1, 2, 3 di bawah (nama, role, NIP) — TIDAK ada shortcut "load _ROLE.md langsung".
2. **Setelah jawaban diterima**, baru cek `_ROLE.md` lama untuk validasi/cross-check.
3. **Tampilkan ke user**: hasil input vs `_ROLE.md` lama (kalau ada).
4. **Tulis `_ROLE.md` baru** (overwrite kalau berbeda) + append ke `_ROLE-history.jsonl` untuk audit trail multi-role.

**Alasan**: Auditor yang berbeda (AT vs KT, atau anggota tim yang berganti) dapat membuka penugasan yang sama di waktu berbeda. `_ROLE.md` sebelumnya tidak boleh menjadi presumsi identitas auditor yang sedang chat sekarang.

---

## Langkah Eksekusi

### 1. (BARU v4.5) Cek `_ROLE.md` lama HANYA sebagai konteks — JANGAN auto-load

Path: `penugasan/[nama-penugasan]/_ROLE.md`

- Kalau **ada**: baca isinya, simpan sebagai konteks untuk validasi nanti di Langkah 3. **JANGAN langsung tampilkan ke user atau anggap user sebagai identitas di file lama.**
- Kalau **tidak ada**: lanjut Langkah 2 tanpa konteks.

**DILARANG** menampilkan kalimat seperti:
- ❌ "Saya kenal Anda sebagai [Nama dari _ROLE.md lama]. Lanjut?"
- ❌ "Sesi sebelumnya Anda login sebagai [Role lama]."

User mungkin bukan orang yang sama. Selalu tanya fresh dulu.

### 2. Tanya nama lengkap & role (WAJIB setiap sesi)

Gunakan tool `AskUserQuestion`:

**Pertanyaan 1**: "Siapa nama lengkap Anda?" (free text via "Other")

**Pertanyaan 2**: "Apa peran Anda di penugasan ini?"
Opsi:
- Anggota Tim (AT)
- Ketua Tim (KT)
- Pengendali Teknis (PT)
- Pengendali Mutu (PM)

**Pertanyaan 3 (BARU — untuk integrasi INTEGRAL)**: "Berapa NIP Anda (18 digit)?"
- Free text via "Other"
- Validasi: harus 18 digit angka, tanpa spasi/strip
- NIP wajib untuk integrasi auto-inject KKP ke INTEGRAL (Task 03)
- Kalau auditor tidak ingat saat ini, boleh skip → field `nip:` di _ROLE.md akan kosong, tapi Task 03 auto-inject akan gagal sampai NIP dilengkapi

### 3. (BARU v4.5) Cross-check dengan `_ROLE.md` lama (kalau ada)

Setelah Pertanyaan 1, 2, 3 dijawab, bandingkan dengan `_ROLE.md` lama yang dibaca di Langkah 1.

**4 skenario yang mungkin:**

| Skenario | Sikap Claude |
|---|---|
| **Match penuh** (nama+role+NIP sama dengan _ROLE.md lama) | Sampaikan: *"Identitas Anda cocok dengan sesi sebelumnya. Lanjut."* Update `session_start` ke timestamp sekarang. |
| **Nama berbeda** (orang berbeda) | Tampilkan: *"Sesi sebelumnya dilakukan oleh [Nama Lama] ([Role Lama]). Anda input [Nama Baru]. Apakah benar Anda mengambil alih penugasan ini, atau ada salah ketik?"* Tunggu konfirmasi. Kalau konfirmasi → tulis `_ROLE.md` baru + log `ROLE_TAKEOVER` ke audit trail. |
| **Nama sama, role berbeda** (mis. dari AT jadi KT, atau Sarah switch role) | Tampilkan: *"Sesi sebelumnya role Anda [Role Lama]. Sekarang Anda input [Role Baru]. Konfirmasi perubahan role?"* Wajar untuk KT yang dulu juga jadi AT di penugasan sama, tapi tetap perlu konfirmasi. Log `ROLE_CHANGED`. |
| **NIP berbeda dari nama** (potensi salah input) | Tampilkan WARNING: *"NIP yang Anda input ([NIP]) terdaftar untuk [Nama lain di Whitelist Inspektorat II], bukan [Nama Anda]. Mohon koreksi salah satu."* (Jika punya whitelist email→NIP→nama mapping; kalau belum, skip warning ini.) |

### 5. Validasi terhadap PKP

Jika `00-input/PKP-*.docx` atau `00-input/PKP-*.pdf` sudah ada (Task 01 sudah pernah jalan):
- Ekstrak daftar tim dari PKP (Pengendali Mutu, Pengendali Teknis, Ketua Tim, Anggota Tim 1..N).
- Cocokkan nama yang diinput user dengan daftar tim. Jika **tidak cocok**, tampilkan warning dan minta konfirmasi: *"Nama '[X]' tidak ditemukan di PKP. Lanjut sebagai guest atau perbaiki?"*
- Jika cocok, ambil role dari PKP (override input user) dan beri info: *"Sesuai PKP, role Anda adalah [Y]."*

### 6. Tulis `_ROLE.md` (overwrite kalau ada) + Append ke `_ROLE-history.jsonl`

Format `_ROLE.md` (single source of truth role AKTIF saat ini):

```markdown
---
nama_lengkap: Sarah Aulia
role: Anggota Tim
role_kode: AT
nip: 198501012010011001
role_validated_against_pkp: true
session_start: 2026-05-02T14:30:00+07:00
session_takeover_from: null   # diisi kalau take over dari user lain (v4.5)
---

# Sesi Aktif — Sarah Aulia (Anggota Tim)

Penugasan: 2026-05-001-reviu-pengadaan-bakti
Sasaran yang diassign ke Anda (dari PKP, akan diisi Task 01):
- (belum dijalankan Task 01)
```

**Format `_ROLE-history.jsonl` (BARU v4.5, append-only audit trail multi-role):**

Setiap kali Task 00 selesai dengan identitas valid, append 1 baris JSON ke `_ROLE-history.jsonl`:

```json
{"timestamp": "2026-05-02T14:30:00+07:00", "nama_lengkap": "Sarah Aulia", "role": "Anggota Tim", "role_kode": "AT", "nip": "198501012010011001", "action": "ROLE_LOGIN", "previous_role_kode": null}
{"timestamp": "2026-05-05T09:15:00+07:00", "nama_lengkap": "Budi Hartono", "role": "Ketua Tim", "role_kode": "KT", "nip": "197812121999031002", "action": "ROLE_TAKEOVER", "previous_role_kode": "AT", "previous_user": "Sarah Aulia"}
```

File ini **append-only** (tidak boleh dihapus/diedit) sebagai audit trail siapa yang pernah login di penugasan ini. Berguna kalau ada pertanyaan: *"Siapa yang membuat KKP/LHP pada tanggal X?"*

### 7. Log ke audit trail

Panggil `scripts/audit_trail.py log-event` dengan:
- `action`: `ROLE_LOGIN` (login pertama) atau `ROLE_TAKEOVER` (ganti user) atau `ROLE_CHANGED` (sama user beda role)
- `actor`: `{nama, role, nip}`
- `target`: `_ROLE.md`
- `payload`: `{validated_against_pkp: bool, source: "input"|"pkp_match", previous_role_kode: "AT"|null, previous_user: "Nama Lama"|null}`

### 8. Konfirmasi ke user

Tampilkan ringkasan:
> "Selamat datang, **Sarah Aulia** (Anggota Tim). Anda terdaftar di penugasan **2026-05-001-reviu-pengadaan-bakti**. Saya akan melanjutkan ke Task 01 (Inisiasi) untuk membaca ST + KP + PKP. LANJUT / KOREKSI?"

---

## Aturan Penolakan (deny rules)

Saat task lain dipanggil:

```python
# pseudocode di tiap task:
role = read_role_md()
if not role:
    raise "Jalankan Task 00 dulu — _ROLE.md belum ada."

allowed_tasks = ROLE_PERMISSIONS[role.role_kode]  # AT: [00,01,03], KT/PT/PM: [00,04]
if current_task not in allowed_tasks:
    raise f"Role '{role.role}' tidak boleh menjalankan {current_task}. Minta {required_role} untuk login."
```

---

## Output

- `penugasan/[nama]/_ROLE.md` — sumber kebenaran role sesi ini
- 1 entry ke `_AUDIT-TRAIL/events.jsonl` (action=ROLE_LOGIN)

## Konfirmasi auditor

Setelah Task 00 selesai, tanya:
> "Apakah Anda ingin saya lanjut ke **Task 01 (Inisiasi)** sekarang? LANJUT / TUNGGU"
