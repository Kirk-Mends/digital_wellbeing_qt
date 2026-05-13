from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt, QRectF


class FatigueGauge(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(120, 120)
        self.value = 0

    def set_value(self, v):
        self.value = max(0, min(100, v))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(10, 10, self.width() - 20, self.height() - 20)

        # Background arc
        pen = QPen(QColor("#DDDDDD"), 10)
        painter.setPen(pen)
        painter.drawArc(rect, 0, 360 * 16)

        # Value arc
        pen = QPen(self.color(), 10)
        painter.setPen(pen)
        painter.drawArc(rect, 90 * 16, -int(360 * 16 * (self.value / 100)))

        # Text
        painter.setPen(Qt.black)
        painter.setFont(QFont("Segoe UI", 14, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self.value}%")

    def color(self):
        if self.value < 30:
            return QColor("#4CAF50")
        if self.value < 60:
            return QColor("#FFC107")
        if self.value < 85:
            return QColor("#FF9800")
        return QColor("#F44336")
