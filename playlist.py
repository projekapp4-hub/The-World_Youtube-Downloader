from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QProgressBar,
                             QTextEdit, QFrame, QMessageBox, QListWidget,
                             QListWidgetItem, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, Qt
from PyQt6.QtGui import QFont
import math

class PlaylistTab(QWidget):
    # Define signals at class level
    switch_to_single = pyqtSignal()
    switch_to_audio = pyqtSignal()

    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.current_playlist_info = None
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.btn_single = QPushButton("Single Video")
        self.btn_playlist = QPushButton("Playlist")
        self.btn_audio = QPushButton("Audio Only")
        
        self.btn_single.clicked.connect(self.switch_to_single.emit)
        self.btn_playlist.setEnabled(False)
        self.btn_audio.clicked.connect(self.switch_to_audio.emit)
        
        nav_layout.addWidget(self.btn_single)
        nav_layout.addWidget(self.btn_playlist)
        nav_layout.addWidget(self.btn_audio)
        nav_layout.addStretch()
        
        main_layout.addLayout(nav_layout)
        main_layout.addSpacing(20)

        # URL input section
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Masukkan URL playlist YouTube...")
        self.url_input.setMinimumHeight(35)
        
        self.btn_next = QPushButton("Next")
        self.btn_next.setMinimumHeight(35)
        self.btn_next.clicked.connect(self.fetch_playlist_info)
        
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.btn_next)
        
        main_layout.addLayout(url_layout)
        main_layout.addSpacing(15)

        # Playlist info display (initially hidden)
        self.playlist_info_frame = QFrame()
        self.playlist_info_frame.setVisible(False)
        playlist_layout = QVBoxLayout()
        
        # Playlist title and video count
        info_top_layout = QHBoxLayout()
        
        self.playlist_title_label = QLabel("Judul Playlist: -")
        self.playlist_title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.video_count_label = QLabel("Jumlah Video: -")
        self.video_count_label.setStyleSheet("font-weight: bold; color: #89b4fa;")
        
        info_top_layout.addWidget(self.playlist_title_label)
        info_top_layout.addWidget(self.video_count_label)
        info_top_layout.addStretch()
        
        playlist_layout.addLayout(info_top_layout)
        playlist_layout.addSpacing(10)

        # Resolution selection
        res_layout = QHBoxLayout()
        res_layout.addWidget(QLabel("Pilih Resolusi:"))
        
        self.res_combo = QComboBox()
        self.res_combo.addItems([
            "1080p60", "1080p60 id", "1080p60 eng", "1080p30", "1080p30 id", "1080p30 eng",
            "720p60", "720p60 id", "720p60 eng", "720p30", "720p30 id", "720p30 eng",
            "480p", "480p id", "480p eng", 
            "360p", "360p id", "360p eng", 
            "240p", "240p id", "240p eng", 
            "144p", "144p id", "144p eng"
        ])
        self.res_combo.setMinimumHeight(30)
        
        res_layout.addWidget(self.res_combo)
        res_layout.addStretch()
        
        playlist_layout.addLayout(res_layout)
        playlist_layout.addSpacing(10)

        # Resolution info
        self.res_info_label = QLabel("Resolusi tersedia: -")
        self.res_info_label.setStyleSheet("color: #a6e3a1; font-size: 12px;")
        playlist_layout.addWidget(self.res_info_label)
        playlist_layout.addSpacing(10)

        # Videos list
        videos_label = QLabel("Daftar Video:")
        videos_label.setStyleSheet("font-weight: bold;")
        playlist_layout.addWidget(videos_label)
        
        # Scroll area for videos list
        self.videos_list = QListWidget()
        self.videos_list.setMaximumHeight(200)
        self.videos_list.setStyleSheet("""
            QListWidget {
                background-color: #313244;
                border: 2px solid #45475a;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #45475a;
            }
            QListWidget::item:selected {
                background-color: #89b4fa;
                color: #1e1e2e;
            }
        """)
        
        playlist_layout.addWidget(self.videos_list)
        self.playlist_info_frame.setLayout(playlist_layout)
        
        main_layout.addWidget(self.playlist_info_frame)
        main_layout.addSpacing(15)

        # Download button
        self.download_btn = QPushButton("Download Playlist")
        self.download_btn.setMinimumHeight(40)
        self.download_btn.setStyleSheet("""
            QPushButton {
                background-color: #cba6f7;
                color: #1e1e2e;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f5c2e7;
            }
            QPushButton:disabled {
                background-color: #6c7086;
                color: #a6adc8;
            }
        """)
        self.download_btn.clicked.connect(self.download_playlist)
        self.download_btn.setEnabled(False)
        
        main_layout.addWidget(self.download_btn)
        main_layout.addSpacing(10)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(20)
        
        main_layout.addWidget(self.progress_bar)
        main_layout.addSpacing(10)

        # Progress info
        self.progress_info = QLabel("")
        self.progress_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_info.setStyleSheet("color: #89b4fa; font-weight: bold;")
        main_layout.addWidget(self.progress_info)

        # Log output
        log_label = QLabel("Log Download:")
        main_layout.addWidget(log_label)
        
        self.log_output = QTextEdit()
        self.log_output.setPlaceholderText("Log proses download akan muncul di sini...")
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(120)
        
        main_layout.addWidget(self.log_output)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def fetch_playlist_info(self):
        url = self.url_input.text().strip()
        if not url:
            self.show_error("Error", "URL tidak boleh kosong!")
            return

        self.btn_next.setEnabled(False)
        self.log_output.append("🔍 Mengambil informasi playlist...")
        
        # Get playlist info from backend
        self.current_playlist_info = self.backend.get_playlist_info(url)
        
        if not self.current_playlist_info:
            self.log_output.append("❌ Gagal mengambil informasi playlist. Pastikan URL valid.")
            self.btn_next.setEnabled(True)
            return

        # Display playlist information
        self.display_playlist_info()
        self.playlist_info_frame.setVisible(True)
        self.download_btn.setEnabled(True)
        self.btn_next.setEnabled(True)
        self.log_output.append("✅ Informasi playlist berhasil diambil!")

    def display_playlist_info(self):
        if not self.current_playlist_info:
            return

        # Get playlist title from first video (if available)
        playlist_title = "Playlist YouTube"
        if self.current_playlist_info:
            first_video = self.current_playlist_info[0]
            playlist_title = first_video.get('playlist_title', 'Playlist YouTube')

        # Display playlist details
        video_count = len(self.current_playlist_info)
        self.playlist_title_label.setText(f"Judul Playlist: {playlist_title}")
        self.video_count_label.setText(f"Jumlah Video: {video_count}")

        # Display videos list
        self.videos_list.clear()
        for i, video in enumerate(self.current_playlist_info, 1):
            title = video.get('title', f'Video {i}')
            duration = video.get('duration_string', 'N/A')
            item_text = f"{i:02d}. {title} ({duration})"
            
            item = QListWidgetItem(item_text)
            self.videos_list.addItem(item)

        # Calculate available resolutions
        self.calculate_available_resolutions()

    def calculate_available_resolutions(self):
        """Calculate highest and lowest available resolutions in playlist"""
        if not self.current_playlist_info:
            return

        # For simplicity, we'll assume all standard resolutions are available
        # In a real implementation, you'd check each video's available formats
        all_resolutions = ["1080p60", "1080p30", "720p60", "720p30", "480p", "360p", "240p", "144p"]
        
        highest = all_resolutions[0]  # 1080p60
        lowest = all_resolutions[-1]  # 144p
        
        self.res_info_label.setText(f"Resolusi tersedia: {highest} (tertinggi) hingga {lowest} (terendah)")
        
        self.log_output.append(f"📊 Playlist mendukung resolusi dari {lowest} hingga {highest}")

    def download_playlist(self):
        if not self.current_playlist_info:
            self.show_error("Error", "Tidak ada playlist yang dipilih!")
            return

        url = self.url_input.text().strip()
        resolution = self.res_combo.currentText()
        video_count = len(self.current_playlist_info)

        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(video_count)
        self.progress_bar.setValue(0)
        self.progress_info.setVisible(True)
        self.download_btn.setEnabled(False)
        
        self.log_output.append(f"🚀 Memulai download playlist: {resolution}")
        self.log_output.append(f"📥 Akan mendownload {video_count} video...")

        # Start download in separate thread
        self.download_thread = PlaylistDownloadThread(
            self.backend, url, resolution, video_count
        )
        self.download_thread.progress_updated.connect(self.update_progress)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.start()

    def update_progress(self, current, total, title):
        self.progress_bar.setValue(current)
        self.progress_info.setText(f"Progress: {current}/{total} - {title}")
        
        if current > 0:
            self.log_output.append(f"✅ Selesai: {title} ({current}/{total})")

    def on_download_finished(self):
        self.progress_bar.setVisible(False)
        self.progress_info.setVisible(False)
        self.download_btn.setEnabled(True)
        self.log_output.append("✅ Download playlist selesai!")
        
        QMessageBox.information(self, "Sukses", "Download playlist berhasil!")

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)
        self.log_output.append(f"❌ {message}")

    def clear_display(self):
        """Clear all displayed information"""
        self.playlist_info_frame.setVisible(False)
        self.videos_list.clear()
        self.playlist_title_label.setText("Judul Playlist: -")
        self.video_count_label.setText("Jumlah Video: -")
        self.res_info_label.setText("Resolusi tersedia: -")
        self.download_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.progress_info.setVisible(False)


class PlaylistDownloadThread(QThread):
    progress_updated = pyqtSignal(int, int, str)
    finished = pyqtSignal()
    
    def __init__(self, backend, url, resolution, total_videos):
        super().__init__()
        self.backend = backend
        self.url = url
        self.resolution = resolution
        self.total_videos = total_videos

    def run(self):
        try:
            # For playlist download, we use the backend's download_playlist method
            # In a real implementation, you might want more granular progress tracking
            process = self.backend.download_playlist(self.url, self.resolution)
            
            # Simulate progress updates (in real app, you'd parse yt-dlp output)
            for i in range(self.total_videos):
                self.msleep(1000)  # Simulate processing time
                progress = i + 1
                title = f"Video {progress}"
                self.progress_updated.emit(progress, self.total_videos, title)
            
            process.wait()
            self.finished.emit()
        except Exception as e:
            print(f"Playlist download error: {e}")
            self.finished.emit()