# Pemantauan TLHP Wasdig (November 2025)

**Summary**: Laporan pemantauan TLHP eksternal dan internal atas Ditjen Pengawasan Ruang Digital per 28 November 2025. **44 rekomendasi eksternal** — hanya 9 sesuai, **35 belum** (tingkat pemenuhan tahun berjalan cuma **17,07%**). **21 rekomendasi internal** (10 sesuai, 11 belum). Penarik utama: 34 dari 35 temuan eksternal belum sesuai adalah **rekomendasi BPK atas audit TKPPSE 2019–Sem I 2024**, dan temuan internal didominasi akumulasi kewajiban pembayaran OM TKPPSE + Kolokasi + Metro-E.

**Sources**: B-412/IJ.3/PW.04.04/11/2025 tanggal 28 November 2025

**Last updated**: 2025-11-28

---

## Konteks

Pasangan Wasdig dari [[pemantauan-tlhp-ekdig-november-2025]]. ST 264/IJ.3/KP.01.06/11/2025 tanggal 19 November 2025. Ditjen [[direktorat-jenderal-pengawasan-ruang-digital|Wasdig]] adalah pewaris ex-PPI (TKPPSE, monitoring penyiaran) + sebagian ex-Aptika (TKPPSE OM, PSrE) — sehingga menanggung **seluruh beban rekomendasi BPK atas audit kinerja pencegahan konten dilarang**.

Kontras dengan EkDig (83,33% sesuai) tajam: Wasdig **17,07%** sesuai untuk tahun berjalan. Ini bukan karena Wasdig malas — tapi karena skala rekomendasi BPK 2025 TKPPSE raksasa (34 rekomendasi) dan sebagian besar bersifat struktural (menyusun regulasi, MoU lintas K/L, sinkronisasi TrustPositif, dll) yang butuh waktu berbulan-bulan untuk dituntaskan.

## Ringkasan Eksekutif

### 1. TLHP Eksternal (44 rekomendasi total)

| Status | Jumlah | Sesuai | Tingkat Pemenuhan |
|---|---:|---:|---:|
| Tahun Berjalan (2025) | 41 | 7 | **17,07%** |
| Tahun Sebelumnya | 3 | 2 | 66,67% |

### 2. TLHP Internal (21 rekomendasi total)

| Status | Jumlah | Sesuai | Tingkat Pemenuhan |
|---|---:|---:|---:|
| Tahun Berjalan (2025) | 18 | 10 | 55,56% |
| Tahun Sebelumnya | 3 | 0 | **0%** |

## 35 Rekomendasi Eksternal Belum Sesuai

### BPK — Kinerja Pencegahan Penyebarluasan Konten Dilarang TA 2019–Sem I 2024 (34 rekomendasi)

Audit kinerja BPK atas [[tkppse|TKPPSE]] yang dirilis 2025 menjadi **mother lode** rekomendasi Wasdig. Daftar yang masih "Belum Sesuai" (per Nov 2025) disusun berdasarkan topik di tabel laporan asli:

#### Kluster A — Arsitektur, kapasitas, & SOP CSE
- **Menyusun dan menerapkan arsitektur bisnis** pencegahan konten yang terpadu dan komprehensif, dengan teknologi terbaru dan pemutakhiran berkelanjutan.
- Meningkatkan kapasitas SDM — pelatihan IT untuk aplikasi CSE setiap tahun.
- Menyusun **SOP pengawasan layanan pemeliharaan CSE** (pemantauan, evaluasi kinerja penyedia, SLA, sistem pelaporan, penunjukan pihak yang bertanggungjawab).

#### Kluster B — Infrastruktur TKPPSE, RPZ, RTBH
- Evaluasi distribusi dan alokasi penempatan TKPPSE — **menyusun ulang distribusi** agar sesuai perkembangan.
- Mengoptimalkan TKPPSE — menghindari **redundancy pemasangan** antara ISP dan NAP.
- Pemeliharaan infrastruktur TKPPSE sesuai hasil evaluasi.
- Evaluasi kinerja infrastruktur **RPZ dan RTBH** dan menindaklanjuti dengan penyusunan ulang alokasi TKPPSE.

#### Kluster C — Regulasi ISP
- Menyusun peraturan yang mengharuskan ISP sinkronisasi TrustPositif, menerapkan RPZ pada seluruh DNS, dan **redirecting DNS Publik** (Google, Cloudflare, OpenDNS) yang belum RPZ.
- Pemantauan seluruh ISP tersinkronisasi TrustPositif, evaluasi berkala, peringatan kepada ISP tidak patuh.
- **Sanksi/reward system**: apresiasi 370 ISP yang telah BIND RPZ + memblokir konten, sanksi 798 ISP yang belum.
- Menetapkan kewajiban ISP untuk **sinkronisasi daftar hitam** dari database Kominfo.
- Menyusun Analisis Log memantau kepatuhan ISP + perangkat lunak terintegrasi + evaluasi periodik.
- Tata cara/metode sinkronisasi daftar hitam ke sistem DNS Komdigi yang **dapat dimonitor**.
- Sistem pemantauan terpadu berbasis risiko untuk memantau kepatuhan ISP.

