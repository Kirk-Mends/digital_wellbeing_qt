


















# # fixed the block of firing
# import os
# import sys
# import time
# import platform
# import subprocess
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QFrame, QProgressBar
# from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
# from PySide6.QtGui import QFont, QMouseEvent

# # --- WINDOWS NOTIFICATION SETUP ---
# WINOTIFY_AVAILABLE = False
# if platform.system() == "Windows":
#     try:
#         from winotify import Notification, audio
#         WINOTIFY_AVAILABLE = True
#     except Exception:
#         WINOTIFY_AVAILABLE = False


# # ============================================================
# # PREMIUM HUD (unchanged, safe)
# # ============================================================
# class PremiumHUD(QFrame):
#     def __init__(self, message, is_meeting=False, parent=None):
#         super().__init__(parent)
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.NoDropShadowWindowHint)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.setAttribute(Qt.WA_ShowWithoutActivating)
#         self.setWindowOpacity(0.0)
        
#         layout = QVBoxLayout(self)
#         self.container = QFrame()
#         self.container.setObjectName("HUDContainer")
#         bg_alpha = 230 if is_meeting else 210
#         self.container.setStyleSheet(
#             f"#HUDContainer {{ background-color: rgba(22, 22, 22, {bg_alpha}); "
#             f"border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; }}"
#         )
        
#         c_layout = QVBoxLayout(self.container)
#         self.label = QLabel(message)
#         font = QFont("SF Pro Display", 12) if platform.system() == "Darwin" else QFont("Segoe UI Variable Text", 10)
#         self.label.setFont(font)
#         self.label.setStyleSheet("color: #F8FAFC; border: none; background: transparent;")
#         self.label.setWordWrap(True)
#         self.label.setFixedWidth(260)
        
#         self.progress = QProgressBar()
#         self.progress.setFixedHeight(2)
#         self.progress.setTextVisible(False)
#         self.progress.setRange(0, 100)
#         self.progress.setValue(100)
        
#         c_layout.addWidget(self.label)
#         c_layout.addSpacing(10)
#         c_layout.addWidget(self.progress)
#         layout.addWidget(self.container)
        
#         self.adjustSize()
#         self._position_by_os()

#         self.anim = QPropertyAnimation(self, b"windowOpacity")
#         self.anim.setDuration(500)
#         self.anim.setEasingCurve(QEasingCurve.OutCubic)

#     def _position_by_os(self):
#         screen = QApplication.primaryScreen().availableGeometry()
#         p_x, p_y = (30, 65) if platform.system() == "Darwin" else (25, 25)
#         self.move(screen.left() + p_x, screen.top() + p_y)

#     def mousePressEvent(self, event: QMouseEvent):
#         self._hide_and_close()

#     def show_and_fade(self, duration=7000):
#         self.show()
#         self.anim.setStartValue(0.0)
#         self.anim.setEndValue(1.0)
#         self.anim.start()
        
#         self.total_duration = duration
#         self.remaining_ms = duration
#         self.prog_timer = QTimer(self)
#         self.prog_timer.timeout.connect(self._update_progress)
#         self.prog_timer.start(50)

#     def _update_progress(self):
#         self.remaining_ms -= 50
#         if self.remaining_ms <= 0:
#             self.prog_timer.stop()
#             self._hide_and_close()
#         else:
#             self.progress.setValue(int((self.remaining_ms / self.total_duration) * 100))

#     def _hide_and_close(self):
#         try:
#             if not self or (self.anim.state() == QPropertyAnimation.Running and self.windowOpacity() == 0):
#                 return
#             self.prog_timer.stop()
#             self.anim.stop()
#             self.anim.setStartValue(self.windowOpacity())
#             self.anim.setEndValue(0.0)
#             self.anim.finished.connect(self.deleteLater)
#             self.anim.start()
#         except RuntimeError:
#             pass


# # ============================================================
# # FIXED REMINDER CLASS (THIS IS THE IMPORTANT PART)
# # ============================================================
# class Reminder:
#     def __init__(self, main_window, min_interval_seconds=60):
#         """
#         min_interval_seconds:
#             - Prevents spam
#             - Ensures break_count increments correctly
#             - Ensures dashboard updates correctly
#         """
#         self.main_window = main_window
#         self.hud = None
#         self.break_count = 0
#         self._last_toast = 0
#         self.min_interval = min_interval_seconds

