# TKPPSE — Tata Kelola Pengendalian Penyelenggara Sistem Elektronik

**Summary**: Sistem infrastruktur untuk memutus akses secara langsung ketika pengguna internet mengakses konten yang dilarang, melalui mekanisme TCP Reset. Dipasang di lokasi-lokasi Pemilik Jaringan Telekomunikasi (PJT) di Indonesia. Dikelola oleh Ditjen Pengawasan Ruang Digital (PRD) / d.h. Ditjen Aptika. Masuk wilayah pengawasan Inspektorat II dengan riwayat audit dan pemantauan mencakup pengadaan, OM, redesain, hingga akuntabilitas pembayaran.

**Sources**: 62 IJ.3 PW.02.06 surat keluar 20.02.2025 (Pendampingan OM TKPPSE TA 2024); 34 IJ.3 PW.04.03 surat keluar 30.01.2026 (Redesain TKPPSE); 51 IJ.3 PW.04.01 surat keluar 11.02.2026 (LHA OM TKPPSE TA 2025); 100/103 IJ.3 PW.02.04/04.04 surat keluar 17-20.3.25 (CHR/LHR Tambahan Anggaran Wasdig); 111 IJ.3 PW.02.01 surat keluar 27.03.25 (DHA Tahap 2 Audit Prestasi OM TKPPSE); 116 IJ.3 PW.04.04 surat keluar 14.04.25 (Relaksasi Anggaran Wasdig); 127 IJ.3 PW.02.02 surat keluar 28.04.25 (LHA Final OM TKPPSE TA 2024); 156 IJ.3 PW.02.06 surat keluar 23.05.25 (Atensi Pemutusan Konektivitas TKPPSE); 231 IJ.3 PW.02.06 surat keluar 25.07.25 (Notisi Tata Kelola Konten Negatif); 233 IJ.3 PW.04.04 surat keluar 25.07.25 (Revisi Relaksasi EkDig Rp233,74M); 264 IJ.3 PW.02.06 surat keluar 29.08.25 (Laporan Final Tata Kelola Konten Negatif)

**Last updated**: 2026-04-22

---

## Definisi dan Mekanisme

**TKPPSE** (Tata Kelola Pengendalian Penyelenggara Sistem Elektronik) adalah sistem pemerintah untuk memutus akses pengguna internet ke konten yang dilarang. Mekanisme: **TCP Reset** — mengakhiri koneksi TCP secara tiba-tiba pada lapisan transport layer.

Sistem TKPPSE dipasang di lokasi-lokasi **Pemilik Jaringan Telekomunikasi (PJT)** di seluruh Indonesia, termasuk operator seluler, ISP, dan penyedia infrastruktur fiber.

## Sumber LHP BPK

Rekomendasi 34 poin BPK yang dipantau di wiki berasal dari **[[bpk-kinerja-pste-2024]]** (LHP Kinerja, 6 Feb 2025) — audit 5,5 tahun cakupan (TA 2019 s.d. Semester I 2024), total nilai pengembangan sistem Rp1,82 triliun, kesimpulan **Kurang Efektif**.

Temuan kelebihan bayar Rp4,66M + utang tidak didukung bukti Rp57,34M berasal dari **[[bpk-spi-lk-kominfo-2024]]** (LHP SPI LK, 19 Mei 2025).

## Kronologi Pengadaan dan OM

| Tanggal | Kejadian |
|---|---|
| 6 Agustus 2021 | Surat perjanjian Pekerjaan Sistem TKPPSE dengan PT LTI dan Eltrans — **nilai kontrak Rp963.122.600.000** |
| 30 Maret 2022 | BAST TKPPSE 100% — periode OM TKPPSE dimulai |
| 29 September 2022 | Surat Perjanjian Pemenuhan PKJT dengan PT Eltran Indonesia — **nilai kontrak Rp827.857.609.593** |
| 17 Maret 2023 | BAST PKJT 100% — periode OM PKJT dimulai |
| 17 Maret 2024 | **OM PKJT PT Eltran Indonesia selesai** — kewajiban OM beralih ke Kemkomdigi (belum ada anggaran/kontrak) |
| 30 Maret 2024 | **OM TKPPSE PT LTI dan Eltrans selesai** — beralih ke Kemkomdigi (belum ada anggaran/kontrak) |
| 22 Agustus 2024 | **Revisi Anggaran OM TKPPSE disetujui** |
| Desember 2024 | Pembayaran OM TKPPSE ke PT SUFI dilakukan (Rp21,2M) — lihat [[pendampingan-om-tkppse-2024]] |

