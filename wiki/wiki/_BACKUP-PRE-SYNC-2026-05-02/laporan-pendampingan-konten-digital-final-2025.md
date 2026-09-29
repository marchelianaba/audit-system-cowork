# Laporan Final Pendampingan Tata Kelola Pengawasan dan Pengendalian Konten Digital

**Summary**: Laporan **final** Inspektorat II atas pendampingan Tata Kelola Pengawasan dan Pengendalian Konten Digital Ditjen Wasdig — gabungan dari [[notisi-tata-kelola-konten-negatif-2025]] (B-231) + [[laporan-tata-kelola-konten-negatif-final-2025]] (B-264) + tindak lanjut **8 temuan LHP Kinerja BPK**. Substansi tata kelola identik (efektivitas TKPPSE 22,44%, aset BMN Rp1,59T idle, 5 rekomendasi). Tambahan: **rencana aksi konkret per temuan BPK** dengan progres dari Wasdig (rapat penyedia 10 Sep, kajian selesai 25 Okt, KAK Pemeliharaan, MICT sedang dirancang). Dirilis dengan ST yang sama (127/IJ.3, 1 Juli 2025).

**Sources**: 309 IJ.3 PW.04.06 surat keluar 30.09.2025 ND Penyampaian Laporan Hasil Pendampingan Tata Kelola Pengawasan dan Pengendalian Konten Digital Direktorat Jenderal Pengawasan Ruang Digital.pdf

**Last updated**: 2026-04-22

---

## Identitas Dokumen

| Field | Nilai |
|---|---|
| Nomor surat | B-309/IJ.3/PW.04.06/09/2025 |
| Tanggal | 30 September 2025 |
| Klasifikasi | Terbatas |
| Ditujukan kepada | Sekretaris Ditjen Pengawasan Ruang Digital |
| Surat Tugas | 127/IJ.3/KP.01.06/07/2025 tgl 1 Juli 2025 (**SAMA** dengan B-231 + B-264) |
| Penandatangan | Muhammad Arief, Inspektur II |

## Tujuan Pendampingan

1. Meningkatkan efektivitas, efisiensi, akuntabilitas tata kelola pengawasan + pengendalian konten digital.
2. **Memetakan risiko** proses pengawasan + pengendalian konten digital.
3. **Mendampingi proses penyelesaian tindak lanjut atas LHP Kinerja BPK**.

## Hubungan dengan Notisi 231 dan Laporan Final 264

| Dokumen | Tanggal | Status |
|---|---|---|
| [[notisi-tata-kelola-konten-negatif-2025]] (B-231) | 25 Juli 2025 | Notisi awal — deadline tanggapan 31 Juli |
| [[laporan-tata-kelola-konten-negatif-final-2025]] (B-264) | 29 Agustus 2025 | Laporan Final substansi tata kelola |
| **Pendampingan ini (B-309)** | **30 September 2025** | **Laporan Final + Tindak Lanjut LHP BPK** |

B-309 menggabungkan **Notisi 231/Laporan 264 + tindak lanjut konkret 8 temuan LHP Kinerja BPK** = dokumen comprehensive final.

## Substansi Tata Kelola (Sama dengan B-231/B-264)

Lihat [[notisi-tata-kelola-konten-negatif-2025]] dan [[laporan-tata-kelola-konten-negatif-final-2025]] untuk detail. Ringkasan:

- **TKPPSE tidak efektif**: kekurangan 17 NAP + 1.183 ISP + 40,6 TB kapasitas; lisensi kedaluwarsa; **efektivitas pemblokiran 22,44%**.
- **TKPPSE tidak efisien**: tumpang tindih CNS vs CSE-Rugos + TKPPSE vs RTBH/TrustNG/RPZ; 89 ISP redundant; risiko inefisiensi OM.
- **5 rekomendasi**: pemetaan ulang, relokasi, fokus NAP, **tunda pengadaan baru + upgrade lisensi**.
- **5 residu/risiko**: aset BMN Rp1,59T idle, dismantle, takedown lambat, CSE peremajaan, DoH/VPN bypass.

## 8 Temuan LHP Kinerja BPK + Rencana Aksi Wasdig