#     # --------------------------------------------------------
#     # RESET WHEN MONITORING STARTS (CRITICAL FIX)
#     # --------------------------------------------------------
#     def reset(self):
#         """Called when monitoring starts to ensure first break always fires."""
#         self._last_toast = 0

#     # --------------------------------------------------------
#     # MAIN BREAK MESSAGE LOGIC
#     # --------------------------------------------------------
#     def send_break_message(self, engine_output: dict):
#         now = time.time()

#         # SAFETY INTERVAL FIX
#         if self.min_interval > 0 and (now - self._last_toast) < self.min_interval:
#             return  # Block spam, but allow next real break

#         # UPDATE BREAK COUNT
#         self.break_count += 1
#         self._last_toast = now

#         # MESSAGE CONTENT
#         msg = engine_output.get("message", "Time for a quick reset.")
#         behavior = engine_output.get("behavior", "").lower()
#         is_meeting = any(k in behavior for k in ["meeting", "call", "zoom", "teams"])

#         # SAFELY CLOSE OLD HUD
#         if self.hud:
#             try:
#                 self.hud._hide_and_close()
#             except (RuntimeError, AttributeError):
#                 pass
#             self.hud = None

#         # CREATE NEW HUD
#         display_title = "Polite Update" if is_meeting else behavior.title()
#         self.hud = PremiumHUD(f"{display_title}: {msg}", is_meeting=is_meeting)
#         self.hud.show_and_fade(7000)

#         # SYSTEM NOTIFICATION
#         if not is_meeting:
#             self._trigger_system_notification("Break Reminder", msg)

#     # --------------------------------------------------------
#     # OS NOTIFICATION
#     # --------------------------------------------------------
#     def _trigger_system_notification(self, title, msg):
#         try:
#             current_os = platform.system()
#             if current_os == "Darwin":
#                 subprocess.run([
#                     "osascript", "-e",
#                     f'display notification "{msg}" with title "{title}" sound name "Glass"'
#                 ])
#             elif current_os == "Windows" and WINOTIFY_AVAILABLE:
#                 Notification(app_id="K-Mends AI", title=title, msg=msg, duration="short").show()
#         except:
#             pass













# fixed the block of firing
import os
import sys
import time
import platform
import subprocess
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QFrame, QProgressBar
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QMouseEvent

# --- WINDOWS NOTIFICATION SETUP ---
WINOTIFY_AVAILABLE = False
if platform.system() == "Windows":
    try:
        from winotify import Notification, audio
        WINOTIFY_AVAILABLE = True
    except Exception:
        WINOTIFY_AVAILABLE = False


