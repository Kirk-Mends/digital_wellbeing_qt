# # ui/dialogs/break_modal.py

# from PySide6.QtCore import Qt, QTimer, QEasingCurve, QPropertyAnimation, QRect
# from PySide6.QtWidgets import (
#     QDialog, QLabel, QVBoxLayout, QPushButton, QWidget, QHBoxLayout
# )
# from PySide6.QtGui import QColor, QPainter, QBrush, QFont


# class BreathingCircle(QWidget):
#     """A smooth breathing animation circle."""
#     def __init__(self, diameter=140, parent=None):
#         super().__init__(parent)
#         self.diameter = diameter
#         self.current_size = diameter * 0.6

#         # Animation: expand → contract → repeat
#         self.anim = QPropertyAnimation(self, b"size_anim")
#         self.anim.setDuration(4000)  # 4 seconds inhale/exhale
#         self.anim.setStartValue(self.diameter * 0.6)
#         self.anim.setEndValue(self.diameter)
#         self.anim.setEasingCurve(QEasingCurve.InOutQuad)
#         self.anim.setLoopCount(-1)
#         self.anim.start()

#     def get_size(self):
#         return self.current_size

#     def set_size(self, value):
#         self.current_size = value
#         self.update()

#     size_anim = property(get_size, set_size)

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)

#         # Soft calming color
#         color = QColor(90, 170, 255, 180)
#         painter.setBrush(QBrush(color))
#         painter.setPen(Qt.NoPen)

#         # Draw centered circle
#         x = (self.width() - self.current_size) / 2
#         y = (self.height() - self.current_size) / 2
#         painter.drawEllipse(x, y, self.current_size, self.current_size)


# class BreakModal(QDialog):
#     """Centered premium break modal with breathing animation + timer."""
#     def __init__(self, engine_output: dict, parent=None):
#         super().__init__(parent)

#         self.setWindowFlags(
#             Qt.Dialog |
#             Qt.FramelessWindowHint |
#             Qt.WindowStaysOnTopHint
#         )
#         self.setModal(True)
#         self.setAttribute(Qt.WA_TranslucentBackground)

#         # Extract engine output
#         behavior = engine_output.get("behavior", "Activity")
#         reason = engine_output.get("reason", "")
#         message = engine_output.get("message", "Take a moment to reset.")
#         self.break_duration = 20  # seconds (can be 20–60)

#         # Outer layout
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(40, 40, 40, 40)

#         # Background container
#         container = QWidget()
#         container.setObjectName("container")
#         container.setStyleSheet("""
#             #container {
#                 background-color: rgba(30, 30, 30, 230);
#                 border-radius: 18px;
#             }
#             QLabel {
#                 color: white;
#             }
#         """)
#         inner = QVBoxLayout(container)
#         inner.setContentsMargins(30, 30, 30, 30)
#         inner.setSpacing(18)

#         # Headline
#         headline = QLabel(f"{behavior} — {reason}" if reason else behavior)
#         headline.setFont(QFont("Segoe UI", 18, QFont.Bold))
#         headline.setAlignment(Qt.AlignCenter)
#         inner.addWidget(headline)

#         # Message
#         msg_label = QLabel(message)
#         msg_label.setFont(QFont("Segoe UI", 14))
#         msg_label.setAlignment(Qt.AlignCenter)
#         msg_label.setWordWrap(True)
#         inner.addWidget(msg_label)

#         # Breathing animation
#         self.circle = BreathingCircle(diameter=160)
#         self.circle.setFixedHeight(200)
#         inner.addWidget(self.circle, alignment=Qt.AlignCenter)

#         # Timer label
#         self.timer_label = QLabel(f"{self.break_duration} seconds")
#         self.timer_label.setFont(QFont("Segoe UI", 14))
#         self.timer_label.setAlignment(Qt.AlignCenter)
#         inner.addWidget(self.timer_label)

#         # Buttons
#         btn_row = QHBoxLayout()
#         btn_row.setSpacing(20)

#         busy_btn = QPushButton("I'm Busy")
#         busy_btn.setStyleSheet("padding: 10px 20px; font-size: 14px;")
#         busy_btn.clicked.connect(self.reject)
#         btn_row.addWidget(busy_btn)

#         close_btn = QPushButton("Close")
#         close_btn.setStyleSheet("padding: 10px 20px; font-size: 14px;")
#         close_btn.clicked.connect(self.accept)
#         btn_row.addWidget(close_btn)

