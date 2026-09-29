# Integrasi llm-wiki ↔ audit-system-v2

**Summary**: Penjelasan hubungan antara `llm-wiki` (knowledge base Inspektorat II) dan `audit-system-v2` (pipeline eksekusi penugasan berbasis Claude). Memposisikan wiki sebagai *context bank* dan v2 sebagai *mesin eksekusi*.

**Sources**: audit-system-v2/README.md, MEMORY auto-wiki, internal.

**Last updated**: 2026-04-24

---

## Dua Komponen, Satu Ekosistem

Di dalam folder kerja `Audit otomatis berbasis claude (1)` hidup dua komponen yang saling mendukung:

| Komponen | Fungsi Utama | Bentuk |
|---|---|---|
| **`llm-wiki/`** | Knowledge base ter-*link* tentang auditee, regulasi, isu, laporan, pola temuan. Memberi konteks tahan-lama. | Markdown + Obsidian vault; di-maintain Claude dari sumber di `raw/`. |
| **`audit-system-v2/`** | Pipeline eksekusi penugasan (Task 01–04: ST, KP+PKP, KKP, LHP). | Skill Claude + template + checklist + pattern library. |

## Pembagian Peran

| Kebutuhan Anda | Pakai | Contoh |
|---|---|---|
| Memahami objek audit sebelum turun lapangan | `llm-wiki` | Baca [[igrs]], [[direktorat-pengembangan-ekosistem-digital]] sebelum survei. |
| Menyusun Kerangka Pengawasan & PKP | `audit-system-v2` Task 02 | Skill `audit-kinerja` atau `reviu-pengadaan` dsb. |
| Mengisi Kertas Kerja Pengawasan | `audit-system-v2` Task 03 | Dengan auto-pre-digest RKA-K/L, pattern library pengadaan, dsb. |
| Menyusun LHP | `audit-system-v2` Task 04 + skill `isi-laporan` | Template LHP sesuai jenis penugasan. |
| Reviu dokumen cepat (kontrak, SOP, LK, pengadaan) | Skill `reviu-dokumen-auditor` | Output KKA berformat Excel. |
| Cross-check temuan lintas-penugasan | `llm-wiki` | Halaman [[pola-temuan-berulang]]. |
| Kumpulan regulasi, istilah, profil mitra | `llm-wiki` | Halaman [[glossary]], `regulasi-*.md`, `vendor-*.md`. |
| Status mingguan temuan & risiko | `llm-wiki/dashboard.md` | Auditor minta Claude update. |

## Alur Penugasan dengan Dukungan Wiki

```
┌─────────────────────────────────────────────────────┐
│  1. ST turun (Task 01 — audit-system-v2)            │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  2. Survei pendahuluan: baca wiki objek audit       │
│     [[direktorat-...]], [[igrs]], [[peta-risiko-*]] │
│     → pahami histori, isu, regulasi, vendor          │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  3. KP+PKP (Task 02 — audit-system-v2)              │
│     Claude menarik kriteria dari wiki + pedoman     │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  4. Eksekusi KKP (Task 03)                          │
│     Reviu dokumen (skill) → temuan                  │
│     Cek pola [[pola-temuan-berulang]]               │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  5. LHP (Task 04 — skill isi-laporan)               │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│  6. Ingest LHP ke wiki                              │
│     → halaman LHP baru + update [[dashboard]]       │
│     → memperkaya [[pola-temuan-berulang]]           │
└─────────────────────────────────────────────────────┘
```

## Loop Pembelajaran

LHP yang sudah di-ingest kembali ke wiki menjadi sumber konteks untuk penugasan berikutnya. Inilah yang membuat wiki "compound over time" — setiap audit baru mendapat manfaat dari seluruh audit sebelumnya.

## Yang Belum Terhubung (Backlog)

- Belum ada mekanisme otomatis untuk ingest LHP baru dari `audit-system-v2/penugasan/` ke `llm-wiki/raw/`.
- Belum ada halaman di wiki yang menautkan ke skill mana yang cocok untuk tiap jenis penugasan.
- Penamaan file antara dua komponen belum seragam (mis. format nomor ND dan timestamp).

## Related pages

- [[index]]
- [[dashboard]]
- [[pola-temuan-berulang]]
- [[inspektorat-ii]]
