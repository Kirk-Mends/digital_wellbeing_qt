# from PySide6.QtWidgets import QWidget
# from PySide6.QtGui import QPainter, QPen, QColor, QFont
# from PySide6.QtCore import Qt, QTimer
# import math
# import time


# class ProgressRing(QWidget):
#     def __init__(self, engine, main_window):
#         super().__init__()

#         self.engine = engine
#         self.main = main_window

#         self.setMinimumSize(220, 220)

#         # Update every second
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update)
#         self.timer.start(1000)

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)

#         w = self.width()
#         h = self.height()
#         size = min(w, h) - 20

#         # Background circle
#         pen = QPen(QColor("#cccccc"), 14)
#         painter.setPen(pen)
#         painter.drawArc(10, 10, size, size, 0, 360 * 16)

#         # Progress
#         interval = int(self.main.settings.get("break_interval_minutes")) * 60
#         real_time = getattr(self.engine, "real_time", 0)
#         progress = min(real_time / interval if interval > 0 else 0, 1.0)

#         angle = int(progress * 360)

#         pen = QPen(QColor("#4A90E2"), 14)
#         painter.setPen(pen)
#         painter.drawArc(10, 10, size, size, 90 * 16, -angle * 16)

#         # Time text
#         minutes = int(real_time // 60)
#         seconds = int(real_time % 60)
#         text = f"{minutes:02d}:{seconds:02d}"

#         painter.setPen(QColor("#333"))
#         painter.setFont(QFont("Segoe UI", 22, QFont.Bold))
#         painter.drawText(self.rect(), Qt.AlignCenter, text)








# mac and windows

import platform # Added for OS detection
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt, QTimer
import math
import time

# --- CROSS-PLATFORM FONT LOGIC ---
if platform.system() == "Darwin":
    UI_FONT = ".AppleSystemUIFont"
else:
    UI_FONT = "Segoe UI"

class ProgressRing(QWidget):
    def __init__(self, engine, main_window):
        super().__init__()

        self.engine = engine
        self.main = main_window

        self.setMinimumSize(220, 220)

        # Update every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        size = min(w, h) - 20

        # Background circle
        pen = QPen(QColor("#cccccc"), 14)
        painter.setPen(pen)
        painter.drawArc(10, 10, size, size, 0, 360 * 16)

        # Progress
        interval = int(self.main.settings.get("break_interval_minutes")) * 60
        real_time = getattr(self.engine, "real_time", 0)
        progress = min(real_time / interval if interval > 0 else 0, 1.0)

        angle = int(progress * 360)

        pen = QPen(QColor("#4A90E2"), 14)
        painter.setPen(pen)
        painter.drawArc(10, 10, size, size, 90 * 16, -angle * 16)

        # Time text
        minutes = int(real_time // 60)
        seconds = int(real_time % 60)
        text = f"{minutes:02d}:{seconds:02d}"

        painter.setPen(QColor("#333"))
        # Corrected: Use UI_FONT variable instead of hardcoded string
        painter.setFont(QFont(UI_FONT, 22, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, text)