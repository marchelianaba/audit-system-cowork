# Mind Map Audit Kinerja IGRS

**Summary**: Peta audit kinerja IGRS yang disusun Inspektorat II dengan struktur **4 Aspek × N Risiko × Fokus Sasaran × Kondisi × Rekomendasi × Simpulan**. Berfungsi sebagai matriks kerja audit kinerja yang sedang berjalan ([[audit-kinerja-layanan-klasifikasi-gim]]). Per April 2026, sebagian besar risiko sudah memiliki rekomendasi yang **Terjawab** atau **Terjawab Sebagian** — sebagian dari [[laporan-igrs-2026]] yang diterbitkan oleh Direktur Pengembangan Ekosistem Digital. **2 risiko Belum Terjawab**: (a) keseimbangan rasio personil tim penguji vs jumlah game, dan (b) selarasnya output IGRS dengan keberhasilan program di atasnya.

**Sources**: `raw/Mind Map Audit Kinerja IGRS.xlsx - Sasaran.pdf` — ekspor sheet "Sasaran" dari spreadsheet kerja audit

**Last updated**: 2026-04-26

---

## Struktur Matriks

Mind map memetakan tiap aspek audit ke kolom-kolom kerja yang konsisten:

| Kolom | Keterangan |
|---|---|
| **Aspek** | Klasifikasi luas: Kebijakan, Sistem Informasi, SDM, Kinerja |
| **Isu** | Pernyataan masalah tingkat tinggi |
| **Sasaran** | Apa yang ingin dipastikan auditor |
| **Risiko** | Risiko spesifik dalam aspek |
| **Fokus Sasaran** | Penjelasan operasional sasaran |
| **Kondisi** | Temuan auditor di lapangan (saat ini) |
| **Rekomendasi** | Tindakan untuk menutup gap |
| **Simpulan** | Status: Terjawab / Terjawab sebagian / Belum terjawab |

## Aspek 1: Kebijakan

**Isu:** Terdapat kelemahan kebijakan dalam implementasi klasifikasi game.
**Sasaran:** Memastikan kecukupan kebijakan dalam implementasi layanan klasifikasi game.

### Risiko 1.1 — Pelaksanaan Tidak Sesuai Tugas dan Fungsi

| Aspek | Konten |
|---|---|
| Fokus Sasaran | Memastikan kesesuaian implementasi dengan tugas dan fungsi organisasi |
| Kondisi | (1) Posisi IGRS belum jelas — instrumen informasi atau pengawas? (2) Tidak ada tugas/fungsi Dit. PED yang selaras dengan pelaksanaan pengawasan klasifikasi game |
| Rekomendasi | (1) Revisi PM 2/2024 untuk mempertegas posisi IGRS sebagai sistem informasi bukan alat blokir; (2) belum dijelaskan pada laporan |
| Simpulan | **Terjawab sebagian** |

### Risiko 1.2 — Belum Tersedianya Kebijakan Operasional & Pengawasan

| Aspek | Konten |
|---|---|
| Fokus Sasaran | Memastikan aktivitas operasional didukung dengan prosedur pelaksanaan |
| Kondisi | (1) Belum ada UU khusus dengan kekuatan penegakan lebih kuat dari sanksi administratif; (2) belum ada mekanisme pola pengawasan acuan kementerian; (3) badan klasifikasi semi-independen dengan representasi industri/akademisi/konsumen perlu dibentuk; (4) sistem klasifikasi 7 tingkat tersedia, tapi tidak ada panduan intensitas konten granular; (5) tren digital baru (gacha, NFT, reward harian) belum diakomodir |
| Rekomendasi | (1) Revisi regulasi jangka menengah; (2) belum dijelaskan mekanisme pengawasan; (3) pembentukan badan klasifikasi semi-independen — belum dipastikan kapan; (4) revisi PM 2/2024, redesain taksonomi konten; (5) revisi PM 2/2024, pembaruan konten tren baru |
| Simpulan | **Terjawab** |

## Aspek 2: Sistem Informasi

**Isu:** Terdapat kelemahan dalam sistem informasi pendukung layanan klasifikasi game.
**Sasaran:** Memastikan kecukupan sistem informasi pendukung pada layanan klasifikasi game.

### Risiko 2.1 — Belum Tersedianya Kerjasama dengan Platform Distribusi

