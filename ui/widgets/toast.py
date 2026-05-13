from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PySide6.QtWidgets import QGraphicsOpacityEffect



class Toast(QWidget):
    def __init__(self, message, parent=None):
        super().__init__(parent)

        self.setObjectName("Toast")
        self.setWindowFlags(
            Qt.ToolTip |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        self.label = QLabel(message)
        self.label.setObjectName("ToastLabel")
        self.label.setWordWrap(True)

        layout.addWidget(self.label)

        # Fade effect
        self.opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity)

        # Fade animation
        self.fade_anim = QPropertyAnimation(self.opacity, b"opacity")
        self.fade_anim.setDuration(400)

        # Slide animation
        self.slide_anim = QPropertyAnimation(self, b"geometry")
        self.slide_anim.setDuration(350)

        # Auto-dismiss timer
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.fade_out)

    def show_toast(self):
        # Parent window geometry
        screen = self.parent().geometry()
        width = 320
        height = self.sizeHint().height()

        # Start position (off-screen bottom-right)
        start_rect = QRect(
            screen.right() - width - 20,
            screen.bottom() - 20,
            width,
            height
        )

        # End position (slid up slightly)
        end_rect = QRect(
            screen.right() - width - 20,
            screen.bottom() - height - 40,
            width,
            height
        )

        self.setGeometry(start_rect)
        self.show()

        # Slide in
        self.slide_anim.setStartValue(start_rect)
        self.slide_anim.setEndValue(end_rect)
        self.slide_anim.start()

        # Fade in
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()

        # Auto-dismiss after 4 seconds
        self.timer.start(4000)

    def fade_out(self):
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.start()
        self.fade_anim.finished.connect(self.close)
