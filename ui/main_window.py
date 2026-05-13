


# # =============================
# # main_window.py — PART 1/3 (macOS‑aware)
# # =============================

# import time
# import sys
# from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
# from PySide6.QtCore import QTimer, Qt

# from ui.sidebar import Sidebar
# from ui.pages.dashboard import Dashboard
# from ui.pages.smart_mode import SmartModePage
# from ui.pages.ai_mode import AIModePage
# from ui.pages.settings import SettingsPage
# from ui.pages.weekly_analytics import WeeklyAnalyticsPage
# from ui.pages.analytics_suite import AnalyticsSuitePage
# from ui.pages.ai_insights import AIInsightsPage
# from ui.pages.weekly_report import WeeklyReportPage
# from ui.pages.monthly_report import MonthlyReportPage

# from core.settings import SettingsManager
# from core.smart_break_engine import SmartBreakEngine, SmartConfig
# from core.smart_break_engine_v2 import SmartBreakEngineV2
# from core.signal_collector import SignalCollector
# from core.reminder import Reminder
# from core.ai_reminder_messages import AIMessageGenerator
# from core.storage_manager import StorageManager
# from core.daily_summary_engine import DailySummaryEngine
# from ui.widgets.mini_video_window import MiniVideoWindow

# from datetime import datetime

# # =============================
# # WINDOWS-SPECIFIC POWER CONSTANTS (GUARDED)
# # =============================
# if sys.platform == "win32":
#     import ctypes
#     from ctypes import wintypes

#     PBT_APMSUSPEND = 0x0004
#     PBT_APMRESUMEAUTOMATIC = 0x0012
#     PBT_APMRESUMESUSPEND = 0x0007
#     WM_POWERBROADCAST = 0x0218


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Digital Wellbeing Assistant")
#         self.resize(960, 620)
#         self.setMinimumSize(820, 560)

#         # =============================
#         # macOS-aware state tracking
#         # =============================
#         self.last_tick = time.time()
#         self.was_minimized = False

#         # =============================
#         # CORE SYSTEMS
#         # =============================
#         self.settings = SettingsManager()
#         DailySummaryEngine().generate_yesterday()
#         self.signals = SignalCollector()
#         self.hybrid_engine = SmartBreakEngine(SmartConfig())
#         self.ai_engine = SmartBreakEngineV2()
#         self.reminder = Reminder(main_window=self)
#         self.ai_messages = AIMessageGenerator()

#         # Mini always-on-top Lottie window
#         self.break_window = MiniVideoWindow()

#         # =============================
#         # GLOBAL TRACKING
#         # =============================
#         self.app_start_time = time.time()
#         self.global_screen_seconds = 0
#         self.storage = StorageManager()
#         self.last_behavior_log = time.time()
#         self.ai_history = []

#         # =============================
#         # MONITORING STATE
#         # =============================
#         self.monitoring = False
#         self.active_monitoring_mode = None
#         self.poll_interval = 1.0

#         # =============================
#         # LAYOUT
#         # =============================
#         container = QWidget()
#         layout = QHBoxLayout(container)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

#         self.sidebar = Sidebar(self)
#         layout.addWidget(self.sidebar)

#         self.pages = QStackedWidget()
#         layout.addWidget(self.pages, 1)

#         self.dashboard_page = Dashboard(self)
#         self.smart_page = SmartModePage(self)
#         self.ai_mode_page = AIModePage(self)
#         self.settings_page = SettingsPage(self)
#         self.weekly_page = WeeklyAnalyticsPage()
#         self.analytics_page = AnalyticsSuitePage()
#         self.insights_page = AIInsightsPage()
#         self.weekly_report_page = WeeklyReportPage()
#         self.monthly_report_page = MonthlyReportPage()

#         for page in [
#             self.dashboard_page, self.smart_page, self.ai_page, self.settings_page,
#             self.weekly_page, self.analytics_page, self.insights_page,
#             self.weekly_report_page, self.monthly_report_page
#         ]:
#             self.pages.addWidget(page)

#         self.setCentralWidget(container)

#         # =============================
#         # MAIN LOOP TIMER
#         # =============================
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_break_engine)
#         self.timer.start(1000)

#         self.apply_theme()
#         self.show_dashboard()
# # =============================
# # main_window.py — PART 2/3 (macOS‑aware)
# # =============================

#     # =============================
#     # macOS window state helpers
#     # =============================
#     def is_minimized(self):
#         return self.windowState() & Qt.WindowMinimized

#     def is_hidden_or_background(self):
#         return not self.isActiveWindow()

#     # =============================
#     # FATIGUE LEVEL
#     # =============================
#     def fatigue_level(self, score):
#         try:
#             score = float(score)
#         except Exception:
#             return "Low"

#         if score < 25:
#             return "Low"
#         elif score < 50:
#             return "Medium"
#         elif score < 75:
#             return "High"
#         else:
#             return "Critical"

#     # =============================
#     # DASHBOARD DATA
#     # =============================
#     def build_dashboard_data(self):
#         signals = self.signals.to_dict()

#         mode = self.active_monitoring_mode or "No Active Mode"

#         meeting_active = (
#             signals.get("window_category") == "meeting"
#             or signals.get("webcam_active") is True
#         )

#         screen_seconds = self.global_screen_seconds
#         screen_time = time.strftime("%H:%M:%S", time.gmtime(screen_seconds))

#         breaks_taken = getattr(self.reminder, "break_count", 0)

#         raw_behavior = getattr(self.ai_engine, "last_behavior", "—")
#         behavior = str(raw_behavior).replace("_", " ").title()

#         fatigue_score = getattr(self.ai_engine, "last_fatigue", 0.0)
#         fatigue_level = self.fatigue_level(fatigue_score)

#         status = "Monitoring" if self.monitoring else "Not Monitoring"

#         trend_value = screen_seconds

#         return {
#             "screen_time": screen_time,
#             "screen_seconds": screen_seconds,
#             "breaks": str(breaks_taken),
#             "mode": mode,
#             "behavior": behavior,
#             "fatigue_score": float(fatigue_score),
#             "fatigue_level": fatigue_level,
#             "meeting": "On" if meeting_active else "Off",
#             "status": status,
#             "trend_value": trend_value
#         }

#     # =============================
#     # PAGE SWITCHING
#     # =============================
#     def show_dashboard(self): self.pages.setCurrentWidget(self.dashboard_page)
#     def show_smart(self): self.pages.setCurrentWidget(self.smart_page)
#     def show_ai(self): self.pages.setCurrentWidget(self.ai_page)
#     def show_settings(self): self.pages.setCurrentWidget(self.settings_page)
#     def show_weekly(self): self.pages.setCurrentWidget(self.weekly_page)

#     def show_analytics(self):
#         self.analytics_page.refresh_all()
#         self.pages.setCurrentWidget(self.analytics_page)

#     def show_insights(self):
#         self.insights_page.update_insights(self.ai_history)
#         self.pages.setCurrentWidget(self.insights_page)

#     def show_weekly_report(self):
#         self.weekly_report_page.refresh()
#         self.pages.setCurrentWidget(self.weekly_report_page)

#     def show_monthly_report(self):
#         self.monthly_report_page.refresh()
#         self.pages.setCurrentWidget(self.monthly_report_page)

#     # =============================
#     # MONITORING TOGGLE
#     # =============================
#     def toggle_monitoring(self):

#         self.monitoring = not self.monitoring

#         if self.monitoring:
#             if self.pages.currentWidget() == self.smart_page:
#                 self.active_monitoring_mode = "Smart Mode"
#                 self.hybrid_engine.reset_after_break()

#             elif self.pages.currentWidget() == self.ai_page:
#                 self.active_monitoring_mode = "AI Mode"
#                 self.ai_engine.session_start = time.time()
#                 self.ai_engine.real_time = 0
#         else:
#             self.active_monitoring_mode = None

#         print("Monitoring:", "ON" if self.monitoring else "OFF")

#     # =============================
#     # THEME
#     # =============================
#     def apply_theme(self):
#         theme_name = self.settings.get("theme")
#         path = f"assets/themes/{theme_name}.qss"

#         try:
#             with open(path, "r") as f:
#                 self.setStyleSheet(f.read())
#         except Exception as e:
#             print(f"Failed to load theme {path}: {e}")

#     # =============================
#     # OS SLEEP / RESUME HANDLERS
#     # =============================
#     def handle_os_sleep(self):
#         now = time.time()
#         print("[SYSTEM] Sleep detected — resetting engines")

#         # Reset Smart Mode engine
#         self.hybrid_engine.session_start = now
#         self.hybrid_engine.last_break_time = now - self.hybrid_engine.config.min_interval
#         self.hybrid_engine.last_behavior = "Idle"
#         self.hybrid_engine.last_fatigue = 0.0

#         # Reset AI Mode engine
#         self.ai_engine.session_start = now
#         self.ai_engine.real_time = 0
#         if hasattr(self.ai_engine, "last_break_time"):
#             self.ai_engine.last_break_time = now - self.ai_engine.min_interval

#     def handle_os_resume(self):
#         self.handle_os_sleep()
# # =============================
# # main_window.py — PART 3/3 (macOS‑aware)
# # =============================

#     # =============================
#     # WINDOWS NATIVE EVENT (SLEEP/RESUME)
#     # =============================
#     def nativeEvent(self, eventType, message):
#         if sys.platform == "win32":
#             try:
#                 msg = ctypes.cast(message, ctypes.POINTER(wintypes.MSG)).contents
#                 if msg.message == WM_POWERBROADCAST:
#                     wparam = msg.wParam
#                     if wparam == PBT_APMSUSPEND:
#                         print("[SYSTEM] OS Sleep (Windows) detected via WM_POWERBROADCAST")
#                         self.handle_os_sleep()
#                     elif wparam in (PBT_APMRESUMEAUTOMATIC, PBT_APMRESUMESUSPEND):
#                         print("[SYSTEM] OS Resume (Windows) detected via WM_POWERBROADCAST")
#                         self.handle_os_resume()
#             except Exception:
#                 pass

#         return False, 0

#     # =============================
#     # BREAK ENGINE LOOP (macOS‑aware)
#     # =============================
#     def update_break_engine(self):

#         now = time.time()
#         last_tick = self.last_tick
#         self.last_tick = now

#         # =============================
#         # macOS-aware time-jump handling
#         # =============================
#         if sys.platform == "darwin":
#             if self.is_minimized():
#                 if now - last_tick > 120:
#                     print("[macOS] Ignoring time-jump (window minimized)")
#             else:
#                 if now - last_tick > 120:
#                     print("[SYSTEM] Sleep detected via time-jump fallback")
#                     self.handle_os_sleep()
#                     return

#         else:
#             if now - last_tick > 120:
#                 print("[SYSTEM] Sleep detected via time-jump fallback")
#                 self.handle_os_sleep()
#                 return

#         # =============================
#         # Global time
#         # =============================
#         if self.monitoring:
#             self.global_screen_seconds = int(time.time() - self.app_start_time)

#         # Update dashboard
#         data = self.build_dashboard_data()
#         self.dashboard_page.update_dashboard(data)

#         if not self.monitoring or not self.active_monitoring_mode:
#             return

#         # Update signals
#         self.signals.update()
#         signals = self.signals.to_dict()
#         self.last_signals = signals

#         should_break = False
#         decision = None

#         # =============================
#         # SMART MODE
#         # =============================
#         if self.active_monitoring_mode == "Smart Mode":

#             decision = self.hybrid_engine.should_trigger_break(signals)

#             behavior = decision.get("behavior", "Activity")
#             fatigue = decision.get("fatigue_score", 0.0)
#             reason = decision.get("reason", "")
#             trigger = decision.get("trigger", False)

#             # Convert seconds → minutes
#             raw_seconds = decision.get(
#                 "next_break_seconds",
#                 decision.get("interval_used", 20 * 60)
#             )
#             next_break_minutes = max(0, round(raw_seconds / 60))

#             self.smart_page.update_smart_status(
#                 behavior=behavior,
#                 fatigue=fatigue,
#                 reason=reason,
#                 trigger=trigger,
#                 next_break_seconds=next_break_minutes
#             )

#             should_break = trigger

#         # =============================
#         # AI MODE
#         # =============================
#         elif self.active_monitoring_mode == "AI Mode":

#             if self.ai_engine.session_start is None:
#                 self.ai_engine.session_start = time.time()

#             self.ai_engine.real_time = time.time() - self.ai_engine.session_start

#             decision = self.ai_engine.should_trigger_break(signals)

#             self.ai_history.append({
#                 "timestamp": datetime.now(),
#                 "behavior": decision.get("behavior", "Idle"),
#                 "fatigue": decision.get("fatigue_score", 0.0),
#                 "break_triggered": decision.get("trigger", False),
#                 "break_reason": decision.get("reason", ""),
#                 "suppression": False
#             })

#             self.insights_page.update_insights(self.ai_history)

#             should_break = decision.get("trigger", False)

#             self.ai_engine.last_behavior = decision.get("behavior", "Idle")
#             self.ai_engine.last_fatigue = decision.get("fatigue_score", 0.0)

#             # Convert seconds → minutes
#             raw_seconds = decision.get(
#                 "remaining_seconds",
#                 decision.get("interval_used", 20 * 60)
#             )
#             next_break_minutes = max(0, round(raw_seconds / 60))

#             self.ai_page.update_ai_status(
#                 behavior=self.ai_engine.last_behavior,
#                 fatigue=self.ai_engine.last_fatigue,
#                 reason=decision.get("reason", ""),
#                 trigger=decision.get("trigger", False),
#                 next_break_seconds=next_break_minutes
#             )

#         # =============================
#         # BREAK TRIGGER
#         # =============================
#         if not should_break:
#             return

#         # Video disabled
#         # self.break_window.play_stepping_away(duration_ms=6000)

#         # AI MODE BREAK
#         if decision and self.active_monitoring_mode == "AI Mode":
#             engine_output = {
#                 "behavior": decision.get("behavior", "Activity"),
#                 "reason": decision.get("reason", ""),
#                 "message": decision.get("message", "Take a moment to pause."),
#                 "interval_used": decision.get("interval_used", 20 * 60),
#                 "last_break_time": decision.get("last_break_time", time.time()),
#                 "trigger": decision.get("trigger", True),
#             }

#             self.last_engine_output = engine_output
#             self.reminder.send_break_message(engine_output)
#             return

#         # SMART MODE BREAK
#         engine_output = {
#             "behavior": decision.get("behavior", "Activity"),
#             "reason": decision.get("reason", ""),
#             "message": decision.get("message", "Smart Mode suggests a short break."),
#             "interval_used": decision.get("interval_used", 20 * 60),
#             "last_break_time": decision.get("last_break_time", time.time()),
#             "trigger": True,
#         }

#         self.last_engine_output = engine_output
#         self.reminder.send_break_message(engine_output)

#     # =============================
#     # BREAK MODAL HANDLER
#     # =============================
#     def show_break_modal(self, engine_output):
#         from ui.dialogs.break_modal import BreakModal

#         was_monitoring = self.monitoring
#         self.monitoring = False

#         modal = BreakModal(engine_output, parent=self)
#         result = modal.exec()

#         self.monitoring = was_monitoring

#         if result == 1:
#             if self.active_monitoring_mode == "Smart Mode":
#                 self.hybrid_engine.reset_after_break()
#             elif self.active_monitoring_mode == "AI Mode":
#                 self.ai_engine.session_start = time.time()
#                 self.ai_engine.real_time = 0

#     def closeEvent(self, event):
#         from core.daily_summary_engine import DailySummaryEngine
#         DailySummaryEngine().generate_today()
#         event.accept()































#THIS IS THE PART i AM ADDING THE LOGO AND STARTING IN WINDOW

# # =============================
# # main_window.py — PART 1/3 (macOS‑aware)
# # =============================

# import time
# import sys
# from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QApplication
# from PySide6.QtCore import QTimer, Qt

# from ui.sidebar import Sidebar
# from ui.pages.dashboard import Dashboard
# from ui.pages.smart_mode import SmartModePage
# from ui.pages.ai_mode import AIModePage
# from ui.pages.settings import SettingsPage
# from ui.pages.weekly_analytics import WeeklyAnalyticsPage
# from ui.pages.analytics_suite import AnalyticsSuitePage
# from ui.pages.ai_insights import AIInsightsPage
# from ui.pages.weekly_report import WeeklyReportPage
# from ui.pages.monthly_report import MonthlyReportPage