| Aspek | Konten |
|---|---|
| Fokus Sasaran | Memastikan kecukupan rincian kerjasama antar pihak |
| Kondisi | Belum ada standar mekanisme teknis untuk integrasi dengan platform |
| Rekomendasi | Susun mekanisme teknis yang memastikan hanya rating dari proses resmi IGRS yang dapat ditampilkan dengan label IGRS + pengembangan API aman antara igrs.id dengan storefront, disertai sistem kriptografis untuk verifikasi keaslian sertifikat rating |
| Simpulan | Terjawab → **Belum terjawab** *(perlu eksekusi)* |

### Risiko 2.2 — Proses Bisnis Belum Termuat dalam Sistem

| Aspek | Konten |
|---|---|
| Fokus Sasaran | Memastikan seluruh proses bisnis telah termuat dalam sistem |
| Kondisi | Tidak ada kanal resmi rating-spesifik untuk game. Pengaduan melalui kanal umum Komdigi |
| Rekomendasi | Akan dibangun kanal pengaduan bersamaan dengan operasional IGRS, sementara menggunakan kanal aduan komdigi |
| Simpulan | **Terjawab** |

### Risiko 2.3 — Hasil Pengujian Tidak Disampaikan Transparan

| Aspek | Konten |
|---|---|
| Fokus Sasaran | Memastikan sistem telah menampilkan hasil pengujian secara transparan |
| Kondisi | Tidak dijelaskan pada laporan |
| Rekomendasi | Publikasi rating rationale untuk setiap judul + mekanisme sanggah 30 hari (target Maret 2027) |
| Simpulan | **Terjawab** |

### Risiko 2.4 — Sistem Belum Memiliki Standar Keamanan & Mutu

| Aspek | Konten |
|---|---|
| Fokus Sasaran | Memastikan Sistem Informasi telah terstandar |
| Kondisi | (1) Sistem belum memiliki sertifikasi standar keamanan; (2) terdapat 2 celah pada sistem: GDrive yang diunggah tidak diproteksi + data terekspose di HTML yang dapat dilihat melalui developer tools browser |
| Rekomendasi | (1) Audit keamanan independen (target Juni 2026); (2) Perbaikan keamanan sistem |
| Simpulan | **Terjawab** |

## Aspek 3: SDM

**Isu:** Terdapat kelemahan Sumber Daya Manusia dalam implementasi layanan klasifikasi game.
**Sasaran:** Memastikan kecukupan Sumber Daya Manusia dalam implementasi layanan klasifikasi game.

### Risiko 3.1 — Tim Penguji Tidak Didukung SDM Kompeten

| Aspek | Konten |
|---|---|
| Fokus Sasaran | Memastikan kompetensi tim penguji telah sesuai dengan ketentuan |
| Kondisi | Belum ada standar kompetensi formal yang mengatur kualifikasi minimum verifikator IGRS |
| Rekomendasi | Akan disusun kebijakan formal standar kompetensi verifikator + skema sertifikasi |
| Simpulan | **Terjawab** |

### Risiko 3.2 — Rasio Tim Penguji vs Jumlah Game

| Aspek | Konten |
|---|---|
| Fokus Sasaran | Memastikan kecukupan jumlah personil tim penguji |
| Kondisi | Belum tersedia |
| Rekomendasi | Belum tersedia |
| Simpulan | **❌ Belum terjawab** |

## Aspek 4: Kinerja

**Isu:** Terdapat ketidakefektifan kinerja implementasi layanan klasifikasi game.
**Sasaran:** Menilai keefektifan kinerja layanan klasifikasi game.

### Risiko 4.1 — Output Tidak Selaras dengan Keberhasilan Program di Atasnya

| Aspek | Konten |
|---|---|
| Fokus Sasaran | Memastikan output kegiatan telah mendukung sasaran program di atasnya |
| Kondisi | Belum tersedia |
| Rekomendasi | Belum tersedia |
| Simpulan | **❌ Belum terjawab** |

### Risiko 4.2 — Akurasi Hasil Uji Kesesuaian Rendah vs Target

| Aspek | Konten |
|---|---|
| Fokus Sasaran | Memastikan kepatuhan hasil tim penguji dengan target yang ditetapkan |
| Kondisi | Belum ada KPI yang ditetapkan sebagai kinerja tim penguji kesesuaian rating game |
| Rekomendasi | Telah ditetapkan pada roadmap target mismatch-rate 15% (September 2026) + melibatkan AI untuk meningkatkan akurasi dan efisiensi |
| Simpulan | **Terjawab** |

## Rekapitulasi Status Audit

