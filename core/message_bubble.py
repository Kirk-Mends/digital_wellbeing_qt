from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt


class MessageBubble(QWidget):
    def __init__(self, text, sender="ai"):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)

        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setObjectName("MessageBubble")

        if sender == "ai":
            bubble.setProperty("sender", "ai")
        else:
            bubble.setProperty("sender", "user")

        layout.addWidget(bubble)
