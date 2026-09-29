# Pemantauan ISU dan Risiko — Trello Tim Ekodig

**Summary**: Mekanisme baru pemantauan isu/risiko Inspektorat II — disepakati di rapat WFH 24 April 2026. Tiap entitas/satker binaan diregister sebagai card Trello pada list "Pemantauan ISU dan Risiko", diperbarui mingguan oleh penanggung jawab, lalu direkap sebagai bahan Rapim. Total **12 card terdaftar dengan prioritas Tinggi/Sedang**: 7 Tinggi, 5 Sedang. Card memuat 4 sub-kolom standar: (1) Isu/Risiko, (2) Kegiatan Pengawasan, (3) Progres Mitigasi, (4) Rencana Aksi.

**Sources**: `raw/Laporan WFH Tim Irfan-24 April 2026-1.pdf` Section C

**Last updated**: 2026-04-26

---

## Mekanisme Reporting

Disepakati pada rapat tim WFH 24 April 2026 oleh Tim Ekodig Inspektorat II:

1. **Setiap satker/entitas binaan = 1 card Trello** di list "Pemantauan ISU dan Risiko" pada board Tim Ekodig.
2. **Pembaruan mingguan** oleh masing-masing penanggung jawab.
3. **Setiap card berisi 4 sub-kolom standar:**
   - Isu/Risiko teridentifikasi
   - Kegiatan Pengawasan yang dilakukan
   - Progres Mitigasi/Penyelesaian
   - Rencana Aksi
4. **Rekapitulasi mingguan** menjadi bahan Rapim.
5. **Prioritas:** Tinggi (perlu intervensi cepat) atau Sedang (perlu pemantauan rutin).

Status implementasi (per 26 Apr 2026): **12 card sudah ter-register dengan label prioritas; uraian Isu/Progres/Rencana Aksi belum diisi penanggung jawab masing-masing — target pengisian: minggu berjalan.**

## 12 Card Pemantauan ISU dan Risiko

### Kelompok Wasdig (4 card)

| # | Entitas | Prioritas | Item Dipantau (Checklist) |
|--:|---|---|---|
| 1 | **TKPPSE** | 🟡 Sedang | (a) Pengadaan 2026; (b) Pengadaan 2025; (c) Redesain; (d) TLHP Kinerja BPK; (e) TLHP LK BPK; (f) Inventarisasi Aset |
| 2 | **CSE** | 🔴 **Tinggi** | (a) Pengadaan Server 2026; (b) Tumpang Tindih CNS dan CSE; (c) TLHP BPK 2025 |
| 3 | **PSE dan PSrE** | 🟡 Sedang | (a) Pengadaan PSrE; (b) Wikimedia; (c) Magdalene.co (Pers) |
| 4 | **PANDI** | 🟡 Sedang | (a) TLHP Jamintel |

### Kelompok Ekosdig (6 card)

| # | Entitas | Prioritas | Item Dipantau (Checklist) |
|--:|---|---|---|
| 5 | **DBS** | 🟡 Sedang | (a) Alih Status; (b) Pembatalan Tender |
| 6 | **Garuda Spark** | 🔴 **Tinggi** | (a) Pengadaan; (b) Tata Kelola |
| 7 | **Bantuan IoT** | 🟡 Sedang | (a) Pengadaan |
| 8 | **PSO POS** | 🔴 **Tinggi** | (a) TLHP BPKH 2025; (b) Akuntabilitas Belanja 2026 |
| 9 | **IGRS** | 🔴 **Tinggi** | (a) Tata Kelola dan Kinerja |
| 10 | **Perangkat QOS** | 🔴 **Tinggi** | (a) Pengadaan |

### Kelompok Kementerian (2 card)

| # | Entitas | Prioritas | Item Dipantau (Checklist) |
|--:|---|---|---|
| 11 | **SAKIP** | 🔴 **Tinggi** | (a) Pemenuhan AoI; (b) Progres Pengisian 2026 |
| 12 | **SPIP** | 🔴 **Tinggi** | (a) Pemenuhan AoI; (b) Progres Pengisian 2026 |

## Rekapitulasi Prioritas

