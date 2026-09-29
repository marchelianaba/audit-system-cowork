# LHP Pengadaan dan Redesain TKPPSE TA 2026

**Summary**: Laporan Hasil Pemantauan atas pengadaan dan redesain TKPPSE TA 2026 oleh [[inspektorat-ii]]; menemukan kajian teknis belum diimplementasikan dan 6 PJT belum berkontrak — termasuk 2 PJT (Moratel dan Lintasarta) dengan kendala teknis dan legalitas signifikan.

**Sources**: 34 IJ.3 PW.04.03 surat keluar 30.01.2026 ND Laporan Monitoring atas Pengadaan dan Redesain TKPPSE TA 2026.pdf

**Last updated**: 2026-04-17

---

## Identitas Dokumen

| Field | Nilai |
|---|---|
| Nomor surat | B-34/IJ.3/PW.04.03/01/2026 |
| Tanggal | 30 Januari 2026 |
| Jenis | Laporan Hasil Pemantauan (LHP) |
| Ditujukan kepada | Direktur Pengendalian Ruang Digital, Ditjen Wasdig |
| Pelaksana | [[inspektorat-ii]] |

## Gambaran Umum TKPPSE

TKPPSE (Tata Kelola Pengendalian Penyelenggara Sistem Elektronik) memiliki fungsi utama memutus akses secara langsung ketika pengguna internet mengakses konten yang dilarang. Mekanisme: **TCP Reset** — mengakhiri koneksi TCP secara tiba-tiba. Sistem ini dipasang di lokasi-lokasi PJT (Penyedia Jasa Telekomunikasi) di seluruh Indonesia. (source: 34 IJ.3 PW.04.03 surat keluar 30.01.2026)

## Temuan 1 — Hasil Kajian Teknis TKPPSE Belum Diimplementasikan

Ditjen Wasdig telah melakukan kajian teknis tentang teknologi mutakhir dan optimalisasi infrastruktur TKPPSE, namun hasilnya belum diimplementasikan. Rekomendasi dari kajian teknis meliputi:

- Perlunya analisa teknis adaptif secara berkala mengikuti pertumbuhan protokol internet yang makin *secure* dan *private*
- Sebelum implementasi opsi teknis baru, perlu dasar regulasi yang menyeluruh dan disepakati pemangku kepentingan skala nasional
- Proyeksi pertumbuhan trafik nasional 5 tahun ke depan tidak bisa langsung dipakai untuk menghitung kebutuhan perangkat TKPPSE (karena perangkat mengikuti jumlah koneksi fisik, bukan volume trafik)
- Perlu pengukuran kuantitatif skala implementasi di PJT dan analisa teknis hasil pemutusan trafik
- Perlu verifikasi berkala kebutuhan koneksi internasional
- Perlu peninjauan lokasi DC dan KOS pasca merger operator seluler menjadi 3 perusahaan: **IOH, XLSmart, dan Telkomsel**
- Trafik CDN memerlukan kolaborasi dengan CDN provider; trafik domestik perlu dipertimbangkan untuk penempatan TKPPSE

**Rencana redesain**: Kajian komprehensif pada TW II 2026, selesai paling cepat Agustus. Eksekusi redesain pada TA 2027. Dismantle dan relokasi perangkat dapat dilakukan tahun ini setelah kajian selesai. (source: 34 IJ.3 PW.04.03 surat keluar 30.01.2026)

## Temuan 2 — 6 PJT Belum Berkontrak per 26 Januari 2026

Pada tahun 2025 terdapat 16 PJT yang berkontrak, namun tidak semua lanjut ke 2026.

**PJT Terkontrak TA 2026** (6 PJT via INAPROC):
Indosat, Telkomsel, XLSmart, Telkom, Telkomsat, Kreatif Pacific

**PJT Belum Terkontrak** (6 PJT):

| PJT | Jenis Kendala | Detail |
|---|---|---|
| PT NTT | Administratif + Status NAP | Email korporat vs. persyaratan email pribadi INAPROC; ada perbedaan info status perpanjangan NAP |
| PT Trans Hybrid Communication | Teknis | Kendala layanan teknis |
| PT Dinamika | Lokasi | Lokasi DC disewa oleh PT SUFI |
| **[[vendor-moratel\|PT Mora Telematika (Moratel)]]** | **Teknis signifikan** | Perubahan topologi jaringan terenkripsi — perangkat TKPPSE tidak dapat membaca trafik; usulan pindah ke BDx masih dikaji dari sisi legalitas dan SOP |
| **[[vendor-lintasarta\|PT Lintasarta]] + iForte** | **Legalitas signifikan** | Lokasi DC berkontrak dengan PT SUFI — ada batasan kerahasiaan (*confidentiality*) yang membatasi akses data |

(source: 34 IJ.3 PW.04.03 surat keluar 30.01.2026)

## Rekomendasi

1. Tindaklanjuti hasil kajian teknis TKPPSE dengan rencana aksi tahun 2026.
2. Buat checklist untuk memastikan keberlanjutan kontrak Lintasarta dan iForte, termasuk kemungkinan pengambilalihan lokasi DC dari SUFI.
3. Lakukan *Cost-Benefit Analysis* atas opsi-opsi penyelesaian masalah di PT Moratel.
4. Susun timeline untuk menyelesaikan masalah PJT yang belum berkontrak di 2026.
5. Buat roadmap TKPPSE 5 tahun hingga akhir Renstra.

(source: 34 IJ.3 PW.04.03 surat keluar 30.01.2026)

## Konteks

Kendala Moratel (topologi terenkripsi) merupakan tantangan teknis mendasar — jika TCP Reset tidak dapat membaca trafik, fungsi TKPPSE di lokasi tersebut tidak berjalan. Konteks ini relevan untuk memahami keterbatasan cakupan sistem pemblokiran konten yang dilaporkan dalam [[lhp-pengadaan-program-prioritas-wasdig-2026]] dan [[lha-om-tkppse-2025]].

## Related pages

- [[inspektorat-ii]]
- [[lha-om-tkppse-2025]]
- [[lhp-pengadaan-program-prioritas-wasdig-2026]]
- [[lhr-lkj-wasdig-2025]]
- [[peta-risiko-wasdig-2026]]
