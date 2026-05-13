# from PySide6.QtWidgets import QWidget
# from PySide6.QtGui import QPainter, QPen, QColor, QFont
# from PySide6.QtCore import Qt, QRectF


# class FatigueGauge(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setMinimumSize(140, 140)
#         self.value = 0

#     def set_value(self, v):
#         self.value = max(0, min(100, v))
#         self.update()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)

#         rect = QRectF(10, 10, self.width() - 20, self.height() - 20)

#         # Background arc
#         pen = QPen(QColor("#DDDDDD"), 10)
#         painter.setPen(pen)
#         painter.drawArc(rect, 0, 360 * 16)

#         # Value arc
#         pen = QPen(self.color(), 10)
#         painter.setPen(pen)
#         painter.drawArc(rect, 90 * 16, -int(360 * 16 * (self.value / 100)))

#         # Text
#         painter.setPen(Qt.black)
#         painter.setFont(QFont("Segoe UI", 14, QFont.Bold))
#         painter.drawText(self.rect(), Qt.AlignCenter, f"{self.value}%")

#     def color(self):
#         if self.value < 30:
#             return QColor("#4CAF50")
#         if self.value < 60:
#             return QColor("#FFC107")
#         if self.value < 85:
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















# 26th March

# from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QGraphicsDropShadowEffect
# from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient
# from PySide6.QtCore import Qt, QRectF, QTimer

# class AIRing(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setMinimumSize(220, 220)

#         # State Variables
#         self.fatigue = 0
#         self.ai_active = False
#         self.pulse = 0
#         self.behavior = "IDLE"

#         # Smooth Animation Timer (30 FPS)
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_animation)
#         self.timer.start(33)

#     def update_animation(self):
#         if self.ai_active:
#             self.pulse = (self.pulse + 3) % 360
#         self.update()

#     def set_fatigue(self, value):
#         self.fatigue = max(0, min(100, value))
#         self.update()

#     def set_behavior(self, text):
#         # Convert underscores to spaces and make Uppercase
#         self.behavior = str(text).replace("_", " ").upper()
#         self.update()

#     def set_ai_active(self, active):
#         self.ai_active = active
#         self.update()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)

#         # Setup Geometry
#         width, height = self.width(), self.height()
#         side = min(width, height) - 60
#         rect = QRectF((width - side)/2, (height - side)/2, side, side)
#         center = rect.center()

#         # 1. THE AMBIENT GLOW (Only active when AI is active)
#         if self.ai_active:
#             glow_rad = side / 2 + 20
#             gradient = QRadialGradient(center, glow_rad)
#             gradient.setColorAt(0.6, QColor(0, 120, 215, 0))    
#             gradient.setColorAt(0.9, QColor(0, 120, 215, 40)) # Soft Electric Blue
#             gradient.setColorAt(1.0, QColor(0, 120, 215, 0))   
#             painter.setBrush(gradient)
#             painter.setPen(Qt.NoPen)
#             painter.drawEllipse(self.rect())

#         # 2. THE BACKGROUND TRACK (Faint guide)
#         track_pen = QPen(QColor(128, 128, 128, 30), 10)
#         track_pen.setCapStyle(Qt.RoundCap) # Premium rounded edges
#         painter.setPen(track_pen)
#         painter.drawEllipse(rect)

#         # 3. FATIGUE GAUGE (Main Data)
#         f_color = self.get_premium_color(self.fatigue)
#         f_pen = QPen(f_color, 14)
#         f_pen.setCapStyle(Qt.RoundCap) 
#         painter.setPen(f_pen)
#         painter.drawArc(rect, 90 * 16, -int(360 * 16 * (self.fatigue / 100)))

#         # 4. AI STATUS RING (Activity)
#         if self.ai_active:
#             ai_pen = QPen(QColor(0, 120, 215, 200), 5)
#             ai_pen.setCapStyle(Qt.RoundCap)
#             painter.setPen(ai_pen)
#             painter.drawArc(rect, -self.pulse * 16, 90 * 16)

