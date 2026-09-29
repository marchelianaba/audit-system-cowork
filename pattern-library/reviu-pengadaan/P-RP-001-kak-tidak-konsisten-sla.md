---
kode: P-RP-001
judul: Nilai SLA pada KAK tidak konsisten antara bagian Latar Belakang dan Persyaratan Teknis
jenis: reviu-pengadaan
status: aktif
frekuensi: 1 kali (Reviu DC/DRC PSrE Induk 2026) — perlu validasi di penugasan lain untuk promote
false_positive_note: Tidak berlaku jika SLA di Latar Belakang adalah SLA agregat (mis. layanan), sedangkan SLA di Persyaratan Teknis adalah SLA komponen (mis. infrastruktur per region). Harus dicek apakah levelnya sama.
---

## Kondisi (template)
Pada KAK [nama paket] TA [tahun], nilai Service Level Agreement (SLA) yang tercantum di bagian [Latar Belakang / Pendahuluan] berbeda dengan nilai SLA pada bagian Persyaratan Teknis / Spesifikasi Teknis.

Contoh perbedaan:
- Bagian Latar Belakang menyebut SLA [X%]
- Bagian Persyaratan Teknis menyebut SLA [Y%]

Inkonsistensi ini berpotensi menimbulkan ambiguitas saat evaluasi penawaran dan pengawasan kontrak.

## Kriteria
- Perpres 16/2018 jo. Perpres 12/2021 jo. Perpres 46/2025 tentang Pengadaan Barang/Jasa Pemerintah — KAK harus memuat spesifikasi yang jelas, terukur, dan konsisten
- Perlem LKPP 12/2021 tentang Pedoman Pelaksanaan Pengadaan — KAK sebagai dokumen dasar wajib bebas ambiguitas

## Akibat
1. Penyedia kesulitan menentukan kebutuhan teknis yang harus dipenuhi
2. Risiko dispute saat evaluasi SLA di masa kontrak
3. Pengukuran kinerja kontrak tidak valid

## Rekomendasi Tipikal (di LHP)
Agar PPK [sebutkan unit] merevisi KAK dengan menyatukan nilai SLA di seluruh bagian dokumen. Revisi harus didokumentasikan dalam Addendum KAK yang ditetapkan sebelum tahap pemilihan berlanjut. Deadline: sebelum pengumuman tender. Ukuran sukses: tidak ada perbedaan angka SLA antar bagian dalam dokumen pemilihan final.

## Precheck Claude (saat Task 03)
Tanda-tanda pola ini mungkin berlaku:
- [ ] File KAK ada di `03-perencanaan/` atau `02-kontrak/`
- [ ] Panjang KAK >20 halaman (KAK kompleks lebih rentan inkonsisten)
- [ ] KAK menyebut SLA, uptime, availability, atau service level di >1 bagian
- [ ] Jenis paket: layanan TI (cloud, DC/DRC, managed service), telekomunikasi

## Cara Cek Cepat
1. Grep "SLA" / "availability" / "uptime" di KAK (baik PDF text maupun OCR)
2. Catat angka yang muncul per section
3. Jika ada ≥2 angka berbeda yang tampak mengukur hal sama → temuan

## Kasus Preseden
- **Reviu DC/DRC PSrE Induk TA 2026** (8 Apr 2026): SLA di Latar Belakang berbeda dengan SLA di Persyaratan Teknis. Direkomendasikan revisi KAK sebelum tender berlanjut.
