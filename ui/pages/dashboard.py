
# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
# )
# from PySide6.QtCore import Qt, QPropertyAnimation
# from PySide6.QtSvgWidgets import QSvgWidget

# from ui.widgets.meeting_badge import MeetingBadge
# from ui.widgets.mini_chart import MiniChart
# from ui.widgets.fluent_blur import FluentBlur

# from datetime import datetime, timedelta
# import json, os


# class FluentCard(QFrame):
#     """
#     Premium Fluent dashboard card:
#       - 22px Fluent SVG icon (theme-adaptive)
#       - title
#       - animated value
#       - optional heat bar
#       - optional MiniChart sparkline
#       - NO info icon
#     """

#     def __init__(self, title, value="—", show_chart=True, show_heat=False, icon_path=None):
#         super().__init__()
#         self.setObjectName("FluentCard")

#         self.setMinimumHeight(190)
#         self.setFocusPolicy(Qt.NoFocus)
#         self.setAttribute(Qt.WA_NoMousePropagation)

#         # Fade-in animation
#         self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
#         self.fade_anim.setDuration(350)
#         self.fade_anim.setStartValue(0.0)
#         self.fade_anim.setEndValue(1.0)
#         self.fade_anim.start()

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(12, 4, 10, 10)
#         layout.setSpacing(8)

#         # ---------------------------------------------------------
#         # LEFT ICON (22px Fluent SVG, theme-adaptive)
#         # ---------------------------------------------------------
#         self.icon = None
#         if icon_path:
#             self.icon = QSvgWidget(icon_path)
#             self.icon.setFixedSize(22, 22)  # bigger Fluent icon
#             self.icon.setObjectName("FluentIcon")  # for theme coloring

#         # Meeting badge
#         self.meeting_badge = MeetingBadge()
#         self.meeting_badge.setVisible(False)
#         layout.addWidget(self.meeting_badge, alignment=Qt.AlignLeft)

#         # ---------------------------------------------------------
#         # TITLE ROW
#         # ---------------------------------------------------------
#         title_row = QHBoxLayout()
#         title_row.setSpacing(8)

#         if self.icon:
#             title_row.addWidget(self.icon)

#         self.title_label = QLabel(title)
#         self.title_label.setObjectName("CardTitle")
#         title_row.addWidget(self.title_label)

#         title_row.addStretch()
#         layout.addLayout(title_row)

#         # ---------------------------------------------------------
#         # VALUE
#         # ---------------------------------------------------------
#         self.value_label = QLabel(value)
#         self.value_label.setObjectName("CardValue")
#         layout.addWidget(self.value_label)

#         self.current_value = value

#         # ---------------------------------------------------------
#         # HEAT BAR
#         # ---------------------------------------------------------
#         self.heat_bar = None
#         if show_heat:
#             self.heat_bar = QFrame()
#             self.heat_bar.setFixedHeight(6)
#             self.heat_bar.setObjectName("HeatBar")
#             layout.addWidget(self.heat_bar)

#         # ---------------------------------------------------------
#         # SPARKLINE (MiniChart)
#         # ---------------------------------------------------------
#         self.chart = None
#         if show_chart:
#             self.chart = MiniChart()
#             layout.addWidget(self.chart)

#         layout.addStretch()

#     # ---------------------------------------------------------
#     def update_value(self, new_value):
#         self.value_label.setText(str(new_value))
#         self.current_value = new_value

#     # ---------------------------------------------------------
#     def set_heat_color(self, level):
#         if not self.heat_bar:
#             return

#         colors = {
#             "Low": "#4CAF50",
#             "Medium": "#FFC107",
#             "High": "#FF5722",
#             "Critical": "#F44336"
#         }
#         self.heat_bar.setStyleSheet(
#             f"background-color: {colors.get(level, '#4CAF50')}; border-radius: 3px;"
#         )
# # ============================================================
# # DASHBOARD (PERSISTENT DAILY FATIGUE HISTORY)
# # ============================================================

# class Dashboard(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main

#         self.daily_fatigue_history = []
#         self.last_fatigue_sample_time = None
#         self.current_day = datetime.now().date()

#         self.load_daily_fatigue_history()

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)
#         layout.setSpacing(20)

#         # ============================================================
#         # ROW 1
#         # ============================================================
#         row1 = QHBoxLayout()
#         row1.setSpacing(20)

#         self.card_screen_time = FluentCard(
#             "Screen Time Today",
#             show_chart=True,
#             icon_path="assets/icons/clock-20-regular.svg"
#         )

