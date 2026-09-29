# Security Advisories — Sistem Audit v2

Berisi temuan keamanan sistem dan mitigasi yang direkomendasikan.

---

## SEC-01 — GitHub Personal Access Token dalam plaintext di root OneDrive

**Status:** 🔴 TERBUKA — perlu tindakan auditor
**Ditemukan:** 2026-04-19 (audit sistem v2.8)
**File:** `Audit otomatis berbasis claude (1)/github token.txt`

### Risiko

File berisi classic GitHub Personal Access Token (prefix `ghp_`, panjang 40 karakter) tersimpan sebagai plaintext di root folder OneDrive yang disinkronkan antar-device. Implikasi:

1. **Exfiltrasi otomatis**: setiap aplikasi di device yang dapat membaca folder OneDrive dapat membaca token (termasuk malware, Claude Cowork session, ekstensi browser dengan akses filesystem).
2. **Backup tidak terenkripsi**: OneDrive menyimpan versi historis — token tetap ada meski dihapus.
3. **Visibilitas multi-device**: jika OneDrive di-share untuk kolaborasi tim, semua anggota dapat membaca.
4. **Tidak ada scope control visible**: tidak jelas scope token (repo, gist, admin:org). Jika scope luas, breach dampaknya signifikan.

### Rekomendasi Mitigasi (urutan prioritas)

1. **Revoke token sekarang** di https://github.com/settings/tokens dan catat kapan terakhir dipakai.
2. **Regenerate dengan scope minimum** yang benar-benar dibutuhkan (biasanya `repo:read` sudah cukup untuk push/pull private repo audit-system).
3. **Simpan di credential manager OS**:
   - Windows: Credential Manager (control panel) atau `cmdkey /add:github.com /user:<username> /pass:<token>`
   - Gunakan Git Credential Manager (`git config --global credential.helper manager-core`)
4. **Jangan commit ke repo** — tambahkan `github token.txt` dan pola `*token*.txt` ke `.gitignore` di audit-system-v2.
5. **Token expiry**: set expiry pendek (30–90 hari) dan rotasi terjadwal.

### Dokumentasi Terkait
- Kebijakan pengelolaan kredensial Kemkomdigi (jika ada) — rujuk SE terbaru Biro Umum/ICT.
- GitHub best practices: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure

---

## SEC-02 — Folder penugasan berisi dokumen sensitif di OneDrive

**Status:** 🟡 PERHATIAN — kebijakan
**Ditemukan:** 2026-04-19

### Risiko
Folder `penugasan/` memuat dokumen audit (ST, KKP, bukti dukung) yang berisi:
- Nama pegawai + NIP (data pribadi)
- Nilai kontrak, rincian anggaran (keuangan negara)
- Hasil penilaian SPIP/SAKIP satker (klasifikasi internal)

Sinkronisasi OneDrive publik bisa jadi tidak sesuai dengan klasifikasi dokumen pemerintahan.

### Rekomendasi
1. Konfirmasi klasifikasi OneDrive yang dipakai (Personal vs M365 Tenant Kemkomdigi). Untuk dokumen dinas, wajib tenant kementerian dengan kontrol akses.
2. Gunakan Information Protection label (Microsoft Purview) untuk tag "Rahasia/Terbatas" — mencegah forward accidental.
3. Pertimbangkan folder archive lokal ter-enkripsi (VeraCrypt / BitLocker) untuk penugasan yang sudah closing.

---

## SEC-03 — Prinsip Proteksi Sistem (sudah diterapkan — untuk dokumentasi)

**Status:** ✅ TERIMPLEMENTASI
Sejak v2.x, Claude dilarang memodifikasi `tasks/`, `skills/`, `checklists/`, `README.md` saat penugasan berjalan (tertulis eksplisit di Task 01). Ini mencegah drift sistem saat eksekusi.

**Audit aturan ini berlaku juga untuk `scripts/`, `pattern-library/`, dan `SECURITY.md`** — file inti sistem hanya diubah saat mode pemeliharaan (di luar penugasan aktif).
