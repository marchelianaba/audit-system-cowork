# REMINDER — Informasi yang Belum Bisa Diisi di Wiki

**Dibuat**: 2026-04-24
**Fungsi**: Daftar celah informasi di `llm-wiki/` yang tidak dapat diisi hanya dari dokumen sumber yang sudah diingest. Masing-masing butuh input dari auditor (unggah dokumen ke `raw/`, atau beri informasi verbal/email).

---

## Prioritas 1 — Perlu Segera

### 1. Profil utuh kedua Ditjen mitra

**Yang ada**: hanya `peta-risiko-wasdig-2026.md` dan `peta-risiko-ekosistem-digital-2026.md` (daftar risiko).

**Yang belum ada**:
- Struktur organisasi eselon II/III masing-masing Ditjen.
- Pagu DIPA TA 2026 per Ditjen dan breakdown ke eselon II.
- IKU (Indikator Kinerja Utama) dan IKSP.
- Renstra 2025–2029 (bila sudah terbit di nomenklatur Komdigi).
- Daftar PIC per eselon II (nama, email, HP).

**Bagaimana mengisi**:
- Upload: Renstra Ditjen Wasdig, Renstra Ditjen Ekosistem Digital, SK Menkomdigi tentang SOTK, DIPA TA 2026 per satker.
- Beri Claude daftar kontak PIC (email internal, tidak akan disimpan ke memory jika tergolong sensitif).

### 2. Tim auditor Inspektorat II

**Yang ada**: `TIM/DAFTAR-TIM.md` di folder induk — baru placeholder `[Nama KT1]`, `[Nama AT1]`, dll.

**Yang belum ada**:
- Nama anggota tim sesungguhnya (PJP, Dalnis, KT1, KT2, AT1–AT4).
- Sertifikasi dan spesialisasi masing-masing.
- Beban kerja / penugasan aktif per orang.
- Struktur wewenang (who signs what).

**Bagaimana mengisi**:
- Edit langsung `TIM/DAFTAR-TIM.md` dengan nama asli, atau sampaikan ke Claude untuk diisi ke wiki.
- Buat halaman `wiki/tim-inspektorat-ii.md` setelah informasi terverifikasi.

### 3. PKPT TA 2026 lengkap

**Yang ada**: hanya PKPT B04 (6 kegiatan PKPT + 2 Reviu RKA-K/L) di `realisasi-anggaran-inspektorat-ii-2026.md`.

**Yang belum ada**:
- PKPT lengkap TA 2026 (Q1–Q4): jenis penugasan, obrik, periode, PIC.
- Kalender audit: deadline ST, KKP, LHP, TLHP.

**Bagaimana mengisi**:
- Upload dokumen PKPT TA 2026 Itjen Kemkomdigi ke `raw/`.

---

## Prioritas 2 — Penting untuk Cross-Reference

### 4. TLHP BPK & BPKP historis

**Yang ada**: di `peta-risiko-wasdig-2026.md` hanya disebut "TLHP BPK TKPPSE" sebagai risiko MEDIUM.

**Yang belum ada**:
- Daftar temuan BPK TA 2023, 2024, 2025 untuk Kemkomdigi/Kominfo yang masih terbuka.
- Daftar temuan BPKP (Audit Tujuan Tertentu, Reviu Pagu Indikatif, dll.).
- Status per temuan: selesai / dalam proses / belum ditindaklanjuti.

**Bagaimana mengisi**:
- Upload LHP BPK terbaru yang menyentuh Kemkomdigi + matriks TLHP yang biasa dikelola Bagian Hukum/Itjen.
- Claude bisa buat halaman `wiki/tlhp-bpk-historis.md` dan `wiki/tlhp-bpkp-historis.md`.

### 5. Stakeholder eksternal (halaman profil)

**Yang ada**: disebut-sebut tapi tidak ada halaman.

**Yang belum ada**: profil ringkas untuk
- BPK — pemeriksa eksternal.
- BPKP — auditor internal pemerintah (Audit BPKP sedang ditunggu untuk kasus TKPPSE).
- Dewan Pers — terkait kasus @magdaleneid.
- Lembaga PDP — penerima notifikasi kebocoran.
- Kejaksaan Agung — untuk TLHP yang memerlukan tindak lanjut hukum.
- LPP TVRI — penerima alih status DBS.

**Bagaimana mengisi**:
- Tidak perlu dokumen baru — cukup minta Claude buat halaman singkat: peran, alur koordinasi, kontak utama.

### 6. Template dokumen standar

**Yang ada**: template sudah ada di `audit-system-v4/templates/` — tapi belum ada halaman wiki yang menunjuk ke template tersebut.