(source: 62 IJ.3 PW.02.06 surat keluar 20.02.2025)

## Cakupan OM TKPPSE

Berdasarkan B-62 (Pendampingan Akuntabilitas Tagihan OM TKPPSE TA 2024), layanan OM mencakup:

1. **Kolokasi** (penempatan perangkat di data center PJT)
2. **Paket data/internet**
3. **Metro-E** (jaringan Ethernet metropolitan untuk konektivitas antar lokasi)

Monitoring Metro-E menggunakan tool **Zabbik**.

## Aktor Utama

| Aktor | Peran |
|---|---|
| Kemkomdigi / Ditjen PRD (d.h. Aptika) | Pemilik program, pengguna akhir |
| **PT SUFI** | Penyedia/aggregator OM pasca 2024 — memiliki perikatan kontrak dengan PJT dan Kemkomdigi |
| **PJT** (Pemilik Jaringan Telekomunikasi) | Penyedia lokasi DC + infrastruktur fisik tempat TKPPSE dipasang. Contoh: Indosat, Telkomsel, XLSmart, Telkom, Telkomsat, Kreatif Pacific, PT NTT, PT Trans Hybrid Communication, PT Dinamika, **PT Mora Telematika (Moratel)**, **PT Lintasarta + iForte**, PT Eltran Indonesia |
| PT LTI dan Eltrans | Penyedia pekerjaan sistem TKPPSE 2021 |
| PT Eltran Indonesia | Penyedia pekerjaan pemenuhan PKJT 2022 |

## Status PJT TA 2026

Berdasarkan [[lhp-pengadaan-redesain-tkppse-2026]]:

**Terkontrak TA 2026** (6 PJT via INAPROC):
Indosat, Telkomsel, XLSmart, Telkom, Telkomsat, Kreatif Pacific

**Belum Terkontrak TA 2026** (6 PJT — kendala administratif/teknis/legalitas):
PT NTT, PT Trans Hybrid Communication, PT Dinamika, **PT Moratel** (topologi jaringan terenkripsi — perangkat TKPPSE tidak dapat membaca trafik), **PT Lintasarta + iForte** (lokasi DC berkontrak PT SUFI dengan batasan confidentiality)

## Isu dan Audit Inspektorat II