# ============================================================
# PREMIUM HUD (unchanged, safe)
# ============================================================
class PremiumHUD(QFrame):
    def __init__(self, message, is_meeting=False, parent=None):
        super().__init__(parent)
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.NoDropShadowWindowHint)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setWindowOpacity(0.0)
        
        layout = QVBoxLayout(self)
        self.container = QFrame()
        self.container.setObjectName("HUDContainer")
        bg_alpha = 230 if is_meeting else 210
        self.container.setStyleSheet(
            f"#HUDContainer {{ background-color: rgba(22, 22, 22, {bg_alpha}); "
            f"border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; }}"
        )
        
        c_layout = QVBoxLayout(self.container)
        self.label = QLabel(message)
        font = QFont("SF Pro Display", 12) if platform.system() == "Darwin" else QFont("Segoe UI Variable Text", 10)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #F8FAFC; border: none; background: transparent;")
        self.label.setWordWrap(True)
        self.label.setFixedWidth(260)
        
        self.progress = QProgressBar()
        self.progress.setFixedHeight(2)
        self.progress.setTextVisible(False)
        self.progress.setRange(0, 100)
        self.progress.setValue(100)
        
        c_layout.addWidget(self.label)
        c_layout.addSpacing(10)
        c_layout.addWidget(self.progress)
        layout.addWidget(self.container)
        
        self.adjustSize()
        self._position_by_os()

        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(1500)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

    def _position_by_os(self):
        screen = QApplication.primaryScreen().availableGeometry()
        p_x, p_y = (30, 65) if platform.system() == "Darwin" else (25, 25)
        self.move(screen.left() + p_x, screen.top() + p_y)

    def mousePressEvent(self, event: QMouseEvent):
        self._hide_and_close()

    def show_and_fade(self, duration=12000):
        self.show()
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()
        
        self.total_duration = duration
        self.remaining_ms = duration
        self.prog_timer = QTimer(self)
        self.prog_timer.timeout.connect(self._update_progress)
        self.prog_timer.start(50)

    def _update_progress(self):
        self.remaining_ms -= 50
        if self.remaining_ms <= 0:
            self.prog_timer.stop()
            self._hide_and_close()
        else:
            self.progress.setValue(int((self.remaining_ms / self.total_duration) * 100))

    def _hide_and_close(self):
        try:
            if not self or (self.anim.state() == QPropertyAnimation.Running and self.windowOpacity() == 0):
                return
            self.prog_timer.stop()
            self.anim.stop()
            self.anim.setStartValue(self.windowOpacity())
            self.anim.setEndValue(0.0)
            self.anim.finished.connect(self.deleteLater)
            self.anim.start()
        except RuntimeError:
            pass


# ============================================================
# FIXED REMINDER CLASS (THIS IS THE IMPORTANT PART)
# ============================================================
class Reminder:
    def __init__(self, main_window, min_interval_seconds=60):
        """
        min_interval_seconds:
            - Prevents spam
            - Ensures break_count increments correctly
            - Ensures dashboard updates correctly
        """
        self.main_window = main_window
        self.hud = None
        self.break_count = 0
        self._last_toast = 0
        self.min_interval = min_interval_seconds

    # --------------------------------------------------------
    # RESET WHEN MONITORING STARTS (CRITICAL FIX)
    # --------------------------------------------------------
    def reset(self):
        """Called when monitoring starts to ensure first break always fires."""
        self._last_toast = 0

    # --------------------------------------------------------
    # MAIN BREAK MESSAGE LOGIC
    # --------------------------------------------------------
    def send_break_message(self, engine_output: dict):
        now = time.time()

        # SAFETY INTERVAL FIX
        if self.min_interval > 0 and (now - self._last_toast) < self.min_interval:
            return 

        # UPDATE BREAK COUNT
        self.break_count += 1
        self._last_toast = now

        # MESSAGE CONTENT
        msg = engine_output.get("message", "Time for a quick reset.")
        behavior = engine_output.get("behavior", "").lower()
        is_meeting = any(k in behavior for k in ["meeting", "call", "zoom", "teams"])

        # SAFELY CLOSE OLD HUD
        if self.hud:
            try:
                self.hud._hide_and_close()
            except:
                pass
            self.hud = None

        # --- THE FIX IS HERE ---
        display_title = "Polite Update" if is_meeting else behavior.title()
        self.hud = PremiumHUD(f"{display_title}: {msg}", is_meeting=is_meeting)
        
        # 1. Force the HUD to the very top layer of the screen
        self.hud.setAttribute(Qt.WA_ShowWithoutActivating)
        self.hud.show()
        self.hud.raise_() 
        #self.hud.activateWindow() 
        
        # 2. Now start the animation and progress bar
        self.hud.show_and_fade(20000)

        # SYSTEM NOTIFICATION (Banner + Sound)
        if not is_meeting:
            self._trigger_system_notification("Break Reminder", msg)
    # --------------------------------------------------------
    # OS NOTIFICATION
    # --------------------------------------------------------
    def _trigger_system_notification(self, title, msg):
        try:
            current_os = platform.system()
            if current_os == "Darwin":
                subprocess.run([
                    "osascript", "-e",
                    f'display notification "{msg}" with title "{title}" sound name "Glass"'
                ])
            elif current_os == "Windows" and WINOTIFY_AVAILABLE:
                Notification(app_id="K-Mends AI", title=title, msg=msg, duration="short").show()
        except:
            pass
