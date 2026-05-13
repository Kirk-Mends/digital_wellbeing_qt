# import csv
# from datetime import datetime, timedelta

# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
# from PySide6.QtCore import Qt
# import pyqtgraph as pg


# class WeeklyAnalyticsPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("WeeklyAnalyticsPage")

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)
#         layout.setSpacing(20)

#         # -------------------------
#         # TITLE
#         # -------------------------
#         title = QLabel("Weekly Analytics")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # -------------------------
#         # SUMMARY CARDS
#         # -------------------------
#         self.summary_container = QHBoxLayout()
#         layout.addLayout(self.summary_container)

#         self.card_avg = self.make_card("Average Active Minutes", "0")
#         self.card_total = self.make_card("Total Active Minutes", "0")
#         self.card_best = self.make_card("Best Day", "-")
#         self.card_trend = self.make_card("Trend", "-")

#         self.summary_container.addWidget(self.card_avg)
#         self.summary_container.addWidget(self.card_total)
#         self.summary_container.addWidget(self.card_best)
#         self.summary_container.addWidget(self.card_trend)

#         # -------------------------
#         # WEEKLY BAR CHART
#         # -------------------------
#         self.chart = pg.PlotWidget()
#         self.chart.setBackground(None)
#         self.chart.showGrid(x=False, y=True, alpha=0.2)
#         self.chart.getAxis("left").setVisible(False)
#         self.chart.getAxis("bottom").setVisible(False)

#         self.bar_item = pg.BarGraphItem(x=[], height=[], width=0.6, brush="#0078D7")
#         self.chart.addItem(self.bar_item)

#         layout.addWidget(self.chart)

#         # Load data immediately
#         self.update_weekly_data()

#     # -------------------------
#     # SUMMARY CARD WIDGET
#     # -------------------------
#     def make_card(self, title, value):
#         frame = QFrame()
#         frame.setObjectName("SummaryCard")
#         frame.setMinimumWidth(150)

#         v = QVBoxLayout(frame)
#         v.setContentsMargins(16, 16, 16, 16)

#         label_title = QLabel(title)
#         label_title.setObjectName("CardTitle")

#         label_value = QLabel(value)
#         label_value.setObjectName("CardValue")

#         v.addWidget(label_title)
#         v.addWidget(label_value)
#         v.addStretch()

#         frame.value_label = label_value
#         return frame

#     # -------------------------
#     # LOAD WEEKLY DATA
#     # -------------------------
#     def update_weekly_data(self):
#         today = datetime.now().date()
#         week_start = today - timedelta(days=today.weekday())  # Monday

#         dates = []
#         minutes = []

#         # Initialize dictionary for 7 days
#         daily = {week_start + timedelta(days=i): 0 for i in range(7)}

#         # Read CSV
#         try:
#             with open("usage_log.csv", "r") as f:
#                 reader = csv.DictReader(f)
#                 for row in reader:
#                     date = datetime.fromisoformat(row["date"]).date()
#                     if date in daily:
#                         daily[date] += float(row["active_minutes"])
#         except FileNotFoundError:
#             pass

#         # Convert to lists
#         dates = list(daily.keys())
#         minutes = list(daily.values())

#         # Update chart
#         x = list(range(7))
#         self.bar_item.setOpts(x=x, height=minutes)

#         # Update summary cards
#         avg = sum(minutes) / 7
#         total = sum(minutes)
#         best_day_index = minutes.index(max(minutes))
#         best_day = dates[best_day_index].strftime("%A")

#         # Trend: compare last week vs this week
#         trend = "↗ Improving" if minutes[-1] > minutes[0] else "↘ Declining"

#         self.card_avg.value_label.setText(f"{avg:.1f} min")
#         self.card_total.value_label.setText(f"{total:.0f} min")
#         self.card_best.value_label.setText(best_day)
#         self.card_trend.value_label.setText(trend)














# # Cleaned for UI nice seeing without dashes
# import csv
# from datetime import datetime, timedelta

# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
# from PySide6.QtCore import Qt
# import pyqtgraph as pg


# class WeeklyAnalyticsPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("WeeklyAnalyticsPage")

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)
#         layout.setSpacing(20)

#         # -------------------------
#         # TITLE
#         # -------------------------
#         title = QLabel("Weekly Analytics")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # -------------------------
#         # SUMMARY CARDS
#         # -------------------------
#         self.summary_container = QHBoxLayout()
#         layout.addLayout(self.summary_container)

#         self.card_avg = self.make_card("Average Active Minutes", "0")
#         self.card_total = self.make_card("Total Active Minutes", "0")
#         self.card_best = self.make_card("Best Day", "-")
#         self.card_trend = self.make_card("Trend", "-")

#         self.summary_container.addWidget(self.card_avg)
#         self.summary_container.addWidget(self.card_total)
#         self.summary_container.addWidget(self.card_best)
#         self.summary_container.addWidget(self.card_trend)

#         # -------------------------
#         # WEEKLY BAR CHART
#         # -------------------------
#         self.chart = pg.PlotWidget()
#         self.chart.setBackground(None)
#         self.chart.showGrid(x=False, y=True, alpha=0.2)
#         self.chart.getAxis("left").setVisible(False)
#         self.chart.getAxis("bottom").setVisible(False)

