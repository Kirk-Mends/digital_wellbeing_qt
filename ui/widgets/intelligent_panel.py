# from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtGui import QFont


# class IntelligentPanel(QWidget):
#     def __init__(self, engine, main_window):
#         super().__init__()

#         self.engine = engine
#         self.main = main_window

#         layout = QVBoxLayout(self)
#         layout.setAlignment(Qt.AlignTop)
#         layout.setSpacing(12)

#         # Card container
#         card = QFrame()
#         card.setStyleSheet("""
#             QFrame {
#                 background: #ffffff;
#                 border-radius: 12px;
#                 padding: 20px;
#                 border: 1px solid #dddddd;
#             }
#         """)
#         card_layout = QVBoxLayout(card)

#         self.behavior_label = QLabel("Behavior: —")
#         self.behavior_label.setFont(QFont("Segoe UI", 16))
#         card_layout.addWidget(self.behavior_label)

#         self.fatigue_label = QLabel("Fatigue Score: —")
#         self.fatigue_label.setFont(QFont("Segoe UI", 16))
#         card_layout.addWidget(self.fatigue_label)

#         self.reason_label = QLabel("Reason: —")
#         self.reason_label.setFont(QFont("Segoe UI", 14))
#         self.reason_label.setWordWrap(True)
#         card_layout.addWidget(self.reason_label)

#         layout.addWidget(card)

#         # Update every 2 seconds
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.refresh)
#         self.timer.start(2000)

#     def refresh(self):
#         if hasattr(self.engine, "last_decision"):
#             d = self.engine.last_decision
#             self.behavior_label.setText(f"Behavior: {d.get('behavior', '—')}")
#             self.fatigue_label.setText(f"Fatigue Score: {d.get('fatigue_score', '—')}")
#             self.reason_label.setText(f"Reason: {d.get('reason', '—')}")











# mac and windows 

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
import platform  # Added for OS detection

# --- CROSS-PLATFORM FONT LOGIC ---
if platform.system() == "Darwin":
    UI_FONT = ".AppleSystemUIFont"
else:
    UI_FONT = "Segoe UI"

class IntelligentPanel(QWidget):
    def __init__(self, engine, main_window):
        super().__init__()

        self.engine = engine
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(12)

        # Card container
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: #ffffff;
                border-radius: 12px;
                padding: 20px;
                border: 1px solid #dddddd;
            }
        """)
        card_layout = QVBoxLayout(card)

        self.behavior_label = QLabel("Behavior: —")
        self.behavior_label.setFont(QFont(UI_FONT, 16)) # Corrected
        card_layout.addWidget(self.behavior_label)

        self.fatigue_label = QLabel("Fatigue Score: —")
        self.fatigue_label.setFont(QFont(UI_FONT, 16)) # Corrected
        card_layout.addWidget(self.fatigue_label)

        self.reason_label = QLabel("Reason: —")
        self.reason_label.setFont(QFont(UI_FONT, 14)) # Corrected
        self.reason_label.setWordWrap(True)
        card_layout.addWidget(self.reason_label)

        layout.addWidget(card)

        # Update every 2 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(2000)

    def refresh(self):
        if hasattr(self.engine, "last_decision"):
            d = self.engine.last_decision
            self.behavior_label.setText(f"Behavior: {d.get('behavior', '—')}")
            self.fatigue_label.setText(f"Fatigue Score: {d.get('fatigue_score', '—')}")
            self.reason_label.setText(f"Reason: {d.get('reason', '—')}")