#         # 5. TYPOGRAPHY
#         painter.setPen(QColor("#1E293B")) # Slate Dark Gray
#         font = QFont("Segoe UI Variable Display", 12)
#         font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
#         font.setWeight(QFont.Bold)
#         painter.setFont(font)
#         painter.drawText(self.rect(), Qt.AlignCenter, self.behavior)

#     def get_premium_color(self, val):
#         if val < 30: return QColor("#10B981") # Emerald Green
#         if val < 60: return QColor("#F59E0B") # Amber
#         if val < 85: return QColor("#F97316") # Deep Orange
#         return QColor("#F43F5E")             # Rose Red

# class PremiumAIRingContainer(QFrame):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setFixedSize(280, 280)
        
#         # Glassmorphism Style
#         self.setStyleSheet("""
#             QFrame {
#                 background-color: rgba(255, 255, 255, 0.1);
#                 border: 1px solid rgba(255, 255, 255, 0.2);
#                 border-radius: 140px;
#             }
#         """)

#         # Soft Shadow for lift
#         shadow = QGraphicsDropShadowEffect(self)
#         shadow.setBlurRadius(35)
#         shadow.setXOffset(0)
#         shadow.setYOffset(15)
#         shadow.setColor(QColor(0, 0, 0, 40))
#         self.setGraphicsEffect(shadow)

#         layout = QVBoxLayout(self)
#         self.ring = AIRing()
#         layout.addWidget(self.ring)

#     def set_fatigue(self, v): self.ring.set_fatigue(v)
#     def set_behavior(self, t): self.ring.set_behavior(t)
#     def set_ai_active(self, a): self.ring.set_ai_active(a)













# from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QGraphicsDropShadowEffect
# from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient
# from PySide6.QtCore import Qt, QRectF, QTimer
# import math

# # ============================================================
# # PREMIUM AI RING WIDGET (With Smooth Motion & Critical Pulse)
# # ============================================================
# class AIRing(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setMinimumSize(220, 220)

#         # State Variables
#         self.fatigue = 0          # The VISUAL position (moves smoothly)
#         self.target_fatigue = 0   # The ACTUAL data value
#         self.ai_active = False
#         self.pulse = 0
#         self.behavior = "IDLE"
        
#         # Red Pulse Animation variable
#         self.glow_alpha = 0
#         self.glow_dir = 1

#         # Smooth Animation Timer (30 FPS)
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_animation)
#         self.timer.start(33)

#     def update_animation(self):
#         # 1. SMOOTH CHASE LOGIC (Linear Interpolation)
#         # Move the bar 10% of the way to the target every 33ms
#         if abs(self.fatigue - self.target_fatigue) > 0.05:
#             diff = self.target_fatigue - self.fatigue
#             self.fatigue += diff * 0.1
#         else:
#             self.fatigue = self.target_fatigue

#         # 2. AI ROTATION
#         if self.ai_active:
#             self.pulse = (self.pulse + 3) % 360

#         # 3. CRITICAL PULSE (If Fatigue > 90)
#         if self.target_fatigue >= 90:
#             self.glow_alpha += 5 * self.glow_dir
#             if self.glow_alpha >= 100 or self.glow_alpha <= 0:
#                 self.glow_dir *= -1
#         else:
#             self.glow_alpha = 0

#         self.update()

#     # --- Public Setters ---
#     def set_fatigue(self, value):
#         """Now sets the target; the bar will slide to it smoothly."""
#         self.target_fatigue = max(0, min(100, value))

#     def set_behavior(self, text):
#         self.behavior = str(text).replace("_", " ").upper()
#         self.update()

#     def set_ai_active(self, active):
#         self.ai_active = active
#         self.update()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)

#         # Setup Geometry
#         width, height = self.width(), self.height()
#         side = min(width, height) - 60
#         rect = QRectF((width - side)/2, (height - side)/2, side, side)
#         center = rect.center()

