# Instruksi Push ke GitHub

Repo tujuan: https://github.com/irfansihab/audit_cowork.git

Status saat file ini dibuat: repo **Public** — ubah ke **Private** dulu sebelum push karena folder `penugasan/` berisi dokumen audit Kemkomdigi yang tidak boleh terbuka.

---

## Ringkasan langkah

1. Ubah visibility repo ke **Private** di GitHub
2. Pause OneDrive sync sementara (biar `.git` tidak di-lock)
3. Bersihkan folder `.git` yang rusak dari percobaan sebelumnya
4. Jalankan `git init` + commit + push dari PowerShell
5. Resume OneDrive sync

---

## Langkah 1 — Ubah repo ke Private

1. Buka https://github.com/irfansihab/audit_cowork/settings
2. Scroll ke bagian **Danger Zone** paling bawah
3. Klik **Change repository visibility** → **Make private**
4. Ketik nama repo untuk konfirmasi

---

## Langkah 2 — Pause OneDrive

- Klik ikon OneDrive di system tray (pojok kanan bawah)
- Settings → **Pause syncing** → 2 jam

Alternatif permanen: Settings → **Sync and backup** → **Manage backup** → pastikan folder ini tidak ikut di-backup, atau pindahkan project ke luar OneDrive.

---

## Langkah 3 — Bersihkan .git yang rusak

Buka PowerShell (bukan admin), lalu:

```powershell
cd "C:\Users\irfan\OneDrive\Audit otomatis berbasis claude (1)\audit-system-v2"

# Hapus .git yang rusak
Remove-Item -Recurse -Force .git -ErrorAction SilentlyContinue
```

Kalau gagal karena file masih di-lock, tutup dulu semua editor/IDE yang mengakses folder ini, tunggu 30 detik, lalu coba lagi.

---

## Langkah 4 — git init + commit + push

Masih di PowerShell:

```powershell
cd "C:\Users\irfan\OneDrive\Audit otomatis berbasis claude (1)\audit-system-v2"

# Init repo
git init -b main
git config user.email "inspektorat2.kominfo.2@gmail.com"
git config user.name "Inspektorat II Kemkomdigi"

# Verifikasi .gitignore sudah ada
Test-Path .gitignore     # harus True

# Stage semua
git add .

# Cek apa yang akan di-commit (ideally TIDAK ada file token, ~$*, desktop.ini)
git status | Select-String -Pattern "token|~\$|desktop.ini"

# Commit
git commit -m "Initial commit: Sistem Audit v2.8 (Kemkomdigi Inspektorat II)"

# Tambah remote
git remote add origin https://github.com/irfansihab/audit_cowork.git

# Push (akan minta username + PAT sebagai password)
git push -u origin main
```

Saat diminta password: **jangan masukkan password akun GitHub** — pakai Personal Access Token.
Token ada di `C:\Users\irfan\OneDrive\Audit otomatis berbasis claude (1)\github token.txt`.

Setelah push selesai, segera:

1. **Rotate token** di https://github.com/settings/tokens — hapus yang lama, buat baru dengan scope `repo` saja, simpan di password manager (bukan di file plaintext di OneDrive).
2. **Hapus** `github token.txt` dari OneDrive (SEC-01).

---

## Langkah 5 — Resume OneDrive

- Klik ikon OneDrive → **Resume syncing**

---

## Kalau push lambat

Repo ini berisi folder `penugasan/` sebesar 1,4 GB. Push awal akan lama (tergantung koneksi). Kalau ingin push ringan dulu lalu data belakangan, sebelum `git add .` jalankan:

```powershell
# Sementara exclude folder besar
"penugasan/
uji coba/" | Add-Content .gitignore
```

Lalu nanti kalau mau include datanya, edit `.gitignore`, commit perubahan, dan push lagi.

---

## Validasi setelah push

```powershell
# Cek bahwa token tidak ter-commit
git log --all --full-history --diff-filter=A -- "**/github token.txt"
# Output harus kosong
```

Kalau ternyata token ter-commit (harusnya tidak karena .gitignore sudah melindungi), segera rotate token dan gunakan `git filter-repo` untuk menghapus dari history.
