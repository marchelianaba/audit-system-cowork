# Rekomendasi Perbaikan IGRS

**Summary**: Rekomendasi perbaikan yang dirumuskan [[inspektorat-ii]] berdasarkan [[penelaahan-igrs]], dikelompokkan dalam tiga cakrawala waktu.

**Sources**: Penelaahan_IGRS.docx

**Last updated**: 2026-04-17

---

## A. Tindakan Segera (Jangka Pendek)

| # | Tindakan | Deskripsi |
|---|---|---|
| 1 | **Audit Keamanan Darurat** | Audit keamanan menyeluruh terhadap sistem IGRS, khususnya mekanisme API dan manajemen akses file submission; dokumentasikan semua patch yang telah dilakukan. |
| 2 | **Notifikasi Insiden Data** | Segera laksanakan kewajiban notifikasi kepada seluruh developer yang datanya bocor sesuai Pasal 46 UU PDP (batas 14 hari kerja); laporkan insiden kepada Lembaga PDP. |
| 3 | **Moratorium Status RC Otomatis** | Tunda pemberlakuan efek hukum dari status RC yang diperoleh melalui mekanisme otomatis hingga proses verifikasi manual selesai. |
| 4 | **Klarifikasi Data Publik** | Samakan data database internal igrs.id dengan tampilan publik; tidak boleh ada perbedaan antara data internal dan yang ditampilkan kepada publik. |

(source: Penelaahan_IGRS.docx)

---

## B. Perbaikan Sistemik (Jangka Menengah)

| 1 | **Penguatan Mekanisme Verifikasi** | Bangun alur kerja verifikasi manual oleh penguji yang ditetapkan Menteri sesuai Permenkominfo 2/2024, dengan SLA terukur per kategori game. |
| 2 | **Penerapan Standar Keamanan Informasi** | Implementasikan kontrol ISO/IEC 27001, minimal pada domain akses, operasional, komunikasi, dan manajemen insiden. Ganti mekanisme Google Drive ad hoc dengan sistem submission terenkripsi terpusat. |
| 3 | **Revisi Perjanjian Kemitraan** | Perbarui PKS dengan Steam dan Roblox untuk memuat klausul jelas mengenai tanggung jawab atas akurasi rating, kerahasiaan materi, dan sanksi atas pelanggaran. |
| 4 | **Penyelarasan Standar IARC** | Percepat penyelarasan metodologi klasifikasi dengan standar IARC, PEGI, dan ESRB untuk meningkatkan kredibilitas IGRS di mata developer global. |


---

## C. Penguatan Kelembagaan (Jangka Panjang)

| 1 | **Penambahan Kapasitas Tim** | Tingkatkan jumlah dan kualifikasi SDM tim IGRS secara signifikan — tim saat ini tidak proporsional dengan volume submission global. |
| 2 | **Evaluasi Regulasi** | Evaluasi [[regulasi-permenkominfo-2-2024|Permenkominfo 2/2024]] untuk mengakomodasi kategori antara di bawah RC (seperti adult-only tanpa RC), agar konten dewasa yang legal tidak otomatis dikategorikan tidak layak distribusi. |
| 3 | **Pembangunan Mekanisme Transparansi** | Kembangkan portal publik yang memungkinkan developer mengecek status aplikasi rating secara real-time, dengan alur keberatan yang jelas dan terukur. |


---

## Related pages

- [[isu-igrs]]
- [[sasaran-audit-igrs]]
- [[regulasi-igrs]]
- [[regulasi-uu-pdp]] — UU 27/2022 (basis hukum Tindakan Segera #2 notifikasi insiden data)
- [[regulasi-permenkominfo-2-2024]] — Permenkominfo 2/2024 (target Tindakan Jangka Menengah #2)
- [[regulasi-pp-tunas]] — PP 17/2025 (induk regulasi IGRS)
