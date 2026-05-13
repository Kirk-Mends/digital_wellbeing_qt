from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

from ui.widgets.progress_ring import ProgressRing


class ClassicDashboard(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel("Classic Mode")
        title.setStyleSheet("font-size: 24px; font-weight: 600;")
        layout.addWidget(title)

        # Progress Ring
        self.ring = ProgressRing(self.main.hybrid_engine, self.main)
        layout.addWidget(self.ring, alignment=Qt.AlignCenter)
