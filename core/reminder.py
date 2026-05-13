

# 5
# upgraded Completely

# reminder.py — Premium, behavior-aware, warm-tone break reminders

# import os
# import sys
# import time
# import traceback
# import tkinter as tk
# from tkinter import messagebox

# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout

# from ui.widgets.toast import Toast  # fallback toast

# # Try to import winotify
# try:
#     from winotify import Notification, audio
#     WINOTIFY_AVAILABLE = True
# except Exception:
#     WINOTIFY_AVAILABLE = False

# from core.settings import SettingsManager
# settings = SettingsManager()


# def resource_path(relative_path):
#     """Get absolute path for PyInstaller or local."""
#     if hasattr(sys, "_MEIPASS"):
#         return os.path.join(sys._MEIPASS, relative_path)
#     return os.path.join(os.path.abspath("."), relative_path)


# class AnimatedToast(QWidget):
#     """Custom animated toast for in-app notifications using GIFs."""
#     def __init__(self, message, gif_path=None, parent=None, duration=5000):
#         super().__init__(parent)
#         self.setWindowFlags(self.windowFlags() |
#                             Qt.FramelessWindowHint |
#                             Qt.WindowStaysOnTopHint |
#                             Qt.Tool)
#         self.setAttribute(Qt.WA_TranslucentBackground)

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(10, 10, 10, 10)

#         # Message label
#         self.label = QLabel(message)
#         self.label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
#         self.label.setWordWrap(True)
#         layout.addWidget(self.label)

#         # Animated GIF
#         self.movie = None
#         if gif_path and os.path.exists(gif_path):
#             from PySide6.QtGui import QMovie
#             self.movie = QMovie(gif_path)
#             self.gif_label = QLabel()
#             self.gif_label.setMovie(self.movie)
#             layout.addWidget(self.gif_label)
#             self.movie.start()

#         # Auto-close timer
#         QTimer.singleShot(duration, self.close)
#         self.show()


# class Reminder:
#     """Premium break reminder handler for Smart Mode & AI Mode."""
#     def __init__(self, main_window, min_interval_seconds=5):
#         self.main_window = main_window
#         self.min_interval = float(min_interval_seconds)
#         self._last_toast = 0.0
#         self.break_count = 0

#     # ---------------------------------------------------------
#     # WINOTIFY NOTIFICATION (clean, no snooze)
#     # ---------------------------------------------------------
#     def _show_winotify(self, title, msg, icon_path=None):
#         if not WINOTIFY_AVAILABLE:
#             return

#         toast = Notification(
#             app_id="Digital Wellbeing Assistant",
#             title=title,
#             msg=msg,
#             duration="long",
#             icon=icon_path
#         )

#         # Sound
#         if settings.get("sound_on"):
#             try:
#                 toast.set_audio(audio.Reminder, loop=False)
#             except Exception:
#                 pass
#         else:
#             try:
#                 toast.set_audio(None)
#             except Exception:
#                 pass

#         # Clean actions (no snooze, no analytics)
#         try:
#             # toast.add_actions(label="Skip this break", launch="python skip_break.py")
#             # toast.add_actions(label="Open Insights", launch="python app.py --insights")
#             toast.add_actions(label="Take Break", launch="app://take_break")
#             toast.add_actions(label="I'm Busy", launch="app://busy")
#         except Exception:
#             pass

#         toast.show()

#     # ---------------------------------------------------------
#     # SEND BREAK MESSAGE (behavior-aware, warm tone)
#     # ---------------------------------------------------------
#     def send_break_message(self, engine_output: dict, gif_path=None):
#         """
#         engine_output must contain:
#         - behavior (clean label)
#         - reason (clean label)
#         - message (warm tone)
#         - interval_used
#         - last_break_time (from engine)
#         """
#         now = time.time()
#         if now - self._last_toast < self.min_interval:
#             return

#         self.break_count += 1

#         # Extract engine output
#         behavior = engine_output.get("behavior", "Activity")
#         reason = engine_output.get("reason", "")
#         message = engine_output.get("message", "Take a moment to pause.")
#         interval_used = engine_output.get("interval_used", 20 * 60)
#         last_break_time = engine_output.get("last_break_time", now)

#         # Time until next break
#         elapsed = now - last_break_time
#         remaining = max(0, int((interval_used - elapsed) / 60))
#         next_break_text = f"Next break in {remaining} minutes." if remaining > 0 else ""

#         # Premium headline
#         headline = f"{behavior} — {reason}" if reason else behavior

#         # Final popup text
#         popup_text = f"{headline}\n{message}\n{next_break_text}".strip()

#         # ---------------------------------------------------------
#         # In-App animated toast
#         # ---------------------------------------------------------
#         try:
#             AnimatedToast(
#                 message=popup_text,
#                 gif_path=gif_path,
#                 parent=self.main_window,
#                 duration=6000
#             )
#         except Exception:
#             # fallback
#             toast = Toast(popup_text, parent=self.main_window)
#             toast.show_toast()

