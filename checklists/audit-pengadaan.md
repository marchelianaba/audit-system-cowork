# Checklist Dokumen — Audit Pengadaan Barang/Jasa

**Skill:** audit-pengadaan
**Lingkup:** Seluruh siklus pengadaan — dari perencanaan hingga serah terima dan pembayaran.
**Audit pengadaan menuntut dokumen sumber yang lengkap untuk pengujian bukti yang memadai.**

---

## Dokumen WAJIB (harus ada sebelum audit dimulai)

| No | Dokumen | Folder | Keterangan |
|----|---------|--------|------------|
| W1 | Surat Tugas (ST) | `00-surat-tugas/` | Dasar penugasan, menentukan lingkup audit |
| W2 | Kontrak / SPK (ditandatangani) | `02-kontrak/` | Dokumen utama pengujian: nilai, jangka waktu, spesifikasi |
| W3 | KAK / TOR / Spesifikasi Teknis | `03-perencanaan/` | Dasar pengujian kesesuaian output |
| W4 | HPS | `03-perencanaan/` | Pengujian kewajaran harga kontrak |
| W5 | BAST / Berita Acara Serah Terima | `04-pelaksanaan/` | Pengujian output vs kontrak |

---

## Dokumen PENTING (audit terbatas jika tidak ada)

| No | Dokumen | Folder | Dampak jika tidak ada |
|----|---------|--------|-----------------------|
| P1 | Data dukung pembentuk harga (survei harga pasar / e-katalog / harga referensi / penawaran sebelumnya) | `03-perencanaan/` | Kewajaran metodologi HPS tidak dapat diverifikasi |
| P2 | Addendum kontrak (jika ada) | `02-kontrak/` | Perubahan nilai/lingkup tidak dapat diverifikasi |
| P3 | BAHP / BA Evaluasi pemenang | `02-kontrak/` | Proses pemilihan penyedia tidak dapat diaudit |
| P4 | Laporan progres / kemajuan pekerjaan | `04-pelaksanaan/` | Monitoring pelaksanaan tidak dapat dinilai |
| P5 | SPM / SP2D / bukti pembayaran | `05-keuangan/` | Kewajaran pembayaran tidak dapat diverifikasi |
| P6 | Foto/dokumentasi pelaksanaan | `04-pelaksanaan/` | Verifikasi fisik pekerjaan tidak dapat dilakukan |
| P7 | SPPBJ | `02-kontrak/` | Legalitas penetapan pemenang tidak dapat dikonfirmasi |

---

## Dokumen OPSIONAL (memperkuat pengujian)

| No | Dokumen | Folder | Manfaat |
|----|---------|--------|---------|
| O1 | SOP / Peraturan Internal | `01-peraturan-internal/` | Kriteria tambahan (juklak internal PA/KPA) |
| O2 | DPA / DIPA / RKA | `03-perencanaan/` | Verifikasi kesesuaian pagu dan sumber dana |
| O3 | Dokumen kualifikasi penyedia | `02-kontrak/` | Pengujian legalitas penyedia |
| O4 | Laporan pengawas lapangan | `04-pelaksanaan/` | Konfirmasi kondisi fisik dari pihak independen |
| O5 | Kwitansi / faktur penyedia | `05-keuangan/` | Verifikasi rincian pembayaran |
| O6 | ND Permintaan (jika ada) | `00-surat-tugas/` | Konteks isu yang melatarbelakangi penugasan |

---

## Aturan Validasi

```
KRITIS (harus ada, audit TIDAK DAPAT dilanjutkan):
  → W1 (Surat Tugas)
  → W2 (Kontrak/SPK)

PERINGATAN — area audit TIDAK DAPAT dinilai:
  → W3 tidak ada → perencanaan dan kewajaran spesifikasi tidak dapat diaudit
  → W4 tidak ada → kewajaran harga kontrak tidak dapat diaudit
  → W5 tidak ada → output vs kontrak tidak dapat diverifikasi → catat sebagai keterbatasan MATERIAL
  → P5 tidak ada → pembayaran tidak dapat diverifikasi → catat sebagai keterbatasan MATERIAL

PERINGATAN — area terbatas:
  → P1 tidak ada → kewajaran metodologi HPS tidak dapat diverifikasi
  → P2 tidak ada → hanya kontrak awal yang dapat diaudit
  → P3 tidak ada → proses pemilihan tidak dapat diaudit
  → P3 tidak ada → monitoring pelaksanaan tidak dapat dinilai

INFORMASI (catat, lanjutkan):
  → O1–O6 tidak ada → audit tetap berjalan dengan kriteria Perpres
```

---

## Pesan Notifikasi untuk Auditor

Jika dokumen kritis tidak ada:
> ❌ **Audit tidak dapat dimulai.** Dokumen wajib berikut tidak ditemukan: [daftar]. Mohon upload dokumen tersebut ke folder yang sesuai, kemudian ketik **ULANG** untuk memeriksa ulang.

Jika ada dokumen penting yang tidak ada:
> ⚠️ **Audit dapat dilanjutkan dengan keterbatasan material.** Dokumen berikut tidak ditemukan: [daftar]. Area audit yang terkait tidak dapat dinilai dan akan dicatat sebagai keterbatasan signifikan dalam laporan. Ketik **LANJUT** untuk melanjutkan atau upload dokumen tambahan terlebih dahulu.

Jika semua dokumen wajib tersedia:
> ✅ **Dokumen inti tersedia.** Audit dapat dimulai. Ketik **LANJUT** untuk memulai analisis.