#         self.bar_item = pg.BarGraphItem(x=[], height=[], width=0.6, brush="#0078D7")
#         self.chart.addItem(self.bar_item)

#         layout.addWidget(self.chart)

#         # Load data immediately
#         self.update_weekly_data()

#     # -------------------------
#     # SUMMARY CARD WIDGET
#     # -------------------------
#     def make_card(self, title, value):
#         frame = QFrame()
#         frame.setObjectName("SummaryCard")
#         frame.setMinimumWidth(150)

#         v = QVBoxLayout(frame)
#         v.setContentsMargins(16, 16, 16, 16)

#         label_title = QLabel(title)
#         label_title.setObjectName("CardTitle")

#         label_value = QLabel(value)
#         label_value.setObjectName("CardValue")

#         v.addWidget(label_title)
#         v.addWidget(label_value)
#         v.addStretch()

#         frame.value_label = label_value
#         return frame

#     # -------------------------
#     # LOAD WEEKLY DATA
#     # -------------------------
#     def update_weekly_data(self):
#         today = datetime.now().date()
#         week_start = today - timedelta(days=today.weekday())  # Monday

#         # Initialize dictionary for 7 days
#         daily = {week_start + timedelta(days=i): 0 for i in range(7)}

#         # Read CSV
#         try:
#             with open("usage_log.csv", "r") as f:
#                 reader = csv.DictReader(f)
#                 for row in reader:
#                     date = datetime.fromisoformat(row["date"]).date()
#                     if date in daily:
#                         daily[date] += float(row["active_minutes"])
#         except FileNotFoundError:
#             pass

#         # Convert to lists
#         dates = list(daily.keys())
#         minutes = list(daily.values())

#         # Update chart
#         x = list(range(7))
#         self.bar_item.setOpts(x=x, height=minutes)

#         # Update summary cards
#         avg = sum(minutes) / 7
#         total = sum(minutes)
#         best_day_index = minutes.index(max(minutes))
#         best_day = dates[best_day_index].strftime("%A")

#         # Trend: compare first vs last day
#         if minutes[-1] > minutes[0]:
#             trend = "↗ Improving"
#         elif minutes[-1] < minutes[0]:
#             trend = "↘ Declining"
#         else:
#             trend = "→ Stable"

#         self.card_avg.value_label.setText(f"{avg:.1f} min")
#         self.card_total.value_label.setText(f"{total:.0f} min")
#         self.card_best.value_label.setText(best_day)
#         self.card_trend.value_label.setText(trend)
















# # Cleaned for UI nice seeing without dashes
# from datetime import datetime, timedelta
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
# from PySide6.QtCore import Qt
# import pyqtgraph as pg

# from core.weekly_summary_engine import WeeklySummaryEngine


# class WeeklyAnalyticsPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("WeeklyAnalyticsPage")

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)
#         layout.setSpacing(20)

#         # -------------------------
#         # TITLE
#         # -------------------------
#         title = QLabel("Weekly Analytics")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # -------------------------
#         # SUMMARY CARDS
#         # -------------------------
#         self.summary_container = QHBoxLayout()
#         layout.addLayout(self.summary_container)

#         self.card_avg = self.make_card("Average Focus Minutes", "0")
#         self.card_total = self.make_card("Total Focus Minutes", "0")
#         self.card_best = self.make_card("Strongest Day", "-")
#         self.card_trend = self.make_card("Trend", "-")

#         self.summary_container.addWidget(self.card_avg)
#         self.summary_container.addWidget(self.card_total)
#         self.summary_container.addWidget(self.card_best)
#         self.summary_container.addWidget(self.card_trend)

#         # -------------------------
#         # WEEKLY BAR CHART
#         # -------------------------
#         self.chart = pg.PlotWidget()
#         self.chart.setBackground(None)
#         self.chart.showGrid(x=False, y=True, alpha=0.2)
#         self.chart.getAxis("left").setVisible(False)
#         self.chart.getAxis("bottom").setVisible(False)

#         # Disable all mouse interaction (fixes the "A" issue)
#         vb = self.chart.getViewBox()
#         vb.setMouseEnabled(x=False, y=False)
#         vb.setMenuEnabled(False)
#         self.chart.wheelEvent = lambda event: None
#         vb.setLimits(minXRange=1, minYRange=1)

#         self.bar_item = pg.BarGraphItem(x=[], height=[], width=0.6, brush="#0078D7")
#         self.chart.addItem(self.bar_item)

#         layout.addWidget(self.chart)

#         # Load data immediately
#         self.update_weekly_data()

#     # -------------------------
#     # SUMMARY CARD WIDGET
#     # -------------------------
#     def make_card(self, title, value):
#         frame = QFrame()
#         frame.setObjectName("SummaryCard")
#         frame.setMinimumWidth(150)

#         v = QVBoxLayout(frame)
#         v.setContentsMargins(16, 16, 16, 16)

#         label_title = QLabel(title)
#         label_title.setObjectName("CardTitle")

#         label_value = QLabel(value)
#         label_value.setObjectName("CardValue")