# from core.settings import SettingsManager
# from core.smart_break_engine import SmartBreakEngine, SmartConfig
# from core.smart_break_engine_v2 import SmartBreakEngineV2
# from core.signal_collector import SignalCollector
# from core.reminder import Reminder
# from core.ai_reminder_messages import AIMessageGenerator
# from core.storage_manager import StorageManager
# from core.daily_summary_engine import DailySummaryEngine
# from ui.widgets.mini_video_window import MiniVideoWindow

# from datetime import datetime

# from PySide6.QtWidgets import QSystemTrayIcon, QMenu
# from PySide6.QtGui import QIcon, QAction

# # =============================
# # WINDOWS-SPECIFIC POWER CONSTANTS (GUARDED)
# # =============================
# if sys.platform == "win32":
#     import ctypes
#     from ctypes import wintypes

#     PBT_APMSUSPEND = 0x0004
#     PBT_APMRESUMEAUTOMATIC = 0x0012
#     PBT_APMRESUMESUSPEND = 0x0007
#     WM_POWERBROADCAST = 0x0218


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Digital Wellbeing Assistant")
#         self.resize(960, 620)
#         self.setMinimumSize(820, 560)

#         # =============================
#         # macOS-aware state tracking
#         # =============================
#         self.last_tick = time.time()
#         self.was_minimized = False

#         # =============================
#         # CORE SYSTEMS
#         # =============================
#         self.settings = SettingsManager()
#         DailySummaryEngine().generate_yesterday()
#         self.signals = SignalCollector()
#         self.hybrid_engine = SmartBreakEngine(SmartConfig())
#         self.ai_engine = SmartBreakEngineV2()
#         self.reminder = Reminder(main_window=self)
#         self.ai_messages = AIMessageGenerator()

#         # Mini always-on-top Lottie window
#         self.break_window = MiniVideoWindow()

#         # =============================
#         # GLOBAL TRACKING
#         # =============================
#         self.app_start_time = time.time()
#         self.global_screen_seconds = 0
#         self.storage = StorageManager()
#         self.last_behavior_log = time.time()
#         self.ai_history = []

#         # =============================
#         # MONITORING STATE
#         # =============================
#         self.monitoring = False
#         self.active_monitoring_mode = None
#         self.poll_interval = 1.0

#         # =============================
#         # LAYOUT
#         # =============================
#         container = QWidget()
#         layout = QHBoxLayout(container)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

#         self.sidebar = Sidebar(self)
#         layout.addWidget(self.sidebar)

#         self.pages = QStackedWidget()
#         layout.addWidget(self.pages, 1)

#         self.dashboard_page = Dashboard(self)
#         self.smart_page = SmartModePage(self)
#         self.ai_page = AIModePage(self)
#         self.settings_page = SettingsPage(self)
#         self.weekly_page = WeeklyAnalyticsPage()
#         self.analytics_page = AnalyticsSuitePage()
#         self.insights_page = AIInsightsPage()
#         self.weekly_report_page = WeeklyReportPage()
#         self.monthly_report_page = MonthlyReportPage()

#         for page in [
#             self.dashboard_page, self.smart_page, self.ai_page, self.settings_page,
#             self.weekly_page, self.analytics_page, self.insights_page,
#             self.weekly_report_page, self.monthly_report_page
#         ]:
#             self.pages.addWidget(page)

#         self.setCentralWidget(container)

#         # =============================
#         # MAIN LOOP TIMER
#         # =============================
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_break_engine)
#         self.timer.start(1000)

#         self.apply_theme()
#         self.show_dashboard()

#     def setup_system_tray(self):
#         # 1. Create the Tray Icon
#         self.tray_icon = QSystemTrayIcon(self)
        
#         # Point this to your logo (use the relative path that works for you)
#         self.tray_icon.setIcon(QIcon("assets/icons/logo.png")) 
        
#         # 2. Create the Menu
#         tray_menu = QMenu()
        
#         show_action = QAction("Open Dashboard", self)
#         show_action.triggered.connect(self.show_and_activate)
        
#         quit_action = QAction("Exit K-Mends", self)
#         quit_action.triggered.connect(QApplication.instance().quit)
        
#         tray_menu.addAction(show_action)
#         tray_menu.addSeparator()
#         tray_menu.addAction(quit_action)
        
#         self.tray_icon.setContextMenu(tray_menu)
        
#         # 3. Handle Double Click on the Tray Icon
#         self.tray_icon.activated.connect(self.on_tray_icon_activated)
        
#         self.tray_icon.show()

#     def on_tray_icon_activated(self, reason):
#         if reason == QSystemTrayIcon.DoubleClick:
#             self.show_and_activate()

#     def show_and_activate(self):
#         self.showNormal()
#         self.activateWindow()
#         self.raise_()

#     # Add this to handle the 'X' button
#     def closeEvent(self, event):
#         # If the user clicks 'X', we just hide it to the tray
#         if self.tray_icon.isVisible():
#             self.hide()
#             event.ignore()

#     # =============================
#     # macOS window state helpers
#     # =============================
#     def is_minimized(self):
#         return self.windowState() & Qt.WindowMinimized

#     def is_hidden_or_background(self):
#         return not self.isActiveWindow()

#     # =============================
#     # FATIGUE LEVEL
#     # =============================
#     def fatigue_level(self, score):
#         try:
#             score = float(score)
#         except Exception:
#             return "Low"

#         if score < 25:
#             return "Low"
#         elif score < 50:
#             return "Medium"
#         elif score < 75:
#             return "High"
#         else:
#             return "Critical"

#     # =============================
#     # DASHBOARD DATA
#     # =============================
#     def build_dashboard_data(self):
#         signals = self.signals.to_dict()

#         mode = self.active_monitoring_mode or "No Active Mode"

#         meeting_active = (
#             signals.get("window_category") == "meeting"
#             or signals.get("webcam_active") is True
#         )

#         screen_seconds = self.global_screen_seconds
#         screen_time = time.strftime("%H:%M:%S", time.gmtime(screen_seconds))

#         breaks_taken = getattr(self.reminder, "break_count", 0)

#         raw_behavior = getattr(self.ai_engine, "last_behavior", "—")
#         behavior = str(raw_behavior).replace("_", " ").title()

#         fatigue_score = getattr(self.ai_engine, "last_fatigue", 0.0)
#         fatigue_level = self.fatigue_level(fatigue_score)

#         status = "Monitoring" if self.monitoring else "Not Monitoring"

#         trend_value = screen_seconds

#         return {
#             "screen_time": screen_time,
#             "screen_seconds": screen_seconds,
#             "breaks": str(breaks_taken),
#             "mode": mode,
#             "behavior": behavior,
#             "fatigue_score": float(fatigue_score),
#             "fatigue_level": fatigue_level,
#             "meeting": "On" if meeting_active else "Off",
#             "status": status,
#             "trend_value": trend_value
#         }

#     # =============================
#     # PAGE SWITCHING
#     # =============================
#     def show_dashboard(self): self.pages.setCurrentWidget(self.dashboard_page)
#     def show_smart(self): self.pages.setCurrentWidget(self.smart_page)
#     def show_ai(self): self.pages.setCurrentWidget(self.ai_page)
#     def show_settings(self): self.pages.setCurrentWidget(self.settings_page)
#     def show_weekly(self): self.pages.setCurrentWidget(self.weekly_page)

#     def show_analytics(self):
#         self.analytics_page.refresh_all()
#         self.pages.setCurrentWidget(self.analytics_page)

#     def show_insights(self):
#         self.insights_page.update_insights(self.ai_history)
#         self.pages.setCurrentWidget(self.insights_page)

#     def show_weekly_report(self):
#         self.weekly_report_page.refresh()
#         self.pages.setCurrentWidget(self.weekly_report_page)

#     def show_monthly_report(self):
#         self.monthly_report_page.refresh()
#         self.pages.setCurrentWidget(self.monthly_report_page)

#     # =============================
#     # MONITORING TOGGLE
#     # =============================
#     def toggle_monitoring(self):

#         self.monitoring = not self.monitoring

#         if self.monitoring:
#             if self.pages.currentWidget() == self.smart_page:
#                 self.active_monitoring_mode = "Smart Mode"
#                 self.hybrid_engine.reset_after_break()

#             elif self.pages.currentWidget() == self.ai_page:
#                 self.active_monitoring_mode = "AI Mode"
#                 self.ai_engine.session_start = time.time()
#                 self.ai_engine.real_time = 0
#         else:
#             self.active_monitoring_mode = None

#         print("Monitoring:", "ON" if self.monitoring else "OFF")

#     # =============================
#     # THEME
#     # =============================
#     def apply_theme(self):
#         theme_name = self.settings.get("theme")
#         path = f"assets/themes/{theme_name}.qss"

#         try:
#             with open(path, "r") as f:
#                 self.setStyleSheet(f.read())
#         except Exception as e:
#             print(f"Failed to load theme {path}: {e}")

#     # =============================
#     # OS SLEEP / RESUME HANDLERS
#     # =============================
#     def handle_os_sleep(self):
#         now = time.time()
#         print("[SYSTEM] Sleep detected — resetting engines")

#         # Reset Smart Mode engine
#         self.hybrid_engine.session_start = now
#         self.hybrid_engine.last_break_time = now - self.hybrid_engine.config.min_interval
#         self.hybrid_engine.last_behavior = "Idle"
#         self.hybrid_engine.last_fatigue = 0.0

#         # Reset AI Mode engine
#         self.ai_engine.session_start = now
#         self.ai_engine.real_time = 0
#         if hasattr(self.ai_engine, "last_break_time"):
#             self.ai_engine.last_break_time = now - self.ai_engine.min_interval

#     def handle_os_resume(self):
#         self.handle_os_sleep()
# # =============================
# # main_window.py — PART 3/3 (macOS‑aware)
# # =============================

#     # =============================
#     # WINDOWS NATIVE EVENT (SLEEP/RESUME)
#     # =============================
#     def nativeEvent(self, eventType, message):
#         if sys.platform == "win32":
#             try:
#                 msg = ctypes.cast(message, ctypes.POINTER(wintypes.MSG)).contents
#                 if msg.message == WM_POWERBROADCAST:
#                     wparam = msg.wParam
#                     if wparam == PBT_APMSUSPEND:
#                         print("[SYSTEM] OS Sleep (Windows) detected via WM_POWERBROADCAST")
#                         self.handle_os_sleep()
#                     elif wparam in (PBT_APMRESUMEAUTOMATIC, PBT_APMRESUMESUSPEND):
#                         print("[SYSTEM] OS Resume (Windows) detected via WM_POWERBROADCAST")
#                         self.handle_os_resume()
#             except Exception:
#                 pass

#         return False, 0

#     # =============================
#     # BREAK ENGINE LOOP (macOS‑aware)
#     # =============================
#     def update_break_engine(self):

#         now = time.time()
#         last_tick = self.last_tick
#         self.last_tick = now

#         # =============================
#         # macOS-aware time-jump handling
#         # =============================
#         if sys.platform == "darwin":
#             if self.is_minimized():
#                 if now - last_tick > 120:
#                     print("[macOS] Ignoring time-jump (window minimized)")
#             else:
#                 if now - last_tick > 120:
#                     print("[SYSTEM] Sleep detected via time-jump fallback")
#                     self.handle_os_sleep()
#                     return

#         else:
#             if now - last_tick > 120:
#                 print("[SYSTEM] Sleep detected via time-jump fallback")
#                 self.handle_os_sleep()
#                 return

#         # =============================
#         # Global time
#         # =============================
#         if self.monitoring:
#             self.global_screen_seconds = int(time.time() - self.app_start_time)

#         # Update dashboard
#         data = self.build_dashboard_data()
#         self.dashboard_page.update_dashboard(data)

#         if not self.monitoring or not self.active_monitoring_mode:
#             return

#         # Update signals
#         self.signals.update()
#         signals = self.signals.to_dict()
#         self.last_signals = signals

#         should_break = False
#         decision = None

#         # =============================
#         # SMART MODE
#         # =============================
#         if self.active_monitoring_mode == "Smart Mode":

#             decision = self.hybrid_engine.should_trigger_break(signals)

#             behavior = decision.get("behavior", "Activity")
#             fatigue = decision.get("fatigue_score", 0.0)
#             reason = decision.get("reason", "")
#             trigger = decision.get("trigger", False)

#             # Convert seconds → minutes
#             raw_seconds = decision.get(
#                 "next_break_seconds",
#                 decision.get("interval_used", 20 * 60)
#             )
#             next_break_minutes = max(0, round(raw_seconds / 60))

#             self.smart_page.update_smart_status(
#                 behavior=behavior,
#                 fatigue=fatigue,
#                 reason=reason,
#                 trigger=trigger,
#                 next_break_seconds=next_break_minutes
#             )

#             should_break = trigger

#         # =============================
#         # AI MODE
#         # =============================
#         elif self.active_monitoring_mode == "AI Mode":

#             if self.ai_engine.session_start is None:
#                 self.ai_engine.session_start = time.time()

#             self.ai_engine.real_time = time.time() - self.ai_engine.session_start

#             decision = self.ai_engine.should_trigger_break(signals)

#             self.ai_history.append({
#                 "timestamp": datetime.now(),
#                 "behavior": decision.get("behavior", "Idle"),
#                 "fatigue": decision.get("fatigue_score", 0.0),
#                 "break_triggered": decision.get("trigger", False),
#                 "break_reason": decision.get("reason", ""),
#                 "suppression": False
#             })

#             self.insights_page.update_insights(self.ai_history)

#             should_break = decision.get("trigger", False)

#             self.ai_engine.last_behavior = decision.get("behavior", "Idle")
#             self.ai_engine.last_fatigue = decision.get("fatigue_score", 0.0)

#             # Convert seconds → minutes
#             raw_seconds = decision.get(
#                 "remaining_seconds",
#                 decision.get("interval_used", 20 * 60)
#             )
#             next_break_minutes = max(0, round(raw_seconds / 60))

#             self.ai_page.update_ai_status(
#                 behavior=self.ai_engine.last_behavior,
#                 fatigue=self.ai_engine.last_fatigue,
#                 reason=decision.get("reason", ""),
#                 trigger=decision.get("trigger", False),
#                 next_break_seconds=next_break_minutes
#             )

#         # =============================
#         # BREAK TRIGGER
#         # =============================
#         if not should_break:
#             return

#         # Video disabled
#         # self.break_window.play_stepping_away(duration_ms=6000)

#         # AI MODE BREAK
#         if decision and self.active_monitoring_mode == "AI Mode":
#             engine_output = {
#                 "behavior": decision.get("behavior", "Activity"),
#                 "reason": decision.get("reason", ""),
#                 "message": decision.get("message", "Take a moment to pause."),
#                 "interval_used": decision.get("interval_used", 20 * 60),
#                 "last_break_time": decision.get("last_break_time", time.time()),
#                 "trigger": decision.get("trigger", True),
#             }

#             self.last_engine_output = engine_output
#             self.reminder.send_break_message(engine_output)
#             return

#         # SMART MODE BREAK
#         engine_output = {
#             "behavior": decision.get("behavior", "Activity"),
#             "reason": decision.get("reason", ""),
#             "message": decision.get("message", "Smart Mode suggests a short break."),
#             "interval_used": decision.get("interval_used", 20 * 60),
#             "last_break_time": decision.get("last_break_time", time.time()),
#             "trigger": True,
#         }

#         self.last_engine_output = engine_output
#         self.reminder.send_break_message(engine_output)

#     # =============================
#     # BREAK MODAL HANDLER
#     # =============================
#     def show_break_modal(self, engine_output):
#         from ui.dialogs.break_modal import BreakModal

#         was_monitoring = self.monitoring
#         self.monitoring = False

#         modal = BreakModal(engine_output, parent=self)
#         result = modal.exec()

#         self.monitoring = was_monitoring

#         if result == 1:
#             if self.active_monitoring_mode == "Smart Mode":
#                 self.hybrid_engine.reset_after_break()
#             elif self.active_monitoring_mode == "AI Mode":
#                 self.ai_engine.session_start = time.time()
#                 self.ai_engine.real_time = 0

