import sys
import os
from pathlib import Path

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = Path(__file__).parent

    return Path(base_path) / relative_path

def get_bin_path():
    """
    Get path to bin directory
    """
    return resource_path("bin")

def get_asset_path():
    """
    Get path to assets directory  
    """
    return resource_path("assets")

def get_style_path():
    """
    Get path to style directory
    """
    return resource_path("style")

def setup_directories():
    """
    Create necessary directories if they don't exist
    """
    directories = ["bin", "assets", "style"]
    for dir_name in directories:
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
    
    print("✅ Directories setup completed")

def check_required_files():
    """
    Check if required binary files exist
    """
    required_binaries = {
        "yt-dlp.exe": "Download from: https://github.com/yt-dlp/yt-dlp/releases",
        "ffmpeg.exe": "Download from: https://ffmpeg.org/download.html"
    }
    
    bin_path = get_bin_path()
    missing_files = []
    
    for file_name, download_info in required_binaries.items():
        file_path = bin_path / file_name
        if not file_path.exists():
            missing_files.append((file_name, download_info))
    
    if missing_files:
        print("❌ Missing required binary files:")
        for file_name, download_info in missing_files:
            print(f"   - {file_name}: {download_info}")
        return False
    
    print("✅ All required binary files found")
    return True