#         inner.addLayout(btn_row)
#         layout.addWidget(container)

#         # Timer countdown
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_timer)
#         self.timer.start(1000)

#     def update_timer(self):
#         self.break_duration -= 1
#         if self.break_duration <= 0:
#             self.accept()
#             return
#         self.timer_label.setText(f"{self.break_duration} seconds")








# Mac and Windows

# ui/dialogs/break_modal.py

import platform  # Added to detect OS
from PySide6.QtCore import Qt, QTimer, QEasingCurve, QPropertyAnimation, QRect
from PySide6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QPushButton, QWidget, QHBoxLayout
)
from PySide6.QtGui import QColor, QPainter, QBrush, QFont

# --- CROSS-PLATFORM FONT LOGIC ---
# Resolves the 142ms delay on Mac while keeping Fluent style on Windows
if platform.system() == "Darwin":
    UI_FONT = ".AppleSystemUIFont"
else:
    UI_FONT = "Segoe UI"

class BreathingCircle(QWidget):
    """A smooth breathing animation circle."""
    def __init__(self, diameter=140, parent=None):
        super().__init__(parent)
        self.diameter = diameter
        self.current_size = diameter * 0.6

        # Animation: expand → contract → repeat
        self.anim = QPropertyAnimation(self, b"size_anim")
        self.anim.setDuration(4000)  # 4 seconds inhale/exhale
        self.anim.setStartValue(self.diameter * 0.6)
        self.anim.setEndValue(self.diameter)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.setLoopCount(-1)
        self.anim.start()

    def get_size(self):
        return self.current_size

    def set_size(self, value):
        self.current_size = value
        self.update()

    size_anim = property(get_size, set_size)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Soft calming color
        color = QColor(90, 170, 255, 180)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)

        # Draw centered circle
        x = (self.width() - self.current_size) / 2
        y = (self.height() - self.current_size) / 2
        painter.drawEllipse(x, y, self.current_size, self.current_size)


class BreakModal(QDialog):
    """Centered premium break modal with breathing animation + timer."""
    def __init__(self, engine_output: dict, parent=None):
        super().__init__(parent)

        self.setWindowFlags(
            Qt.Dialog |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )
        self.setModal(True)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Extract engine output
        behavior = engine_output.get("behavior", "Activity")
        reason = engine_output.get("reason", "")
        message = engine_output.get("message", "Take a moment to reset.")
        self.break_duration = 20  # seconds (can be 20–60)

        # Outer layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)

        # Background container
        container = QWidget()
        container.setObjectName("container")
        container.setStyleSheet("""
            #container {
                background-color: rgba(30, 30, 30, 230);
                border-radius: 18px;
            }
            QLabel {
                color: white;
            }
        """)
        inner = QVBoxLayout(container)
        inner.setContentsMargins(30, 30, 30, 30)
        inner.setSpacing(18)

        # Headline
        headline = QLabel(f"{behavior} — {reason}" if reason else behavior)
        headline.setFont(QFont(UI_FONT, 18, QFont.Bold)) # Corrected
        headline.setAlignment(Qt.AlignCenter)
        inner.addWidget(headline)

        # Message
        msg_label = QLabel(message)
        msg_label.setFont(QFont(UI_FONT, 14)) # Corrected
        msg_label.setAlignment(Qt.AlignCenter)
        msg_label.setWordWrap(True)
        inner.addWidget(msg_label)

        # Breathing animation
        self.circle = BreathingCircle(diameter=160)
        self.circle.setFixedHeight(200)
        inner.addWidget(self.circle, alignment=Qt.AlignCenter)

        # Timer label
        self.timer_label = QLabel(f"{self.break_duration} seconds")
        self.timer_label.setFont(QFont(UI_FONT, 14)) # Corrected
        self.timer_label.setAlignment(Qt.AlignCenter)
        inner.addWidget(self.timer_label)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)

        busy_btn = QPushButton("I'm Busy")
        busy_btn.setStyleSheet("padding: 10px 20px; font-size: 14px;")
        busy_btn.clicked.connect(self.reject)
        btn_row.addWidget(busy_btn)

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("padding: 10px 20px; font-size: 14px;")
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)

        inner.addLayout(btn_row)
        layout.addWidget(container)

        # Timer countdown
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def update_timer(self):
        self.break_duration -= 1
        if self.break_duration <= 0:
            self.accept()
            return
        self.timer_label.setText(f"{self.break_duration} seconds")