#         # ---------------------------------------------------------
#         # System notification (winotify)
#         # ---------------------------------------------------------
#         try:
#             if WINOTIFY_AVAILABLE:
#                 icon_path = resource_path("assets/icons/icon.png")
#                 self._show_winotify("Break Reminder", popup_text, icon_path)
#         except Exception:
#             # Fallback: Tkinter messagebox
#             try:
#                 root = tk._default_root
#                 if root:
#                     messagebox.showinfo("Break Reminder", popup_text, parent=root)
#                 else:
#                     tmp = tk.Tk()
#                     tmp.withdraw()
#                     messagebox.showinfo("Break Reminder", popup_text, parent=tmp)
#                     tmp.destroy()
#             except Exception:
#                 print("Reminder fallback:", popup_text)
#                 traceback.print_exc()

#         finally:
#             self._last_toast = time.time()






# 20th March 
# Worked on Modal (Additional Window) for Take Break 

# # reminder.py — Premium, behavior-aware, warm-tone break reminders

# import os
# import sys
# import time
# import traceback
# import tkinter as tk
# from tkinter import messagebox

# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout

# from ui.widgets.toast import Toast  # fallback toast

# # Try to import winotify
# try:
#     from winotify import Notification, audio
#     WINOTIFY_AVAILABLE = True
# except Exception:
#     WINOTIFY_AVAILABLE = False

# from core.settings import SettingsManager
# settings = SettingsManager()


# def resource_path(relative_path):
#     """Get absolute path for PyInstaller or local."""
#     if hasattr(sys, "_MEIPASS"):
#         return os.path.join(sys._MEIPASS, relative_path)
#     return os.path.join(os.path.abspath("."), relative_path)


# class AnimatedToast(QWidget):
#     """Custom animated toast for in-app notifications using GIFs."""
#     def __init__(self, message, gif_path=None, parent=None, duration=5000):
#         super().__init__(parent)
#         self.setWindowFlags(self.windowFlags() |
#                             Qt.FramelessWindowHint |
#                             Qt.WindowStaysOnTopHint |
#                             Qt.Tool)
#         self.setAttribute(Qt.WA_TranslucentBackground)

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(10, 10, 10, 10)

#         # Message label
#         self.label = QLabel(message)
#         self.label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
#         self.label.setWordWrap(True)
#         layout.addWidget(self.label)

#         # Animated GIF
#         self.movie = None
#         if gif_path and os.path.exists(gif_path):
#             from PySide6.QtGui import QMovie
#             self.movie = QMovie(gif_path)
#             self.gif_label = QLabel()
#             self.gif_label.setMovie(self.movie)
#             layout.addWidget(self.gif_label)
#             self.movie.start()

#         # Auto-close timer
#         QTimer.singleShot(duration, self.close)
#         self.show()


# class Reminder:
#     """Premium break reminder handler for Smart Mode & AI Mode."""
#     def __init__(self, main_window, min_interval_seconds=5):
#         self.main_window = main_window
#         self.min_interval = float(min_interval_seconds)
#         self._last_toast = 0.0
#         self.break_count = 0

#     # ---------------------------------------------------------
#     # WINOTIFY NOTIFICATION (clean, no snooze)
#     # ---------------------------------------------------------
#     def _show_winotify(self, title, msg, icon_path=None):
#         if not WINOTIFY_AVAILABLE:
#             return

#         toast = Notification(
#             app_id="Digital Wellbeing Assistant",
#             title=title,
#             msg=msg,
#             duration="long",
#             icon=icon_path
#         )

#         # Sound
#         if settings.get("sound_on"):
#             try:
#                 toast.set_audio(audio.Reminder, loop=False)
#             except Exception:
#                 pass
#         else:
#             try:
#                 toast.set_audio(None)
#             except Exception:
#                 pass

#         # Clean actions
#         try:
#             toast.add_actions(label="Take Break", launch="app://take_break")
#             toast.add_actions(label="I'm Busy", launch="app://busy")
#         except Exception:
#             pass

#         toast.show()
#     # ---------------------------------------------------------
#     # SEND BREAK MESSAGE (behavior-aware, warm tone)
#     # ---------------------------------------------------------
#     def send_break_message(self, engine_output: dict, gif_path=None):
#         """
#         engine_output must contain:
#         - behavior
#         - reason
#         - message
#         - interval_used
#         - last_break_time
#         """
#         now = time.time()
#         if now - self._last_toast < self.min_interval:
#             return

#         self.break_count += 1

#         # Extract engine output
#         behavior = engine_output.get("behavior", "Activity")
#         reason = engine_output.get("reason", "")
#         message = engine_output.get("message", "Take a moment to pause.")
#         interval_used = engine_output.get("interval_used", 20 * 60)
#         last_break_time = engine_output.get("last_break_time", now)

#         # Time until next break
#         elapsed = now - last_break_time
#         remaining = max(0, int((interval_used - elapsed) / 60))
#         next_break_text = f"Next break in {remaining} minutes." if remaining > 0 else ""

#         # Premium headline
#         headline = f"{behavior} — {reason}" if reason else behavior

#         # Final popup text
#         popup_text = f"{headline}\n{message}\n{next_break_text}".strip()

#         # ---------------------------------------------------------
#         # In-App animated toast
#         # ---------------------------------------------------------
#         try:
#             AnimatedToast(
#                 message=popup_text,
#                 gif_path=gif_path,
#                 parent=self.main_window,
#                 duration=6000
#             )
#         except Exception:
#             toast = Toast(popup_text, parent=self.main_window)
#             toast.show_toast()

