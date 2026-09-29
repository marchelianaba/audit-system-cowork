# BPK LHP Kinerja PSTE — Pencegahan Konten Dilarang TA 2019 s.d. Sem I 2024

**Summary**: Laporan Hasil Pemeriksaan Kinerja BPK RI atas Kegiatan Pencegahan Penyebarluasan Konten yang Dilarang Peraturan Perundang-undangan dalam Rangka Penyelenggaraan Sistem Elektronik dan Transaksi Elektronik Tahun Anggaran 2019 sampai dengan Semester I 2024 pada Kementerian Komunikasi dan Informatika dan Instansi Terkait Lainnya. **Kesimpulan: Kinerja Kemenkominfo Kurang Efektif**. Nilai pengembangan sistem Rp1,82 triliun (CSE Rp30,57M + Dashboard Rp283jt + TKPPSE 2021 Rp963,15M + PKJT 2022 Rp827,86M). Dokumen ini adalah **sumber utama 34 rekomendasi BPK** yang dipantau Inspektorat II di [[pemantauan-tlhp-wasdig-november-2025]].

**Sources**: LHP Nomor **14/LHP/XVI/02/2025** tanggal **6 Februari 2025**, ditandatangani Penanggung Jawab Pemeriksaan Edward G. Hasiholan Simanjuntak (NIP 196807161989031002).

**Last updated**: 2026-04-24

---

## Identitas Laporan

| Field | Nilai |
|---|---|
| Nomor | 14/LHP/XVI/02/2025 |
| Tanggal | 6 Februari 2025 |
| Jenis | Pemeriksaan Kinerja (BPK AKN XVI) |
| Periode | TA 2019 s.d. Semester I 2024 |
| Entitas | Kementerian Komunikasi dan Informatika + instansi terkait |
| Lingkup | Kegiatan pencegahan penyebarluasan konten dilarang (judi online + pornografi) |
| Tujuan | Menilai efektivitas upaya Kemenkominfo |
| **Kesimpulan** | **Kurang Efektif** |

## Konteks

Ini adalah **audit raksasa BPK** yang menjadi payung seluruh rekomendasi pengawasan TKPPSE di wiki. Audit dimulai setelah kekhawatiran publik dan Kemenkopolhukam tentang **transaksi judi online Rp100 triliun di triwulan I 2024** dan **5,5 juta anak Indonesia korban pornografi** (sumber: detik.com).

Dari 34 rekomendasi BPK di audit ini, hanya 7 yang sudah sesuai per 28 November 2025 (27 masih Belum Sesuai — 17,07% TLHP eksternal Wasdig tahun berjalan). Lihat [[pemantauan-tlhp-wasdig-november-2025]].

## Dasar hukum audit

- UU 15/2004 (Pemeriksaan Pengelolaan dan Tanggung Jawab Keuangan Negara).
- UU 15/2006 (Badan Pemeriksa Keuangan).
- Peraturan BPK 1/2017 (Standar Pemeriksaan Keuangan Negara/SPKN).
- **UU 1/2024 (Perubahan Kedua UU ITE)** — Pasal 40 ayat (2) & (2a): pemerintah wajib melakukan pencegahan dan penyebarluasan Informasi Elektronik yang memuat muatan dilarang.

## Anggaran yang diperiksa

Total nilai pengembangan sistem selama 2019–2023: **Rp1.821.862.114.733** (≈ Rp1,82 triliun).

| Sistem | Periode | Nilai |
|---|---|---:|
| **CSE + Google API** (Custom Search Engine) | 2019–2023 | Rp30.572.090.140 |
| | 2019 | Rp2.221.560.000 |
| | 2020 | Rp3.785.802.867 |
| | 2021 | Rp7.990.000.000 |
| | 2022 | Rp9.737.727.273 |
| | 2023 | Rp6.837.000.000 |
| Aplikasi Dashboard UX (twitter + media online) | 2020 | Rp283.415.000 |
| **Pengadaan Sistem TKPPSE** | 2021 | **Rp963.149.000.000** |
| **Pemenuhan Perangkat Koneksi Jaringan Terdistribusi (PKJT)** | 2022 | **Rp827.857.609.593** |
| **Total** | | **Rp1.821.862.114.733** |

Angka OM TKPPSE 2024 (Rp78,56M; Rp21,22M dibayar + Rp57,34M disputed) tidak masuk dalam periode audit ini tapi menjadi isu paralel — lihat [[lha-verifikasi-tagihan-om-tkppse-2024-rp57m]].

## Angka efektivitas pemblokiran (uji BPK)