| Status | Jumlah Risiko | Risiko |
|---|---:|---|
| ✅ **Terjawab** | 6 | 1.2 (Kebijakan), 2.2-2.4 (SI), 3.1 (SDM), 4.2 (Kinerja) |
| 🟡 **Terjawab sebagian** | 1 | 1.1 (Tusi org) |
| ⏳ **Terjawab → perlu eksekusi** | 1 | 2.1 (Kerjasama platform) |
| ❌ **Belum terjawab** | 2 | 3.2 (Rasio penguji), 4.1 (Selarasnya output) |
| **Total** | **10** | |

**Score:** 6 dari 10 risiko fully terjawab, 1 sebagian, 1 perlu eksekusi, 2 masih belum terjawab.

## 2 Risiko Belum Terjawab — Aksi Audit yang Dibutuhkan

### Risiko 3.2 — Rasio Personil Tim Penguji

**Apa yang dibutuhkan:**
- Data jumlah verifikator/penguji aktual saat ini
- Data jumlah game yang masuk antrean rating per bulan
- Benchmark dari sistem rating lain (ESRB ~50 staff, PEGI ~20 staff inti, dll dari [[laporan-igrs-2026]] Bab 3)

**Output yang diharapkan:** rekomendasi penambahan personil dengan justifikasi terukur.

### Risiko 4.1 — Output Selarasnya dengan Program di Atasnya

**Apa yang dibutuhkan:**
- Mapping IKU program "Pengembangan dan Penguatan Ekosistem dan Ruang Digital" DJED
- Identifikasi apakah IGRS punya kontribusi terukur ke IKU tersebut
- KPI IGRS turunan dari IKU program

**Output yang diharapkan:** logical chain Sasaran Strategis → Program → IGRS dengan indikator yang traceable.

## Hubungan dengan Laporan IGRS

[[laporan-igrs-2026]] yang disusun oleh Direktur Pengembangan Ekosistem Digital adalah **bukti tindak lanjut substantif** dari mayoritas rekomendasi di mind map ini. Pemetaan:

| Aspek/Risiko | Section di Laporan IGRS yang Menjawab |
|---|---|
| 1.1 Posisi IGRS | Rekomendasi Strategis #1 (Reposisi sebagai instrumen informasi) |
| 1.2 Kebijakan & taksonomi | Rekomendasi Strategis #2 (Redesain taksonomi) + Bab 8 |
| 2.1 Kerjasama platform | Roadmap Fase 2 (integrasi storefront) |
| 2.3 Transparansi | Roadmap Fase 2 (publikasi rationale + sanggah 30 hari) |
| 2.4 Standar keamanan | Roadmap Fase 0 (audit keamanan independen) + Rekomendasi #5 |
| 3.1 Kompetensi penguji | Bab 9 (Standar Kompetensi Verifikator) + Roadmap Fase 1 |
| 4.2 Akurasi rating | Roadmap Fase 1 (mismatch rate <15%) |

**Yang TIDAK dijawab Laporan IGRS** = Risiko 3.2 (rasio personil) dan 4.1 (selarasnya output) — ini gap yang harus dikejar Inspektorat II di fase fieldwork audit kinerja.

## Implikasi untuk Card Trello "IGRS"

Card IGRS (Ekosdig — Tinggi) di [[pemantauan-isu-risiko-trello]] memantau "Tata Kelola dan Kinerja". Mind Map ini memberi struktur konkret untuk update progress card:

```
Tata Kelola IGRS:
- Aspek Kebijakan: 🟡 Terjawab sebagian (perlu klarifikasi tusi Dit PED)
- Aspek Sistem Informasi: ✅ Mostly terjawab (kecuali eksekusi 2.1)
- Aspek SDM: 🟡 1/2 terjawab (kompetensi: ya, rasio: belum)
- Aspek Kinerja: 🟡 1/2 terjawab (akurasi: ya, output selarasnya: belum)
```

## Related Pages

- [[laporan-igrs-2026]] — laporan komprehensif yang menjawab mayoritas risiko di mind map ini
- [[audit-kinerja-layanan-klasifikasi-gim]] — audit aktif yang menggunakan mind map ini sebagai matriks kerja
- [[sasaran-audit-igrs]] — turunan dari mind map ini ke sasaran konkret
- [[isu-igrs]], [[regulasi-igrs]], [[rekomendasi-igrs]] — IGRS issue cluster
- [[regulasi-permenkominfo-2-2024]] — regulasi yang dievaluasi
- [[regulasi-uu-pdp]] — relevant untuk Aspek SI Risiko 2.4
- [[direktorat-pengembangan-ekosistem-digital]] — auditan
- [[pemantauan-isu-risiko-trello]] — card IGRS (Tinggi)
- [[dashboard]]
- [[inspektorat-ii]]