| Tahun | Kegiatan | Sumber |
|---|---|---|
| Feb 2025 | **Pendampingan akuntabilitas OM TKPPSE TA 2024** — pekerjaan mendahului kontrak Rp78,56M; 6 bukti belum memadai | [[pendampingan-om-tkppse-2024]] |
| Mar 2025 | **CHR + LHR Usulan Tambahan Anggaran Ditjen Wasdig TA 2025** — Rp414,7M, OM TKPPSE Rp337,6M (80%) untuk pembayaran tunggakan; 3 aspek catatan diselesaikan → disetujui | [[chr-tambahan-anggaran-wasdig-2025]], [[lhr-tambahan-anggaran-wasdig-2025]] |
| Mar 2025 | **DHA Tahap 2 Audit Prestasi OM TKPPSE TA 2024** — pakai Zabbix + Log Server, SLA 99,5%; dari Rp78,56M total hanya **Rp22,93M (29%) dapat diyakini** | [[dha-tahap2-om-tkppse-2024]] |
| Apr 2025 | **LHR Relaksasi Anggaran Ditjen Wasdig TA 2025** — buka blokir Rp100,81M (OM TKPPSE Rp72,6M + Konten Ilegal Rp28,2M); mekanisme PMK 107/2024 (perubahan PMK 62/2023); disetujui | [[lhr-relaksasi-anggaran-wasdig-2025]] |
| Apr 2025 | **LHA Final Prestasi Kerja OM TKPPSE TA 2024** — update DHA Tahap 2 dengan data tambahan: **Rp39,20M (50%) dapat diyakini**, Rp34,70M belum dapat dinilai; Legal Opinion Biro Hukum: pembayaran tanpa kontrak berpotensi masalah hukum; rekomendasi KPA/PPK konsultasi Biro Hukum | [[lha-om-tkppse-2024]] |
| Mei 2025 | **⚠ Laporan Atensi Pemutusan Konektivitas TKPPSE** — krisis operasional: kapasitas sudah turun 33% (27.552 Gbps dari 83.402 Gbps); tambahan risiko 26% dari PT XL Axiata + PT Indosat berencana putus layanan akhir Mei 2025 (21.640 Gbps); kebutuhan bayar Rp103,06M vs tersedia Rp72,6M | [[atensi-pemutusan-tkppse-2025]] |
| Jul 2025 | **⚠⚠ Notisi Tata Kelola Pengendalian Konten Negatif** — kritik sistematis: **efektivitas TKPPSE 22,44%** (vs RTBH 81,45% dan RPZ 79,60%); kekurangan 17 NAP + 1.183 ISP + 40.620 GB kapasitas; lisensi Oracle Linux 7 kedaluwarsa Des 2024; tumpang tindih CNS vs CSE-Rugos + TKPPSE vs RTBH/TrustNG; **aset BMN Rp1,59T berpotensi idle**; 5 rekomendasi termasuk tunda pengadaan perangkat baru | [[notisi-tata-kelola-konten-negatif-2025]] |
| Jul 2025 | **Relaksasi EkDig ke ABT OM TKPPSE Rp233,74M** — Ditjen EkDig memindahkan Rp233,74M ke Wasdig untuk ABT OM TKPPSE; 7447 Pengelolaan data EkDig turun 83% | [[lhr-revisi-relaksasi-anggaran-ekdig-2025]] |
| Agu 2025 | **Laporan Final Tata Kelola Konten Negatif** — versi final Notisi 231; substansi identik; perubahan minor (TrustNG → DNS TrustNG) | [[laporan-tata-kelola-konten-negatif-final-2025]] |
| Sep 2025 | **LHR Pemblokiran ISP via RTBH+DNS TrustNG** — pekerjaan Jan-Aug 2025 tanpa kontrak Rp50jt/bulan; dasar Perpres 46/2025 Pasal 9(1)f2; output sinkronisasi 3x/minggu terpenuhi | [[lhr-pemblokiran-rtbh-trustng-2025]] |
| Sep 2025 | **CHR RKA-K/L Wasdig TA 2026** — pagu Rp134,82M vs kebutuhan bare minimum Rp542M (gap Rp407M); peremajaan AIS Rp118,98M; risiko 6 fungsi pengawasan terhenti | [[chr-rka-kl-wasdig-2026]] |
| Sep 2025 | **Laporan Final Pendampingan Tata Kelola Konten Digital** — gabungan Notisi 231 + Laporan 264 + tindak lanjut 8 temuan LHP Kinerja BPK; rencana aksi Wasdig (kajian TKPPSE selesai 25 Okt) | [[laporan-pendampingan-konten-digital-final-2025]] |
| Okt 2025 | **KHA Revisi 2 Verifikasi Tagihan OM TKPPSE Rp16M+Rp57M** — **Rp23,96M dapat diyakini** sebagai tunggakan (dari Rp28,74M non-dispute); Rp4,78M butuh data dukung; Rp1,30M butuh cek fisik; framework LKPP 22441/D.4.1/10/2025 untuk kontrak pembayaran retroaktif | [[kha-revisi2-om-tkppse-2024-rp16-rp57]] |
| Okt 2025 | **LHR Revisi Anggaran Wasdig + Relaksasi PNBP** — tambahan Rp41,63M (Setjen+KPM) + Rp217,01M (PNBP antar UKE1) = Rp258,64M; dukungan OM TKPPSE | [[lhr-revisi-anggaran-wasdig-oktober-2025]], [[lhr-relaksasi-pnbp-wasdig-oktober-2025]] |
| Nov 2025 | **LHR LK TW III TA 2025 Wasdig** — belanja 7,05% + **Utang Kontinjensi TKPPSE Rp36,02M** (Kolokasi Rp10,93M + Internet Rp4,19M + Metro-E Rp20,90M) + **potensi utang OM TKPPSE 2025 ~Rp57M** + selisih TKTM Rp497jt | [[lhr-lk-tw3-2025-itjen-ekdig-wasdig]] |
| Nov 2025 | **Pemantauan TLHP Wasdig** — 35 dari 44 rekomendasi eksternal belum sesuai (17,07%), 34 di antaranya BPK Kinerja Pencegahan Konten 2019–Sem I 2024; 11 dari 21 internal belum, eksposur finansial OM TKPPSE ~Rp92M | [[pemantauan-tlhp-wasdig-november-2025]] |
| **Des 2025** | **⚠⚠⚠ LHA Final Verifikasi Tagihan OM TKPPSE 2024 Rp57M** — **seluruh Rp57.336.027.828 tidak dapat diyakini → tidak dapat diakui sebagai tunggakan, tidak dibayar**; SLA akumulasi 50,12% dari target 99,5%; cek fisik 3 lokasi (Batam, Aceh, Solo) Metro-E mati ~1 tahun; **187 titik topologi dikunci PT SUFI**; BPKP menolak audit tunggakan (23 Okt 2025); B-435 ke Biro Keuangan: "kemungkinan memengaruhi LK Kemkomdigi 2025"; rekomendasi **redesain TKPPSE tanpa PT SUFI + evaluasi tim TKPPSE** | [[lha-verifikasi-tagihan-om-tkppse-2024-rp57m]] |
| Jan 2026 | **LHP Monitoring Pengadaan dan Redesain TKPPSE TA 2026** — 2 temuan: kajian teknis belum diimplementasikan, 6 PJT belum berkontrak | [[lhp-pengadaan-redesain-tkppse-2026]] |
| Feb 2026 | **LHA Audit OM TKPPSE TA 2025 (3 tahap)** — total tagihan Rp14,23M di tahap 3, dapat diyakini Rp10,66M; 4 temuan termasuk tagihan Desember tanpa kontrak Rp2,69M | [[lha-om-tkppse-2025]] |