#     def closeEvent(self, event):
#         from core.daily_summary_engine import DailySummaryEngine
#         DailySummaryEngine().generate_today()
#         event.accept()


















# This was not firing the notifications

# import time
# import sys
# import os
# from datetime import datetime
# from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget, 
#                                QApplication, QSystemTrayIcon, QMenu)
# from PySide6.QtCore import QTimer, Qt
# from PySide6.QtGui import QIcon, QAction

# # Internal UI Imports
# from ui.sidebar import Sidebar
# from ui.pages.dashboard import Dashboard
# from ui.pages.smart_mode import SmartModePage
# from ui.pages.ai_mode import AIModePage
# from ui.pages.settings import SettingsPage
# from ui.pages.weekly_analytics import WeeklyAnalyticsPage
# from ui.pages.analytics_suite import AnalyticsSuitePage
# from ui.pages.ai_insights import AIInsightsPage
# from ui.pages.weekly_report import WeeklyReportPage
# from ui.pages.monthly_report import MonthlyReportPage

# # Internal Core Imports
# from core.settings import SettingsManager
# from core.smart_break_engine import SmartBreakEngine, SmartConfig
# from core.smart_break_engine_v2 import SmartBreakEngineV2
# from core.signal_collector import SignalCollector
# from core.reminder import Reminder
# from core.ai_reminder_messages import AIMessageGenerator
# from core.storage_manager import StorageManager
# from core.daily_summary_engine import DailySummaryEngine
# from ui.widgets.mini_video_window import MiniVideoWindow


# def resource_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# # =============================
# # WINDOWS-SPECIFIC POWER CONSTANTS (GUARDED)
# # =============================
# if sys.platform == "win32":
#     import ctypes
#     from ctypes import wintypes

#     PBT_APMSUSPEND = 0x0004
#     PBT_APMRESUMEAUTOMATIC = 0x0012
#     PBT_APMRESUMESUSPEND = 0x0007
#     WM_POWERBROADCAST = 0x0218

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # --- DYNAMIC PATH LOGIC ---
#         #basedir = os.path.dirname(os.path.abspath(__file__))
#         #project_root = os.path.dirname(basedir) 
#         #self.icon_path = os.path.join(project_root, "assets", "icons", "logo.png")
#         self.icon_path = resource_path(os.path.join("assets", "icons", "logo.png"))
        
#         # Set Window/Taskbar Icon
#         self.setWindowIcon(QIcon(self.icon_path))

#         self.setWindowTitle("Digital Wellbeing Assistant")
#         self.resize(960, 620)
#         self.setMinimumSize(820, 560)

#         # macOS-aware state tracking
#         self.last_tick = time.time()
#         self.was_minimized = False

#         # CORE SYSTEMS
#         self.settings = SettingsManager()
#         DailySummaryEngine().generate_yesterday()
#         self.signals = SignalCollector()
#         self.hybrid_engine = SmartBreakEngine(SmartConfig())
#         self.ai_engine = SmartBreakEngineV2()
#         self.reminder = Reminder(main_window=self)
#         self.ai_messages = AIMessageGenerator()
#         self.break_window = MiniVideoWindow()

#         # GLOBAL TRACKING
#         self.app_start_time = time.time()
#         self.global_screen_seconds = 0
#         self.storage = StorageManager()
#         self.last_behavior_log = time.time()
#         self.ai_history = []

#         # MONITORING STATE
#         self.monitoring = False
#         self.active_monitoring_mode = None
#         self.poll_interval = 1.0

#         # LAYOUT
#         container = QWidget()
#         layout = QHBoxLayout(container)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

#         self.sidebar = Sidebar(self)
#         layout.addWidget(self.sidebar)

#         self.pages = QStackedWidget()
#         layout.addWidget(self.pages, 1)

#         self.dashboard_page = Dashboard(self)
#         self.smart_page = SmartModePage(self)
#         self.ai_page = AIModePage(self)
#         self.settings_page = SettingsPage(self)
#         self.weekly_page = WeeklyAnalyticsPage()
#         self.analytics_page = AnalyticsSuitePage()
#         self.insights_page = AIInsightsPage()
#         self.weekly_report_page = WeeklyReportPage()
#         self.monthly_report_page = MonthlyReportPage()

#         for page in [
#             self.dashboard_page, self.smart_page, self.ai_page, self.settings_page,
#             self.weekly_page, self.analytics_page, self.insights_page,
#             self.weekly_report_page, self.monthly_report_page
#         ]:
#             self.pages.addWidget(page)

#         self.setCentralWidget(container)

#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_break_engine)
#         self.timer.start(1000)

#         self.apply_theme()
#         self.show_dashboard()
        
#         # ACTIVATE TRAY
#         self.setup_system_tray()
    
#     def setup_system_tray(self):
#         self.tray_icon = QSystemTrayIcon(self)
#         self.tray_icon.setIcon(QIcon(self.icon_path)) 
        
#         tray_menu = QMenu()
#         show_action = QAction("Open Dashboard", self)
#         show_action.triggered.connect(self.show_and_activate)
        
#         quit_action = QAction("Exit K-Mends", self)
#         quit_action.triggered.connect(QApplication.instance().quit)
        
#         tray_menu.addAction(show_action)
#         tray_menu.addSeparator()
#         tray_menu.addAction(quit_action)
        
#         self.tray_icon.setContextMenu(tray_menu)
#         self.tray_icon.activated.connect(self.on_tray_icon_activated)
#         self.tray_icon.show()

#     def on_tray_icon_activated(self, reason):
#         if reason == QSystemTrayIcon.DoubleClick:
#             self.show_and_activate()

#     def show_and_activate(self):
#         self.showNormal()
#         self.activateWindow()
#         self.raise_()

#     def closeEvent(self, event):
#         if self.tray_icon.isVisible():
#             self.hide()
#             event.ignore()
#         else:
#             DailySummaryEngine().generate_today()
#             event.accept()

#     def is_minimized(self):
#         return self.windowState() & Qt.WindowMinimized

#     def is_hidden_or_background(self):
#         return not self.isActiveWindow()

#     def fatigue_level(self, score):
#         try:
#             score = float(score)
#         except Exception:
#             return "Low"
#         if score < 25: return "Low"
#         elif score < 50: return "Medium"
#         elif score < 75: return "High"
#         else: return "Critical"
    
#     def update_break_engine(self):
#         now = time.time()
#         last_tick = self.last_tick
#         self.last_tick = now

#         if sys.platform == "darwin":
#             if self.is_minimized():
#                 if now - last_tick > 120: return
#             else:
#                 if now - last_tick > 120:
#                     self.handle_os_sleep()
#                     return
#         else:
#             if now - last_tick > 120:
#                 self.handle_os_sleep()
#                 return

#         if self.monitoring:
#             self.global_screen_seconds = int(time.time() - self.app_start_time)

#         data = self.build_dashboard_data()
#         self.dashboard_page.update_dashboard(data)

#         if not self.monitoring or not self.active_monitoring_mode:
#             return

#         self.signals.update()
#         signals = self.signals.to_dict()
#         self.last_signals = signals
#         should_break = False
#         decision = None

#         if self.active_monitoring_mode == "Smart Mode":
#             decision = self.hybrid_engine.should_trigger_break(signals)
#             behavior = decision.get("behavior", "Activity")
#             fatigue = decision.get("fatigue_score", 0.0)
#             reason = decision.get("reason", "")
#             trigger = decision.get("trigger", False)
#             raw_seconds = decision.get("next_break_seconds", decision.get("interval_used", 1200))
#             self.smart_page.update_smart_status(
#                 behavior=behavior, fatigue=fatigue, reason=reason, 
#                 trigger=trigger, next_break_seconds=max(0, round(raw_seconds / 60))
#             )
#             should_break = trigger

#         elif self.active_monitoring_mode == "AI Mode":
#             if self.ai_engine.session_start is None:
#                 self.ai_engine.session_start = time.time()
#             self.ai_engine.real_time = time.time() - self.ai_engine.session_start
#             decision = self.ai_engine.should_trigger_break(signals)
            
#             self.ai_history.append({
#                 "timestamp": datetime.now(),
#                 "behavior": decision.get("behavior", "Idle"),
#                 "fatigue": decision.get("fatigue_score", 0.0),
#                 "break_triggered": decision.get("trigger", False),
#                 "break_reason": decision.get("reason", ""),
#                 "suppression": False
#             })
#             self.insights_page.update_insights(self.ai_history)
#             should_break = decision.get("trigger", False)
#             self.ai_engine.last_behavior = decision.get("behavior", "Idle")
#             self.ai_engine.last_fatigue = decision.get("fatigue_score", 0.0)
#             raw_seconds = decision.get("remaining_seconds", decision.get("interval_used", 1200))
#             self.ai_page.update_ai_status(
#                 behavior=self.ai_engine.last_behavior, fatigue=self.ai_engine.last_fatigue,
#                 reason=decision.get("reason", ""), trigger=should_break, 
#                 next_break_seconds=max(0, round(raw_seconds / 60))
#             )

#         if not should_break: return

#         engine_output = {
#             "behavior": decision.get("behavior", "Activity"),
#             "reason": decision.get("reason", ""),
#             "message": decision.get("message", "Suggesting a short break."),
#             "interval_used": decision.get("interval_used", 1200),
#             "last_break_time": decision.get("last_break_time", time.time()),
#             "trigger": True,
#         }
#         self.last_engine_output = engine_output
#         self.reminder.send_break_message(engine_output)
#     def build_dashboard_data(self):
#         signals = self.signals.to_dict()
#         mode = self.active_monitoring_mode or "No Active Mode"
#         meeting_active = (signals.get("window_category") == "meeting" or signals.get("webcam_active") is True)
#         screen_time = time.strftime("%H:%M:%S", time.gmtime(self.global_screen_seconds))
#         behavior = str(getattr(self.ai_engine, "last_behavior", "—")).replace("_", " ").title()
#         fatigue_score = getattr(self.ai_engine, "last_fatigue", 0.0)
        
#         return {
#             "screen_time": screen_time, "screen_seconds": self.global_screen_seconds,
#             "breaks": str(getattr(self.reminder, "break_count", 0)), "mode": mode,
#             "behavior": behavior, "fatigue_score": float(fatigue_score),
#             "fatigue_level": self.fatigue_level(fatigue_score),
#             "meeting": "On" if meeting_active else "Off",
#             "status": "Monitoring" if self.monitoring else "Not Monitoring",
#             "trend_value": self.global_screen_seconds
#         }

#     def show_dashboard(self): self.pages.setCurrentWidget(self.dashboard_page)
#     def show_smart(self): self.pages.setCurrentWidget(self.smart_page)
#     def show_ai(self): self.pages.setCurrentWidget(self.ai_page)
#     def show_settings(self): self.pages.setCurrentWidget(self.settings_page)
#     def show_weekly(self): self.pages.setCurrentWidget(self.weekly_page)
#     def show_analytics(self): self.analytics_page.refresh_all(); self.pages.setCurrentWidget(self.analytics_page)
#     def show_insights(self): self.insights_page.update_insights(self.ai_history); self.pages.setCurrentWidget(self.insights_page)
#     def show_weekly_report(self): self.weekly_report_page.refresh(); self.pages.setCurrentWidget(self.weekly_report_page)
#     def show_monthly_report(self): self.monthly_report_page.refresh(); self.pages.setCurrentWidget(self.monthly_report_page)

#     # def toggle_monitoring(self):
#     #     self.monitoring = not self.monitoring
#     #     if self.monitoring:
#     #         if self.pages.currentWidget() == self.smart_page:
#     #             self.active_monitoring_mode = "Smart Mode"
#     #             self.hybrid_engine.reset_after_break()
#     #         elif self.pages.currentWidget() == self.ai_page:
#     #             self.active_monitoring_mode = "AI Mode"
#     #             self.ai_engine.session_start = time.time()
#     #             self.ai_engine.real_time = 0
#     #     else: self.active_monitoring_mode = None

#     def toggle_monitoring(self):
#         self.monitoring = not self.monitoring

#         if self.monitoring:
#             # Check which page we are on to decide the mode
#             if self.pages.currentWidget() == self.smart_page:
#                 self.active_monitoring_mode = "Smart Mode"
#                 self.hybrid_engine.reset_after_break()

#             elif self.pages.currentWidget() == self.ai_page:
#                 self.active_monitoring_mode = "AI Mode"
#                 self.ai_engine.session_start = time.time()
#                 self.ai_engine.real_time = 0
                
#             print(f"Monitoring: ON ({self.active_monitoring_mode})")
#         else:
#             # This part is crucial so the engine actually stops when you click 'Stop'
#             self.active_monitoring_mode = None
#             print("Monitoring: OFF")

#     # def apply_theme(self):
#     #     theme_name = self.settings.get("theme")
#     #     path = f"assets/themes/{theme_name}.qss"
#     #     try:
#     #         with open(path, "r") as f: self.setStyleSheet(f.read())
#     #     except Exception as e: print(f"Theme load error: {e}")

#     def apply_theme(self):
#         """ Fixes the theme path so the EXE can find the .qss file """
#         theme_name = self.settings.get("theme")
#         # UPDATED: Wrapping the theme path in resource_path
#         path = resource_path(os.path.join("assets", "themes", f"{theme_name}.qss"))
        
#         try:
#             if os.path.exists(path):
#                 with open(path, "r") as f: 
#                     self.setStyleSheet(f.read())
#             else:
#                 print(f"Theme file not found at: {path}")
#         except Exception as e: 
#             print(f"Theme load error: {e}")

#     def handle_os_sleep(self):
#         now = time.time()
#         print("[SYSTEM] Sleep detected — resetting engines")
#         self.hybrid_engine.session_start = now
#         self.hybrid_engine.last_break_time = now - self.hybrid_engine.config.min_interval
#         self.hybrid_engine.last_behavior = "Idle"; self.hybrid_engine.last_fatigue = 0.0
#         self.ai_engine.session_start = now; self.ai_engine.real_time = 0

#     def handle_os_resume(self): self.handle_os_sleep()

#     def nativeEvent(self, eventType, message):
#         if sys.platform == "win32":
#             try:
#                 msg = ctypes.cast(message, ctypes.POINTER(wintypes.MSG)).contents
#                 if msg.message == WM_POWERBROADCAST:
#                     if msg.wParam == PBT_APMSUSPEND: self.handle_os_sleep()
#                     elif msg.wParam in (PBT_APMRESUMEAUTOMATIC, PBT_APMRESUMESUSPEND): self.handle_os_resume()
#             except Exception: pass
#         return False, 0

#     def show_break_modal(self, engine_output):
#         from ui.dialogs.break_modal import BreakModal
#         was_monitoring = self.monitoring
#         self.monitoring = False
#         modal = BreakModal(engine_output, parent=self)
#         result = modal.exec()
#         self.monitoring = was_monitoring
#         if result == 1:
#             if self.active_monitoring_mode == "Smart Mode": self.hybrid_engine.reset_after_break()
#             elif self.active_monitoring_mode == "AI Mode": self.ai_engine.session_start = time.time(); self.ai_engine.real_time = 0

















# This updated worked perfectly

# import time
# import sys
# import os
# import traceback
# from datetime import datetime
# from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget, 
#                                QApplication, QSystemTrayIcon, QMenu)
# from PySide6.QtCore import QTimer, Qt
# from PySide6.QtGui import QIcon, QAction

# # Internal UI Imports
# from ui.sidebar import Sidebar
# from ui.pages.dashboard import Dashboard
# from ui.pages.smart_mode import SmartModePage
# from ui.pages.ai_mode import AIModePage
# from ui.pages.settings import SettingsPage
# from ui.pages.weekly_analytics import WeeklyAnalyticsPage
# from ui.pages.analytics_suite import AnalyticsSuitePage
# from ui.pages.ai_insights import AIInsightsPage
# from ui.pages.weekly_report import WeeklyReportPage
# from ui.pages.monthly_report import MonthlyReportPage

# # Internal Core Imports
# from core.settings import SettingsManager
# from core.smart_break_engine import SmartBreakEngine, SmartConfig
# from core.smart_break_engine_v2 import SmartBreakEngineV2
# from core.signal_collector import SignalCollector
# from core.reminder import Reminder
# from core.ai_reminder_messages import AIMessageGenerator
# from core.storage_manager import StorageManager
# from core.daily_summary_engine import DailySummaryEngine
# from ui.widgets.mini_video_window import MiniVideoWindow

