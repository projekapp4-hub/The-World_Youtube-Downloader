import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtGui import QIcon
from backend import Backend
from single import SingleTab
from playlist import PlaylistTab
from audio import AudioTab
from utils import resource_path, setup_directories, check_required_files

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Setup directories and check files
        setup_directories()
        if not check_required_files():
            print("⚠️ Application may not work properly without required binaries")
        
        self.backend = Backend()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("The World - YouTube Downloader")
        self.setGeometry(100, 100, 900, 700)
        
        # Set window icon
        self.set_window_icon()
        
        # Create stacked widget for tabs
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create tabs
        self.single_tab = SingleTab(self.backend)
        self.playlist_tab = PlaylistTab(self.backend)
        self.audio_tab = AudioTab(self.backend)
        
        # Add tabs to stacked widget FIRST
        self.stacked_widget.addWidget(self.single_tab)
        self.stacked_widget.addWidget(self.playlist_tab)
        self.stacked_widget.addWidget(self.audio_tab)
        
        # THEN connect signals
        self.connect_signals()
        
        # Load stylesheet
        self.load_stylesheet()
        
    def connect_signals(self):
        """Connect all tab switching signals"""
        try:
            # Single tab signals
            if hasattr(self.single_tab, 'switch_to_playlist'):
                self.single_tab.switch_to_playlist.connect(self.show_playlist_tab)
            if hasattr(self.single_tab, 'switch_to_audio'):
                self.single_tab.switch_to_audio.connect(self.show_audio_tab)
            
            # Playlist tab signals  
            if hasattr(self.playlist_tab, 'switch_to_single'):
                self.playlist_tab.switch_to_single.connect(self.show_single_tab)
            if hasattr(self.playlist_tab, 'switch_to_audio'):
                self.playlist_tab.switch_to_audio.connect(self.show_audio_tab)
            
            # Audio tab signals
            if hasattr(self.audio_tab, 'switch_to_single'):
                self.audio_tab.switch_to_single.connect(self.show_single_tab)
            if hasattr(self.audio_tab, 'switch_to_playlist'):
                self.audio_tab.switch_to_playlist.connect(self.show_playlist_tab)
                
            print("✅ All signals connected successfully")
        except Exception as e:
            print(f"❌ Error connecting signals: {e}")
        
    def set_window_icon(self):
        """Set icon for main window"""
        try:
            icon_path = resource_path("assets/icon.ico")
            if icon_path.exists():
                self.setWindowIcon(QIcon(str(icon_path)))
                print("✅ Logo aplikasi berhasil dimuat")
            else:
                print("⚠️ File logo tidak ditemukan:", icon_path)
        except Exception as e:
            print(f"❌ Error loading icon: {e}")
        
    def load_stylesheet(self):
        """Load stylesheet with resource_path"""
        try:
            style_path = resource_path("style/base.qss")
            style_file = QFile(str(style_path))
            if style_file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
                stream = QTextStream(style_file)
                self.setStyleSheet(stream.readAll())
                print("✅ Stylesheet loaded successfully")
        except Exception as e:
            print(f"❌ Error loading stylesheet: {e}")

    def show_single_tab(self):
        """Show single video tab"""
        self.stacked_widget.setCurrentWidget(self.single_tab)
        self.single_tab.clear_display()
        
    def show_playlist_tab(self):
        """Show playlist tab"""
        self.stacked_widget.setCurrentWidget(self.playlist_tab)
        self.playlist_tab.clear_display()
        
    def show_audio_tab(self):
        """Show audio tab"""
        self.stacked_widget.setCurrentWidget(self.audio_tab)
        self.audio_tab.clear_display()

def main():
    app = QApplication(sys.argv)
    
    # Set application properties and icon
    app.setApplicationName("The World")
    app.setApplicationVersion("1.0.0")
    app.setApplicationDisplayName("The World - YouTube Downloader")
    
    # Set application icon (for taskbar)
    try:
        icon_path = resource_path("assets/icon.ico")
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))
    except Exception as e:
        print(f"Error setting app icon: {e}")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()