## Isu Struktural

### 1. Pekerjaan Mendahului Kontrak (Maret-Desember 2024)

Saat OM beralih dari penyedia pengadaan ke Kemkomdigi (Maret 2024), **belum ada anggaran dan kontrak OM**. Alokasi baru tersedia 22 Agt 2024. Ini menciptakan **5+ bulan pekerjaan tanpa dasar kontrak**, dengan total tagihan Rp78,56M (lihat [[pendampingan-om-tkppse-2024]]).

**Kuantifikasi Final LHA (28 April 2025)** — dari Rp78,56M total:
- Sudah dibayar Rp21,23M: diyakini **Rp16,56M (78%)**; belum dinilai Rp4,66M.
- Belum dibayar Rp57,34M: diyakini **Rp22,63M (39,5%)**; belum dinilai Rp34,70M (kolokasi Rp13,60M + Metro-E Rp21,10M).
- **Total dapat diyakini: Rp39,20M (50%) dari Rp78,56M**.

**Kuantifikasi KHA Revisi 2 Okt 2025** ([[kha-revisi2-om-tkppse-2024-rp16-rp57]]):
- Obyek verifikasi non-dispute (dari tagihan Rp57,34M): **Rp28,74M**.
- Rp1,30M tidak masuk pengujian (kolokasi SUFI butuh cek fisik).
- Rp27,44M yang masuk pengujian.
- **Rp23,96M dapat diyakini dan diakui sebagai tunggakan**.
- Rp4,78M belum dapat diyakini (butuh data dukung atau tidak diakui).

**Kuantifikasi Final LHA Desember 2025** ([[lha-verifikasi-tagihan-om-tkppse-2024-rp57m]]):
- Obyek: seluruh sisa Rp57,34M yang belum dibayar.
- SLA akumulasi 50,12% (non-dispute Rp28,74M) vs target 99,5%.
- **Setelah cek fisik 3 lokasi + konsolidasi temuan: seluruh Rp57,34M tidak dapat diyakini kewajarannya**.
- **Seluruh Rp57,34M tidak dapat diakui sebagai tunggakan → tidak dibayar**.
- BPKP menolak audit tunggakan (23 Okt 2025, surat PE.04.01/S-364) → syarat PMK 62/2023 gagal.
- Framework legal LKPP 22441/D.4.1/10/2025 **runtuh** untuk Rp57,34M karena 3 syarat (analisis urgensi, reviu APIP, audit BPKP) tidak terpenuhi.

