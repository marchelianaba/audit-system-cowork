# Surat BPKP — Pelimpahan Audit OM TKPPSE 2025 ke Itjen II

**Summary**: Surat resmi dari **Direktorat Pengawasan Bidang Pertahanan dan Keamanan BPKP** (Nomor PE.04.01/S-128/D201/2/2026 tanggal 22 April 2026) yang **menolak permohonan audit OM TKPPSE periode Januari s.d. Desember 2025** dengan alasan: setelah ekspose dan pembahasan lanjutan, **nilai tagihan tiap Penyedia Jasa Telekomunikasi (PJT) berada di bawah Rp 2 miliar** setelah penyesuaian SLA. Karena di bawah threshold BPKP, audit dilimpahkan kembali ke Inspektorat Jenderal Komdigi untuk ditelaah dan dilanjutkan. **Dampak besar:** mengubah status temuan di [[lha-om-tkppse-2025]] yang sebelumnya "Menunggu hasil audit BPKP" — sekarang Itjen II yang harus mengaudit sendiri atau menyesuaikan kesimpulan.

**Sources**: `raw/Surat Jawaban Permintaan Audit TKPPSE_signed-1.pdf` (Nomor PE.04.01/S-128/D201/2/2026, 22 April 2026, ditandatangani Setia Pria Husada — Direktur Pengawasan Bidang Pertahanan dan Keamanan BPKP)

**Last updated**: 2026-04-26

---

## Identitas Dokumen

| Field | Nilai |
|---|---|
| Nomor surat | PE.04.01/S-128/D201/2/2026 |
| Tanggal | 22 April 2026 |
| Penerbit | Direktorat Pengawasan Bidang Pertahanan dan Keamanan BPKP |
| Penandatangan | Setia Pria Husada (Direktur) |
| Penerima | Inspektur Wilayah II, Kementerian Komunikasi dan Digital RI |
| Tembusan | Deputi Polkamhum PMK BPKP; Inspektur Jenderal Komdigi; Dirjen Wasdig |
| Surat induk yang dibalas | Surat Dirjen Wasdig 45/DJPRD/KU.01.02/01/2026 (19 Januari 2026) |
| Hasil ekspose | 19 Februari 2026 (DJPRD + Itjen Komdigi) |

## Inti Putusan

> "Berdasarkan hasil ekspose dan rangkaian pembahasan lanjutannya, **diperoleh informasi bahwa nilai tagihan yang diyakini menjadi lingkup pembayaran pada masing-masing Penyedia Jasa Telekomunikasi berada di bawah dua miliar**, setelah dilakukan penyesuaian (pengujian/pemeriksaan) SLA (Service Level Agreement) lebih lanjut oleh Direktorat Jenderal Pengawasan Ruang Digital dan Inspektorat Jenderal Komdigi. Sehubungan dengan hal tersebut, dapat kami sampaikan bahwa **Permohonan Audit dapat ditelaah dan dilanjutkan oleh Inspektorat Jenderal Komdigi**."

## Implikasi pada Temuan TKPPSE

### Sebelum Surat Ini

Di [[lha-om-tkppse-2025]] (B-51/IJ.3/PW.04.01/02/2026):

| Temuan | Nilai (Rp) | Status sebelum 22 Apr |
|---|---:|---|
| Tagihan melebihi bukti — PT Telkom & Moratel | 36.851.550 | 🟡 **Menunggu hasil audit BPKP** |
| Tagihan PT Telkom & Moratel >Rp 2M (yang besar) | (lebih dari Rp 2M) | 🟡 Menunggu BPKP |

Asumsi waktu itu: BPKP akan mengaudit nilai >Rp 2M, Itjen II tunggu dan lanjut sesuai kesimpulan BPKP.

### Setelah Surat Ini (22 Apr 2026)

Asumsi tersebut **batal**. Dampak konkret:

