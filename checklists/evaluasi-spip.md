# Checklist Dokumen — Evaluasi SPIP (Penjaminan Kualitas Maturitas SPIP)

**Skill:** evaluasi-spip
**Lingkup:** Penjaminan Kualitas (PK) oleh APIP atas Penilaian Mandiri (PM) maturitas SPIP terintegrasi
**Dasar Hukum:** Peraturan BPKP Nomor 5 Tahun 2021
**Catatan:** Evaluasi SPIP tidak menggunakan KKP tabel biasa — output utama adalah Lembar Kerja Evaluasi (Excel) dengan kolom Nilai PK terisi. Folder dokumen per unsur/subunsur menggantikan struktur folder penugasan standar.

---

## Dokumen WAJIB (harus ada sebelum evaluasi dimulai)

| No | Dokumen | Folder/Sumber | Keterangan |
|----|---------|--------------|------------|
| W1 | Surat Tugas (ST) | `00-surat-tugas/` | Dasar penugasan dan cakupan unit/unsur yang dievaluasi |
| W2 | Lembar Kerja Evaluasi (LKE) Excel — kolom Nilai PM sudah terisi | `03-perencanaan/` atau via chat | **Dokumen inti** — berisi parameter, bobot, dan Nilai PM dari asesor manajemen |
| W3 | Folder dokumen pendukung per unsur/subunsur | `04-pelaksanaan/` atau subfolder khusus | SOP, SK, laporan, notulen, data kinerja — bukti atas klaim Nilai PM |

---

## Struktur Folder Dokumen Pendukung

Dokumen pendukung idealnya diorganisir per unsur SPIP:

| Unsur SPIP | Contoh Dokumen yang Relevan |
|------------|----------------------------|
| Unsur 1 — Lingkungan Pengendalian | SK Tim, Kode Etik, Pakta Integritas, laporan kepegawaian |
| Unsur 2 — Penilaian Risiko | Register Risiko, kebijakan MR, laporan monitoring risiko |
| Unsur 3 — Kegiatan Pengendalian | SOP, prosedur operasional, laporan pelaksanaan SOP |
| Unsur 4 — Informasi dan Komunikasi | Kebijakan informasi, sistem informasi, laporan keterbukaan |
| Unsur 5 — Pemantauan Pengendalian | Laporan pemantauan SPIP, TLHP, laporan tindak lanjut |
| Kepemimpinan (jika termasuk) | SK/Disposisi pimpinan, notulen rapat pimpinan |

> Jika dokumen tidak diorganisir per unsur, Claude akan membaca semua dokumen yang tersedia dan mengkaitkan ke unsur yang relevan secara mandiri.

---

## Dokumen PENTING (evaluasi terbatas per unsur jika tidak ada)

| No | Dokumen | Dampak jika tidak ada |
|----|---------|----------------------|
| P1 | Laporan hasil PM (narasi dari asesor, bukan hanya nilai) | Konteks dan argumentasi PM tidak dapat dipahami — PK hanya berdasarkan dokumen |
| P2 | Hasil penilaian BPKP tahun sebelumnya (jika ada) | Perbandingan tren tidak dapat dilakukan |
| P3 | Laporan Area of Improvement (AoI) BPKP tahun lalu | Tindak lanjut perbaikan tidak dapat diverifikasi |
| P4 | Dokumen tindak lanjut atas rekomendasi tahun lalu | Unsur Pemantauan tidak dapat dinilai dengan lengkap |

---

## Dokumen OPSIONAL

| No | Dokumen | Manfaat |
|----|---------|---------|
| O1 | Screenshot/demo sistem informasi manajemen risiko | Verifikasi infrastruktur pengendalian |
| O2 | Laporan audit keuangan BPK terakhir | Korelasi pengendalian dengan temuan audit keuangan |
| O3 | TLHP (Tindak Lanjut Hasil Pemeriksaan) BPK | Indikator kualitas pengendalian internal |
| O4 | Dokumen kasus integritas/korupsi (jika ada) | Menentukan apakah penalti penurunan gradasi berlaku |

---

## Aturan Validasi

```
KRITIS (evaluasi TIDAK DAPAT dilanjutkan):
  → W1 (Surat Tugas)
  → W2 (LKE Excel dengan Nilai PM) — tanpa ini tidak ada objek yang dinilai

PERINGATAN — penilaian per unsur tidak dapat dilakukan:
  → W3 tidak ada sama sekali → Claude tidak dapat memverifikasi klaim PM
    → Tampilkan: "Dokumen pendukung tidak tersedia. Nilai PK tidak dapat diisi
       secara mandiri. Mohon sediakan folder dokumen per unsur/subunsur."
  → W3 sebagian ada (hanya beberapa unsur) → catat unsur mana yang tidak ada
    dokumen pendukungnya; nilai PK untuk unsur tersebut tidak dapat diverifikasi

PERINGATAN — konteks terbatas:
  → P1 tidak ada → Claude menilai murni dari dokumen, tanpa mempertimbangkan
    narasi asesor (ini dapat diterima — PK memang harus mandiri)
  → P4 tidak ada → komponen tindak lanjut/pemantauan tidak dapat dikonfirmasi

INFORMASI:
  → O1–O4 tidak ada → evaluasi tetap berjalan dengan dokumen yang tersedia
```

---

## Pesan Notifikasi untuk Auditor

Jika W2 (LKE) tidak ada:
> ❌ **Evaluasi tidak dapat dimulai.** Lembar Kerja Evaluasi (LKE) Excel dengan Nilai PM dari asesor tidak ditemukan. Mohon upload file LKE atau kirim via chat. Pastikan kolom **Nilai PM** sudah terisi sebelum upload.

Jika W3 (folder dokumen) tidak ada:
> ❌ **Dokumen pendukung tidak tersedia.** Tanpa dokumen pendukung (SOP, SK, laporan per unsur), Claude tidak dapat mengisi kolom Nilai PK secara mandiri. Mohon sediakan folder berisi dokumen pendukung per unsur SPIP, kemudian ketik **ULANG**.

Jika dokumen pendukung sebagian ada:
> ⚠️ **Dokumen pendukung tidak lengkap untuk semua unsur.** Unsur berikut tidak memiliki dokumen pendukung: [daftar unsur]. Nilai PK untuk unsur tersebut tidak dapat diverifikasi dan akan diberi catatan "Dokumen tidak tersedia — verifikasi tidak dapat dilakukan". Ketik **LANJUT** untuk melanjutkan, atau upload dokumen tambahan terlebih dahulu.

Jika dokumen lengkap:
> ✅ **Dokumen siap.** LKE dengan Nilai PM tersedia dan folder dokumen pendukung ditemukan. Ketik **LANJUT** untuk memulai penjaminan kualitas.
