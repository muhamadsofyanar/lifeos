# LifeOS v1.1

**Sudah deploy versi sebelumnya? Ikuti `UPDATE-v1.1.md`. Pertahankan volume `/data` yang sekarang.**

Versi ini menambahkan Sullamul Hifz rubu awal Juz 30 dan Idea Planner enam langkah tanpa API AI. Lihat `CHANGELOG.md`.

Aplikasi produktivitas pribadi single-user dalam bahasa Indonesia. Siap dijalankan sebagai satu container Docker di Coolify. Tidak memerlukan layanan eksternal, CDN, API berbayar, atau instalasi package saat startup.

## Yang sudah bekerja

- Login password pribadi melalui environment variable, cookie HttpOnly, CSRF, pembatasan percobaan login.
- Dashboard Today, Big 3 maksimal tiga hasil per hari.
- Inbox: capture, konversi ke tugas/catatan/proyek, aturan 2 menit, nanti, menunggu, buang.
- Tasks: Kanban, batas Doing tiga tugas, prioritas, deadline, estimasi, hasil akhir, relasi proyek, relasi tugas induk, pengulangan setelah selesai.
- Eisenhower sederhana dengan empat kategori prioritas manual (bukan dua sumbu independen).
- Projects: deskripsi, area, goal, progres berdasarkan jumlah tugas selesai dibagi seluruh tugas proyek, bobot sama termasuk subtasks.
- Notes: editor teks dengan subset tampilan Markdown (heading, bold), folder, tags, internal links `[[Judul]]`, backlinks, ekspor Markdown.
- Agenda/time blocking sederhana dalam bentuk daftar tanggal dan jam, relasi tugas opsional.
- Timer fokus berdasarkan timestamp, satu sesi aktif, durasi aktual dapat dikoreksi, energi opsional, catatan gangguan. Timer tetap dihitung saat browser tutup; alarm tidak berjalan di browser tertutup. Setelah target habis, sesi menunggu pengguna menghentikan dan mengoreksi durasi.
- Review harian, pekanan, bulanan dengan pertanyaan refleksi.
- Analytics total waktu, estimasi vs aktual per tugas; area dan goals dasar.
- Backup/restore JSON v2 seluruh data (restore v1 tetap didukung), export CSV tugas, 30 snapshot riwayat di server.
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
- Semua edit disimpan saat menekan Simpan, bukan autosave per ketikan. Jangan tutup dialog sebelum menyimpan.
- Online-first. Tidak ada service worker/offline editing/sinkronisasi antrean. Jika jaringan gagal, perubahan dibatalkan dan pesan error ditampilkan. Tidak ada refresh lintas perangkat otomatis; muat ulang untuk mengambil data terbaru. Konflik revisi ditolak, bukan digabung otomatis.
- Search hanya teks pada halaman terkait. Tidak ada pencarian global lanjutan atau graph view.
- Kalender berupa agenda daftar, belum kalender grid atau deteksi bentrok. Blok waktu harus mulai dan selesai di hari yang sama.
- Pengulangan membuat satu tugas berikutnya setelah tugas selesai dan menyimpan referensinya untuk mencegah duplikasi saat dibuka-tutup. Subtasks adalah relasi parent sederhana, tanpa roll-up otomatis.
- Waktu aktual dihitung dari sesi fokus yang dihentikan; belum ada editor waktu manual terpisah atau laporan waktu seluruh aktivitas.
- Markdown subset, tanpa HTML mentah, upload attachment atau renderer Markdown penuh. Link menggunakan judul sehingga rename membutuhkan pembaruan link manual.
- Modul Sullamul Hifz baru mencakup rubu Al-Qari’ah–An-Nas, bukan semua jilid atau seluruh 30 juz. Belum ada penyimpanan audio. Idea Planner menggunakan template dan jawaban pengguna, bukan AI.
- Belum tersedia: milestone khusus, custom dashboard, habit tracking, template builder, automations, AI, analisis keselarasan area/waktu, serta sinkronisasi kalender eksternal.
- Keamanan dasar tersedia, tetapi belum ada audit keamanan independen. Database di disk tidak terenkripsi oleh aplikasi; gunakan enkripsi/backup server sesuai kebutuhan.

Lihat `ROADMAP.md` untuk sisa cakupan PRD. Versi ini adalah fondasi operasional, bukan seluruh V1–V4 dalam PRD.

## Verifikasi

```bash
python3 -m unittest discover -s tests -v
node --check static/app.js
node --check static/features.js
node tests/test_frontend.cjs
```

Integration test memeriksa autentikasi, CSRF, penyimpanan/readback, konflik revisi, penolakan timer ganda, history, restore state dan logout. Docker image dan deployment Coolify perlu diverifikasi di server tujuan.

## Referensi deployment

- https://coolify.io/docs/applications/configuration/persistent-storage
- https://coolify.io/docs/core/networking-in-coolify
