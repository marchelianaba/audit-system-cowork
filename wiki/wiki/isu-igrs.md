# Isu-Isu Implementasi IGRS

**Summary**: Tiga isu serius yang muncul dalam dua minggu pertama operasional [[igrs]] (sejak 4 April 2026) dan mendapat sorotan luas dari komunitas game, media internasional, dan pelaku industri.

**Sources**: Kartu_Penugasan_Survei_Pendahuluan_IGRS_1.docx, Penelaahan_IGRS.docx, FGD tentang IGRS — 8 April 2026 1.md

**Last updated**: 2026-04-17

---

## Ringkasan Isu

Dalam waktu kurang dari dua minggu sejak IGRS beroperasi pada 4 April 2026, tiga isu serius mencuat secara bersamaan (source: Penelaahan_IGRS.docx):

1. Inkonsistensi masif dalam pemberian rating usia.
2. Pengenaan status Refused Classification (RC) yang tidak sah prosedural dan tidak transparan.
3. Kebocoran data sensitif ribuan developer game beserta materi pra-rilis.

---

## Isu 1 — Inkonsistensi Klasifikasi Rating

### Deskripsi
Sejak IGRS terintegrasi ke Steam pada awal April 2026, ditemukan kejanggalan besar dalam pemberian rating (source: Penelaahan_IGRS.docx):

- *Nukitashi* (game erotis eksplisit) mendapat rating **3+**.
- *PEAK* (game panjat tebing bergaya kartun) mendapat rating **18+**.
- *Balatro* (game kartu poker) mendapat rating **3+** tanpa deskriptor.
- *Umamusume: Pretty Derby* berlabel **18+** dengan alasan simulasi judi.
- *Grand Theft Auto V*, *Cyberpunk 2077*, *The Witcher 3*, dan *Clair Obscur: Expedition 33* (GOTY 2025) berstatus **RC**.

### Akar Masalah
Sistem mengandalkan Steam Content Survey yang diteruskan langsung sebagai rating **tanpa uji kesesuaian** oleh penguji yang ditetapkan Menteri, sebagaimana diwajibkan [[regulasi-igrs]]. Saat dikonfirmasi, pemerintah menyatakan rating di Steam bukan hasil klasifikasi resmi IGRS — namun pernyataan ini memperlihatkan ketiadaan pengawasan memadai (source: Penelaahan_IGRS.docx).

### Regulasi yang Dilanggar
Lihat [[regulasi-igrs]] — bagian Inkonsistensi Klasifikasi.

---

## Isu 2 — Status RC dan Transparansi Data

### Deskripsi
Sejumlah game besar terkena status RC tanpa verifikasi konten yang dapat dipertanggungjawabkan. Temuan komunitas mengungkap **dual data** (source: Penelaahan_IGRS.docx):

- *Balatro* tercatat berstatus RC di database internal IGRS (`igrs.id/game-detail/2514`) dengan deskriptor 'Simulasi Judi' dan 'Seksualitas/Pornografi'.
- Halaman tersebut **sengaja disembunyikan** dari tampilan publik.
- Rating berbeda muncul di Steam.
- Tidak ada mekanisme notifikasi kepada penerbit sebelum status RC aktif.

### Akar Masalah
RC diberikan secara otomatis tanpa prosedur verifikasi manual, tanpa notifikasi, tanpa kesempatan keberatan sebelum status aktif. Keberadaan data internal yang berbeda dari tampilan publik mengindikasikan ketidaktransparanan yang bertentangan dengan asas penyelenggara negara yang baik (source: Penelaahan_IGRS.docx).

### Regulasi yang Dilanggar
Lihat [[regulasi-igrs]] — bagian Status RC dan Transparansi.

---

## Isu 3 — Kebocoran Data Developer dan Materi Game Pra-Rilis

### Deskripsi
Pertengahan April 2026: celah keamanan kritis ditemukan pada API sistem IGRS. Bermula dari seseorang yang membangun frontend alternatif karena situs resmi sangat lambat, dan menemukan API yang tidak terproteksi (source: Penelaahan_IGRS.docx).

**Data yang bocor:**
- Lebih dari 1 jam footage gameplay *007: First Light* (IO Interactive) — termasuk adegan akhir cerita, rilis 27 Mei 2026.
- Footage gameplay *Echoes of Aincrad* (Bandai Namco) beserta cutscene cerita.
- Footage *Assassin's Creed: Black Flag remake* (Ubisoft) dan *Castlevania: Belmont's Curse* (Konami).
- ±2.000 alamat email developer, dari studio indie lokal hingga AAA global (termasuk Hoyoverse).

### Akar Masalah
- Materi submission dikirim melalui Google Drive link secara **ad hoc** tanpa prosedur manajemen akses baku.
- API sistem IGRS **tidak memiliki autentikasi dan otorisasi** yang memadai.
- Tidak ada mekanisme monitoring atau alerting terhadap akses tidak wajar.
- Kebocoran baru diketahui setelah viral di media sosial — bukan dari deteksi internal.

(source: Penelaahan_IGRS.docx)

### Regulasi yang Dilanggar
Lihat [[regulasi-igrs]] — bagian Kebocoran Data.

---

## Konfirmasi dari FGD (8 April 2026)

Dalam [[fgd-igrs-8-april-2026]], Komdigi mengakui adanya masalah, namun mengarahkan penyebab ke "bug Steam" dan kelalaian developer yang belum mengisi formulir. Pelaku industri tidak menerima penjelasan ini — kekhawatiran mereka tetap pada mekanisme RC itu sendiri yang bisa memblokir karya kapan saja (source: FGD tentang IGRS — 8 April 2026 1.md).

Temuan audit perlu menverifikasi klaim "bug Steam" tersebut secara independen.

## Catatan Prioritas

Berdasarkan [[penelaahan-igrs]] (source: Penelaahan_IGRS.docx):

- **Paling mendesak**: Isu 3 (Kebocoran Data) — ada kewajiban hukum *time-bound* notifikasi 14 hari per [[regulasi-uu-pdp|UU PDP]] (Pasal 46).
- **Paling mudah dibuktikan**: Isu 1 (Akurasi Klasifikasi) — evidence bersifat publik dan dapat diverifikasi objektif.

## Related pages

- [[igrs]]
- [[fgd-igrs-8-april-2026]]
- [[sasaran-audit-igrs]]
- [[rekomendasi-igrs]]
- [[regulasi-igrs]]
- [[regulasi-uu-pdp]] — UU 27/2022 Perlindungan Data Pribadi
- [[regulasi-permenkominfo-2-2024]] — Permenkominfo 2/2024 Klasifikasi Gim
- [[regulasi-pp-tunas]] — PP 17/2025 Perlindungan Anak Ruang Digital
- [[penelaahan-igrs]]
- [[audit-kinerja-layanan-klasifikasi-gim]]