BPK menguji 25.321+ situs konten dilarang yang diduga terblokir. Hasilnya:

| Sistem | Tingkat Keberhasilan | Tingkat Kegagalan |
|---|---:|---:|
| **RPZ** (Response Policy Zone) | **79,60%** (15.559/19.547) | 20,40% (3.988) — 0% jika DoH tanpa redirecting |
| **RTBH** (Remotely Triggered Black Hole) | **81,45%** (7.315/8.981) | 18,55% (1.666) |
| **TKPPSE** | **22,44%** (5.844/(19.438+6.609)) | 77,56% |

Penyebab kegagalan TKPPSE:
1. Web browser modern (Chrome, Edge, Firefox) sudah punya teknologi **anti-TCP Reset** — beralih ke UDP yang tidak bisa TKPPSE blokir.
2. **VPN** — enkripsi lalu lintas + menyembunyikan IP membuat TKPPSE tidak berfungsi.
3. Uji petik laboratorium 24 Oktober 2024: pada laptop, **0 dari 40 akses berhasil diblokir TKPPSE murni** (tanpa bantuan RPZ/RTBH).

## Capaian Kemenkominfo (sisi positif yang diakui BPK)

1. Telah ada kegiatan sosialisasi oleh 3 unit: Ditjen IKP (judi, hoaks, SARA), Ditjen Aptika (kesusilaan, judi, hoaks), Biro Humas (judi, hoaks).
2. Strategi komunikasi pencegahan judi online Ditjen IKP: Awareness, Edukasi, Promosi Pencegahan, Advokasi.

## 13 Temuan Pemeriksaan (34 rekomendasi turunan)

### 1.1 Kelembagaan, Regulasi, dan Infrastruktur TI

**1.1.1 CSE belum memadai** — verifikator tidak seragam, machine learning/crawling belum mutakhir.

**1.1.2 TKPPSE belum memadai** — 17 NAP kurang + 1.183 ISP kurang + 40.620 GB kapasitas kurang; lisensi Oracle Linux 7 kedaluwarsa Des 2024; **efektivitas 22,44%**.

**1.1.3 RPZ dan RTBH belum memadai** — pemantauan pasif hanya berdasar laporan NAP/ISP; tidak evaluasi berkala; DoH dengan public DNS tanpa redirecting → RPZ 0%.

**1.1.4 Tanggung jawab antar satker belum ditetapkan jelas** — SOTK Kemkomdigi mengubah pembagian, tata hubungan direktorat pengawasan, penegakan hukum, pemeliharaan aset TI belum terintegrasi dalam arsitektur SPBE.

**1.1.5 Regulasi pelaksanaan belum lengkap dan mutakhir** — spesifikasi sistem deteksi dini, pemantauan real-time, mekanisme eskalasi lintas K/L.

### 1.2 Pemantauan dan Tindak Lanjut

**1.2.1 Pemantauan konten ilegal tidak memadai** — **3.839.549 hasil crawling belum ditindaklanjuti**; keyword management lemah; verifikator tidak independen; pemblokiran terlambat.

### 1.3 Distribusi dan Penerapan Daftar Hitam

**1.3.1 Pendistribusian, penerapan, normalisasi daftar hitam belum optimal** — jumlah daftar hitam di database TKPPSE tidak sesuai batch list.

**1.3.2 Pemutusan akses pada PSE Lingkup Privat UGC + PSE Lingkup Publik belum optimal** — kepatuhan platform belum dipantau periodic; MoU dengan platform belum ada.

### 1.4 Pengendalian atas ISP

**1.4.1 Pengendalian ISP belum memadai** — dari 1.188 ISP, baru 508 sinkron dengan TrustPositif; **370 ISP sudah BIND RPZ + blokir** vs **798 ISP belum**. Rekomendasi reward/sanction belum diterapkan.

### 1.5 Sosialisasi kepada Masyarakat

**1.5.1 Perencanaan dan penetapan sasaran sosialisasi belum optimal** — belum klasifikasi sasaran berdasarkan demografis + sebaran akses; pengukuran efektivitas belum ada.

### 1.6 Koordinasi dan Kerjasama

**1.6.1 Belum ada SOP koordinasi dengan K/L dan instansi lain** — judi online online penanganannya butuh OJK, Kepolisian, PPATK.

**1.6.2 Belum ada struktur tata kerja dengan PSE dan stakeholder lain** — terkait khususnya 798 ISP tidak patuh, APJII, platform UGC.

## 5 Rekomendasi Utama BPK kepada Menteri Komdigi