# def resource_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# if sys.platform == "win32":
#     import ctypes
#     from ctypes import wintypes
#     PBT_APMSUSPEND = 0x0004
#     PBT_APMRESUMEAUTOMATIC = 0x0012
#     PBT_APMRESUMESUSPEND = 0x0007
#     WM_POWERBROADCAST = 0x0218

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.icon_path = resource_path(os.path.join("assets", "icons", "logo.png"))
#         self.setWindowIcon(QIcon(self.icon_path))
#         self.setWindowTitle("K-Mends Digital Wellbeing")
#         self.resize(960, 620)
#         self.setMinimumSize(820, 560)

#         # State tracking
#         self.last_tick = time.time()
#         self.monitoring = False
#         self.active_monitoring_mode = None
        
#         # Core Systems
#         self.settings = SettingsManager()
#         self.signals = SignalCollector()
#         self.hybrid_engine = SmartBreakEngine(SmartConfig())
#         self.ai_engine = SmartBreakEngineV2()
#         self.reminder = Reminder(main_window=self)
#         self.ai_messages = AIMessageGenerator()
#         self.storage = StorageManager()
#         self.ai_history = []
#         self.app_start_time = time.time()
#         self.global_screen_seconds = 0

#         # UI Setup
#         container = QWidget()
#         layout = QHBoxLayout(container)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

#         self.sidebar = Sidebar(self)
#         self.pages = QStackedWidget()
#         layout.addWidget(self.sidebar)
#         layout.addWidget(self.pages, 1)

#         # Initialize Pages
#         self.dashboard_page = Dashboard(self)
#         self.smart_page = SmartModePage(self)
#         self.ai_page = AIModePage(self)
#         self.settings_page = SettingsPage(self)
#         self.weekly_page = WeeklyAnalyticsPage()
#         self.analytics_page = AnalyticsSuitePage()
#         self.insights_page = AIInsightsPage()
#         self.weekly_report_page = WeeklyReportPage()
#         self.monthly_report_page = MonthlyReportPage()

#         for page in [self.dashboard_page, self.smart_page, self.ai_page, 
#                      self.settings_page, self.weekly_page, self.analytics_page, 
#                      self.insights_page, self.weekly_report_page, self.monthly_report_page]:
#             self.pages.addWidget(page)

#         self.setCentralWidget(container)
#         self.apply_theme()
#         self.show_dashboard()
#         self.setup_system_tray()

#         # Timer
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_break_engine)
#         self.timer.start(1000)

#     def update_break_engine(self):
#         now = time.time()
#         last_tick = self.last_tick
#         self.last_tick = now

#         # 1. OS Sleep Guard (Restore Old Sensitivity)
#         if now - last_tick > 120:
#             print("[SYSTEM] Time-jump detected, handling sleep.")
#             self.handle_os_sleep()
#             return

#         # 2. Global Tracking
#         if self.monitoring:
#             self.global_screen_seconds = int(time.time() - self.app_start_time)

#         # 3. Update Dashboard UI
#         data = self.build_dashboard_data()
#         self.dashboard_page.update_dashboard(data)

#         # 4. Engine Guards
#         if not self.monitoring or not self.active_monitoring_mode:
#             return

#         self.signals.update()
#         signals = self.signals.to_dict()
        
#         # --- AI MODE LOGIC (RESTORED FROM OLD VERSION) ---
#         if self.active_monitoring_mode == "AI Mode":
#             if self.ai_engine.session_start is None:
#                 self.ai_engine.session_start = now
            
#             self.ai_engine.real_time = now - self.ai_engine.session_start
#             decision = self.ai_engine.should_trigger_break(signals)
            
#             # History log
#             self.ai_history.append({
#                 "timestamp": datetime.now(),
#                 "behavior": decision.get("behavior", "Idle"),
#                 "fatigue": decision.get("fatigue_score", 0.0),
#                 "break_triggered": decision.get("trigger", False),
#                 "break_reason": decision.get("reason", ""),
#                 "suppression": False
#             })

#             # Sync UI
#             self.ai_engine.last_behavior = decision.get("behavior", "Idle")
#             self.ai_engine.last_fatigue = decision.get("fatigue_score", 0.0)
            
#             raw_seconds = decision.get("remaining_seconds", 1200)
#             self.ai_page.update_ai_status(
#                 behavior=self.ai_engine.last_behavior,
#                 fatigue=self.ai_engine.last_fatigue,
#                 reason=decision.get("reason", ""),
#                 trigger=decision.get("trigger", False),
#                 next_break_seconds=max(0, round(raw_seconds / 60))
#             )

#             # TRIGGER CHECK
#             if decision.get("trigger", False):
#                 engine_output = {
#                     "behavior": decision.get("behavior", "Activity"),
#                     "reason": decision.get("reason", ""),
#                     "message": decision.get("message", "Suggesting a short reset."),
#                     "interval_used": decision.get("interval_used", 1200),
#                     "last_break_time": now,
#                     "trigger": True,
#                 }
#                 self.reminder.send_break_message(engine_output)
#                 return  # EXIT EARLY (FIXED)

#         # --- SMART MODE LOGIC ---
#         elif self.active_monitoring_mode == "Smart Mode":
#             decision = self.hybrid_engine.should_trigger_break(signals)
#             trigger = decision.get("trigger", False)
            
#             raw_seconds = decision.get("next_break_seconds", 1200)
#             self.smart_page.update_smart_status(
#                 behavior=decision.get("behavior", "Activity"),
#                 fatigue=decision.get("fatigue_score", 0.0),
#                 reason=decision.get("reason", ""),
#                 trigger=trigger,
#                 next_break_seconds=max(0, round(raw_seconds / 60))
#             )

#             if trigger:
#                 engine_output = {
#                     "behavior": decision.get("behavior", "Activity"),
#                     "reason": decision.get("reason", ""),
#                     "message": decision.get("message", "Smart Mode recommends a break."),
#                     "interval_used": decision.get("interval_used", 1200),
#                     "last_break_time": now,
#                     "trigger": True,
#                 }
#                 self.reminder.send_break_message(engine_output)
#                 return # EXIT EARLY (FIXED)
#     def build_dashboard_data(self):
#         signals = self.signals.to_dict()
#         mode = self.active_monitoring_mode or "No Active Mode"
#         meeting_active = (signals.get("window_category") == "meeting" or signals.get("webcam_active") is True)
#         screen_time = time.strftime("%H:%M:%S", time.gmtime(self.global_screen_seconds))
        
#         behavior = str(getattr(self.ai_engine, "last_behavior", "—")).replace("_", " ").title()
#         fatigue_score = getattr(self.ai_engine, "last_fatigue", 0.0)
        
#         return {
#             "screen_time": screen_time, "screen_seconds": self.global_screen_seconds,
#             "breaks": str(getattr(self.reminder, "break_count", 0)), "mode": mode,
#             "behavior": behavior, "fatigue_score": float(fatigue_score),
#             "fatigue_level": self.fatigue_level(fatigue_score),
#             "meeting": "On" if meeting_active else "Off",
#             "status": "Monitoring" if self.monitoring else "Not Monitoring",
#             "trend_value": self.global_screen_seconds
#         }

#     def fatigue_level(self, score):
#         if score < 25: return "Low"
#         elif score < 50: return "Medium"
#         elif score < 75: return "High"
#         else: return "Critical"

#     def toggle_monitoring(self):
#         self.monitoring = not self.monitoring
#         if self.monitoring:
#             if self.pages.currentWidget() == self.smart_page:
#                 self.active_monitoring_mode = "Smart Mode"
#                 self.hybrid_engine.reset_after_break()
#             elif self.pages.currentWidget() == self.ai_page:
#                 self.active_monitoring_mode = "AI Mode"
#                 self.ai_engine.session_start = time.time()
#                 self.ai_engine.real_time = 0
            
#             # Sync the button text on the page
#             if hasattr(self.ai_page, 'start_button'):
#                 self.ai_page.start_button.setText("Stop K-Mends AI")
#         else:
#             self.active_monitoring_mode = None
#             if hasattr(self.ai_page, 'start_button'):
#                 self.ai_page.start_button.setText("Start K-Mends AI")
        
#         print(f"Monitoring: {self.monitoring} Mode: {self.active_monitoring_mode}")

#     def setup_system_tray(self):
#         self.tray_icon = QSystemTrayIcon(self)
#         self.tray_icon.setIcon(QIcon(self.icon_path))
#         tray_menu = QMenu()
#         show_action = QAction("Open Dashboard", self)
#         show_action.triggered.connect(self.show_and_activate)
#         quit_action = QAction("Exit", self)
#         quit_action.triggered.connect(QApplication.instance().quit)
#         tray_menu.addAction(show_action)
#         tray_menu.addAction(quit_action)
#         self.tray_icon.setContextMenu(tray_menu)
#         self.tray_icon.show()

#     def show_and_activate(self):
#         self.showNormal()
#         self.activateWindow()
#         self.raise_()

#     def apply_theme(self):
#         theme_name = self.settings.get("theme")
#         path = resource_path(os.path.join("assets", "themes", f"{theme_name}.qss"))
#         try:
#             with open(path, "r") as f: self.setStyleSheet(f.read())
#         except: pass

#     def handle_os_sleep(self):
#         now = time.time()
#         self.ai_engine.session_start = now
#         self.ai_engine.real_time = 0
#         if hasattr(self.ai_engine, "last_break_time"):
#             self.ai_engine.last_break_time = now - 1200 # Fixed to prevent jump

#     def show_dashboard(self): self.pages.setCurrentWidget(self.dashboard_page)
#     def show_ai(self): self.pages.setCurrentWidget(self.ai_page)
#     def show_smart(self): self.pages.setCurrentWidget(self.smart_page)
#     def show_settings(self): self.pages.setCurrentWidget(self.settings_page)
#     def show_weekly(self): self.pages.setCurrentWidget(self.weekly_page)
#     def show_analytics(self): self.analytics_page.refresh_all(); self.pages.setCurrentWidget(self.analytics_page)
#     def show_insights(self): self.insights_page.update_insights(self.ai_history); self.pages.setCurrentWidget(self.insights_page)
#     def show_weekly_report(self): self.weekly_report_page.refresh(); self.pages.setCurrentWidget(self.weekly_report_page)
#     def show_monthly_report(self): self.monthly_report_page.refresh(); self.pages.setCurrentWidget(self.monthly_report_page)

#     def closeEvent(self, event):
#         if self.tray_icon.isVisible():
#             self.hide()
#             event.ignore()
#         else:
#             DailySummaryEngine().generate_today()
#             event.accept()











# 27th

# I added a sync so whe you start it will show start in the AI too

# import time
# import sys
# import os
# import traceback
# from datetime import datetime
# from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget, 
#                                QApplication, QSystemTrayIcon, QMenu)
# from PySide6.QtCore import QTimer, Qt
# from PySide6.QtGui import QIcon, QAction

# # Internal UI Imports
# from ui.sidebar import Sidebar
# from ui.pages.dashboard import Dashboard
# from ui.pages.smart_mode import SmartModePage
# from ui.pages.ai_mode import AIModePage
# from ui.pages.settings import SettingsPage
# from ui.pages.weekly_analytics import WeeklyAnalyticsPage
# from ui.pages.analytics_suite import AnalyticsSuitePage
# from ui.pages.ai_insights import AIInsightsPage
# from ui.pages.weekly_report import WeeklyReportPage
# from ui.pages.monthly_report import MonthlyReportPage

# # Internal Core Imports
# from core.settings import SettingsManager
# from core.smart_break_engine import SmartBreakEngine, SmartConfig
# from core.smart_break_engine_v2 import SmartBreakEngineV2
# from core.signal_collector import SignalCollector
# from core.reminder import Reminder
# from core.ai_reminder_messages import AIMessageGenerator
# from core.storage_manager import StorageManager
# from core.daily_summary_engine import DailySummaryEngine
# from ui.widgets.mini_video_window import MiniVideoWindow

# # --- PACKAGING HELPER (Kept for PyInstaller) ---
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# # --- WINDOWS POWER EVENTS ---
# if sys.platform == "win32":
#     import ctypes
#     from ctypes import wintypes
#     PBT_APMSUSPEND = 0x0004
#     PBT_APMRESUMEAUTOMATIC = 0x0012
#     PBT_APMRESUMESUSPEND = 0x0007
#     WM_POWERBROADCAST = 0x0218

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
        
#         # Paths & Icons
#         self.icon_path = resource_path(os.path.join("assets", "icons", "logo.png"))
#         self.setWindowIcon(QIcon(self.icon_path))
#         self.setWindowTitle("K-Mends Digital Wellbeing")
#         self.resize(960, 620)
#         self.setMinimumSize(820, 560)

#         # State tracking
#         self.last_tick = time.time()
#         self.monitoring = False
#         self.active_monitoring_mode = None
        
#         # Core Systems
#         self.settings = SettingsManager()
#         self.signals = SignalCollector()
#         self.hybrid_engine = SmartBreakEngine(SmartConfig())
#         self.ai_engine = SmartBreakEngineV2()
#         self.reminder = Reminder(main_window=self)
#         self.ai_messages = AIMessageGenerator()
#         self.storage = StorageManager()
#         self.ai_history = []
#         self.app_start_time = time.time()
#         self.global_screen_seconds = 0

#         # UI Layout
#         container = QWidget()
#         layout = QHBoxLayout(container)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

#         self.sidebar = Sidebar(self)
#         self.pages = QStackedWidget()
#         layout.addWidget(self.sidebar)
#         layout.addWidget(self.pages, 1)

#         # Initialize Pages
#         self.dashboard_page = Dashboard(self)
#         self.smart_page = SmartModePage(self)
#         self.ai_page = AIModePage(self)
#         self.settings_page = SettingsPage(self)
#         self.weekly_page = WeeklyAnalyticsPage()
#         self.analytics_page = AnalyticsSuitePage()
#         self.insights_page = AIInsightsPage()
#         self.weekly_report_page = WeeklyReportPage()
#         self.monthly_report_page = MonthlyReportPage()

#         for page in [self.dashboard_page, self.smart_page, self.ai_page, 
#                      self.settings_page, self.weekly_page, self.analytics_page, 
#                      self.insights_page, self.weekly_report_page, self.monthly_report_page]:
#             self.pages.addWidget(page)

#         self.setCentralWidget(container)
#         self.apply_theme()
#         self.show_dashboard()
#         self.setup_system_tray()

#         # Timer setup
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_break_engine)
#         self.timer.start(1000)

#     def update_break_engine(self):
#         now = time.time()
#         last_tick = self.last_tick
#         self.last_tick = now

#         # 1. Sleep Guard (Restored from your working version)
#         if now - last_tick > 120:
#             self.handle_os_sleep()
#             return

#         if self.monitoring:
#             self.global_screen_seconds = int(time.time() - self.app_start_time)

#         # 2. Update Dashboard UI
#         data = self.build_dashboard_data()
#         self.dashboard_page.update_dashboard(data)

#         # 3. Guard: If not monitoring, stop logic here
#         if not self.monitoring or not self.active_monitoring_mode:
#             return

#         self.signals.update()
#         signals = self.signals.to_dict()
        
#         # --- AI MODE LOGIC (Fixed for Notifications) ---
#         if self.active_monitoring_mode == "AI Mode":
#             if self.ai_engine.session_start is None:
#                 self.ai_engine.session_start = now
            
#             self.ai_engine.real_time = now - self.ai_engine.session_start
#             decision = self.ai_engine.should_trigger_break(signals)
            
#             # Update history
#             self.ai_history.append({
#                 "timestamp": datetime.now(),
#                 "behavior": decision.get("behavior", "Idle"),
#                 "fatigue": decision.get("fatigue_score", 0.0),
#                 "break_triggered": decision.get("trigger", False),
#                 "break_reason": decision.get("reason", ""),
#                 "suppression": False
#             })

#             # Sync Engine state to UI
#             self.ai_engine.last_behavior = decision.get("behavior", "Idle")
#             self.ai_engine.last_fatigue = decision.get("fatigue_score", 0.0)
            
