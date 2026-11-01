# LifeOS v1.8.0

**Sudah deploy versi sebelumnya? Ikuti `UPDATE-v1.8.0.md`. Pertahankan volume `/data` yang sekarang.**

Versi 1.6 menambahkan impor gabung dan template seluruh jenis data. Versi 1.5 memperbaiki validasi backup, keamanan atribut HTML, tanggal selesai tugas, pemulihan metadata audio, riwayat/koreksi sesi hafalan, penilaian sambungan dua halaman, dan definisi pengukuran Goal. Seluruh fitur v1.4 tetap tersedia. Lihat `LAPORAN-PERBAIKAN-v1.5.md` dan `CHANGELOG.md`.

Aplikasi produktivitas pribadi single-user dalam bahasa Indonesia. Siap dijalankan sebagai satu container Docker di Coolify. Tidak memerlukan layanan eksternal, CDN, API berbayar, atau instalasi package saat startup.

Versi 1.8.0 menambahkan murajaah halaman/surah/rubu/juz utuh, teks Uthmani lokal, catatan murajaah dan batas rekaman panjang. Baca `UPDATE-v1.8.0.md`, `CEK-v1.8.0.md` dan `LAPORAN-MURAJAAH-v1.8.0.md`.

Versi 1.7.2 menambahkan penelusuran folder/tag Notes, pembaca catatan lengkap, dan menu layar kecil. Panduan pemeriksaan tersedia di `CEK-v1.7.2.md`.

## Fitur paket gabungan

Rutinitas Process Goal, bantuan isi planner berbasis kata kunci, review dari data aktual, anggaran dan kalender pekanan, waktu manual, Daily Notes, pencarian lintas data, jeda Pomodoro, jadwal murajaah dan perlindungan draft perangkat. Baca MULAI-DI-SINI.md.

## Yang sudah bekerja

- Login password pribadi melalui environment variable, cookie HttpOnly, CSRF, pembatasan percobaan login.
- Dashboard Today, Big 3 maksimal tiga hasil per hari.
- Inbox: capture, konversi ke tugas/catatan/proyek, aturan 2 menit, nanti, menunggu, buang.
- Tasks: Kanban, batas Doing tiga tugas, prioritas, deadline, estimasi, hasil akhir, relasi proyek, relasi tugas induk, pengulangan setelah selesai.
- Eisenhower sederhana dengan empat kategori prioritas manual (bukan dua sumbu independen).
- Projects: deskripsi, area, goal, progres berdasarkan jumlah tugas selesai dibagi seluruh tugas proyek, bobot sama termasuk subtasks.
- Notes: editor teks dengan subset tampilan Markdown (heading, bold), folder, tags, internal links `[[Judul]]`, backlinks, ekspor Markdown.
- Agenda/time blocking dengan tampilan pekanan dan daftar, relasi tugas, serta peringatan bentrok pada editor.
- Timer fokus berdasarkan timestamp, satu sesi aktif, durasi aktual dapat dikoreksi, energi opsional, catatan gangguan. Timer tetap dihitung saat browser tutup; alarm tidak berjalan di browser tertutup. Setelah target habis, sesi menunggu pengguna menghentikan dan mengoreksi durasi.
- Review harian, pekanan, bulanan dengan pertanyaan refleksi.
- Analytics total waktu, estimasi vs aktual per tugas; area dan goals dasar.
- Backup/restore JSON v4 seluruh data (restore v1/v2/v3 tetap didukung), export CSV tugas, 30 snapshot riwayat di server.
- UI responsive, manifest instalasi web app. Semua data aplikasi disimpan di SQLite server, bukan hanya localStorage.

## Upload GitHub manual

1. Ekstrak ZIP ini di komputer.
2. Buat repository GitHub baru (private disarankan).
3. Pilih **Add file → Upload files**.
4. Unggah **isi folder `lifeos`**, sehingga `Dockerfile`, `server.py`, `static/`, dan `docker-compose.yml` berada di root repository, bukan di dalam folder tambahan.
5. Sertakan `.dockerignore`, `.gitignore`, dan `.env.example` bila aplikasi file browser menyembunyikan dotfiles. Jangan unggah `.env`, database, password asli, atau folder `data`.
6. Commit upload. Aplikasi ini tidak memerlukan GitHub Actions.

## Deploy Coolify: Dockerfile (jalur utama)