#         # ---------------------------------------------------------
#         # System notification (winotify)
#         # ---------------------------------------------------------
#         try:
#             if WINOTIFY_AVAILABLE:
#                 icon_path = resource_path("assets/icons/icon.png")
#                 self._show_winotify("Break Reminder", popup_text, icon_path)
#         except Exception:
#             # Fallback: Tkinter messagebox
#             try:
#                 root = tk._default_root
#                 if root:
#                     messagebox.showinfo("Break Reminder", popup_text, parent=root)
#                 else:
#                     tmp = tk.Tk()
#                     tmp.withdraw()
#                     messagebox.showinfo("Break Reminder", popup_text, parent=tmp)
#                     tmp.destroy()
#             except Exception:
#                 print("Reminder fallback:", popup_text)
#                 traceback.print_exc()

#         finally:
#             self._last_toast = time.time()

#         # ---------------------------------------------------------
#         # OPEN BREAK MODAL (Smart Mode + AI Mode)
#         # ---------------------------------------------------------
#         try:
#             #self.main_window.show_break_modal(engine_output)
#             pass
#         except Exception:
#             traceback.print_exc()




















# 25th March

# import os
# import sys
# import time
# import platform
# import subprocess
# import traceback
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QMessageBox
# from PySide6.QtGui import QMovie

# from core.settings import SettingsManager
# settings = SettingsManager()

# # Try to import winotify only on Windows
# WINOTIFY_AVAILABLE = False
# if platform.system() == "Windows":
#     try:
#         from winotify import Notification, audio
#         WINOTIFY_AVAILABLE = True
#     except ImportError:
#         pass

# def resource_path(relative_path):
#     if hasattr(sys, "_MEIPASS"):
#         return os.path.join(sys._MEIPASS, relative_path)
#     return os.path.join(os.path.abspath("."), relative_path)

# class AnimatedToast(QWidget):
#     """Custom animated toast for in-app notifications."""
#     def __init__(self, message, gif_path=None, parent=None, duration=6000):
#         super().__init__(parent)
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
#         self.setAttribute(Qt.WA_TranslucentBackground)

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(15, 15, 15, 15)

#         # Content styling
#         self.label = QLabel(message)
#         self.label.setStyleSheet("color: white; font-family: 'Segoe UI', 'SF Pro'; font-size: 14px; font-weight: 600;")
#         self.label.setWordWrap(True)
#         layout.addWidget(self.label)

#         if gif_path and os.path.exists(gif_path):
#             self.movie = QMovie(gif_path)
#             self.gif_label = QLabel()
#             self.gif_label.setMovie(self.movie)
#             layout.addWidget(self.gif_label)
#             self.movie.start()

#         QTimer.singleShot(duration, self.close)
#         self.show()

# class Reminder:
#     """Premium, cross-platform behavior-aware break reminders."""
#     def __init__(self, main_window, min_interval_seconds=5):
#         self.main_window = main_window
#         self.min_interval = float(min_interval_seconds)
#         self._last_toast = 0.0
#         self.break_count = 0

#     def _show_native_notification(self, title, msg):
#         """Dispatches to the correct system notification engine."""
#         system = platform.system()

#         if system == "Darwin":  # macOS Premium Native
#             try:
#                 # Triggers the macOS Slide-in notification
#                 script = f'display notification "{msg}" with title "{title}" sound name "Glass"'
#                 subprocess.run(["osascript", "-e", script], check=True)
#             except Exception as e:
#                 print(f"macOS Notification Error: {e}")

#         elif system == "Windows" and WINOTIFY_AVAILABLE:
#             self._show_winotify(title, msg)
            
#         else:
#             # Fallback to a styled PySide6 Message Box (No Tkinter!)
#             self._show_fallback_box(title, msg)

#     def _show_winotify(self, title, msg):
#         icon_path = resource_path("assets/icons/icon.png")
#         toast = Notification(
#             app_id="Digital Wellbeing",
#             title=title,
#             msg=msg,
#             duration="long",
#             icon=icon_path
#         )
#         if settings.get("sound_on"):
#             toast.set_audio(audio.Reminder, loop=False)
        
#         toast.add_actions(label="Take Break", launch="app://take_break")
#         toast.show()

#     def _show_fallback_box(self, title, msg):
#         """A clean, styled fallback using PySide6."""
#         msg_box = QMessageBox(self.main_window)
#         msg_box.setWindowTitle(title)
#         msg_box.setText(msg)
#         msg_box.setIcon(QMessageBox.Information)
#         msg_box.show()

#     def send_break_message(self, engine_output: dict, gif_path=None):
#         now = time.time()
#         if now - self._last_toast < self.min_interval:
#             return

#         self.break_count += 1

#         # Data extraction
#         behavior = engine_output.get("behavior", "Activity")
#         reason = engine_output.get("reason", "")
#         message = engine_output.get("message", "Time for a quick pause.")
        
#         # Formatting
#         headline = f"{behavior} — {reason}" if reason else behavior
#         popup_text = f"{headline}\n{message}".strip()

#         # 1. Show In-App Animated Toast
#         try:
#             AnimatedToast(popup_text, gif_path, self.main_window)
#         except Exception:
#             traceback.print_exc()

#         # 2. Show System-Level Notification
#         self._show_native_notification("Break Reminder", popup_text)
        
#         self._last_toast = now









# # I removed the video 
# import os
# import sys
# import time
# import platform
# import subprocess
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QFrame
# from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
# from PySide6.QtGui import QFont

