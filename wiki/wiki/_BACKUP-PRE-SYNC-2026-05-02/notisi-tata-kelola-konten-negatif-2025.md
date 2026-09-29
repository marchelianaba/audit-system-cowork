# Notisi Hasil Penelaahan Tata Kelola Pengendalian Konten Negatif (TKPPSE)

**⚠ Catatan**: Versi final dokumen ini adalah [[laporan-tata-kelola-konten-negatif-final-2025]] (B-264, 29 Agustus 2025). Notisi ini adalah draft awal untuk tanggapan (deadline 31 Juli 2025). Substansi identik, perubahan minor: "TrustNG" → "DNS TrustNG", 1 residu risiko dihapus di final.

**Summary**: Notisi Inspektorat II yang **mengkritik secara sistematis tata kelola TKPPSE** sebagai sistem pemblokiran konten negatif. Temuan kunci: **efektivitas pemblokiran TKPPSE hanya 22,44%** (dari uji BPK) vs RTBH 81,45% dan RPZ 79,6%. Infrastruktur TKPPSE kekurangan **17 titik NAP + 1.183 titik ISP + 40.620 GB kapasitas ISP**. Lisensi kedaluwarsa (Oracle Linux 7 exp 31 Des 2024). **Tumpang tindih**: (a) CNS di TKPPSE vs CSE-Rugos (OM Rp233,74M vs Rp5,11M); (b) TKPPSE vs RTBH + TrustNG + RPZ untuk pemblokiran domain/IP. **Aset BMN TKPPSE Rp1,59T terancam idle**. 5 rekomendasi termasuk **menunda pengadaan perangkat baru + upgrade lisensi** sampai kajian pemetaan selesai. Deadline tanggapan 31 Juli 2025.

**Sources**: 231 IJ.3 PW.02.06 surat keluar 25.07.2025 Nodin Notisi Hasil Penelaahan Tata Kelola Ditjen Pengawasan Ruang Digital.pdf

**Last updated**: 2026-04-22

---

## Identitas Dokumen

| Field | Nilai |
|---|---|
| Nomor surat | B-231/IJ.3/PW.02.06/07/2025 |
| Tanggal | 25 Juli 2025 |
| Jenis | **Notisi Hasil Penelaahan** (dokumen kritik sistematis) |
| Klasifikasi | **Terbatas** |
| Ditujukan kepada | Sekretaris Ditjen Wasdig; Direktur Pengendalian Ruang Digital |
| Deadline tanggapan | **31 Juli 2025** |
| Penandatangan | Muhammad Arief, Inspektur II |

## Dasar Penugasan

| Item | Referensi |
|---|---|
| Surat Tugas | 127/IJ.3/KP.01.06/07/2025 tgl 1 Juli 2025 |
| Obyek | Tata kelola pengawasan dan pengendalian konten digital Ditjen Wasdig |

## Lanskap Sistem Pemblokiran Konten Negatif

Kemkomdigi saat ini menggunakan **4 sistem pemblokiran paralel**:

| Sistem | Fungsi | Input | Titik Pasang |
|---|---|---|---|
| **RPZ (Response Policy Zone)** | Block domain | Domain dari Trust Positif | ISP |
| **TKPPSE** | Block + tapping FO | Domain & IP | 62 NAP + 89 ISP (151 KOS) |
| **RTBH (Remotely Triggered Black Hole)** | Block IP address | IP Address | 803 ISP |
| **TrustNG** | Block domain & URL | Domain + URL | 132 non-ISP + 803 ISP |

**Proses bisnis**: aduan masyarakat/K-L + patroli siber + CSE crawling → verifikasi → database Trust Positif → pemblokiran via 4 sistem di atas.

## Dua Temuan Utama

### Temuan 1: TKPPSE Tidak Efektif

#### a. Kekurangan Penyediaan Perangkat + Kapasitas

Berdasarkan **LHP Kinerja BPK** — TKPPSE kekurangan infrastruktur:

**Kebutuhan Titik Penyediaan Perangkat**:

| Jenis | Kebutuhan | Tersedia | Kekurangan |
|---|---|---|---|
| NAP | 43 NAP | 26 NAP (26 lokasi) | **17 NAP (39,53%)** |
| ISP | 1.188 ISP | 5 ISP (89 lokasi) | **1.183 ISP (99,58%)** |

**Kebutuhan Kapasitas**:

