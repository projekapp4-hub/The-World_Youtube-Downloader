# The World

## Tentang
The World adalah aplikasi youtube downloader yang menyediakan 3 fiur utama yakni download video tunggal, playlist, dan mp3 only. App ini menggunakan 2 binnary yakni yt-dlp untuk proses scrap youtube nya, FFMPEG untuk alat dukungan, dan aria2c untuk optimasi download. aplikasi ini juga menyediakan script auto update untuk yt-dlp karena sering kali mengalami error.

## Rencana Pembangunan

- lokasi \bin\yt-dlp.exe; aria2c.exe; ffmpeg.exe
- aplikasi ini akan menggunakan beberapa script.
- main.py berisi logika utama untuk menampilkan ui (PyQT6) yang akan terhubung ke semua script.
- backend.py berisi kode untuk mengatur yt-dlp, aria2c, dan ffmpeg sekaligus.
- single.py berisi ui untuk tampilan download mode tunggal, berisi juga tombol untuk pindah ke ui lain.
- playlist.py berisi ui untuk tampilan download mode playlist, berisi juga tombol untuk pindah ke ui lain.
- audio.py berisi ui untuk tampilan download mode mp3 only, berisi juga tombol untuk pindah ke ui lain.
- \style\base.qss; single.qss; playlist.qss; audio.qss berisi styling menggunakan qss untuk ui. tema blue dark magician.

## Alur Kerja Aplikasi

1. main.py secara default memuat single.py sebagai ui utama.
2. isi dari ui adalah kolom untuk input link; next button; markdown resolusi(kecuali mode audio); download button.
3. untuk single menampilkan thumnail video nya dan judul nya.
4. untuk playlist menampilkan semua judul videonya saja.
5. untuk audio menampilkan thumnail video nya dan judul nya.
6. tiap ui memiliki tombol di atas untuk berpindah ui.
7. aturan markdown resolusi di single :
 - resolusi dinamis hanya menunjukkan resolusi yang disediakan dan ukuran file.
 - 1080p 60 fps : 299 + 140 (id video dari yt dlp)
 - 1080p 30 fps : 137 + 140 (id video dari yt dlp)
 - 720p 60 fps : 298 + 140 (id video dari yt dlp)
 - 720p 30 fps : 136 + 140 (id video dari yt dlp)
 - 480p : 135 + 140 (id video dari yt dlp)
 - 360p : 134 + 140 (id video dari yt dlp)
 - 240p : 133 + 140 (id video dari yt dlp)
 - 144p : 160 + 140 (id video dari yt dlp)
8. aturan markdown resolusi di playlist :
 - resolusi dinamis hanya menunjukkan resolusi yang disediakan. Tapi karena video nya banyak, tampilkan resolusi tertinggi dan yang terendah yang ada di salah satu video. 
 - 1080p 60 fps : 299 + 140 (id video dari yt dlp)
 - 1080p 30 fps : 137 + 140 (id video dari yt dlp)
 - 720p 60 fps : 298 + 140 (id video dari yt dlp)
 - 720p 30 fps : 136 + 140 (id video dari yt dlp)
 - 480p : 135 + 140 (id video dari yt dlp)
 - 360p : 134 + 140 (id video dari yt dlp)
 - 240p : 133 + 140 (id video dari yt dlp)
 - 144p : 160 + 140 (id video dari yt dlp)
9. aturan download video di single :
 - download 2 id yang telah disediakan di dalam format lalu merge dengan ffmpeg yang hasil akhirnya adalah .mkv
 - ketika proses download menggunakan aria2c dengan perintah -x 3 -s 3 untuk memecah menjadi 3 server dan bagian agar lebih cepat.
 - direktori download langsung letakkan sejajar dengan app.
10. aturan download video di playlist :
 - download 2 id yang telah disediakan di dalam format lalu merge dengan ffmpeg yang hasil akhirnya adalah .mkv
 - ketika proses download menggunakan aria2c dengan perintah -x 3 -s 3 untuk memecah menjadi 3 server dan bagian agar lebih cepat.
 - direktori download langsung letakkan sejajar dengan app.
 - karena video banyak dan kemungkinan tidak memiliki resolusi yang sama ini tentu menjadi masalah. untuk mengatasi nya jika resolusi yang dipilih lebih tinggi dan di video lain tidak tersedia, maka untuk video yang tidak memiliki resolusi tersebut langsung secara otomatis memilh resolusi tepat di bawahnya dan terus berlanjut.
11. aturan download video di audio :
 - download id video 140 lalu format dengan ffmpeg yang hasil akhirnya adalah .mp3
 - ketika proses download menggunakan aria2c dengan perintah -x 3 -s 3 untuk memecah menjadi 3 server dan bagian agar lebih cepat.
 - direktori download langsung letakkan sejajar dengan app.
12. setiap kali app dijalankan, maka jalankan perintah yt-dlp -U untuk cek update.

## Sekian Terima Kasih