#         # 1. CRITICAL ALERT GLOW (Layer 0)
#         if self.target_fatigue >= 90:
#             glow_grad = QRadialGradient(center, side / 2 + 30)
#             glow_grad.setColorAt(0.7, QColor(244, 63, 94, 0))
#             glow_grad.setColorAt(1.0, QColor(244, 63, 94, self.glow_alpha))
#             painter.setBrush(glow_grad)
#             painter.setPen(Qt.NoPen)
#             painter.drawEllipse(self.rect())

#         # 2. THE AMBIENT AI GLOW (Layer 1)
#         elif self.ai_active:
#             gradient = QRadialGradient(center, side / 2 + 20)
#             gradient.setColorAt(0.6, QColor(0, 120, 215, 0))    
#             gradient.setColorAt(0.9, QColor(0, 120, 215, 40))
#             gradient.setColorAt(1.0, QColor(0, 120, 215, 0))   
#             painter.setBrush(gradient)
#             painter.setPen(Qt.NoPen)
#             painter.drawEllipse(self.rect())

#         # 3. THE BACKGROUND TRACK
#         track_pen = QPen(QColor(128, 128, 128, 30), 10)
#         track_pen.setCapStyle(Qt.RoundCap)
#         painter.setPen(track_pen)
#         painter.drawEllipse(rect)

#         # 4. FATIGUE GAUGE (Smoothly moving)
#         f_color = self.get_premium_color(self.fatigue)
#         f_pen = QPen(f_color, 14)
#         f_pen.setCapStyle(Qt.RoundCap) 
#         painter.setPen(f_pen)
#         painter.drawArc(rect, 90 * 16, -int(360 * 16 * (self.fatigue / 100)))

#         # 5. AI STATUS RING
#         if self.ai_active:
#             ai_pen = QPen(QColor(0, 120, 215, 200), 5)
#             ai_pen.setCapStyle(Qt.RoundCap)
#             painter.setPen(ai_pen)
#             painter.drawArc(rect, -self.pulse * 16, 90 * 16)

#         # 6. TYPOGRAPHY
#         # Set text color to Red if critical, otherwise Dark Slate
#         txt_color = QColor("#F43F5E") if self.target_fatigue >= 90 else QColor("#1E293B")
#         painter.setPen(txt_color)
#         font = QFont("Segoe UI Variable Display", 11)
#         font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
#         font.setWeight(QFont.Bold)
#         painter.setFont(font)
#         painter.drawText(self.rect(), Qt.AlignCenter, self.behavior)

#     def get_premium_color(self, val):
#         if val < 30: return QColor("#10B981") # Emerald Green
#         if val < 60: return QColor("#F59E0B") # Amber
#         if val < 85: return QColor("#F97316") # Deep Orange
#         return QColor("#F43F5E")             # Rose Red

# # ============================================================
# # PREMIUM WRAPPER (Glassmorphism Frame)
# # ============================================================
# class PremiumAIRingContainer(QFrame):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setFixedSize(280, 280)
        
#         self.setStyleSheet("""
#             QFrame {
#                 background-color: rgba(255, 255, 255, 0.12);
#                 border: 1px solid rgba(255, 255, 255, 0.2);
#                 border-radius: 140px;
#             }
#         """)

#         shadow = QGraphicsDropShadowEffect(self)
#         shadow.setBlurRadius(35)
#         shadow.setXOffset(0)
#         shadow.setYOffset(15)
#         shadow.setColor(QColor(0, 0, 0, 40))
#         self.setGraphicsEffect(shadow)

#         layout = QVBoxLayout(self)
#         self.ring = AIRing()
#         layout.addWidget(self.ring)

#     def set_fatigue(self, v): self.ring.set_fatigue(v)
#     def set_behavior(self, t): self.ring.set_behavior(t)
#     def set_ai_active(self, a): self.ring.set_ai_active(a)






















# from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QGraphicsDropShadowEffect
# from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient
# from PySide6.QtCore import Qt, QRectF, QTimer
# import math

# class AIRing(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setMinimumSize(220, 220)

#         # State Variables
#         self.fatigue = 0          # Visual smooth value
#         self.target_fatigue = 0   # Actual data value
#         self.ai_active = False
#         self.pulse = 0
#         self.behavior = "IDLE"
        
