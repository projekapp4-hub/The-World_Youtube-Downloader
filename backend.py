import subprocess
import os
import json
from pathlib import Path
from utils import resource_path, get_bin_path
import sys

class Backend:
    def __init__(self):
        self.bin_path = get_bin_path()
        self.ytdlp_path = self.bin_path / "yt-dlp.exe"
        self.ffmpeg_path = self.bin_path / "ffmpeg.exe"
        
        print(f"📁 Binary path: {self.bin_path}")
        print(f"📄 yt-dlp path: {self.ytdlp_path.exists()}")
        print(f"📄 ffmpeg path: {self.ffmpeg_path.exists()}")
        
        # Auto update yt-dlp
        self.update_ytdlp()
        
    def update_ytdlp(self):
        """Update yt-dlp binary"""
        try:
            subprocess.run([str(self.ytdlp_path), "-U"], check=True, capture_output=True)
            print("yt-dlp updated successfully")
        except Exception as e:
            print(f"Update failed: {e}")
    
    def get_video_info(self, url):
        """Get video information"""
        cmd = [
            str(self.ytdlp_path),
            "-j",
            "--no-playlist",
            url
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error getting video info: {e}")
            print(f"stderr: {e.stderr}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def get_playlist_info(self, url):
        """Get playlist information"""
        cmd = [
            str(self.ytdlp_path),
            "-j",
            "--flat-playlist",
            url
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            videos = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        video_info = json.loads(line)
                        videos.append(video_info)
                    except json.JSONDecodeError:
                        continue
            return videos
        except subprocess.CalledProcessError as e:
            print(f"Error getting playlist info: {e}")
            print(f"stderr: {e.stderr}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def download_single(self, url, resolution, output_dir="."):
        """Download single video tanpa aria2c"""
        format_id = self._get_format_id(resolution)
        cmd = [
            str(self.ytdlp_path),
            "-f", format_id,
            "--merge-output-format", "mkv",
            "--extractor-args", "youtube:formats=dashy",
            "-N", "8",
            "--concurrent-fragments", "4",
            "--throttled-rate", "0",
            "-o", f"{output_dir}/%(title)s.%(ext)s",
            url
        ]
        
        return subprocess.Popen(cmd)
    
    def download_playlist(self, url, resolution, output_dir="."):
        """Download playlist videos tanpa aria2c"""
        format_id = self._get_format_id(resolution)
        cmd = [
            str(self.ytdlp_path),
            "-f", f"{format_id}/best",
            "--merge-output-format", "mkv",
            "--extractor-args", "youtube:formats=dashy",
            "-N", "8",
            "--concurrent-fragments", "4",
            "--throttled-rate", "0",
            "--yes-playlist",
            "-o", f"{output_dir}/%(playlist_title)s/%(title)s.%(ext)s",
            url
        ]
        
        return subprocess.Popen(cmd)
    
    def download_audio(self, url, output_dir="."):
        """Download audio only tanpa aria2c"""
        cmd = [
            str(self.ytdlp_path),
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--embed-thumbnail",
            "--add-metadata",
            "-o", f"{output_dir}/%(title)s.%(ext)s",
            url
        ]
        
        return subprocess.Popen(cmd)
    
    def _get_format_id(self, resolution):
        """Map resolution to format ID"""
        format_map = {
            "1080p60": "299+140",
            "1080p30": "137+140", 
            "720p60": "298+140",
            "720p30": "136+140",
            "480p": "135+140",
            "360p": "134+140",
            "240p": "133+140",
            "144p": "160+140"
        }
        return format_map.get(resolution, "136+140")