1. Buat Project dan Resource/Application dari repository GitHub tersebut. Hubungkan GitHub ke Coolify untuk repository private.
2. Pilih build pack **Dockerfile**, base directory `/`, lokasi Dockerfile `/Dockerfile` jika diminta.
3. Set **Ports Exposes = 8000**. Aplikasi mendengarkan `0.0.0.0:8000`. Jangan arahkan proxy ke port 80 di dalam container.
4. Tambahkan environment runtime:
   - `LIFEOS_PASSWORD`: password unik minimal 12 karakter. Jangan menggunakan nilai contoh.
   - `COOKIE_SECURE=true`.
   - `DATA_DIR=/data` (sudah menjadi default dalam image).
5. Tambahkan **Persistent Storage** berupa volume dengan destination path **`/data`**. Nama volume misalnya `lifeos-data`. Harus terpasang sebelum deploy pertama. Container berjalan sebagai UID/GID 10001; jika menggunakan bind mount, direktori host harus writable oleh UID tersebut.
6. Tetapkan domain HTTPS pada aplikasi dan aktifkan sertifikat TLS melalui Coolify.
7. Deploy. Health endpoint: `/api/health`, port 8000. Masuk dengan password dari environment.
8. Buat satu tugas, restart/redeploy aplikasi, lalu pastikan tugas masih ada untuk memverifikasi volume.

Jika menggunakan Dockerfile, Coolify tidak otomatis menggunakan volume dari docker-compose.yml. Konfigurasikan `/data` secara eksplisit di UI.

## Alternatif: Docker Compose di Coolify

Pilih resource berbasis Docker Compose dari repository, gunakan `/docker-compose.yml`, isi `LIFEOS_PASSWORD`, lalu tetapkan domain HTTPS untuk service `lifeos` dengan port internal 8000. Named volume `lifeos_data` sudah dideklarasikan di file Compose. Tidak perlu mempublikasikan database atau port host.

## Menjalankan lokal tanpa Docker

Python 3.12+, tanpa dependency tambahan:

```bash
export LIFEOS_PASSWORD='password-lokal-unik-minimal-12'
export COOKIE_SECURE=false
python3 server.py
```

Buka http://localhost:8000. `COOKIE_SECURE=false` hanya untuk HTTP lokal; pada server HTTPS gunakan `true`. Data lokal default ada di `data/lifeos.db`.

Docker lokal:

```bash
docker build -t lifeos .
docker run --rm -p 8000:8000 -e LIFEOS_PASSWORD='password-lokal-unik-minimal-12' -e COOKIE_SECURE=false -v lifeos_data:/data lifeos
```

## Backup dan pemulihan

- Buka **Settings → Download backup JSON**, simpan di perangkat lain. File ini berisi data pribadi dalam teks biasa; lindungi file tersebut.
- Restore dari Settings mengganti seluruh data setelah konfirmasi, tetap menggunakan guard revisi agar tidak menimpa perubahan tab lain.
- Volume persisten bukan backup. Untuk backup database level server, gunakan SQLite online backup API atau hentikan container sebelum menyalin seluruh direktori `/data`. Jangan hanya menyalin file `.db` yang sedang berjalan karena menggunakan WAL.
- Riwayat 30 revisi tersimpan di tabel `history`; UI hanya menampilkan metadata, belum menyediakan tombol restore snapshot. Gunakan JSON untuk restore melalui UI.
- Saat password diganti, restart/redeploy membatalkan semua sesi login. Sesi juga dibatalkan setiap restart.

## Arsitektur dan batasan

