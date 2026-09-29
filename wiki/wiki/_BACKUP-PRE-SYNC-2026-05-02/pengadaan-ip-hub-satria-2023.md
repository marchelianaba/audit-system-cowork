# Pengadaan IP HUB SATRIA-1 TA 2023

**Summary**: Pengadaan 5 paket Perangkat Hub untuk mendukung Proyek SATRIA-1 oleh [[bakti]] pada TA 2023; total kontrak Rp807,69M; 4 paket oleh PT PSN (HNS) di Batam/Pontianak/Tarakan/Manado dan 1 paket oleh KBISA (iDirect) di Jayapura. Pengadaan ini diperiksa BPK (indikasi pemborosan Rp216,86M) dan ditindaklanjuti oleh Inspektorat II via [[adtt-ip-hub-bakti-2025]].

**Sources**: 15 IJ.3 PW.04.02 surat keluar 16.01.25 (ADTT IP HUB BAKTI)

**Last updated**: 2026-04-22

---

## Gambaran Umum

IP HUB (Internet Protocol Hub) adalah perangkat ground segment yang menghubungkan jaringan satelit SATRIA-1 dengan infrastruktur internet terestrial. Setiap IP HUB memiliki kapasitas tertentu (Gbps) dan memerlukan konfigurasi di lokasi gateway. SATRIA-1 sendiri adalah satelit multifungsi pemerintah Indonesia, beroperasi mulai awal 2024.

## Kontrak

| Lokasi | Kapasitas | Penyedia | Pabrikan | Lokasi Prinsipal | Nilai SP2D |
|---|---|---|---|---|---|
| Batam | 15 Gbps (10+5) | PT PSN | HNS | Amerika Serikat | Rp173.329.000.000 |
| Pontianak | 14 Gbps (10+4) | PT PSN | HNS | Amerika Serikat | Rp162.584.000.000 |
| Tarakan | 14 Gbps (10+4) | PT PSN | HNS | Amerika Serikat | Rp162.584.000.000 |
| Manado | 15 Gbps (10+5) | PT PSN | HNS | Amerika Serikat | Rp173.329.000.000 |
| Jayapura | 9 Gbps (7+2) | KBISA | iDirect/ID | Belgia | Rp135.865.260.000 |
| **Total** | **67 Gbps** | | | | **Rp807.691.260.000** |

Metode: e-purchasing via e-Katalog LKPP. Kontrak ditandatangani Oktober/November 2023 dengan target penyediaan terpasang & terintegrasi paling lambat **31 Desember 2023**.

(source: 15 IJ.3 PW.04.02 surat keluar 16.01.25)

## Pemilihan Penyedia

BAKTI mengirim Surat Permohonan RFI (Request for Information) pada 13 Oktober 2023 kepada **9 calon penyedia**:

| No | Calon Penyedia | Merk Ditawarkan | Sanggup ≤31 Des 2023? |
|---|---|---|---|
| 1 | PT Pasifik Satelit Nusantara | HNS | ✓ (15 Des 2023) |
| 2 | PT Abhimata Citra Abadi | HNS | ✗ (TA 2024) |
| 3 | PT Bis Data Indonesia (KBISA) | iDirect | ✓ (17 Des 2023) |
| 4 | PT Dwi Tunggal Putra | HNS | ✗ (TA 2024) |
| 5 | PT Halik Selindo Alpha | HNS | ✗ (TA 2024) |
| 6 | PT Kurongkor Utama | GILAT | ✗ (8 Mar 2024) |
| 7 | PT Primacom Interbuana | HNS/GILAT | ✗ (191 hari) |
| 8 | PT Tele Net | GILAT | ✓ (20 Des 2023) |
| 9 | PT Transtel Universal | GILAT | ✓ (15 Des 2023) |

**Hasil seleksi**: PT PSN dan KBISA dipilih.

**Pertimbangan eliminasi**:
- 5 penyedia gugur karena tidak sanggup menyediakan sebelum 31 Des 2023.
- 3 penyedia merk GILAT (Transtel Universal, Kurongkor Utama, Telenet) gugur karena prinsipal di Israel — negara tanpa hubungan diplomatik dengan Indonesia (risiko OM/penggantian perangkat rusak terganggu).

PT PSN dan KBISA menempati harga penawaran **terbaik 2 dari 9** penyedia (bukan terendah — selisih Rp41,5M dari penawaran terendah).

(source: 15 IJ.3 PW.04.02 surat keluar 16.01.25)

## Komponen Pembentuk Harga (per Pasal 21 ayat 2 Surat Pesanan)

a. Keuntungan
b. Pajak (termasuk PPN)
c. Biaya overhead
d. Biaya asuransi
e. Biaya Jaminan Pelaksanaan
f. Penyediaan Perangkat IP Hub
g. Inspeksi Pabrikan
h. Pengiriman Perangkat IP Hub
i. Pemasangan Perangkat IP Hub
j. Pengujian di Lokasi
k. Integrasi
l. Pelatihan
m. Garansi
n. Pertanggungan risiko atas Perangkat IP Hub

Seluruh komponen dibayar **lump sum** sesuai harga kontrak, berdasarkan Berita Acara Serah Terima.

## Dashboard OSS NADIA (Khusus Jayapura/KBISA)

KBISA mengembangkan aplikasi **NADIA** (Network Analysis, Diagnostic, Integration, and Administration) sebagai OSS Dashboard. Modul:
1. **Dashboard** — kapasitas internet/satelit, uptime, cuaca gateway, peta reference terminal, status RTGS-AI/RT/Beam
2. **Pemantauan Real Time** — monitoring perangkat IPCN, status perangkat IP HUB
3. **Basis Pengetahuan** — artikel proyek infrastruktur BAKTI
4. **Pengaturan** — akun, pengguna, role, general
5. **Catatan Rilis** — versi 1.0 rilis 31 Des 2023

Beberapa fitur (Kapasitas Internet, Uptime, Status RTGS-AI, dll.) berstatus *Not Available* saat BAST karena (a) IP Transit Jayapura baru ditandatangani 22 Okt 2024 dan (b) integrasi dengan dashboard Satria-1 tidak masuk dalam Program Mutu KBISA.

## Indikasi Permasalahan dan Tindak Lanjut

LHP BPK RI atas LK Kominfo TA 2023 menyoroti **5 area** (lihat detail di [[adtt-ip-hub-bakti-2025]]):

1. Proses pengadaan tidak sesuai ketentuan (penetapan oleh PA, harga e-Katalog serentak, harga PT PSN/KBISA bukan terendah).
2. Harga pengadaan tidak dapat diverifikasi memadai (selisih ~Rp217M antara nilai kontrak dan komponen pengeluaran tervalidasi).
3. OSS Dashboard belum berfungsi penuh (133 hari keterlambatan menurut BPK).
4. Pelatihan tidak sesuai KAK (2 hari vs minimal 5 hari).
5. PPN tidak dipungut Rp80,04M.

**Hasil ADTT Itjen**:
- Tidak ditemukan pemborosan; pemilihan penyedia wajar; OSS NADIA sesuai Program Mutu.
- 2 temuan: pelatihan kurang hari (pengembalian Rp4,125M) + PPN tidak dipungut (koreksi administrasi).

## Related pages

- [[bakti]]
- [[adtt-ip-hub-bakti-2025]]
- [[lhe-rb-bakti-tw4-2024]]
- [[lhr-lkj-itjen-2024]]
- [[pedoman-pengawasan-buku-iii]]
