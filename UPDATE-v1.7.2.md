# Pembaruan LifeOS v1.7.2

1. Sebelum memperbarui, unduh backup JSON melalui Settings dan backup audio ZIP jika memiliki rekaman.
2. Ekstrak paket dan unggah seluruh isi folder lifeos ke root repository yang digunakan Coolify. Sertakan static/notes.js, static/index.html, static/app.js, static/style.css dan server.py dari paket yang sama. Gunakan seluruh paket agar fitur versi sebelumnya tetap lengkap.
3. Pertahankan konfigurasi environment, password dan volume /data yang sekarang. Jangan menghapus atau membuat ulang volume data.
4. Build/redeploy di Coolify, lalu muat ulang browser dengan Ctrl+F5. Footer harus menunjukkan LifeOS v1.7.2. Bila masih versi lama, periksa commit deployment dan file yang diunggah.
5. Jalankan pemeriksaan dalam CEK-v1.7.2.md, termasuk data lama dan rekaman.

Tidak perlu mengimpor ulang Area, Goal, Project, Task atau Notes. Folder dan tag memakai kolom catatan yang sudah ada, tanpa migrasi database. Filter bersifat tampilan sementara dan direset ketika berpindah halaman. Tag dipisahkan koma; nama tag dan folder dipilih sesuai ejaan yang tersimpan. Tidak ada folder bertingkat atau pengubahan nama folder secara massal pada rilis ini.

Sumber ini belum dipasang pada server aktif pengguna. Log deployment yang dilampirkan menunjukkan container versi sebelumnya dimulai, belum memverifikasi pembaruan ini atau kesehatan seluruh fungsi.

## Cara memakai Notes

- Folder: satu tempat utama catatan. Contoh IZINHUKUM, STIFIN, Kuliah, TPA, atau Pribadi.
- Tags: beberapa penanda topik, dipisahkan koma. Contoh klien, tindak-lanjut, panduan.
- Klik + Catatan baru, isi judul/isi, pilih proyek jika perlu, isi folder dan tags, lalu Simpan.
- Untuk melihat catatan IZINHUKUM yang perlu follow up, pilih Folder IZINHUKUM dan Tag tindak-lanjut. Ketik kata di pencarian untuk mempersempit hasil.
- Klik tag pada kartu untuk memfilternya. Klik Reset filter untuk melihat semua catatan.
- Klik Baca untuk isi lengkap, Edit untuk mengubah, dan Markdown untuk mengunduh isi.
- Folder baru cukup diketik di formulir. Nama folder yang sudah dipakai disarankan saat mengetik.
- Layar kecil: tombol Menu membuka semua tujuan navigasi; pilih halaman dan menu menutup.

## Verifikasi penyusunan

33 pengujian Python dan delapan suite JavaScript lulus. Aset baru ikut diperiksa melalui server HTTP. Pengujian Notes mencakup filter gabungan, folder kosong, reset, data tidak berubah saat penyaringan, isi lengkap, backlink, dan escaping.

Pemeriksaan sintaks JavaScript lulus. Pengujian browser opsional diperluas untuk alur Notes dan lebar 360, 390, 768, 1440, tetapi belum dijalankan: Chromium tidak tersedia di lingkungan penyusunan. Tampilan nyata dan perilaku browser tetap perlu diperiksa menggunakan daftar cek. Jangan menganggap pengujian logika sebagai bukti tampilan sempurna di setiap perangkat.
