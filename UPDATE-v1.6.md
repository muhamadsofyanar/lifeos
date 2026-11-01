# Update LifeOS v1.6 — Impor Gabung & Template

1. Unduh backup JSON dan ZIP audio dari aplikasi yang sedang berjalan.
2. Ganti seluruh source dengan isi folder lifeos pada paket ini. Sertakan data_transfer.py, static/transfer.js, folder templates, index.html, server.py dan Dockerfile terbaru.
3. Pertahankan password, domain, port 8000 dan volume /data yang sama. Jangan menghapus atau mengganti volume.
4. Build/redeploy di Coolify, muat ulang browser dan periksa footer v1.6.
5. Buka Settings → Impor data & template → Buka impor & template. Pilih DATA-PRIBADI/ISIAN-SAYA.json dari paket, buat pratinjau lalu simpan hasil impor.

Sumber aplikasi ini belum dipasang pada server aktif pengguna. Build Docker dan uji browser nyata belum dijalankan pada lingkungan penyusunan paket.

## Data lama

Tidak ada perubahan koleksi atau migrasi database tambahan dari v1.5. Isian yang cocok dipertahankan, bukan ditimpa. Pencocokan judul mengikuti cakupannya; variasi nama dapat menghasilkan baris baru. Jika ada nama lama ganda, gunakan ID tujuan yang tepat.

Impor menolak perubahan apabila revisi sudah berubah sejak pratinjau. Muat ulang lalu buat pratinjau lagi. Impor ulang tanpa data baru tidak membuat revisi atau snapshot tambahan. Snapshot bukan backup di luar server.

File import memakai versi teks 1.0, sedangkan backup memakai versi angka. Gunakan Impor Gabung untuk isian/template. Restore backup tetap mengganti keseluruhan data setelah konfirmasi dan tidak digunakan untuk paket ini.
