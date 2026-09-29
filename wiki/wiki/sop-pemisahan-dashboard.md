# SOP — Pemisahan Peran PROJECT-STATUS.md vs dashboard.md

**Summary**: Kedua file sama-sama berjudul "status/dashboard" tetapi melayani audiens dan tujuan yang berbeda. SOP ini membatasi overlap dan mendefinisikan sumber kebenaran untuk tiap jenis informasi.

**Sources**: `PROJECT-STATUS.md` (root folder induk) dan `llm-wiki/wiki/dashboard.md`.

**Last updated**: 2026-04-24

---

## Masalah yang Dipecahkan

| File | Lokasi | Isi Saat Ini |
|---|---|---|
| `PROJECT-STATUS.md` | Folder induk `Audit otomatis berbasis claude (1)/` | Status pengembangan sistem AI (v1, v2, v2.3, v2.4); pilot test; progress per sesi; changelog skill. |
| `dashboard.md` | `llm-wiki/wiki/` | Status isu, temuan audit, rekomendasi, risiko HIGH yang sedang diawasi Inspektorat II. |

Risiko tanpa SOP: auditor bingung harus update di mana; informasi bisa *drift* (angka berbeda di dua tempat).

## Prinsip Pemisahan

> `PROJECT-STATUS.md` = **status produk (sistem AI)**.
> `dashboard.md` = **status pengawasan (substansi audit)**.

## Matriks Pemisahan

| Jenis Informasi | Rumah Kanonik | Alasan |
|---|---|---|
| Versi sistem AI (v2.7, v2.8, dsb.) | **PROJECT-STATUS.md** | Tentang sistem, bukan tentang audit |
| Changelog skill (reviu-pengadaan v1.2 → v1.4) | **PROJECT-STATUS.md** | Product changelog |
| Progress pilot test skill | **PROJECT-STATUS.md** | Uji sistem |
| Gate penilaian SPIP yang sudah selesai (gate 1A, 1B...) | **PROJECT-STATUS.md** (progres sistem) + lintas ke `dashboard.md` (catatan temuan) | Gate-nya adalah progres produk; AoI yang dihasilkan adalah substansi pengawasan |
| Isu Strategis yang sedang dipantau | **dashboard.md** | Substansi pengawasan |
| Temuan audit yang perlu tindak lanjut | **dashboard.md** | Substansi pengawasan |
| Status rekomendasi IGRS jangka pendek | **dashboard.md** | Substansi pengawasan |
| Peta risiko HIGH (Wasdig, DJED) | **dashboard.md** | Substansi pengawasan |
| Audit aktif (penugasan yang sedang berjalan) | **dashboard.md** | Substansi pengawasan |
| Deadline UU PDP 14 hari kerja kasus IGRS | **dashboard.md** | Substansi pengawasan |
| Konfigurasi model AI (Sonnet vs Haiku) | **PROJECT-STATUS.md** | Tentang sistem |
| Realisasi anggaran Inspektorat II | **llm-wiki/wiki/realisasi-anggaran-inspektorat-ii-2026.md** | Halaman wiki tersendiri |
| Daftar tim auditor | `TIM/DAFTAR-TIM.md` | Sudah punya rumah |

## Aturan Cross-Reference

- `dashboard.md` boleh merujuk ke `PROJECT-STATUS.md` dengan kalimat seperti: *"Status pilot evaluasi SPIP — lihat PROJECT-STATUS.md."*
- `PROJECT-STATUS.md` boleh merujuk ke `dashboard.md` untuk hasil substansi: *"AoI yang dihasilkan sudah dicatat di llm-wiki/dashboard."*
- **Jangan menyalin tabel yang sama di dua tempat** — rujuk saja.

## Frekuensi Update

| File | Frekuensi | Pemicu |
|---|---|---|
| `PROJECT-STATUS.md` | Saat ada sesi pengembangan sistem | Pilot test selesai; skill dirilis; bug fix |
| `dashboard.md` | Mingguan atau saat ada perubahan material | Temuan baru; status tindak lanjut berubah; LHP baru |

## Cara Update

### Untuk `PROJECT-STATUS.md`
Editor: auditor (atau Claude saat dikonsultasikan tentang iterasi sistem).
Struktur: kronologis per sesi (SESI 1, SESI 2, dst.), tiap sesi memuat perubahan sistem + pilot test.

### Untuk `dashboard.md`
Editor: Claude berdasarkan input auditor mingguan.
Struktur: ringkasan status + 5 seksi tematik (Audit Aktif, Isu Strategis, Temuan, Rekomendasi IGRS, Peta Risiko).

## Template Permintaan Update ke Claude

**Untuk dashboard:**
> "Update dashboard: [daftar perubahan]. Mis. 'Notifikasi PDP IGRS sudah dikirim 26 April', 'TLHP BPKP atas TKPPSE sudah terbit — tagihan Rp36,8jt dikembalikan'."

**Untuk PROJECT-STATUS:**
> "Tambahkan entry SESI N di PROJECT-STATUS: [apa yang berubah di sistem]."

## Migrasi Saat Ini

Per 24 April 2026, SOP ini baru disusun. Langkah migrasi yang disarankan:
1. Tinjau `dashboard.md` — apakah ada informasi yang sebenarnya milik `PROJECT-STATUS.md`? Tidak terlihat ada.
2. Tinjau `PROJECT-STATUS.md` — apakah ada temuan substansi yang bocor ke sana? Seksi SPIP pilot (7 AoI) adalah *borderline* — substansi ada di `penugasan/SPIP/AoI-SPIP-2026.md`; ringkasan pilot di `PROJECT-STATUS.md` untuk konteks sistem. Tidak perlu dipindah.
3. Tambahkan baris di atas setiap file yang menunjuk ke SOP ini agar editor berikutnya paham pembagian peran.

## Related pages

- [[dashboard]]
- [[integrasi-audit-system]]
- [[sop-ingest-lhp-ke-wiki]]