#         self.card_breaks = FluentCard(
#             "Breaks Taken",
#             show_chart=True,
#             icon_path="assets/icons/pause-circle-20-regular.svg"
#         )

#         self.card_mode = FluentCard(
#             "Active Mode",
#             show_chart=False,
#             icon_path="assets/icons/flash-20-regular.svg"
#         )

#         row1.addWidget(self.wrap_blur(self.card_screen_time))
#         row1.addWidget(self.wrap_blur(self.card_breaks))
#         row1.addWidget(self.wrap_blur(self.card_mode))
#         layout.addLayout(row1)

#         # ============================================================
#         # ROW 2
#         # ============================================================
#         row2 = QHBoxLayout()
#         row2.setSpacing(20)

#         self.card_behavior = FluentCard(
#             "Behavior",
#             show_chart=True,
#             icon_path="assets/icons/insights.svg"
#         )

#         self.card_fatigue = FluentCard(
#             "Fatigue",
#             show_chart=True,
#             show_heat=True,
#             icon_path="assets/icons/heart-pulse-20-regular.svg"
#         )

#         self.card_status = FluentCard(
#             "Status",
#             show_chart=False,
#             icon_path="assets/icons/monitoring.svg"
#         )

#         row2.addWidget(self.wrap_blur(self.card_behavior))
#         row2.addWidget(self.wrap_blur(self.card_fatigue))
#         row2.addWidget(self.wrap_blur(self.card_status))
#         layout.addLayout(row2)

#         # ============================================================
#         # ROW 3 — DAILY OVERVIEW
#         # ============================================================
#         row3 = QHBoxLayout()
#         row3.setSpacing(20)

#         self.card_overview = FluentCard(
#             "Daily Overview",
#             value="Daily Fatigue Trend",
#             show_chart=True,
#             icon_path="assets/icons/data-line-20-regular.svg"
#         )

#         if self.card_overview.chart:
#             self.card_overview.chart.set_points(self.daily_fatigue_history)

#         row3.addWidget(self.wrap_blur(self.card_overview))
#         layout.addLayout(row3)

#         self.meeting_badge = self.card_status.meeting_badge

#     # ---------------------------------------------------------
#     def wrap_blur(self, card):
#         blur = FluentBlur(radius=25, opacity=0.30)
#         blur.layout.addWidget(card)
#         return blur

#     # ---------------------------------------------------------
#     def fatigue_history_path(self):
#         day = datetime.now().strftime("%Y-%m-%d")
#         return os.path.join("data", f"fatigue_history_{day}.json")

#     # ---------------------------------------------------------
#     def load_daily_fatigue_history(self):
#         path = self.fatigue_history_path()
#         if os.path.exists(path):
#             try:
#                 with open(path, "r") as f:
#                     self.daily_fatigue_history = json.load(f).get("history", [])
#             except:
#                 self.daily_fatigue_history = []
#         else:
#             self.daily_fatigue_history = []

#     # ---------------------------------------------------------
#     def save_daily_fatigue_history(self):
#         path = self.fatigue_history_path()
#         os.makedirs(os.path.dirname(path), exist_ok=True)
#         with open(path, "w") as f:
#             json.dump({"history": self.daily_fatigue_history}, f, indent=2)

#     # ---------------------------------------------------------
#     def update_daily_fatigue_history(self, fatigue_score):
#         now = datetime.now()

#         if now.date() != self.current_day:
#             self.daily_fatigue_history = []
#             self.current_day = now.date()
#             self.last_fatigue_sample_time = None

#         if self.last_fatigue_sample_time is None:
#             self.daily_fatigue_history.append(fatigue_score)
#             self.last_fatigue_sample_time = now
#             self.save_daily_fatigue_history()
#             return

#         if now - self.last_fatigue_sample_time >= timedelta(minutes=5):
#             self.daily_fatigue_history.append(fatigue_score)
#             self.last_fatigue_sample_time = now
#             self.save_daily_fatigue_history()

#         if self.card_overview.chart:
#             self.card_overview.chart.set_points(self.daily_fatigue_history)

#     # ---------------------------------------------------------
#     def update_dashboard(self, data):

#         self.card_screen_time.update_value(data["screen_time"])
#         self.card_breaks.update_value(data["breaks"])
#         self.card_mode.update_value(data["mode"])

#         self.card_behavior.update_value(data["behavior"])
#         self.card_fatigue.update_value(f"{data['fatigue_score']} ({data['fatigue_level']})")
#         self.card_fatigue.set_heat_color(data["fatigue_level"])
#         self.card_status.update_value(data["status"])

