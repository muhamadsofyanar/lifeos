# Update langsung ke LifeOS v1.5

Paket ini kumulatif. Tidak perlu memasang versi perantara.

## Langkah pembaruan

1. Sebelum memperbarui, unduh backup JSON dan backup ZIP audio dari Settings. JSON tidak menyertakan file audio.
2. Ganti sumber aplikasi di repository dengan seluruh isi folder `lifeos` dalam paket ini, termasuk file baru `validation.py`, Dockerfile dan seluruh folder `static`. Jangan mengunggah `.env` atau data pribadi.
3. Pada Coolify, pertahankan password, domain HTTPS, port 8000 dan volume persisten `/data` yang sama. Jangan menghapus volume. Jika memakai Dockerfile, pastikan mount `/data` tetap dikonfigurasi di Coolify.
4. Build/redeploy aplikasi. Periksa log startup dan `/api/health`, lalu muat ulang halaman browser dan login kembali.
5. Verifikasi data lama, riwayat sesi, pemutaran audio dan penyimpanan satu koreksi sesi. Pastikan footer menampilkan v1.5.

Paket ini belum dipasang pada server aktif pengguna. Build image dan deployment Coolify belum diuji pada lingkungan penyusunan paket.

## Koreksi catatan sesi

- Koreksi sesi sekarang mencakup tanggal, durasi, target dan penilaian. Pada sesi unit, beban dan sambungan juga dapat dikoreksi.
- Koreksi historis secara default hanya mengubah riwayat. Centang **Terapkan penilaian ... ke mutabaah** jika status hafalan saat ini memang perlu diubah.
- Mengganti target sesi tidak menghapus status target lama. Koreksi bagian lama melalui tombol ayat/unit bila diperlukan.
- Hapus catatan sesi tidak menghapus status mutabaah atau file audio.

## Dua halaman dan sambungan

S2 otomatis memilih halaman awal dan halaman berikutnya dalam juz yang sama. Kelancaran tiap halaman tidak otomatis berarti sambungan keduanya lancar. Pilih penilaian sambungan secara terpisah. Nama penyimak diperlukan ketika halaman atau sambungan berstatus disimak guru. Halaman terakhir suatu juz belum dapat dipasangkan otomatis dengan juz berikutnya; gunakan catatan persiapan dan evaluasi bersama penyimak.

## Indikator Goal

Definisi baru memerlukan indikator, satuan, kondisi awal, target, periode dan sumber data. Jika kondisi awal/target belum diketahui, tulis secara eksplisit dan tentukan cara mengumpulkan data. Definisi lama tetap tersimpan; lengkapi melalui Edit ukuran / Edit indikator.

## Kompatibilitas dan pemulihan

Struktur koleksi dan backup JSON tetap versi 4. Aplikasi tidak menebak tanggal selesai tugas lama, nilai sambungan sesi lama, ataupun baseline indikator. Validasi lebih ketat dapat menolak backup yang dahulu diterima meskipun rusak. Pesan error menjelaskan bagian yang perlu diperbaiki; penolakan tidak mengganti revisi/data yang tersimpan. Simpan salinan backup asli sebelum memperbaiki isinya.

Jika ada kendala setelah update, simpan log error dan backup. Sumber versi sebelumnya dapat digunakan kembali dengan volume yang sama; jangan menimpa database aktif dengan salinan file `.db` yang diambil saat SQLite masih berjalan.