# # --- WINDOWS SPECIFIC ---
# WINOTIFY_AVAILABLE = False
# if platform.system() == "Windows":
#     try:
#         from winotify import Notification, audio
#         WINOTIFY_AVAILABLE = True
#     except ImportError:
#         pass

# # --- PREMIUM HUD (Top-Left Minimalist Message) ---
# class PremiumHUD(QFrame):
#     """
#     The 'Faint Message' replacement. 
#     A high-end, top-left glass overlay for subtle AI updates.
#     """
#     def __init__(self, message, parent=None):
#         super().__init__(parent)
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus | Qt.Tool)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.setWindowOpacity(0.0)
        
#         # UI Setup
#         layout = QVBoxLayout(self)
#         self.container = QFrame()
#         # macOS-inspired 'Vibrant' style
#         self.container.setStyleSheet("""
#             background-color: rgba(25, 25, 25, 210);
#             border: 1px solid rgba(255, 255, 255, 0.1);
#             border-radius: 10px;
#         """)
#         c_layout = QVBoxLayout(self.container)
        
#         self.label = QLabel(message)
#         # Use SF Pro for Mac, Segoe UI for Windows
#         font_name = "SF Pro Display" if platform.system() == "Darwin" else "Segoe UI"
#         self.label.setFont(QFont(font_name, 11, QFont.Medium))
#         self.label.setStyleSheet("color: #E4E7F2; border: none;")
#         self.label.setWordWrap(True)
        
#         c_layout.addWidget(self.label)
#         layout.addWidget(self.container)
        
#         self.adjustSize()
#         self._position_top_left()

#         # Animation
#         self.anim = QPropertyAnimation(self, b"windowOpacity")
#         self.anim.setDuration(600)
#         self.anim.setEasingCurve(QEasingCurve.OutCubic)

#     def _position_top_left(self):
#         screen = QApplication.primaryScreen().availableGeometry()
        
#         # macOS Menu Bar is typically 24-32px. 
#         # We place the HUD 60px down and 30px in for a 'floating' look.
#         # This keeps it clear of the 'File' and 'Edit' menus.
#         padding_x = 30
#         padding_y = 65 
        
#         self.move(screen.left() + padding_x, screen.top() + padding_y)

#     def show_and_fade(self, duration=6000):
#         self.show()
#         # Start the animation
#         self.anim.setStartValue(0.0)
#         self.anim.setEndValue(1.0)
#         self.anim.start()
        
#         # The 'Kill Timer'
#         # After 'duration' ms, trigger the fade out
#         QTimer.singleShot(duration, self._hide_and_close)

#     def _hide_and_close(self):
#         # Reverse the animation
#         self.anim.setStartValue(self.windowOpacity())
#         self.anim.setEndValue(0.0)
#         # CRITICAL: Only close the widget AFTER the fade is finished
#         self.anim.finished.connect(self.deleteLater) 
#         self.anim.start()

# # --- MAIN REMINDER CLASS ---
# class Reminder:
#     def __init__(self, main_window):
#         self.main_window = main_window
#         self.last_notify_time = 0

#     def send_break_message(self, engine_output: dict):
#         """Entry point for all platforms."""
#         msg = engine_output.get("message", "Time for a quick reset.")
#         behavior = engine_output.get("behavior", "Deep Work")
        
#         # 1. Show the 'Faint' HUD for behavior updates (Top Left)
#         self.hud = PremiumHUD(f"{behavior}: {msg}")
#         self.hud.show_and_fade(6000)

#         # 2. Trigger System Notification (Slide-in)
#         self._trigger_system_notification("Break Reminder", msg)

#     def _trigger_system_notification(self, title, msg):
#         current_os = platform.system()

#         if current_os == "Darwin": # macOS
#             # APPLE REVIEW SAFE: Uses standard AppleScript notification
#             script = f'display notification "{msg}" with title "{title}" sound name "Glass"'
#             subprocess.run(["osascript", "-e", script])

#         elif current_os == "Windows" and WINOTIFY_AVAILABLE:
#             toast = Notification(app_id="K-Mends AI", title=title, msg=msg, duration="short")
#             toast.show()

#         elif current_os == "Linux":
#             # Standard Linux Desktop Notification
#             try:
#                 subprocess.run(["notify-send", title, msg])
#             except:
#                 pass
    
    







# import os
# import sys
# import time
# import platform
# import subprocess  # Fixed: Added missing import
# import traceback
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QFrame
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

# # --- PREMIUM HUD (The Faint Top-Left Message) ---
# class PremiumHUD(QFrame):
#     def __init__(self, message, parent=None):
#         super().__init__(parent)
        
#         # Flags: Tool ensures it doesn't show in the Dock/Taskbar
#         self.setWindowFlags(
#             Qt.FramelessWindowHint | 
#             Qt.WindowStaysOnTopHint | 
#             Qt.Tool |
#             Qt.NoDropShadowWindowHint
#         )
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.setWindowOpacity(0.0)
        
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(10, 10, 10, 10)
        
#         self.container = QFrame()
#         self.container.setObjectName("HUDContainer")
#         self.container.setStyleSheet("""
#             #HUDContainer {
#                 background-color: rgba(20, 20, 20, 210);
#                 border: 1px solid rgba(255, 255, 255, 0.12);
#                 border-radius: 12px;
#             }
#         """)
        