#         if data.get("meeting") and data["meeting"] != "Off":
#             self.meeting_badge.show()
#             #self.meeting_badge.update_text(data["meeting"])
#             self.meeting_badge.setText(data["meeting"])

#         else:
#             self.meeting_badge.hide()

#         self.card_overview.update_value("Daily Fatigue Trend")
#         self.update_daily_fatigue_history(data["fatigue_score"])

#         if self.card_screen_time.chart:
#             self.card_screen_time.chart.add_point(data["screen_seconds"])

#         if self.card_breaks.chart:
#             self.card_breaks.chart.add_point(float(data["breaks"]))

#         if self.card_behavior.chart:
#             self.card_behavior.chart.add_point(data.get("behavior_score", 0))

#         if self.card_fatigue.chart:
#             self.card_fatigue.chart.add_point(data["fatigue_score"])



















import os
import sys
import json
from datetime import datetime, timedelta

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
)
from PySide6.QtCore import Qt, QPropertyAnimation
from PySide6.QtGui import QPixmap
from PySide6.QtSvgWidgets import QSvgWidget

from ui.widgets.meeting_badge import MeetingBadge
from ui.widgets.mini_chart import MiniChart
from ui.widgets.fluent_blur import FluentBlur

# --- THE MAGIC HELPER FOR EXE PATHS ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class FluentCard(QFrame):
    """
    Premium Fluent dashboard card:
      - 22px Fluent SVG icon (wrapped for EXE)
      - title, animated value, optional heat bar, optional MiniChart
    """
    def __init__(self, title, value="—", show_chart=True, show_heat=False, icon_path=None):
        super().__init__()
        self.setObjectName("FluentCard")
        self.setMinimumHeight(190)
        self.setFocusPolicy(Qt.NoFocus)
        self.setAttribute(Qt.WA_NoMousePropagation)

        # Fade-in animation
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(350)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 4, 10, 10)
        layout.setSpacing(8)

        # ---------------------------------------------------------
        # LEFT ICON (Correctly wrapped for PyInstaller)
        # ---------------------------------------------------------
        self.icon = None
        if icon_path:
            fixed_icon_path = resource_path(icon_path)
            self.icon = QSvgWidget(fixed_icon_path)
            self.icon.setFixedSize(22, 22)
            self.icon.setObjectName("FluentIcon")

        self.meeting_badge = MeetingBadge()
        self.meeting_badge.setVisible(False)
        layout.addWidget(self.meeting_badge, alignment=Qt.AlignLeft)

        # ---------------------------------------------------------
        # TITLE ROW
        # ---------------------------------------------------------
        title_row = QHBoxLayout()
        title_row.setSpacing(8)
        if self.icon:
            title_row.addWidget(self.icon)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("CardTitle")
        title_row.addWidget(self.title_label)
        title_row.addStretch()
        layout.addLayout(title_row)

        # ---------------------------------------------------------
        # VALUE
        # ---------------------------------------------------------
        self.value_label = QLabel(value)
        self.value_label.setObjectName("CardValue")
        layout.addWidget(self.value_label)
        self.current_value = value

        # ---------------------------------------------------------
        # HEAT BAR
        # ---------------------------------------------------------
        self.heat_bar = None
        if show_heat:
            self.heat_bar = QFrame()
            self.heat_bar.setFixedHeight(6)
            self.heat_bar.setObjectName("HeatBar")
            layout.addWidget(self.heat_bar)

        # ---------------------------------------------------------
        # SPARKLINE (MiniChart)
        # ---------------------------------------------------------
        self.chart = None
        if show_chart:
            self.chart = MiniChart()
            layout.addWidget(self.chart)

        layout.addStretch()

    def update_value(self, new_value):
        self.value_label.setText(str(new_value))
        self.current_value = new_value

    def set_heat_color(self, level):
        if not self.heat_bar: return
        colors = {"Low": "#4CAF50", "Medium": "#FFC107", "High": "#FF5722", "Critical": "#F44336"}
        self.heat_bar.setStyleSheet(f"background-color: {colors.get(level, '#4CAF50')}; border-radius: 3px;")

# ============================================================
# DASHBOARD CLASS
# ============================================================

