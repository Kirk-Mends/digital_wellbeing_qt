# from PySide6.QtWidgets import QWidget
# from PySide6.QtGui import QPainter, QPen, QColor, QFont
# from PySide6.QtCore import Qt, QRectF, QTimer


# class AIRing(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setMinimumSize(160, 160)

#         self.fatigue = 0
#         self.ai_active = False
#         self.pulse = 0
#         self.behavior = "Idle"

#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_pulse)
#         self.timer.start(40)

#     def update_pulse(self):
#         if self.ai_active:
#             self.pulse = (self.pulse + 2) % 360
#         else:
#             self.pulse = 0
#         self.update()

#     def set_fatigue(self, value):
#         self.fatigue = max(0, min(100, value))
#         self.update()

#     def set_behavior(self, text):
#         self.behavior = text
#         self.update()

#     def set_ai_active(self, active):
#         self.ai_active = active
#         self.update()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)

#         rect = QRectF(10, 10, self.width() - 20, self.height() - 20)

#         # Outer AI activity ring
#         pen = QPen(QColor(0, 120, 215, 180), 8)
#         painter.setPen(pen)
#         painter.drawArc(rect, self.pulse * 16, 120 * 16)

#         # Inner fatigue ring
#         pen = QPen(self.fatigue_color(self.fatigue), 10)
#         painter.setPen(pen)
#         painter.drawArc(rect.adjusted(12, 12, -12, -12),
#                         0, int(360 * 16 * (self.fatigue / 100)))

#         # Center text
#         painter.setPen(Qt.black)
#         painter.setFont(QFont("Segoe UI", 14, QFont.Bold))
#         painter.drawText(self.rect(), Qt.AlignCenter, self.behavior)

#     def fatigue_color(self, value):
#         if value < 30:
#             return QColor("#4CAF50")
#         if value < 60:
#             return QColor("#FFC107")
#         if value < 85:
#             return QColor("#FF9800")
#         return QColor("#F44336")











# # Cleaned up version without underscores in UI labels:
# from PySide6.QtWidgets import QWidget
# from PySide6.QtGui import QPainter, QPen, QColor, QFont
# from PySide6.QtCore import Qt, QRectF, QTimer


# class AIRing(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setMinimumSize(160, 160)

#         self.fatigue = 0
#         self.ai_active = False
#         self.pulse = 0
#         self.behavior = "Idle"

#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_pulse)
#         self.timer.start(40)

#     # ---------------------------------------------------------
#     # UI CLEANING HELPERS
#     # ---------------------------------------------------------
#     @staticmethod
#     def clean_label(text: str) -> str:
#         """Convert internal identifiers into readable UI text."""
#         if not isinstance(text, str):
#             return str(text)

#         words = text.replace("_", " ").split()
#         return " ".join(w.capitalize() if not w.isupper() else w for w in words)

#     # ---------------------------------------------------------
#     # STATE UPDATES
#     # ---------------------------------------------------------
#     def update_pulse(self):
#         if self.ai_active:
#             self.pulse = (self.pulse + 2) % 360
#         else:
#             self.pulse = 0
#         self.update()

#     def set_fatigue(self, value):
#         self.fatigue = max(0, min(100, value))
#         self.update()

#     def set_behavior(self, text):
#         # Clean UI text before displaying
#         self.behavior = self.clean_label(text)
#         self.update()

#     def set_ai_active(self, active):
#         self.ai_active = active
#         self.update()

#     # ---------------------------------------------------------
#     # PAINT EVENT
#     # ---------------------------------------------------------
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)

#         rect = QRectF(10, 10, self.width() - 20, self.height() - 20)

#         # Outer AI activity ring
#         pen = QPen(QColor(0, 120, 215, 180), 8)
#         painter.setPen(pen)
#         painter.drawArc(rect, self.pulse * 16, 120 * 16)

#         # Inner fatigue ring
#         pen = QPen(self.fatigue_color(self.fatigue), 10)
#         painter.setPen(pen)
#         painter.drawArc(
#             rect.adjusted(12, 12, -12, -12),
#             0,
#             int(360 * 16 * (self.fatigue / 100))
#         )

#         # Center text
#         painter.setPen(Qt.black)
#         painter.setFont(QFont("Segoe UI", 14, QFont.Bold))
#         painter.drawText(self.rect(), Qt.AlignCenter, self.behavior)

#     # ---------------------------------------------------------
#     # FATIGUE COLOR LOGIC
#     # ---------------------------------------------------------
#     def fatigue_color(self, value):
#         if value < 30:
#             return QColor("#4CAF50")   # Green
#         if value < 60:
#             return QColor("#FFC107")   # Yellow
#         if value < 85:
#             return QColor("#FF9800")   # Orange
#         return QColor("#F44336")       # Red



















# 26th March for apple review

# import os
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QGraphicsDropShadowEffect
# from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient
# from PySide6.QtCore import Qt, QRectF, QTimer

