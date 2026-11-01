# LifeOS v1.8.0 — Murajaah utuh

## Memasang pembaruan

1. Download backup JSON dan ZIP audio melalui Settings sebelum memperbarui.
2. Unggah seluruh isi folder lifeos pada paket ini ke root repository yang digunakan Coolify. Jangan hanya menyalin JavaScript: Dockerfile, server.py, validation.py, media_store.py, quran_coverage.py, seluruh static/ dan templates/ harus berasal dari paket yang sama.
3. Pertahankan environment, password, domain dan volume /data yang sekarang. Jangan menghapus volume atau mengimpor ulang data lama.
4. Build/redeploy, lalu Ctrl+F5. Footer dan Settings harus menunjukkan LifeOS v1.8.0.
5. Periksa menggunakan CEK-v1.8.0.md. Source ini belum dipasang pada server pengguna oleh penyusun paket.

Tidak ada koleksi/database baru. Catatan murajaah memakai quranChecks dengan coverageVersion=1. Catatan evaluasi dan rekaman lama tetap didukung; metadata rekaman utuh memakai targetVersion=2. Backup JSON mencakup catatan murajaah; ZIP audio tetap diperlukan untuk file rekamannya.

## Cara menggunakan

1. Buka Sullamul Hifz dan pilih juz pada pilihan juz yang sudah ada.
2. Pada panel Murajaah utuh, pilih cakupan: Satu halaman penuh, Satu surah penuh, Satu rubu penuh, atau Satu juz penuh.
3. Pilih bagian. Periksa judul, rentang dan jumlah ayat sebelum mulai.
4. Klik Baca / rekam bagian penuh. Seluruh teks cakupan tampil di jendela yang sama dengan perekam.
5. Untuk membaca saja, langsung baca; tidak perlu mengaktifkan mikrofon. Pilih ukuran huruf jika diperlukan.
6. Untuk merekam, pilih batas waktu 30, 60, atau 120 menit sebelum Mulai rekam. Biarkan perangkat aktif dan halaman terbuka. Kontrol Mulai, Hentikan, Simpan audio dan penghitung waktu tetap terlihat saat menggulir bacaan.
7. Tekan Hentikan, dengarkan hasil, lalu Simpan audio. Membuka bacaan atau menyimpan audio tidak membuat sesi atau mengubah mutabaah.
8. Jika ingin mencatat waktu dan penilaian murajaah, tutup bacaan dan pilih Catat murajaah pada panel utama. Catat bagian penuh hanya jika seluruh bagian benar-benar dibaca/diulang. Pilih membaca dengan melihat atau mengulang dari hafalan, durasi aktual, penilaian dan penyimak jika diperlukan.
9. Catatan muncul pada Riwayat murajaah utuh. Baca / rekam lagi membuka cakupan yang sama dan memilih hubungan ke catatan itu. Hubungan hanya tersedia jika cakupan audio termasuk dalam cakupan catatan.

## Arti cakupan

- Halaman 562 utuh: Al-Mulk 1–12, sesuai metadata Mushaf Madinah 604 halaman. Berbeda dari potongan tiga baris latihan Jilid 2.
- Surah Al-Mulk utuh: 30 ayat. Surah panjang yang melewati beberapa juz tetap ditampilkan lengkap, dengan penjelasan lintas juz. Rekaman berada pada daftar juz yang dipilih ketika dibuka.
- Rubu 1 buku Juz 30: Al-Qari’ah sampai An-Nas. Delapan rubu Juz 30 tetap mengikuti buku pengguna.
- Rubu juz lain: delapan rubu standar per juz, berdasarkan pembagian seperempat hizb pada metadata Tanzil. Pembagian ini berbeda dari urutan kelompok buku Juz 30; aplikasi memberi label standar secara eksplisit.
- Juz penuh: batas ayat juz dari metadata, tanpa membatasi jumlah surah atau satu unit latihan.

## Teks bacaan dan rekaman

Teks Uthmani v1.1 berasal dari Tanzil Project, disertakan utuh dalam paket dengan atribusi/lisensi. Font Amiri Quran juga disertakan lokal. Tidak ada permintaan API eksternal saat membaca. Paket memakai nomor/cakupan halaman Madinah 604 halaman, tetapi susunan baris menyesuaikan layar. Ini bukan gambar/faksimile mushaf yang dikirim pengguna, dan tidak menjamin posisi 15 baris identik. Rujukan baris latihan tetap perlu dicocokkan dengan mushaf pengguna.

Batas ayat/cakupan divalidasi pada browser dan server; teks memiliki pemeriksaan jumlah 6.236 ayat dan SHA-256 pada browser yang mendukung Web Crypto. Bila teks gagal dimuat atau pemeriksaan integritas gagal, aplikasi menampilkan kesalahan, tanpa membuat teks pengganti.

Potongan hafalan baru tetap memakai perekam lama dengan batas 10 menit. Murajaah utuh menyediakan pilihan batas 30/60/120 menit, maksimum file 50 MB. Permintaan bitrate untuk rekaman panjang adalah 48 kbps, tetapi browser dapat memakai bitrate berbeda; pengaman ukuran menghentikan rekaman sekitar 45 MB. Karena itu pilihan 120 menit bukan jaminan seluruh perangkat merekam selama itu. Perangkat yang terkunci, browser yang ditangguhkan, izin mikrofon dan jaringan dapat memengaruhi hasil. Audio sementara dapat diunduh sebelum upload jika penyimpanan gagal. Unggah audio perangkat tetap tersedia.

Durasi catatan adalah waktu aktual yang diisi pengguna, bukan otomatis sama dengan durasi file audio. Jangan mencatat waktu yang sama lagi sebagai sesi potongan latihan karena ringkasan waktu menjumlahkan keduanya. Membaca dengan melihat, lancar mandiri dan disimak guru tetap merupakan kondisi yang berbeda.