#             # Convert seconds to minutes for display
#             raw_seconds = decision.get("remaining_seconds", decision.get("interval_used", 1200))
#             self.ai_page.update_ai_status(
#                 behavior=self.ai_engine.last_behavior,
#                 fatigue=self.ai_engine.last_fatigue,
#                 reason=decision.get("reason", ""),
#                 trigger=decision.get("trigger", False),
#                 next_break_seconds=max(0, round(raw_seconds / 60))
#             )

#             # CRITICAL: Trigger check and Early Return (The "Old Way" that worked)
#             if decision.get("trigger", False):
#                 engine_output = {
#                     "behavior": decision.get("behavior", "Activity"),
#                     "reason": decision.get("reason", ""),
#                     "message": decision.get("message", "Suggesting a short reset."),
#                     "interval_used": decision.get("interval_used", 1200),
#                     "last_break_time": now,
#                     "trigger": True,
#                 }
#                 self.reminder.send_break_message(engine_output)
#                 return 

#         # --- SMART MODE LOGIC ---
#         elif self.active_monitoring_mode == "Smart Mode":
#             decision = self.hybrid_engine.should_trigger_break(signals)
#             trigger = decision.get("trigger", False)
            
#             raw_seconds = decision.get("next_break_seconds", 1200)
#             self.smart_page.update_smart_status(
#                 behavior=decision.get("behavior", "Activity"),
#                 fatigue=decision.get("fatigue_score", 0.0),
#                 reason=decision.get("reason", ""),
#                 trigger=trigger,
#                 next_break_seconds=max(0, round(raw_seconds / 60))
#             )

#             if trigger:
#                 engine_output = {
#                     "behavior": decision.get("behavior", "Activity"),
#                     "reason": decision.get("reason", ""),
#                     "message": decision.get("message", "Smart Mode recommends a break."),
#                     "interval_used": decision.get("interval_used", 1200),
#                     "last_break_time": now,
#                     "trigger": True,
#                 }
#                 self.reminder.send_break_message(engine_output)
#                 return

#     def toggle_monitoring(self):
#         """ Handles the Start/Stop logic and syncs button text """
#         self.monitoring = not self.monitoring
        
#         if self.monitoring:
#             if self.pages.currentWidget() == self.smart_page:
#                 self.active_monitoring_mode = "Smart Mode"
#                 self.hybrid_engine.reset_after_break()
#             elif self.pages.currentWidget() == self.ai_page:
#                 self.active_monitoring_mode = "AI Mode"
#                 self.ai_engine.session_start = time.time()
#                 self.ai_engine.real_time = 0
            
#             # Sync Button Text to STOP
#             if hasattr(self.ai_page, 'start_button'):
#                 self.ai_page.start_button.setText("Stop K-Mends AI")
#                 self.ai_page.start_button.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; border-radius: 8px;")
#         else:
#             self.active_monitoring_mode = None
#             # Sync Button Text to START
#             if hasattr(self.ai_page, 'start_button'):
#                 self.ai_page.start_button.setText("Start K-Mends AI")
#                 self.ai_page.start_button.setStyleSheet("") # Revert to theme default
        
#         print(f"Monitoring Toggled: {self.monitoring}")

#     def build_dashboard_data(self):
#         signals = self.signals.to_dict()
#         mode = self.active_monitoring_mode or "No Active Mode"
#         meeting_active = (signals.get("window_category") == "meeting" or signals.get("webcam_active") is True)
#         screen_time = time.strftime("%H:%M:%S", time.gmtime(self.global_screen_seconds))
        
#         behavior = str(getattr(self.ai_engine, "last_behavior", "—")).replace("_", " ").title()
#         fatigue_score = getattr(self.ai_engine, "last_fatigue", 0.0)
        
#         return {
#             "screen_time": screen_time, "screen_seconds": self.global_screen_seconds,
#             "breaks": str(getattr(self.reminder, "break_count", 0)), "mode": mode,
#             "behavior": behavior, "fatigue_score": float(fatigue_score),
#             "fatigue_level": self.fatigue_level(fatigue_score),
#             "meeting": "On" if meeting_active else "Off",
#             "status": "Monitoring" if self.monitoring else "Not Monitoring",
#             "trend_value": self.global_screen_seconds
#         }

#     def fatigue_level(self, score):
#         try:
#             s = float(score)
#             if s < 25: return "Low"
#             elif s < 50: return "Medium"
#             elif s < 75: return "High"
#             else: return "Critical"
#         except: return "Low"

#     def setup_system_tray(self):
#         self.tray_icon = QSystemTrayIcon(self)
#         self.tray_icon.setIcon(QIcon(self.icon_path))
#         tray_menu = QMenu()
#         show_action = QAction("Open Dashboard", self)
#         show_action.triggered.connect(self.show_and_activate)
#         quit_action = QAction("Exit", self)
#         quit_action.triggered.connect(QApplication.instance().quit)
#         tray_menu.addAction(show_action)
#         tray_menu.addSeparator()
#         tray_menu.addAction(quit_action)
#         self.tray_icon.setContextMenu(tray_menu)
#         self.tray_icon.show()

#     def show_and_activate(self):
#         self.showNormal()
#         self.activateWindow()
#         self.raise_()

#     def apply_theme(self):
#         theme_name = self.settings.get("theme")
#         path = resource_path(os.path.join("assets", "themes", f"{theme_name}.qss"))
#         try:
#             if os.path.exists(path):
#                 with open(path, "r") as f: self.setStyleSheet(f.read())
#         except: pass

#     def handle_os_sleep(self):
#         now = time.time()
#         self.ai_engine.session_start = now
#         self.ai_engine.real_time = 0
#         # Prevent the "19m to 20m" jump by forcing last break time back
#         if hasattr(self.ai_engine, "last_break_time"):
#             self.ai_engine.last_break_time = now - 1200 

#     # Page Navigation
#     def show_dashboard(self): self.pages.setCurrentWidget(self.dashboard_page)
#     def show_ai(self): self.pages.setCurrentWidget(self.ai_page)
#     def show_smart(self): self.pages.setCurrentWidget(self.smart_page)
#     def show_settings(self): self.pages.setCurrentWidget(self.settings_page)
#     def show_weekly(self): self.pages.setCurrentWidget(self.weekly_page)
#     def show_analytics(self): self.analytics_page.refresh_all(); self.pages.setCurrentWidget(self.analytics_page)
#     def show_insights(self): self.insights_page.update_insights(self.ai_history); self.pages.setCurrentWidget(self.insights_page)
#     def show_weekly_report(self): self.weekly_report_page.refresh(); self.pages.setCurrentWidget(self.weekly_report_page)
#     def show_monthly_report(self): self.monthly_report_page.refresh(); self.pages.setCurrentWidget(self.monthly_report_page)

#     def closeEvent(self, event):
#         if self.tray_icon.isVisible():
#             self.hide()
#             event.ignore()
#         else:
#             DailySummaryEngine().generate_today()
#             event.accept()

















# import time
# import sys
# import os
# import traceback
# from datetime import datetime
# from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget, 
#                                QApplication, QSystemTrayIcon, QMenu)
# from PySide6.QtCore import QTimer, Qt
# from PySide6.QtGui import QIcon, QAction

# # Internal UI Imports
# from ui.sidebar import Sidebar
# from ui.pages.dashboard import Dashboard
# from ui.pages.smart_mode import SmartModePage
# from ui.pages.ai_mode import AIModePage
# from ui.pages.settings import SettingsPage
# from ui.pages.weekly_analytics import WeeklyAnalyticsPage
# from ui.pages.analytics_suite import AnalyticsSuitePage
# from ui.pages.ai_insights import AIInsightsPage
# from ui.pages.weekly_report import WeeklyReportPage
# from ui.pages.monthly_report import MonthlyReportPage

# # Internal Core Imports
# from core.settings import SettingsManager
# from core.smart_break_engine import SmartBreakEngine, SmartConfig
# from core.smart_break_engine_v2 import SmartBreakEngineV2
# from core.signal_collector import SignalCollector
# from core.reminder import Reminder
# from core.ai_reminder_messages import AIMessageGenerator
# from core.storage_manager import StorageManager
# from core.daily_summary_engine import DailySummaryEngine
# from ui.widgets.mini_video_window import MiniVideoWindow

# # --- PACKAGING HELPER (Kept for PyInstaller) ---
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# # --- WINDOWS POWER EVENTS ---
# if sys.platform == "win32":
#     import ctypes
#     from ctypes import wintypes
#     PBT_APMSUSPEND = 0x0004
#     PBT_APMRESUMEAUTOMATIC = 0x0012
#     PBT_APMRESUMESUSPEND = 0x0007
#     WM_POWERBROADCAST = 0x0218

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
        
#         # Paths & Icons
#         self.icon_path = resource_path(os.path.join("assets", "icons", "logo.png"))
#         self.setWindowIcon(QIcon(self.icon_path))
#         self.setWindowTitle("K-Mends Digital Wellbeing")
#         self.resize(960, 620)
#         self.setMinimumSize(820, 560)

#         # State tracking
#         self.last_tick = time.time()
#         self.monitoring = False
#         self.active_monitoring_mode = None
        
#         # Core Systems
#         self.settings = SettingsManager()
#         self.signals = SignalCollector()
#         self.hybrid_engine = SmartBreakEngine(SmartConfig())
#         self.ai_engine = SmartBreakEngineV2()
        
#         # FIX: Ensure Reminder is initialized with the 5s safety interval
#         self.reminder = Reminder(main_window=self, min_interval_seconds=5)
        
#         self.ai_messages = AIMessageGenerator()
#         self.storage = StorageManager()
#         self.ai_history = []
#         self.app_start_time = time.time()
#         self.global_screen_seconds = 0

#         # UI Layout
#         container = QWidget()
#         layout = QHBoxLayout(container)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

#         self.sidebar = Sidebar(self)
#         self.pages = QStackedWidget()
#         layout.addWidget(self.sidebar)
#         layout.addWidget(self.pages, 1)

#         # Initialize Pages
#         self.dashboard_page = Dashboard(self)
#         self.smart_page = SmartModePage(self)
#         self.ai_page = AIModePage(self)
#         self.settings_page = SettingsPage(self)
#         self.weekly_page = WeeklyAnalyticsPage()
#         self.analytics_page = AnalyticsSuitePage()
#         self.insights_page = AIInsightsPage()
#         self.weekly_report_page = WeeklyReportPage()
#         self.monthly_report_page = MonthlyReportPage()

#         for page in [self.dashboard_page, self.smart_page, self.ai_page, 
#                      self.settings_page, self.weekly_page, self.analytics_page, 
#                      self.insights_page, self.weekly_report_page, self.monthly_report_page]:
#             self.pages.addWidget(page)

#         self.setCentralWidget(container)
#         self.apply_theme()
#         self.show_dashboard()
#         self.setup_system_tray()

#         # Timer setup
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_break_engine)
#         self.timer.start(1000)

#     def update_break_engine(self):
#         now = time.time()
#         last_tick = self.last_tick
#         self.last_tick = now

#         # 1. Sleep Guard
#         if now - last_tick > 120:
#             self.handle_os_sleep()
#             return

#         if self.monitoring:
#             self.global_screen_seconds = int(time.time() - self.app_start_time)

#         # 2. Update Dashboard UI (Uses self.reminder.break_count)
#         data = self.build_dashboard_data()
#         self.dashboard_page.update_dashboard(data)

#         # 3. Guard: If not monitoring, stop logic here
#         if not self.monitoring or not self.active_monitoring_mode:
#             return

#         self.signals.update()
#         signals = self.signals.to_dict()
        
#         # --- AI MODE LOGIC ---
#         if self.active_monitoring_mode == "AI Mode":
#             if self.ai_engine.session_start is None:
#                 self.ai_engine.session_start = now
            
#             self.ai_engine.real_time = now - self.ai_engine.session_start
#             decision = self.ai_engine.should_trigger_break(signals)
            
#             # Update history
#             self.ai_history.append({
#                 "timestamp": datetime.now(),
#                 "behavior": decision.get("behavior", "Idle"),
#                 "fatigue": decision.get("fatigue_score", 0.0),
#                 "break_triggered": decision.get("trigger", False),
#                 "break_reason": decision.get("reason", ""),
#                 "suppression": False
#             })

#             # Sync Engine state to UI
#             self.ai_engine.last_behavior = decision.get("behavior", "Idle")
#             self.ai_engine.last_fatigue = decision.get("fatigue_score", 0.0)
            
#             raw_seconds = decision.get("remaining_seconds", decision.get("interval_used", 1200))
#             self.ai_page.update_ai_status(
#                 behavior=self.ai_engine.last_behavior,
#                 fatigue=self.ai_engine.last_fatigue,
#                 reason=decision.get("reason", ""),
#                 trigger=decision.get("trigger", False),
#                 next_break_seconds=max(0, round(raw_seconds / 60))
#             )

#             # CRITICAL: Trigger check
#             if decision.get("trigger", False):
#                 # Pass the decision directly to the reminder
#                 self.reminder.send_break_message(decision)
#                 return 

#         # --- SMART MODE LOGIC ---
#         elif self.active_monitoring_mode == "Smart Mode":
#             decision = self.hybrid_engine.should_trigger_break(signals)
#             trigger = decision.get("trigger", False)
            
#             raw_seconds = decision.get("next_break_seconds", 1200)
#             self.smart_page.update_smart_status(
#                 behavior=decision.get("behavior", "Activity"),
#                 fatigue=decision.get("fatigue_score", 0.0),
#                 reason=decision.get("reason", ""),
#                 trigger=trigger,
#                 next_break_minutes=max(0, round(raw_seconds / 60))
#             )

#             if trigger:
#                 self.reminder.send_break_message(decision)
#                 return

#     def toggle_monitoring(self):
#         """ Handles the Start/Stop logic and syncs button text """
#         self.monitoring = not self.monitoring
        
#         if self.monitoring:
#             if self.pages.currentWidget() == self.smart_page:
#                 self.active_monitoring_mode = "Smart Mode"
#                 self.hybrid_engine.reset_after_break()
#             elif self.pages.currentWidget() == self.ai_page:
#                 self.active_monitoring_mode = "AI Mode"
#                 self.ai_engine.session_start = time.time()
#                 self.ai_engine.real_time = 0
            
#             # Sync Button Text to STOP
#             if hasattr(self.ai_page, 'start_button'):
#                 self.ai_page.start_button.setText("Stop K-Mends AI")
#                 self.ai_page.start_button.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; border-radius: 8px;")
#         else:
#             self.active_monitoring_mode = None
#             # Sync Button Text to START
#             if hasattr(self.ai_page, 'start_button'):
#                 self.ai_page.start_button.setText("Start K-Mends AI")
#                 self.ai_page.start_button.setStyleSheet("") # Revert to theme default
        
#         print(f"Monitoring Toggled: {self.monitoring}")

#     def build_dashboard_data(self):
#         signals = self.signals.to_dict()
#         mode = self.active_monitoring_mode or "No Active Mode"
#         meeting_active = (signals.get("window_category") == "meeting" or signals.get("webcam_active") is True)
#         screen_time = time.strftime("%H:%M:%S", time.gmtime(self.global_screen_seconds))
        
#         behavior = str(getattr(self.ai_engine, "last_behavior", "—")).replace("_", " ").title()
#         fatigue_score = getattr(self.ai_engine, "last_fatigue", 0.0)
        
#         return {
#             "screen_time": screen_time, "screen_seconds": self.global_screen_seconds,
#             "breaks": str(getattr(self.reminder, "break_count", 0)), "mode": mode,
#             "behavior": behavior, "fatigue_score": float(fatigue_score),
#             "fatigue_level": self.fatigue_level(fatigue_score),
#             "meeting": "On" if meeting_active else "Off",
#             "status": "Monitoring" if self.monitoring else "Not Monitoring",
#             "trend_value": self.global_screen_seconds
#         }

#     def fatigue_level(self, score):
#         try:
#             s = float(score)
#             if s < 25: return "Low"
#             elif s < 50: return "Medium"
#             elif s < 75: return "High"
#             else: return "Critical"
#         except: return "Low"