Catatan: KHA Okt 2025 yang menilai Rp23,96M dapat diyakini **di-override** oleh LHA Des 2025 karena konsolidasi temuan cek fisik (Metro-E mati 1 tahun di 3 lokasi) + risiko strategis penguasaan 187 titik topologi oleh PT SUFI. Transisi dari "partial yes" ke "full no".

**Framework legal pembayaran retroaktif**: Surat LKPP 22441/D.4.1/10/2025 (13 Okt 2025) mengukuhkan **Perpres 16/2018 Pasal 9(1)f2** (dan Perpres 46/2025 perubahan kedua) sebagai dasar PA/KPA untuk pembayaran TKPPSE tanpa kontrak. Hasil APIP dapat menjadi landasan kontrak pembayaran setelah anggaran tersedia. **Namun** untuk Rp57,34M, framework ini tidak dipenuhi syaratnya (lihat di atas).

Naik dari **Rp22,93M (29%)** di DHA Tahap 2 (27 Mar 2025) ke **Rp39,20M (50%)** di LHA (28 Apr 2025) — peningkatan Rp16,26M dalam 1 bulan karena Ditjen Wasdig submit data prestasi tambahan. Namun **50% masih belum dapat dinilai**: dari 184 lokasi, 55 lokasi belum ada data dukung + 7 lokasi dengan CMD server tanpa uptime.

Lebih detail di [[lha-om-tkppse-2024]]. Rekomendasi utama: **jangan bayar Rp34,70M** sampai data prestasi memadai; KPA/PPK wajib **konsultasi Biro Hukum** atas rencana pembayaran mengikuti Legal Opinion yang menyatakan pembayaran tanpa kontrak berpotensi masalah hukum.

### Leadership Ditjen Aptika TA 2024

Selama masa tagihan OM TKPPSE Mar–Des 2024, Ditjen Aptika mengalami **4 transisi kepemimpinan**:
- Maret – 4 Juli 2024: **Semuel Abrijani Pangerapan**
- 4 – 19 Juli 2024: Plt Dr. Ir. **Ismail MT**
- 19 Juli – 6 Desember 2024: **Hokky Situngkir**
- 7 – 31 Desember 2024: (Ditjen Wasdig baru) **Alexander Sabar**

**KPA Ditjen Aptika Mar–Des 2024**: Ir. I Nyoman Adhiarna M.Eng, Ph.D (konsisten).

**Pemilik Program OM TKPPSE** (data versi LHA final, lihat [[lha-om-tkppse-2024]]):
- Mar – Jun 2024: **Teguh Arifiyadi** (Direktur Pengendalian Aptika).
- Jun – Des 2024: **Aries Kusdaryono** (Direktur Tata Kelola Aptika).

**PPK OM TKPPSE**:
- Mar – Okt 2024: **Sunnas Ginanjar**.
- Okt – Des 2024: **Aries Kusdaryono**.

Ketidakstabilan kepemimpinan ini menjadi konteks pengambilan keputusan untuk melanjutkan layanan tanpa kontrak formal.

### Efektivitas TKPPSE Hanya 22,44% (LHP Kinerja BPK, 6 Februari 2025)

Sumber temuan: [[bpk-kinerja-pste-2024]] (LHP 14/LHP/XVI/02/2025 BPK, 6 Februari 2025). Dirangkum kembali di Notisi Itjen [[notisi-tata-kelola-konten-negatif-2025]] (25 Juli 2025):

**Efektivitas pemblokiran** (uji BPK atas situs yang tidak berhasil diblokir RTBH+RPZ):

| Sistem | Tingkat Keberhasilan |
|---|---|
| RTBH | **81,45%** |
| RPZ | **79,60%** |
| **TKPPSE** | **22,44%** |

**Kekurangan infrastruktur**:
- **17 NAP kurang** (perlu 43, tersedia 26 = kurang 39,53%).
- **1.183 ISP kurang** (perlu 1.188, tersedia 5 lokasi = kurang 99,58%).
- **970 GB kapasitas NAP kurang** + **40.620 GB kapasitas ISP kurang**.

**Lisensi kedaluwarsa**: TKPPSE pakai **Oracle Enterprise Linux 7** yang **kedaluwarsa 31 Desember 2024**. Perlu upgrade ke versi 9 untuk tangani HTTPS, DoH, browser modern.