#### Kluster D — Tata kelola antar direktorat & lintas K/L
- Ketentuan tata hubungan direktorat yang menangani pengawasan/penegakan hukum ISP & NAP, direktorat metro ethernet, direktorat pemantauan pelaporan & penganggaran aset TI — terintegrasi dalam arsitektur SPBE di Komdigi.
- Regulasi pelaksanaan spesifik: mekanisme & tanggung jawab pencegahan konten ilegal, standar sistem deteksi dini & pemantauan real-time.
- Mekanisme koordinasi & eskalasi lintas instansi + standar minimum sistem pencegahan & pemantauan.
- Pemantauan **kepatuhan platform** secara periodik + sanksi.
- MoU/PKS dengan platform, APJII, dan K/L terkait pengendalian konten.
- Instruksi kerja penyampaian informasi sisipan muatan ilegal kepada pimpinan K/L/D + prosedur alternatif jika pengelola situs pemerintah tidak takedown.

#### Kluster E — Proses crawling & verifikasi
- Pemantauan berkala penyampaian hasil **crawling** + pendokumentasian Berita Acara dengan rincian hasil.
- Kerjasama dengan instansi lain untuk aduankonten.id selain judi/pornografi.
- Analisa hasil **crawling CSE yang belum diverifikasi** + kebijakan lebih lanjut.
- Pedoman pengelolaan SDM: rekrutmen, target kinerja verifikator, evaluasi berkala.
- SOP & sistem verifikasi, validasi serah terima, dan tindak lanjut atas domain, IP, UGC hasil crawling — integratif, transparan, akuntabel.
- SOP dan juknis crawling termasuk teknis pembuatan dan penggunaan keyword.

#### Kluster F — Sinkronisasi database TKPPSE
- Memastikan jumlah daftar hitam di database TKPPSE **sesuai dokumen batch list** sebagai dokumen sumber.

#### Kluster G — Pengawasan PSE
- Pemantauan & pengawasan atas **PSE** yang beraktivitas di Indonesia secara menyeluruh + sanksi tegas bagi PSE belum berizin.
- MoU/PKS antara PSE platform dan Komdigi untuk prosedur tindak lanjut daftar URL/konten diblokir.

#### Kluster H — Sosialisasi
- Rencana & klasifikasi sasaran masyarakat berdasarkan demografis & sebaran akses konten dilarang untuk sosialisasi pencegahan.
- Mengukur tingkat keberhasilan dan ketepatan sasaran sosialisasi.

### BPK — Kinerja Keamanan & Ketahanan Siber (1 rekomendasi, 2022)

- Koordinasi dengan **BSSN** terkait verifikasi pendaftaran, pengawasan, dan pelaksanaan Sistem Pengamanan dalam Penyelenggaraan Sistem Elektronik + membangun sistem terpadu pendaftaran & pengawasan PSE lingkup publik maupun privat. **Belum Sesuai** sejak 2022.

## 11 Rekomendasi Internal Belum Sesuai

### Cluster O&M TKPPSE 2024 (5 rekomendasi — kewajiban finansial)

| Rek | Isi | Nilai |
|---|---|---:|
| 1 | Pembayaran kolokasi yang belum dapat dinilai ketersediaan layanannya | **Rp4.661.397.331** |
| 2 | Tagihan kolokasi & Metro-E yang belum dapat dinilai — jangan dibayar dulu | Rp13,60M (kolokasi) + **Rp21,10M** (Metro-E) |
| 3 | Tagihan kolokasi & Metro-E yang **dapat diyakini** — bayar dengan dokumen akuntabilitas per LPKA 62/2025 | Rp22.631.211.040 |
| 4 | Direktur Pengendalian Ruang Digital agar memperbaiki sistem pengendalian kontrak OM TKPPSE (SLA, prosedur inspeksi, kebijakan durasi penyimpanan data prestasi kerja) | — |
| 5 | KPA & PPK agar konsultasi dengan Biro Hukum perihal rencana pembayaran seluruh tagihan O&M TKPPSE TA 2024 | — |

Total kewajiban yang masih jadi bahasan: **Rp39,4M** (dari Rek 1–2) + Rp22,63M yang sudah dapat dibayar tapi belum jadi. Lihat [[kha-revisi2-om-tkppse-2024-rp16-rp57]] untuk framework pembayarannya.

### Cluster PPK JAR, P3KJT, dan TKPPSE TA 2021–2023 (3 rekomendasi — penarikan kelebihan bayar)