#     def setup_system_tray(self):
#         self.tray_icon = QSystemTrayIcon(self)
#         self.tray_icon.setIcon(QIcon(self.icon_path))
#         tray_menu = QMenu()
#         show_action = QAction("Open Dashboard", self)
#         show_action.triggered.connect(self.show_and_activate)
#         quit_action = QAction("Exit", self)
#         quit_action.triggered.connect(QApplication.instance().quit)
#         tray_menu.addAction(show_action)
#         tray_menu.addSeparator()
#         tray_menu.addAction(quit_action)
#         self.tray_icon.setContextMenu(tray_menu)
#         self.tray_icon.show()

#     def show_and_activate(self):
#         self.showNormal()
#         self.activateWindow()
#         self.raise_()

#     def apply_theme(self):
#         theme_name = self.settings.get("theme")
#         path = resource_path(os.path.join("assets", "themes", f"{theme_name}.qss"))
#         try:
#             if os.path.exists(path):
#                 with open(path, "r") as f: self.setStyleSheet(f.read())
#         except: pass

#     def handle_os_sleep(self):
#         now = time.time()
#         self.ai_engine.session_start = now
#         self.ai_engine.real_time = 0
#         if hasattr(self.ai_engine, "last_break_time"):
#             self.ai_engine.last_break_time = now - 1200 

#     # Page Navigation
#     def show_dashboard(self): self.pages.setCurrentWidget(self.dashboard_page)
#     def show_ai(self): self.pages.setCurrentWidget(self.ai_page)
#     def show_smart(self): self.pages.setCurrentWidget(self.smart_page)
#     def show_settings(self): self.pages.setCurrentWidget(self.settings_page)
#     def show_weekly(self): self.pages.setCurrentWidget(self.weekly_page)
#     def show_analytics(self): self.analytics_page.refresh_all(); self.pages.setCurrentWidget(self.analytics_page)
#     def show_insights(self): self.insights_page.update_insights(self.ai_history); self.pages.setCurrentWidget(self.insights_page)
#     def show_weekly_report(self): self.weekly_report_page.refresh(); self.pages.setCurrentWidget(self.weekly_report_page)
#     def show_monthly_report(self): self.monthly_report_page.refresh(); self.pages.setCurrentWidget(self.monthly_report_page)

#     def closeEvent(self, event):
#         if self.tray_icon.isVisible():
#             self.hide()
#             event.ignore()
#         else:
#             DailySummaryEngine().generate_today()
#             event.accept()










## Fixed the reminder 29th March

# import time
# import sys
# import os
# import traceback
# from datetime import datetime
# from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget, 
#                                QApplication, QSystemTrayIcon, QMenu)
# from PySide6.QtCore import QTimer, Qt
# from PySide6.QtGui import QIcon, QAction

# # Internal UI Imports
# from ui.sidebar import Sidebar
# from ui.pages.dashboard import Dashboard
# from ui.pages.smart_mode import SmartModePage
# from ui.pages.ai_mode import AIModePage
# from ui.pages.settings import SettingsPage
# from ui.pages.weekly_analytics import WeeklyAnalyticsPage
# from ui.pages.analytics_suite import AnalyticsSuitePage
# from ui.pages.ai_insights import AIInsightsPage
# from ui.pages.weekly_report import WeeklyReportPage
# from ui.pages.monthly_report import MonthlyReportPage

# # Internal Core Imports
# from core.settings import SettingsManager
# from core.smart_break_engine import SmartBreakEngine, SmartConfig
# from core.smart_break_engine_v2 import SmartBreakEngineV2
# from core.signal_collector import SignalCollector
# from core.reminder import Reminder
# from core.ai_reminder_messages import AIMessageGenerator
# from core.storage_manager import StorageManager
# from core.daily_summary_engine import DailySummaryEngine
# from ui.widgets.mini_video_window import MiniVideoWindow

# # --- PACKAGING HELPER (Kept for PyInstaller) ---
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# # --- WINDOWS POWER EVENTS ---
# if sys.platform == "win32":
#     import ctypes
#     from ctypes import wintypes
#     PBT_APMSUSPEND = 0x0004
#     PBT_APMRESUMEAUTOMATIC = 0x0012
#     PBT_APMRESUMESUSPEND = 0x0007
#     WM_POWERBROADCAST = 0x0218

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
        
#         # Paths & Icons
#         self.icon_path = resource_path(os.path.join("assets", "icons", "logo.png"))
#         self.setWindowIcon(QIcon(self.icon_path))
#         self.setWindowTitle("K-Mends Digital Wellbeing")
#         self.resize(960, 620)
#         self.setMinimumSize(820, 560)

#         # State tracking
#         self.last_tick = time.time()
#         self.monitoring = False
#         self.active_monitoring_mode = None
        
#         # Core Systems
#         self.settings = SettingsManager()
#         self.signals = SignalCollector()
#         self.hybrid_engine = SmartBreakEngine(SmartConfig())
#         self.ai_engine = SmartBreakEngineV2()
        
#         # PRODUCTION REMINDER (60s interval)
#         self.reminder = Reminder(main_window=self, min_interval_seconds=60)
        
#         self.ai_messages = AIMessageGenerator()
#         self.storage = StorageManager()
#         self.ai_history = []
#         self.app_start_time = time.time()
#         self.global_screen_seconds = 0

#         # UI Layout
#         container = QWidget()
#         layout = QHBoxLayout(container)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

#         self.sidebar = Sidebar(self)
#         self.pages = QStackedWidget()
#         layout.addWidget(self.sidebar)
#         layout.addWidget(self.pages, 1)

#         # Initialize Pages
#         self.dashboard_page = Dashboard(self)
#         self.smart_page = SmartModePage(self)
#         self.ai_page = AIModePage(self)
#         self.settings_page = SettingsPage(self)
#         self.weekly_page = WeeklyAnalyticsPage()
#         # self.analytics_page = AnalyticsSuitePage()
#         self.analytics_page = AnalyticsSuitePage(theme=self.settings.get("theme"))

#         self.insights_page = AIInsightsPage()
#         self.weekly_report_page = WeeklyReportPage()
#         self.monthly_report_page = MonthlyReportPage()

#         for page in [self.dashboard_page, self.smart_page, self.ai_page, 
#                      self.settings_page, self.weekly_page, self.analytics_page, 
#                      self.insights_page, self.weekly_report_page, self.monthly_report_page]:
#             self.pages.addWidget(page)

#         self.setCentralWidget(container)
#         self.apply_theme()
#         self.show_dashboard()
#         self.setup_system_tray()

#         # Timer setup
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_break_engine)
#         self.timer.start(1000)

#     def update_break_engine(self):
#         now = time.time()
#         last_tick = self.last_tick
#         self.last_tick = now

#         # 1. Sleep Guard
#         if now - last_tick > 120:
#             self.handle_os_sleep()
#             return

#         if self.monitoring:
#             self.global_screen_seconds = int(time.time() - self.app_start_time)

#         # 2. Update Dashboard UI
#         data = self.build_dashboard_data()
#         self.dashboard_page.update_dashboard(data)

#         # 3. Guard: If not monitoring, stop logic here
#         if not self.monitoring or not self.active_monitoring_mode:
#             return

#         self.signals.update()
#         signals = self.signals.to_dict()
        
#         # --- AI MODE LOGIC ---
#         if self.active_monitoring_mode == "AI Mode":
#             if self.ai_engine.session_start is None:
#                 self.ai_engine.session_start = now
            
#             self.ai_engine.real_time = now - self.ai_engine.session_start
#             decision = self.ai_engine.should_trigger_break(signals)
            
#             # Update history
#             self.ai_history.append({
#                 "timestamp": datetime.now(),
#                 "behavior": decision.get("behavior", "Idle"),
#                 "fatigue": decision.get("fatigue_score", 0.0),
#                 "break_triggered": decision.get("trigger", False),
#                 "break_reason": decision.get("reason", ""),
#                 "suppression": False
#             })

#             # Sync Engine state to UI
#             self.ai_engine.last_behavior = decision.get("behavior", "Idle")
#             self.ai_engine.last_fatigue = decision.get("fatigue_score", 0.0)
            
#             raw_seconds = decision.get("remaining_seconds", decision.get("interval_used", 1200))
#             self.ai_page.update_ai_status(
#                 behavior=self.ai_engine.last_behavior,
#                 fatigue=self.ai_engine.last_fatigue,
#                 reason=decision.get("reason", ""),
#                 trigger=decision.get("trigger", False),
#                 next_break_minutes=max(0, round(raw_seconds / 60))
#             )

#             # CRITICAL: Trigger check
#             if decision.get("trigger", False):
#                 self.reminder.send_break_message(decision)
#                 return 

#         # --- SMART MODE LOGIC ---
#         elif self.active_monitoring_mode == "Smart Mode":
#             decision = self.hybrid_engine.should_trigger_break(signals)
#             trigger = decision.get("trigger", False)
            
#             raw_seconds = decision.get("next_break_seconds", 1200)
#             self.smart_page.update_smart_status(
#                 behavior=decision.get("behavior", "Activity"),
#                 fatigue=decision.get("fatigue_score", 0.0),
#                 reason=decision.get("reason", ""),
#                 trigger=trigger,
#                 next_break_minutes=max(0, round(raw_seconds / 60))
#             )

#             if trigger:
#                 self.reminder.send_break_message(decision)
#                 return

#     # def toggle_monitoring(self):
#     #     """ Handles the Start/Stop logic and syncs button text """
#     #     self.monitoring = not self.monitoring
        
#     #     if self.monitoring:
#     #         # RESET REMINDER SAFETY INTERVAL
#     #         self.reminder.reset()

#     #         if self.pages.currentWidget() == self.smart_page:
#     #             self.active_monitoring_mode = "Smart Mode"
#     #             self.hybrid_engine.reset_after_break()
#     #         elif self.pages.currentWidget() == self.ai_page:
#     #             self.active_monitoring_mode = "AI Mode"
#     #             self.ai_engine.session_start = time.time()
#     #             self.ai_engine.real_time = 0
            
#     #         # Sync Button Text to STOP
#     #         if hasattr(self.ai_page, 'start_button'):
#     #             self.ai_page.start_button.setText("Stop K-Mends AI")
#     #             self.ai_page.start_button.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; border-radius: 8px;")
#     #     else:
#     #         self.active_monitoring_mode = None
#     #         # Sync Button Text to START
#     #         if hasattr(self.ai_page, 'start_button'):
#     #             self.ai_page.start_button.setText("Start K-Mends AI")
#     #             self.ai_page.start_button.setStyleSheet("") 
        
#     #     print(f"Monitoring Toggled: {self.monitoring}")

#     def toggle_monitoring(self):
#         """ Handles the Start/Stop logic and syncs button text """
#         self.monitoring = not self.monitoring

#         if self.monitoring:
#             # RESET REMINDER SAFETY INTERVAL
#             self.reminder.reset()

#             if self.pages.currentWidget() == self.smart_page:
#                 self.active_monitoring_mode = "Smart Mode"
#                 self.hybrid_engine.reset_after_break()

#             elif self.pages.currentWidget() == self.ai_page:
#                 self.active_monitoring_mode = "AI Mode"
#                 self.ai_engine.session_start = time.time()
#                 self.ai_engine.real_time = 0

#             # Correct button name
#             self.ai_page.btn_toggle.setText("Stop K-Mends AI")

#         else:
#             self.active_monitoring_mode = None

#             # Correct button name
#             self.ai_page.btn_toggle.setText("Start K-Mends AI")

#         print(f"Monitoring Toggled: {self.monitoring}")


#     def build_dashboard_data(self):
#         signals = self.signals.to_dict()
#         mode = self.active_monitoring_mode or "No Active Mode"
#         meeting_active = (signals.get("window_category") == "meeting" or signals.get("webcam_active") is True)
#         screen_time = time.strftime("%H:%M:%S", time.gmtime(self.global_screen_seconds))
        
#         behavior = str(getattr(self.ai_engine, "last_behavior", "—")).replace("_", " ").title()
#         fatigue_score = getattr(self.ai_engine, "last_fatigue", 0.0)
        
#         return {
#             "screen_time": screen_time, "screen_seconds": self.global_screen_seconds,
#             "breaks": str(getattr(self.reminder, "break_count", 0)), "mode": mode,
#             "behavior": behavior, "fatigue_score": float(fatigue_score),
#             "fatigue_level": self.fatigue_level(fatigue_score),
#             "meeting": "On" if meeting_active else "Off",
#             "status": "Monitoring" if self.monitoring else "Not Monitoring",
#             "trend_value": self.global_screen_seconds
#         }

#     def fatigue_level(self, score):
#         try:
#             s = float(score)
#             if s < 25: return "Low"
#             elif s < 50: return "Medium"
#             elif s < 75: return "High"
#             else: return "Critical"
#         except: return "Low"

#     def setup_system_tray(self):
#         self.tray_icon = QSystemTrayIcon(self)
#         self.tray_icon.setIcon(QIcon(self.icon_path))
#         tray_menu = QMenu()
#         show_action = QAction("Open Dashboard", self)
#         show_action.triggered.connect(self.show_and_activate)
#         quit_action = QAction("Exit", self)
#         quit_action.triggered.connect(QApplication.instance().quit)
#         tray_menu.addAction(show_action)
#         tray_menu.addSeparator()
#         tray_menu.addAction(quit_action)
#         self.tray_icon.setContextMenu(tray_menu)
#         self.tray_icon.show()

#     def show_and_activate(self):
#         self.showNormal()
#         self.activateWindow()
#         self.raise_()

#     def apply_theme(self):
#         theme_name = self.settings.get("theme")
#         path = resource_path(os.path.join("assets", "themes", f"{theme_name}.qss"))
#         try:
#             if os.path.exists(path):
#                 with open(path, "r") as f: self.setStyleSheet(f.read())
#         except: pass

#     def handle_os_sleep(self):
#         now = time.time()
#         self.ai_engine.session_start = now
#         self.ai_engine.real_time = 0
#         if hasattr(self.ai_engine, "last_break_time"):
#             self.ai_engine.last_break_time = now - 1200 

#     # Page Navigation
#     def show_dashboard(self): self.pages.setCurrentWidget(self.dashboard_page)
#     def show_ai(self): self.pages.setCurrentWidget(self.ai_page)
#     def show_smart(self): self.pages.setCurrentWidget(self.smart_page)
#     def show_settings(self): self.pages.setCurrentWidget(self.settings_page)
#     def show_weekly(self): self.pages.setCurrentWidget(self.weekly_page)
#     def show_analytics(self): self.analytics_page.refresh_all(); self.pages.setCurrentWidget(self.analytics_page)
#     def show_insights(self): self.insights_page.update_insights(self.ai_history); self.pages.setCurrentWidget(self.insights_page)
#     def show_weekly_report(self): self.weekly_report_page.refresh(); self.pages.setCurrentWidget(self.weekly_report_page)
#     def show_monthly_report(self): self.monthly_report_page.refresh(); self.pages.setCurrentWidget(self.monthly_report_page)

#     def closeEvent(self, event):
#         if self.tray_icon.isVisible():
#             self.hide()
#             event.ignore()
#         else:
#             DailySummaryEngine().generate_today()
#             event.accept()











# # Final correct for mac

# # Fixed the reminder 29th March
# import time
# import sys
# import os
# import traceback
# from datetime import datetime
# from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget, 
#                                QApplication, QSystemTrayIcon, QMenu)
# from PySide6.QtCore import QTimer, Qt
# from PySide6.QtGui import QIcon, QAction

# # Internal UI Imports
# from ui.sidebar import Sidebar
# from ui.pages.dashboard import Dashboard
# from ui.pages.smart_mode import SmartModePage
# from ui.pages.ai_mode import AIModePage
# from ui.pages.settings import SettingsPage
# from ui.pages.weekly_analytics import WeeklyAnalyticsPage
# from ui.pages.analytics_suite import AnalyticsSuitePage
# from ui.pages.ai_insights import AIInsightsPage
# from ui.pages.weekly_report import WeeklyReportPage
# from ui.pages.monthly_report import MonthlyReportPage

# # Internal Core Imports
# from core.settings import SettingsManager
# from core.smart_break_engine import SmartBreakEngine, SmartConfig
# from core.smart_break_engine_v2 import SmartBreakEngineV2
# from core.signal_collector import SignalCollector
# from core.reminder import Reminder
# from core.ai_reminder_messages import AIMessageGenerator
# from core.storage_manager import StorageManager
# from core.daily_summary_engine import DailySummaryEngine
# from ui.widgets.mini_video_window import MiniVideoWindow

