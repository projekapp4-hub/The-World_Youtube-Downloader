# The-World_Youtube-Downloader

**The World** adalah aplikasi downloader video dan audio dari YouTube yang memanfaatkan `yt-dlp` sebagai backend utama serta `ffmpeg` untuk proses konversi dan manipulasi media.

## Fitur Utama
- Download video dari YouTube dengan berbagai resolusi
- Download video dari playlist public/unlisted dari youtube dengan berbagai resolusi
- Download audio saja (ekstrak dari video YouTube)
- Mendukung penggabungan dan konversi format dengan ffmpeg
- Penggunaan mudah dengan antarmuka sederhana

## Cara Kerja
Aplikasi ini menggunakan binari `yt-dlp` untuk mengekstrak dan mengunduh konten dari YouTube, kemudian memanfaatkan `ffmpeg` untuk mengolah file hasil unduhan (misal: konversi ke format lain, ekstraksi audio).

## Prasyarat
- Python 3.x
- yt-dlp (https://github.com/yt-dlp/yt-dlp)
- ffmpeg (https://ffmpeg.org/)

Pastikan kedua binari (`yt-dlp` dan `ffmpeg`) sudah tersedia di folder "bin" dan dapat diakses dari terminal/command prompt.

## Instalasi
Clone repository ini:
```bash
git clone https://github.com/projekapp4-hub/The-World_Youtube-Downloader.git
```
Instal dependensi Python jika diperlukan:
```bash
pip install -r requirements.txt
```

## Penggunaan
Contoh pemakaian sederhana:
```bash
python main.py
```
Untuk opsi dan fitur lebih lanjut, silakan cek dokumentasi atau bantuan dalam aplikasi.

## Lisensi
Aplikasi ini menggunakan MIT License dan dapat digunakan/dimodifikasi sesuai kebutuhan, dengan tetap menghormati lisensi dari yt-dlp dan ffmpeg.

## Kontribusi
Silakan ajukan issue atau pull request untuk perbaikan, penambahan fitur, atau saran pengembangan.

---
**The World** adalah solusi mudah untuk mengunduh konten YouTube secara fleksibel menggunakan kekuatan yt-dlp dan ffmpeg.
