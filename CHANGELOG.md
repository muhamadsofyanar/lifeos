# v1.8.1 — Rentang dan tampilan

- Rentang ayat dalam semua juz dan rentang baris 1–15 untuk tahap Juz 1–29.
- Ketuk ayat/unit atau Catat sesi membuka formulir rentang; sesi tahap dan S2 tetap tersedia.
- Penerapan hanya ke ayat atau unit yang tercakup utuh; unit parsial tidak ditandai selesai.
- Nomor surah pada daftar pilihan dan rujukan unit.
- Riwayat/koreksi rentang, ringkasan waktu, pemulihan draft serta bacaan/rekaman rentang ayat.
- Warna, kedalaman kartu dan animasi singkat yang mengikuti prefers-reduced-motion.

# v1.8.0 — Murajaah utuh

- Cakupan satu halaman, satu surah, satu rubu atau satu juz penuh; rentang dihitung dari metadata ayat.
- Rubu Juz 30 mengikuti buku; juz lain memakai rubu standar berlabel jelas.
- Teks Uthmani Tanzil dan font Amiri Quran lokal, pembaca RTL dengan ukuran huruf dan atribusi.
- Bacaan dan kontrol rekam dalam dialog yang sama; batas 30/60/120 menit untuk murajaah utuh, pengaman ukuran audio tetap berlaku.
- Catatan/koreksi murajaah serta hubungan audio ke cakupan sesi yang sesuai, tanpa mutabaah otomatis.
- Kompatibilitas metadata lama dan backup audio tetap dipertahankan.

# v1.7.2 — Notes dan layar kecil

- Filter folder dan tag yang dapat digabungkan dengan pencarian, hitungan hasil dan reset.
- Folder/tag berasal dari catatan lama; tanpa migrasi atau impor ulang.
- Ringkasan kartu, tombol Baca untuk isi lengkap serta backlink.
- Saran nama folder dan petunjuk tag pada editor dengan area menulis lebih luas.
- Menu utama pada layar kecil, toolbar membungkus, kartu satu kolom pada lebar menengah, form/modal lebih sesuai viewport.
- Tambahan pengujian filter, keamanan tampilan dan cakupan aset server.

# Changelog

## 1.7.1 — batas ayat dan hubungan rekaman (1 November 2026)
- Dropdown ayat dibatasi jumlah ayat surah; pilihan akhir mulai dari pilihan awal.
- Perubahan surah menyiapkan ulang pilihan rentang; pemulihan draft menyiapkan opsi sebelum mengisi nilai lama.
- Pilihan catatan latihan memuat tanggal, juz, target, durasi dan kode pembeda, dengan penyaringan per juz.
- Tombol Rekam sesi ini dari riwayat mengisi hubungan dan target secara langsung.
- Pemilihan sesi menyesuaikan target tanpa mengubah tanggal rekaman; judul pengguna dipertahankan.
- Target di luar cakupan melepas hubungan di formulir; server menolak hubungan yang hilang/salah juz/di luar rentang saat upload.
- Metadata target terstruktur disimpan pada rekaman baru, tetap kompatibel dengan metadata lama dan pemulihan ZIP audio.
- Hubungan sesi yang tidak ditemukan ditampilkan sebagai tidak tersedia, tanpa mengubah rekaman lama.

## 1.7.0 — belajar sambil menerapkan (1 November 2026)
- Menu Belajar LifeOS dengan 9 materi, sumber, contoh adaptasi dan latihan yang dapat disimpan.
- Klinik Goal SMART lima langkah: draft, pemeriksaan bahan, pratinjau dan penerapan eksplisit ke Goal baru/yang dipilih.
- Kelengkapan isian dibedakan dari bukti kelayakan; informasi yang belum diketahui tetap ditandai.
- Kartu belajar dari materi dapat dibuat satu kali, dikembangkan dan diberi jadwal review oleh pengguna.
- Bantuan kontekstual pada Tasks, Areas & Goals, Panduan serta detail Goal.
- Catatan latihan/draft memakai preferences; tidak menambah Task atau menciptakan hasil aktual secara otomatis.
- Validasi struktur catatan belajar serta pemetaan referensi Goal pada draft saat impor gabung.

## 1.6.0 — impor gabung & template (1 November 2026)
- Impor JSON dengan pemilihan jenis data, pratinjau dan penyimpanan atomik menggunakan pemeriksaan revisi.
- Data lama dipertahankan; pencocokan ID/nama/kunci memetakan kembali relasi antar-data.
- ID duplikat dalam file, referensi hilang, nama ambigu, timer aktif dan data tidak valid ditolak.
- Template kosong, contoh fiktif dan panduan kolom untuk seluruh 23 jenis data; audio melalui alur ZIP yang sudah ada.
- Isian pribadi berdasarkan percakapan: 6 Area, 14 Goal, 14 Project, 42 Task dan 15 Note; tanpa riwayat atau angka aktual buatan.
- Format paket impor dibedakan dari restore agar paket tidak keliru mengganti seluruh data.
- Regresi unit, API dan antarmuka impor ditambahkan.

