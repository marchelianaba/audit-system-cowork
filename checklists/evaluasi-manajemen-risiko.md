# Checklist Dokumen — Evaluasi Manajemen Risiko

**Skill:** evaluasi-manajemen-risiko
**Lingkup:** Efektivitas implementasi manajemen risiko — dari kebijakan, proses identifikasi, hingga monitoring dan pengendalian risiko
**Dasar Hukum:** ISO 31000:2018, PP 60/2008 (SPIP), Pedoman Menkominfo 6/2017
**Catatan:** Laporan evaluasi MR berbeda dari jenis lain: Seksi F berisi catatan naratif bernomor (bukan tabel CCSAA), Seksi G Rekomendasi terpisah dari catatan kondisi.

---

## Dokumen WAJIB (harus ada sebelum evaluasi dimulai)

| No | Dokumen | Folder/Sumber | Keterangan |
|----|---------|--------------|------------|
| W1 | Surat Tugas (ST) | `00-surat-tugas/` | Dasar penugasan dan cakupan unit yang dievaluasi |
| W2 | Pedoman/Kebijakan Manajemen Risiko internal | `01-peraturan-internal/` | Kerangka dasar MR instansi — SK, Peraturan Menteri, atau Juklak internal |
| W3 | Register Risiko (daftar risiko per unit kerja) | `04-pelaksanaan/` | Objek utama evaluasi — berisi risiko teridentifikasi, skor, dan perlakuan |

---

## Dokumen PENTING (aspek tertentu tidak dapat dievaluasi jika tidak ada)

| No | Dokumen | Folder | Dampak jika tidak ada |
|----|---------|--------|-----------------------|
| P1 | Laporan monitoring dan evaluasi risiko (triwulanan/tahunan) | `04-pelaksanaan/` | Siklus pemantauan risiko tidak dapat dinilai |
| P2 | SK penetapan Risk Owner / Risk Officer / Risk Champion | `01-peraturan-internal/` | Struktur tanggung jawab MR tidak dapat dikonfirmasi |
| P3 | Matriks risiko / Risk Heat Map | `04-pelaksanaan/` | Kualitas analisis dan evaluasi risiko tidak dapat diverifikasi |
| P4 | Laporan perlakuan risiko (risk treatment plan + realisasi) | `04-pelaksanaan/` | Tahap perlakuan dan pengendalian tidak dapat dievaluasi |
| P5 | Dokumen Area of Improvement dari penilaian SPIP BPKP (jika ada) | via chat atau `04-pelaksanaan/` | Konteks area lemah yang perlu menjadi fokus evaluasi |

---

## Dokumen OPSIONAL (memperkaya analisis)

| No | Dokumen | Manfaat |
|----|---------|---------|
| O1 | Struktur organisasi dan SK Tim/Komite Manajemen Risiko | Verifikasi Three Lines Model — apakah struktur sudah sesuai |
| O2 | Screenshot/demo sistem informasi manajemen risiko | Kematangan infrastruktur teknologi MR |
| O3 | Notulen rapat/forum manajemen risiko | Bukti budaya dan intensitas pembahasan risiko |
| O4 | Laporan hasil evaluasi MR tahun sebelumnya | Perbandingan perkembangan dan tindak lanjut rekomendasi |
| O5 | Dokumen risk appetite/risk tolerance yang ditetapkan | Keberadaan panduan batas penerimaan risiko |

---

## Aturan Validasi

```
KRITIS (evaluasi TIDAK DAPAT dilanjutkan):
  → W1 (Surat Tugas)
  → W3 (Register Risiko) — tanpa ini tidak ada objek evaluasi

PERINGATAN — aspek siklus MR tidak dapat dinilai:
  → W2 tidak ada → kerangka kebijakan MR tidak dapat dievaluasi
    → Catatan: "Pedoman MR tidak ditemukan — aspek kelembagaan tidak dapat dinilai"
  → P1 tidak ada → monitoring dan pengendalian tidak dapat dievaluasi
    → Catatan: "Laporan monitoring risiko tidak tersedia"
  → P2 tidak ada → struktur tanggung jawab (Three Lines) tidak dapat dikonfirmasi
  → P3 tidak ada → kualitas analisis risiko (matriks) tidak dapat diverifikasi
  → P4 tidak ada → tahap perlakuan risiko tidak dapat dievaluasi

INFORMASI (catat, lanjutkan):
  → O1–O5 tidak ada → evaluasi tetap berjalan dengan dokumen yang tersedia
```

---

## Pesan Notifikasi untuk Auditor

Jika W3 (Register Risiko) tidak ada:
> ❌ **Evaluasi tidak dapat dimulai.** Register Risiko tidak ditemukan. Dokumen ini adalah objek utama evaluasi manajemen risiko — berisi daftar risiko, skor, dan rencana perlakuan. Mohon upload Register Risiko (format Excel/PDF), kemudian ketik **ULANG**.

Jika W2 (Pedoman MR) tidak ada:
> ⚠️ **Kebijakan Manajemen Risiko tidak tersedia.** Aspek kelembagaan dan kerangka kebijakan MR tidak dapat dievaluasi. Evaluasi akan difokuskan pada aspek operasional (register risiko dan monitoring). Ketik **LANJUT** untuk melanjutkan dengan keterbatasan, atau upload Pedoman MR terlebih dahulu.

Jika laporan monitoring (P1) tidak ada:
> ⚠️ **Laporan monitoring risiko tidak ditemukan.** Aspek pemantauan dan pengendalian tidak dapat dinilai. Evaluasi akan difokuskan pada kualitas identifikasi dan analisis risiko berdasarkan register yang tersedia. Ketik **LANJUT** atau upload laporan monitoring.

Jika dokumen lengkap:
> ✅ **Dokumen siap.** Register Risiko, Pedoman MR, dan laporan monitoring tersedia. Ketik **LANJUT** untuk memulai evaluasi manajemen risiko.