1. **Tidak akan ada audit BPKP** atas tagihan TKPPSE 2025. BPKP melepas tanggung jawab karena setelah penyesuaian SLA, nilai per PJT < Rp 2 M (di bawah threshold BPKP).
2. **Itjen II harus mengeksekusi audit sendiri** — atau memutuskan menyesuaikan kesimpulan tanpa audit ulang.
3. **Status temuan harus di-update**: dari "Menunggu BPKP" → "Pelimpahan ke Itjen II" → keputusan internal Itjen apakah audit lanjutan diperlukan.

### Pertanyaan Strategis untuk Itjen II

1. **Apakah perlu audit ulang Itjen II atas tagihan TKPPSE 2025?**
   - Pro: konsistensi dengan rekomendasi BPK terkait (Rp 16,56 M verifikasi yang [[tlrhp-bpk-semester-2-2025|masih Belum Sesuai]]).
   - Con: nilai sudah di bawah threshold materialitas (per PJT), mungkin proporsionalitas tidak sepadan biaya audit.

2. **Bagaimana respons di [[tlhp-internal-simwas-ir2|SIMWAS]]?**
   - 2 rekomendasi B-51/2026 saat ini "Belum Ditindaklanjuti" (No.1-2). Status pelimpahan dari BPKP harus dicatat di SIMWAS sebagai konteks.

3. **Apakah relasi dengan Audit November 2026 (verifikasi pembayaran OM TKPPSE 2024 Rp 16 M)?**
   - Audit November adalah rekomendasi BPK No.12 LK 2024 — terpisah dari periode 2025. Tapi metodologi & temuan akan saling-pengaruh.

## Konteks SLA yang Disebut

Surat menyebut "penyesuaian (pengujian/pemeriksaan) SLA". Ini terkait temuan SLA di B-51/2026:
- "SLA di bawah minimum 99,5%" senilai Rp 842.024.701 (tahap 3)
- Setelah penyesuaian SLA, sebagian tagihan dipotong → nilai per PJT turun di bawah Rp 2 M
- Ini berarti **mekanisme SLA-adjustment sudah dijalankan** oleh DJPRD + Itjen Komdigi — proses tidak macet, hanya hasil akhirnya nilai material kecil per PJT.

## Implikasi untuk Card Trello TKPPSE & Dashboard

Card TKPPSE di [[pemantauan-isu-risiko-trello]] (Sedang) memantau "Pengadaan 2025" — ini relevan langsung. Update yang direkomendasikan untuk card:
- Hapus "Menunggu BPKP" dari Progress
- Tambah info "BPKP melimpahkan kembali 22 Apr 2026 — keputusan audit lanjutan ada di Itjen II"
- Rencana Aksi: keputusan apakah Itjen II audit ulang atau tutup TLHP dengan justifikasi pelimpahan

**Dashboard yang perlu di-update:**
- Section 3.5.1 (Temuan TKPPSE) — kolom Status untuk row "Tagihan melebihi bukti — PT Telkom & Moratel" Rp 36.851.550 dari "🟡 Menunggu" → "🟡 BPKP melimpahkan, keputusan internal Itjen II diperlukan"

## Related Pages

- [[lha-om-tkppse-2025]] — LHA induk yang status temuannya berubah
- [[tkppse]] — overview TKPPSE
- [[tlrhp-bpk-semester-2-2025]] — TLRHP BPK terkait yang masih outstanding
- [[tlhp-internal-simwas-ir2]] — TLHP Internal SIMWAS yang merekam status B-51/2026
- [[pkpt-2026]] — Audit verifikasi pembayaran OM TKPPSE 2024 Rp 16 M (Nov 2026) — terpisah, untuk periode 2024 bukan 2025
- [[direktorat-jenderal-pengawasan-ruang-digital]] — pengirim surat permohonan asli
- [[bpk-laporan-hasil-pemeriksaan]] — konteks pemeriksaan BPK yang relate
- [[pemantauan-isu-risiko-trello]] — card TKPPSE
- [[dashboard]]
- [[inspektorat-ii]]
