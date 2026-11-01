# Verifikasi v1.7.1

Tanggal: 1 November 2026. Basis: source v1.7 yang dibuat dalam percakapan.

## Hasil

33 pengujian Python dan 7 skrip JavaScript lulus pada source pembaruan. Kompilasi Python dan pemeriksaan sintaks JavaScript juga dijalankan.

Batas ayat backend dibandingkan dengan metadata bawaan untuk seluruh 37 surah Juz 30, termasuk batas tepat dan satu ayat di atas batas. Nilai negatif, nol, boolean dan rentang terbalik ditolak.

Regresi formulir memeriksa jumlah opsi, perubahan surah, perubahan ayat awal, pemulihan draft ke surah dengan rentang lebih panjang, label sesi yang berbeda, kode untuk ID berawalan sama, penyaringan juz, sinkronisasi target, pelepasan hubungan yang tidak sesuai, judul pengguna dan informasi sesi yang hilang.

Integrasi HTTP memeriksa penolakan hubungan salah/hilang, penyimpanan target terstruktur, serta pemulihan ZIP audio dengan referensi sesi yang belum tersedia. Pengujian lama mencakup penyimpanan, migrasi, backup, impor gabung dan pembelajaran.

## Batas

Pengujian antarmuka menggunakan fixture DOM di Node VM, bukan browser nyata. Uji mikrofon/browser nyata, Docker build dan deployment Coolify belum diverifikasi pada lingkungan ini. Source belum diterapkan ke server aktif pengguna. Database asli pengguna tidak diakses.

Tidak ada perubahan otomatis terhadap sesi atau hubungan rekaman lama. Pemeriksaan rentang pada upload baru tidak menggantikan pemeriksaan bacaan oleh penyimak.
