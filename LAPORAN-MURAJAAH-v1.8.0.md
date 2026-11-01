# Verifikasi murajaah utuh

Penyebab keterbatasan sebelumnya: model input audio mengikuti satu unit hafalan bertahap (satu surah/rentang Juz 30 atau satu potongan baris/halaman juz lain), tanpa pilihan cakupan murajaah. Bacaan Arab belum disertakan dan timer berhenti pada 10 menit.

Perubahan:
- quran_coverage.py dan quran-coverage.json menentukan rentang kanonis untuk halaman, surah, rubu, dan juz. Browser dan server menolak cakupan di luar konteks juz.
- murajaah.js menyediakan pilihan, pembaca teks RTL, rekaman dalam jendela yang sama, riwayat/koreksi catatan dan hubungan audio ke catatan murajaah yang sesuai.
- Rekaman lama targetVersion=1 dan metadata tanpa versi tetap diterima. Rekaman baru targetVersion=2 memiliki scope terstruktur; label dihitung ulang server. Referensi sesi diperiksa saat upload baru, tetapi dipertahankan saat restore ZIP sehingga pemulihan audio boleh mendahului JSON.
- quranChecks dengan coverageVersion=1 menyimpan catatan murajaah tanpa mengubah status ayat/unit. Ringkasan waktu memasukkan catatan ini; audio tidak otomatis dihitung sebagai sesi tambahan.
- File teks/font disertakan dalam static agar pembaca tidak bergantung pada API eksternal. Teks raw tidak disunting. Metadata berasal dari sources/quran-data.xml yang sudah disertakan sebelumnya.

Pengujian yang dijalankan:
- 41 tes Python: cakupan kanonis, batas/tipe salah, jumlah 6.236 ayat, partisi 30 juz/rubu, validasi state, HTTP upload/putar audio empat cakupan, containment hubungan, backup/restore ZIP, serta regresi fitur lama.
- Sembilan suite JavaScript: termasuk pembaca RTL, isi halaman/surah/juz utuh, integritas teks, alur catatan/koreksi tanpa mutabaah otomatis, metadata audio v2, simulasi timer 120 menit dan upload, serta regresi fitur lama.
- Pemeriksaan sintaks semua JavaScript dan kompilasi Python.

Batas bukti:
- Simulasi timer menguji batas yang dijadwalkan; bukan uji perekaman nyata selama 120 menit.
- Percobaan menyediakan Chromium gagal karena unduhan binary tidak lengkap. Pengujian browser/visual dan mikrofon nyata belum dapat dijalankan. Font, responsivitas dialog dan kestabilan rekaman panjang masih memerlukan pemeriksaan perangkat melalui CEK-v1.8.0.md.
- Paket belum diunggah ke repository atau dideploy ke server pengguna oleh penyusun paket.

Sumber:
- https://tanzil.net/download/ — Quran Text Uthmani v1.1.
- https://tanzil.net/docs/Text_License — atribusi dan ketentuan salinan teks tanpa perubahan.
- https://tanzil.net/docs/Quran_Metadata — metadata cakupan ayat.
- https://github.com/google/fonts/tree/main/ofl/amiriquran — font Amiri Quran, SIL OFL; lisensi disertakan.