# # --- PACKAGING HELPER (Kept for PyInstaller) ---
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# # --- WINDOWS POWER EVENTS ---
# if sys.platform == "win32":
#     import ctypes
#     from ctypes import wintypes
#     PBT_APMSUSPEND = 0x0004
#     PBT_APMRESUMEAUTOMATIC = 0x0012
#     PBT_APMRESUMESUSPEND = 0x0007
#     WM_POWERBROADCAST = 0x0218

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
        
#         # Paths & Icons
#         self.icon_path = resource_path(os.path.join("assets", "icons", "logo.png"))
#         self.setWindowIcon(QIcon(self.icon_path))
#         self.setWindowTitle("K-Mends Digital Wellbeing")
#         self.resize(960, 620)
#         self.setMinimumSize(820, 560)

#         # State tracking
#         self.last_tick = time.time()
#         self.monitoring = False
#         self.active_monitoring_mode = None
        
#         # Core Systems
#         self.settings = SettingsManager()
#         self.signals = SignalCollector()
#         self.hybrid_engine = SmartBreakEngine(SmartConfig())
#         self.ai_engine = SmartBreakEngineV2()
        
#         # PRODUCTION REMINDER (60s interval)
#         self.reminder = Reminder(main_window=self, min_interval_seconds=60)
        
#         self.ai_messages = AIMessageGenerator()
#         self.storage = StorageManager()
#         self.ai_history = []
#         self.app_start_time = time.time()
#         self.global_screen_seconds = 0

#         # UI Layout
#         container = QWidget()
#         layout = QHBoxLayout(container)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

#         self.sidebar = Sidebar(self)
#         self.pages = QStackedWidget()
#         layout.addWidget(self.sidebar)
#         layout.addWidget(self.pages, 1)

#         # Initialize Pages
#         self.dashboard_page = Dashboard(self)
#         self.smart_page = SmartModePage(self)
#         self.ai_mode_page = AIModePage(self) # Renamed to match main.py
#         self.settings_page = SettingsPage(self)
#         self.weekly_page = WeeklyAnalyticsPage()
#         self.analytics_page = AnalyticsSuitePage(theme=self.settings.get("theme"))

#         self.insights_page = AIInsightsPage()
#         self.weekly_report_page = WeeklyReportPage()
#         self.monthly_report_page = MonthlyReportPage()

#         for page in [self.dashboard_page, self.smart_page, self.ai_mode_page, 
#                      self.settings_page, self.weekly_page, self.analytics_page, 
#                      self.insights_page, self.weekly_report_page, self.monthly_report_page]:
#             self.pages.addWidget(page)

#         self.setCentralWidget(container)
#         self.apply_theme()
#         self.show_dashboard()
#         self.setup_system_tray()

#         # Timer setup
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_break_engine)
#         self.timer.start(1000)

#     def update_break_engine(self):
#         now = time.time()
#         last_tick = self.last_tick
#         self.last_tick = now

#         # 1. Sleep Guard
#         if now - last_tick > 120:
#             self.handle_os_sleep()
#             return

#         if self.monitoring:
#             self.global_screen_seconds = int(time.time() - self.app_start_time)

#         # 2. Update Dashboard UI
#         data = self.build_dashboard_data()
#         self.dashboard_page.update_dashboard(data)

#         # 3. Guard: If not monitoring, stop logic here
#         if not self.monitoring or not self.active_monitoring_mode:
#             return

#         self.signals.update()
#         signals = self.signals.to_dict()
        
#         # --- AI MODE LOGIC ---
#         if self.active_monitoring_mode == "AI Mode":
#             if self.ai_engine.session_start is None:
#                 self.ai_engine.session_start = now
            
#             self.ai_engine.real_time = now - self.ai_engine.session_start
#             decision = self.ai_engine.should_trigger_break(signals)
            
#             # Update history
#             self.ai_history.append({
#                 "timestamp": datetime.now(),
#                 "behavior": decision.get("behavior", "Idle"),
#                 "fatigue": decision.get("fatigue_score", 0.0),
#                 "break_triggered": decision.get("trigger", False),
#                 "break_reason": decision.get("reason", ""),
#                 "suppression": False
#             })

#             # Sync Engine state to UI
#             self.ai_engine.last_behavior = decision.get("behavior", "Idle")
#             self.ai_engine.last_fatigue = decision.get("fatigue_score", 0.0)
            
#             raw_seconds = decision.get("remaining_seconds", decision.get("interval_used", 1200))
#             self.ai_mode_page.update_ai_status(
#                 behavior=self.ai_engine.last_behavior,
#                 fatigue=self.ai_engine.last_fatigue,
#                 reason=decision.get("reason", ""),
#                 trigger=decision.get("trigger", False),
#                 next_break_minutes=max(0, round(raw_seconds / 60))
#             )

#             # CRITICAL: Trigger check
#             if decision.get("trigger", False):
#                 self.reminder.send_break_message(decision)
#                 return 

#         # --- SMART MODE LOGIC ---
#         elif self.active_monitoring_mode == "Smart Mode":
#             decision = self.hybrid_engine.should_trigger_break(signals)
#             trigger = decision.get("trigger", False)
            
#             raw_seconds = decision.get("next_break_seconds", 1200)
#             self.smart_page.update_smart_status(
#                 behavior=decision.get("behavior", "Activity"),
#                 fatigue=decision.get("fatigue_score", 0.0),
#                 reason=decision.get("reason", ""),
#                 trigger=trigger,
#                 next_break_minutes=max(0, round(raw_seconds / 60))
#             )

#             if trigger:
#                 self.reminder.send_break_message(decision)
#                 return

#     def toggle_monitoring(self):
#         """ Handles the Start/Stop logic and syncs button text """
#         self.monitoring = not self.monitoring

#         if self.monitoring:
#             # RESET REMINDER SAFETY INTERVAL
#             self.reminder.reset()

#             if self.pages.currentWidget() == self.smart_page:
#                 self.active_monitoring_mode = "Smart Mode"
#                 self.hybrid_engine.reset_after_break()

#             elif self.pages.currentWidget() == self.ai_mode_page:
#                 self.active_monitoring_mode = "AI Mode"
#                 self.ai_engine.session_start = time.time()
#                 self.ai_engine.real_time = 0

#             # Correct button name
#             self.ai_mode_page.btn_toggle.setText("Stop K-Mends AI")

#         else:
#             self.active_monitoring_mode = None

#             # Correct button name
#             self.ai_mode_page.btn_toggle.setText("Start K-Mends AI")

#         print(f"Monitoring Toggled: {self.monitoring}")


#     def build_dashboard_data(self):
#         signals = self.signals.to_dict()
#         mode = self.active_monitoring_mode or "No Active Mode"
#         meeting_active = (signals.get("window_category") == "meeting" or signals.get("webcam_active") is True)
#         screen_time = time.strftime("%H:%M:%S", time.gmtime(self.global_screen_seconds))
        
#         behavior = str(getattr(self.ai_engine, "last_behavior", "—")).replace("_", " ").title()
#         #fatigue_score = getattr(self.ai_engine, "last_fatigue", 0.0)
#         fatigue_score = round(float(getattr(self.ai_engine, "last_fatigue", 0.0)), 1)

#         return {
#             "screen_time": screen_time, "screen_seconds": self.global_screen_seconds,
#             "breaks": str(getattr(self.reminder, "break_count", 0)), "mode": mode,
#             "behavior": behavior, "fatigue_score": float(fatigue_score),
#             "fatigue_level": self.fatigue_level(fatigue_score),
#             "meeting": "On" if meeting_active else "Off",
#             "status": "Monitoring" if self.monitoring else "Not Monitoring",
#             "trend_value": self.global_screen_seconds
#         }

#     def fatigue_level(self, score):
#         try:
#             s = float(score)
#             if s < 25: return "Low"
#             elif s < 50: return "Medium"
#             elif s < 75: return "High"
#             else: return "Critical"
#         except: return "Low"

#     def setup_system_tray(self):
#         self.tray_icon = QSystemTrayIcon(self)
#         self.tray_icon.setIcon(QIcon(self.icon_path))
#         tray_menu = QMenu()
#         show_action = QAction("Open Dashboard", self)
#         show_action.triggered.connect(self.show_and_activate)
#         quit_action = QAction("Exit", self)
#         quit_action.triggered.connect(QApplication.instance().quit)
#         tray_menu.addAction(show_action)
#         tray_menu.addSeparator()
#         tray_menu.addAction(quit_action)
#         self.tray_icon.setContextMenu(tray_menu)
#         self.tray_icon.show()

#     def show_and_activate(self):
#         self.showNormal()
#         self.activateWindow()
#         self.raise_()

#     def apply_theme(self):
#         theme_name = self.settings.get("theme")
#         path = resource_path(os.path.join("assets", "themes", f"{theme_name}.qss"))
#         try:
#             if os.path.exists(path):
#                 with open(path, "r") as f: self.setStyleSheet(f.read())
#         except: pass

#     def handle_os_sleep(self):
#         now = time.time()
#         self.ai_engine.session_start = now
#         self.ai_engine.real_time = 0
#         if hasattr(self.ai_engine, "last_break_time"):
#             self.ai_engine.last_break_time = now - 1200 

#     # Page Navigation
#     def show_dashboard(self): self.pages.setCurrentWidget(self.dashboard_page)
#     def show_ai(self): self.pages.setCurrentWidget(self.ai_mode_page)
#     def show_smart(self): self.pages.setCurrentWidget(self.smart_page)
#     def show_settings(self): self.pages.setCurrentWidget(self.settings_page)
#     def show_weekly(self): self.pages.setCurrentWidget(self.weekly_page)
#     def show_analytics(self): self.analytics_page.refresh_all(); self.pages.setCurrentWidget(self.analytics_page)
#     def show_insights(self): self.insights_page.update_insights(self.ai_history); self.pages.setCurrentWidget(self.insights_page)
#     def show_weekly_report(self): self.weekly_report_page.refresh(); self.pages.setCurrentWidget(self.weekly_report_page)
#     def show_monthly_report(self): self.monthly_report_page.refresh(); self.pages.setCurrentWidget(self.monthly_report_page)

#     def closeEvent(self, event):
#         if self.tray_icon.isVisible():
#             self.hide()
#             event.ignore()
#         else:
#             DailySummaryEngine().generate_today()
#             event.accept()









# Best for 54

# # Final correct for mac
# # Fixed the reminder 29th March
# import time
# import sys
# import os
# import traceback
# from datetime import datetime
# from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget, 
#                                QApplication, QSystemTrayIcon, QMenu)
# from PySide6.QtCore import QTimer, Qt
# from PySide6.QtGui import QIcon, QAction

# # Internal UI Imports
# from ui.sidebar import Sidebar
# from ui.pages.dashboard import Dashboard
# from ui.pages.smart_mode import SmartModePage
# from ui.pages.ai_mode import AIModePage
# from ui.pages.settings import SettingsPage
# from ui.pages.weekly_analytics import WeeklyAnalyticsPage
# from ui.pages.analytics_suite import AnalyticsSuitePage
# from ui.pages.ai_insights import AIInsightsPage
# from ui.pages.weekly_report import WeeklyReportPage
# from ui.pages.monthly_report import MonthlyReportPage

# # Internal Core Imports
# from core.settings import SettingsManager
# from core.smart_break_engine import SmartBreakEngine, SmartConfig
# from core.smart_break_engine_v2 import SmartBreakEngineV2
# from core.signal_collector import SignalCollector
# from core.reminder import Reminder
# from core.ai_reminder_messages import AIMessageGenerator
# from core.storage_manager import StorageManager
# from core.daily_summary_engine import DailySummaryEngine
# from ui.widgets.mini_video_window import MiniVideoWindow

# # --- PACKAGING HELPER (Kept for PyInstaller) ---
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# # --- WINDOWS POWER EVENTS ---
# if sys.platform == "win32":
#     import ctypes
#     from ctypes import wintypes
#     PBT_APMSUSPEND = 0x0004
#     PBT_APMRESUMEAUTOMATIC = 0x0012
#     PBT_APMRESUMESUSPEND = 0x0007
#     WM_POWERBROADCAST = 0x0218

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
        
#         # Paths & Icons
#         self.icon_path = resource_path(os.path.join("assets", "icons", "logo.png"))
#         self.setWindowIcon(QIcon(self.icon_path))
#         self.setWindowTitle("K-Mends Digital Wellbeing")
#         self.resize(960, 620)
#         self.setMinimumSize(820, 560)

#         # State tracking
#         self.last_tick = time.time()
#         self.monitoring = False
#         self.active_monitoring_mode = None
        
#         # Core Systems
#         self.settings = SettingsManager()
#         self.signals = SignalCollector()
#         self.hybrid_engine = SmartBreakEngine(SmartConfig())
#         self.ai_engine = SmartBreakEngineV2()
        
#         # PRODUCTION REMINDER (60s interval)
#         self.reminder = Reminder(main_window=self, min_interval_seconds=60)
        
#         self.ai_messages = AIMessageGenerator()
#         self.storage = StorageManager()
#         self.ai_history = []
#         self.app_start_time = time.time()
#         self.global_screen_seconds = 0

#         # UI Layout
#         container = QWidget()
#         layout = QHBoxLayout(container)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

#         self.sidebar = Sidebar(self)
#         self.pages = QStackedWidget()
#         layout.addWidget(self.sidebar)
#         layout.addWidget(self.pages, 1)

#         # Initialize Pages
#         self.dashboard_page = Dashboard(self)
#         self.smart_page = SmartModePage(self)
#         self.ai_mode_page = AIModePage(self) 
#         self.settings_page = SettingsPage(self)
#         self.weekly_page = WeeklyAnalyticsPage()
#         self.analytics_page = AnalyticsSuitePage(theme=self.settings.get("theme"))

#         self.insights_page = AIInsightsPage()
#         self.weekly_report_page = WeeklyReportPage()
#         self.monthly_report_page = MonthlyReportPage()

#         for page in [self.dashboard_page, self.smart_page, self.ai_mode_page, 
#                      self.settings_page, self.weekly_page, self.analytics_page, 
#                      self.insights_page, self.weekly_report_page, self.monthly_report_page]:
#             self.pages.addWidget(page)

#         self.setCentralWidget(container)
#         self.apply_theme()
#         self.show_dashboard()
#         self.setup_system_tray()

#         # Timer setup (1 second)
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.update_break_engine)
#         self.timer.start(1000)

#     def update_break_engine(self):
#         now = time.time()
#         last_tick = self.last_tick
#         self.last_tick = now

#         # 1. Sleep Guard (Detect if time jumped more than 60s)
#         if now - last_tick > 60:
#             self.handle_os_sleep()
#             return

#         if self.monitoring:
#             # Increment by 1 second instead of calculating from app_start_time
#             # to avoid counting time while the laptop was closed.
#             self.global_screen_seconds += 1

#         # 2. Update Dashboard UI
#         data = self.build_dashboard_data()
#         self.dashboard_page.update_dashboard(data)

#         # 3. Guard: If not monitoring, stop logic here
#         if not self.monitoring or not self.active_monitoring_mode:
#             return

#         self.signals.update()
#         signals = self.signals.to_dict()
        
#         # --- AI MODE LOGIC ---
#         if self.active_monitoring_mode == "AI Mode":
#             if self.ai_engine.session_start is None:
#                 self.ai_engine.session_start = now
            
#             self.ai_engine.real_time = now - self.ai_engine.session_start
#             decision = self.ai_engine.should_trigger_break(signals)
            
#             # Update history
#             self.ai_history.append({
#                 "timestamp": datetime.now(),
#                 "behavior": decision.get("behavior", "Idle"),
#                 "fatigue": decision.get("fatigue_score", 0.0),
#                 "break_triggered": decision.get("trigger", False),
#                 "break_reason": decision.get("reason", ""),
#                 "suppression": False
#             })

#             # Sync Engine state to UI
#             self.ai_engine.last_behavior = decision.get("behavior", "Idle")
#             self.ai_engine.last_fatigue = decision.get("fatigue_score", 0.0)
            