#         c_layout = QVBoxLayout(self.container)
#         c_layout.setContentsMargins(18, 12, 18, 12)
        
#         self.label = QLabel(message)
#         sys_font = "SF Pro Display" if platform.system() == "Darwin" else "Segoe UI"
#         self.label.setFont(QFont(sys_font, 11, QFont.Medium))
#         self.label.setStyleSheet("color: #E4E7F2; border: none; background: transparent;")
#         self.label.setWordWrap(True)
#         self.label.setFixedWidth(240)
        
#         c_layout.addWidget(self.label)
#         layout.addWidget(self.container)
        
#         self.adjustSize()
#         self._position_by_os()

#         self.anim = QPropertyAnimation(self, b"windowOpacity")
#         self.anim.setDuration(500)
#         self.anim.setEasingCurve(QEasingCurve.OutCubic)

#     def _position_by_os(self):
#         screen = QApplication.primaryScreen().availableGeometry()
#         if platform.system() == "Darwin":
#             padding_x, padding_y = 30, 65
#         else:
#             padding_x, padding_y = 20, 20
#         self.move(screen.left() + padding_x, screen.top() + padding_y)

#     def mousePressEvent(self, event: QMouseEvent):
#         if event.button() == Qt.LeftButton:
#             self._hide_and_close()

#     def show_and_fade(self, duration=6000):
#         self.show()
#         self.anim.setStartValue(0.0)
#         self.anim.setEndValue(1.0)
#         self.anim.start()
        
#         self.kill_timer = QTimer(self)
#         self.kill_timer.setSingleShot(True)
#         self.kill_timer.timeout.connect(self._hide_and_close)
#         self.kill_timer.start(duration)

#     def _hide_and_close(self):
#         try: self.kill_timer.stop()
#         except: pass
        
#         self.anim.stop()
#         self.anim.setStartValue(self.windowOpacity())
#         self.anim.setEndValue(0.0)
#         self.anim.finished.connect(self.deleteLater)
#         self.anim.start()

# # --- MAIN REMINDER CLASS ---
# class Reminder:
#     def __init__(self, main_window):
#         self.main_window = main_window
#         self.last_notify_time = 0
#         self.hud = None

#     def send_break_message(self, engine_output: dict):
#         """Main entry point called by the AI Engine."""
#         msg = engine_output.get("message", "Time for a quick reset.")
#         behavior = engine_output.get("behavior", "Deep Work")
        
#         # 1. Show the HUD (Subtle Overlay)
#         if self.hud:
#             self.hud._hide_and_close()
        
#         self.hud = PremiumHUD(f"{behavior}: {msg}")
#         self.hud.show_and_fade(6000)

#         # 2. Trigger System Notification
#         self._trigger_system_notification("Break Reminder", msg)

#     def _trigger_system_notification(self, title, msg):
#         current_os = platform.system()

#         if current_os == "Darwin":
#             # macOS Native (Apple Review Safe)
#             script = f'display notification "{msg}" with title "{title}" sound name "Glass"'
#             subprocess.run(["osascript", "-e", script])

#         elif current_os == "Windows" and WINOTIFY_AVAILABLE:
#             # Windows Native
#             try:
#                 toast = Notification(app_id="K-Mends AI", title=title, msg=msg, duration="short")
#                 toast.show()
#             except Exception:
#                 pass

#         elif current_os == "Linux":
#             # Linux Native
#             try:
#                 subprocess.run(["notify-send", title, msg])
#             except Exception:
#                 pass










# # Added more premium things
# import os
# import sys
# import time
# import platform
# import subprocess
# import traceback
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QFrame, QProgressBar
# from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
# from PySide6.QtGui import QFont, QMouseEvent

# # --- WINDOWS NOTIFICATION SETUP ---
# WINOTIFY_AVAILABLE = False
# if platform.system() == "Windows":
#     try:
#         from winotify import Notification, audio
#         WINOTIFY_AVAILABLE = True
#     except Exception:
#         WINOTIFY_AVAILABLE = False

# # --- PREMIUM HUD (Top-Left Minimalist Message) ---
# class PremiumHUD(QFrame):
#     """
#     A high-end, top-left glass overlay. 
#     Features: OS-aware fonts, Progress Timer, Click-to-Dismiss, Meeting-Aware.
#     """
#     def __init__(self, message, is_meeting=False, parent=None):
#         super().__init__(parent)
        
#         # Window Flags: Tool mode hides from Dock/Taskbar
#         self.setWindowFlags(
#             Qt.FramelessWindowHint | 
#             Qt.WindowStaysOnTopHint | 
#             Qt.Tool |
#             Qt.NoDropShadowWindowHint
#         )
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.setWindowOpacity(0.0)
        
#         # MAIN LAYOUT
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(10, 10, 10, 10)
        
#         self.container = QFrame()
#         self.container.setObjectName("HUDContainer")
        
#         # PREMIUM GLASS STYLING
#         # Uses a deep-night alpha and a micro-border for Retina sharpness
#         bg_alpha = 235 if is_meeting else 210
#         self.container.setStyleSheet(f"""
#             #HUDContainer {{
#                 background-color: rgba(22, 22, 22, {bg_alpha});
#                 border: 1px solid rgba(255, 255, 255, 0.12);
#                 border-radius: 12px;
#             }}
#         """)
        