#         v.addWidget(label_title)
#         v.addWidget(label_value)
#         v.addStretch()

#         frame.value_label = label_value
#         return frame

    # -------------------------
    # LOAD WEEKLY DATA (NEW)
    # -------------------------
    # def update_weekly_data(self):
    #     engine = WeeklySummaryEngine()
    #     summary = engine.generate_this_week()

    #     # Extract values
    #     total = summary["total_focus"]
    #     avg = total / 7
    #     deep_work = summary["deep_work"]
    #     deep_reading = summary["deep_reading"]
    #     focused_interaction = summary["focused_interaction"]

    #     # Build bar chart data (focus minutes per day)
    #     # We load daily summaries directly from storage
    #     week_start = datetime.strptime(summary["week_start"], "%Y-%m-%d")
    #     daily_values = []

    #     for i in range(7):
    #         date_str = (week_start).strftime("%Y-%m-%d")
    #         row = engine.storage.get_daily_summary(date_str)
    #         if row:
    #             daily_values.append(row[1])  # total_focus
    #         else:
    #             daily_values.append(0)
    #         week_start += timedelta(days=1)

    #     # Update chart
    #     x = list(range(7))
    #     self.bar_item.setOpts(x=x, height=daily_values)

    #     # Best day
    #     best_index = daily_values.index(max(daily_values))
    #     best_day = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][best_index]

    #     # Trend
    #     if daily_values[-1] > daily_values[0]:
    #         trend = "↗ Improving"
    #     elif daily_values[-1] < daily_values[0]:
    #         trend = "↘ Declining"
    #     else:
    #         trend = "→ Stable"

    #     # Update summary cards
    #     self.card_avg.value_label.setText(f"{avg:.1f} min")
    #     self.card_total.value_label.setText(f"{total:.0f} min")
    #     self.card_best.value_label.setText(best_day)
    #     self.card_trend.value_label.setText(trend)















# 25th March
# from datetime import datetime, timedelta
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QColor  # Fixed the missing import
# import pyqtgraph as pg

# # --- ENGINE IMPORT ---
# try:
#     from core.weekly_summary_engine import WeeklySummaryEngine
# except ImportError:
#     # Mock engine for standalone testing
#     class WeeklySummaryEngine:
#         def __init__(self): 
#             self.storage = type('obj', (object,), {'get_daily_summary': lambda s, d: [0, 45]})()
#         def generate_this_week(self): 
#             return {
#                 "total_focus": 320, 
#                 "week_start": datetime.now().strftime("%Y-%m-%d"),
#                 "deep_work": 150, 
#                 "deep_reading": 100, 
#                 "focused_interaction": 70
#             }

# class WeeklyAnalyticsPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("WeeklyAnalyticsPage")

#         # 1. THEME DETECTION FOR PREMIUM UI
#         current_bg = self.palette().window().color().name().upper()
#         # Set executive accent based on background
#         if current_bg == "#F2F6FC": # Blue Mode
#             self.accent = "#0057D9"
#         elif current_bg == "#161618": # Dark Mode
#             self.accent = "#4DA3FF"
#         else: # Light Mode
#             self.accent = "#0057D9"

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(25)

#         # --- HEADER ---
#         header = QHBoxLayout()
#         title_v = QVBoxLayout()
#         title = QLabel("Weekly Performance")
#         title.setObjectName("PageTitle")
        
#         subtitle = QLabel("AI-Powered Behavioral Insights")
#         subtitle.setStyleSheet("font-size: 12px; opacity: 0.6; font-weight: 400; letter-spacing: 0.5px;")
        
#         title_v.addWidget(title)
#         title_v.addWidget(subtitle)
#         header.addLayout(title_v)
#         header.addStretch()
#         layout.addLayout(header)

#         # --- SUMMARY CARDS ---
#         self.summary_container = QHBoxLayout()
#         self.summary_container.setSpacing(15)
#         layout.addLayout(self.summary_container)

#         self.card_avg = self.make_card("Daily Average", "0m")
#         self.card_total = self.make_card("Week Total", "0m")
#         self.card_best = self.make_card("Peak Day", "-")
#         self.card_trend = self.make_card("7D Trend", "-")

#         self.summary_container.addWidget(self.card_avg)
#         self.summary_container.addWidget(self.card_total)
#         self.summary_container.addWidget(self.card_best)
#         self.summary_container.addWidget(self.card_trend)

#         # --- PREMIUM CHART SECTION ---
#         self.chart_card = QFrame()
#         self.chart_card.setObjectName("FluentCard")
#         self.chart_card.setStyleSheet("background-color: rgba(255,255,255,0.05); border-radius: 12px;")
#         chart_layout = QVBoxLayout(self.chart_card)
#         chart_layout.setContentsMargins(20, 20, 20, 20)
        
#         self.chart = pg.PlotWidget()
#         self.chart.setBackground(None)
#         self.chart.setAntialiasing(True)
#         self.chart.showGrid(x=False, y=True, alpha=0.1)
        
#         # Style X-Axis (Essential for Apple Review)
#         ax_bottom = self.chart.getAxis("bottom")
#         ax_bottom.setPen(QColor(150, 150, 150, 50))
#         ax_bottom.setTextPen(QColor(150, 150, 150, 180))
        
