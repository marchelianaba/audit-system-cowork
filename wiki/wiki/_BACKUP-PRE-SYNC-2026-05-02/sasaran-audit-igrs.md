# Sasaran Audit Kinerja IGRS

**Summary**: Lima area sasaran audit dan metode pengujiannya, hasil [[penelaahan-igrs]] oleh [[inspektorat-ii]].

**Sources**: Penelaahan_IGRS.docx

**Last updated**: 2026-04-17

---

## Peta Sasaran Audit (Ringkasan)

| Isu | Sasaran Audit | Metode Utama | Regulasi/Standar |
|---|---|---|---|
| Inkonsistensi Klasifikasi | Rating sesuai konten? | Uji sampel, tracing proses | Permenkominfo 2/2024 Ps. 9–13; UU 1/2024; PP TUNAS 17/2025 |
| Status RC & Transparansi | RC diterapkan secara sah? | Inspeksi database, tracing | Permenkominfo 2/2024; UU 28/1999; UU 25/2009 |
| Kebocoran Data | Data developer terlindungi? | Reviu arsitektur, log, gap analysis ISO 27001 | UU PDP 27/2022; PP PSTE 71/2019; ISO/IEC 27001 |
| Kesiapan Sistem | Layak go-live? | Reviu dokumen, wawancara | Permenkominfo 2/2024; prinsip kehati-hatian |
| Tata Kelola Kemitraan | PKS dengan platform jelas? | Reviu kontrak, analisis klausul | Permenkominfo 2/2024; hukum perjanjian |

(source: Penelaahan_IGRS.docx)

---

## Area 1 — Kesiapan Sistem Sebelum Go-Live

**Sasaran**: Memastikan IGRS telah memenuhi syarat kesiapan teknis, SDM, dan prosedur sebelum dioperasikan.

**Pengujian:**
- Reviu dokumen perencanaan: Feasibility Study, Rencana Implementasi, hasil UAT, go/no-go criteria.
- Wawancara tim teknis: apakah ada pilot terbatas sebelum integrasi global, siapa yang memberi otorisasi go-live.
- Benchmarking kapasitas SDM: bandingkan jumlah reviewer vs. volume submission (≥1.000 game terdata).

**Kriteria**: Permenkominfo 2/2024 (kewajiban uji kesesuaian); prinsip kehati-hatian tata kelola proyek pemerintah.

(source: Penelaahan_IGRS.docx)

---

## Area 2 — Akurasi Proses Klasifikasi

**Sasaran**: Memastikan rating yang diberikan sesuai kriteria konten Permenkominfo 2/2024, bukan sekadar self-declare.

**Pengujian:**
- Uji sampel 30–50 game: bandingkan konten aktual dengan kriteria Pasal 9–13 Permenkominfo 2/2024. Prioritaskan sampel dari dua ujung ekstrem: game rated 3+ dengan konten berat, dan game rated RC/18+ dengan konten ringan.
- Tracing proses per sampel: apakah ada bukti uji kesesuaian oleh penguji yang ditunjuk Menteri.
- Analisis konsistensi lintas platform: bandingkan rating di Steam, Google Play, dan database internal igrs.id.

**Kriteria**: Permenkominfo 2/2024 Pasal 9–13; kewajiban uji kesesuaian oleh penguji yang ditetapkan Menteri.

(source: Penelaahan_IGRS.docx)

---

## Area 3 — Mekanisme Pengenaan Status RC

**Sasaran**: Memastikan status RC hanya diberikan berdasarkan proses verifikasi yang sah dan transparan.

**Pengujian:**
- Inspeksi database internal: minta daftar lengkap game RC, bandingkan dengan tampilan publik igrs.id. Apakah ada game RC yang sengaja disembunyikan?
- Tracing per game: pilih 10–15 game RC, telusuri kapan dan berdasarkan dokumen apa status RC ditetapkan, apakah ada notifikasi ke publisher.
- Verifikasi prosedur keberatan: pastikan mekanisme keberatan 7 hari kalender (Permenkominfo 2/2024) terdokumentasi dan dapat dioperasikan.

**Kriteria**: Permenkominfo 2/2024 (mekanisme keberatan); UU 28/1999 (asas transparansi); UU 25/2009 (pelayanan publik).

(source: Penelaahan_IGRS.docx)

---

## Area 4 — Keamanan Sistem Informasi ⚠️ Paling Mendesak

**Sasaran**: Memastikan sistem IGRS memiliki kontrol keamanan memadai untuk melindungi data developer dan materi pra-rilis.

**Pengujian:**
- Reviu arsitektur keamanan API: dokumentasi teknis, verifikasi autentikasi/otorisasi setiap endpoint, patch atas API yang dieksploitasi.
- Pengujian manajemen akses: verifikasi RBAC pada materi submission, prosedur Google Drive kepada tim reviewer.
- Reviu log akses: server/access log periode sebelum dan saat kebocoran; verifikasi mekanisme alerting anomali.
- Pengujian pemberitahuan insiden: kapan tim IGRS mengetahui kebocoran? Apakah sudah ada notifikasi ke subjek data dan Lembaga PDP dalam 14 hari (Pasal 46 UU PDP)?
- Gap analysis ISO/IEC 27001: domain A.9 (Access Control), A.12 (Operations Security), A.13 (Communications Security), A.16 (Incident Management).

**Kriteria**: UU PDP 27/2022 (Pasal 35 dan 46); PP PSTE 71/2019 Pasal 12; ISO/IEC 27001.

(source: Penelaahan_IGRS.docx)

---

## Area 5 — Tata Kelola Kemitraan Platform

**Sasaran**: Memastikan integrasi IGRS dengan Steam dan Roblox didasari perjanjian yang mengatur hak, kewajiban, dan tanggung jawab secara jelas.

**Pengujian:**
- Reviu dokumen PKS/MoU dengan Valve dan Roblox: klausul tanggung jawab atas akurasi rating, SLA verifikasi, kerahasiaan materi submission.
- Analisis pembagian tanggung jawab: apakah PKS menetapkan siapa bertanggung jawab saat mismatch rating?
- Verifikasi kewenangan hukum integrasi: apakah integrasi ke platform global sudah melalui kajian hukum dan persetujuan pejabat berwenang?

**Kriteria**: Permenkominfo 2/2024 (kewajiban pencantuman hasil klasifikasi resmi); prinsip akuntabilitas; ketentuan PKS.

(source: Penelaahan_IGRS.docx)

---

## Related pages

- [[isu-igrs]]
- [[rekomendasi-igrs]]
- [[regulasi-igrs]]
- [[penelaahan-igrs]]
- [[kartu-penugasan-survei-pendahuluan-igrs]]
- [[audit-kinerja-layanan-klasifikasi-gim]]