#         c_layout = QVBoxLayout(self.container)
#         c_layout.setContentsMargins(20, 14, 20, 10)
        
#         # TYPOGRAPHY
#         self.label = QLabel(message)
#         if platform.system() == "Darwin":
#             # Apple SF Pro: The world-standard for premium UI
#             font = QFont("SF Pro Display", 12)
#             font.setWeight(QFont.Medium)
#             font.setLetterSpacing(QFont.AbsoluteSpacing, -0.3)
#         else:
#             # Windows 11 Segoe UI Variable: Modern and crisp
#             font = QFont("Segoe UI Variable Text", 10)
#             font.setWeight(QFont.DemiBold)
            
#         self.label.setFont(font)
#         self.label.setStyleSheet("color: #F8FAFC; border: none; background: transparent;")
#         self.label.setWordWrap(True)
#         self.label.setFixedWidth(260)
        
#         # PROGRESS BAR (The "Time-Remaining" Indicator)
#         self.progress = QProgressBar()
#         self.progress.setFixedHeight(2)
#         self.progress.setTextVisible(False)
#         self.progress.setRange(0, 100)
#         self.progress.setValue(100)
#         self.progress.setStyleSheet("""
#             QProgressBar {
#                 background: rgba(255, 255, 255, 0.05);
#                 border: none;
#                 border-radius: 1px;
#             }
#             QProgressBar::chunk {
#                 background: rgba(255, 255, 255, 0.3);
#                 border-radius: 1px;
#             }
#         """)
        
#         c_layout.addWidget(self.label)
#         c_layout.addSpacing(10)
#         c_layout.addWidget(self.progress)
#         layout.addWidget(self.container)
        
#         self.adjustSize()
#         self._position_by_os()

#         # FADE ANIMATION
#         self.anim = QPropertyAnimation(self, b"windowOpacity")
#         self.anim.setDuration(500)
#         self.anim.setEasingCurve(QEasingCurve.OutCubic)

#     def _position_by_os(self):
#         screen = QApplication.primaryScreen().availableGeometry()
#         if platform.system() == "Darwin":
#             padding_x, padding_y = 30, 65 # Below macOS Menu Bar
#         else:
#             padding_x, padding_y = 25, 25 # Standard Windows Corner
#         self.move(screen.left() + padding_x, screen.top() + padding_y)

#     def mousePressEvent(self, event: QMouseEvent):
#         if event.button() == Qt.LeftButton:
#             self._hide_and_close()

#     def show_and_fade(self, duration=7000):
#         self.show()
#         self.anim.setStartValue(0.0)
#         self.anim.setEndValue(1.0)
#         self.anim.start()
        
#         # Progress timer update
#         self.remaining_ms = duration
#         self.timer_step = 50 # Update every 50ms for smoothness
#         self.prog_timer = QTimer(self)
#         self.prog_timer.timeout.connect(self._update_progress)
#         self.prog_timer.start(self.timer_step)

#     def _update_progress(self):
#         self.remaining_ms -= self.timer_step
#         if self.remaining_ms <= 0:
#             self.prog_timer.stop()
#             self._hide_and_close()
#         else:
#             # Map remaining time to progress percentage
#             pct = int((self.remaining_ms / 7000) * 100)
#             self.progress.setValue(pct)

#     def _hide_and_close(self):
#         try: self.prog_timer.stop()
#         except: pass
        
#         self.anim.stop()
#         self.anim.setStartValue(self.windowOpacity())
#         self.anim.setEndValue(0.0)
#         self.anim.finished.connect(self.deleteLater)
#         self.anim.start()

# # --- MAIN REMINDER CLASS ---
# class Reminder:
#     def __init__(self, main_window):
#         self.main_window = main_window
#         self.hud = None

#     def send_break_message(self, engine_output: dict):
#         """Logic-aware message delivery."""
#         msg = engine_output.get("message", "Time for a quick reset.")
#         behavior = engine_output.get("behavior", "").lower()
        
#         # MEETING DETECTION: Polite mode check
#         meeting_keywords = ["meeting", "call", "presentation", "zoom", "teams"]
#         is_meeting = any(k in behavior for k in meeting_keywords)

#         # 1. Show the Premium HUD (Always Silent)
#         if self.hud:
#             self.hud._hide_and_close()
        
#         # Clean title for display
#         display_title = "Focus Update" if is_meeting else behavior.title()
#         self.hud = PremiumHUD(f"{display_title}: {msg}", is_meeting=is_meeting)
#         self.hud.show_and_fade(7000)

#         # 2. System Notification (Only if NOT in a meeting)
#         if not is_meeting:
#             self._trigger_system_notification("Break Reminder", msg)

#     def _trigger_system_notification(self, title, msg):
#         current_os = platform.system()
#         if current_os == "Darwin":
#             script = f'display notification "{msg}" with title "{title}" sound name "Glass"'
#             subprocess.run(["osascript", "-e", script])
#         elif current_os == "Windows" and WINOTIFY_AVAILABLE:
#             try:
#                 toast = Notification(app_id="K-Mends AI", title=title, msg=msg, duration="short")
#                 toast.show()
#             except Exception: pass
#         elif current_os == "Linux":
#             try: subprocess.run(["notify-send", title, msg])
#             except Exception: pass












# Added a silence 

