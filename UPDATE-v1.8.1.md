# LifeOS v1.8.1 — Rentang latihan dan tampilan

## Pasang pembaruan

1. Download backup JSON dan ZIP audio melalui Settings sebelum memperbarui.
2. Unggah seluruh isi folder lifeos ke root repository yang digunakan Coolify. Sertakan Dockerfile, tracking_ranges.py, quran_coverage.py, server.py, validation.py dan seluruh static/ dari paket yang sama.
3. Pertahankan konfigurasi dan volume /data yang sekarang. Tidak perlu impor ulang atau menghapus data.
4. Build/redeploy dan Ctrl+F5. Footer serta Settings harus menunjukkan v1.8.1.

Paket belum dipasang pada server pengguna oleh penyusun paket.

## Mengisi rentang ayat

- Buka Sullamul Hifz, pilih juz, lalu + Catat rentang atau + Catat sesi.
- Mengetuk nomor ayat juga membuka formulir ini, dengan surah dan ayat awal sudah dipilih.
- Pilih Rentang ayat, nomor/nama surah, Dari ayat dan Sampai ayat. Contoh: 107. Al-Ma’un, ayat 1–3.
- Pilihan dibatasi jumlah ayat surah dan batas juz yang dipilih. Misalnya, Al-Baqarah dalam Juz 2 hanya dapat dipilih pada ayat 142–252. Mengganti surah mengatur ulang batas rentang.
- Isi durasi aktual, cara latihan, penilaian, penyimak bila disimak guru, dan catatan.
- Untuk Juz 30, centang penerapan mutabaah memperbarui setiap ayat dalam rentang. Ayat di luar rentang tidak berubah.
- Untuk Juz 1–29, rentang ayat dicatat sebagai sesi; unit baris tidak diubah otomatis karena posisi batas baris tidak sama dengan batas ayat.

## Mengisi rentang baris

- Pilih Juz 1–29. Ketuk bagian latihan, atau buka + Catat rentang lalu pilih Rentang baris mushaf.
- Pilih halaman, Dari baris dan Sampai baris (1–15). Rentang berlaku pada satu halaman per catatan. Untuk rangkaian dua halaman, formulir Sesi tahap / S2 tetap tersedia.
- Contoh Juz 29, halaman 562, baris 2–7: hanya unit baris 4–6 yang tercakup utuh. Unit 1–3 dan 7–9 tidak diubah oleh penerapan ini.
- Contoh baris 1–2: tetap dapat dicatat, tetapi tidak ada unit tiga baris utuh yang diperbarui.
- Juz 28 memakai unit lima baris, Juz 27 memakai unit 1–7/8–15, dan tahap lain mengikuti unit halaman yang sudah ada.
- Nomor baris merujuk mushaf 15 baris, bukan jumlah baris teks Arab yang menyesuaikan layar. Aplikasi tidak menebak teks untuk potongan baris yang tidak tersedia pemetaan tepatnya.

## Riwayat dan koreksi

- Simpan mencatat satu sesi berikut durasinya. Jangan mencatat latihan yang sama lagi di formulir lain karena ringkasan menjumlahkan durasi sesi yang disimpan.
- Riwayat baru berada di Riwayat rentang Juz yang dipilih. Koreksi memperbarui catatan yang sama; penerapan mutabaah tidak dicentang secara bawaan saat koreksi.
- Mengubah rentang tidak menghapus status bagian lama. Koreksi bagian lama secara eksplisit bila diperlukan.
- Riwayat ayat/unit lama tetap tersedia dan dapat dikoreksi melalui alur lama. S2 tetap tersedia melalui tombol Gunakan sesi tahap / S2.
- Dari riwayat rentang ayat, Baca / rekam rentang membuka teks dan perekam dengan cakupan yang tepat. Audio disimpan terpisah tanpa otomatis membuat catatan baru. Rekaman tersebut belum dihubungkan ke ID catatan rentang; hubungan murajaah utuh lama tetap tersedia.
- Membaca dengan melihat tidak dapat diterapkan sebagai hafalan lancar/guru pada mutabaah melalui formulir ini. Pilih dilatih/penguatan, atau simpan sebagai penilaian sesi tanpa penerapan.

Catatan rentang memakai quranChecks dengan coverageVersion=2 dan scope terstruktur. Tidak ada koleksi/database baru. Backup JSON mencakup catatan ini; fitur impor gabung dan ZIP audio tetap dipertahankan. Seluruh fitur v1.8.0 dan perbaikan Notes tetap disertakan.

## Tampilan

Kartu diberi kedalaman ringan, aksen hijau/emas, gradasi ringkasan, dan respons tombol. Dialog serta isi halaman memakai animasi masuk singkat tanpa pengulangan terus-menerus. Pengaturan sistem prefers-reduced-motion menonaktifkan animasi/transisi. Bacaan Arab tidak memakai animasi bergerak.

## Pemeriksaan setelah deploy

1. Footer v1.8.1; Notes, data dan rekaman lama tetap tersedia.
2. Ketuk ayat 1 Al-Ma’un, pilih sampai 3, isi sesi dan nilai, lalu simpan. Jika penerapan dicentang, hanya ayat 1–3 yang diperbarui.
3. Pilih Juz 29, halaman 562, baris 2–7. Simpan dengan penerapan. Hanya unit 4–6 yang diperbarui.
4. Coba baris 1–2; tidak ada unit tiga baris yang berubah. Pilihan baris tidak melebihi 15 atau lebih kecil dari awal.
5. Uji Juz 28 pada baris 1–10, Juz 27 pada 1–7, dan Juz 26 pada 1–14. Masing-masing mencakup 2, 1, dan 0 unit utuh.
6. Muat ulang, periksa riwayat rentang dan koreksi. Pastikan tidak membuat catatan ganda dan durasinya sesuai.
7. Pastikan pilihan surah memuat nomor, misalnya 67. Al-Mulk dan 107. Al-Ma’un.
8. Coba murajaah utuh, rekaman lama, sesi S2 dan filter Notes untuk memeriksa regresi.
9. Periksa HP/desktop: dialog, pilihan dan tombol tetap terjangkau. Aktifkan Reduce Motion pada perangkat; animasi aplikasi harus berhenti.

Verifikasi penyusunan: 46 tes Python dan sepuluh suite JavaScript lulus, termasuk validasi/simpan-baca HTTP, pemilihan batas dinamis, pemulihan draft, perlindungan unit parsial, nomor surah, koreksi, ringkasan durasi, serta regresi sebelumnya. Sintaks JavaScript/Python diperiksa. Browser/visual dan mikrofon nyata belum diuji karena Chromium tidak tersedia di lingkungan penyusunan; uji perangkat tetap diperlukan.