| No | Judul Temuan | Rekomendasi BPK | Renaksi Wasdig |
|---|---|---|---|
| 1 | Penetapan Daftar Hitam Konten Perjudian/Pornografi Belum Didukung Infrastruktur CSE Memadai | Susun dan terapkan **arsitektur bisnis pencegahan** + perangkat lunak terintegrasi dengan prosedur normalisasi | **MICT sedang dirancang**; progress di SIMWAS menunggu keputusan BPK |
| 2 | Pendistribusian/Penerapan/Normalisasi Daftar Hitam URL/Domain/IP Belum Optimal | Tetapkan kewajiban ISP sinkronisasi daftar hitam dari database Kemkomdigi | Dokumen revisi masih dalam proses reviu Tim HK Setditjen |
| 3 | Kemkomdigi Belum Melaksanakan Pengendalian atas ISP secara Memadai | Terapkan sistem pemantauan terpadu + berbasis risiko pantau kepatuhan ISP | Output: Laporan pemantauan terpadu dari **dashboard** |
| 4 | Pendistribusian/Penerapan/Normalisasi (lanjutan) | Susun & terapkan Analisis Log + perangkat lunak terintegrasi + evaluasi periodik perencanaan/pemanfaatan/pemeliharaan TKPPSE | **TKPPSE: 10 Sep rapat penyedia, kajian selesai 25 Okt, KAK Pemeliharaan dibuat sesuai KAK Kajian**; **Tim Infra: Analisis log via dashboard RTBH TrustNG** |
| 5 | Belum Ada Ketentuan/SOP Koordinasi Pencegahan Penyebarluasan Konten Dilarang | Susun peraturan ISP wajib sinkronisasi TrustPositif + RPZ pada DNS + redirecting DNS Publik (Google/Cloudflare/OpenDNS) | Dokumen revisi dalam reviu Tim HK Setditjen; **redirecting DNS perlu negosiasi BPK** karena tidak mungkin push Google → diusulkan pakai TKPPSE |
| 6 | Regulasi Pelaksanaan Pencegahan/Pemantauan Belum Lengkap | Susun + tetapkan regulasi spesifik pencegahan konten ilegal + standar deteksi dini real-time | **Perlu mapping satgas Judol**; output: regulasi spesifik konten ilegal; **Itjen: telaah dari PM 5 + KM437** untuk diusulkan TL tahun ini |
| 7 | Regulasi Belum Lengkap (lanjutan) | Inisiasi mekanisme koordinasi + eskalasi lintas instansi + standar minimum sistem pencegahan/pemantauan | Masukan poin 2 perlu ditanyakan ke BPK |
| 8 | Pemblokiran Daftar Hitam Belum Didukung Infrastruktur RPZ/RTBH Memadai | Evaluasi kinerja RPZ + RTBH + tindaklanjuti dengan penyusunan ulang distribusi/penempatan TKPPSE (update 7 Juli: evaluasi penempatan KOS TKPPSE belum berdasar evaluasi kinerja RPZ/RTBH) | **Buat dokumen kajian/peta layering arsitektur pemblokiran**; hasil kajian TKPPSE dilampirkan; Tim TKPPSE + Infra koordinasi membahas kajian |

## Insight Rencana Aksi

- **MICT (Master Index Content Trustee?)** muncul sebagai sistem baru yang sedang dirancang.
- **KAK Pemeliharaan TKPPSE** akan dibuat **sesuai hasil Kajian TKPPSE** yang selesai 25 Okt 2025 — **menunggu kajian sebelum eksekusi pengadaan baru** (konsisten rekomendasi B-264).
- **Negosiasi dengan BPK** untuk redirecting DNS Public — **tidak feasible push Google** → diusulkan alternatif TKPPSE.
- **Telaah PM 5/2021 + KM 437** sebagai dasar regulasi konten ilegal.
- **Layering arsitektur pemblokiran** menjadi tema kunci — gabungan RPZ + RTBH + TrustNG + TKPPSE harus dipetakan jelas.

## Konteks

Dokumen ini menutup **siklus 3 bulan pendampingan tata kelola TKPPSE** yang dimulai dari Surat Tugas 1 Juli 2025:
- **Juli**: Notisi 231 (kritik awal).
- **Agustus**: Laporan Final 264.
- **September**: **Laporan Pendampingan 309** dengan tindak lanjut + rencana aksi konkret.

Terdapat **harapan progress nyata**:
- Kajian Pemetaan TKPPSE selesai **25 Oktober 2025**.
- KAK Pemeliharaan TKPPSE TA 2026 sesuai kajian.
- Redesain TKPPSE direncanakan TA 2027 ([[lhp-pengadaan-redesain-tkppse-2026]]).

Dengan deadline 25 Oktober, **siklus rapor kinerja Itjen II di TA 2025 menutup babak TKPPSE Mei-Sep dengan kajian sebagai output kunci** — selanjutnya keputusan strategis pemerintah pusat yang akan menentukan arah TKPPSE.

## Related pages

- [[notisi-tata-kelola-konten-negatif-2025]]
- [[laporan-tata-kelola-konten-negatif-final-2025]]
- [[tkppse]]
- [[atensi-pemutusan-tkppse-2025]]
- [[lha-om-tkppse-2024]]
- [[lhp-pengadaan-redesain-tkppse-2026]]
- [[lhr-pemblokiran-rtbh-trustng-2025]]
- [[chr-rka-kl-wasdig-2026]]
- [[inspektorat-ii]]