#             raw_seconds = decision.get("remaining_seconds", decision.get("interval_used", 1200))
#             self.ai_mode_page.update_ai_status(
#                 behavior=self.ai_engine.last_behavior,
#                 fatigue=self.ai_engine.last_fatigue,
#                 reason=decision.get("reason", ""),
#                 trigger=decision.get("trigger", False),
#                 next_break_minutes=max(0, round(raw_seconds / 60))
#             )

#             # Trigger check
#             if decision.get("trigger", False):
#                 self.reminder.send_break_message(decision)
#                 return 

#         # --- SMART MODE LOGIC ---
#         elif self.active_monitoring_mode == "Smart Mode":
#             decision = self.hybrid_engine.should_trigger_break(signals)
#             trigger = decision.get("trigger", False)
            
#             raw_seconds = decision.get("next_break_seconds", 1200)
#             self.smart_page.update_smart_status(
#                 behavior=decision.get("behavior", "Activity"),
#                 fatigue=decision.get("fatigue_score", 0.0),
#                 reason=decision.get("reason", ""),
#                 trigger=trigger,
#                 next_break_minutes=max(0, round(raw_seconds / 60))
#             )

#             if trigger:
#                 self.reminder.send_break_message(decision)
#                 return

#     def toggle_monitoring(self):
#         """ Handles the Start/Stop logic and syncs button text """
#         self.monitoring = not self.monitoring

#         if self.monitoring:
#             self.reminder.reset()

#             if self.pages.currentWidget() == self.smart_page:
#                 self.active_monitoring_mode = "Smart Mode"
#                 self.hybrid_engine.reset_after_break()

#             elif self.pages.currentWidget() == self.ai_mode_page:
#                 self.active_monitoring_mode = "AI Mode"
#                 self.ai_engine.session_start = time.time()
#                 self.ai_engine.real_time = 0

#             self.ai_mode_page.btn_toggle.setText("Stop K-Mends AI")
#         else:
#             self.active_monitoring_mode = None
#             self.ai_mode_page.btn_toggle.setText("Start K-Mends AI")

#         print(f"Monitoring Toggled: {self.monitoring}")

#     def build_dashboard_data(self):
#         signals = self.signals.to_dict()
#         mode = self.active_monitoring_mode or "No Active Mode"
#         meeting_active = (signals.get("window_category") == "meeting" or signals.get("webcam_active") is True)
#         screen_time = time.strftime("%H:%M:%S", time.gmtime(self.global_screen_seconds))
        
#         behavior = str(getattr(self.ai_engine, "last_behavior", "—")).replace("_", " ").title()
#         fatigue_score = round(float(getattr(self.ai_engine, "last_fatigue", 0.0)), 1)

#         return {
#             "screen_time": screen_time, "screen_seconds": self.global_screen_seconds,
#             "breaks": str(getattr(self.reminder, "break_count", 0)), "mode": mode,
#             "behavior": behavior, "fatigue_score": float(fatigue_score),
#             "fatigue_level": self.fatigue_level(fatigue_score),
#             "meeting": "On" if meeting_active else "Off",
#             "status": "Monitoring" if self.monitoring else "Not Monitoring",
#             "trend_value": self.global_screen_seconds
#         }

#     def fatigue_level(self, score):
#         try:
#             s = float(score)
#             if s < 25: return "Low"
#             elif s < 50: return "Medium"
#             elif s < 75: return "High"
#             else: return "Critical"
#         except: return "Low"

#     def setup_system_tray(self):
#         self.tray_icon = QSystemTrayIcon(self)
#         self.tray_icon.setIcon(QIcon(self.icon_path))
#         tray_menu = QMenu()
#         show_action = QAction("Open Dashboard", self)
#         show_action.triggered.connect(self.show_and_activate)
#         quit_action = QAction("Exit", self)
#         quit_action.triggered.connect(QApplication.instance().quit)
#         tray_menu.addAction(show_action)
#         tray_menu.addSeparator()
#         tray_menu.addAction(quit_action)
#         self.tray_icon.setContextMenu(tray_menu)
#         self.tray_icon.show()

#     def show_and_activate(self):
#         self.showNormal()
#         self.activateWindow()
#         self.raise_()

#     def apply_theme(self):
#         theme_name = self.settings.get("theme")
#         path = resource_path(os.path.join("assets", "themes", f"{theme_name}.qss"))
#         try:
#             if os.path.exists(path):
#                 with open(path, "r") as f: self.setStyleSheet(f.read())
#         except: pass

#     def handle_os_sleep(self):
#         """ Resets engines and silences reminders after system wake """
#         now = time.time()
#         print(f"Wake detected at {datetime.now()}. Resetting session clocks.")
        
#         self.ai_engine.session_start = now
#         self.ai_engine.real_time = 0
#         self.ai_engine.last_fatigue = 0.0
        
#         if hasattr(self.ai_engine, "last_break_time"):
#             self.ai_engine.last_break_time = now - 1200 
            
#         if hasattr(self, 'reminder'):
#             self.reminder.reset() # Mute notifications for 60s cooldown

#     # Page Navigation
#     def show_dashboard(self): self.pages.setCurrentWidget(self.dashboard_page)
#     def show_ai(self): self.pages.setCurrentWidget(self.ai_mode_page)
#     def show_smart(self): self.pages.setCurrentWidget(self.smart_page)
#     def show_settings(self): self.pages.setCurrentWidget(self.settings_page)
#     def show_weekly(self): self.pages.setCurrentWidget(self.weekly_page)
#     def show_analytics(self): self.analytics_page.refresh_all(); self.pages.setCurrentWidget(self.analytics_page)
#     def show_insights(self): self.insights_page.update_insights(self.ai_history); self.pages.setCurrentWidget(self.insights_page)
#     def show_weekly_report(self): self.weekly_report_page.refresh(); self.pages.setCurrentWidget(self.weekly_report_page)
#     def show_monthly_report(self): self.monthly_report_page.refresh(); self.pages.setCurrentWidget(self.monthly_report_page)

#     def closeEvent(self, event):
#         if self.tray_icon.isVisible():
#             self.hide()
#             event.ignore()
#         else:
#             DailySummaryEngine().generate_today()
#             event.accept()









# Final correct for mac
# Fixed the reminder 29th March
import time
import sys
import os
import traceback
from datetime import datetime
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget, 
                               QApplication, QSystemTrayIcon, QMenu)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon, QAction

# Internal UI Imports
from ui.sidebar import Sidebar
from ui.pages.dashboard import Dashboard
from ui.pages.smart_mode import SmartModePage
from ui.pages.ai_mode import AIModePage
from ui.pages.settings import SettingsPage
from ui.pages.weekly_analytics import WeeklyAnalyticsPage
from ui.pages.analytics_suite import AnalyticsSuitePage
from ui.pages.ai_insights import AIInsightsPage
from ui.pages.weekly_report import WeeklyReportPage
from ui.pages.monthly_report import MonthlyReportPage

# Internal Core Imports
from core.settings import SettingsManager
from core.smart_break_engine import SmartBreakEngine, SmartConfig
from core.smart_break_engine_v2 import SmartBreakEngineV2
from core.signal_collector import SignalCollector
from core.reminder import Reminder
from core.ai_reminder_messages import AIMessageGenerator
from core.storage_manager import StorageManager
from core.daily_summary_engine import DailySummaryEngine
from ui.widgets.mini_video_window import MiniVideoWindow

# --- PACKAGING HELPER (Kept for PyInstaller) ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- WINDOWS POWER EVENTS ---
if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes
    PBT_APMSUSPEND = 0x0004
    PBT_APMRESUMEAUTOMATIC = 0x0012
    PBT_APMRESUMESUSPEND = 0x0007
    WM_POWERBROADCAST = 0x0218

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Paths & Icons
        self.icon_path = resource_path(os.path.join("assets", "icons", "logo.png"))
        self.setWindowIcon(QIcon(self.icon_path))
        self.setWindowTitle("K-Mends Digital Wellbeing")
        self.resize(960, 620)
        self.setMinimumSize(820, 560)

        # State tracking
        self.last_tick = time.time()
        self.monitoring = False
        self.active_monitoring_mode = None
        
        # Core Systems
        self.settings = SettingsManager()
        self.signals = SignalCollector()
        self.hybrid_engine = SmartBreakEngine(SmartConfig())
        self.ai_engine = SmartBreakEngineV2()
        
        # PRODUCTION REMINDER (60s interval)
        self.reminder = Reminder(main_window=self, min_interval_seconds=60)
        
        self.ai_messages = AIMessageGenerator()
        self.storage = StorageManager()
        self.ai_history = []
        self.app_start_time = time.time()
        self.global_screen_seconds = 0

        # UI Layout
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = Sidebar(self)
        self.pages = QStackedWidget()
        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages, 1)

        # Initialize Pages
        self.dashboard_page = Dashboard(self)
        self.smart_page = SmartModePage(self)
        self.ai_mode_page = AIModePage(self) 
        self.settings_page = SettingsPage(self)
        self.weekly_page = WeeklyAnalyticsPage()
        self.analytics_page = AnalyticsSuitePage(theme=self.settings.get("theme"))

        self.insights_page = AIInsightsPage()
        self.weekly_report_page = WeeklyReportPage()
        self.monthly_report_page = MonthlyReportPage()

        for page in [self.dashboard_page, self.smart_page, self.ai_mode_page, 
                     self.settings_page, self.weekly_page, self.analytics_page, 
                     self.insights_page, self.weekly_report_page, self.monthly_report_page]:
            self.pages.addWidget(page)

        self.setCentralWidget(container)
        self.apply_theme()
        self.show_dashboard()
        self.setup_system_tray()

        # Timer setup (1 second)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_break_engine)
        self.timer.start(1000)

    def update_break_engine(self):
        now = time.time()
        last_tick = self.last_tick
        self.last_tick = now

        # 1. Sleep Guard (Detect if time jumped more than 60s)
        if now - last_tick > 60:
            self.handle_os_sleep()
            return

        if self.monitoring:
            self.global_screen_seconds += 1

        # 2. Update Dashboard UI
        data = self.build_dashboard_data()
        self.dashboard_page.update_dashboard(data)

        # 3. Guard: If not monitoring, stop logic here
        if not self.monitoring or not self.active_monitoring_mode:
            return

        self.signals.update()
        signals = self.signals.to_dict()
        
        # --- AI MODE LOGIC ---
        if self.active_monitoring_mode == "AI Mode":
            if self.ai_engine.session_start is None:
                self.ai_engine.session_start = now
            
            self.ai_engine.real_time = now - self.ai_engine.session_start
            decision = self.ai_engine.should_trigger_break(signals)
            
            self.ai_history.append({
                "timestamp": datetime.now(),
                "behavior": decision.get("behavior", "Idle"),
                "fatigue": decision.get("fatigue_score", 0.0),
                "break_triggered": decision.get("trigger", False),
                "break_reason": decision.get("reason", ""),
                "suppression": False
            })

            self.ai_engine.last_behavior = decision.get("behavior", "Idle")
            self.ai_engine.last_fatigue = decision.get("fatigue_score", 0.0)
            
            raw_seconds = decision.get("remaining_seconds", decision.get("interval_used", 1200))
            self.ai_mode_page.update_ai_status(
                behavior=self.ai_engine.last_behavior,
                fatigue=self.ai_engine.last_fatigue,
                reason=decision.get("reason", ""),
                trigger=decision.get("trigger", False),
                next_break_minutes=max(0, round(raw_seconds / 60))
            )

            if decision.get("trigger", False):
                self.reminder.send_break_message(decision)
                return 

        # --- SMART MODE LOGIC ---
        elif self.active_monitoring_mode == "Smart Mode":
            decision = self.hybrid_engine.should_trigger_break(signals)
            trigger = decision.get("trigger", False)
            
            raw_seconds = decision.get("next_break_seconds", 1200)
            self.smart_page.update_smart_status(
                behavior=decision.get("behavior", "Activity"),
                fatigue=decision.get("fatigue_score", 0.0),
                reason=decision.get("reason", ""),
                trigger=trigger,
                next_break_minutes=max(0, round(raw_seconds / 60))
            )

            if trigger:
                self.reminder.send_break_message(decision)
                return

    def toggle_monitoring(self):
        self.monitoring = not self.monitoring
        if self.monitoring:
            self.reminder.reset()
            if self.pages.currentWidget() == self.smart_page:
                self.active_monitoring_mode = "Smart Mode"
                self.hybrid_engine.reset_after_break()
            elif self.pages.currentWidget() == self.ai_mode_page:
                self.active_monitoring_mode = "AI Mode"
                self.ai_engine.session_start = time.time()
                self.ai_engine.real_time = 0
            self.ai_mode_page.btn_toggle.setText("Stop K-Mends AI")
        else:
            self.active_monitoring_mode = None
            self.ai_mode_page.btn_toggle.setText("Start K-Mends AI")

    def build_dashboard_data(self):
        signals = self.signals.to_dict()
        mode = self.active_monitoring_mode or "No Active Mode"
        meeting_active = (signals.get("window_category") == "meeting" or signals.get("webcam_active") is True)
        screen_time = time.strftime("%H:%M:%S", time.gmtime(self.global_screen_seconds))
        
        behavior = str(getattr(self.ai_engine, "last_behavior", "—")).replace("_", " ").title()
        fatigue_score = round(float(getattr(self.ai_engine, "last_fatigue", 0.0)), 1)

        return {
            "screen_time": screen_time, "screen_seconds": self.global_screen_seconds,
            "breaks": str(getattr(self.reminder, "break_count", 0)), "mode": mode,
            "behavior": behavior, "fatigue_score": float(fatigue_score),
            "fatigue_level": self.fatigue_level(fatigue_score),
            "meeting": "On" if meeting_active else "Off",
            "status": "Monitoring" if self.monitoring else "Not Monitoring",
            "trend_value": self.global_screen_seconds
        }

    def fatigue_level(self, score):
        try:
            s = float(score)
            if s < 25: return "Low"
            elif s < 50: return "Medium"
            elif s < 75: return "High"
            else: return "Critical"
        except: return "Low"

    def setup_system_tray(self):
        """ Configures the macOS/Windows tray icon with theme awareness """
        self.tray_icon = QSystemTrayIcon(self)
        
        # MAC FIX: Use specific tray icon if available, otherwise fallback to logo
        # We ensure setIsMask(True) so it turns white on dark menu bars
        tray_icon_file = resource_path(os.path.join("assets", "icons", "logo.png"))
        icon = QIcon(tray_icon_file)
        
        if sys.platform == "darwin":
            icon.setIsMask(True)
            
        self.tray_icon.setIcon(icon)
        
        tray_menu = QMenu()
        show_action = QAction("Open Dashboard", self)
        show_action.triggered.connect(self.show_and_activate)
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def show_and_activate(self):
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def apply_theme(self):
        theme_name = self.settings.get("theme")
        path = resource_path(os.path.join("assets", "themes", f"{theme_name}.qss"))
        try:
            if os.path.exists(path):
                with open(path, "r") as f: self.setStyleSheet(f.read())
        except: pass

    def handle_os_sleep(self):
        now = time.time()
        self.ai_engine.session_start = now
        self.ai_engine.real_time = 0
        self.ai_engine.last_fatigue = 0.0
        if hasattr(self.ai_engine, "last_break_time"):
            self.ai_engine.last_break_time = now - 1200 
        if hasattr(self, 'reminder'):
            self.reminder.reset()

    # Page Navigation
    def show_dashboard(self): self.pages.setCurrentWidget(self.dashboard_page)
    def show_ai(self): self.pages.setCurrentWidget(self.ai_mode_page)
    def show_smart(self): self.pages.setCurrentWidget(self.smart_page)
    def show_settings(self): self.pages.setCurrentWidget(self.settings_page)
    def show_weekly(self): self.pages.setCurrentWidget(self.weekly_page)
    def show_analytics(self): self.analytics_page.refresh_all(); self.pages.setCurrentWidget(self.analytics_page)
    def show_insights(self): self.insights_page.update_insights(self.ai_history); self.pages.setCurrentWidget(self.insights_page)
    def show_weekly_report(self): self.weekly_report_page.refresh(); self.pages.setCurrentWidget(self.weekly_report_page)
    def show_monthly_report(self): self.monthly_report_page.refresh(); self.pages.setCurrentWidget(self.monthly_report_page)

    def closeEvent(self, event):
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            DailySummaryEngine().generate_today()
            event.accept()