# import os
# import sys
# import time
# import platform
# import subprocess
# import traceback
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QFrame, QProgressBar
# from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
# from PySide6.QtGui import QFont, QMouseEvent

# # --- WINDOWS NOTIFICATION SETUP ---
# WINOTIFY_AVAILABLE = False
# if platform.system() == "Windows":
#     try:
#         from winotify import Notification, audio
#         WINOTIFY_AVAILABLE = True
#     except Exception:
#         WINOTIFY_AVAILABLE = False

# # --- PREMIUM HUD (The "Silent Executive" Overlay) ---
# class PremiumHUD(QFrame):
#     """
#     A high-end, top-left glass overlay. 
#     Click to dismiss. Focus-safe. OS-aware fonts. Progress indicator.
#     """
#     def __init__(self, message, is_meeting=False, parent=None):
#         super().__init__(parent)
        
#         # WINDOW FLAGS
#         # Tool: Hides from Taskbar/Dock. StaysOnTop: Ensures visibility.
#         self.setWindowFlags(
#             Qt.FramelessWindowHint | 
#             Qt.WindowStaysOnTopHint | 
#             Qt.Tool |
#             Qt.NoDropShadowWindowHint
#         )
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         # CRITICAL: Ensures the HUD doesn't steal focus while typing
#         self.setAttribute(Qt.WA_ShowWithoutActivating)
#         self.setWindowOpacity(0.0)
        
#         # MAIN LAYOUT
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(10, 10, 10, 10)
        
#         self.container = QFrame()
#         self.container.setObjectName("HUDContainer")
        
#         # PREMIUM GLASS STYLING
#         bg_alpha = 230 if is_meeting else 210
#         self.container.setStyleSheet(f"""
#             #HUDContainer {{
#                 background-color: rgba(22, 22, 22, {bg_alpha});
#                 border: 1px solid rgba(255, 255, 255, 0.12);
#                 border-radius: 12px;
#             }}
#         """)
        
#         c_layout = QVBoxLayout(self.container)
#         c_layout.setContentsMargins(20, 14, 20, 10)
        
#         # TYPOGRAPHY (Executive Grade)
#         self.label = QLabel(message)
#         if platform.system() == "Darwin":
#             # Apple SF Pro: The gold standard for macOS
#             font = QFont("SF Pro Display", 12)
#             font.setWeight(QFont.Medium)
#             font.setLetterSpacing(QFont.AbsoluteSpacing, -0.3)
#         else:
#             # Windows 11 Segoe UI Variable: Modern and crisp
#             font = QFont("Segoe UI Variable Text", 10)
#             font.setWeight(QFont.DemiBold)
            
#         self.label.setFont(font)
#         self.label.setStyleSheet("color: #F8FAFC; border: none; background: transparent;")
#         self.label.setWordWrap(True)
#         self.label.setFixedWidth(260)
        
#         # PROGRESS BAR (The "Time-Remaining" Indicator)
#         self.progress = QProgressBar()
#         self.progress.setFixedHeight(2)
#         self.progress.setTextVisible(False)
#         self.progress.setRange(0, 100)
#         self.progress.setValue(100)
#         self.progress.setStyleSheet("""
#             QProgressBar {
#                 background: rgba(255, 255, 255, 0.05);
#                 border: none;
#                 border-radius: 1px;
#             }
#             QProgressBar::chunk {
#                 background: rgba(255, 255, 255, 0.3);
#                 border-radius: 1px;
#             }
#         """)
        
#         c_layout.addWidget(self.label)
#         c_layout.addSpacing(10)
#         c_layout.addWidget(self.progress)
#         layout.addWidget(self.container)
        
#         self.adjustSize()
#         self._position_by_os()

#         # FADE ANIMATION
#         self.anim = QPropertyAnimation(self, b"windowOpacity")
#         self.anim.setDuration(500)
#         self.anim.setEasingCurve(QEasingCurve.OutCubic)

#     def _position_by_os(self):
#         """Positions the HUD based on the active screen and OS standards."""
#         screen = QApplication.primaryScreen().availableGeometry()
#         current_os = platform.system()
        
#         if current_os == "Darwin": # macOS: Drop below the Menu Bar (Notch-safe)
#             padding_x, padding_y = 30, 65 
#         else: # Windows/Linux
#             padding_x, padding_y = 25, 25 
            
#         self.move(screen.left() + padding_x, screen.top() + padding_y)

#     def mousePressEvent(self, event: QMouseEvent):
#         """Allow user to tap the message to dismiss it instantly."""
#         if event.button() == Qt.LeftButton:
#             self._hide_and_close()

#     def show_and_fade(self, duration=7000):
#         """Initiates the 7-second visibility lifecycle."""
#         self.show()
#         self.anim.setStartValue(0.0)
#         self.anim.setEndValue(1.0)
#         self.anim.start()
        
#         # Progress timer setup
#         self.total_duration = duration
#         self.remaining_ms = duration
#         self.timer_step = 50 
#         self.prog_timer = QTimer(self)
#         self.prog_timer.timeout.connect(self._update_progress)
#         self.prog_timer.start(self.timer_step)

#     def _update_progress(self):
#         """Updates the visual progress bar every 50ms."""
#         self.remaining_ms -= self.timer_step
#         if self.remaining_ms <= 0:
#             self.prog_timer.stop()
#             self._hide_and_close()
#         else:
#             pct = int((self.remaining_ms / self.total_duration) * 100)
#             self.progress.setValue(pct)