**Yang belum ada**:
- Halaman `wiki/template-dokumen-standar.md` yang memuat: jenis → template path → penjelasan singkat.

**Bagaimana mengisi**:
- Claude bisa langsung mapping dari direktori `audit-system-v4/templates/` (tidak perlu dokumen baru).

---

## Prioritas 3 — Nilai Tambah Jangka Panjang

### 7. Struktur organisasi Kemkomdigi (bagan)

**Yang belum ada**:
- Bagan menteri → sekretariat + 5–6 Ditjen.
- Relasi Itjen dengan unit-unit di atasnya.

**Bagaimana mengisi**:
- Upload SK Menkomdigi SOTK atau ambil dari web resmi.

### 8. Unit-unit Ditjen Wasdig yang belum teridentifikasi

**Yang ada sebagai istilah**: TKPPSE, CSE, CNS, PSE, PSrE, PANDI, Direktorat Penyidikan.

**Yang belum ada**:
- Halaman sendiri untuk masing-masing direktorat (kecuali [[pdsi]]).
- Definisi yang rigorous untuk **CSE vs CNS** — peta risiko Wasdig mencatat "tumpang tindih CSE dan CNS" sebagai risiko HIGH, tapi definisi CNS belum jelas di wiki.

**Bagaimana mengisi**:
- Upload dokumen referensi tata kelola Wasdig.
- Wawancara internal dengan PIC di Wasdig.

### 9. Unit-unit Ditjen Ekosistem Digital yang belum teridentifikasi

**Yang ada sebagai istilah**: Direktorat Pengembangan Ekosistem Digital (sudah ada halaman), IGRS (sudah ada), Garuda Spark, Bantuan IoT, PSO POS, DBS.

**Yang belum ada**:
- Halaman sendiri untuk Garuda Spark, Bantuan IoT, PSO POS (dashboard menandai mereka sebagai Risiko HIGH tapi detail belum tersedia).

### 10. Kamus istilah yang masih *placeholder*

Di `glossary.md` beberapa akronim masih ditandai *(perlu verifikasi)*:
- **CNS** — Content Negative System (?)
- **SUFI** — definisi lengkap klausul confidentiality Lintasarta.
- **NWS** — muncul di pola, belum pasti kepanjangan.

### 11. Vendor lain yang dicatat LHP tapi belum ada halaman

- PT CSE (sebagai vendor server crawling) — berbeda dari sistem CSE di Wasdig.
- Vendor Root CA PSrE Induk Rp2,9 M (LHR Aptika).
- Vendor Colocation Rp2,2 M (LHR Aptika).
- Vendor ISP Rp1 M (LHR Aptika).

---

## Prioritas 4 — Nice to Have

*Seluruh item Prioritas 4 sudah diselesaikan pada 2026-04-24. Lihat seksi "✅ Selesai Diisi" di bagian bawah.*

---

## Cara Menindaklanjuti

1. **Tinjau berkala**: buka file ini setiap awal bulan, cek item mana yang masih terbuka.
2. **Upload dokumen**: taruh di `llm-wiki/raw/` → minta Claude *ingest* (Claude akan otomatis buat halaman wiki + update index + update log).
3. **Input verbal**: cukup katakan ke Claude "catat bahwa X adalah Y" dan arahkan ke halaman mana yang relevan.
4. **Hapus item yang sudah selesai**: kalau satu item sudah terpenuhi, move entry-nya ke bagian "✅ Selesai Diisi" di bawah ini (atau hapus).

---

## ✅ Selesai Diisi

### 2026-04-24 — Prioritas 4 (semua 3 item)

- **Item 12 — Loop llm-wiki ↔ audit-system-v4**: diisi dengan [[sop-ingest-lhp-ke-wiki]]; SOP 5 langkah manual + konvensi penamaan file baku.
- **Item 13 — Pemisahan PROJECT-STATUS vs dashboard**: diisi dengan [[sop-pemisahan-dashboard]]; matriks jenis informasi dan aturan cross-reference.
- **Item 14 — Halaman framework evaluasi (SAKIP/SPIP/RB/MR)**: diisi dengan 4 halaman framework:
  - [[framework-evaluasi-sakip]] — PermenPAN-RB 88/2021; 4 komponen × 3 dimensi × skala AA–E.
  - [[framework-evaluasi-spip]] — Peraturan BPKP 5/2021; alur 9 gate bertahap.
  - [[framework-evaluasi-rb]] — PermenPAN-RB 9/2023 + KepmenPAN-RB 182/2024 + SE 6/2025; Ex-Ante + TW I–IV.
  - [[framework-evaluasi-mr]] — Pedoman Menkomdigi 6/2017 + ISO 31000:2018; format catatan KKSA.
