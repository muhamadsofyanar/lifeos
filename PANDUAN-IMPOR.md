# Mengisi LifeOS sekaligus

## 1. Pasang aplikasi v1.6

Ikuti UPDATE-v1.6.md. Semua fitur lama tetap tersedia. Server aktif belum berubah hanya dengan mengunduh paket ini.

## 2. Impor isian pribadi

Buka Settings → Impor data & template → Buka impor & template. Pilih DATA-PRIBADI/ISIAN-SAYA.json dari paket ZIP. File ini dipisahkan dari source aplikasi; cukup unggah lewat dialog impor setelah aplikasi terpasang, tidak perlu diunggah ke repository.

Biarkan Area dan Goal ikut dipilih meskipun sudah diisi: pencocokan akan mempertahankan data lama dan memetakan hubungan Project/Task/Note. Buat pratinjau. Periksa nama dan jumlah data baru/dilewati, lalu klik Simpan hasil impor.

Isi maksimal paket: 6 Area, 14 Goal, 14 Project, 42 Task dan 15 Note. Jika data yang sama sudah ada, penambahannya lebih sedikit. Paket berisi rencana yang perlu ditinjau; tidak semuanya menjadi prioritas hari ini.

Tidak ada pembayaran, transaksi, hasil tes, promotor aktif, sesi belajar, nilai hafalan, deadline atau estimasi waktu yang dibuat sebagai fakta. Keinginan motor, sewa rumah dan aset disimpan sebagai catatan yang belum diperjelas, bukan Goal tambahan yang diasumsikan sudah dipilih.

## 3. Mulai satu alur

Buka Projects → IZINHUKUM — Menyusun daftar penanganan pekerjaan klien tertunda → Buka alur proyek. Lihat tugas dan catatan yang terhubung. Pilih satu tugas, tekan bintang untuk Today, kerjakan, isi hasil dalam Note, lalu tandai selesai.

## 4. Template seluruh fitur

Di dialog impor, pilih jenis data lalu unduh Template kosong, Contoh kolom fiktif, atau Panduan kolom JSON. Folder templates juga memuat contoh per jenis. Contoh per fitur menyertakan dependensi yang dibutuhkan.

Template kosong berisi array tanpa baris; gunakan contoh untuk mempelajari kolom, ganti dengan data sendiri, dan pertahankan ID yang stabil. Contoh bernama FIKTIF bukan riwayat pengguna. Contoh memakai tanggal 2000-01-01 agar jelas bukan rencana yang telah disepakati. ID khusus Quran memakai format ayat/unit yang benar. Jangan impor contoh hafalan sebagai catatan pribadi tanpa menggantinya dengan penilaian yang benar-benar dilakukan.

Jenis yang didukung: Area, Goal beserta indikator, Project, Task, Note, Inbox, Calendar, riwayat Focus yang selesai, Review, Idea Planner, pengaturan, mutabaah ayat, sesi Juz 30, mutabaah unit, sesi unit, evaluasi hafalan, kartu belajar, riwayat praktik, anggaran hari, angka indikator, rutinitas, catatan rutinitas, dan waktu manual.

Today, Analytics dan pencarian dihitung dari data tersebut. Panduan adalah konten bantuan aplikasi. File audio tetap melalui ZIP audio atau unggahan perekam; JSON tidak memuat berkas audio.

## 5. Aturan penggabungan

- Data lama tidak diedit atau dihapus. ID sama dilewati.
- Nama dibandingkan setelah normalisasi huruf besar/kecil dan spasi; bukan pencocokan samar.
- Area dibandingkan menurut nama. Goal menurut nama dan Area. Project menurut nama, Area dan Goal. Task/Note menurut nama dan Project.
- Jika nama yang berbeda sebenarnya mewakili hal yang sama, rapikan file/ID sebelum impor. Aplikasi tidak menebak kesamaan.
- Data dengan referensi hilang, nama ambigu atau nilai tidak valid ditolak sebelum penyimpanan.
- Memilih hanya sebagian fitur tetap membutuhkan data terkait yang sudah ada atau ikut diimpor.
- Impor hanya menambahkan definisi indikator ke Goal yang baru. Jika Goal lama dipertahankan, indikator baru pada paket tidak disisipkan diam-diam; log yang tidak memiliki definisi akan ditolak.
- Sesi Focus aktif tidak dimulai melalui impor. Mulai timer melalui Focus.
- File maksimal 8 MB. Audio memiliki batas dan alur tersendiri.
- Paket ini tidak digunakan melalui Restore backup.