**4 Sistem Pemblokiran Kemkomdigi**:
- **RPZ** (Response Policy Zone) — 508/1.188 ISP sinkron
- **TKPPSE** — 26 NAP + 89 ISP (151 KOS), 22,44% efektif
- **RTBH** — 803 ISP, 81,45% efektif
- **TrustNG** — 803 ISP + 132 non-ISP, cakupan luas

### Tumpang Tindih & Inefisiensi

1. **CNS (di TKPPSE) vs CSE-Rugos**: OM Rp233,74M vs Rp5,11M untuk fungsi crawling serupa. Jika CSE dihidupkan, CNS jadi redundant → Rp233,74M tidak sepadan.
2. **TKPPSE vs RTBH + TrustNG + RPZ**: pemblokiran domain/IP yang sama via 4 sistem. RTBH + TrustNG sudah cakup 803 ISP + 132 non-ISP (estimasi Rp1,2-1,5M) — lebih luas dari TKPPSE.
3. **89 ISP TKPPSE** redundant karena traffic sudah tercakup NAP yang sama.

### Krisis Kapasitas TKPPSE (Mei 2025)

Laporan Atensi 23 Mei 2025 (lihat [[atensi-pemutusan-tkppse-2025]]) mengungkap krisis operasional:

**Kapasitas TKPPSE saat ini**:
- Awal: **83.402 Gbps** (total kapasitas pengawasan konten negatif)
- Sudah turun: **−27.552 Gbps (33%)** karena Metro-E PJT tidak tersedia
- **Tersisa: 55.850 Gbps (67%)**

**Risiko pemutusan akhir Mei 2025**:
- **PT XL Axiata: 13.420 Gbps**
- **PT Indosat: 8.220 Gbps**
- Total risiko: 21.640 Gbps (**26%** tambahan penurunan)

**Skenario terburuk** (jika XL + Indosat memutus): **34.210 Gbps (41% dari awal)** — **penurunan total 59%**.

**Akar krisis**: tunggakan pembayaran OM TKPPSE Mar 2024 – Mei 2025 → PJT enggan memperbarui perjanjian OM 2025.

- Kebutuhan: Rp103,06M
- Tersedia: Rp72,6M (relaksasi disetujui April 2025)
- Gap: Rp30,5M

### Legal Opinion Biro Hukum (Mar 2025)

Nota Dinas Kepala Biro Hukum Kemkomdigi **270/SJ.4/HK.05.01/03/2025 tgl 10 Maret 2025** — merespons permintaan Itjen II (84/IJ.3/PW.02.02/03/2025) — menyimpulkan:

1. Pembayaran tagihan OM TKPPSE setelah 30 Maret 2024 **berpotensi masalah hukum** akibat ketiadaan kontrak.
2. Tanpa kontrak → tidak ada SLA → ketidakjelasan standar layanan dan evaluasi penyedia.
3. Sebagian pembayaran tanpa kontrak → **risiko kepatuhan pengelolaan keuangan negara**.

Rekomendasi Biro Hukum: audit dan validasi tagihan + koordinasi dengan **Kemenkeu, BPK, BPKP, dan Jamdatun Kejaksaan Agung**.

Legal Opinion ini menjadi dasar rekomendasi LHA agar KPA/PPK berkonsultasi Biro Hukum sebelum pembayaran lebih lanjut.

### 2. Topologi Terenkripsi PT Moratel

Perubahan topologi jaringan terenkripsi di PT Moratel berarti **perangkat TKPPSE tidak dapat membaca trafik** — fungsi TCP Reset gagal. Solusi: usulan pindah ke BDx masih dikaji dari sisi legalitas dan SOP.

### 3. Confidentiality PT SUFI di Lokasi Lintasarta/iForte

Lokasi DC Lintasarta dan iForte berkontrak dengan PT SUFI — ada batasan **confidentiality** yang membatasi akses data Kemkomdigi.

### 3b. **PT SUFI Menguasai 187 Titik Topologi TKPPSE (Des 2025)**