| Rek | Isi | Nilai |
|---|---|---:|
| 6 | Teguran PPK JAR TA 2022 + SOP Pra Implementasi/Survei Lapangan (Sekretaris Ditjen Aptika ex KPA TA 2022) | — |
| 7 | Tarik kembali biaya PPK P3KJT TA 2022: **Rp410,98jt (jasa)** + Rp85,07jt (denda keterlambatan) | Rp496,05jt |
| 8 | Tarik kembali biaya PPK TKPPSE 2021 + P3KJT 2022: **biaya pengiriman Rp2,76M + IXIA Rp18,19M + SFP Rp6,16M** | **Rp27,12M** |

**Total penarikan kas negara yang belum ditindaklanjuti**: ~Rp27,6M.

### Cluster Tahun Sebelumnya (3 rekomendasi — 2023)

Sisa warisan dari audit internal TKPPSE 2021–2022 (Direktur Pengendalian Aplikasi Informatika ex Aptika):
- Tandatangan laporan bulanan + evaluasi status unblock 5 operator seluler di WIB/WITA/WIT.
- Teguran tertulis PPK + laporan capaian SLA koneksi jaringan akses TKPPSE 2021–2022.
- Penilaian ulang JAR TA 2021 **Rp2.298.693.100** (biaya instalasi, pengiriman, pajak) + setor kas negara jika tidak sesuai.

**Total warisan yang belum sesuai**: ~Rp2,3M.

## Angka absolut yang masih "menggantung" di Wasdig

| Klaster | Nilai | Status |
|---|---:|---|
| OM TKPPSE 2024 — kolokasi belum dapat dinilai | Rp4,66M | belum dibayar, belum sesuai |
| OM TKPPSE 2024 — kolokasi + Metro-E belum dapat dinilai | Rp34,70M | belum dibayar, belum sesuai |
| OM TKPPSE 2024 — dapat diyakini | Rp22,63M | kerangka pembayaran sudah ada, eksekusi belum |
| Penarikan kas negara P3KJT + TKPPSE 2021–2022 | Rp27,6M + Rp2,3M | piutang negara belum ditagih |
| **Total eksposur internal** | **≈Rp91,9M** | |

Ini belum termasuk:
- **Rp23,96M** OM TKPPSE 2024 yang sudah framework LKPP tapi belum cair (di [[kha-revisi2-om-tkppse-2024-rp16-rp57]]).
- **~Rp57M** potensi OM TKPPSE 2025 baru (di [[lhr-lk-tw3-2025-itjen-ekdig-wasdig]]).

Jadi eksposur finansial TKPPSE total untuk Wasdig di akhir 2025 dapat melampaui **Rp150M**.

## Pola umum

- **Wasdig jauh tertinggal** dalam TLHP (17,07% vs EkDig 83,33%) — karena skala rekomendasi BPK TKPPSE 2025 (34 rek struktural) yang tidak bisa diselesaikan dalam hitungan bulan.
- **100% tahun sebelumnya "0% sesuai"** — 3 rekomendasi Direktur Pengendalian Aplikasi Informatika era Aptika sama sekali belum bergerak.
- Kewajiban finansial TKPPSE yang menumpuk ~Rp92M → butuh paket pengadaan/pembayaran tersendiri yang sudah mulai diproses di 2026 (lihat [[lhp-pengadaan-redesain-tkppse-2026]]).

## Update progres per April 2026

[[tlhp-eksternal-simwas-ir2|SIMWAS TLHP Eksternal]] (ekspor April 2026) menunjukkan progres signifikan dari laporan pemantauan November 2025 ini:

- **Kinerja Konten**: 17,07% sesuai (Nov 2025) → **45,5% sesuai** (April 2026) — 15 dari 33 rek tercatat "Sudah Sesuai kedua pihak"
- **LK 2024 BPK**: 20 rek di SIMWAS, 11 Sudah Sesuai (55%)

Yang masih tertinggal: rekomendasi struktural arsitektur TKPPSE (No.24-26), MoU lintas K/L (No.50-53), sinkronisasi ISP DNS (No.41, 47), regulasi sistem deteksi konten ilegal (No.32-33).

## Related pages

- [[pemantauan-tlhp-ekdig-november-2025]]
- [[tlhp-eksternal-simwas-ir2]]
- [[tlhp-internal-simwas-ir2]]
- [[tkppse]]
- [[kha-revisi2-om-tkppse-2024-rp16-rp57]]
- [[dha-tahap2-om-tkppse-2024]]
- [[pendampingan-om-tkppse-2024]]
- [[lha-om-tkppse-2024]]
- [[lha-om-tkppse-2025]]
- [[notisi-tata-kelola-konten-negatif-2025]]
- [[laporan-tata-kelola-konten-negatif-final-2025]]
- [[lhp-pengadaan-redesain-tkppse-2026]]
- [[lhr-lk-tw3-2025-itjen-ekdig-wasdig]]
- [[direktorat-jenderal-pengawasan-ruang-digital]]
- [[inspektorat-ii]]