| Prioritas | Jumlah | Card |
|---|--:|---|
| 🔴 Tinggi | **7** | CSE, Garuda Spark, PSO POS, IGRS, Perangkat QOS, SAKIP, SPIP |
| 🟡 Sedang | **5** | TKPPSE, PSE dan PSrE, PANDI, DBS, Bantuan IoT |
| **Total** | **12** | |

## Pemetaan ke Wiki Existing

Setiap card di Trello ada padanan wiki page-nya untuk detail teknis:

| Card Trello | Wiki Page Detail |
|---|---|
| TKPPSE | [[lha-om-tkppse-2025]], [[lhp-pengadaan-redesain-tkppse-2026]] |
| CSE | [[lhr-server-crawling-2025]] |
| PSE dan PSrE | [[lhr-kontrak-aptika-2025]] (untuk PSrE) |
| PANDI | (belum ada wiki khusus) |
| DBS | [[isu-dbs]] |
| Garuda Spark | (belum ada wiki khusus) |
| Bantuan IoT | (belum ada wiki khusus) |
| PSO POS | (belum ada wiki khusus) |
| IGRS | [[igrs]], [[isu-igrs]], [[regulasi-igrs]], [[rekomendasi-igrs]], [[audit-kinerja-layanan-klasifikasi-gim]] |
| Perangkat QOS | (belum ada wiki khusus) |
| SAKIP | [[framework-evaluasi-sakip]] |
| SPIP | [[framework-evaluasi-spip]], [[asistensi-spip-wasdig-2025]], [[penjaminan-kualitas-spip-itjen-2025]] |

## Implikasi untuk Dashboard

Mekanisme Trello ini menggantikan tracking ad-hoc sebelumnya. Implikasi struktur dashboard:

1. **Heatmap risiko & Risk Aging** harus konsisten dengan 12 card ini sebagai sumber tunggal kebenaran (single source of truth).
2. **Top 5 Prioritas Minggu Ini** sebaiknya pakai card berlabel 🔴 Tinggi yang memiliki tenggat eksternal terdekat.
3. **Decisions Pending** sebaiknya menyebutkan "card Trello mana" supaya akuntabilitas kelihatan.
4. **Update mingguan dashboard** sinkron dengan update mingguan Trello — keduanya sama dasar datanya, hanya bentuk tampil berbeda.

## Tindak Lanjut Operasional

| # | Aksi | Target Waktu | PIC |
|---|---|---|---|
| 1 | Isi uraian Isu/Risiko, Progress, Rencana Aksi pada masing-masing card | Minggu berjalan (sd 30 Apr) | Penanggung jawab tiap card |
| 2 | Akses file SAKTI yang sebelumnya tidak dapat diakses | Segera | Tim Audit AI |
| 3 | Sampel RKKL tambahan untuk TOR RAB Audit AI | Segera | Tim Audit AI |
| 4 | Realisasi akses OneDrive untuk sinkronisasi data audit | Bulan depan (Mei 2026) | Tim Sekretariat / IT |
| 5 | Upload ke Wiki: dokumen Desember, struktur organisasi, pagu, indikator, PKPT 2026 | Segera | Tim Wiki |
| 6 | Perpanjangan Surat Tugas Reviu Renja | Segera (kickoff baru 24 Apr) | Sekretariat |

## Related Pages

- [[dashboard]] — dashboard Inspektorat II yang menampilkan ringkasan
- [[inspektorat-ii]] — overview unit
- [[paparan-rapim-inspektorat-ii-17-april-2026]] — basis prioritas isu sebelumnya
- [[pkpt-2026]] — penugasan terjadwal yang merekam isu-isu di card
- [[tlhp-internal-simwas-ir2]] — TLHP yang muncul di banyak item card (TLHP BPK, TLHP Jamintel, dll)
- [[peta-risiko-wasdig-2026]], [[peta-risiko-ekosistem-digital-2026]] — peta risiko struktural
- [[isu-igrs]], [[isu-dbs]] — isu prioritas Tinggi
- [[framework-evaluasi-sakip]], [[framework-evaluasi-spip]] — kerangka evaluasi untuk card SAKIP/SPIP