#         self.chart.getAxis("left").setVisible(False)

#         # Interaction Lock (Dashboard Mode)
#         vb = self.chart.getViewBox()
#         vb.setMouseEnabled(x=False, y=False)
#         vb.setMenuEnabled(False)
#         self.chart.setMenuEnabled(False)

#         self.bar_item = pg.BarGraphItem(x=[], height=[], width=0.6)
#         self.chart.addItem(self.bar_item)

#         chart_layout.addWidget(self.chart)
#         layout.addWidget(self.chart_card)

#         self.update_weekly_data()

#     def make_card(self, title, value):
#         frame = QFrame()
#         frame.setObjectName("SummaryCard")
#         frame.setMinimumHeight(120)

#         v = QVBoxLayout(frame)
#         v.setContentsMargins(20, 20, 20, 20)

#         label_title = QLabel(title.upper())
#         label_title.setStyleSheet("font-size: 10px; font-weight: 800; letter-spacing: 1.2px; opacity: 0.6;")

#         label_value = QLabel(value)
#         label_value.setObjectName("CardValue")
#         label_value.setStyleSheet("font-size: 26px; font-weight: 800; margin-top: 5px;")

#         v.addWidget(label_title)
#         v.addWidget(label_value)
#         v.addStretch()

#         frame.value_label = label_value
#         return frame

#     def update_weekly_data(self):
#         try:
#             engine = WeeklySummaryEngine()
#             summary = engine.generate_this_week()

#             total = summary.get("total_focus", 0)
#             avg = total / 7 if total > 0 else 0

#             week_start_str = summary.get("week_start")
#             if not week_start_str: return
            
#             week_start = datetime.strptime(week_start_str, "%Y-%m-%d")
#             daily_values = []
#             day_labels = []

#             for i in range(7):
#                 current_date = week_start + timedelta(days=i)
#                 day_labels.append((i, current_date.strftime("%a")))
                
#                 row = engine.storage.get_daily_summary(current_date.strftime("%Y-%m-%d"))
#                 daily_values.append(row[1] if row else 0)

#             # Update Chart Unit Labels
#             self.chart.getAxis("bottom").setTicks([day_labels])

#             # Premium Styling for Bar Graph
#             x = list(range(7))
#             self.bar_item.setOpts(x=x, height=daily_values, brush=QColor(self.accent), pen=None)
            
#             # Goal logic: Auto-scale Y axis
#             y_max = max(daily_values) if max(daily_values) > 0 else 100
#             self.chart.setYRange(0, y_max * 1.2)

#             # Analytics logic
#             if max(daily_values) > 0:
#                 best_idx = daily_values.index(max(daily_values))
#                 best_day = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][best_idx]
#             else:
#                 best_day = "N/A"

#             # Dynamic Trend Analysis
#             if len(daily_values) >= 7:
#                 # Compare today vs start of week
#                 if daily_values[-1] > daily_values[0]:
#                     trend = "↗ Growth"
#                     color = "#2ECC71"
#                 elif daily_values[-1] < daily_values[0]:
#                     trend = "↘ Decline"
#                     color = "#E74C3C"
#                 else:
#                     trend = "→ Stable"
#                     color = "#95A5A6"
#                 self.card_trend.value_label.setText(trend)
#                 self.card_trend.value_label.setStyleSheet(f"font-size: 22px; font-weight: 800; color: {color};")

#             # Update Main Values
#             self.card_avg.value_label.setText(f"{int(avg)}m")
#             self.card_total.value_label.setText(f"{int(total):,}m")
#             self.card_best.value_label.setText(best_day)

#         except Exception as e:
#             print(f"Weekly Sync Error: {e}")

















# # This is premium 

# from datetime import datetime, timedelta
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QColor
# import pyqtgraph as pg

# # --- ENGINE IMPORT ---
# try:
#     from core.weekly_summary_engine import WeeklySummaryEngine
# except ImportError:
#     # Mock engine for standalone testing or missing files
#     class WeeklySummaryEngine:
#         def __init__(self): 
#             self.storage = type('obj', (object,), {'get_daily_summary': lambda s, d: [0, 45]})()
#         def generate_this_week(self): 
#             return {
#                 "total_focus": 320, 
#                 "week_start": datetime.now().strftime("%Y-%m-%d"),
#                 "deep_work": 150, "deep_reading": 100, "focused_interaction": 70
#             }

# class WeeklyAnalyticsPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("WeeklyAnalyticsPage")

#         # 1. THEME DETECTION
#         current_bg = self.palette().window().color().name().upper()
#         # Executive accent colors matched to your specific UI modes
#         if current_bg == "#F2F6FC":
#             self.accent = "#0057D9"
#         elif current_bg == "#161618":
#             self.accent = "#4DA3FF"
#         else:
#             self.accent = "#0057D9"

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(25)

#         # --- HEADER ---
#         header = QHBoxLayout()
#         title_v = QVBoxLayout()
#         title = QLabel("Weekly Performance")
#         title.setObjectName("PageTitle")
        
