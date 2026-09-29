# Pattern Library — Temuan Berulang Lintas Penugasan

## Tujuan

Pattern library mengkurasi **temuan yang sering muncul** di penugasan audit/reviu/evaluasi Inspektorat II. Tiap pola tersimpan sebagai *template KKSA* yang bisa dipakai Claude sebagai:

1. **Input checklist proaktif** saat Task 03 (KKP): Claude mem-precheck pola ini terhadap dokumen yang direviu → percepat identifikasi temuan tipikal.
2. **Benchmark**: auditor bisa lihat berapa banyak temuan serupa sudah ditemukan lintas penugasan → signal kalau ini sistemik.
3. **Pembelajaran**: tim baru belajar dari pola yang sudah terbukti.

## Prinsip

- Pattern BUKAN pengganti analisis kasus per kasus. Selalu verifikasi kondisi dengan dokumen aktual.
- Pattern tidak boleh dipakai untuk "menempel" temuan tanpa bukti — prinsip anti-halusinasi tetap berlaku.
- Setiap pola harus punya *false positive rate* catatan — kapan pola ini ternyata tidak berlaku.

## Struktur File

```
pattern-library/
├── README.md (file ini)
├── reviu-pengadaan/
│   ├── P-RP-001-kak-tidak-konsisten-sla.md
│   ├── P-RP-002-hps-kurang-komponen-migrasi.md
│   └── ...
├── audit-pengadaan/
│   └── P-AP-001-...
├── evaluasi-spip/
│   └── P-SP-001-...
├── evaluasi-sakip/
│   └── ...
└── _index.md (daftar semua pattern dengan status aktif/deprecated)
```

## Penomoran

`P-[KODE_JENIS]-[NOMOR_URUT]-[slug-judul].md`

- `P-RP` = Reviu Pengadaan
- `P-AP` = Audit Pengadaan
- `P-RK` = Reviu RKA-KL
- `P-RL` = Reviu Laporan Kinerja
- `P-PP` = Pemantauan Pengadaan
- `P-SP` = Evaluasi SPIP
- `P-SK` = Evaluasi SAKIP
- `P-RB` = Evaluasi RB
- `P-MR` = Evaluasi Manajemen Risiko
- `P-AK` = Audit Kinerja
- `P-TL` = Pemantauan TLHP

## Template Pattern

Setiap file pattern harus memuat:

```markdown
---
kode: P-[KODE]-[NOMOR]
judul: [Kalimat deskriptif kondisi yang jadi judul temuan]
jenis: [reviu-pengadaan / audit-pengadaan / ...]
status: aktif / draft / deprecated
frekuensi: n kali ditemukan dari m penugasan yang direviu (sumber: feedback/)
false_positive_note: kondisi dimana pola ini ternyata tidak berlaku
---

## Kondisi (template)
[Deskripsi kondisi yang biasanya ditemukan — gunakan placeholder untuk data spesifik]

## Kriteria
[Regulasi + pasal + ayat yang dilanggar]

## Sebab Tipikal (audit-pengadaan saja)
[Root cause yang biasanya ditemukan]

## Akibat
[Konsekuensi ke organisasi]

## Rekomendasi Tipikal (dipakai di LHP, bukan KKP)
[Format: siapa, apa, kapan, ukuran sukses]

## Precheck Claude (saat Task 03)
Tanda-tanda pola ini mungkin berlaku di penugasan:
- [ ] [tanda 1 — yang bisa dicek dari file listing / ringkasan dokumen]
- [ ] [tanda 2]

## Kasus Preseden
- [Kode penugasan 1]: [ringkasan temuan]
- [Kode penugasan 2]: ...
```

## Cara Update

1. **Setelah Task 04 SETUJU** di suatu penugasan, auditor (atau Claude) review temuan:
   - Apakah temuan ini mirip pattern yang sudah ada? → Update frekuensi + tambah kasus preseden di pattern existing.
   - Apakah pola baru? → Buat file pattern baru dengan status "draft".
2. **Setelah pattern muncul ≥3 kali lintas penugasan** → promote status dari draft ke aktif.
3. **Pattern aktif** dirujuk oleh SKILL.md jenis pengawasan terkait (tambahkan di bagian "Pattern Library untuk dirujuk saat Task 03").

## Status Initial (19 April 2026)

⬜ **FOLDER BARU** — dibuat sebagai bagian v2.8. Seeding awal dari 2 pattern yang terdokumentasi di `feedback/2026-04-08-KKP-UJI-Reviu-DCDRC-PSrE-2026.md`:
- P-RP-001 (KAK tidak konsisten SLA)
- P-RP-002 (HPS kurang komponen migrasi)

Pattern library akan tumbuh organik dari setiap penugasan yang selesai.
