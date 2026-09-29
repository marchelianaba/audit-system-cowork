# SOP — Ingest LHP dari audit-system-v4 ke llm-wiki

**Summary**: Prosedur baku untuk memindahkan LHP final yang dihasilkan `audit-system-v4/` agar dapat di-ingest oleh `llm-wiki/`. Menutup celah loop yang sebelumnya manual dan ad-hoc.

**Sources**: internal — disusun berdasarkan arsitektur audit-system-v4 dan konvensi ingest wiki.

**Last updated**: 2026-04-24

---

## Mengapa SOP Ini Diperlukan

Sistem audit (`audit-system-v4/`) menghasilkan LHP di folder penugasan (`audit-system-v4/penugasan/[nomor-ST]/_LHP/`). Sementara `llm-wiki/` hanya membaca dokumen dari `llm-wiki/raw/`. Tanpa SOP, LHP yang sudah selesai tidak otomatis memperkaya knowledge base — artinya pola lintas-penugasan tidak terakumulasi.

## Prasyarat

- LHP sudah final dan disetujui (bukan draft KKP atau _SUBSTANSI yang masih uji coba).
- Nomor surat sudah terbit dari SIMWAS.
- File sudah dalam format PDF final (hasil ekspor dari .docx).

## Alur (5 Langkah Manual)

```
┌─────────────────────────────────────────────────────────┐
│ 1. LHP FINAL di audit-system-v4/penugasan/[ST]/_LHP/    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 2. EKSPOR KE PDF (jika masih .docx)                     │
│    Simpan dengan nama baku:                              │
│    [no-surat] [KODE] [tgl] ND [judul LHP].pdf            │
│    Contoh: "72 IJ.3 PW.04.01 surat keluar 05.05.2026    │
│             ND LHP Audit Kinerja IGRS.pdf"               │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 3. COPY PDF KE llm-wiki/raw/                            │
│    (drag-drop di Explorer atau cp di terminal)           │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 4. MINTA CLAUDE INGEST                                  │
│    "Ingest LHP baru di raw/ ke wiki"                     │
│    Claude otomatis: baca PDF → buat halaman LHP          │
│    → update halaman konsep terkait → update index        │
│    → append log                                          │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 5. VERIFIKASI                                            │
│    - halaman LHP baru muncul di wiki/                    │
│    - index.md → kategori "Laporan Hasil Pengawasan"      │
│    - dashboard.md → temuan baru masuk                    │
│    - pola-temuan-berulang.md → update bila ada pola      │
└─────────────────────────────────────────────────────────┘
```

## Konvensi Penamaan File (Wajib)

Nama file PDF mengikuti format yang sudah dipakai `raw/` existing:

```
[no-surat] [Kode Unit] [Kode Klasifikasi] [surat keluar] [tgl] ND [Judul Singkat].pdf
```

Contoh dari `raw/` existing:
- `34 IJ.3 PW.04.03 surat keluar 30.01.2026 ND Laporan Monitoring...`
- `70 IJ.3 PW.04.05 surat keluar 27.02.2026 ND Laporan Hasil Evaluasi Manajemen Risiko...`

**Kode klasifikasi (PW.04.xx)**:
- PW.04.01 — Audit/LHA
- PW.04.03 — Pemantauan/Monitoring Pengadaan
- PW.04.04 — Reviu
- PW.04.05 — Evaluasi

## Template Permintaan Ingest ke Claude

Paling sederhana, kalimat ke Claude:
> "Saya baru taruh [nama file].pdf di llm-wiki/raw/. Tolong ingest ke wiki: buat halaman LHP, update index, update log, dan periksa apakah ada pola baru yang perlu masuk ke pola-temuan-berulang."

Claude akan:
1. Baca PDF.
2. Buat halaman `wiki/lhX-[slug].md` sesuai format CLAUDE.md.
3. Update halaman konsep lain yang berdekatan (vendor, unit kerja, regulasi).
4. Tambah entry baru ke index.
5. Append log dengan tanggal dan daftar halaman baru/diperbarui.
6. Periksa apakah temuan baru memperkuat pola di `pola-temuan-berulang.md` → update bila ya.

## Opsional — Ingest Berkelompok (Batch)

Jika Anda mengumpulkan beberapa LHP sekaligus (mis. setelah Rapim bulanan):

1. Copy semua PDF ke `raw/` sekaligus.
2. Sampaikan ke Claude: "Ingest semua LHP baru di raw/ — X sampai Y."
3. Claude akan proses satu per satu dan menggabungkan ringkasan ke log.

## Yang TIDAK Diingest

- Draft KKP / LHP SUBSTANSI yang masih uji coba (file dengan prefix `_UJI-` atau `DRAFT-`).
- File notulen internal tim audit.
- File kertas kerja (Excel) — hanya dokumen final terbitan resmi yang masuk `raw/`.

## Integrasi dengan Dashboard

Setiap ingest berpotensi menambah temuan baru → update `dashboard.md`. Minta Claude:
> "Setelah ingest, update dashboard dengan temuan baru dari LHP ini."

## Related pages

- [[integrasi-audit-system]]
- [[sop-pemisahan-dashboard]]
- [[dashboard]]
- [[pola-temuan-berulang]]
- [[index]]
