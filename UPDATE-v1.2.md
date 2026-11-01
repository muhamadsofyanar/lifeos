# Update ke LifeOS v1.2 — ritme hidup, ilmu menjadi praktik, Sullamul Hifz 30 juz

## 1. Backup dulu

Di aplikasi yang sekarang, download Settings → backup JSON. Simpan backup pra-update terpisah dari backup sesudah update. Catat nama volume yang terpasang ke `/data`. Selesaikan timer yang tidak ingin dilanjutkan dan tutup tab aplikasi lain.

## 2. Upload source pada repository GitHub yang sama

Ekstrak ZIP. Upload file dari dalam folder `lifeos`, jangan menambahkan lapisan folder `lifeos` di root repository.

File yang wajib diganti/ditambahkan untuk versi ini:

1. `Dockerfile` — berubah agar modul backend baru ikut masuk image.
2. `server.py`
3. `hifz.py` — baru, wajib.
4. `static/index.html`
5. `static/app.js`
6. `static/features.js`
7. `static/hifz.js` — baru, wajib.
8. `static/wellbeing.js` — baru, wajib.
9. `static/style.css`

Upload README, tests, CHANGELOG, ROADMAP dan panduan update ini bila diinginkan. Pertahankan `docker-compose.yml` yang sudah kamu sesuaikan di server/repository, environment, nama resource, dan volume `/data`. Jangan upload password, `.env`, atau database ke GitHub.

**Berbeda dari update v1.1, Dockerfile harus ikut diganti pada v1.2.** Jika Dockerfile telah kamu modifikasi sendiri, perubahan pentingnya adalah COPY `server.py hifz.py` ke `/app/`, selain COPY seluruh folder static.

## 3. Deploy

Commit lalu Redeploy resource Coolify yang sudah ada. Port tetap 8000, environment tetap sama. Jangan hapus volume atau membuat resource pengganti yang mengarah ke volume kosong.

## 4. Periksa sesudah update

- Hard refresh, login kembali, pastikan footer v1.2.
- Periksa tugas, Goal, draft planner dan catatan hafalan lama masih ada.
- Buka Panduan untuk alur lengkap.
- Buka Today → Atur ritme hari ini. Masukkan alokasi yang sesuai kenyataan, bukan mengikuti contoh tanpa penyesuaian.
- Buka Belajar & Praktik, buat satu kartu ilmu, buat tugas praktik, lalu catat hasil.
- Buka Sullamul Hifz. Default tetap Juz 30 rubu Al-Qari'ah–An-Nas, sementara semua 30 juz bisa dipilih sesuai urutan Sullamul.
- Buka Goal → Lihat arah & kemajuan → tentukan indikator/satuan sebelum mencatat angka.
- Download backup baru format v3.

## Migrasi dan rollback

Migrasi menambahkan koleksi baru kosong, mempertahankan koleksi lama, menyimpan snapshot revisi lama dan menaikkan revisi tepat sekali. Backup v1/v2 masih bisa direstore; restore mengganti seluruh state, jadi jangan restore jika data lama sudah ada. Backup v3 ditujukan untuk v1.2.

Tes migrasi dilakukan pada database contoh v1.0 dan v1.1, bukan pada database servermu. Jika ada masalah data, jangan menghapus volume. Periksa mount dahulu. Untuk rollback, siapkan backup pra-update pada volume terpisah; jangan langsung menjalankan server lama pada database yang telah memakai schema baru.

## Batasan yang perlu dipahami

- Online-first; tombol simpan, belum autosave/offline sync. Tidak ada scheduler background atau notifikasi otomatis.
- Panduan planner berbasis pertanyaan/template. Bukan AI; tidak menghasilkan otomatis strategi bisnis dari satu kalimat.
- Alokasi Today adalah anggaran 24 jam, bukan jadwal otomatis. Istirahat mencakup tidur. Hindari menghitung satu kegiatan dalam beberapa kategori. Big 3 dibandingkan kapasitas kerja/belajar, bukan dikurangi otomatis oleh semua event kalender.
- Keahlian, kebahagiaan, dan ketenangan bukan skor yang dapat dijamin aplikasi. Review menyediakan ruang refleksi.
- Sullamul memetakan seluruh 30 juz menggunakan jenis unit sesuai tahap: ayat untuk Juz 30, baris/halaman untuk juz lain. Tidak memuat teks ayat atau file buku lengkap; baca dari mushaf sendiri.
- Tidak ada unggahan/penyimpanan audio atau penilaian tajwid otomatis. Rekam di perangkat sendiri. Penilaian mandiri dibedakan dari penyimakan guru.
- Fase adaptif mencatat per halaman dengan beban N/S/S2. Bila baru setengah halaman, statusnya latihan/penguatan, belum dianggap satu halaman lancar. Ini adaptasi digital, bukan salinan persis seluruh kolom buku.
- Tidak otomatis naik juz/tahap atau menghitung tanggal khatam. Evaluasi/gerbang dicatat manual.
- Koreksi log sesi tidak otomatis menimpa status mutabaah. Status ayat/unit dapat dikoreksi terpisah sesuai penilaian terbaru.
- Pola murajaah dan pemeriksaan guru tetap perlu disesuaikan kemampuan. Jika beban berat, kurangi hafalan baru terlebih dahulu.
