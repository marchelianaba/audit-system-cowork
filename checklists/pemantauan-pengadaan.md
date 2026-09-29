# Checklist Dokumen — Pemantauan Pelaksanaan Pengadaan

**Skill:** pemantauan-pengadaan
**Lingkup:** Pelaksanaan kontrak yang sedang berjalan — progres fisik, keuangan, kepatuhan penyedia, isu aktif.
**Pemantauan bersifat real-time; dokumen harus merepresentasikan kondisi TERKINI.**

---

## Dokumen WAJIB (harus ada sebelum pemantauan dimulai)

| No | Dokumen | Folder | Keterangan |
|----|---------|--------|------------|
| W1 | Surat Tugas (ST) | `00-surat-tugas/` | Dasar penugasan dan periode pemantauan |
| W2 | Kontrak (ditandatangani) + addendum jika ada | `02-kontrak/` | Data nilai kontrak, jadwal, klausul utama |
| W3 | Laporan progres terbaru (penyedia / pengawas) | `04-pelaksanaan/` | Data kondisi terkini pelaksanaan pekerjaan |

---

## Dokumen PENTING (pemantauan terbatas jika tidak ada)

| No | Dokumen | Folder | Dampak jika tidak ada |
|----|---------|--------|-----------------------|
| P1 | BA Kemajuan Pekerjaan (terakhir) | `04-pelaksanaan/` | Progres fisik tidak dapat dikonfirmasi |
| P2 | SPM / SP2D yang sudah terbit | `05-keuangan/` | Progres keuangan tidak dapat dihitung |
| P3 | Jadwal pelaksanaan (time schedule / kurva S) | `04-pelaksanaan/` | Deviasi dari jadwal tidak dapat diukur |
| P4 | Laporan/surat teguran PPK (jika ada) | `04-pelaksanaan/` | Riwayat masalah dan respons PPK tidak diketahui |

---

## Dokumen OPSIONAL (memperkaya analisis)

| No | Dokumen | Folder | Manfaat |
|----|---------|--------|---------|
| O1 | Foto/dokumentasi lapangan terbaru | `04-pelaksanaan/` | Konfirmasi visual progres fisik |
| O2 | Laporan pemantauan sebelumnya | `04-pelaksanaan/` | Perbandingan tren dan tindak lanjut |
| O3 | Surat-menyurat PPK–Penyedia | `04-pelaksanaan/` | Isu yang sudah dikomunikasikan |
| O4 | Daftar hadir tenaga ahli/personel | `04-pelaksanaan/` | Verifikasi ketersediaan SDM penyedia |

---

## Aturan Validasi

```
KRITIS (harus ada, pemantauan TIDAK DAPAT dilanjutkan):
  → W1 (Surat Tugas)
  → W2 (Kontrak)

PERINGATAN — data tidak dapat dihitung:
  → W3 tidak ada → kondisi aktual pelaksanaan tidak dapat dilaporkan
    → minta auditor konfirmasi data verbal atau tunda sampai laporan tersedia
  → P2 tidak ada → Dashboard progres keuangan tidak dapat diisi → catat "Data keuangan tidak tersedia"
  → P3 tidak ada → Deviasi jadwal tidak dapat diukur → catat "Jadwal referensi tidak tersedia"

INFORMASI (catat, lanjutkan):
  → O1–O4 tidak ada → pemantauan tetap berjalan dengan data yang tersedia
```

---

## Pesan Notifikasi untuk Auditor

Jika dokumen kritis tidak ada:
> ❌ **Pemantauan tidak dapat dimulai.** Dokumen wajib berikut tidak ditemukan: [daftar]. Mohon upload dokumen tersebut ke folder yang sesuai, kemudian ketik **ULANG** untuk memeriksa ulang.

Jika laporan progres tidak ada:
> ⚠️ **Laporan progres terbaru tidak ditemukan** di folder `04-pelaksanaan/`. Pemantauan tidak dapat menghasilkan data kondisi terkini tanpa dokumen ini. Apakah Anda ingin: (a) upload laporan progres terlebih dahulu, atau (b) lanjutkan dengan data kontrak saja dan tambahkan data progres secara manual?

Jika semua dokumen wajib tersedia:
> ✅ **Dokumen tersedia.** Pemantauan dapat dimulai. Ketik **LANJUT** untuk memulai analisis.