- Python standard library HTTP server di belakang reverse proxy HTTPS Coolify; SQLite WAL; frontend HTML/CSS/JavaScript tanpa build.
- Satu pengguna, satu container/replica. Tidak ada multi-user, horizontal scaling, registrasi publik, atau integrasi email.
- Penyimpanan berupa state JSON berversi di SQLite dan tabel snapshot, bukan schema relasional PostgreSQL final dalam visi PRD. Ini menyederhanakan deployment pribadi; migrasi diperlukan jika diperluas ke kolaborasi atau volume data besar.
- Data server disimpan saat menekan Simpan. Editor/form fitur memiliki draft lokal browser; ini bukan autosave server atau offline sync. Planner tetap menyimpan draft pada Lanjut/Kembali/Simpan draft.
- Online-first. Tidak ada service worker/offline editing/sinkronisasi antrean. Jika jaringan gagal, perubahan dibatalkan dan pesan error ditampilkan. Tidak ada refresh lintas perangkat otomatis; muat ulang untuk mengambil data terbaru. Konflik revisi ditolak, bukan digabung otomatis.
- Pencarian teks tersedia per halaman dan lintas entitas. Belum semantic search/advanced query atau graph view.
- Kalender berupa tampilan pekanan dan daftar; bentrok event diperingatkan saat menyimpan. Belum drag/drop atau deteksi konflik seluruh rutinitas. Blok waktu harus mulai dan selesai di hari yang sama.
- Pengulangan membuat satu tugas berikutnya setelah tugas selesai dan menyimpan referensinya untuk mencegah duplikasi saat dibuka-tutup. Subtasks adalah relasi parent sederhana, tanpa roll-up otomatis.
- Waktu aktual tersedia dari sesi fokus dan catatan manual terpisah. Hindari duplikasi. Belum audit otomatis seluruh aktivitas.
- Markdown subset, tanpa HTML mentah, upload attachment atau renderer Markdown penuh. Link menggunakan judul sehingga rename membutuhkan pembaruan link manual.
- Sullamul Hifz memetakan 30 juz dengan unit ayat/baris/halaman sesuai tahap. Lihat SOURCES-AND-DESIGN.md untuk dasar dan batas adaptasi. Tidak ada teks ayat. Audio kini disimpan terpisah pada `/data/recordings`, memerlukan backup ZIP audio selain JSON. Idea Planner menggunakan template dan jawaban pengguna, bukan AI.
- Belum tersedia: milestone khusus, custom dashboard, habit tracking, template builder, automations, AI, analisis keselarasan area/waktu, serta sinkronisasi kalender eksternal.
- Keamanan dasar tersedia, tetapi belum ada audit keamanan independen. Database di disk tidak terenkripsi oleh aplikasi; gunakan enkripsi/backup server sesuai kebutuhan.

Lihat `ROADMAP.md` untuk sisa cakupan PRD. Versi ini adalah fondasi operasional, bukan seluruh V1–V4 dalam PRD.

## Verifikasi

```bash
python3 -m unittest discover -s tests -v
node --check static/app.js
node --check static/features.js
node --check static/hifz.js
node --check static/wellbeing.js
node tests/test_frontend.cjs
node tests/test_recording_frontend.cjs
node tests/test_consolidated.cjs
node tests/test_repairs.cjs
node tests/test_transfer_ui.cjs
node tests/test_academy.cjs
node tests/test_quran_forms.cjs
```

Integration test memeriksa autentikasi, CSRF, penyimpanan/readback, konflik revisi, penolakan timer ganda, history, restore state dan logout. Docker image dan deployment Coolify perlu diverifikasi di server tujuan.

## Referensi deployment

- https://coolify.io/docs/applications/configuration/persistent-storage
- https://coolify.io/docs/core/networking-in-coolify

## Penggunaan v1.2
Buka Panduan, lalu Today untuk ritme harian. Goal → Lihat arah & kemajuan untuk indikator. Project → Buka alur proyek untuk hubungan data. Belajar & Praktik untuk mengubah ilmu menjadi tindakan dan pengulangan. Sullamul Hifz untuk seluruh peta tahap 30 juz. Tidak ada pengisian data kehidupan otomatis atau perubahan data lama tanpa tindakan pengguna.

## Audio v1.3
Lihat UPDATE-v1.3.md untuk langkah rekam/putar, batas file, kompatibilitas, dan backup. JSON saja tidak mencakup audio. HTTPS dan izin mikrofon diperlukan untuk rekaman browser. Simpan klip pendek, dengarkan, lalu beri penilaian hafalan secara terpisah.

## Status dan roadmap
ROADMAP.md adalah daftar status tunggal. Versi ZIP tidak sama dengan tahap PRD. Paket v1.4 kumulatif dan bisa langsung menggantikan versi lama tanpa deploy setiap versi antara. Jangan menimpa compose/volume/environment yang sudah dikonfigurasi.

## Pengujian browser opsional

`node tests/test_browser.cjs` memerlukan Playwright dan Chromium yang sudah terpasang pada lingkungan pengujian. Keduanya bukan dependensi runtime aplikasi. Pengujian browser belum berhasil dijalankan pada lingkungan penyusunan paket ini karena executable Chromium tidak tersedia dan unduhannya gagal. Jangan menganggap skrip ini sebagai bukti kelulusan uji browser.

## Perilaku data v1.5

Backup JSON tetap versi 4. Koleksi dan ID lama dipertahankan. Definisi pengukuran baru memakai `measurementVersion: 1`; sesi unit yang baru atau dikoreksi memakai `sessionVersion: 2`. Sesi lama tidak otomatis mendapat nilai sambungan atau tanggal penyelesaian yang belum pernah dicatat. Validasi baru menolak backup dengan tipe atau nilai yang tidak valid sebelum mengganti data.

## Impor gabung & template v1.6

Buka **Settings → Impor data & template → Buka impor & template**. Pilih paket JSON, pilih jenis data, buat pratinjau, lalu simpan hasil impor. Template kosong, contoh fiktif, dan panduan kolom dapat diunduh dari dialog tersebut.