## 1.5.0 — perbaikan data dan alur hafalan (1 November 2026)
- Validasi tipe data, tanggal/jam, rentang ayat, preferensi, indikator dan sesi sebelum penyimpanan/restore.
- ID pada option HTML di-escape; kegagalan render saat memuat data menampilkan jalur backup/pemulihan.
- Tanggal selesai tugas konsisten pada editor, tombol penyelesaian dan Inbox; salinan pengulangan tidak mewarisi tanggal selesai.
- Impor audio mempertahankan timestamp pembuatan asli dan memvalidasi tanggal kalender/durasi.
- Riwayat sesi lebih ringkas, tanpa pemisah/catatan kosong, penilaian saat sesi terlabel dan 20 sesi per halaman.
- Koreksi sesi ayat/unit lengkap dengan pilihan eksplisit memperbarui mutabaah; hapus catatan tidak menghapus mutabaah/audio.
- S2 mencakup dua halaman berurutan dengan penilaian sambungan terpisah; penyimak wajib untuk status guru.
- Definisi indikator baru wajib berisi satuan, baseline, target, periode dan sumber data; sumber ukur dipisahkan dari referensi Inbox planner.
- Format tanggal lokal eksplisit YYYY-MM-DD; keterangan backup audio dan daftar fitur Settings diperbarui.
- Tambahan regresi Python/JavaScript serta skrip uji browser opsional.

## 1.4.0 — paket konsolidasi
- Beberapa indikator per Goal dengan satuan dan log aktual terpisah.
- Rutinitas Process Goal dan murajaah, hari pilihan, catatan done/skip tanpa utang otomatis.
- Bantuan isi planner untuk kolom kosong berdasarkan konteks kata kunci, tetap dapat diedit dan tanpa AI.
- Ringkasan review tujuh hari dan draft review dari data aktual; tanggal selesai tugas baru dicatat.
- Catatan waktu manual, kalender pekanan dan peringatan bentrok event.
- Daily Notes dan pencarian teks lintas entitas.
- Jeda Pomodoro pendek/panjang dengan hitungan ronde, dapat diatur/dinonaktifkan.
- Draft browser editor/form fitur, pemulihan sadar saat revisi berbeda, tanpa password/file audio.
- Backup JSON v4 dan migrasi koleksi tambahan, mempertahankan audio v1.3.
- ROADMAP disatukan dan paket/panduan update kumulatif.


## 1.3.0
- Rekam mikrofon dengan negosiasi format, pratinjau, putar, unggah file, loop, download dan hapus audio.
- File audio persisten dan privat di /data/recordings, byte-range playback, indeks terpisah, validasi/kuota, deduplikasi.
- Backup dan impor ZIP audio terpisah dari backup JSON; impor tidak valid dibatalkan.
- Label 100 unit Juz 29 dari mutabaah Jilid 2; cakupan 604 halaman dari metadata Tanzil dengan atribusi.
- Dukungan CSP media-src self/blob. Dockerfile menyalin media_store.py.
- Tes backend audio, restart/persistensi, archive round-trip, autentikasi dan simulasi perekam frontend.


## 1.2.0
- Panduan alur aplikasi dan bantuan kontekstual per halaman.
- Ritme Today: anggaran kerja/belajar, tidur/istirahat, kontemplasi, Al-Qur’an, kewajiban tetap dan cadangan; peringatan Big 3 melebihi kapasitas.
- Belajar & Praktik: sumber ilmu, inti pelajaran, latihan, bukti, tugas praktik, riwayat dan tanggal review manual.
- Detail alur Project/Goal, indikator dan log angka aktual.
- Pecah tugas besar menjadi subtasks yang bisa dimulai.
- Review ditambah perasaan/beban, pengurangan pekerjaan dan pemulihan. Kalender ditambah jenis waktu.
- Sullamul Hifz seluruh 30 juz sesuai peta delapan jilid, jenis unit bertahap, delapan rubu Juz 30, evaluasi/gerbang dan tanggal murajaah.
- Backup format v3, restore v1/v2 dan migrasi tambahan koleksi.
- Dockerfile menyalin modul backend hifz.py.


## 1.1.0
- Menu Sullamul Hifz dengan rubu Al-Qari'ah–An-Nas, 79 ayat.
- Status ayat: dilatih, perlu penguatan, lancar mandiri, disimak guru.
- Mutabaah, catatan penyimak, sesi harian, koreksi durasi dan catatan, rutinitas 20–30 menit, kartu Today.
- Idea Planner enam langkah, draft persisten, template bisnis/kuliah/sosial, estimasi vs kapasitas kasar, tinjauan sebelum membuat Goal/Project/Note/Tasks.
- Tombol Urai jadi rencana dari Inbox.
- Migrasi tambahan koleksi dengan mempertahankan state lama, backup format v2 dan restore format v1.
- Perbaikan: kegagalan penyimpanan editor mempertahankan dialog, tombol aksi tidak ikut men-submit form, recurring task tidak menggandakan tugas berikutnya saat status dibuka-tutup.
- Tes migrasi ulang, restore lama, status ayat, workflow planner, dan render string halaman.

## 1.0.0
- Fondasi aplikasi pribadi, login, inbox, tugas, proyek, catatan, timer, kalender sederhana, review dan backup.