#         subtitle = QLabel("AI-Powered Behavioral Insights")
#         subtitle.setStyleSheet("font-size: 12px; opacity: 0.6; font-weight: 400; letter-spacing: 0.5px;")
        
#         title_v.addWidget(title)
#         title_v.addWidget(subtitle)
#         header.addLayout(title_v)
#         header.addStretch()
#         layout.addLayout(header)

#         # --- SUMMARY CARDS ---
#         self.summary_container = QHBoxLayout()
#         self.summary_container.setSpacing(15)
#         layout.addLayout(self.summary_container)

#         self.card_avg = self.make_card("Daily Average", "0m")
#         self.card_total = self.make_card("Week Total", "0m")
#         self.card_best = self.make_card("Peak Day", "-")
#         self.card_trend = self.make_card("7D Trend", "-")

#         self.summary_container.addWidget(self.card_avg)
#         self.summary_container.addWidget(self.card_total)
#         self.summary_container.addWidget(self.card_best)
#         self.summary_container.addWidget(self.card_trend)

#         # --- PREMIUM CHART SECTION (LOCKED) ---
#         self.chart_card = QFrame()
#         self.chart_card.setObjectName("FluentCard")
#         # Subtle background for the chart area
#         self.chart_card.setStyleSheet("background-color: rgba(255,255,255,0.02); border-radius: 12px;")
#         chart_layout = QVBoxLayout(self.chart_card)
#         chart_layout.setContentsMargins(20, 20, 20, 20)
        
#         self.chart = pg.PlotWidget()
#         self.chart.setBackground(None)
#         self.chart.setAntialiasing(True)
        
#         # 2. STRIP SCIENTIFIC UI ELEMENTS (The "A" Button Fix)
#         self.chart.hideButtons()             # Removes the 'A' button
#         self.chart.setMenuEnabled(False)      # Disables right-click context menu
        
#         # Lock the ViewBox completely
#         vb = self.chart.getViewBox()
#         vb.setMouseEnabled(x=False, y=False) # Disables zooming/panning
#         vb.setMenuEnabled(False)             # Redundant but safe for older versions
        
#         # Style the background grid
#         self.chart.showGrid(x=False, y=True, alpha=0.1)
        
#         # Style X-Axis for Apple Compliance
#         ax_bottom = self.chart.getAxis("bottom")
#         ax_bottom.setPen(QColor(150, 150, 150, 50))
#         ax_bottom.setTextPen(QColor(150, 150, 150, 180))
        
#         # Hide Y-Axis for cleaner look
#         self.chart.getAxis("left").setVisible(False)

#         self.bar_item = pg.BarGraphItem(x=[], height=[], width=0.6)
#         self.chart.addItem(self.bar_item)

#         chart_layout.addWidget(self.chart)
#         layout.addWidget(self.chart_card)

#         self.update_weekly_data()

#     def make_card(self, title, value):
#         frame = QFrame()
#         frame.setObjectName("SummaryCard")
#         frame.setMinimumHeight(120)

#         v = QVBoxLayout(frame)
#         v.setContentsMargins(20, 20, 20, 20)

#         label_title = QLabel(title.upper())
#         label_title.setStyleSheet("font-size: 10px; font-weight: 800; letter-spacing: 1.2px; opacity: 0.6;")

#         label_value = QLabel(value)
#         label_value.setObjectName("CardValue")
#         label_value.setStyleSheet("font-size: 26px; font-weight: 800; margin-top: 5px;")

#         v.addWidget(label_title)
#         v.addWidget(label_value)
#         v.addStretch()

#         frame.value_label = label_value
#         return frame

#     def update_weekly_data(self):
#         try:
#             engine = WeeklySummaryEngine()
#             summary = engine.generate_this_week()

#             total = summary.get("total_focus", 0)
#             avg = total / 7 if total > 0 else 0

#             week_start_str = summary.get("week_start")
#             if not week_start_str: return
            
#             week_start = datetime.strptime(week_start_str, "%Y-%m-%d")
#             daily_values = []
#             day_labels = []

#             for i in range(7):
#                 current_date = week_start + timedelta(days=i)
#                 day_labels.append((i, current_date.strftime("%a")))
                
#                 row = engine.storage.get_daily_summary(current_date.strftime("%Y-%m-%d"))
#                 daily_values.append(row[1] if row else 0)

#             # Update Axis Labels
#             self.chart.getAxis("bottom").setTicks([day_labels])

#             # Update Bars with Accent Color
#             x = list(range(7))
#             self.bar_item.setOpts(x=x, height=daily_values, brush=QColor(self.accent), pen=None)
            
#             # Auto-Scale Y Axis for data visibility
#             y_max = max(daily_values) if max(daily_values) > 0 else 100
#             self.chart.setYRange(0, y_max * 1.2)

#             # Peak Day logic
#             if max(daily_values) > 0:
#                 best_idx = daily_values.index(max(daily_values))
#                 best_day = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][best_idx]
#             else:
#                 best_day = "N/A"

#             # Trend Coloring Logic
#             if daily_values[-1] > daily_values[0]:
#                 trend = "↗ Growth"
#                 color = "#2ECC71"
#             elif daily_values[-1] < daily_values[0]:
#                 trend = "↘ Decline"
#                 color = "#E74C3C"
#             else:
#                 trend = "→ Stable"
#                 color = "#95A5A6"
            