| Jenis | Kebutuhan | Tersedia | Kekurangan |
|---|---|---|---|
| NAP | 1.570 GB | 600 GB | **970 GB** |
| ISP | 88.500 GB | 47.880 GB | **40.620 GB** |

**Akibat**: traffic jaringan yang melewati NAP/ISP yang belum tercover **tidak dapat dimonitor/dikendalikan** TKPPSE.

#### b. Lisensi TKPPSE Kedaluwarsa

- TKPPSE saat ini pakai **versi 7** dengan **Oracle Enterprise Linux 7** — **kedaluwarsa 31 Desember 2024**.
- Tidak mampu tangani **HTTPS + DNS over HTTPS (DoH)** + browser modern (Chrome, Edge, Firefox).
- Diperlukan **upgrade ke versi 9** untuk menangani akses terenkripsi.

#### c. Efektivitas Pemblokiran Rendah

**Hasil uji BPK** pada situs yang tidak berhasil diblokir oleh RTBH + RPZ:

| Sistem | Tingkat Keberhasilan Pemblokiran |
|---|---|
| RTBH | **81,45%** |
| RPZ | **79,60%** |
| **TKPPSE** | **22,44%** (dari residu RTBH+RPZ) |

**Tidak efektif untuk**: browser modern (enkripsi), VPN, DoH, DNS Public.

### Temuan 2: TKPPSE Tidak Efisien

#### a. Tumpang Tindih CNS (TKPPSE) vs CSE-Rugos

**CNS (Content Netsweeper System)** — komponen crawling TKPPSE:
- Netsweeper real-time pada perangkat TKPPSE.
- **OM: Rp233,74 miliar** (ABT TA 2025).
- Fungsi: deteksi + feedback konten dalam database Trust Positif.

**CSE-Rugos** — sistem crawling terpisah:
- Keyword-based pakai Google API + sistem RUGOS (image capture untuk verifikasi).
- **OM: Rp5,11 miliar** (lihat [[pendampingan-crawling-wasdig-2025]]).
- Aktif sejak akhir Des 2024 dihidupkan kembali TA 2025.

**Redundansi**: Jika CSE dihidupkan → CNS jadi redundant, hanya sebagai feedback → **tidak sepadan dengan Rp233,74M** → inefisiensi anggaran.

**Gap current**: antara data CNS → verifikator masih besar. **3.839.549 URL dari pemeriksaan BPK belum diblokir**. Verifikator (Cyberdrone 9 / CD9) sumber daya terbatas.

#### b. Tumpang Tindih TKPPSE vs RTBH + TrustNG

**RTBH + TrustNG (2024)**: dipasang di 935 titik (803 ISP + 132 non-ISP); estimasi biaya **Rp1,2-1,5 miliar** (relatif murah).

**Database Trust Positif** memuat domain + IP:
- Domain diblokir via RPZ + TrustNG.
- IP diblokir via RTBH.
- **TKPPSE juga blokir domain + IP yang sama** → duplikasi.

**Coverage ISP**:
- RTBH + TrustNG: 803 ISP + 132 non-ISP (100% ISP Indonesia).
- RPZ: **508/1.188 ISP (42,87%)** — sisa 680 ISP belum sinkron dengan Trust Positif.
- TKPPSE: 26 NAP + 5 ISP.

#### c. Penempatan TKPPSE di 89 ISP Redundant dengan NAP

TKPPSE pasang di 62 NAP + 89 ISP (151 KOS). Menurut LHP Kinerja BPK:
- **NAP adalah titik krusial** (internet domestik ↔ internet global).
- **89 ISP TKPPSE** tercakup di traffic NAP yang sama → redundant.
- **Menurut Juknis TKPPSE**: perangkat seharusnya di level ISP — tapi banyak dipasang di level NAP (kontradiksi).

#### d. Risiko Inefisiensi Belanja OM TKPPSE

**ABT 2025 Rp233,74 miliar untuk OM TKPPSE** — Itjen menilai tidak sepadan dengan efektivitas 22,44%:
- Infrastruktur pendukung belum memadai.
- Kapasitas ISP tidak cukup.
- **Potensi kewajiban pembayaran kemudian hari** seperti yang terjadi 2024 ([[lha-om-tkppse-2024]] Rp78,56M piutang macet, hanya 50% dapat diyakini).

## 5 Rekomendasi ke Ditjen Wasdig