#         # Pulse/Glow Variables
#         self.glow_alpha = 0
#         self.glow_dir = 1
#         self.text_scale = 1.0     # For the "Pulse Larger" effect
#         self.scale_dir = 1

#         # Smooth Animation Timer (30 FPS)
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_animation)
#         self.timer.start(33)

#     def update_animation(self):
#         # 1. SMOOTH CHASE LOGIC
#         if abs(self.fatigue - self.target_fatigue) > 0.05:
#             diff = self.target_fatigue - self.fatigue
#             self.fatigue += diff * 0.1
#         else:
#             self.fatigue = self.target_fatigue

#         # 2. AI ROTATION
#         if self.ai_active:
#             self.pulse = (self.pulse + 3) % 360

#         # 3. CRITICAL PULSE (If Fatigue >= 90)
#         if self.target_fatigue >= 90:
#             # Glow pulse
#             self.glow_alpha += 5 * self.glow_dir
#             if self.glow_alpha >= 100 or self.glow_alpha <= 0:
#                 self.glow_dir *= -1
            
#             # Text size pulse (Small "breathing" effect)
#             self.text_scale += 0.005 * self.scale_dir
#             if self.text_scale >= 1.1 or self.text_scale <= 1.0:
#                 self.scale_dir *= -1
#         else:
#             self.glow_alpha = 0
#             self.text_scale = 1.0

#         self.update()

#     def set_fatigue(self, value):
#         self.target_fatigue = max(0, min(100, value))

#     def set_behavior(self, text):
#         self.behavior = str(text).replace("_", " ").upper()
#         self.update()

#     def set_ai_active(self, active):
#         self.ai_active = active
#         self.update()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)

#         width, height = self.width(), self.height()
#         side = min(width, height) - 60
#         rect = QRectF((width - side)/2, (height - side)/2, side, side)
#         center = rect.center()

#         # 1. CRITICAL ALERT GLOW
#         if self.target_fatigue >= 90:
#             glow_grad = QRadialGradient(center, side / 2 + 30)
#             glow_grad.setColorAt(0.7, QColor(244, 63, 94, 0))
#             glow_grad.setColorAt(1.0, QColor(244, 63, 94, self.glow_alpha))
#             painter.setBrush(glow_grad)
#             painter.setPen(Qt.NoPen)
#             painter.drawEllipse(self.rect())

#         # 2. THE AMBIENT AI GLOW
#         elif self.ai_active:
#             gradient = QRadialGradient(center, side / 2 + 20)
#             gradient.setColorAt(0.6, QColor(0, 120, 215, 0))    
#             gradient.setColorAt(0.9, QColor(0, 120, 215, 40))
#             gradient.setColorAt(1.0, QColor(0, 120, 215, 0))   
#             painter.setBrush(gradient)
#             painter.setPen(Qt.NoPen)
#             painter.drawEllipse(self.rect())

#         # 3. THE BACKGROUND TRACK
#         track_pen = QPen(QColor(128, 128, 128, 30), 10)
#         track_pen.setCapStyle(Qt.RoundCap)
#         painter.setPen(track_pen)
#         painter.drawEllipse(rect)

#         # 4. FATIGUE GAUGE
#         f_color = self.get_premium_color(self.fatigue)
#         f_pen = QPen(f_color, 14)
#         f_pen.setCapStyle(Qt.RoundCap) 
#         painter.setPen(f_pen)
#         painter.drawArc(rect, 90 * 16, -int(360 * 16 * (self.fatigue / 100)))

#         # 5. AI STATUS RING
#         if self.ai_active:
#             ai_pen = QPen(QColor(0, 120, 215, 200), 5)
#             ai_pen.setCapStyle(Qt.RoundCap)
#             painter.setPen(ai_pen)
#             painter.drawArc(rect, -self.pulse * 16, 90 * 16)

#         # 6. TYPOGRAPHY (Behavior + Smooth Numeric Value)
#         is_critical = self.target_fatigue >= 90
#         txt_color = QColor("#F43F5E") if is_critical else QColor("#1E293B")
#         painter.setPen(txt_color)

