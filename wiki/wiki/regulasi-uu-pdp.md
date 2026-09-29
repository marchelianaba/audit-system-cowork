# UU 27/2022 — Perlindungan Data Pribadi (UU PDP)

**Summary**: Undang-Undang Perlindungan Data Pribadi yang mengatur kewajiban pengendali dan prosesor data; relevan untuk audit keamanan sistem dan penanganan kebocoran data.

**Sources**: UU 27/2022; Penelaahan_IGRS.docx (sebagai rujukan kasus aktif).

**Last updated**: 2026-04-24

---

## Identitas Regulasi

- **Judul**: Undang-Undang Nomor 27 Tahun 2022 tentang Perlindungan Data Pribadi
- **Tanggal pengundangan**: 17 Oktober 2022
- **Masa transisi**: 2 tahun sejak diundangkan (penegakan penuh sejak Oktober 2024)

## Relevansi untuk Pengawasan Inspektorat II

1. Setiap sistem elektronik K/L yang memproses data pribadi warga atau mitra tunduk pada UU ini.
2. Audit keamanan sistem (mis. [[igrs]]) wajib menguji kepatuhan atas kewajiban PDP.
3. Insiden kebocoran data memicu kewajiban notifikasi berbatas waktu.

## Ketentuan Kunci yang Sering Diuji Audit

| Pasal | Pokok | Bunyi Singkat |
|---|---|---|
| Pasal 4 | Kategori data sensitif | Data biometrik, kesehatan, finansial, anak, dsb. — perlakuan khusus. |
| Pasal 16 | Kewajiban pengendali | Memproses data sesuai tujuan, akurat, dan aman. |
| Pasal 35 | Kewajiban teknis pelindungan | Menerapkan sistem keamanan informasi, enkripsi, kontrol akses. |
| **Pasal 46** | **Kewajiban notifikasi kebocoran** | Dalam **14 hari kerja** setelah diketahui, wajib notifikasi ke subjek data dan Lembaga PDP. |
| Pasal 47 | Penilaian dampak | Data Protection Impact Assessment untuk pemrosesan berisiko tinggi. |
| Pasal 57–67 | Sanksi administratif dan pidana | Denda hingga 2% pendapatan tahunan atau 4 miliar; pidana maks. 6 tahun. |

## Kewajiban Notifikasi (Pasal 46) — *Critical*

Alur audit yang direkomendasikan saat menemukan indikasi kebocoran:
1. Konfirmasi tanggal diketahuinya kebocoran → hitung deadline 14 hari kerja.
2. Cek: apakah subjek data sudah dinotifikasi? (cek dokumentasi, email, pengumuman publik).
3. Cek: apakah Lembaga PDP sudah dinotifikasi? (minta bukti submit).
4. Cek: konten notifikasi — harus memuat minimal: apa yang bocor, kapan, dampak, tindakan mitigasi.

## Kasus Aktif di Wiki

- [[isu-igrs]] — Kebocoran data ~2.000 developer + 4 game AAA; deadline 14 hari kerja dari tanggal diketahui. Dashboard mencatat deadline ~28 April 2026 (sumber: [[dashboard]]).

## Kaitan dengan Regulasi Lain

- [[regulasi-igrs]] — konteks IGRS sebagai sistem yang memicu kewajiban PDP.
- PP Pelaksana UU PDP — *(belum terbit secara lengkap; perlu update jika PP baru keluar)*.

## Related pages

- [[isu-igrs]]
- [[rekomendasi-igrs]]
- [[igrs]]
- [[dashboard]]
