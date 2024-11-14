import sys
import subprocess
import os
import base64
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPalette, QColor, QPixmap, QIcon
from PyQt5.QtCore import Qt, QByteArray, QBuffer

class VideoRecorderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('DRMRecPro')
        self.setGeometry(100, 100, 300, 300)  # Adjusted size for logo

        # Set dark mode theme
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(53, 53, 53))
        palette.setColor(QPalette.Button, QColor(75, 75, 75))
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        self.setPalette(palette)
        
        self.layout = QVBoxLayout()

        # Set window icon
        icon_base64 = "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"  # Replace with your base64 string
        icon_bytes = QByteArray.fromBase64(icon_base64.encode())
        icon_buffer = QBuffer()
        icon_buffer.setData(icon_bytes)
        icon_buffer.open(QBuffer.ReadOnly)
        icon_pixmap = QPixmap()
        icon_pixmap.loadFromData(icon_buffer.data())
        
        self.setWindowIcon(QIcon(icon_pixmap))

        # Set logo (optional if you want to display it within the window)
        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(icon_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo_label)

        self.start_button = QPushButton('Start Recording (F9)', self)
        self.start_button.clicked.connect(self.start_recording)
        self.layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton('Stop Recording (F8)', self)
        self.stop_button.clicked.connect(self.stop_recording)
        self.layout.addWidget(self.stop_button)
        
        self.compress_button = QPushButton('Compress Video', self)
        self.compress_button.clicked.connect(self.compress_video)
        self.layout.addWidget(self.compress_button)
        
        self.status_label = QLabel('', self)
        self.layout.addWidget(self.status_label)
        
        self.setLayout(self.layout)

        self.recording_process = None
        self.raw_output_file = 'output.avi'
        self.compressed_output_file = 'output_compressed.mp4'

        # Set keyboard shortcuts
        self.start_button.setShortcut('F9')
        self.stop_button.setShortcut('F8')

    def start_recording(self):
        if not self.recording_process:
            # First, list available audio devices
            try:
                devices = subprocess.check_output(
                    ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'],
                    stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
                print("Available devices:", devices)
            except subprocess.CalledProcessError as e:
                print("Device list output:", e.output)

            self.status_label.setText('<font color="green">Recording started...</font>')
            self.recording_process = subprocess.Popen([
                'ffmpeg',
                # Video input
                '-f', 'gdigrab', '-framerate', '60', '-i', 'desktop',
                # Audio input - using default audio device
                '-f', 'dshow', '-i', 'audio=@device_cm_{33D9A762-90C8-11D0-BD43-00A0C911CE86}\wave_{F0F4E03F-A3A5-4A9E-8F8B-A4A8D1DFA9D6}',
                # Output options
                '-c:v', 'libx264', '-b:v', '8000k',
                '-c:a', 'aac', '-b:a', '192k',
                '-pix_fmt', 'yuv420p',
                self.raw_output_file
            ])
        else:
            self.status_label.setText('<font color="yellow">Recording is already in progress.</font>')

    def stop_recording(self):
        if self.recording_process:
            self.status_label.setText('<font color="red">Stopping the recording...</font>')
            self.recording_process.terminate()
            self.recording_process.wait()
            self.recording_process = None
            self.status_label.setText('<font color="red">Recording stopped.</font>')
        else:
            self.status_label.setText('<font color="yellow">No recording in progress.</font>')

    def compress_video(self):
        if not os.path.exists(self.raw_output_file):
            self.status_label.setText('<font color="yellow">No video file to compress.</font>')
            return
        
        self.status_label.setText('<font color="blue">Compressing the video...</font>')
        try:
            subprocess.run([
                'ffmpeg', '-i', self.raw_output_file, '-vcodec', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', self.compressed_output_file
            ], check=True)
            self.status_label.setText('<font color="green">Video compression completed.</font>')
            os.remove(self.raw_output_file)  # Optionally remove the raw file
        except subprocess.CalledProcessError as e:
            self.status_label.setText(f'<font color="red">Error during compression: {e}</font>')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoRecorderApp()
    ex.show()
    sys.exit(app.exec_())
