# Laporan Final Hasil Penelaahan Tata Kelola Pengendalian Konten Negatif

**Summary**: **Versi final/laporan** dari penelaahan tata kelola TKPPSE yang sebelumnya diterbitkan sebagai **Notisi** B-231 (25 Juli 2025). Substansi identik: efektivitas TKPPSE 22,44% vs RTBH 81,45%, RPZ 79,6%; kekurangan 17 NAP + 1.183 ISP + 40,6 TB kapasitas; lisensi kedaluwarsa; tumpang tindih sistem crawling + pemblokiran; aset BMN Rp1,59T terancam idle. 5 rekomendasi dan 5 residu/risiko. Perubahan minor: "TrustNG" → "**DNS TrustNG**" (penambahan kata "DNS").

**Sources**: 264 IJ.3 PW.02.06 surat keluar 29.08.2025 Nodin Laporan Hasil Penelaahan Tata Kelola Pengendalian Konten Negatif.pdf

**Last updated**: 2026-04-22

---

## Identitas Dokumen

| Field | Nilai |
|---|---|
| Nomor surat | B-264/IJ.3/PW.02.06/08/2025 |
| Tanggal | 29 Agustus 2025 |
| Jenis | **Laporan Hasil Penelaahan** (dokumen final) |
| Klasifikasi | **Terbatas** |
| Ditujukan kepada | Sekretaris Ditjen Pengawasan Ruang Digital; Direktur Pengendalian Ruang Digital |
| Surat Tugas | 127/IJ.3/KP.01.06/07/2025 tgl 1 Juli 2025 (**SAMA** dengan B-231) |
| Penandatangan | Muhammad Arief, Inspektur II |

## Relasi dengan Notisi B-231 (25 Juli 2025)

Dokumen ini adalah **versi final** dari [[notisi-tata-kelola-konten-negatif-2025]] (B-231):

| Aspek | B-231 (25 Jul 2025) | **B-264 (29 Agu 2025)** |
|---|---|---|
| Jenis | **Notisi** (penelaahan awal) | **Laporan Hasil Penelaahan** (final) |
| Deadline tanggapan | 31 Juli 2025 (eksplisit) | Tidak ada (final) |
| Nama sistem | "TrustNG" | "**DNS TrustNG**" (lebih akurat) |
| Substansi | Efektivitas 22,44%, 5 rekomendasi, 5 residu/risiko | **Sama persis** |
| Klasifikasi | Terbatas | Terbatas |

Jalur siklus: **Notisi → Tanggapan → Laporan Final** — standar AAIPI untuk penelaahan governance. B-264 menunjukkan bahwa **tanggapan 31 Juli 2025 tidak mengubah substansi temuan** — Itjen II tetap dengan simpulan awalnya.

## Substansi (Identik dengan B-231)

Lihat [[notisi-tata-kelola-konten-negatif-2025]] untuk detail lengkap. Ringkasan kritis:

**Efektivitas TKPPSE hanya 22,44%** (dari LHP Kinerja BPK) vs:
- RTBH: 81,45%
- RPZ: 79,60%

**Kekurangan infrastruktur**:
- 17 NAP (dari kebutuhan 43 — kurang 39,53%).
- 1.183 ISP (dari kebutuhan 1.188 — kurang 99,58%).
- Kapasitas NAP: kurang 970 GB.
- Kapasitas ISP: kurang 40.620 GB.

**Lisensi kedaluwarsa**: Oracle Enterprise Linux 7 expired 31 Desember 2024.

**Tumpang tindih**:
- **CNS (TKPPSE) vs CSE-Rugos** — OM Rp233,74M vs Rp5,11M.
- **TKPPSE vs RTBH + DNS TrustNG + RPZ** — pemblokiran domain/IP.
- **89 ISP TKPPSE redundant** dengan tapping NAP.

**Aset BMN Rp1.591.221.659.249 terancam idle**.

## 5 Rekomendasi (Sama dengan B-231)

1. Pemetaan ulang titik TKPPSE mempertimbangkan RTBH + **DNS TrustNG**.
2. Relokasi titik TKPPSE yang tumpang tindih.
3. Relokasi seluruh 89 perangkat TKPPSE di ISP ke NAP.
4. Fokuskan OM TKPPSE pada titik NAP.
5. **Tunda pengadaan perangkat baru + upgrade lisensi TKPPSE** sampai kajian pemetaan selesai.

## 4 Residu & Risiko (dari 5 di B-231)

B-264 memiliki **4 residu/risiko** (bukan 5 di B-231):
1. Aset BMN Rp1,59T idle jika TKPPSE dihentikan.
2. Risiko pembongkaran/dismantle jika TKPPSE dihentikan sementara.
3. Waktu takedown lebih lama jika TKPPSE tidak dilanjutkan.
4. Tidak dapat diblokirnya konten negatif karena DoH + DNS Public + VPN.

**Risiko yang hilang di B-264**: "CSE tidak dapat peremajaan jika IPP PNBP belum disetujui" — kemungkinan karena [[chr-ipp-pnbp-wasdig-2025-2028]] (25 Juli 2025) sudah ditindaklanjuti.

## Konteks

Dokumen ini menandai **finalisasi formal kritik tata kelola TKPPSE oleh Itjen II**. Setelah B-264, tidak ada revisi substantif — temuan Notisi 25 Juli 2025 menjadi **posisi resmi Inspektorat**.

Implikasi:
- Ditjen Wasdig harus menindaklanjuti 5 rekomendasi ini — terutama **menunda pengadaan perangkat baru + upgrade lisensi** — meskipun sudah ada IPP PNBP Rp1,28T untuk OM TKPPSE 2025-2028 ([[chr-ipp-pnbp-wasdig-2025-2028]]).
- Aset BMN Rp1,59T tetap jadi **risiko idle** jika keputusan strategis redesain/penghentian TKPPSE diambil.
- [[lhp-pengadaan-redesain-tkppse-2026]] (Jan 2026) menindaklanjuti dengan rencana redesain TKPPSE TA 2027 — memberi waktu 1,5 tahun transisi.

## Related pages

- [[notisi-tata-kelola-konten-negatif-2025]]
- [[tkppse]]
- [[chr-ipp-pnbp-wasdig-2025-2028]]
- [[atensi-pemutusan-tkppse-2025]]
- [[lha-om-tkppse-2024]]
- [[lhp-pengadaan-redesain-tkppse-2026]]
- [[inspektorat-ii]]