#         # Draw Behavior (Top Label)
#         font_b = QFont("Segoe UI Variable Display", 10, QFont.Bold)
#         font_b.setLetterSpacing(QFont.AbsoluteSpacing, 1.2)
#         painter.setFont(font_b)
#         painter.drawText(rect.adjusted(0, -35, 0, -35), Qt.AlignCenter, self.behavior)

#         # Draw Numeric Fatigue (Large Center Value)
#         # Apply the text_scale pulse here
#         base_font_size = 28 if is_critical else 24
#         font_v = QFont("Segoe UI Variable Display", int(base_font_size * self.text_scale), QFont.DemiBold)
#         painter.setFont(font_v)
        
#         # Use :.1f for 1 decimal place precision
#         fatigue_str = f"{self.fatigue:.1f}%"
#         painter.drawText(rect.adjusted(0, 10, 0, 10), Qt.AlignCenter, fatigue_str)

#     def get_premium_color(self, val):
#         if val < 30: return QColor("#10B981") # Emerald
#         if val < 60: return QColor("#F59E0B") # Amber
#         if val < 85: return QColor("#F97316") # Orange
#         return QColor("#F43F5E")             # Rose Red

# class PremiumAIRingContainer(QFrame):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setFixedSize(280, 280)
        
#         self.setStyleSheet("""
#             QFrame {
#                 background-color: rgba(255, 255, 255, 0.12);
#                 border: 1px solid rgba(255, 255, 255, 0.2);
#                 border-radius: 140px;
#             }
#         """)

#         shadow = QGraphicsDropShadowEffect(self)
#         shadow.setBlurRadius(35)
#         shadow.setXOffset(0)
#         shadow.setYOffset(15)
#         shadow.setColor(QColor(0, 0, 0, 40))
#         self.setGraphicsEffect(shadow)

#         layout = QVBoxLayout(self)
#         self.ring = AIRing()
#         layout.addWidget(self.ring)

#     def set_fatigue(self, v): self.ring.set_fatigue(v)
#     def set_behavior(self, t): self.ring.set_behavior(t)
#     def set_ai_active(self, a): self.ring.set_ai_active(a)









# mac and windows font cleanup

from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QGraphicsDropShadowEffect
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient
from PySide6.QtCore import Qt, QRectF, QTimer
import math
import platform  # Added for OS detection

# --- CROSS-PLATFORM FONT LOGIC ---
if platform.system() == "Darwin":
    UI_FONT = ".AppleSystemUIFont"
else:
    UI_FONT = "Segoe UI Variable Display"