class Dashboard(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.daily_fatigue_history = []
        self.last_fatigue_sample_time = None
        self.current_day = datetime.now().date()
        self.load_daily_fatigue_history()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 20)
        layout.setSpacing(15)

        # # --- LOGO SECTION ---
        # self.logo_label = QLabel() 
        # logo_img = resource_path(os.path.join("assets", "icons", "logo.png"))
        # self.logo_label.setPixmap(QPixmap(logo_img).scaledToHeight(50, Qt.SmoothTransformation))
        # layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

        # --- ROW 1 ---
        row1 = QHBoxLayout()
        row1.setSpacing(20)
        self.card_screen_time = FluentCard("Screen Time Today", icon_path="assets/icons/clock-20-regular.svg")
        self.card_breaks = FluentCard("Breaks Taken", icon_path="assets/icons/pause-circle-20-regular.svg")
        self.card_mode = FluentCard("Active Mode", show_chart=False, icon_path="assets/icons/flash-20-regular.svg")
        
        row1.addWidget(self.wrap_blur(self.card_screen_time))
        row1.addWidget(self.wrap_blur(self.card_breaks))
        row1.addWidget(self.wrap_blur(self.card_mode))
        layout.addLayout(row1)

        # --- ROW 2 ---
        row2 = QHBoxLayout()
        row2.setSpacing(20)
        self.card_behavior = FluentCard("Behavior", icon_path="assets/icons/insights.svg")
        self.card_fatigue = FluentCard("Fatigue", show_heat=True, icon_path="assets/icons/heart-pulse-20-regular.svg")
        self.card_status = FluentCard("Status", show_chart=False, icon_path="assets/icons/monitoring.svg")
        
        row2.addWidget(self.wrap_blur(self.card_behavior))
        row2.addWidget(self.wrap_blur(self.card_fatigue))
        row2.addWidget(self.wrap_blur(self.card_status))
        layout.addLayout(row2)

        # --- ROW 3 (TREND) ---
        row3 = QHBoxLayout()
        self.card_overview = FluentCard("Daily Overview", value="Daily Fatigue Trend", icon_path="assets/icons/data-line-20-regular.svg")
        if self.card_overview.chart:
            self.card_overview.chart.set_points(self.daily_fatigue_history)
        row3.addWidget(self.wrap_blur(self.card_overview))
        layout.addLayout(row3)

        self.meeting_badge = self.card_status.meeting_badge

    def wrap_blur(self, card):
        blur = FluentBlur(radius=25, opacity=0.30)
        blur.layout.addWidget(card)
        return blur

    def fatigue_history_path(self):
        day = datetime.now().strftime("%Y-%m-%d")
        return os.path.join("data", f"fatigue_history_{day}.json")

    def load_daily_fatigue_history(self):
        path = self.fatigue_history_path()
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    self.daily_fatigue_history = json.load(f).get("history", [])
            except: self.daily_fatigue_history = []
        else: self.daily_fatigue_history = []

    def save_daily_fatigue_history(self):
        path = self.fatigue_history_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump({"history": self.daily_fatigue_history}, f, indent=2)

    def update_daily_fatigue_history(self, fatigue_score):
        now = datetime.now()
        if now.date() != self.current_day:
            self.daily_fatigue_history = []
            self.current_day = now.date()
            self.last_fatigue_sample_time = None

        if self.last_fatigue_sample_time is None or (now - self.last_fatigue_sample_time >= timedelta(minutes=5)):
            self.daily_fatigue_history.append(fatigue_score)
            self.last_fatigue_sample_time = now
            self.save_daily_fatigue_history()

        if self.card_overview.chart:
            self.card_overview.chart.set_points(self.daily_fatigue_history)

    def update_dashboard(self, data):
        self.card_screen_time.update_value(data["screen_time"])
        self.card_breaks.update_value(data["breaks"])
        self.card_mode.update_value(data["mode"])
        self.card_behavior.update_value(data["behavior"])
        self.card_fatigue.update_value(f"{data['fatigue_score']}% ({data['fatigue_level']})")
        self.card_fatigue.set_heat_color(data["fatigue_level"])
        self.card_status.update_value(data["status"])

        if data.get("meeting") and data["meeting"] != "Off":
            self.meeting_badge.show()
            self.meeting_badge.setText(data["meeting"])
        else:
            self.meeting_badge.hide()

        self.update_daily_fatigue_history(data["fatigue_score"])
        if self.card_screen_time.chart: self.card_screen_time.chart.add_point(data["screen_seconds"])
        if self.card_breaks.chart: self.card_breaks.chart.add_point(float(data["breaks"]))
        if self.card_behavior.chart: self.card_behavior.chart.add_point(data.get("behavior_score", 0))
        if self.card_fatigue.chart: self.card_fatigue.chart.add_point(data["fatigue_score"])