#     def _hide_and_close(self):
#         """Animates out and cleans up memory."""
#         try: self.prog_timer.stop()
#         except: pass
        
#         self.anim.stop()
#         self.anim.setStartValue(self.windowOpacity())
#         self.anim.setEndValue(0.0)
#         self.anim.finished.connect(self.deleteLater)
#         self.anim.start()

# # --- MAIN REMINDER CLASS ---
# class Reminder:
#     def __init__(self, main_window):
#         self.main_window = main_window
#         self.hud = None

#     def send_break_message(self, engine_output: dict):
#         """The brain of the reminder system: Handles delivery based on activity."""
#         msg = engine_output.get("message", "Time for a quick reset.")
#         behavior = engine_output.get("behavior", "").lower()
        
#         # MEETING DETECTION: Suppress loud alerts if user is in a call
#         meeting_keywords = ["meeting", "call", "presentation", "zoom", "teams"]
#         is_meeting = any(k in behavior for k in meeting_keywords)

#         # 1. Show the Silent HUD (Always appears, even if minimized)
#         if self.hud:
#             # Close existing HUD to prevent stacking
#             self.hud._hide_and_close()
        
#         display_title = "Polite Update" if is_meeting else behavior.title()
#         self.hud = PremiumHUD(f"{display_title}: {msg}", is_meeting=is_meeting)
#         self.hud.show_and_fade(7000)

#         # 2. Trigger System Notification (Only if user is NOT in a meeting)
#         if not is_meeting:
#             self._trigger_system_notification("Break Reminder", msg)

#     def _trigger_system_notification(self, title, msg):
#         """Triggers the native OS slide-in notification banner."""
#         current_os = platform.system()
        
#         if current_os == "Darwin": # macOS Native
#             script = f'display notification "{msg}" with title "{title}" sound name "Glass"'
#             subprocess.run(["osascript", "-e", script])
            
#         elif current_os == "Windows" and WINOTIFY_AVAILABLE: # Windows Native
#             try:
#                 toast = Notification(app_id="K-Mends AI", title=title, msg=msg, duration="short")
#                 toast.show()
#             except Exception: pass
            
#         elif current_os == "Linux": # Linux Native
#             try: subprocess.run(["notify-send", title, msg])
#             except Exception: pass










# # 27th
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
#         self.container.setStyleSheet(f"#HUDContainer {{ background-color: rgba(22, 22, 22, {bg_alpha}); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; }}")
        
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
#         # The Fix: Verify the underlying C++ object still exists before animating
#         try:
#             if not self or self.anim.state() == QPropertyAnimation.Running and self.windowOpacity() == 0:
#                 return
#             self.prog_timer.stop()
#             self.anim.stop()
#             self.anim.setStartValue(self.windowOpacity())
#             self.anim.setEndValue(0.0)
#             self.anim.finished.connect(self.deleteLater)
#             self.anim.start()
#         except RuntimeError:
#             pass # Object already deleted, nothing to do

# class Reminder:
#     def __init__(self, main_window, min_interval_seconds=5):
#         self.main_window = main_window
#         self.hud = None
#         self.break_count = 0
#         self._last_toast = 0
#         self.min_interval = min_interval_seconds

#     def send_break_message(self, engine_output: dict):
#         now = time.time()
#         if now - self._last_toast < self.min_interval:
#             return

#         self.break_count += 1
#         self._last_toast = now

#         msg = engine_output.get("message", "Time for a quick reset.")
#         behavior = engine_output.get("behavior", "").lower()
#         is_meeting = any(k in behavior for k in ["meeting", "call", "zoom", "teams"])

#         # SAFE HUD CLOSE
#         if self.hud:
#             try:
#                 self.hud._hide_and_close()
#             except (RuntimeError, AttributeError):
#                 self.hud = None

#         display_title = "Polite Update" if is_meeting else behavior.title()
#         self.hud = PremiumHUD(f"{display_title}: {msg}", is_meeting=is_meeting)
#         self.hud.show_and_fade(7000)

#         if not is_meeting:
#             self._trigger_system_notification("Break Reminder", msg)

#     def _trigger_system_notification(self, title, msg):
#         try:
#             current_os = platform.system()
#             if current_os == "Darwin":
#                 subprocess.run(["osascript", "-e", f'display notification "{msg}" with title "{title}" sound name "Glass"'])
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
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.NoDropShadowWindowHint)
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
        self.anim.setDuration(500)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

    def _position_by_os(self):
        screen = QApplication.primaryScreen().availableGeometry()
        p_x, p_y = (30, 65) if platform.system() == "Darwin" else (25, 25)
        self.move(screen.left() + p_x, screen.top() + p_y)

    def mousePressEvent(self, event: QMouseEvent):
        self._hide_and_close()

    def show_and_fade(self, duration=7000):
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
            return  # Block spam, but allow next real break

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
            except (RuntimeError, AttributeError):
                pass
            self.hud = None

        # CREATE NEW HUD
        display_title = "Polite Update" if is_meeting else behavior.title()
        self.hud = PremiumHUD(f"{display_title}: {msg}", is_meeting=is_meeting)
        self.hud.show_and_fade(7000)

        # SYSTEM NOTIFICATION
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