# # ============================================================
# # PREMIUM AI RING WIDGET
# # ============================================================
# class AIRing(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setMinimumSize(220, 220)

#         # State Variables
#         self.fatigue = 0
#         self.ai_active = False
#         self.pulse = 0
#         self.behavior = "IDLE"

#         # Animation Timer (30 FPS for silky smoothness)
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_animation)
#         self.timer.start(33)

#     def update_animation(self):
#         if self.ai_active:
#             # Rotating at a variable speed feels more "AI" than a constant spin
#             self.pulse = (self.pulse + 3) % 360
#         else:
#             if self.pulse > 0:
#                 self.pulse = (self.pulse + 5) % 360 # Smoothly finish rotation
#         self.update()

#     # --- Setters ---
#     def set_fatigue(self, value):
#         self.fatigue = max(0, min(100, value))
#         self.update()

#     def set_behavior(self, text):
#         # Premium Touch: Convert snake_case to clean Uppercase
#         clean_text = str(text).replace("_", " ").upper()
#         self.behavior = clean_text
#         self.update()

#     def set_ai_active(self, active):
#         self.ai_active = active
#         self.update()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)

#         # Setup Geometry
#         width = self.width()
#         height = self.height()
#         side = min(width, height) - 40
#         rect = QRectF((width - side)/2, (height - side)/2, side, side)
#         center = rect.center()

#         # 1. THE AMBIENT GLOW (Only when AI is Active)
#         if self.ai_active:
#             glow_rad = side / 2 + 20
#             gradient = QRadialGradient(center, glow_rad)
#             gradient.setColorAt(0.5, QColor(0, 120, 215, 0))    # Transparent center
#             gradient.setColorAt(0.8, QColor(0, 120, 215, 30))   # Soft blue mid-glow
#             gradient.setColorAt(1.0, QColor(0, 120, 215, 0))    # Fade out
#             painter.setBrush(gradient)
#             painter.setPen(Qt.NoPen)
#             painter.drawEllipse(self.rect())

#         # 2. THE BACKGROUND TRACK (Faint "Ghost" Ring)
#         track_pen = QPen(QColor(128, 128, 128, 40), 10)
#         track_pen.setCapStyle(Qt.RoundCap)
#         painter.setPen(track_pen)
#         painter.drawEllipse(rect)

#         # 3. FATIGUE ARC (The Data Layer)
#         f_color = self.get_fatigue_color(self.fatigue)
#         f_pen = QPen(f_color, 12)
#         f_pen.setCapStyle(Qt.RoundCap)
#         painter.setPen(f_pen)
        
#         # Draw fatigue progress from the top (12 o'clock)
#         start_angle = 90 * 16 
#         span_angle = -int(360 * 16 * (self.fatigue / 100))
#         painter.drawArc(rect, start_angle, span_angle)

#         # 4. AI SPINNING RING (The Status Layer)
#         if self.ai_active:
#             ai_pen = QPen(QColor(0, 120, 215, 200), 5)
#             ai_pen.setCapStyle(Qt.RoundCap)
#             painter.setPen(ai_pen)
#             # A rotating arc that covers 1/4 of the circle
#             painter.drawArc(rect, -self.pulse * 16, 90 * 16)

#         # 5. TYPOGRAPHY (The Label Layer)
#         # Using a modern Slate Blue-Gray
#         painter.setPen(QColor("#1E293B"))
#         font = QFont("Segoe UI Variable Display", 11)
#         font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
#         font.setWeight(QFont.Bold)
#         painter.setFont(font)
        
#         # Center the text in the ring
#         painter.drawText(self.rect(), Qt.AlignCenter, self.behavior)

#     def get_fatigue_color(self, val):
#         """Premium Tailwind-inspired Palette"""
#         if val < 30: return QColor("#10B981") # Emerald Green
#         if val < 60: return QColor("#F59E0B") # Amber
#         if val < 85: return QColor("#F97316") # Orange
#         return QColor("#F43F5E")             # Rose Red

# # ============================================================
# # GLASS CONTAINER (The "Premium" Frame)
# # ============================================================
# class PremiumAIRingContainer(QFrame):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setFixedSize(260, 260)
        
#         # Glassmorphism Style
#         self.setStyleSheet("""
#             QFrame {
#                 background-color: rgba(255, 255, 255, 0.1);
#                 border: 1px solid rgba(255, 255, 255, 0.2);
#                 border-radius: 130px; /* Perfect Circle Wrapper */
#             }
#         """)

#         # Add a soft Drop Shadow to give it lift
#         shadow = QGraphicsDropShadowEffect(self)
#         shadow.setBlurRadius(25)
#         shadow.setXOffset(0)
#         shadow.setYOffset(10)
#         shadow.setColor(QColor(0, 0, 0, 40))
#         self.setGraphicsEffect(shadow)

