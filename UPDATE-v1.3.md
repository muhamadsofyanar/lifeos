# LifeOS v1.3 — rekam, putar dan penjelas bagian hafalan

## Update dari versi yang sudah berjalan

1. Download backup JSON dari Settings. Pada update pertama ini belum ada audio server versi lama.
2. Pertahankan resource Coolify, environment, compose dan volume `/data` yang sekarang.
3. Ekstrak ZIP. Upload isi folder `lifeos` pada root repository GitHub yang sama. Untuk pembaruan ini file wajib adalah:
   - `Dockerfile` — berubah agar `media_store.py` ikut masuk image.
   - `server.py`, `hifz.py`, `media_store.py` (baru).
   - `static/index.html`, `static/app.js`, `static/features.js`, `static/hifz.js`, `static/wellbeing.js`, `static/style.css`.
   - `static/recordings.js` dan `static/quran-meta.json` (baru).
4. Jangan menimpa compose yang telah kamu sesuaikan, jangan ganti nama volume, jangan unggah `.env` berisi password atau database.
5. Commit lalu Redeploy. Hard refresh, login kembali, pastikan footer v1.3.
6. Buka Sullamul Hifz. Data mutabaah lama memakai ID yang sama dan tidak diubah oleh label baru.

## Cara rekam dan putar

1. Pilih juz dan rubu/bagian. Tekan **Rekam**, atau buka nomor ayat/unit lalu **Rekam ayat/bagian ini**.
2. Pilih target yang tepat, isi tanggal/judul bila perlu.
3. Tekan **Mulai rekam** dan izinkan mikrofon pada browser. Ini memerlukan HTTPS, kecuali localhost untuk pengujian lokal.
4. Tetap buka halaman. Tekan **Hentikan**. Audio berhenti otomatis setelah sekitar 10 menit ketika browser aktif.
5. Putar pratinjau dan periksa bacaan. Kecepatan pratinjau dapat diubah. Download salinan sementara jika ingin berjaga sebelum upload.
6. Tekan **Simpan audio**. Tunggu konfirmasi. Setelah itu audio tampil pada daftar rekaman untuk juz terkait, dapat diputar lagi, diulang, didownload atau dihapus.
7. Catat sesi dan penilaian hafalan secara terpisah. Rekaman tidak otomatis dinilai lancar atau disimak guru. Sesi yang sudah ada dapat dihubungkan saat menyimpan audio.

Kalau sudah punya rekaman dari HP, gunakan pilihan **audio dari perangkat**. Format yang diterima: WebM, OGG, M4A/MP4 audio, WAV dan MP3. Format perekaman dipilih dari yang didukung browser; kemampuan memutar suatu format bisa berbeda antarperangkat. Jika rekaman tertentu tidak dapat diputar pada perangkat lain, download file dan buka dengan pemutar yang mendukung format tersebut. Aplikasi tidak melakukan transcoding.

## Penyimpanan dan backup

- Audio berada pada `/data/recordings`; indeks/metadata berada di database `/data/lifeos.db`. Tetap di volume yang sama, tidak perlu akun/API tambahan.
- File disajikan melalui endpoint yang memerlukan login. Tidak ada URL publik tanpa autentikasi.
- Batas file 50 MB; perekaman browser maksimal 10 menit per klip. Total audio aplikasi 512 MB atau 2000 rekaman. Hapus rekaman yang tidak diperlukan setelah menyimpan backup.
- **Backup JSON tidak berisi audio.** Settings menyediakan **Download ZIP audio** dan **Impor ZIP audio**. Simpan JSON dan ZIP untuk backup lengkap.
- Impor ZIP audio menggabungkan koleksi, file identik tidak diduplikasi. Tidak mengganti state tugas/Goal/mutabaah. Hanya arsip audio buatan LifeOS yang didukung, maksimal 600 MB.
- Kalau memulihkan JSON dan ZIP pada server baru, ID sesi dalam JSON dipertahankan; ID file audio dapat baru. Audio ditautkan lewat metadata sesi, bukan ID yang disisipkan ke state hafalan.
- File backup berisi rekaman dan catatan pribadi. Simpan di tempat yang kamu kendalikan.
- Backup seluruh volume dapat digunakan juga. Hentikan aplikasi atau gunakan mekanisme SQLite online backup yang benar agar file database dan audio konsisten.

## Penjelas Juz 29 dan juz lain

- Juz 29: 100 unit diberi nama surah dan rentang ayat sesuai tabel Jilid 2 unggahan pengguna. Contoh: **Al-Mulk 1–2 · Halaman 562 · baris 1–3**.
- Untuk semua 604 halaman, cakupan surah/ayat berasal dari metadata Tanzil yang dibundel. Tidak ada panggilan layanan luar saat aplikasi dipakai.
- Jika suatu unit hanya mencakup 3/5/7 baris, rentang satu halaman tidak diklaim sebagai rentang unit tersebut. Nomor baris tetap batas utama. Kecuali unit Juz 29 yang sudah dicocokkan dari tabel, batas ayat per potongan kecil belum diberikan.
- Tidak ada teks ayat atau penentuan waqaf otomatis. Baca dari mushaf sendiri dan cocokkan edisinya.

## Bila tidak bisa merekam

- Pastikan URL HTTPS, bukan HTTP biasa melalui alamat IP server.
- Periksa izin mikrofon pada ikon pengaturan situs di address bar. Pastikan mikrofon tidak sedang dikuasai aplikasi lain.
- Bila browser tidak mendukung, gunakan unggah file dari perangkat.
- Jangan mengunci HP/menutup tab saat merekam. Browser bisa menangguhkan perekaman; aplikasi tidak menjamin rekam di background.
- Saat upload gagal, pratinjau tetap dipertahankan untuk dicoba ulang atau didownload. Audio yang belum disimpan dapat hilang jika halaman ditutup/di-refresh.
- Jika upload ditolak oleh proxy Coolify, periksa batas ukuran request pada proxy. Tidak perlu mengubah environment bawaan aplikasi untuk fitur ini.

## Verifikasi yang dilakukan

Tes backend: autentikasi/CSRF, upload WAV fixture, penolakan format tak dikenal, deduplikasi, byte-range playback, file tetap ada setelah restart, backup/impor, rollback impor tidak valid dan penolakan akses anonim. Tes frontend simulasi: format pilihan browser, berhenti mikrofon, pratinjau, upload, izin ditolak dan draft dipertahankan saat upload gagal.

Belum diuji dengan mikrofon fisik atau deployment Coolify pengguna. Setelah update, uji rekaman pendek 5–10 detik, simpan, refresh lalu putar ulang sebelum memakai sesi panjang.