#             self.card_trend.value_label.setText(trend)
#             self.card_trend.value_label.setStyleSheet(f"font-size: 22px; font-weight: 800; color: {color};")

#             # Final Value Updates
#             self.card_avg.value_label.setText(f"{int(avg)}m")
#             self.card_total.value_label.setText(f"{int(total):,}m")
#             self.card_best.value_label.setText(best_day)

#         except Exception as e:
#             print(f"Weekly Sync Error: {e}")



















# # Only added hover to the premium

# from datetime import datetime, timedelta
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QColor, QBrush
# import pyqtgraph as pg

# # --- ENGINE IMPORT ---
# try:
#     from core.weekly_summary_engine import WeeklySummaryEngine
# except ImportError:
#     # Mock engine for standalone testing
#     class WeeklySummaryEngine:
#         def __init__(self): 
#             self.storage = type('obj', (object,), {'get_daily_summary': lambda s, d: [0, 45]})()
#         def generate_this_week(self): 
#             return {
#                 "total_focus": 320, 
#                 "week_start": datetime.now().strftime("%Y-%m-%d"),
#                 "deep_work": 150, "deep_reading": 100, "focused_interaction": 70
#             }

# class WeeklyAnalyticsPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("WeeklyAnalyticsPage")

#         # 1. THEME DETECTION
#         current_bg = self.palette().window().color().name().upper()
#         if current_bg == "#F2F6FC":
#             self.accent = "#0057D9"
#         elif current_bg == "#161618":
#             self.accent = "#4DA3FF"
#         else:
#             self.accent = "#0057D9"

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(25)

#         # --- HEADER ---
#         header = QHBoxLayout()
#         title_v = QVBoxLayout()
#         title = QLabel("Weekly Performance")
#         title.setObjectName("PageTitle")
        
#         subtitle = QLabel("AI-Powered Behavioral Insights")
#         subtitle.setStyleSheet("font-size: 12px; opacity: 0.6; font-weight: 400; letter-spacing: 0.5px;")
        
#         title_v.addWidget(title)
#         title_v.addWidget(subtitle)
#         header.addLayout(title_v)
#         header.addStretch()
#         layout.addLayout(header)

#         # --- SUMMARY CARDS ---
#         self.summary_container = QHBoxLayout()
#         self.summary_container.setSpacing(15)
#         layout.addLayout(self.summary_container)

#         self.card_avg = self.make_card("Daily Average", "0m")
#         self.card_total = self.make_card("Week Total", "0m")
#         self.card_best = self.make_card("Peak Day", "-")
#         self.card_trend = self.make_card("7D Trend", "-")

#         self.summary_container.addWidget(self.card_avg)
#         self.summary_container.addWidget(self.card_total)
#         self.summary_container.addWidget(self.card_best)
#         self.summary_container.addWidget(self.card_trend)

#         # --- PREMIUM CHART SECTION (LOCKED & HOVERABLE) ---
#         self.chart_card = QFrame()
#         self.chart_card.setObjectName("FluentCard")
#         self.chart_card.setStyleSheet("background-color: rgba(255,255,255,0.02); border-radius: 12px;")
#         chart_layout = QVBoxLayout(self.chart_card)
#         chart_layout.setContentsMargins(20, 20, 20, 20)
        
#         self.chart = pg.PlotWidget()
#         self.chart.setBackground(None)
#         self.chart.setAntialiasing(True)
        
#         # Strip Scientific UI
#         self.chart.hideButtons()
#         self.chart.setMenuEnabled(False)
        
#         vb = self.chart.getViewBox()
#         vb.setMouseEnabled(x=False, y=False)
#         vb.setMenuEnabled(False)
        
#         self.chart.showGrid(x=False, y=True, alpha=0.1)
        
#         # Style X-Axis
#         ax_bottom = self.chart.getAxis("bottom")
#         ax_bottom.setPen(QColor(150, 150, 150, 50))
#         ax_bottom.setTextPen(QColor(150, 150, 150, 180))
#         self.chart.getAxis("left").setVisible(False)

#         # 2. CREATE HOVERABLE BAR ITEM
#         # hoverBrush uses a lighter version of the accent for that 'glow' effect
#         glow_color = QColor(self.accent).lighter(130)
#         self.bar_item = pg.BarGraphItem(
#             x=[], 
#             height=[], 
#             width=0.6, 
#             hoverable=True, 
#             hoverBrush=QBrush(glow_color)
#         )
#         self.chart.addItem(self.bar_item)

#         chart_layout.addWidget(self.chart)
#         layout.addWidget(self.chart_card)

#         self.update_weekly_data()

#     def make_card(self, title, value):
#         frame = QFrame()
#         frame.setObjectName("SummaryCard")
#         frame.setMinimumHeight(120)

#         v = QVBoxLayout(frame)
#         v.setContentsMargins(20, 20, 20, 20)

#         label_title = QLabel(title.upper())
#         label_title.setStyleSheet("font-size: 10px; font-weight: 800; letter-spacing: 1.2px; opacity: 0.6;")

