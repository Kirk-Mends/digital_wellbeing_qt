# ui/widgets/fluent_blur.py

from PySide6.QtWidgets import QWidget, QGraphicsBlurEffect, QVBoxLayout
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainterPath

class FluentBlur(QWidget):
    """
    A translucent Fluent-style blurred background panel.
    Use this as a wrapper around any content.
    """

    def __init__(self, radius=20, opacity=0.35):
        super().__init__()

        self.opacity = opacity

        # Blur effect
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(radius)
        self.setGraphicsEffect(blur)

        # Transparent background
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

        # Layout for child widgets
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.Antialiasing)

    #     color = QColor(255, 255, 255, int(self.opacity * 255))
    #     painter.setBrush(color)
    #     painter.setPen(Qt.NoPen)

    #     painter.drawRoundedRect(self.rect(), 5, 5)



def paintEvent(self, event):
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)

    # Create custom path
    path = QPainterPath()
    r = 16  # top radius

    rect = self.rect()

    # Start at top-left corner
    path.moveTo(rect.left() + r, rect.top())

    # Top edge → top-right corner
    path.lineTo(rect.right() - r, rect.top())
    path.quadTo(rect.right(), rect.top(), rect.right(), rect.top() + r)

    # Right edge → bottom-right (square)
    path.lineTo(rect.right(), rect.bottom())

    # Bottom edge → bottom-left (square)
    path.lineTo(rect.left(), rect.bottom())

    # Left edge → top-left corner
    path.lineTo(rect.left(), rect.top() + r)
    path.quadTo(rect.left(), rect.top(), rect.left() + r, rect.top())

    # Fill
    painter.setBrush(QColor(255, 255, 255, int(self.opacity * 255)))
    painter.setPen(Qt.NoPen)
    painter.drawPath(path)