#         # Layout to hold the ring
#         layout = QVBoxLayout(self)
#         layout.setAlignment(Qt.AlignCenter)
#         self.ring = AIRing()
#         layout.addWidget(self.ring)

#     # Proxy methods to control the ring directly
#     def set_fatigue(self, v): self.ring.set_fatigue(v)
#     def set_behavior(self, t): self.ring.set_behavior(t)
#     def set_ai_active(self, a): self.ring.set_ai_active(a)







# Mac and windows version

import os
import platform  # Added for cross-platform font detection
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QGraphicsDropShadowEffect
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient
from PySide6.QtCore import Qt, QRectF, QTimer

# --- CROSS-PLATFORM FONT LOGIC ---
if platform.system() == "Darwin":
    UI_FONT = ".AppleSystemUIFont"
else:
    UI_FONT = "Segoe UI Variable Display"

# ============================================================
# PREMIUM AI RING WIDGET
# ============================================================
class AIRing(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(220, 220)

        # State Variables
        self.fatigue = 0
        self.ai_active = False
        self.pulse = 0
        self.behavior = "IDLE"

        # Animation Timer (30 FPS for silky smoothness)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(33)

    def update_animation(self):
        if self.ai_active:
            # Rotating at a variable speed feels more "AI" than a constant spin
            self.pulse = (self.pulse + 3) % 360
        else:
            if self.pulse > 0:
                self.pulse = (self.pulse + 5) % 360 # Smoothly finish rotation
        self.update()

    # --- Setters ---
    def set_fatigue(self, value):
        self.fatigue = max(0, min(100, value))
        self.update()

    def set_behavior(self, text):
        # Premium Touch: Convert snake_case to clean Uppercase
        clean_text = str(text).replace("_", " ").upper()
        self.behavior = clean_text
        self.update()

    def set_ai_active(self, active):
        self.ai_active = active
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Setup Geometry
        width = self.width()
        height = self.height()
        side = min(width, height) - 40
        rect = QRectF((width - side)/2, (height - side)/2, side, side)
        center = rect.center()

        # 1. THE AMBIENT GLOW (Only when AI is Active)
        if self.ai_active:
            glow_rad = side / 2 + 20
            gradient = QRadialGradient(center, glow_rad)
            gradient.setColorAt(0.5, QColor(0, 120, 215, 0))    # Transparent center
            gradient.setColorAt(0.8, QColor(0, 120, 215, 30))   # Soft blue mid-glow
            gradient.setColorAt(1.0, QColor(0, 120, 215, 0))    # Fade out
            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(self.rect())

        # 2. THE BACKGROUND TRACK (Faint "Ghost" Ring)
        track_pen = QPen(QColor(128, 128, 128, 40), 10)
        track_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(track_pen)
        painter.drawEllipse(rect)

        # 3. FATIGUE ARC (The Data Layer)
        f_color = self.get_fatigue_color(self.fatigue)
        f_pen = QPen(f_color, 12)
        f_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(f_pen)
        
        # Draw fatigue progress from the top (12 o'clock)
        start_angle = 90 * 16 
        span_angle = -int(360 * 16 * (self.fatigue / 100))
        painter.drawArc(rect, start_angle, span_angle)

        # 4. AI SPINNING RING (The Status Layer)
        if self.ai_active:
            ai_pen = QPen(QColor(0, 120, 215, 200), 5)
            ai_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(ai_pen)
            # A rotating arc that covers 1/4 of the circle
            painter.drawArc(rect, -self.pulse * 16, 90 * 16)

        # 5. TYPOGRAPHY (The Label Layer)
        # Using a modern Slate Blue-Gray
        painter.setPen(QColor("#1E293B"))
        font = QFont(UI_FONT, 11) # Corrected to use UI_FONT variable
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
        font.setWeight(QFont.Bold)
        painter.setFont(font)
        
        # Center the text in the ring
        painter.drawText(self.rect(), Qt.AlignCenter, self.behavior)

    def get_fatigue_color(self, val):
        """Premium Tailwind-inspired Palette"""
        if val < 30: return QColor("#10B981") # Emerald Green
        if val < 60: return QColor("#F59E0B") # Amber
        if val < 85: return QColor("#F97316") # Orange
        return QColor("#F43F5E")             # Rose Red

# ============================================================
# GLASS CONTAINER (The "Premium" Frame)
# ============================================================
class PremiumAIRingContainer(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(260, 260)
        
        # Glassmorphism Style
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 130px; /* Perfect Circle Wrapper */
            }
        """)

        # Add a soft Drop Shadow to give it lift
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)

        # Layout to hold the ring
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        self.ring = AIRing()
        layout.addWidget(self.ring)

    # Proxy methods to control the ring directly
    def set_fatigue(self, v): self.ring.set_fatigue(v)
    def set_behavior(self, t): self.ring.set_behavior(t)
    def set_ai_active(self, a): self.ring.set_ai_active(a)