1. **Pengembangan & pemutakhiran CSE** — crawling, machine learning, pengolahan gambar; teknologi terbaru.
2. **Penyusunan ulang distribusi & alokasi penempatan TKPPSE** — berdasarkan kondisi terkini; hindari **redundancy pemasangan TKPPSE di ISP dan NAP**.
3. **Analisa hasil crawling CSE yang belum diverifikasi** + SOP/sistem verifikasi, validasi, serah terima, tindak lanjut — integratif, transparan, akuntabel.
4. **Pedoman pengelolaan SDM** — rekrutmen, target kinerja verifikator, penilaian kinerja berkala.
5. **Pemantauan berkala** penyampaian hasil crawling untuk pemblokiran tepat waktu + dokumentasi Berita Acara dengan rincian.

## Respon Menteri Komdigi

> "Menteri Komunikasi dan Digital menyatakan sependapat dengan kesimpulan di atas dan bersedia menindaklanjuti rekomendasi BPK."

## Relevansi dengan rekomendasi detail (34 poin)

34 rekomendasi lengkap ada di [[pemantauan-tlhp-wasdig-november-2025]] — dikluster per:
- **A** Arsitektur, kapasitas, SOP CSE
- **B** Infrastruktur TKPPSE, RPZ, RTBH (evaluasi, redistribusi, hindari redundancy)
- **C** Regulasi ISP (sinkronisasi TrustPositif, RPZ pada DNS, redirecting DNS Publik, sanksi/reward)
- **D** Tata kelola antar direktorat & lintas K/L
- **E** Proses crawling & verifikasi
- **F** Sinkronisasi database TKPPSE
- **G** Pengawasan PSE
- **H** Sosialisasi

## Kaitan dengan laporan lain

| Laporan | Kaitan |
|---|---|
| [[notisi-tata-kelola-konten-negatif-2025]] + [[laporan-tata-kelola-konten-negatif-final-2025]] | Itjen II re-analisis LHP Kinerja ini → notisi kritis 25 Juli 2025 |
| [[laporan-pendampingan-konten-digital-final-2025]] | Tindak lanjut 8 temuan LHP Kinerja + rencana aksi |
| [[pemantauan-tlhp-wasdig-november-2025]] | 34 rekomendasi → 17,07% sesuai per 28 Nov 2025 |
| [[tlhp-eksternal-simwas-ir2]] | **33 rekomendasi di SIMWAS (April 2026): 15 sesuai + 18 belum** — progres dari 17,07% (Nov 2025) → 45,5% (April 2026); cluster belum = arsitektur TKPPSE + MoU lintas K/L + regulasi deteksi konten |
| [[tkppse]] | Overview sistem + kronologi audit |
| [[lha-verifikasi-tagihan-om-tkppse-2024-rp57m]] | Audit Itjen II paralel atas sisa Rp57M OM TKPPSE |

## Status TLHP per April 2026 (SIMWAS)

Dari 34 rekomendasi BPK Kinerja Konten, SIMWAS export April 2026 mencatat **34 rek (No.21–54)** dengan status ganda Itjen vs BPK:

- **15 Sesuai kedua pihak** (44,1%)
- **19 Belum Sesuai kedua pihak** (55,9%)

Rekomendasi dengan **TL ≥7×** yang masih belum selesai: No.24–26 (Infrastruktur TKPPSE), No.30 (database TKPPSE vs batch list), No.38 (analisa crawling CSE), No.41 (kewajiban ISP sinkron DB, 10 TL), No.45 (instruksi kerja lintas K/L/D, 10 TL), No.47 (reward-punishment 370+798 ISP). Tambahan: **No.54 (5 TL) MoU dengan APJII** untuk tugas pencegahan konten — rekomendasi struktural yang menuntut koordinasi asosiasi ISP. Lihat [[tlhp-eksternal-simwas-ir2]] untuk tabel lengkap.

## Related pages

- [[bpk-laporan-hasil-pemeriksaan]]
- [[bpk-spi-lk-kominfo-2024]]
- [[tkppse]]
- [[pemantauan-tlhp-wasdig-november-2025]]
- [[tlhp-eksternal-simwas-ir2]]
- [[notisi-tata-kelola-konten-negatif-2025]]
- [[laporan-tata-kelola-konten-negatif-final-2025]]
- [[laporan-pendampingan-konten-digital-final-2025]]
- [[lha-verifikasi-tagihan-om-tkppse-2024-rp57m]]
- [[direktorat-jenderal-pengawasan-ruang-digital]]
