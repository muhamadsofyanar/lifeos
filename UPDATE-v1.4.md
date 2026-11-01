# Satu kali update ke LifeOS v1.4

Paket ini KUMULATIF: mencakup seluruh source v1.0–v1.3 dan perbaikan v1.4. Tidak perlu deploy versi antara satu per satu. Data dari versi lama dimigrasikan otomatis dengan mempertahankan koleksi lama, metadata audio dan file audio.

## Sebelum update

1. Dari Settings download backup JSON.
2. Jika sudah memakai audio v1.3, download ZIP audio juga. JSON tidak berisi file audio.
3. Catat nama volume dan mount `/data`; pertahankan resource Coolify yang sekarang.
4. Tutup tab lain. Selesaikan sesi fokus bila tidak ingin sesi itu berlanjut setelah restart.

## Upload sekali, deploy sekali

Ekstrak ZIP. Pada repository yang SAMA, upload/ganti:

- `Dockerfile` (wajib versi baru).
- `server.py`, `hifz.py`, `media_store.py`, `workflow.py` (file terakhir baru).
- SELURUH isi folder `static/` dari paket ini, termasuk `consolidated.js` dan `quran-meta.json`.

`static` tetap sebagai folder, bukan seluruh file dipindahkan ke root. Tidak perlu mengganti konfigurasi `docker-compose.yml`, environment, password atau volume yang sudah berjalan. Jangan unggah `.env`, database, atau rekaman pribadi.

Commit seluruh file dalam satu commit, lalu redeploy satu kali pada resource yang sama. Jika auto-deploy Coolify aktif, tunggu deployment commit tersebut selesai; tidak perlu menekan redeploy kedua kali.

Port tetap 8000. Mount tetap `/data`. Nama volume tetap milik instalasimu sekarang. Tidak ada layanan/API/dependency baru.

## Pemeriksaan sesudah update

- Hard refresh dan login kembali. Footer harus v1.4.
- Pastikan tugas, proyek, Goal, mutabaah dan audio lama masih ada.
- Buka Today, Rutinitas, Idea Planner, Review, Calendar dan Sullamul Hifz.
- Uji satu rutinitas, satu catatan waktu manual, satu draft belum disimpan, dan satu rekaman pendek bila memakai audio.
- Download backup baru format v4 dan ZIP audio. Simpan backup pra-update juga.

Tes migrasi menggunakan database contoh v1.0/v1.1/v1.3, termasuk file/indeks audio v1.3. Itu bukan pemeriksaan langsung terhadap database servermu; tetap cek sesudah deploy.

## Cara memakai satu alur utuh

1. Inbox: tulis kebutuhan/ide.
2. Idea Planner: isi ide, gunakan **Bantu isi yang kosong** bila buntu. Ini template berdasarkan kata kunci, bukan AI. Periksa semua usulan sebelum diterapkan.
3. Terapkan rencana untuk membuat Goal, Project, Note dan Tasks.
4. Goal → Lihat arah & kemajuan → tentukan indikator (bisa lebih dari satu), lalu **Jadwalkan proses** untuk menentukan tindakan, hari dan durasi yang benar-benar bisa dijalankan.
5. Today: atur ritme, pilih Big 3, jalankan rutinitas dan catat hasil.
6. Calendar: lihat pekan, blok waktu kerja/istirahat/ibadah. Penyimpanan event memberi peringatan bila bentrok; override memerlukan centang sadar.
7. Focus: kerjakan satu tugas. Setelah dihentikan dan durasi disimpan, jeda singkat/panjang Pomodoro dimulai. Bisa diatur atau dinonaktifkan.
8. Catatan Waktu: isi aktivitas di luar timer, jangan menduplikasi sesi fokus/hafalan.
9. Review → **Review pekanan dari data aktual**, lalu tambahkan refleksi dan keputusanmu sendiri.

## Hafalan dan pengulangan

Sullamul Hifz → Jadwalkan murajaah membuat rutinitas yang dapat kamu atur. Tanggal evaluasi/gerbang yang sudah jatuh tempo muncul di Today. **Tandai sudah ditinjau** hanya menyelesaikan pengingat pemeriksaan, tidak menilai hafalan atau mengganti status ayat. Murajaah dekat/jauh dan penilaian guru masih perlu ditentukan sesuai kemampuan, bukan algoritme otomatis.

## Draft tidak sama dengan autosave server

Form editor dan form fitur mendapatkan perlindungan draft di browser ini. Setelah mengetik, draft disimpan lokal. Saat formulir dibuka lagi pada revisi server yang sama, draft dapat dipulihkan. Jika revisi berbeda, draft lama tidak otomatis menimpa isian baru; tersedia tombol pulihkan dengan sadar.

- Tetap tekan Simpan untuk menyimpan ke server.
- Tidak mendukung offline editing/sinkronisasi.
- Password/login dan file audio tidak ikut dicatat sebagai draft.
- Form rekaman memiliki perlindungan sementara sendiri; audio belum tersimpan sampai upload berhasil.
- Idea Planner tetap menyimpan draft server saat Lanjut/Kembali/Simpan draft. Tidak ada autosave per ketikan untuk planner.
- Draft lokal adalah teks pada browser ini. Pada perangkat bersama gunakan Settings → Hapus draft perangkat ini.
- Draft yang lebih lama dari 30 hari tidak dipulihkan otomatis. Kapasitas browser terbatas; status akan menjelaskan jika penyimpanan gagal.

## Batas paket ini

- Rutinitas muncul ketika aplikasi dibuka, bukan notifikasi background. Belum habit analytics lengkap.
- Kalender pekanan belum drag-and-drop atau scheduler otomatis. Bentrok dicek di editor event, bukan seluruh rutinitas dan anggaran otomatis.
- Perhitungan review menggunakan tanggal sesi/log. Tanggal selesai tugas lama yang tidak pernah dicatat tidak ditebak.
- Waktu fokus, manual dan hafalan ditampilkan terpisah; pengguna perlu menghindari duplikasi.
- Goal mendukung indikator utama lama dan indikator tambahan terpisah, masing-masing dengan satuan, kondisi awal, target dan log angka. Belum ada perhitungan otomatis ketercapaian gabungan atau rekomendasi penyebab perubahan.
- Jeda Pomodoro dimulai ketika pengguna menghentikan dan menyimpan sesi, bukan otomatis menghentikan pekerjaan saat target habis. Tidak ada alarm saat browser ditutup.
- Semua fitur audio, referensi Juz 29, peta 30 juz dan backup ZIP v1.3 tetap tersedia.
- Offline-first, AI, graph view, milestone lengkap, template builder, custom dashboard dan automation belum termasuk.

## Jika perlu membatalkan update

Jangan hapus volume. Simpan backup setelah update, lalu perbaiki source pada resource yang sama bila memungkinkan. Rollback penuh harus memakai backup pra-update pada volume terpisah; jangan menjalankan source lama langsung pada state yang sudah berubah. Backup v1/v2/v3 dapat diimpor ke v1.4, tetapi restore mengganti data aplikasi, bukan menggabungkannya. Backup v4 ditujukan untuk v1.4.
