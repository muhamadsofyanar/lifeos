# Changelog

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
