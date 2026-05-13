# ui/mini_video_window.py

import os

from PySide6.QtCore import Qt, QUrl, QTimer, QPropertyAnimation
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget


class MiniVideoWindow(QWidget):
    """
    Small always-on-top video window that stays visible
    even when the main app is minimized.
    Plays MP4 breathing / stepping-away / eye-blink clips.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # --- Window chrome / behavior ---
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.0)  # start invisible, fade in
        self.setFixedSize(140, 140)

        # --- Layout + video widget ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.video_widget = QVideoWidget(self)
        self.video_widget.setAttribute(Qt.WA_TranslucentBackground)
        self.video_widget.setAspectRatioMode(Qt.KeepAspectRatio)
        layout.addWidget(self.video_widget)

        # --- Media player + audio ---
        self.audio_output = QAudioOutput(self)
        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(self.video_widget)
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.0)  # silent for now

        # --- Fade animation ---
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity", self)
        self.fade_anim.setDuration(400)

        # --- Paths to videos ---
        base_dir = os.path.dirname(os.path.dirname(__file__))  # ui/
        self.videos_dir = os.path.join(base_dir,"animations", "videos")

        self.breathing_path = os.path.join(self.videos_dir, "breathing.mp4")
        self.stepping_path = os.path.join(self.videos_dir, "stepping_away.mp4")
        self.eye_blink_path = os.path.join(self.videos_dir, "eye_blink.mp4")

    # -----------------------------
    # Public API
    # -----------------------------
    def play_breathing(self, duration_ms: int = 15000):
        self._play_video(self.breathing_path, duration_ms)

    def play_stepping_away(self, duration_ms: int = 20000):
        self._play_video(self.stepping_path, duration_ms)

    def play_eye_blink(self, duration_ms: int = 5000):
        self._play_video(self.eye_blink_path, duration_ms)

    # -----------------------------
    # Core logic
    # -----------------------------
    def _play_video(self, path: str, duration_ms: int):
        if not os.path.exists(path):
            # Fail silently in production; you can log if needed
            return

        # Set media
        url = QUrl.fromLocalFile(os.path.abspath(path))
        self.player.setSource(url)
        self.player.setLoops(-1)  # loop indefinitely while visible

        # Position window near bottom-right
        self._position_bottom_right()

        # Show + fade in
        self.show()
        self._fade_in()

        # Start playback
        self.player.play()

        # Auto-close after duration
        QTimer.singleShot(duration_ms, self._fade_out_and_close)

    def _position_bottom_right(self):
        screen: QScreen = QApplication.primaryScreen()
        if not screen:
            return
        geom = screen.availableGeometry()
        x = geom.right() - self.width() - 40
        y = geom.bottom() - self.height() - 80
        self.move(x, y)

    def _fade_in(self):
        self.fade_anim.stop()
        self.fade_anim.setStartValue(self.windowOpacity())
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()

    # def _fade_out_and_close(self):
    #     self.fade_anim.stop()
    #     self.fade_anim.setStartValue(self.windowOpacity())
    #     self.fade_anim.setEndValue(0.0)
    #     self.fade_anim.finished.disconnect() if self.fade_anim.receivers(self.fade_anim.finished) else None
    #     self.fade_anim.finished.connect(self._on_fade_out_done)
    #     self.fade_anim.start()

    def _fade_out_and_close(self):
        self.fade_anim.stop()
        self.fade_anim.setStartValue(self.windowOpacity())
        self.fade_anim.setEndValue(0.0)

        # Safe disconnect
        try:
            self.fade_anim.finished.disconnect()
        except Exception:
            pass

        self.fade_anim.finished.connect(self._on_fade_out_done)
        self.fade_anim.start()


    def _on_fade_out_done(self):
        self.player.stop()
        self.hide()