class AIRing(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(220, 220)

        # State Variables
        self.fatigue = 0          # Visual smooth value
        self.target_fatigue = 0   # Actual data value
        self.ai_active = False
        self.pulse = 0
        self.behavior = "IDLE"
        
        # Pulse/Glow Variables
        self.glow_alpha = 0
        self.glow_dir = 1
        self.text_scale = 1.0     # For the "Pulse Larger" effect
        self.scale_dir = 1

        # Smooth Animation Timer (30 FPS)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(33)

    def update_animation(self):
        # 1. SMOOTH CHASE LOGIC
        if abs(self.fatigue - self.target_fatigue) > 0.05:
            diff = self.target_fatigue - self.fatigue
            self.fatigue += diff * 0.1
        else:
            self.fatigue = self.target_fatigue

        # 2. AI ROTATION
        if self.ai_active:
            self.pulse = (self.pulse + 3) % 360

        # 3. CRITICAL PULSE (If Fatigue >= 90)
        if self.target_fatigue >= 90:
            # Glow pulse
            self.glow_alpha += 5 * self.glow_dir
            if self.glow_alpha >= 100 or self.glow_alpha <= 0:
                self.glow_dir *= -1
            
            # Text size pulse (Small "breathing" effect)
            self.text_scale += 0.005 * self.scale_dir
            if self.text_scale >= 1.1 or self.text_scale <= 1.0:
                self.scale_dir *= -1
        else:
            self.glow_alpha = 0
            self.text_scale = 1.0

        self.update()

    def set_fatigue(self, value):
        self.target_fatigue = max(0, min(100, value))

    def set_behavior(self, text):
        self.behavior = str(text).replace("_", " ").upper()
        self.update()

    def set_ai_active(self, active):
        self.ai_active = active
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width, height = self.width(), self.height()
        side = min(width, height) - 60
        rect = QRectF((width - side)/2, (height - side)/2, side, side)
        center = rect.center()

        # 1. CRITICAL ALERT GLOW
        if self.target_fatigue >= 90:
            glow_grad = QRadialGradient(center, side / 2 + 30)
            glow_grad.setColorAt(0.7, QColor(244, 63, 94, 0))
            glow_grad.setColorAt(1.0, QColor(244, 63, 94, self.glow_alpha))
            painter.setBrush(glow_grad)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(self.rect())

        # 2. THE AMBIENT AI GLOW
        elif self.ai_active:
            gradient = QRadialGradient(center, side / 2 + 20)
            gradient.setColorAt(0.6, QColor(0, 120, 215, 0))    
            gradient.setColorAt(0.9, QColor(0, 120, 215, 40))
            gradient.setColorAt(1.0, QColor(0, 120, 215, 0))   
            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(self.rect())

        # 3. THE BACKGROUND TRACK
        track_pen = QPen(QColor(128, 128, 128, 30), 10)
        track_pen.setCapStyle(Qt.RoundCap)
        painter.setPen(track_pen)
        painter.drawEllipse(rect)

        # 4. FATIGUE GAUGE
        f_color = self.get_premium_color(self.fatigue)
        f_pen = QPen(f_color, 14)
        f_pen.setCapStyle(Qt.RoundCap) 
        painter.setPen(f_pen)
        painter.drawArc(rect, 90 * 16, -int(360 * 16 * (self.fatigue / 100)))

        # 5. AI STATUS RING
        if self.ai_active:
            ai_pen = QPen(QColor(0, 120, 215, 200), 5)
            ai_pen.setCapStyle(Qt.RoundCap)
            painter.setPen(ai_pen)
            painter.drawArc(rect, -self.pulse * 16, 90 * 16)

        # 6. TYPOGRAPHY (Behavior + Smooth Numeric Value)
        is_critical = self.target_fatigue >= 90
        txt_color = QColor("#F43F5E") if is_critical else QColor("#1E293B")
        painter.setPen(txt_color)

        # Draw Behavior (Top Label)
        # Corrected: Use UI_FONT variable
        font_b = QFont(UI_FONT, 10, QFont.Bold)
        font_b.setLetterSpacing(QFont.AbsoluteSpacing, 1.2)
        painter.setFont(font_b)
        painter.drawText(rect.adjusted(0, -35, 0, -35), Qt.AlignCenter, self.behavior)

        # Draw Numeric Fatigue (Large Center Value)
        # Apply the text_scale pulse here
        base_font_size = 28 if is_critical else 24
        # Corrected: Use UI_FONT variable
        font_v = QFont(UI_FONT, int(base_font_size * self.text_scale), QFont.DemiBold)
        painter.setFont(font_v)
        
        # Use :.1f for 1 decimal place precision
        fatigue_str = f"{self.fatigue:.1f}%"
        painter.drawText(rect.adjusted(0, 10, 0, 10), Qt.AlignCenter, fatigue_str)

    def get_premium_color(self, val):
        if val < 30: return QColor("#10B981") # Emerald
        if val < 60: return QColor("#F59E0B") # Amber
        if val < 85: return QColor("#F97316") # Orange
        return QColor("#F43F5E")             # Rose Red

class PremiumAIRingContainer(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(280, 280)
        
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 140px;
            }
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(35)
        shadow.setXOffset(0)
        shadow.setYOffset(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        self.ring = AIRing()
        layout.addWidget(self.ring)

    def set_fatigue(self, v): self.ring.set_fatigue(v)
    def set_behavior(self, t): self.ring.set_behavior(t)
    def set_ai_active(self, a): self.ring.set_ai_active(a)