Impor gabung menambahkan data dan mempertahankan data lama. ID yang sama dilewati. Nama/kunci yang cocok dipakai kembali sesuai cakupan: Goal dalam Area, Project dalam Area dan Goal, Task/Note dalam Project. Hubungan dalam paket dipetakan ke ID data lama yang cocok. Nama yang berbeda dapat menghasilkan baris baru, sehingga pratinjau harus diperiksa. Nama lama yang ambigu memerlukan ID tujuan yang tepat.

Backup JSON v1–4 dapat dipilih untuk digabung, dengan pemeriksaan struktur dan referensi. Referensi yang tidak tersedia harus dilengkapi atau diperbaiki; impor tidak menghapusnya secara diam-diam. Impor ulang paket yang sama tidak menambah duplikat atau revisi baru jika tidak ada penambahan.

Format paket impor memakai `kind: lifeos-import` dan `version: "1.0"` (teks). Restore backup tetap memakai versi angka. Pemisahan ini membuat paket impor ditolak oleh restore versi lama.

Paket pribadi hanya berisi rencana: 6 Area, 14 Goal, 14 Project, 42 Task berstatus todo, dan 15 Note. Tidak ada transaksi keuangan, jadwal, deadline, estimasi durasi, setoran hafalan, sesi, atau hasil aktual yang dikarang. Angka tujuan yang belum jelas tetap berupa uraian rancangan.

Contoh generik berlabel FIKTIF dapat berisi riwayat untuk menjelaskan bentuk kolom. Ubah berdasarkan kejadian nyata sebelum digunakan. JSON tidak memuat file audio; gunakan ZIP audio/unggahan perekam. Today, Analytics, dan pencarian merupakan tampilan dari data yang diimpor.

## Belajar LifeOS v1.7

Menu Belajar LifeOS menyajikan sembilan materi singkat: struktur data, klarifikasi tujuan, SMART, SGS, KPI, OKR, pemrosesan Inbox, pemilihan pekerjaan, dan review. Setiap materi memuat contoh adaptasi, latihan, pemeriksaan pemahaman dan rujukan. Catatan latihan bukan sertifikasi penguasaan atau skor produktivitas.

Klinik Goal SMART memiliki lima langkah dan pratinjau. Bahan yang belum diketahui tetap menjadi draft. Lengkapnya isian tidak membuktikan kelayakan target; semua perumusan memerlukan tinjauan pengguna. Dari detail Goal, tombol Pelajari & perjelas dengan SMART membuka Goal yang dipilih, kemudian hanya memperbaruinya setelah konfirmasi penerapan.

Materi dapat dijadikan kartu Belajar & Praktik untuk dikembangkan melalui Edit, diberi tanggal review, dan dicoba dalam pekerjaan nyata. Membuat kartu tidak membuat Task atau riwayat praktik secara otomatis. Tautan artikel membuka sumber asli; aplikasi tidak mengambil seluruh artikel atau menjalankan AI.

Materi dan alur aplikasi merupakan adaptasi tertulis yang dirujuk pada SUMBER-PEMBELAJARAN.md. SMART memakai varian Achievable/Relevant dari CDC; tidak diklaim sebagai metode eksklusif Darmawan Aji. Aplikasi menggunakan pemetaan Goal/indikator untuk memperkenalkan OKR, belum merupakan sistem OKR tim lengkap.

## Perbaikan formulir hafalan v1.7.1

Pilihan Dari ayat dan Sampai ayat memakai dropdown yang dibatasi jumlah ayat surah. Saat surah berubah, rentang dipilih ulang mulai ayat 1. Sampai ayat tidak dapat mendahului Dari ayat. Batas yang sama berlaku pada catatan sesi, koreksi sesi dan rekaman.

Catatan latihan pada perekam menampilkan tanggal, juz, surah/rentang atau unit, durasi dan kode pembeda. Tombol Rekam sesi ini pada riwayat langsung membuka perekam dengan catatan tersebut terpilih. Memilih catatan mengisi target hafalan, tetapi tidak mengubah tanggal rekaman, membuat sesi baru, atau mengubah penilaian. Judul yang ditulis pengguna dipertahankan.

Audio boleh merekam bagian yang lebih kecil dari cakupan sesi. Mengubah target ke luar cakupan melepas hubungan pada formulir dengan penjelasan. Server memeriksa hubungan saat upload. Arsip audio lama tetap dapat dipulihkan meskipun backup JSON belum dipulihkan; hubungan yang tidak tersedia ditampilkan secara jelas dan tidak ditebak.
