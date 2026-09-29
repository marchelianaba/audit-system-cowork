---
kode: P-RP-002
judul: HPS tidak mencantumkan komponen biaya migrasi/transisi meski KAK mensyaratkan klausul migrasi
jenis: reviu-pengadaan
status: aktif
frekuensi: 1 kali (Reviu DC/DRC PSrE Induk 2026) — perlu validasi di penugasan lain untuk promote
false_positive_note: Tidak berlaku jika KAK secara eksplisit menyebut migrasi di-cover oleh kontrak eksisting atau menjadi tanggung jawab PPK internal. Harus cek klausul terminasi/transisi di kontrak eksisting.
---

## Kondisi (template)
Pada paket pengadaan [nama paket], Kerangka Acuan Kerja (KAK) memuat klausul migrasi/transisi dari penyedia lama atau ke penyedia baru di akhir kontrak. Namun Harga Perkiraan Sendiri (HPS) tidak memuat komponen biaya untuk aktivitas migrasi/transisi tersebut.

Aktivitas migrasi yang umumnya tidak ter-cost antara lain:
- Transfer data dari sistem lama
- Setup infrastruktur paralel selama masa transisi
- Pelatihan personel penyedia baru
- Dokumentasi serah terima

## Kriteria
- Perpres 16/2018 jo. Perpres 12/2021 — HPS harus memperhitungkan seluruh lingkup pekerjaan yang tertulis di KAK
- Perlem LKPP 12/2021 — HPS disusun berdasarkan rincian kebutuhan yang konsisten dengan KAK; komponen biaya yang tidak masuk HPS dianggap tidak diperlukan dan tidak dapat ditagih penyedia

## Akibat
1. Penyedia terpaksa menyerap biaya migrasi ke komponen lain (kemahalan komponen utama) atau menolak di pelaksanaan
2. Perubahan kontrak (addendum) di tengah jalan meningkatkan biaya
3. Risiko layanan terputus saat transisi karena tidak ada dana untuk aktivitas migrasi
4. Potensi sengketa jika penyedia klaim migrasi di luar kontrak

## Rekomendasi Tipikal (di LHP)
Agar PPK [sebutkan unit] merevisi HPS dengan menambahkan komponen biaya migrasi/transisi yang proporsional dengan lingkup yang tertulis di KAK. HPS revisi harus ditetapkan sebelum tahap pemilihan berlanjut. Ukuran sukses: HPS memuat pos biaya spesifik "Migrasi/Transisi" dengan breakdown yang dapat ditelusuri ke klausul KAK.

## Precheck Claude (saat Task 03)
Tanda-tanda pola ini mungkin berlaku:
- [ ] KAK menyebut "migrasi" / "transisi" / "serah terima sistem" / "transfer data"
- [ ] Paket melibatkan pergantian penyedia (kontrak lama akan berakhir)
- [ ] HPS total punya struktur yang sama dengan HPS kontrak sebelumnya (indikasi copy tanpa review migrasi)
- [ ] Jenis paket: sistem TI, data center, aplikasi, layanan berkelanjutan

## Cara Cek Cepat
1. Grep "migrasi" / "transisi" di KAK
2. Jika ada, cek apakah di HPS ada line item bernama "migrasi" atau variasi ("transisi", "setup awal", "onboarding")
3. Jika KAK menyebut migrasi tapi HPS tidak memuatnya → temuan

## Kasus Preseden
- **Reviu DC/DRC PSrE Induk TA 2026** (8 Apr 2026): KAK memuat klausul migrasi dari penyedia lama, tapi HPS tidak memiliki komponen biaya migrasi. Direkomendasikan revisi HPS.