#         label_value = QLabel(value)
#         label_value.setObjectName("CardValue")
#         label_value.setStyleSheet("font-size: 26px; font-weight: 800; margin-top: 5px;")

#         v.addWidget(label_title)
#         v.addWidget(label_value)
#         v.addStretch()

#         frame.value_label = label_value
#         return frame

#     def update_weekly_data(self):
#         try:
#             engine = WeeklySummaryEngine()
#             summary = engine.generate_this_week()

#             total = summary.get("total_focus", 0)
#             avg = total / 7 if total > 0 else 0

#             week_start_str = summary.get("week_start")
#             if not week_start_str: return
            
#             week_start = datetime.strptime(week_start_str, "%Y-%m-%d")
#             daily_values = []
#             day_labels = []

#             for i in range(7):
#                 current_date = week_start + timedelta(days=i)
#                 day_labels.append((i, current_date.strftime("%a")))
                
#                 row = engine.storage.get_daily_summary(current_date.strftime("%Y-%m-%d"))
#                 daily_values.append(row[1] if row else 0)

#             self.chart.getAxis("bottom").setTicks([day_labels])

#             # Update Bars with Accent and Hover Glow
#             x = list(range(7))
#             self.bar_item.setOpts(
#                 x=x, 
#                 height=daily_values, 
#                 brush=QColor(self.accent), 
#                 pen=None
#             )
            
#             y_max = max(daily_values) if max(daily_values) > 0 else 100
#             self.chart.setYRange(0, y_max * 1.2)

#             if max(daily_values) > 0:
#                 best_idx = daily_values.index(max(daily_values))
#                 best_day = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][best_idx]
#             else:
#                 best_day = "N/A"

#             # Trend Logic
#             if daily_values[-1] > daily_values[0]:
#                 trend = "↗ Growth"
#                 color = "#2ECC71"
#             elif daily_values[-1] < daily_values[0]:
#                 trend = "↘ Decline"
#                 color = "#E74C3C"
#             else:
#                 trend = "→ Stable"
#                 color = "#95A5A6"
            
#             self.card_trend.value_label.setText(trend)
#             self.card_trend.value_label.setStyleSheet(f"font-size: 22px; font-weight: 800; color: {color};")

#             self.card_avg.value_label.setText(f"{int(avg)}m")
#             self.card_total.value_label.setText(f"{int(total):,}m")
#             self.card_best.value_label.setText(best_day)

#         except Exception as e:
#             print(f"Weekly Sync Error: {e}")















from datetime import datetime, timedelta
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QBrush
import pyqtgraph as pg

# --- ENGINE IMPORT ---
try:
    from core.weekly_summary_engine import WeeklySummaryEngine
except ImportError:
    class WeeklySummaryEngine:
        def __init__(self): 
            self.storage = type('obj', (object,), {'get_daily_summary': lambda s, d: [0, 45]})()
        def generate_this_week(self): 
            return {
                "total_focus": 320, 
                "week_start": datetime.now().strftime("%Y-%m-%d"),
                "deep_work": 150, "deep_reading": 100, "focused_interaction": 70
            }

class WeeklyAnalyticsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("WeeklyAnalyticsPage")

        # 1. THEME DETECTION
        current_bg = self.palette().window().color().name().upper()
        if current_bg == "#F2F6FC":
            self.accent = "#0057D9"
            self.tip_bg = "#FFFFFF"
            self.tip_text = "#1A1A1A"
        elif current_bg == "#161618":
            self.accent = "#4DA3FF"
            self.tip_bg = "#2D2D30"
            self.tip_text = "#E4E7F2"
        else:
            self.accent = "#0057D9"
            self.tip_bg = "#FFFFFF"
            self.tip_text = "#1A1A1A"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # --- HEADER ---
        header = QHBoxLayout()
        title_v = QVBoxLayout()
        title = QLabel("Weekly Performance")
        title.setObjectName("PageTitle")
        subtitle = QLabel("AI-Powered Behavioral Insights")
        subtitle.setStyleSheet("font-size: 12px; opacity: 0.6; font-weight: 400; margin-left: 20px;")
        title_v.addWidget(title)
        title_v.addWidget(subtitle)
        header.addLayout(title_v)
        header.addStretch()
        layout.addLayout(header)

        # --- SUMMARY CARDS ---
        self.summary_container = QHBoxLayout()
        self.summary_container.setSpacing(15)
        layout.addLayout(self.summary_container)

        self.card_avg = self.make_card("Daily Average", "0m")
        self.card_total = self.make_card("Week Total", "0m")
        self.card_best = self.make_card("Peak Day", "-")
        self.card_trend = self.make_card("7D Trend", "-")

        for card in [self.card_avg, self.card_total, self.card_best, self.card_trend]:
            self.summary_container.addWidget(card)

        # --- PREMIUM CHART SECTION ---
        self.chart_card = QFrame()
        self.chart_card.setObjectName("FluentCard")
        self.chart_card.setStyleSheet("background-color: rgba(255,255,255,0.02); border-radius: 12px;")
        chart_layout = QVBoxLayout(self.chart_card)
        chart_layout.setContentsMargins(20, 20, 20, 20)
        
        self.chart = pg.PlotWidget()
        self.chart.setBackground(None)
        self.chart.setAntialiasing(True)
        self.chart.hideButtons()
        self.chart.setMenuEnabled(False)
        
        vb = self.chart.getViewBox()
        vb.setMouseEnabled(x=False, y=False)
        self.chart.showGrid(x=False, y=True, alpha=0.1)
        
        ax_bottom = self.chart.getAxis("bottom")
        ax_bottom.setPen(QColor(150, 150, 150, 50))
        ax_bottom.setTextPen(QColor(150, 150, 150, 180))
        self.chart.getAxis("left").setVisible(False)

        # 2. PREMIUM TOOLTIP OVERLAY
        self.tooltip = pg.TextItem(text="", color=self.tip_text, anchor=(0.5, 1.2))
        self.tooltip.setParentItem(vb)
        self.tooltip.hide()
        
        # Tooltip Background Styling
        self.tooltip_bg = pg.ScatterPlotItem(size=1, pen=None, brush=pg.mkBrush(self.tip_bg))
        
        # 3. HOVERABLE BARS
        glow_color = QColor(self.accent).lighter(130)
        self.bar_item = pg.BarGraphItem(
            x=[], height=[], width=0.6, 
            hoverable=True, hoverBrush=QBrush(glow_color)
        )
        self.chart.addItem(self.bar_item)

        # Connect Mouse Events for Tooltip
        self.chart.scene().sigMouseMoved.connect(self.on_mouse_moved)

        chart_layout.addWidget(self.chart)
        layout.addWidget(self.chart_card)

        self.update_weekly_data()

    def make_card(self, title, value):
        frame = QFrame()
        frame.setObjectName("SummaryCard")
        frame.setMinimumHeight(120)
        v = QVBoxLayout(frame)
        v.setContentsMargins(20, 20, 20, 20)
        label_title = QLabel(title.upper())
        label_title.setStyleSheet("font-size: 10px; font-weight: 800; letter-spacing: 1.2px; opacity: 0.6;")
        label_value = QLabel(value)
        label_value.setObjectName("CardValue")
        label_value.setStyleSheet("font-size: 26px; font-weight: 800; margin-top: 5px;")
        v.addWidget(label_title)
        v.addWidget(label_value)
        v.addStretch()
        frame.value_label = label_value
        return frame

    def on_mouse_moved(self, pos):
        """Premium Tooltip Logic"""
        if self.chart.sceneBoundingRect().contains(pos):
            mouse_point = self.chart.getViewBox().mapSceneToView(pos)
            x_idx = round(mouse_point.x())
            
            # Check if mouse is over a valid bar (0-6)
            if 0 <= x_idx < len(self.daily_values):
                val = self.daily_values[x_idx]
                day = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][x_idx]
                
                self.tooltip.setText(f"{day}: {int(val)}m")
                self.tooltip.setPos(x_idx, val)
                
                # Dynamic visibility based on proximity
                if abs(mouse_point.x() - x_idx) < 0.3:
                    self.tooltip.show()
                    return
        self.tooltip.hide()

    def update_weekly_data(self):
        try:
            engine = WeeklySummaryEngine()
            summary = engine.generate_this_week()
            total = summary.get("total_focus", 0)
            avg = total / 7 if total > 0 else 0
            week_start_str = summary.get("week_start")
            if not week_start_str: return
            
            week_start = datetime.strptime(week_start_str, "%Y-%m-%d")
            self.daily_values = [] # Stored as class attribute for tooltip
            day_labels = []

            for i in range(7):
                current_date = week_start + timedelta(days=i)
                day_labels.append((i, current_date.strftime("%a")))
                row = engine.storage.get_daily_summary(current_date.strftime("%Y-%m-%d"))
                self.daily_values.append(row[1] if row else 0)

            self.chart.getAxis("bottom").setTicks([day_labels])
            self.bar_item.setOpts(x=list(range(7)), height=self.daily_values, brush=QColor(self.accent), pen=None)
            
            y_max = max(self.daily_values) if max(self.daily_values) > 0 else 100
            self.chart.setYRange(0, y_max * 1.3) # Space for tooltip

            # Final Card Updates
            if max(self.daily_values) > 0:
                best_idx = self.daily_values.index(max(self.daily_values))
                best_day = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][best_idx]
            else:
                best_day = "N/A"

            # Trend Coloring Logic
            if self.daily_values[-1] > self.daily_values[0]:
                trend, color = "↗ Growth", "#2ECC71"
            elif self.daily_values[-1] < self.daily_values[0]:
                trend, color = "↘ Decline", "#E74C3C"
            else:
                trend, color = "→ Stable", "#95A5A6"
            
            self.card_trend.value_label.setText(trend)
            self.card_trend.value_label.setStyleSheet(f"font-size: 22px; font-weight: 800; color: {color};")
            self.card_avg.value_label.setText(f"{int(avg)}m")
            self.card_total.value_label.setText(f"{int(total):,}m")
            self.card_best.value_label.setText(best_day)

        except Exception as e:
            print(f"Weekly Sync Error: {e}")