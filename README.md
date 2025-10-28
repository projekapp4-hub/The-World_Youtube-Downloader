# The-World_Youtube-Downloader

[Indonesia Version](README_id.md)

**The World** is a video and audio downloader application from YouTube that utilizes `yt-dlp` as its main backend and `ffmpeg` for media conversion and manipulation.

## Key Features
- Download videos from YouTube in various resolutions
- Download videos from public/unlisted YouTube playlists in various resolutions
- Download audio only (extract from YouTube videos)
- Supports merging and format conversion with ffmpeg
- Easy to use with a simple interface

## How It Works
This application uses the `yt-dlp` binary to extract and download content from YouTube, then utilizes `ffmpeg` to process the downloaded files (e.g., convert to other formats, extract audio).

## Prerequisites
- Python 3.x
- yt-dlp (https://github.com/yt-dlp/yt-dlp)
- ffmpeg (https://ffmpeg.org/)

Ensure that both binaries (`yt-dlp` and `ffmpeg`) are available in the “bin” folder and accessible from the terminal/command prompt.

## Installation
Clone this repository:
```bash
git clone https://github.com/projekapp4-hub/The-World_Youtube-Downloader.git
```
Install Python dependencies if needed:
```bash
pip install -r requirements.txt
```

## Usage
Simple usage example:
```bash
python main.py
```
For more options and features, please check the documentation or help within the application.

## License
This application uses the MIT License and can be used/modified as needed, while respecting the licenses of yt-dlp and ffmpeg.

## Contributions
Please submit issues or pull requests for improvements, feature additions, or development suggestions.

---
**The World** is an easy solution for flexibly downloading YouTube content using the power of yt-dlp and ffmpeg.


Translated with DeepL.com (free version)
