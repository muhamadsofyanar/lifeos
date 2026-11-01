# Pembaruan LifeOS v1.7.1

Paket ini kumulatif dan memuat fitur versi sebelumnya, termasuk Belajar LifeOS dan impor gabung.

## Pemasangan

1. Simpan backup JSON dan ZIP audio dari aplikasi aktif.
2. Perbarui sumber menggunakan folder lifeos pada ZIP ini. Perubahan utama terdapat pada static/features.js, static/hifz.js, static/recordings.js, static/consolidated.js, static/app.js, hifz.py, server.py dan media_store.py. Gunakan file-file yang berasal dari paket yang sama agar fungsi pembantu dan validasi kompatibel.
3. Pertahankan password, domain, port dan mount volume /data. Jangan menghapus volume.
4. Build/redeploy melalui Coolify, muat ulang halaman (Ctrl+F5) dan login kembali. Footer harus menunjukkan v1.7.1.

Tidak perlu mengimpor ulang Area/Goal/Project/Task, menghapus sesi, atau memulihkan backup hanya untuk memasang pembaruan ini. Tidak ada migrasi koleksi/database baru.

Log yang diberikan pengguna menunjukkan container lama sudah dimulai; log tersebut bukan bukti deployment v1.7.1 ini. Source belum dipasang pada server aktif pengguna dari lingkungan penyusunan paket.

## Cara merekam dari catatan latihan

Buka Sullamul Hifz → pilih juz → Riwayat sesi → Rekam sesi ini. Perekam memilih catatan yang dimaksud dan mengisi targetnya. Anda dapat memilih bagian yang lebih kecil, selama masih termasuk catatan itu. Tanggal rekaman tetap mengikuti kolom tanggal; tidak otomatis disamakan dengan tanggal sesi lama.

Jika membuka perekam melalui tombol umum, pilihan hubungan menampilkan tanggal, juz, surah/rentang atau unit, durasi dan kode. Kode yang sama juga tampil pada kartu riwayat. Pilih Tanpa hubungan ke catatan latihan jika memang tidak mengaitkannya ke sesi yang sudah tercatat.

## Batas ayat

Dari ayat dan Sampai ayat kini berupa pilihan bernomor sesuai surah. Al-Qari’ah dibatasi 1–11, At-Takatsur 1–8, dan surah lain mengikuti jumlah ayatnya. Saat mengganti surah, rentang dimulai kembali dari ayat 1; pilih rentang yang sebenarnya. Mengubah Dari ayat memperbarui pilihan Sampai ayat sehingga tidak dapat lebih kecil.

## Hubungan lama dan backup

Rekaman lama tetap tersedia. Hubungan yang hilang atau tidak cocok tidak diperbaiki dengan tebakan. Jika catatan sesi tidak ditemukan, daftar audio menampilkannya sebagai tidak tersedia. Pemulihan ZIP audio tetap dapat dilakukan sebelum JSON sehingga referensi lama tidak dibuang.

Validasi hubungan baru berlaku saat upload dari perekam. Metadata baru menyimpan targetVersion 1 dan surah/from/to atau unit; metadata lama tanpa kolom tersebut tetap diterima untuk kompatibilitas.

## Pemeriksaan setelah update

1. Pada Al-Qari’ah pastikan pilihan Sampai ayat berakhir pada 11. Ganti ke At-Takatsur dan pastikan berakhir pada 8.
2. Pilih Dari ayat 5; pilihan Sampai ayat dimulai dari 5.
3. Buka Rekam sesi ini pada salah satu riwayat; periksa catatan dan target yang terpilih.
4. Ubah ke surah lain; hubungan harus dilepas dengan penjelasan.
5. Pada juz selain 30, periksa pilihan sesi hanya memuat catatan juz tersebut.
6. Putar rekaman lama untuk memeriksa volume tetap tersedia.
