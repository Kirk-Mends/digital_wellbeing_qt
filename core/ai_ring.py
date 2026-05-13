from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt, QRectF, QTimer


class AIRing(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(160, 160)

        self.fatigue = 0          # 0–100
        self.ai_active = False    # pulsing animation
        self.pulse = 0
        self.behavior = "Idle"

        # Pulse animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_pulse)
        self.timer.start(40)

    def update_pulse(self):
        if self.ai_active:
            self.pulse = (self.pulse + 2) % 360
        else:
            self.pulse = 0
        self.update()

    def set_fatigue(self, value):
        self.fatigue = max(0, min(100, value))
        self.update()

    def set_behavior(self, text):
        self.behavior = text
        self.update()

    def set_ai_active(self, active):
        self.ai_active = active
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(10, 10, self.width() - 20, self.height() - 20)

        # -------------------------
        # OUTER AI ACTIVITY RING
        # -------------------------
        pen = QPen(QColor(0, 120, 215, 180), 8)
        painter.setPen(pen)
        painter.drawArc(rect, self.pulse * 16, 120 * 16)

        # -------------------------
        # INNER FATIGUE RING
        # -------------------------
        fatigue_color = self.fatigue_color(self.fatigue)
        pen = QPen(fatigue_color, 10)
        painter.setPen(pen)
        painter.drawArc(rect.adjusted(12, 12, -12, -12), 0, int(360 * 16 * (self.fatigue / 100)))

        # -------------------------
        # CENTER TEXT
        # -------------------------
        painter.setPen(Qt.black)
        painter.setFont(QFont("Segoe UI", 14, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.behavior)

    def fatigue_color(self, value):
        if value < 30:
            return QColor("#4CAF50")  # green
        if value < 60:
            return QColor("#FFC107")  # yellow
        if value < 85:
            return QColor("#FF9800")  # orange
        return QColor("#F44336")      # red
