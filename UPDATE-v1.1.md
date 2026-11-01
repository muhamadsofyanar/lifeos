# Update LifeOS v1.0 ke v1.1 — GitHub manual + Coolify

## Sebelum update

1. Dari aplikasi lama, buka Settings dan download backup JSON. Simpan di komputer.
2. Catat nama volume Coolify yang sekarang terpasang pada `/data`. Jangan hapus atau ganti volume ini, jangan hapus resource aplikasinya.
3. Selesaikan timer aktif dan tutup tab aplikasi lain untuk menghindari tab versi lama menulis data.

## Upload GitHub

Ekstrak ZIP. Pada repository yang SAMA, branch yang digunakan Coolify, ganti/tambahkan lima file berikut dari folder `lifeos`:

- `server.py` (ganti)
- `static/index.html` (ganti)
- `static/app.js` (ganti)
- `static/style.css` (ganti)
- `static/features.js` (file baru, wajib)

Boleh upload README, tests, ROADMAP, CHANGELOG dan panduan ini juga. Struktur folder `static` harus dipertahankan.

**Tidak perlu mengganti Dockerfile, docker-compose.yml, environment, password, atau konfigurasi storage yang sudah bekerja.** Jika compose di repository telah kamu sesuaikan, pertahankan versi tersebut beserta nama volume. Jangan mengganti nama proyek/resource Coolify atau menjalankan `docker compose down -v`.

Commit, lalu pilih Redeploy pada resource Coolify yang sekarang. Jika auto-deploy aktif, tunggu deployment commit tersebut selesai sebelum memicu deploy tambahan.

## Setelah deploy

1. Buka ulang aplikasi dan hard refresh (Ctrl+Shift+R), lalu login kembali. Login terputus saat restart adalah normal.
2. Pastikan footer menampilkan LifeOS v1.1.
3. Periksa tugas/catatan lama masih ada. Jangan restore backup jika data sudah ada.
4. Buka Sullamul Hifz. Mulai dari rubu Al-Qari'ah–An-Nas (14 surah, 79 ayat). Default target 20 menit, bisa diatur hingga 30 menit.
5. Catat satu sesi dan satu status ayat, refresh, periksa tersimpan.
6. Buka Idea Planner, pilih contoh bisnis/kuliah/sosial atau ide bebas, isi pertanyaan, lalu tinjau sebelum Terapkan.
7. Cek Goal, Project, Note dan Tasks yang dibuat. Tugas tidak otomatis masuk Big 3 atau Doing.
8. Download backup JSON baru (format v2). Simpan backup sebelum dan sesudah update secara terpisah.

## Migrasi data

Server menambahkan empat koleksi kosong: quran, quranSessions, plans, preferences. Koleksi lama tetap dipertahankan. Migrasi otomatis hanya sekali; revisi lama disimpan di history, lalu revisi dinaikkan untuk menolak penyimpanan tab lama.

Backup format v1 dapat direstore di v1.1. Restore mengganti seluruh state, termasuk catatan hafalan baru; lakukan hanya bila memang ingin mengganti data. Backup v2 untuk aplikasi v1.1, bukan untuk server lama.

## Jika ada masalah

- Halaman gagal setelah update: hard refresh dan pastikan `static/features.js` ikut ter-upload dan deployment memakai commit terbaru.
- Data lama tampak kosong: jangan membuat banyak data baru atau restore dahulu. Cek bahwa nama volume dan destination `/data` sama dengan sebelum update.
- Gagal menyimpan/konflik revisi: salin teks yang belum tersimpan, tutup tab lain, muat ulang dan coba lagi.
- Mengembalikan versi: sebelum rollback, backup JSON v2 dan volume. Jangan menunjuk kode server v1.0 langsung ke database yang sudah diperbarui. Cara paling aman adalah redeploy v1.1 yang diperbaiki; rollback penuh membutuhkan pemulihan backup database pra-update pada volume terpisah dan pengecekan terlebih dahulu.

## Cakupan dan batas versi ini

Sullamul Hifz hanya rubu awal Juz 30 yang telah dipilih pengguna. Tidak memuat teks ayat, pemutar murattal, unggahan/penyimpanan audio, atau seluruh jilid. Nomor ayat adalah metadata; baca dengan mushaf sendiri. Rekaman dilakukan di perangkat dan pencatatannya manual. Status mandiri berbeda dari disimak guru, tanpa verifikasi otomatis. Data guru adalah catatan pengguna, bukan tanda tangan digital.

Koreksi log sesi tidak otomatis mengubah mutabaah. Koreksi status ayat lewat tombol ayat agar riwayat sesi lama tidak menimpa penilaian terbaru. Setiap log dapat mencatat satu rentang ayat pada satu surah; jika sesi mencakup banyak surah, catat rentang utama dan rincian lain di catatan, jangan gandakan durasi.

Idea Planner adalah panduan bertanya dan template yang bisa diedit, bukan AI dan bukan jaminan hasil. Draft disimpan saat lanjut/kembali/Simpan draft, belum autosave saat mengetik. Frekuensi proses disimpan dalam catatan, belum scheduler/habit otomatis. Jadwal dan pengingat tidak berjalan otomatis di background.
