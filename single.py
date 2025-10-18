from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QProgressBar,
                             QTextEdit, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
import requests
from io import BytesIO
import os

class SingleTab(QWidget):
    # Define signals at class level, not in __init__
    switch_to_playlist = pyqtSignal()
    switch_to_audio = pyqtSignal()

    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.current_video_info = None
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.btn_single = QPushButton("Single Video")
        self.btn_single.setEnabled(False)
        self.btn_playlist = QPushButton("Playlist")
        self.btn_audio = QPushButton("Audio Only")
        
        self.btn_playlist.clicked.connect(self.switch_to_playlist.emit)
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
        self.url_input.setPlaceholderText("Masukkan URL video YouTube...")
        self.url_input.setMinimumHeight(35)
        
        self.btn_next = QPushButton("Next")
        self.btn_next.setMinimumHeight(35)
        self.btn_next.clicked.connect(self.fetch_video_info)
        
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.btn_next)
        
        main_layout.addLayout(url_layout)
        main_layout.addSpacing(15)

        # Video info display (initially hidden)
        self.video_info_frame = QFrame()
        self.video_info_frame.setVisible(False)
        video_layout = QVBoxLayout()
        
        # Thumbnail and title
        info_top_layout = QHBoxLayout()
        
        # Thumbnail
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(320, 180)
        self.thumbnail_label.setStyleSheet("border: 2px solid #89b4fa; border-radius: 5px;")
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setText("Thumbnail akan muncul di sini")
        
        # Title and details
        details_layout = QVBoxLayout()
        self.title_label = QLabel("Judul: -")
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.duration_label = QLabel("Durasi: -")
        self.channel_label = QLabel("Channel: -")
        
        details_layout.addWidget(self.title_label)
        details_layout.addWidget(self.duration_label)
        details_layout.addWidget(self.channel_label)
        details_layout.addStretch()
        
        info_top_layout.addWidget(self.thumbnail_label)
        info_top_layout.addLayout(details_layout)
        
        video_layout.addLayout(info_top_layout)
        video_layout.addSpacing(10)

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
        
        video_layout.addLayout(res_layout)
        self.video_info_frame.setLayout(video_layout)
        
        main_layout.addWidget(self.video_info_frame)
        main_layout.addSpacing(15)

        # Download button
        self.download_btn = QPushButton("Download Video")
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
        self.download_btn.clicked.connect(self.download_video)
        self.download_btn.setEnabled(False)
        
        main_layout.addWidget(self.download_btn)
        main_layout.addSpacing(10)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(20)
        
        main_layout.addWidget(self.progress_bar)
        main_layout.addSpacing(10)

        # Log output
        log_label = QLabel("Log Download:")
        main_layout.addWidget(log_label)
        
        self.log_output = QTextEdit()
        self.log_output.setPlaceholderText("Log proses download akan muncul di sini...")
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumHeight(150)
        
        main_layout.addWidget(self.log_output)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def fetch_video_info(self):
        url = self.url_input.text().strip()
        if not url:
            self.show_error("Error", "URL tidak boleh kosong!")
            return

        self.btn_next.setEnabled(False)
        self.log_output.append("🔍 Mengambil informasi video...")
        
        # Get video info from backend
        self.current_video_info = self.backend.get_video_info(url)
        
        if not self.current_video_info:
            self.log_output.append("❌ Gagal mengambil informasi video. Pastikan URL valid.")
            self.btn_next.setEnabled(True)
            return

        # Display video information
        self.display_video_info()
        self.video_info_frame.setVisible(True)
        self.download_btn.setEnabled(True)
        self.btn_next.setEnabled(True)
        self.log_output.append("✅ Informasi video berhasil diambil!")

    def display_video_info(self):
        if not self.current_video_info:
            return

        # Display thumbnail
        thumbnail_url = self.current_video_info.get('thumbnail')
        if thumbnail_url:
            try:
                response = requests.get(thumbnail_url)
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                self.thumbnail_label.setPixmap(pixmap.scaled(320, 180))
            except Exception as e:
                self.log_output.append(f"⚠️ Gagal memuat thumbnail: {e}")

        # Display video details
        title = self.current_video_info.get('title', 'Tidak diketahui')
        duration = self.current_video_info.get('duration_string', 'Tidak diketahui')
        channel = self.current_video_info.get('uploader', 'Tidak diketahui')
        
        self.title_label.setText(f"Judul: {title}")
        self.duration_label.setText(f"Durasi: {duration}")
        self.channel_label.setText(f"Channel: {channel}")

    def download_video(self):
        if not self.current_video_info:
            self.show_error("Error", "Tidak ada video yang dipilih!")
            return

        url = self.url_input.text().strip()
        resolution = self.res_combo.currentText()

        self.progress_bar.setVisible(True)
        self.download_btn.setEnabled(False)
        self.log_output.append(f"🚀 Memulai download: {resolution}")

        # Start download in separate thread
        self.download_thread = DownloadThread(
            self.backend, url, resolution, 'single'
        )
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.start()

    def on_download_finished(self):
        self.progress_bar.setVisible(False)
        self.download_btn.setEnabled(True)
        self.log_output.append("✅ Download selesai!")
        
        QMessageBox.information(self, "Sukses", "Download video berhasil!")

    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)
        self.log_output.append(f"❌ {message}")

    def clear_display(self):
        """Clear all displayed information"""
        self.video_info_frame.setVisible(False)
        self.thumbnail_label.clear()
        self.thumbnail_label.setText("Thumbnail akan muncul di sini")
        self.title_label.setText("Judul: -")
        self.duration_label.setText("Durasi: -")
        self.channel_label.setText("Channel: -")
        self.download_btn.setEnabled(False)
        self.progress_bar.setVisible(False)


class DownloadThread(QThread):
    finished = pyqtSignal()
    
    def __init__(self, backend, url, resolution, download_type):
        super().__init__()
        self.backend = backend
        self.url = url
        self.resolution = resolution
        self.download_type = download_type

    def run(self):
        try:
            if self.download_type == 'single':
                process = self.backend.download_single(self.url, self.resolution)
            elif self.download_type == 'playlist':
                process = self.backend.download_playlist(self.url, self.resolution)
            elif self.download_type == 'audio':
                process = self.backend.download_audio(self.url)
            
            process.wait()
            self.finished.emit()
        except Exception as e:
            print(f"Download error: {e}")
            self.finished.emit()