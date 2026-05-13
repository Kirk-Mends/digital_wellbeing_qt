# from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtGui import QFont
# import time


# class LiveTimer(QWidget):
#     def __init__(self, engine, main_window):
#         super().__init__()

#         self.engine = engine
#         self.main = main_window

#         layout = QVBoxLayout(self)
#         layout.setAlignment(Qt.AlignCenter)

#         self.label = QLabel("00:00")
#         self.label.setFont(QFont("Segoe UI", 32, QFont.Bold))
#         layout.addWidget(self.label)

#         # Update every second
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_timer)
#         self.timer.start(1000)

#     def update_timer(self):
#         real_time = getattr(self.engine, "real_time", 0)
#         minutes = int(real_time // 60)
#         seconds = int(real_time % 60)
#         self.label.setText(f"{minutes:02d}:{seconds:02d}")


















# #26th
# from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtGui import QFont, QColor
# from PySide6.QtWidgets import QGraphicsDropShadowEffect

# class LiveTimer(QWidget):
#     def __init__(self, engine, main_window):
#         super().__init__()
#         self.engine = engine
#         self.main = main_window

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(0, 0, 0, 0)
        
#         # 1. PREMIUM TYPOGRAPHY
#         self.label = QLabel("00:00")
#         # 'Segoe UI Variable' or 'Inter' with SemiBold is more modern
#         font = QFont("Segoe UI Variable Display", 36, QFont.DemiBold)
#         # Use Monospaced digits so the timer doesn't 'shake'
#         font.setStyleStrategy(QFont.PreferAntialias)
#         self.label.setFont(font)
#         self.label.setAlignment(Qt.AlignCenter)
        
#         # 2. ADAPTIVE COLORING (Premium Look)
#         self.label.setStyleSheet("color: #0078D4; letter-spacing: 2px;")

#         # 3. SUBTLE GLOW EFFECT
#         glow = QGraphicsDropShadowEffect()
#         glow.setBlurRadius(15)
#         glow.setColor(QColor(0, 120, 212, 80)) # Subtle blue glow
#         glow.setOffset(0, 0)
#         self.label.setGraphicsEffect(glow)

#         layout.addWidget(self.label)

#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_timer)
#         self.timer.start(1000)

#     def update_timer(self):
#         real_time = getattr(self.engine, "real_time", 0)
#         minutes = int(real_time // 60)
#         seconds = int(real_time % 60)
        
#         # 4. OPTIONAL: Change color to Red if screen time is too high
#         if minutes >= 60:
#             self.label.setStyleSheet("color: #FF4B4B;")
            
#         self.label.setText(f"{minutes:02d}:{seconds:02d}")







# mac and windows version

#26th
import platform  # Added for OS detection
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect

# --- CROSS-PLATFORM FONT LOGIC ---
if platform.system() == "Darwin":
    UI_FONT = ".AppleSystemUIFont"
else:
    UI_FONT = "Segoe UI Variable Display"

class LiveTimer(QWidget):
    def __init__(self, engine, main_window):
        super().__init__()
        self.engine = engine
        self.main = main_window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 1. PREMIUM TYPOGRAPHY
        self.label = QLabel("00:00")
        # Corrected: Use UI_FONT variable instead of hardcoded string
        font = QFont(UI_FONT, 36, QFont.DemiBold)
        
        # Use Monospaced digits so the timer doesn't 'shake'
        font.setStyleStrategy(QFont.PreferAntialias)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        
        # 2. ADAPTIVE COLORING (Premium Look)
        self.label.setStyleSheet("color: #0078D4; letter-spacing: 2px;")

        # 3. SUBTLE GLOW EFFECT
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(15)
        glow.setColor(QColor(0, 120, 212, 80)) # Subtle blue glow
        glow.setOffset(0, 0)
        self.label.setGraphicsEffect(glow)

        layout.addWidget(self.label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

    def update_timer(self):
        real_time = getattr(self.engine, "real_time", 0)
        minutes = int(real_time // 60)
        seconds = int(real_time % 60)
        
        # 4. OPTIONAL: Change color to Red if screen time is too high
        if minutes >= 60:
            self.label.setStyleSheet("color: #FF4B4B;")
            
        self.label.setText(f"{minutes:02d}:{seconds:02d}")