[[lha-verifikasi-tagihan-om-tkppse-2024-rp57m]] mengungkap risiko strategis negara: **PT SUFI memegang kendali penuh atas konfigurasi topologi jaringan pada 187 titik TKPPSE** — selain sebagai penyedia eksklusif Secure Metro-E. Konsekuensi: PT SUFI dapat secara unilateral menghentikan Secure Metro-E atau mengubah konfigurasi → seluruh TKPPSE tidak berfungsi. Rekomendasi Itjen: **redesain TKPPSE tanpa PT SUFI** apabila sistem akan dilanjutkan.

Pola penunjukan PT SUFI sendiri cacat: awalnya subkontraktor PT Eltrans (2021–2022), tetapi **tidak ada dokumen formal penunjukan subkontraktor**. Kelanjutan 2024 hanya berbasis Surat Perintah Kelanjutan Pekerjaan — bukan skema kompetisi.

### 3c. Metro-E Mati 1 Tahun — Cek Fisik 3 Lokasi (Des 2025)

Cek fisik [[lha-verifikasi-tagihan-om-tkppse-2024-rp57m]] di Batam, Aceh, dan Solo (Okt–Nov 2025) mengungkap perangkat Metro-E **tidak berfungsi selama ~1 tahun**:
- Batam: kesalahan konfigurasi kabel.
- Aceh + Solo: konfigurasi berubah pasca merger H3I × PT IOH; tidak ada rekonfigurasi TKPPSE.
- PT SUFI tidak melakukan troubleshooting/kunjungan lokasi.
- Tim TKPPSE Komdigi tidak melaporkan malfungsi ke atasan.

Komdigi membayar sewa Metro-E untuk layanan mati selama 1 tahun — kontributor langsung pada penilaian "Rp57M tidak dapat diyakini".

### 4. Kajian Teknis Belum Diimplementasikan

Kajian teknis TKPPSE merekomendasikan: adaptasi teknis berkala mengikuti protokol internet yang makin *secure/private*; regulasi dasar sebelum implementasi opsi teknis baru; verifikasi proyeksi pertumbuhan trafik; peninjauan lokasi DC dan KOS pasca merger operator seluler menjadi 3 perusahaan (IOH, XLSmart, Telkomsel). Redesain TKPPSE akan dikaji TW II 2026, eksekusi TA 2027.

## Konteks

TKPPSE adalah infrastruktur kritis pemblokiran konten negatif (judi online, pornografi, dll.). Capaian Wasdig: konten judol diputus 2,08M (target 1,2M), konten pornografi takedown 581.549 (target 500.000) pada TW IV 2025 — lihat [[lhe-rb-wasdig-tw4-2025]].

Transisi SOTK Kominfo → Komdigi mengubah pemilik program: Ditjen Aptika (lama) → Ditjen Pengawasan Ruang Digital (baru) → namun KPA Ditjen Aptika Masa Transisi masih ada (per B-62). Arsitektur TKPPSE yang lintas-PJT membuatnya rentan terhadap perubahan struktural di industri telekomunikasi (merger operator, perubahan teknologi, batasan confidentiality antar-vendor).

## Related pages

- [[pendampingan-om-tkppse-2024]]
- [[dha-tahap2-om-tkppse-2024]]
- [[lha-om-tkppse-2024]]
- [[atensi-pemutusan-tkppse-2025]]
- [[notisi-tata-kelola-konten-negatif-2025]]
- [[lhr-revisi-relaksasi-anggaran-ekdig-2025]]
- [[lha-om-tkppse-2025]]
- [[lha-verifikasi-tagihan-om-tkppse-2024-rp57m]]
- [[lhp-pengadaan-redesain-tkppse-2026]]
- [[kha-revisi2-om-tkppse-2024-rp16-rp57]]
- [[bpk-kinerja-pste-2024]]
- [[bpk-spi-lk-kominfo-2024]]
- [[bpk-laporan-hasil-pemeriksaan]]
- [[lhr-lk-tw3-2025-itjen-ekdig-wasdig]]
- [[pemantauan-tlhp-wasdig-november-2025]]
- [[tlhp-internal-simwas-ir2]]
- [[chr-tambahan-anggaran-wasdig-2025]]
- [[lhr-tambahan-anggaran-wasdig-2025]]
- [[lhr-relaksasi-anggaran-wasdig-2025]]
- [[pendampingan-crawling-wasdig-2025]]
- [[chr-ipp-pnbp-wasdig-2025-2028]]
- [[lhe-rb-wasdig-tw4-2025]]
- [[inspektorat-ii]]