1. **Pemetaan ulang titik TKPPSE** mempertimbangkan keberadaan 935 titik RTBH + TrustNG untuk mencegah tumpang tindih.
2. Jika hasil pemetaan tunjukkan overlap, **relokasi** titik TKPPSE ke wilayah belum tercakup sistem lain.
3. **Relokasi seluruh 89 perangkat TKPPSE di ISP ke NAP** yang belum terpasang.
4. **Fokuskan OM TKPPSE pada titik NAP**. Untuk ISP, pertimbangkan kembali OM sebelum relokasi ke NAP.
5. **Tunda pengadaan perangkat baru + upgrade lisensi TKPPSE** sampai kajian pemetaan + analisis kebutuhan selesai.

## Residu & Risiko

1. **Aset BMN TKPPSE Rp1.591.221.659.249 idle** jika TKPPSE dihentikan karena keterbatasan anggaran.
2. Risiko pembongkaran (dismantle) alat TKPPSE jika dihentikan sementara tahun ini.
3. Waktu takedown lebih lama jika TKPPSE tidak dilanjutkan.
4. **CSE tidak bisa peremajaan jika IPP PNBP belum disetujui** (lihat [[chr-ipp-pnbp-wasdig-2025-2028]]) → crawling tidak optimal.
5. Tidak bisa blokir konten karena DoH + DNS Public + VPN → perlu kebijakan baru.

## Konteks: Rangkaian Dokumen OM TKPPSE

Notisi ini adalah **dokumen terkuat secara analitis** yang mempertanyakan keberlanjutan TKPPSE:

| Dokumen | Fokus | Kesimpulan |
|---|---|---|
| [[pendampingan-om-tkppse-2024]] (Feb 2025) | Akuntabilitas tagihan OM 2024 Rp78,56M tanpa kontrak | 6 bukti belum memadai |
| [[dha-tahap2-om-tkppse-2024]] (Mar 2025) | Prestasi kerja OM 2024 | 29% diyakini |
| [[lha-om-tkppse-2024]] (Apr 2025) | Final audit OM 2024 | **50% diyakini**, 50% belum dinilai; Legal Opinion Biro Hukum |
| [[atensi-pemutusan-tkppse-2025]] (Mei 2025) | Rencana pemutusan PJT akhir Mei | Kapasitas turun 33% → risiko 59% |
| **Notisi ini (Jul 2025)** | **Efektivitas + efisiensi TKPPSE** | **Efektivitas 22,44% + tumpang tindih + Rp1,59T aset BMN idle** |
| [[lhp-pengadaan-redesain-tkppse-2026]] (Jan 2026) | Redesain TKPPSE TA 2026 | 6 PJT belum berkontrak |

**Eskalasi logis**: dari masalah administrasi (kontrak) → kuantifikasi kualitas layanan → krisis operasional → **pertanyaan keberlanjutan sistem secara keseluruhan**.

Notisi ini membuka kemungkinan bahwa **TKPPSE harus dihentikan atau diredesain total**, dengan implikasi:
- **Penghentian permanen**: Rp1,59T aset BMN idle → masalah akuntansi + inefisiensi.
- **Penghentian sementara**: perangkat dibongkar → risiko waktu takedown konten negatif lebih lama.
- **Redesain**: kajian teknis redesain TKPPSE dikaji TA 2026, eksekusi TA 2027 (lihat [[lhp-pengadaan-redesain-tkppse-2026]]).

## Data Penyediaan TKPPSE 2021-2022

| Tahun | Kontrak | Nilai |
|---|---|---|
| 2021 | PT LTI + PT Eltrans | Rp963.122.600.000 |
| 2022 | PT Eltrans (P3KJT) | Rp827.857.609.593 |
| **Total** | | **Rp1.790.980.209.593** |

Aset BMN TKPPSE dihitung **Rp1.591.221.659.249** (≈Rp1,59T) — mendekati nilai pengadaan awal setelah depresiasi. Jika TKPPSE dihentikan, seluruh nilai ini jadi idle.

## Related pages

- [[tkppse]]
- [[pendampingan-om-tkppse-2024]]
- [[dha-tahap2-om-tkppse-2024]]
- [[lha-om-tkppse-2024]]
- [[atensi-pemutusan-tkppse-2025]]
- [[pendampingan-crawling-wasdig-2025]]
- [[chr-ipp-pnbp-wasdig-2025-2028]]
- [[lhp-pengadaan-redesain-tkppse-2026]]
- [[inspektorat-ii]]
