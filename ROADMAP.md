# Roadmap LifeOS — sumber status tunggal

Status paket source: **v1.4.0**. Nomor paket berbeda dari tahap MVP/V2/V3/V4 pada PRD. Deployment yang benar-benar aktif harus diperiksa melalui footer aplikasi dan Coolify; source siap tidak berarti sudah terpasang.

## Arah produk

Second brain pribadi untuk menghubungkan ide, ilmu, hasil, ukuran kemajuan, proses, tugas, waktu dan review. Mendukung bisnis, kuliah, masjid/organisasi, hafalan 30 juz dan ruang pemulihan. Tujuan penggunaan: langkah lebih jelas, tanggung jawab tertata, ada ruang kerja/ibadah/istirahat/kontemplasi. Aplikasi tidak menjamin hasil bisnis, keahlian atau kebahagiaan dari jumlah centang.

## Tersedia pada v1.4

| Kelompok | Cakupan | Batas |
|---|---|---|
| Fondasi MVP | Today, Inbox, Notes, Tasks, Project, Big 3, Kanban/WIP, timer dan review | Belum offline/autosave server |
| Penyusunan goal | Planner enam langkah, contoh dan bantuan isi berdasarkan kata kunci | Bukan AI; jawaban wajib ditinjau |
| Goal | Indikator utama dan tambahan, satuan, kondisi awal, target dan log aktual | Belum agregasi/analisis otomatis |
| Proses | Rutinitas hari pilihan, hubungan Goal, catatan done/skip, jeda rutinitas | Bukan notifikasi/habit analytics lengkap |
| Waktu | Anggaran ritme, kalender pekanan, peringatan bentrok event, waktu manual | Belum drag/drop/smart scheduling/audit otomatis seluruh hari |
| Fokus | Sesi aktual dan jeda singkat/panjang berdasarkan ronde | Jeda dimulai setelah sesi disimpan, alarm tidak aktif di browser tertutup |
| Review | Ringkasan tujuh hari, draft review dari data, perasaan/beban/pemulihan | Refleksi dan perubahan rencana tetap pengguna |
| Knowledge | Markdown subset, link/backlink, Daily Notes dan pencarian teks lintas entitas | Belum graph/Markdown penuh/pencarian semantik |
| Pembelajaran | Kartu ilmu, tugas praktik, pengalaman dan tanggal review | Belum kurikulum adaptif atau penilaian ahli |
| Sullamul Hifz | Peta 8 jilid/30 juz, mutabaah, evaluasi, rutinitas murajaah dan pengingat jatuh tempo | Adaptasi, bukan seluruh kolom buku; belum penilaian tajwid otomatis |
| Audio | Rekam/putar/upload/download/hapus, persisten, backup/impor ZIP | Bergantung format/izin browser; bukan rekam background |
| Keandalan | Revisi, backup JSON v4, migrasi, draft browser, riwayat snapshot | Restore snapshot UI dan sinkronisasi langsung belum tersedia |

## Pemetaan PRD yang tetap dipertahankan

- **MVP:** fondasi tersedia; berikutnya fokus verifikasi dan kenyamanan alur nyata.
- **Versi 2 PRD:** fitur waktu dan analitik tersedia sebagian; laporan rentang/per Area dan audit yang lebih lengkap menyusul.
- **Versi 3 PRD:** Goals dasar, pencarian lintas data dan rutinitas sudah ada; graph, advanced search, habit analytics, template builder, custom dashboard, automation dan keselarasan nilai masih backlog.
- **Versi 4 PRD:** AI Assistant/Planning/Task Breakdown/Knowledge Search/Smart Scheduling belum dikerjakan.

## Urutan pengembangan berikutnya

1. **Stabilkan paket gabungan:** cek di browser desktop/HP, mikrofon, backup/restore, konflik, draft dan data setelah redeploy. Kumpulkan kendala untuk satu batch perbaikan.
2. **Lengkapi kebutuhan yang terbukti:** pengukuran ketercapaian Goal yang lebih kuat, murajaah dekat/jauh lebih terstruktur, perjelasan unit juz selain 29, milestone dan subtasks yang lebih baik.
3. **Keandalan data:** autosave server yang aman, desain relasional/migrasi jika diperlukan, offline editing/sinkronisasi dengan resolusi konflik.
4. **Lengkapi V2/V3:** kalender lanjutan, analytics per Area/periode, habit/knowledge/template/custom dashboard/automation.
5. **AI:** hanya setelah batas peran, sumber, biaya, privasi dan hasil yang ingin dibantu jelas. Template berbasis kata kunci sekarang tidak dilabeli sebagai AI.

## Belum ada / jangan dianggap selesai

Autosave server, offline-first, sinkronisasi antrean/perangkat otomatis, siklus kalender otomatis, evaluasi SGS otomatis, seluruh rubric Sullamul, koreksi bacaan, API AI, file attachment umum, graph view, semantic search, template builder, backup terjadwal, notifikasi background, audit keamanan independen. SQLite dan server Python tetap arsitektur pribadi saat ini, belum PostgreSQL/Next.js dalam pilihan awal PRD.

## Kebiasaan release

Kumpulkan perbaikan terkait, jalankan tes, sediakan satu ZIP kumulatif dan satu panduan update, lalu deploy sekali. Hotfix terpisah hanya jika ada kerusakan penting yang tidak layak menunggu. Source tidak otomatis berubah/deploy terjadwal tanpa pekerjaan baru.
