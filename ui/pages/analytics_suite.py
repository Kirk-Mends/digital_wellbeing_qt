


# 5
# # Upgrade design

# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QFrame, QSizePolicy, QScrollArea
# )
# from PySide6.QtCore import Qt
# import pyqtgraph as pg

# from core.analytics_engine import AnalyticsEngine


# # -----------------------------
# # Color palette (Apple-style vibrant)
# # -----------------------------
# class AnalyticsColors:
#     BEHAVIOR = "#0A84FF"   # blue
#     FATIGUE = "#FF9F0A"    # orange
#     BREAK = "#30D158"      # green
#     SUPPRESSION = "#FF453A"  # red
#     INSIGHT = "#BF5AF2"    # purple
#     GRID = (255, 255, 255, 40)


# CARD_HEIGHT = 320  # fixed height for chart cards


# # -----------------------------
# # Generic card container
# # -----------------------------
# class AnalyticsCard(QFrame):
#     """
#     Simple Fluent-style card with a title and content area.
#     Used for both charts and text.
#     """
#     def __init__(self, title: str):
#         super().__init__()
#         self.setObjectName("AnalyticsCard")
#         self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#         self.setMinimumHeight(CARD_HEIGHT)

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(14, 14, 14, 14)
#         layout.setSpacing(8)

#         self.title_label = QLabel(title)
#         self.title_label.setObjectName("AnalyticsCardTitle")
#         layout.addWidget(self.title_label)

#         self.body_layout = QVBoxLayout()
#         self.body_layout.setContentsMargins(0, 0, 0, 0)
#         self.body_layout.setSpacing(4)
#         layout.addLayout(self.body_layout)


# # -----------------------------
# # Chart card wrapper
# # -----------------------------
# class ChartCard(AnalyticsCard):
#     """
#     Card that hosts a PyQtGraph PlotWidget with consistent styling.
#     """
#     def __init__(self, title: str, color: str):
#         super().__init__(title)
#         self.color = color

#         self.plot = pg.PlotWidget()
#         self.plot.setBackground(None)
#         self.plot.showGrid(x=False, y=True, alpha=0.15)
#         self.plot.getAxis("left").setVisible(False)
#         self.plot.getAxis("bottom").setVisible(False)
#         self.plot.setMenuEnabled(False)
#         self.plot.setMouseEnabled(x=False, y=False)
#         self.plot.setClipToView(True)
#         self.plot.setDownsampling(mode="peak")  # none
#         self.plot.setAntialiasing(True)

#         # Light grid color
#         self.plot.getPlotItem().getViewBox().setBorder(None)

#         self.body_layout.addWidget(self.plot)

#     def clear(self):
#         self.plot.clear()


# # -----------------------------
# # Two-column layout helper
# # -----------------------------
# class TwoColumnLayout(QVBoxLayout):
#     """
#     Simple helper to place cards in two columns with vertical flow.
#     """
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setContentsMargins(10, 10, 10, 10)
#         self.setSpacing(10)

#         self.row_layout = None
#         self._items_in_row = 0

#     def add_card(self, card: QWidget):
#         if self.row_layout is None or self._items_in_row >= 2:
#             self.row_layout = QHBoxLayout()
#             self.row_layout.setSpacing(10)
#             self.addLayout(self.row_layout)
#             self._items_in_row = 0

#         self.row_layout.addWidget(card)
#         self._items_in_row += 1


# # -----------------------------
# # Main Analytics Suite Page
# # -----------------------------
# class AnalyticsSuitePage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("AnalyticsSuitePage")

#         self.engine = AnalyticsEngine()

#         root_layout = QVBoxLayout(self)
#         root_layout.setContentsMargins(20, 20, 20, 20)
#         root_layout.setSpacing(20)

#         title = QLabel("Analytics")
#         title.setObjectName("PageTitle")
#         root_layout.addWidget(title)

#         # Tab widget
#         self.tabs = QTabWidget()
#         self.tabs.setObjectName("AnalyticsTabs")
#         root_layout.addWidget(self.tabs)

#         # Tabs
#         self._init_behavior_tab()
#         self._init_fatigue_tab()
#         self._init_break_tab()
#         self._init_suppression_tab()
#         self._init_time_of_day_tab()
#         self._init_weekly_tab()
#         self._init_monthly_tab()
#         self._init_insights_tab()

#         # Initial refresh
#         self.refresh_all()

#     # -------------------------
#     # Tab helpers
#     # -------------------------
#     def _create_scrollable_tab(self):
#         """
#         Creates a scrollable area with a two-column layout inside.
#         Returns (container_widget, two_column_layout).
#         """
#         container = QWidget()
#         outer_layout = QVBoxLayout(container)
#         outer_layout.setContentsMargins(0, 0, 0, 0)
#         outer_layout.setSpacing(0)

#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         scroll.setFrameShape(QFrame.NoFrame)

#         inner = QWidget()
#         two_col = TwoColumnLayout(inner)
#         scroll.setWidget(inner)

#         outer_layout.addWidget(scroll)
#         return container, two_col

#     # -------------------------
#     # BEHAVIOR TAB
#     # -------------------------
#     def _init_behavior_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.behavior_layout = layout

#         # Behavior distribution
#         self.card_behavior_dist = ChartCard("Behavior Distribution", AnalyticsColors.BEHAVIOR)
#         self.behavior_layout.add_card(self.card_behavior_dist)

#         # Behavior timeline
#         self.card_behavior_timeline = ChartCard("Behavior Timeline", AnalyticsColors.BEHAVIOR)
#         self.behavior_layout.add_card(self.card_behavior_timeline)

#         # Behavior by time of day
#         self.card_behavior_by_hour = ChartCard("Behavior by Time of Day", AnalyticsColors.BEHAVIOR)
#         self.behavior_layout.add_card(self.card_behavior_by_hour)

#         # Longest streak (text card)
#         self.card_behavior_streak = AnalyticsCard("Longest Focus Streak")
#         self.behavior_streak_label = QLabel("No data yet.")
#         self.behavior_streak_label.setObjectName("AnalyticsText")
#         self.behavior_streak_label.setWordWrap(True)
#         self.card_behavior_streak.body_layout.addWidget(self.behavior_streak_label)
#         self.behavior_layout.add_card(self.card_behavior_streak)

#         self.tabs.addTab(w, "Behavior")

#     def _refresh_behavior_tab(self):
#         # Distribution
#         dist = self.engine.behavior_distribution()
#         self.card_behavior_dist.clear()
#         if dist:
#             behaviors = list(dist.keys())
#             values = list(dist.values())
#             x = range(len(behaviors))
#             bg = pg.BarGraphItem(
#                 x=list(x),
#                 height=values,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_behavior_dist.plot.addItem(bg)
#             ax = self.card_behavior_dist.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)

#         # Timeline (simple line by index for now)
#         timeline = self.engine.behavior_timeline()
#         self.card_behavior_timeline.clear()
#         times = timeline.get("times", [])
#         behaviors = timeline.get("behaviors", [])
#         if times and behaviors:
#             # Map behaviors to numeric categories for a simple stepped line
#             unique_behaviors = list(dict.fromkeys(behaviors))
#             mapping = {b: i for i, b in enumerate(unique_behaviors)}
#             y = [mapping[b] for b in behaviors]
#             curve = self.card_behavior_timeline.plot.plot(
#                 list(range(len(times))), y,
#                 pen=pg.mkPen(AnalyticsColors.BEHAVIOR, width=2)
#             )
#             self.card_behavior_timeline.plot.getAxis("bottom").setVisible(False)

#         # Behavior by hour (simple bar)
#         by_hour = self.engine.behavior_by_hour()
#         self.card_behavior_by_hour.clear()
#         if by_hour:
#             hours = sorted(by_hour.keys())
#             vals = [sum(by_hour[h].values()) for h in hours]
#             x = list(range(len(hours)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_behavior_by_hour.plot.addItem(bg)
#             labels = [f"{h:02d}:00" for h in hours]
#             ax = self.card_behavior_by_hour.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         # Longest streak
#         streak = self.engine.longest_behavior_streak()
#         if streak:
#             self.behavior_streak_label.setText(
#                 f"Longest streak: {streak['behavior']} for {streak['minutes']:.0f} minutes."
#             )
#         else:
#             self.behavior_streak_label.setText("No behavior streak data available yet.")

#     # -------------------------
#     # FATIGUE TAB
#     # -------------------------
#     def _init_fatigue_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.fatigue_layout = layout

#         self.card_fatigue_trend = ChartCard("Fatigue Trend", AnalyticsColors.FATIGUE)
#         self.fatigue_layout.add_card(self.card_fatigue_trend)

#         self.card_fatigue_by_behavior = ChartCard("Fatigue by Behavior", AnalyticsColors.FATIGUE)
#         self.fatigue_layout.add_card(self.card_fatigue_by_behavior)

#         self.card_fatigue_recovery = ChartCard("Fatigue Recovery After Breaks", AnalyticsColors.FATIGUE)
#         self.fatigue_layout.add_card(self.card_fatigue_recovery)

#         self.card_fatigue_peak = AnalyticsCard("Highest Fatigue Moment")
#         self.fatigue_peak_label = QLabel("No data yet.")
#         self.fatigue_peak_label.setObjectName("AnalyticsText")
#         self.fatigue_peak_label.setWordWrap(True)
#         self.card_fatigue_peak.body_layout.addWidget(self.fatigue_peak_label)
#         self.fatigue_layout.add_card(self.card_fatigue_peak)

#         self.tabs.addTab(w, "Fatigue")

#     def _refresh_fatigue_tab(self):
#         # Trend
#         trend = self.engine.fatigue_trend()
#         self.card_fatigue_trend.clear()
#         times = trend.get("times", [])
#         vals = trend.get("fatigue", [])
#         if times and vals:
#             self.card_fatigue_trend.plot.plot(
#                 list(range(len(times))), vals,
#                 pen=pg.mkPen(AnalyticsColors.FATIGUE, width=2)
#             )
#             self.card_fatigue_trend.plot.setYRange(0, 100)

#         # By behavior
#         by_behavior = self.engine.fatigue_by_behavior()
#         self.card_fatigue_by_behavior.clear()
#         if by_behavior:
#             behaviors = list(by_behavior.keys())
#             vals = list(by_behavior.values())
#             x = list(range(len(behaviors)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.FATIGUE
#             )
#             self.card_fatigue_by_behavior.plot.addItem(bg)
#             ax = self.card_fatigue_by_behavior.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)
#             self.card_fatigue_by_behavior.plot.setYRange(0, 100)

#         # Recovery
#         rec = self.engine.fatigue_recovery_after_breaks()
#         self.card_fatigue_recovery.clear()
#         rt = rec.get("times", [])
#         rv = rec.get("fatigue", [])
#         if rt and rv:
#             self.card_fatigue_recovery.plot.plot(
#                 list(range(len(rt))), rv,
#                 pen=pg.mkPen(AnalyticsColors.FATIGUE, width=2)
#             )
#             self.card_fatigue_recovery.plot.setYRange(0, 100)

#         # Peak
#         peak = self.engine.highest_fatigue_moment()
#         if peak:
#             self.fatigue_peak_label.setText(
#                 f"Highest fatigue: {peak['fatigue']:.0f}/100 at {peak['time']}."
#             )
#         else:
#             self.fatigue_peak_label.setText("No fatigue peak data available yet.")

#     # -------------------------
#     # BREAK TAB
#     # -------------------------
#     def _init_break_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.break_layout = layout

#         self.card_break_reasons = ChartCard("Break Reasons", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_reasons)

#         self.card_break_timing = ChartCard("Break Timing Quality", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_timing)

#         self.card_break_timeline = ChartCard("Break Events Timeline", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_timeline)

#         self.card_break_suppression = ChartCard("Break Suppression", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_suppression)

#         self.tabs.addTab(w, "Breaks")

#     def _refresh_break_tab(self):
#         # Reasons
#         reasons = self.engine.break_reasons()
#         self.card_break_reasons.clear()
#         if reasons:
#             labels = list(reasons.keys())
#             vals = list(reasons.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BREAK
#             )
#             self.card_break_reasons.plot.addItem(bg)
#             ax = self.card_break_reasons.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         # Timing quality
#         timing = self.engine.break_timing_quality()
#         self.card_break_timing.clear()
#         if timing:
#             labels = ["Early", "On Time", "Late"]
#             vals = [
#                 timing.get("early", 0),
#                 timing.get("on_time", 0),
#                 timing.get("late", 0),
#             ]
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BREAK
#             )
#             self.card_break_timing.plot.addItem(bg)
#             ax = self.card_break_timing.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         # Timeline
#         timeline = self.engine.break_events_timeline()
#         self.card_break_timeline.clear()
#         times = timeline.get("times", [])
#         if times:
#             x = list(range(len(times)))
#             y = [1] * len(times)
#             self.card_break_timeline.plot.plot(
#                 x, y,
#                 pen=None,
#                 symbol="o",
#                 symbolSize=6,
#                 symbolBrush=AnalyticsColors.BREAK
#             )
#             self.card_break_timeline.plot.getAxis("bottom").setVisible(False)
#             self.card_break_timeline.plot.getAxis("left").setVisible(False)

#         # Suppression
#         supp = self.engine.break_suppression_stats()
#         self.card_break_suppression.clear()
#         if supp:
#             labels = list(supp.keys())
#             vals = list(supp.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BREAK
#             )
#             self.card_break_suppression.plot.addItem(bg)
#             ax = self.card_break_suppression.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#     # -------------------------
#     # SUPPRESSION TAB
#     # -------------------------
#     def _init_suppression_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.supp_layout = layout

#         self.card_supp_counts = ChartCard("Suppression Counts", AnalyticsColors.SUPPRESSION)
#         self.supp_layout.add_card(self.card_supp_counts)

#         self.card_away_resets = AnalyticsCard("Away Resets")
#         self.away_resets_label = QLabel("No data yet.")
#         self.away_resets_label.setObjectName("AnalyticsText")
#         self.away_resets_label.setWordWrap(True)
#         self.card_away_resets.body_layout.addWidget(self.away_resets_label)
#         self.supp_layout.add_card(self.card_away_resets)

#         self.tabs.addTab(w, "Suppression")

#     def _refresh_suppression_tab(self):
#         counts = self.engine.suppression_counts()
#         self.card_supp_counts.clear()
#         if counts:
#             labels = list(counts.keys())
#             vals = list(counts.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.SUPPRESSION
#             )
#             self.card_supp_counts.plot.addItem(bg)
#             ax = self.card_supp_counts.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         away = self.engine.away_resets_count()
#         self.away_resets_label.setText(
#             f"Away-based resets: {away}."
#         )

#     # -------------------------
#     # TIME OF DAY TAB
#     # -------------------------
#     def _init_time_of_day_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.tod_layout = layout

#         self.card_behavior_heatmap = ChartCard("Behavior Heatmap", AnalyticsColors.BEHAVIOR)
#         self.tod_layout.add_card(self.card_behavior_heatmap)

#         self.card_fatigue_heatmap = ChartCard("Fatigue Heatmap", AnalyticsColors.FATIGUE)
#         self.tod_layout.add_card(self.card_fatigue_heatmap)

#         self.card_break_heatmap = ChartCard("Break Heatmap", AnalyticsColors.BREAK)
#         self.tod_layout.add_card(self.card_break_heatmap)

#         self.card_supp_heatmap = ChartCard("Suppression Heatmap", AnalyticsColors.SUPPRESSION)
#         self.tod_layout.add_card(self.card_supp_heatmap)

#         self.tabs.addTab(w, "Time of Day")

#     def _plot_simple_heatmap(self, card: ChartCard, data: dict, color: str):
#         """
#         Simple 1D heatmap: hour -> value, rendered as colored bars.
#         """
#         card.clear()
#         if not data:
#             return

#         hours = sorted(data.keys())
#         vals = [data[h] for h in hours]
#         x = list(range(len(hours)))
#         bg = pg.BarGraphItem(
#             x=x,
#             height=vals,
#             width=0.8,
#             brush=color
#         )
#         card.plot.addItem(bg)
#         labels = [f"{h:02d}:00" for h in hours]
#         ax = card.plot.getAxis("bottom")
#         ax.setTicks([list(zip(x, labels))])
#         ax.setVisible(True)

#     def _refresh_time_of_day_tab(self):
#         beh = self.engine.behavior_heatmap()
#         self._plot_simple_heatmap(self.card_behavior_heatmap, beh, AnalyticsColors.BEHAVIOR)

#         fat = self.engine.fatigue_heatmap()
#         self._plot_simple_heatmap(self.card_fatigue_heatmap, fat, AnalyticsColors.FATIGUE)

#         br = self.engine.break_heatmap()
#         self._plot_simple_heatmap(self.card_break_heatmap, br, AnalyticsColors.BREAK)

#         supp = self.engine.suppression_heatmap()
#         self._plot_simple_heatmap(self.card_supp_heatmap, supp, AnalyticsColors.SUPPRESSION)

#     # -------------------------
#     # WEEKLY TAB
#     # -------------------------
#     def _init_weekly_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.weekly_layout = layout

#         self.card_weekly_behavior = ChartCard("Weekly Behavior Distribution", AnalyticsColors.BEHAVIOR)
#         self.weekly_layout.add_card(self.card_weekly_behavior)

#         self.card_weekly_fatigue = ChartCard("Weekly Fatigue Trend", AnalyticsColors.FATIGUE)
#         self.weekly_layout.add_card(self.card_weekly_fatigue)

#         self.card_weekly_break_consistency = AnalyticsCard("Weekly Break Consistency")
#         self.weekly_break_label = QLabel("No data yet.")
#         self.weekly_break_label.setObjectName("AnalyticsText")
#         self.weekly_break_label.setWordWrap(True)
#         self.card_weekly_break_consistency.body_layout.addWidget(self.weekly_break_label)
#         self.weekly_layout.add_card(self.card_weekly_break_consistency)

#         self.card_weekly_suppression = ChartCard("Weekly Suppression", AnalyticsColors.SUPPRESSION)
#         self.weekly_layout.add_card(self.card_weekly_suppression)

#         self.tabs.addTab(w, "Weekly")

#     def _refresh_weekly_tab(self):
#         summary = self.engine.weekly_behavior_summary()
#         self.card_weekly_behavior.clear()
#         self.card_weekly_fatigue.clear()
#         self.card_weekly_suppression.clear()

#         if not summary:
#             self.weekly_break_label.setText("No weekly data available yet.")
#             return

#         # Behavior distribution
#         dist = summary.get("distribution", {})
#         if dist:
#             behaviors = list(dist.keys())
#             vals = list(dist.values())
#             x = list(range(len(behaviors)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_weekly_behavior.plot.addItem(bg)
#             ax = self.card_weekly_behavior.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)

#         # Fatigue trend
#         ft = summary.get("fatigue_trend", {})
#         days = ft.get("days", [])
#         fv = ft.get("fatigue", [])
#         if days and fv:
#             self.card_weekly_fatigue.plot.plot(
#                 list(range(len(days))), fv,
#                 pen=pg.mkPen(AnalyticsColors.FATIGUE, width=2)
#             )
#             self.card_weekly_fatigue.plot.setYRange(0, 100)

#         # Break consistency
#         cons = summary.get("break_consistency", None)
#         if cons is not None:
#             self.weekly_break_label.setText(
#                 f"Break consistency this week: {cons:.0f}/100."
#             )
#         else:
#             self.weekly_break_label.setText("No break consistency data for this week.")

#         # Suppression
#         supp = summary.get("suppression_counts", {})
#         if supp:
#             labels = list(supp.keys())
#             vals = list(supp.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.SUPPRESSION
#             )
#             self.card_weekly_suppression.plot.addItem(bg)
#             ax = self.card_weekly_suppression.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#     # -------------------------
#     # MONTHLY TAB
#     # -------------------------
#     def _init_monthly_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.monthly_layout = layout

#         self.card_monthly_behavior = ChartCard("Monthly Behavior Distribution", AnalyticsColors.BEHAVIOR)
#         self.monthly_layout.add_card(self.card_monthly_behavior)

#         self.card_monthly_fatigue = ChartCard("Monthly Fatigue Trend", AnalyticsColors.FATIGUE)
#         self.monthly_layout.add_card(self.card_monthly_fatigue)

#         self.card_monthly_break_consistency = AnalyticsCard("Monthly Break Consistency")
#         self.monthly_break_label = QLabel("No data yet.")
#         self.monthly_break_label.setObjectName("AnalyticsText")
#         self.monthly_break_label.setWordWrap(True)
#         self.card_monthly_break_consistency.body_layout.addWidget(self.monthly_break_label)
#         self.monthly_layout.add_card(self.card_monthly_break_consistency)

#         self.card_monthly_suppression = ChartCard("Monthly Suppression", AnalyticsColors.SUPPRESSION)
#         self.monthly_layout.add_card(self.card_monthly_suppression)

#         self.tabs.addTab(w, "Monthly")

#     def _refresh_monthly_tab(self):
#         summary = self.engine.monthly_behavior_summary()
#         self.card_monthly_behavior.clear()
#         self.card_monthly_fatigue.clear()
#         self.card_monthly_suppression.clear()

#         if not summary:
#             self.monthly_break_label.setText("No monthly data available yet.")
#             return

#         # Behavior distribution
#         dist = summary.get("distribution", {})
#         if dist:
#             behaviors = list(dist.keys())
#             vals = list(dist.values())
#             x = list(range(len(behaviors)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_monthly_behavior.plot.addItem(bg)
#             ax = self.card_monthly_behavior.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)

#         # Fatigue trend
#         ft = summary.get("fatigue_trend", {})
#         days = ft.get("days", [])
#         fv = ft.get("fatigue", [])
#         if days and fv:
#             self.card_monthly_fatigue.plot.plot(
#                 list(range(len(days))), fv,
#                 pen=pg.mkPen(AnalyticsColors.FATIGUE, width=2)
#             )
#             self.card_monthly_fatigue.plot.setYRange(0, 100)

#         # Break consistency
#         cons = summary.get("break_consistency", None)
#         if cons is not None:
#             self.monthly_break_label.setText(
#                 f"Break consistency this month: {cons:.0f}/100."
#             )
#         else:
#             self.monthly_break_label.setText("No break consistency data for this month.")

#         # Suppression
#         supp = summary.get("suppression_counts", {})
#         if supp:
#             labels = list(supp.keys())
#             vals = list(supp.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.SUPPRESSION
#             )
#             self.card_monthly_suppression.plot.addItem(bg)
#             ax = self.card_monthly_suppression.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#     # -------------------------
#     # INSIGHTS TAB
#     # -------------------------
#     def _init_insights_tab(self):
#         w = QWidget()
#         v = QVBoxLayout(w)
#         v.setContentsMargins(10, 10, 10, 10)
#         v.setSpacing(10)

#         self.insights_container = QVBoxLayout()
#         v.addLayout(self.insights_container)
#         v.addStretch()

#         self.tabs.addTab(w, "AI Insights")

#     def _refresh_insights_tab(self):
#         insights = self.engine.ai_insights()

#         # Clear old cards
#         while self.insights_container.count():
#             item = self.insights_container.takeAt(0)
#             if item.widget():
#                 item.widget().deleteLater()

#         # Add new cards
#         for text in insights:
#             card = QFrame()
#             card.setObjectName("InsightCard")
#             v = QVBoxLayout(card)
#             v.setContentsMargins(12, 12, 12, 12)

#             lbl = QLabel(text)
#             lbl.setObjectName("InsightText")
#             lbl.setWordWrap(True)
#             v.addWidget(lbl)

#             self.insights_container.addWidget(card)

#     # -------------------------
#     # GLOBAL REFRESH
#     # -------------------------
#     def refresh_all(self):
#         self._refresh_behavior_tab()
#         self._refresh_fatigue_tab()
#         self._refresh_break_tab()
#         self._refresh_suppression_tab()
#         self._refresh_time_of_day_tab()
#         self._refresh_weekly_tab()
#         self._refresh_monthly_tab()
#         self._refresh_insights_tab()

























# # Upgrade design

# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QFrame, QSizePolicy, QScrollArea
# )
# from PySide6.QtCore import Qt
# import pyqtgraph as pg

# from core.analytics_engine import AnalyticsEngine


# # ============================================================
# # GLOBAL RENDERING IMPROVEMENTS (smooth lines everywhere)
# # ============================================================
# #pg.setConfigOptions(useOpenGL=True)
# #pg.setConfigOptions(antialias=True)


# # -----------------------------
# # Color palette (Apple-style vibrant)
# # -----------------------------
# class AnalyticsColors:
#     BEHAVIOR = "#0A84FF"   # blue
#     FATIGUE = "#FF9F0A"    # orange
#     BREAK = "#30D158"      # green
#     SUPPRESSION = "#FF453A"  # red
#     INSIGHT = "#BF5AF2"    # purple
#     GRID = (255, 255, 255, 40)


# CARD_HEIGHT = 320  # fixed height for chart cards


# # -----------------------------
# # Generic card container
# # -----------------------------
# class AnalyticsCard(QFrame):
#     """
#     Simple Fluent-style card with a title and content area.
#     Used for both charts and text.
#     """
#     def __init__(self, title: str):
#         super().__init__()
#         self.setObjectName("AnalyticsCard")
#         self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#         self.setMinimumHeight(CARD_HEIGHT)

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(14, 14, 14, 14)
#         layout.setSpacing(8)

#         self.title_label = QLabel(title)
#         self.title_label.setObjectName("AnalyticsCardTitle")
#         layout.addWidget(self.title_label)

#         self.body_layout = QVBoxLayout()
#         self.body_layout.setContentsMargins(0, 0, 0, 0)
#         self.body_layout.setSpacing(4)
#         layout.addLayout(self.body_layout)


# # -----------------------------
# # Chart card wrapper
# # -----------------------------
# class ChartCard(AnalyticsCard):
#     """
#     Card that hosts a PyQtGraph PlotWidget with consistent styling.
#     """
#     def __init__(self, title: str, color: str):
#         super().__init__(title)
#         self.color = color

#         self.plot = pg.PlotWidget()
#         self.plot.setBackground(None)
#         self.plot.showGrid(x=False, y=True, alpha=0.15)
#         self.plot.getAxis("left").setVisible(False)
#         self.plot.getAxis("bottom").setVisible(False)
#         self.plot.setMenuEnabled(False)
#         self.plot.setMouseEnabled(x=False, y=False)
#         self.plot.setClipToView(True)

#         # Disable downsampling for smooth lines
#         self.plot.setDownsampling(mode=None)

#         # Light grid color
#         self.plot.getPlotItem().getViewBox().setBorder(None)

#         self.body_layout.addWidget(self.plot)

#     def smooth_pen(self):
#         """Return a smooth, anti-aliased pen."""
#         pen = pg.mkPen(self.color, width=2, cosmetic=True)
#         pen.setCapStyle(Qt.RoundCap)
#         pen.setJoinStyle(Qt.RoundJoin)
#         return pen

#     def clear(self):
#         self.plot.clear()


# # -----------------------------
# # Two-column layout helper
# # -----------------------------
# class TwoColumnLayout(QVBoxLayout):
#     """
#     Simple helper to place cards in two columns with vertical flow.
#     """
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setContentsMargins(10, 10, 10, 10)
#         self.setSpacing(10)

#         self.row_layout = None
#         self._items_in_row = 0

#     def add_card(self, card: QWidget):
#         if self.row_layout is None or self._items_in_row >= 2:
#             self.row_layout = QHBoxLayout()
#             self.row_layout.setSpacing(10)
#             self.addLayout(self.row_layout)
#             self._items_in_row = 0

#         self.row_layout.addWidget(card)
#         self._items_in_row += 1
# # -----------------------------
# # Main Analytics Suite Page
# # -----------------------------
# class AnalyticsSuitePage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("AnalyticsSuitePage")

#         self.engine = AnalyticsEngine()

#         root_layout = QVBoxLayout(self)
#         root_layout.setContentsMargins(20, 20, 20, 20)
#         root_layout.setSpacing(20)

#         title = QLabel("Analytics")
#         title.setObjectName("PageTitle")
#         root_layout.addWidget(title)

#         # Tab widget
#         self.tabs = QTabWidget()
#         self.tabs.setObjectName("AnalyticsTabs")
#         root_layout.addWidget(self.tabs)

#         # Tabs
#         self._init_behavior_tab()
#         self._init_fatigue_tab()
#         self._init_break_tab()
#         self._init_suppression_tab()
#         self._init_time_of_day_tab()
#         self._init_weekly_tab()
#         self._init_monthly_tab()
#         self._init_insights_tab()

#         # Initial refresh
#         self.refresh_all()

#     # -------------------------
#     # Tab helpers
#     # -------------------------
#     def _create_scrollable_tab(self):
#         """
#         Creates a scrollable area with a two-column layout inside.
#         Returns (container_widget, two_column_layout).
#         """
#         container = QWidget()
#         outer_layout = QVBoxLayout(container)
#         outer_layout.setContentsMargins(0, 0, 0, 0)
#         outer_layout.setSpacing(0)

#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         scroll.setFrameShape(QFrame.NoFrame)

#         inner = QWidget()
#         two_col = TwoColumnLayout(inner)
#         scroll.setWidget(inner)

#         outer_layout.addWidget(scroll)
#         return container, two_col

#     # -------------------------
#     # BEHAVIOR TAB
#     # -------------------------
#     def _init_behavior_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.behavior_layout = layout

#         # Behavior distribution
#         self.card_behavior_dist = ChartCard("Behavior Distribution", AnalyticsColors.BEHAVIOR)
#         self.behavior_layout.add_card(self.card_behavior_dist)

#         # Behavior timeline
#         self.card_behavior_timeline = ChartCard("Behavior Timeline", AnalyticsColors.BEHAVIOR)
#         self.behavior_layout.add_card(self.card_behavior_timeline)

#         # Behavior by time of day
#         self.card_behavior_by_hour = ChartCard("Behavior by Time of Day", AnalyticsColors.BEHAVIOR)
#         self.behavior_layout.add_card(self.card_behavior_by_hour)

#         # Longest streak (text card)
#         self.card_behavior_streak = AnalyticsCard("Longest Focus Streak")
#         self.behavior_streak_label = QLabel("No data yet.")
#         self.behavior_streak_label.setObjectName("AnalyticsText")
#         self.behavior_streak_label.setWordWrap(True)
#         self.card_behavior_streak.body_layout.addWidget(self.behavior_streak_label)
#         self.behavior_layout.add_card(self.card_behavior_streak)

#         self.tabs.addTab(w, "Behavior")

#     def _refresh_behavior_tab(self):
#         # Distribution
#         dist = self.engine.behavior_distribution()
#         self.card_behavior_dist.clear()
#         if dist:
#             behaviors = list(dist.keys())
#             values = list(dist.values())
#             x = range(len(behaviors))
#             bg = pg.BarGraphItem(
#                 x=list(x),
#                 height=values,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_behavior_dist.plot.addItem(bg)
#             ax = self.card_behavior_dist.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)

#         # Timeline (smooth line)
#         timeline = self.engine.behavior_timeline()
#         self.card_behavior_timeline.clear()
#         times = timeline.get("times", [])
#         behaviors = timeline.get("behaviors", [])
#         if times and behaviors:
#             unique_behaviors = list(dict.fromkeys(behaviors))
#             mapping = {b: i for i, b in enumerate(unique_behaviors)}
#             y = [mapping[b] for b in behaviors]

#             self.card_behavior_timeline.plot.plot(
#                 list(range(len(times))), y,
#                 pen=self.card_behavior_timeline.smooth_pen(),
#                 antialias=True
#             )
#             self.card_behavior_timeline.plot.getAxis("bottom").setVisible(False)

#         # Behavior by hour (bar)
#         by_hour = self.engine.behavior_by_hour()
#         self.card_behavior_by_hour.clear()
#         if by_hour:
#             hours = sorted(by_hour.keys())
#             vals = [sum(by_hour[h].values()) for h in hours]
#             x = list(range(len(hours)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_behavior_by_hour.plot.addItem(bg)
#             labels = [f"{h:02d}:00" for h in hours]
#             ax = self.card_behavior_by_hour.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         # Longest streak
#         streak = self.engine.longest_behavior_streak()
#         if streak:
#             self.behavior_streak_label.setText(
#                 f"Longest streak: {streak['behavior']} for {streak['minutes']:.0f} minutes."
#             )
#         else:
#             self.behavior_streak_label.setText("No behavior streak data available yet.")

#     # -------------------------
#     # FATIGUE TAB
#     # -------------------------
#     def _init_fatigue_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.fatigue_layout = layout

#         self.card_fatigue_trend = ChartCard("Fatigue Trend", AnalyticsColors.FATIGUE)
#         self.fatigue_layout.add_card(self.card_fatigue_trend)

#         self.card_fatigue_by_behavior = ChartCard("Fatigue by Behavior", AnalyticsColors.FATIGUE)
#         self.fatigue_layout.add_card(self.card_fatigue_by_behavior)

#         self.card_fatigue_recovery = ChartCard("Fatigue Recovery After Breaks", AnalyticsColors.FATIGUE)
#         self.fatigue_layout.add_card(self.card_fatigue_recovery)

#         self.card_fatigue_peak = AnalyticsCard("Highest Fatigue Moment")
#         self.fatigue_peak_label = QLabel("No data yet.")
#         self.fatigue_peak_label.setObjectName("AnalyticsText")
#         self.fatigue_peak_label.setWordWrap(True)
#         self.card_fatigue_peak.body_layout.addWidget(self.fatigue_peak_label)
#         self.fatigue_layout.add_card(self.card_fatigue_peak)

#         self.tabs.addTab(w, "Fatigue")

#     def _refresh_fatigue_tab(self):
#         # Trend (smooth line)
#         trend = self.engine.fatigue_trend()
#         self.card_fatigue_trend.clear()
#         times = trend.get("times", [])
#         vals = trend.get("fatigue", [])
#         if times and vals:
#             self.card_fatigue_trend.plot.plot(
#                 list(range(len(times))), vals,
#                 pen=self.card_fatigue_trend.smooth_pen(),
#                 antialias=True
#             )
#             self.card_fatigue_trend.plot.setYRange(0, 100)

#         # By behavior (bar)
#         by_behavior = self.engine.fatigue_by_behavior()
#         self.card_fatigue_by_behavior.clear()
#         if by_behavior:
#             behaviors = list(by_behavior.keys())
#             vals = list(by_behavior.values())
#             x = list(range(len(behaviors)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.FATIGUE
#             )
#             self.card_fatigue_by_behavior.plot.addItem(bg)
#             ax = self.card_fatigue_by_behavior.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)
#             self.card_fatigue_by_behavior.plot.setYRange(0, 100)

#         # Recovery (smooth line)
#         rec = self.engine.fatigue_recovery_after_breaks()
#         self.card_fatigue_recovery.clear()
#         rt = rec.get("times", [])
#         rv = rec.get("fatigue", [])
#         if rt and rv:
#             self.card_fatigue_recovery.plot.plot(
#                 list(range(len(rt))), rv,
#                 pen=self.card_fatigue_recovery.smooth_pen(),
#                 antialias=True
#             )
#             self.card_fatigue_recovery.plot.setYRange(0, 100)

#         # Peak
#         peak = self.engine.highest_fatigue_moment()
#         if peak:
#             self.fatigue_peak_label.setText(
#                 f"Highest fatigue: {peak['fatigue']:.0f}/100 at {peak['time']}."
#             )
#         else:
#             self.fatigue_peak_label.setText("No fatigue peak data available yet.")
#     # -------------------------
#     # BREAK TAB
#     # -------------------------
#     def _init_break_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.break_layout = layout

#         self.card_break_reasons = ChartCard("Break Reasons", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_reasons)

#         self.card_break_timing = ChartCard("Break Timing Quality", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_timing)

#         self.card_break_timeline = ChartCard("Break Events Timeline", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_timeline)

#         self.card_break_suppression = ChartCard("Break Suppression", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_suppression)

#         self.tabs.addTab(w, "Breaks")

#     def _refresh_break_tab(self):
#         # Reasons (bar)
#         reasons = self.engine.break_reasons()
#         self.card_break_reasons.clear()
#         if reasons:
#             labels = list(reasons.keys())
#             vals = list(reasons.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BREAK
#             )
#             self.card_break_reasons.plot.addItem(bg)
#             ax = self.card_break_reasons.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         # Timing quality (bar)
#         timing = self.engine.break_timing_quality()
#         self.card_break_timing.clear()
#         if timing:
#             labels = ["Early", "On Time", "Late"]
#             vals = [
#                 timing.get("early", 0),
#                 timing.get("on_time", 0),
#                 timing.get("late", 0),
#             ]
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BREAK
#             )
#             self.card_break_timing.plot.addItem(bg)
#             ax = self.card_break_timing.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         # Timeline (dots)
#         timeline = self.engine.break_events_timeline()
#         self.card_break_timeline.clear()
#         times = timeline.get("times", [])
#         if times:
#             x = list(range(len(times)))
#             y = [1] * len(times)
#             self.card_break_timeline.plot.plot(
#                 x, y,
#                 pen=None,
#                 symbol="o",
#                 symbolSize=6,
#                 symbolBrush=AnalyticsColors.BREAK
#             )
#             self.card_break_timeline.plot.getAxis("bottom").setVisible(False)
#             self.card_break_timeline.plot.getAxis("left").setVisible(False)

#         # Suppression (bar)
#         supp = self.engine.break_suppression_stats()
#         self.card_break_suppression.clear()
#         if supp:
#             labels = list(supp.keys())
#             vals = list(supp.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BREAK
#             )
#             self.card_break_suppression.plot.addItem(bg)
#             ax = self.card_break_suppression.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#     # -------------------------
#     # SUPPRESSION TAB
#     # -------------------------
#     def _init_suppression_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.supp_layout = layout

#         self.card_supp_counts = ChartCard("Suppression Counts", AnalyticsColors.SUPPRESSION)
#         self.supp_layout.add_card(self.card_supp_counts)

#         self.card_away_resets = AnalyticsCard("Away Resets")
#         self.away_resets_label = QLabel("No data yet.")
#         self.away_resets_label.setObjectName("AnalyticsText")
#         self.away_resets_label.setWordWrap(True)
#         self.card_away_resets.body_layout.addWidget(self.away_resets_label)
#         self.supp_layout.add_card(self.card_away_resets)

#         self.tabs.addTab(w, "Suppression")

#     def _refresh_suppression_tab(self):
#         counts = self.engine.suppression_counts()
#         self.card_supp_counts.clear()
#         if counts:
#             labels = list(counts.keys())
#             vals = list(counts.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.SUPPRESSION
#             )
#             self.card_supp_counts.plot.addItem(bg)
#             ax = self.card_supp_counts.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         away = self.engine.away_resets_count()
#         self.away_resets_label.setText(
#             f"Away-based resets: {away}."
#         )

#     # -------------------------
#     # TIME OF DAY TAB
#     # -------------------------
#     def _init_time_of_day_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.tod_layout = layout

#         self.card_behavior_heatmap = ChartCard("Behavior Heatmap", AnalyticsColors.BEHAVIOR)
#         self.tod_layout.add_card(self.card_behavior_heatmap)

#         self.card_fatigue_heatmap = ChartCard("Fatigue Heatmap", AnalyticsColors.FATIGUE)
#         self.tod_layout.add_card(self.card_fatigue_heatmap)

#         self.card_break_heatmap = ChartCard("Break Heatmap", AnalyticsColors.BREAK)
#         self.tod_layout.add_card(self.card_break_heatmap)

#         self.card_supp_heatmap = ChartCard("Suppression Heatmap", AnalyticsColors.SUPPRESSION)
#         self.tod_layout.add_card(self.card_supp_heatmap)

#         self.tabs.addTab(w, "Time of Day")

#     def _plot_simple_heatmap(self, card: ChartCard, data: dict, color: str):
#         """
#         Simple 1D heatmap: hour -> value, rendered as colored bars.
#         """
#         card.clear()
#         if not data:
#             return

#         hours = sorted(data.keys())
#         vals = [data[h] for h in hours]
#         x = list(range(len(hours)))
#         bg = pg.BarGraphItem(
#             x=x,
#             height=vals,
#             width=0.8,
#             brush=color
#         )
#         card.plot.addItem(bg)
#         labels = [f"{h:02d}:00" for h in hours]
#         ax = card.plot.getAxis("bottom")
#         ax.setTicks([list(zip(x, labels))])
#         ax.setVisible(True)

#     def _refresh_time_of_day_tab(self):
#         beh = self.engine.behavior_heatmap()
#         self._plot_simple_heatmap(self.card_behavior_heatmap, beh, AnalyticsColors.BEHAVIOR)

#         fat = self.engine.fatigue_heatmap()
#         self._plot_simple_heatmap(self.card_fatigue_heatmap, fat, AnalyticsColors.FATIGUE)

#         br = self.engine.break_heatmap()
#         self._plot_simple_heatmap(self.card_break_heatmap, br, AnalyticsColors.BREAK)

#         supp = self.engine.suppression_heatmap()
#         self._plot_simple_heatmap(self.card_supp_heatmap, supp, AnalyticsColors.SUPPRESSION)
#     # -------------------------
#     # WEEKLY TAB
#     # -------------------------
#     def _init_weekly_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.weekly_layout = layout

#         self.card_weekly_behavior = ChartCard("Weekly Behavior Distribution", AnalyticsColors.BEHAVIOR)
#         self.weekly_layout.add_card(self.card_weekly_behavior)

#         self.card_weekly_fatigue = ChartCard("Weekly Fatigue Trend", AnalyticsColors.FATIGUE)
#         self.weekly_layout.add_card(self.card_weekly_fatigue)

#         self.card_weekly_break_consistency = AnalyticsCard("Weekly Break Consistency")
#         self.weekly_break_label = QLabel("No data yet.")
#         self.weekly_break_label.setObjectName("AnalyticsText")
#         self.weekly_break_label.setWordWrap(True)
#         self.card_weekly_break_consistency.body_layout.addWidget(self.weekly_break_label)
#         self.weekly_layout.add_card(self.card_weekly_break_consistency)

#         self.card_weekly_suppression = ChartCard("Weekly Suppression", AnalyticsColors.SUPPRESSION)
#         self.weekly_layout.add_card(self.card_weekly_suppression)

#         self.tabs.addTab(w, "Weekly")

#     def _refresh_weekly_tab(self):
#         summary = self.engine.weekly_behavior_summary()
#         self.card_weekly_behavior.clear()
#         self.card_weekly_fatigue.clear()
#         self.card_weekly_suppression.clear()

#         if not summary:
#             self.weekly_break_label.setText("No weekly data available yet.")
#             return

#         # Behavior distribution (bar)
#         dist = summary.get("distribution", {})
#         if dist:
#             behaviors = list(dist.keys())
#             vals = list(dist.values())
#             x = list(range(len(behaviors)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_weekly_behavior.plot.addItem(bg)
#             ax = self.card_weekly_behavior.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)

#         # Fatigue trend (smooth line)
#         ft = summary.get("fatigue_trend", {})
#         days = ft.get("days", [])
#         fv = ft.get("fatigue", [])
#         if days and fv:
#             self.card_weekly_fatigue.plot.plot(
#                 list(range(len(days))), fv,
#                 pen=self.card_weekly_fatigue.smooth_pen(),
#                 antialias=True
#             )
#             self.card_weekly_fatigue.plot.setYRange(0, 100)

#         # Break consistency
#         cons = summary.get("break_consistency", None)
#         if cons is not None:
#             self.weekly_break_label.setText(
#                 f"Break consistency this week: {cons:.0f}/100."
#             )
#         else:
#             self.weekly_break_label.setText("No break consistency data for this week.")

#         # Suppression (bar)
#         supp = summary.get("suppression_counts", {})
#         if supp:
#             labels = list(supp.keys())
#             vals = list(supp.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.SUPPRESSION
#             )
#             self.card_weekly_suppression.plot.addItem(bg)
#             ax = self.card_weekly_suppression.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#     # -------------------------
#     # MONTHLY TAB
#     # -------------------------
#     def _init_monthly_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.monthly_layout = layout

#         self.card_monthly_behavior = ChartCard("Monthly Behavior Distribution", AnalyticsColors.BEHAVIOR)
#         self.monthly_layout.add_card(self.card_monthly_behavior)

#         self.card_monthly_fatigue = ChartCard("Monthly Fatigue Trend", AnalyticsColors.FATIGUE)
#         self.monthly_layout.add_card(self.card_monthly_fatigue)

#         self.card_monthly_break_consistency = AnalyticsCard("Monthly Break Consistency")
#         self.monthly_break_label = QLabel("No data yet.")
#         self.monthly_break_label.setObjectName("AnalyticsText")
#         self.monthly_break_label.setWordWrap(True)
#         self.card_monthly_break_consistency.body_layout.addWidget(self.monthly_break_label)
#         self.monthly_layout.add_card(self.card_monthly_break_consistency)

#         self.card_monthly_suppression = ChartCard("Monthly Suppression", AnalyticsColors.SUPPRESSION)
#         self.monthly_layout.add_card(self.card_monthly_suppression)

#         self.tabs.addTab(w, "Monthly")

#     def _refresh_monthly_tab(self):
#         summary = self.engine.monthly_behavior_summary()
#         self.card_monthly_behavior.clear()
#         self.card_monthly_fatigue.clear()
#         self.card_monthly_suppression.clear()

#         if not summary:
#             self.monthly_break_label.setText("No monthly data available yet.")
#             return

#         # Behavior distribution (bar)
#         dist = summary.get("distribution", {})
#         if dist:
#             behaviors = list(dist.keys())
#             vals = list(dist.values())
#             x = list(range(len(behaviors)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_monthly_behavior.plot.addItem(bg)
#             ax = self.card_monthly_behavior.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)

#         # Fatigue trend (smooth line)
#         ft = summary.get("fatigue_trend", {})
#         days = ft.get("days", [])
#         fv = ft.get("fatigue", [])
#         if days and fv:
#             self.card_monthly_fatigue.plot.plot(
#                 list(range(len(days))), fv,
#                 pen=self.card_monthly_fatigue.smooth_pen(),
#                 antialias=True
#             )
#             self.card_monthly_fatigue.plot.setYRange(0, 100)

#         # Break consistency
#         cons = summary.get("break_consistency", None)
#         if cons is not None:
#             self.monthly_break_label.setText(
#                 f"Break consistency this month: {cons:.0f}/100."
#             )
#         else:
#             self.monthly_break_label.setText("No break consistency data for this month.")

#         # Suppression (bar)
#         supp = summary.get("suppression_counts", {})
#         if supp:
#             labels = list(supp.keys())
#             vals = list(supp.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.SUPPRESSION
#             )
#             self.card_monthly_suppression.plot.addItem(bg)
#             ax = self.card_monthly_suppression.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#     # -------------------------
#     # INSIGHTS TAB
#     # -------------------------
#     def _init_insights_tab(self):
#         w = QWidget()
#         v = QVBoxLayout(w)
#         v.setContentsMargins(10, 10, 10, 10)
#         v.setSpacing(10)

#         self.insights_container = QVBoxLayout()
#         v.addLayout(self.insights_container)
#         v.addStretch()

#         self.tabs.addTab(w, "AI Insights")

#     def _refresh_insights_tab(self):
#         insights = self.engine.ai_insights()

#         # Clear old cards
#         while self.insights_container.count():
#             item = self.insights_container.takeAt(0)
#             if item.widget():
#                 item.widget().deleteLater()

#         # Add new cards
#         for text in insights:
#             card = QFrame()
#             card.setObjectName("InsightCard")
#             v = QVBoxLayout(card)
#             v.setContentsMargins(12, 12, 12, 12)

#             lbl = QLabel(text)
#             lbl.setObjectName("InsightText")
#             lbl.setWordWrap(True)
#             v.addWidget(lbl)

#             self.insights_container.addWidget(card)

#     # -------------------------
#     # GLOBAL REFRESH
#     # -------------------------
#     def refresh_all(self):
#         self._refresh_behavior_tab()
#         self._refresh_fatigue_tab()
#         self._refresh_break_tab()
#         self._refresh_suppression_tab()
#         self._refresh_time_of_day_tab()
#         self._refresh_weekly_tab()
#         self._refresh_monthly_tab()
#         self._refresh_insights_tab()


















# I only fixed the graph so that A thing and zoom won't work

# # Upgrade design

# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QFrame, QSizePolicy, QScrollArea
# )
# from PySide6.QtCore import Qt
# import pyqtgraph as pg

# from core.analytics_engine import AnalyticsEngine


# # ============================================================
# # GLOBAL RENDERING IMPROVEMENTS (smooth lines everywhere)
# # ============================================================
# #pg.setConfigOptions(useOpenGL=True)
# #pg.setConfigOptions(antialias=True)


# # -----------------------------
# # Color palette (Apple-style vibrant)
# # -----------------------------
# class AnalyticsColors:
#     BEHAVIOR = "#0A84FF"   # blue
#     FATIGUE = "#FF9F0A"    # orange
#     BREAK = "#30D158"      # green
#     SUPPRESSION = "#FF453A"  # red
#     INSIGHT = "#BF5AF2"    # purple
#     GRID = (255, 255, 255, 40)


# CARD_HEIGHT = 320  # fixed height for chart cards


# # -----------------------------
# # Generic card container
# # -----------------------------
# class AnalyticsCard(QFrame):
#     """
#     Simple Fluent-style card with a title and content area.
#     Used for both charts and text.
#     """
#     def __init__(self, title: str):
#         super().__init__()
#         self.setObjectName("AnalyticsCard")
#         self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#         self.setMinimumHeight(CARD_HEIGHT)

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(14, 14, 14, 14)
#         layout.setSpacing(8)

#         self.title_label = QLabel(title)
#         self.title_label.setObjectName("AnalyticsCardTitle")
#         layout.addWidget(self.title_label)

#         self.body_layout = QVBoxLayout()
#         self.body_layout.setContentsMargins(0, 0, 0, 0)
#         self.body_layout.setSpacing(4)
#         layout.addLayout(self.body_layout)


# # -----------------------------
# # Chart card wrapper
# # -----------------------------
# class ChartCard(AnalyticsCard):
#     """
#     Card that hosts a PyQtGraph PlotWidget with consistent styling.
#     """
#     def __init__(self, title: str, color: str):
#         super().__init__(title)
#         self.color = color

#         self.plot = pg.PlotWidget()
#         self.plot.setBackground(None)
#         self.plot.showGrid(x=False, y=True, alpha=0.15)
#         self.plot.getAxis("left").setVisible(False)
#         self.plot.getAxis("bottom").setVisible(False)

#         # Disable all mouse interaction
#         self.plot.setMenuEnabled(False)
#         self.plot.setMouseEnabled(x=False, y=False)
#         self.plot.wheelEvent = lambda event: None  # Prevent wheel zoom

#         # Prevent collapse (fixes the "A" glyph)
#         vb = self.plot.getViewBox()
#         vb.setLimits(minXRange=1, minYRange=1)

#         # Keep chart visually stable
#         self.plot.setClipToView(True)

#         # Disable downsampling for smooth lines
#         self.plot.setDownsampling(mode=None)

#         # Remove border
#         self.plot.getPlotItem().getViewBox().setBorder(None)

#         self.body_layout.addWidget(self.plot)

#     def smooth_pen(self):
#         """Return a smooth, anti-aliased pen."""
#         pen = pg.mkPen(self.color, width=2, cosmetic=True)
#         pen.setCapStyle(Qt.RoundCap)
#         pen.setJoinStyle(Qt.RoundJoin)
#         return pen

#     def clear(self):
#         self.plot.clear()


# # -----------------------------
# # Two-column layout helper
# # -----------------------------
# class TwoColumnLayout(QVBoxLayout):
#     """
#     Simple helper to place cards in two columns with vertical flow.
#     """
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setContentsMargins(10, 10, 10, 10)
#         self.setSpacing(10)

#         self.row_layout = None
#         self._items_in_row = 0

#     def add_card(self, card: QWidget):
#         if self.row_layout is None or self._items_in_row >= 2:
#             self.row_layout = QHBoxLayout()
#             self.row_layout.setSpacing(10)
#             self.addLayout(self.row_layout)
#             self._items_in_row = 0

#         self.row_layout.addWidget(card)
#         self._items_in_row += 1
# # -----------------------------
# # Main Analytics Suite Page
# # -----------------------------
# class AnalyticsSuitePage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("AnalyticsSuitePage")

#         self.engine = AnalyticsEngine()

#         root_layout = QVBoxLayout(self)
#         root_layout.setContentsMargins(20, 20, 20, 20)
#         root_layout.setSpacing(20)

#         title = QLabel("Analytics")
#         title.setObjectName("PageTitle")
#         root_layout.addWidget(title)

#         # Tab widget
#         self.tabs = QTabWidget()
#         self.tabs.setObjectName("AnalyticsTabs")
#         root_layout.addWidget(self.tabs)

#         # Tabs
#         self._init_behavior_tab()
#         self._init_fatigue_tab()
#         self._init_break_tab()
#         self._init_suppression_tab()
#         self._init_time_of_day_tab()
#         self._init_weekly_tab()
#         self._init_monthly_tab()
#         self._init_insights_tab()

#         # Initial refresh
#         self.refresh_all()

#     # -------------------------
#     # Tab helpers
#     # -------------------------
#     def _create_scrollable_tab(self):
#         """
#         Creates a scrollable area with a two-column layout inside.
#         Returns (container_widget, two_column_layout).
#         """
#         container = QWidget()
#         outer_layout = QVBoxLayout(container)
#         outer_layout.setContentsMargins(0, 0, 0, 0)
#         outer_layout.setSpacing(0)

#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         scroll.setFrameShape(QFrame.NoFrame)

#         inner = QWidget()
#         two_col = TwoColumnLayout(inner)
#         scroll.setWidget(inner)

#         outer_layout.addWidget(scroll)
#         return container, two_col

#     # -------------------------
#     # BEHAVIOR TAB
#     # -------------------------
#     def _init_behavior_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.behavior_layout = layout

#         # Behavior distribution
#         self.card_behavior_dist = ChartCard("Behavior Distribution", AnalyticsColors.BEHAVIOR)
#         self.behavior_layout.add_card(self.card_behavior_dist)

#         # Behavior timeline
#         self.card_behavior_timeline = ChartCard("Behavior Timeline", AnalyticsColors.BEHAVIOR)
#         self.behavior_layout.add_card(self.card_behavior_timeline)

#         # Behavior by time of day
#         self.card_behavior_by_hour = ChartCard("Behavior by Time of Day", AnalyticsColors.BEHAVIOR)
#         self.behavior_layout.add_card(self.card_behavior_by_hour)

#         # Longest streak (text card)
#         self.card_behavior_streak = AnalyticsCard("Longest Focus Streak")
#         self.behavior_streak_label = QLabel("No data yet.")
#         self.behavior_streak_label.setObjectName("AnalyticsText")
#         self.behavior_streak_label.setWordWrap(True)
#         self.card_behavior_streak.body_layout.addWidget(self.behavior_streak_label)
#         self.behavior_layout.add_card(self.card_behavior_streak)

#         self.tabs.addTab(w, "Behavior")

#     def _refresh_behavior_tab(self):
#         # Distribution
#         dist = self.engine.behavior_distribution()
#         self.card_behavior_dist.clear()
#         if dist:
#             behaviors = list(dist.keys())
#             values = list(dist.values())
#             x = range(len(behaviors))
#             bg = pg.BarGraphItem(
#                 x=list(x),
#                 height=values,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_behavior_dist.plot.addItem(bg)
#             ax = self.card_behavior_dist.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)

#         # Timeline (smooth line)
#         timeline = self.engine.behavior_timeline()
#         self.card_behavior_timeline.clear()
#         times = timeline.get("times", [])
#         behaviors = timeline.get("behaviors", [])
#         if times and behaviors:
#             unique_behaviors = list(dict.fromkeys(behaviors))
#             mapping = {b: i for i, b in enumerate(unique_behaviors)}
#             y = [mapping[b] for b in behaviors]

#             self.card_behavior_timeline.plot.plot(
#                 list(range(len(times))), y,
#                 pen=self.card_behavior_timeline.smooth_pen(),
#                 antialias=True
#             )
#             self.card_behavior_timeline.plot.getAxis("bottom").setVisible(False)

#         # Behavior by hour (bar)
#         by_hour = self.engine.behavior_by_hour()
#         self.card_behavior_by_hour.clear()
#         if by_hour:
#             hours = sorted(by_hour.keys())
#             vals = [sum(by_hour[h].values()) for h in hours]
#             x = list(range(len(hours)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_behavior_by_hour.plot.addItem(bg)
#             labels = [f"{h:02d}:00" for h in hours]
#             ax = self.card_behavior_by_hour.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         # Longest streak
#         streak = self.engine.longest_behavior_streak()
#         if streak:
#             self.behavior_streak_label.setText(
#                 f"Longest streak: {streak['behavior']} for {streak['minutes']:.0f} minutes."
#             )
#         else:
#             self.behavior_streak_label.setText("No behavior streak data available yet.")

#     # -------------------------
#     # FATIGUE TAB
#     # -------------------------
#     def _init_fatigue_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.fatigue_layout = layout

#         self.card_fatigue_trend = ChartCard("Fatigue Trend", AnalyticsColors.FATIGUE)
#         self.fatigue_layout.add_card(self.card_fatigue_trend)

#         self.card_fatigue_by_behavior = ChartCard("Fatigue by Behavior", AnalyticsColors.FATIGUE)
#         self.fatigue_layout.add_card(self.card_fatigue_by_behavior)

#         self.card_fatigue_recovery = ChartCard("Fatigue Recovery After Breaks", AnalyticsColors.FATIGUE)
#         self.fatigue_layout.add_card(self.card_fatigue_recovery)

#         self.card_fatigue_peak = AnalyticsCard("Highest Fatigue Moment")
#         self.fatigue_peak_label = QLabel("No data yet.")
#         self.fatigue_peak_label.setObjectName("AnalyticsText")
#         self.fatigue_peak_label.setWordWrap(True)
#         self.card_fatigue_peak.body_layout.addWidget(self.fatigue_peak_label)
#         self.fatigue_layout.add_card(self.card_fatigue_peak)

#         self.tabs.addTab(w, "Fatigue")

#     def _refresh_fatigue_tab(self):
#         # Trend (smooth line)
#         trend = self.engine.fatigue_trend()
#         self.card_fatigue_trend.clear()
#         times = trend.get("times", [])
#         vals = trend.get("fatigue", [])
#         if times and vals:
#             self.card_fatigue_trend.plot.plot(
#                 list(range(len(times))), vals,
#                 pen=self.card_fatigue_trend.smooth_pen(),
#                 antialias=True
#             )
#             self.card_fatigue_trend.plot.setYRange(0, 100)
            

#         # By behavior (bar)
#         by_behavior = self.engine.fatigue_by_behavior()
#         self.card_fatigue_by_behavior.clear()
#         if by_behavior:
#             behaviors = list(by_behavior.keys())
#             vals = list(by_behavior.values())
#             x = list(range(len(behaviors)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.FATIGUE
#             )
#             self.card_fatigue_by_behavior.plot.addItem(bg)
#             ax = self.card_fatigue_by_behavior.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)
#             self.card_fatigue_by_behavior.plot.setYRange(0, 100)

#         # Recovery (smooth line)
#         rec = self.engine.fatigue_recovery_after_breaks()
#         self.card_fatigue_recovery.clear()
#         rt = rec.get("times", [])
#         rv = rec.get("fatigue", [])
#         if rt and rv:
#             self.card_fatigue_recovery.plot.plot(
#                 list(range(len(rt))), rv,
#                 pen=self.card_fatigue_recovery.smooth_pen(),
#                 antialias=True
#             )
#             self.card_fatigue_recovery.plot.setYRange(0, 100)

#         # Peak
#         peak = self.engine.highest_fatigue_moment()
#         if peak:
#             self.fatigue_peak_label.setText(
#                 f"Highest fatigue: {peak['fatigue']:.0f}/100 at {peak['time']}."
#             )
#         else:
#             self.fatigue_peak_label.setText("No fatigue peak data available yet.")
#     # -------------------------
#     # BREAK TAB
#     # -------------------------
#     def _init_break_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.break_layout = layout

#         self.card_break_reasons = ChartCard("Break Reasons", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_reasons)

#         self.card_break_timing = ChartCard("Break Timing Quality", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_timing)

#         self.card_break_timeline = ChartCard("Break Events Timeline", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_timeline)

#         self.card_break_suppression = ChartCard("Break Suppression", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_suppression)

#         self.tabs.addTab(w, "Breaks")

#     def _refresh_break_tab(self):
#         # Reasons (bar)
#         reasons = self.engine.break_reasons()
#         self.card_break_reasons.clear()
#         if reasons:
#             labels = list(reasons.keys())
#             vals = list(reasons.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BREAK
#             )
#             self.card_break_reasons.plot.addItem(bg)
#             ax = self.card_break_reasons.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         # Timing quality (bar)
#         timing = self.engine.break_timing_quality()
#         self.card_break_timing.clear()
#         if timing:
#             labels = ["Early", "On Time", "Late"]
#             vals = [
#                 timing.get("early", 0),
#                 timing.get("on_time", 0),
#                 timing.get("late", 0),
#             ]
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BREAK
#             )
#             self.card_break_timing.plot.addItem(bg)
#             ax = self.card_break_timing.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         # Timeline (dots)
#         timeline = self.engine.break_events_timeline()
#         self.card_break_timeline.clear()
#         times = timeline.get("times", [])
#         if times:
#             x = list(range(len(times)))
#             y = [1] * len(times)
#             self.card_break_timeline.plot.plot(
#                 x, y,
#                 pen=None,
#                 symbol="o",
#                 symbolSize=6,
#                 symbolBrush=AnalyticsColors.BREAK
#             )
#             self.card_break_timeline.plot.getAxis("bottom").setVisible(False)
#             self.card_break_timeline.plot.getAxis("left").setVisible(False)

#         # Suppression (bar)
#         supp = self.engine.break_suppression_stats()
#         self.card_break_suppression.clear()
#         if supp:
#             labels = list(supp.keys())
#             vals = list(supp.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BREAK
#             )
#             self.card_break_suppression.plot.addItem(bg)
#             ax = self.card_break_suppression.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#     # -------------------------
#     # SUPPRESSION TAB
#     # -------------------------
#     def _init_suppression_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.supp_layout = layout

#         self.card_supp_counts = ChartCard("Suppression Counts", AnalyticsColors.SUPPRESSION)
#         self.supp_layout.add_card(self.card_supp_counts)

#         self.card_away_resets = AnalyticsCard("Away Resets")
#         self.away_resets_label = QLabel("No data yet.")
#         self.away_resets_label.setObjectName("AnalyticsText")
#         self.away_resets_label.setWordWrap(True)
#         self.card_away_resets.body_layout.addWidget(self.away_resets_label)
#         self.supp_layout.add_card(self.card_away_resets)

#         self.tabs.addTab(w, "Suppression")

#     def _refresh_suppression_tab(self):
#         counts = self.engine.suppression_counts()
#         self.card_supp_counts.clear()
#         if counts:
#             labels = list(counts.keys())
#             vals = list(counts.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.SUPPRESSION
#             )
#             self.card_supp_counts.plot.addItem(bg)
#             ax = self.card_supp_counts.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         away = self.engine.away_resets_count()
#         self.away_resets_label.setText(
#             f"Away-based resets: {away}."
#         )

#     # -------------------------
#     # TIME OF DAY TAB
#     # -------------------------
#     def _init_time_of_day_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.tod_layout = layout

#         self.card_behavior_heatmap = ChartCard("Behavior Heatmap", AnalyticsColors.BEHAVIOR)
#         self.tod_layout.add_card(self.card_behavior_heatmap)

#         self.card_fatigue_heatmap = ChartCard("Fatigue Heatmap", AnalyticsColors.FATIGUE)
#         self.tod_layout.add_card(self.card_fatigue_heatmap)

#         self.card_break_heatmap = ChartCard("Break Heatmap", AnalyticsColors.BREAK)
#         self.tod_layout.add_card(self.card_break_heatmap)

#         self.card_supp_heatmap = ChartCard("Suppression Heatmap", AnalyticsColors.SUPPRESSION)
#         self.tod_layout.add_card(self.card_supp_heatmap)

#         self.tabs.addTab(w, "Time of Day")

#     def _plot_simple_heatmap(self, card: ChartCard, data: dict, color: str):
#         """
#         Simple 1D heatmap: hour -> value, rendered as colored bars.
#         """
#         card.clear()
#         if not data:
#             return

#         hours = sorted(data.keys())
#         vals = [data[h] for h in hours]
#         x = list(range(len(hours)))

#         bg = pg.BarGraphItem(
#             x=x,
#             height=vals,
#             width=0.8,
#             brush=color
#         )
#         card.plot.addItem(bg)

#         # Build hour labels
#         labels = [f"{h:02d}:00" for h in hours]

#         # ⭐ Prevent overlapping labels by thinning them
#         step = max(1, len(hours) // 8)   # show ~8 labels max
#         tick_positions = [(i, labels[i]) for i in range(0, len(labels), step)]

#         ax = card.plot.getAxis("bottom")
#         ax.setTicks([tick_positions])
#         ax.setVisible(True)

        
#     def _refresh_time_of_day_tab(self):
#         beh = self.engine.behavior_heatmap()
#         self._plot_simple_heatmap(self.card_behavior_heatmap, beh, AnalyticsColors.BEHAVIOR)

#         fat = self.engine.fatigue_heatmap()
#         self._plot_simple_heatmap(self.card_fatigue_heatmap, fat, AnalyticsColors.FATIGUE)

#         br = self.engine.break_heatmap()
#         self._plot_simple_heatmap(self.card_break_heatmap, br, AnalyticsColors.BREAK)

#         supp = self.engine.suppression_heatmap()
#         self._plot_simple_heatmap(self.card_supp_heatmap, supp, AnalyticsColors.SUPPRESSION)
#     # -------------------------
#     # WEEKLY TAB
#     # -------------------------
#     def _init_weekly_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.weekly_layout = layout

#         self.card_weekly_behavior = ChartCard("Weekly Behavior Distribution", AnalyticsColors.BEHAVIOR)
#         self.weekly_layout.add_card(self.card_weekly_behavior)

#         self.card_weekly_fatigue = ChartCard("Weekly Fatigue Trend", AnalyticsColors.FATIGUE)
#         self.weekly_layout.add_card(self.card_weekly_fatigue)

#         self.card_weekly_break_consistency = AnalyticsCard("Weekly Break Consistency")
#         self.weekly_break_label = QLabel("No data yet.")
#         self.weekly_break_label.setObjectName("AnalyticsText")
#         self.weekly_break_label.setWordWrap(True)
#         self.card_weekly_break_consistency.body_layout.addWidget(self.weekly_break_label)
#         self.weekly_layout.add_card(self.card_weekly_break_consistency)

#         self.card_weekly_suppression = ChartCard("Weekly Suppression", AnalyticsColors.SUPPRESSION)
#         self.weekly_layout.add_card(self.card_weekly_suppression)

#         self.tabs.addTab(w, "Weekly")

#     def _refresh_weekly_tab(self):
#         summary = self.engine.weekly_behavior_summary()
#         self.card_weekly_behavior.clear()
#         self.card_weekly_fatigue.clear()
#         self.card_weekly_suppression.clear()

#         if not summary:
#             self.weekly_break_label.setText("No weekly data available yet.")
#             return

#         # Behavior distribution (bar)
#         dist = summary.get("distribution", {})
#         if dist:
#             behaviors = list(dist.keys())
#             vals = list(dist.values())
#             x = list(range(len(behaviors)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_weekly_behavior.plot.addItem(bg)
#             ax = self.card_weekly_behavior.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)

#         # Fatigue trend (smooth line)
#         ft = summary.get("fatigue_trend", {})
#         days = ft.get("days", [])
#         fv = ft.get("fatigue", [])
#         if days and fv:
#             self.card_weekly_fatigue.plot.plot(
#                 list(range(len(days))), fv,
#                 pen=self.card_weekly_fatigue.smooth_pen(),
#                 antialias=True
#             )
#             self.card_weekly_fatigue.plot.setYRange(0, 100)

#         # Break consistency
#         cons = summary.get("break_consistency", None)
#         if cons is not None:
#             self.weekly_break_label.setText(
#                 f"Break consistency this week: {cons:.0f}/100."
#             )
#         else:
#             self.weekly_break_label.setText("No break consistency data for this week.")

#         # Suppression (bar)
#         supp = summary.get("suppression_counts", {})
#         if supp:
#             labels = list(supp.keys())
#             vals = list(supp.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.SUPPRESSION
#             )
#             self.card_weekly_suppression.plot.addItem(bg)
#             ax = self.card_weekly_suppression.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#     # -------------------------
#     # MONTHLY TAB
#     # -------------------------
#     def _init_monthly_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.monthly_layout = layout

#         self.card_monthly_behavior = ChartCard("Monthly Behavior Distribution", AnalyticsColors.BEHAVIOR)
#         self.monthly_layout.add_card(self.card_monthly_behavior)

#         self.card_monthly_fatigue = ChartCard("Monthly Fatigue Trend", AnalyticsColors.FATIGUE)
#         self.monthly_layout.add_card(self.card_monthly_fatigue)

#         self.card_monthly_break_consistency = AnalyticsCard("Monthly Break Consistency")
#         self.monthly_break_label = QLabel("No data yet.")
#         self.monthly_break_label.setObjectName("AnalyticsText")
#         self.monthly_break_label.setWordWrap(True)
#         self.card_monthly_break_consistency.body_layout.addWidget(self.monthly_break_label)
#         self.monthly_layout.add_card(self.card_monthly_break_consistency)

#         self.card_monthly_suppression = ChartCard("Monthly Suppression", AnalyticsColors.SUPPRESSION)
#         self.monthly_layout.add_card(self.card_monthly_suppression)

#         self.tabs.addTab(w, "Monthly")

#     def _refresh_monthly_tab(self):
#         summary = self.engine.monthly_behavior_summary()
#         self.card_monthly_behavior.clear()
#         self.card_monthly_fatigue.clear()
#         self.card_monthly_suppression.clear()

#         if not summary:
#             self.monthly_break_label.setText("No monthly data available yet.")
#             return

#         # Behavior distribution (bar)
#         dist = summary.get("distribution", {})
#         if dist:
#             behaviors = list(dist.keys())
#             vals = list(dist.values())
#             x = list(range(len(behaviors)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_monthly_behavior.plot.addItem(bg)
#             ax = self.card_monthly_behavior.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)

#         # Fatigue trend (smooth line)
#         ft = summary.get("fatigue_trend", {})
#         days = ft.get("days", [])
#         fv = ft.get("fatigue", [])
#         if days and fv:
#             self.card_monthly_fatigue.plot.plot(
#                 list(range(len(days))), fv,
#                 pen=self.card_monthly_fatigue.smooth_pen(),
#                 antialias=True
#             )
#             self.card_monthly_fatigue.plot.setYRange(0, 100)

#         # Break consistency
#         cons = summary.get("break_consistency", None)
#         if cons is not None:
#             self.monthly_break_label.setText(
#                 f"Break consistency this month: {cons:.0f}/100."
#             )
#         else:
#             self.monthly_break_label.setText("No break consistency data for this month.")

#         # Suppression (bar)
#         supp = summary.get("suppression_counts", {})
#         if supp:
#             labels = list(supp.keys())
#             vals = list(supp.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.SUPPRESSION
#             )
#             self.card_monthly_suppression.plot.addItem(bg)
#             ax = self.card_monthly_suppression.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#     # -------------------------
#     # INSIGHTS TAB
#     # -------------------------
#     def _init_insights_tab(self):
#         w = QWidget()
#         v = QVBoxLayout(w)
#         v.setContentsMargins(10, 10, 10, 10)
#         v.setSpacing(10)

#         self.insights_container = QVBoxLayout()
#         v.addLayout(self.insights_container)
#         v.addStretch()

#         self.tabs.addTab(w, "AI Insights")

#     def _refresh_insights_tab(self):
#         insights = self.engine.ai_insights()

#         # Clear old cards
#         while self.insights_container.count():
#             item = self.insights_container.takeAt(0)
#             if item.widget():
#                 item.widget().deleteLater()

#         # Add new cards
#         for text in insights:
#             card = QFrame()
#             card.setObjectName("InsightCard")
#             v = QVBoxLayout(card)
#             v.setContentsMargins(12, 12, 12, 12)

#             lbl = QLabel(text)
#             lbl.setObjectName("InsightText")
#             lbl.setWordWrap(True)
#             v.addWidget(lbl)

#             self.insights_container.addWidget(card)

#     # -------------------------
#     # GLOBAL REFRESH
#     # -------------------------
#     def refresh_all(self):
#         self._refresh_behavior_tab()
#         self._refresh_fatigue_tab()
#         self._refresh_break_tab()
#         self._refresh_suppression_tab()
#         self._refresh_time_of_day_tab()
#         self._refresh_weekly_tab()
#         self._refresh_monthly_tab()
#         self._refresh_insights_tab()























# Fixing the A on fatigue tab

# # Upgrade design

# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QFrame, QSizePolicy, QScrollArea
# )
# from PySide6.QtCore import Qt
# import pyqtgraph as pg

# from core.analytics_engine import AnalyticsEngine
# from PySide6 import QtWidgets, QtGui


# # ============================================================
# # GLOBAL RENDERING IMPROVEMENTS (smooth lines everywhere)
# # ============================================================
# #pg.setConfigOptions(useOpenGL=True)
# #pg.setConfigOptions(antialias=True)


# # -----------------------------
# # Color palette (Apple-style vibrant)
# # -----------------------------
# class AnalyticsColors:
#     BEHAVIOR = "#0A84FF"   # blue
#     FATIGUE = "#FF9F0A"    # orange
#     BREAK = "#30D158"      # green
#     SUPPRESSION = "#FF453A"  # red
#     INSIGHT = "#BF5AF2"    # purple
#     GRID = (255, 255, 255, 40)


# CARD_HEIGHT = 320  # fixed height for chart cards


# # -----------------------------
# # Generic card container
# # -----------------------------
# class AnalyticsCard(QFrame):
#     """
#     Simple Fluent-style card with a title and content area.
#     Used for both charts and text.
#     """
#     def __init__(self, title: str):
#         super().__init__()
#         self.setObjectName("AnalyticsCard")
#         self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#         self.setMinimumHeight(CARD_HEIGHT)

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(14, 14, 14, 14)
#         layout.setSpacing(8)

#         self.title_label = QLabel(title)
#         self.title_label.setObjectName("AnalyticsCardTitle")
#         layout.addWidget(self.title_label)

#         self.body_layout = QVBoxLayout()
#         self.body_layout.setContentsMargins(0, 0, 0, 0)
#         self.body_layout.setSpacing(4)
#         layout.addLayout(self.body_layout)


# # -----------------------------
# # Chart card wrapper
# # -----------------------------
# class ChartCard(AnalyticsCard):
#     """
#     Card that hosts a PyQtGraph PlotWidget with consistent styling.
#     """
#     def __init__(self, title: str, color: str):
#         super().__init__(title)
#         self.color = color

#         self.plot = pg.PlotWidget()
#         self.plot.setBackground(None)
#         self.plot.showGrid(x=False, y=True, alpha=0.15)
        
#          # 🔹 Brutal but reliable: hide all PlotItem buttons (including "A")
#         plot_item = self.plot.getPlotItem()
#         if hasattr(plot_item, "buttons"):
#             for btn in plot_item.buttons.values():
#                 btn.hide()

#         self.plot.getAxis("left").setVisible(False)
#         self.plot.getAxis("bottom").setVisible(False)

#         # Disable all mouse interaction
#         self.plot.setMenuEnabled(False)
#         self.plot.setMouseEnabled(x=False, y=False)
#         self.plot.wheelEvent = lambda event: None  # Prevent wheel zoom

#         # Prevent collapse (fixes the "A" glyph)
#         vb = self.plot.getViewBox()
#         vb.setLimits(minXRange=1, minYRange=1)

#         # Keep chart visually stable
#         self.plot.setClipToView(True)

#         # Disable downsampling for smooth lines
#         self.plot.setDownsampling(mode=None)

#         # Remove border
#         self.plot.getPlotItem().getViewBox().setBorder(None)

#         self.body_layout.addWidget(self.plot)

#     def smooth_pen(self):
#         """Return a smooth, anti-aliased pen."""
#         pen = pg.mkPen(self.color, width=2, cosmetic=True)
#         pen.setCapStyle(Qt.RoundCap)
#         pen.setJoinStyle(Qt.RoundJoin)
#         return pen

#     def clear(self):
#         self.plot.clear()


# # -----------------------------
# # Two-column layout helper
# # -----------------------------
# class TwoColumnLayout(QVBoxLayout):
#     """
#     Simple helper to place cards in two columns with vertical flow.
#     """
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setContentsMargins(10, 10, 10, 10)
#         self.setSpacing(10)

#         self.row_layout = None
#         self._items_in_row = 0

#     def add_card(self, card: QWidget):
#         if self.row_layout is None or self._items_in_row >= 2:
#             self.row_layout = QHBoxLayout()
#             self.row_layout.setSpacing(10)
#             self.addLayout(self.row_layout)
#             self._items_in_row = 0

#         self.row_layout.addWidget(card)
#         self._items_in_row += 1
# # -----------------------------
# # Main Analytics Suite Page
# # -----------------------------
# class AnalyticsSuitePage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("AnalyticsSuitePage")

#         self.engine = AnalyticsEngine()

#         root_layout = QVBoxLayout(self)
#         root_layout.setContentsMargins(20, 20, 20, 20)
#         root_layout.setSpacing(20)

#         title = QLabel("Analytics")
#         title.setObjectName("PageTitle")
#         root_layout.addWidget(title)

#         # Tab widget
#         self.tabs = QTabWidget()
#         self.tabs.setObjectName("AnalyticsTabs")
#         root_layout.addWidget(self.tabs)

#         # Tabs
#         self._init_behavior_tab()
#         self._init_fatigue_tab()
#         self._init_break_tab()
#         self._init_suppression_tab()
#         self._init_time_of_day_tab()
#         self._init_weekly_tab()
#         self._init_monthly_tab()
#         self._init_insights_tab()

#         # Initial refresh
#         self.refresh_all()

#     # -------------------------
#     # Tab helpers
#     # -------------------------
#     def _create_scrollable_tab(self):
#         """
#         Creates a scrollable area with a two-column layout inside.
#         Returns (container_widget, two_column_layout).
#         """
#         container = QWidget()
#         outer_layout = QVBoxLayout(container)
#         outer_layout.setContentsMargins(0, 0, 0, 0)
#         outer_layout.setSpacing(0)

#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         scroll.setFrameShape(QFrame.NoFrame)

#         inner = QWidget()
#         two_col = TwoColumnLayout(inner)
#         scroll.setWidget(inner)

#         outer_layout.addWidget(scroll)
#         return container, two_col

#     # -------------------------
#     # BEHAVIOR TAB
#     # -------------------------
#     def _init_behavior_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.behavior_layout = layout

#         # Behavior distribution
#         self.card_behavior_dist = ChartCard("Behavior Distribution", AnalyticsColors.BEHAVIOR)
#         self.behavior_layout.add_card(self.card_behavior_dist)

#         # Behavior timeline
#         self.card_behavior_timeline = ChartCard("Behavior Timeline", AnalyticsColors.BEHAVIOR)
#         self.behavior_layout.add_card(self.card_behavior_timeline)

#         # Behavior by time of day
#         self.card_behavior_by_hour = ChartCard("Behavior by Time of Day", AnalyticsColors.BEHAVIOR)
#         self.behavior_layout.add_card(self.card_behavior_by_hour)

#         # Longest streak (text card)
#         self.card_behavior_streak = AnalyticsCard("Longest Focus Streak")
#         self.behavior_streak_label = QLabel("No data yet.")
#         self.behavior_streak_label.setObjectName("AnalyticsText")
#         self.behavior_streak_label.setWordWrap(True)
#         self.card_behavior_streak.body_layout.addWidget(self.behavior_streak_label)
#         self.behavior_layout.add_card(self.card_behavior_streak)

#         self.tabs.addTab(w, "Behavior")

#     def _refresh_behavior_tab(self):
#         # -------------------------
#         # Distribution
#         # -------------------------
#         dist = self.engine.behavior_distribution()
#         self.card_behavior_dist.clear()
#         if dist:
#             behaviors = list(dist.keys())
#             values = list(dist.values())
#             x = range(len(behaviors))
#             bg = pg.BarGraphItem(
#                 x=list(x),
#                 height=values,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_behavior_dist.plot.addItem(bg)
#             ax = self.card_behavior_dist.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)

#         # -------------------------
#         # Behavior Timeline (color-band)
#         # -------------------------
#         timeline = self.engine.behavior_timeline()
#         self.card_behavior_timeline.clear()

#         times = timeline.get("times", [])
#         behaviors = timeline.get("behaviors", [])

#         if times and behaviors:
#             behavior_colors = {
#                 "Deep Work": "#0A84FF",
#                 "Deep Reading": "#BF5AF2",
#                 "Focused Interaction": "#30D158",
#                 "General Activity": "#FF9F0A",
#                 "Idle": "#8E8E93",
#             }

#             # Batch bars by behavior for performance
#             from collections import defaultdict
#             buckets = defaultdict(list)

#             for i, b in enumerate(behaviors):
#                 buckets[b].append(i)

#             for behavior, indices in buckets.items():
#                 color = behavior_colors.get(behavior, "#CCCCCC")
#                 bg = pg.BarGraphItem(
#                     x=indices,
#                     height=[1] * len(indices),
#                     width=1.0,
#                     brush=color,
#                     pen=None
#                 )
#                 self.card_behavior_timeline.plot.addItem(bg)

#             # Clean strip look
#             self.card_behavior_timeline.plot.getAxis("bottom").setVisible(False)
#             self.card_behavior_timeline.plot.getAxis("left").setVisible(False)
#             self.card_behavior_timeline.plot.setYRange(0, 1)

#             # -------------------------
#             # Legend (correct implementation)
#             # -------------------------
#             legend = pg.LegendItem(offset=(10, 10))
#             legend.setParentItem(self.card_behavior_timeline.plot.getPlotItem())
#             legend.setLabelTextColor("w")

#             for behavior, color in behavior_colors.items():
#                 sample = pg.PlotDataItem(pen=pg.mkPen(color, width=6))
#                 legend.addItem(sample, behavior)

#             # -------------------------
#             # Hover Tooltips (correct QPointF handling)
#             # -------------------------
#             def show_tooltip(pos):
#                 # pos is a QPointF
#                 if self.card_behavior_timeline.plot.sceneBoundingRect().contains(pos):
#                     mouse_point = self.card_behavior_timeline.plot.getPlotItem().vb.mapSceneToView(pos)
#                     idx = int(mouse_point.x())
#                     if 0 <= idx < len(behaviors):
#                         QtWidgets.QToolTip.showText(
#                             QtGui.QCursor.pos(),
#                             f"{times[idx][11:16]} — {behaviors[idx]}"
#                         )

#             self.card_behavior_timeline.plot.scene().sigMouseMoved.connect(show_tooltip)

#         # -------------------------
#         # Behavior by hour (bar)
#         # -------------------------
#         by_hour = self.engine.behavior_by_hour()
#         self.card_behavior_by_hour.clear()
#         if by_hour:
#             hours = sorted(by_hour.keys())
#             vals = [sum(by_hour[h].values()) for h in hours]
#             x = list(range(len(hours)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_behavior_by_hour.plot.addItem(bg)
#             labels = [f"{h:02d}:00" for h in hours]
#             ax = self.card_behavior_by_hour.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         # -------------------------
#         # Longest streak
#         # -------------------------
#         streak = self.engine.longest_behavior_streak()
#         if streak:
#             self.behavior_streak_label.setText(
#                 f"Longest streak: {streak['behavior']} for {streak['minutes']:.0f} minutes."
#             )
#         else:
#             self.behavior_streak_label.setText("No behavior streak data available yet.")

#     # -------------------------
#     # FATIGUE TAB
#     # -------------------------
#     def _init_fatigue_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.fatigue_layout = layout

#         self.card_fatigue_trend = ChartCard("Fatigue Trend", AnalyticsColors.FATIGUE)
#         self.fatigue_layout.add_card(self.card_fatigue_trend)

#         self.card_fatigue_by_behavior = ChartCard("Fatigue by Behavior", AnalyticsColors.FATIGUE)
#         self.fatigue_layout.add_card(self.card_fatigue_by_behavior)

#         self.card_fatigue_recovery = ChartCard("Fatigue Recovery After Breaks", AnalyticsColors.FATIGUE)
#         self.fatigue_layout.add_card(self.card_fatigue_recovery)

#         self.card_fatigue_peak = AnalyticsCard("Highest Fatigue Moment")
#         self.fatigue_peak_label = QLabel("No data yet.")
#         self.fatigue_peak_label.setObjectName("AnalyticsText")
#         self.fatigue_peak_label.setWordWrap(True)
#         self.card_fatigue_peak.body_layout.addWidget(self.fatigue_peak_label)
#         self.fatigue_layout.add_card(self.card_fatigue_peak)

#         self.tabs.addTab(w, "Fatigue")

#     def _refresh_fatigue_tab(self):
#         # -------------------------
#         # Trend (smooth line)
#         # -------------------------
#         trend = self.engine.fatigue_trend()
#         self.card_fatigue_trend.clear()

#         times = trend.get("times", [])
#         vals = trend.get("fatigue", [])

#         if times and vals:
#             # Plot fatigue trend
#             self.card_fatigue_trend.plot.plot(
#                 list(range(len(times))), vals,
#                 pen=self.card_fatigue_trend.smooth_pen(),
#                 antialias=True
#             )

#             # Force a stable Y-range to prevent collapse
#             self.card_fatigue_trend.plot.setYRange(0, 100)

#             # -------------------------
#             # Legend
#             # -------------------------
#             legend = pg.LegendItem(offset=(10, 10))
#             legend.setParentItem(self.card_fatigue_trend.plot.getPlotItem())

#             sample = pg.PlotDataItem(pen=pg.mkPen("#FF9500", width=2))
#             legend.addItem(sample, "Fatigue Level")

#             # -------------------------
#             # Hover Tooltips
#             # -------------------------
#             def show_fatigue_tooltip(pos):
#                 if self.card_fatigue_trend.plot.sceneBoundingRect().contains(pos):
#                     mp = self.card_fatigue_trend.plot.getPlotItem().vb.mapSceneToView(pos)
#                     idx = int(mp.x())
#                     if 0 <= idx < len(vals):
#                         QtWidgets.QToolTip.showText(
#                             QtGui.QCursor.pos(),
#                             f"{times[idx][11:16]} — Fatigue {vals[idx]:.0f}/100"
#                         )

#             self.card_fatigue_trend.plot.scene().sigMouseMoved.connect(show_fatigue_tooltip)

#         # -------------------------
#         # By behavior (bar)
#         # -------------------------
#         by_behavior = self.engine.fatigue_by_behavior()
#         self.card_fatigue_by_behavior.clear()

#         if by_behavior:
#             behaviors = list(by_behavior.keys())
#             vals = list(by_behavior.values())
#             x = list(range(len(behaviors)))

#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.FATIGUE
#             )
#             self.card_fatigue_by_behavior.plot.addItem(bg)

#             ax = self.card_fatigue_by_behavior.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)

#             self.card_fatigue_by_behavior.plot.setYRange(0, 100)

#         # -------------------------
#         # Recovery (smooth line)
#         # -------------------------
#         rec = self.engine.fatigue_recovery_after_breaks()
#         self.card_fatigue_recovery.clear()

#         rt = rec.get("times", [])
#         rv = rec.get("fatigue", [])

#         if rt and rv:
#             self.card_fatigue_recovery.plot.plot(
#                 list(range(len(rt))), rv,
#                 pen=self.card_fatigue_recovery.smooth_pen(),
#                 antialias=True
#             )
#             self.card_fatigue_recovery.plot.setYRange(0, 100)

#         # -------------------------
#         # Peak
#         # -------------------------
#         peak = self.engine.highest_fatigue_moment()
#         if peak:
#             self.fatigue_peak_label.setText(
#                 f"Highest fatigue: {peak['fatigue']:.0f}/100 at {peak['time']}."
#             )
#         else:
#             self.fatigue_peak_label.setText("No fatigue peak data available yet.")

#     # -------------------------
#     # BREAK TAB
#     # -------------------------
#     def _init_break_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.break_layout = layout

#         self.card_break_reasons = ChartCard("Break Reasons", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_reasons)

#         self.card_break_timing = ChartCard("Break Timing Quality", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_timing)

#         self.card_break_timeline = ChartCard("Break Events Timeline", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_timeline)

#         self.card_break_suppression = ChartCard("Break Suppression", AnalyticsColors.BREAK)
#         self.break_layout.add_card(self.card_break_suppression)

#         self.tabs.addTab(w, "Breaks")

#     def _refresh_break_tab(self):
#         # Reasons (bar)
#         reasons = self.engine.break_reasons()
#         self.card_break_reasons.clear()
#         if reasons:
#             labels = list(reasons.keys())
#             vals = list(reasons.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BREAK
#             )
#             self.card_break_reasons.plot.addItem(bg)
#             ax = self.card_break_reasons.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         # Timing quality (bar)
#         timing = self.engine.break_timing_quality()
#         self.card_break_timing.clear()
#         if timing:
#             labels = ["Early", "On Time", "Late"]
#             vals = [
#                 timing.get("early", 0),
#                 timing.get("on_time", 0),
#                 timing.get("late", 0),
#             ]
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BREAK
#             )
#             self.card_break_timing.plot.addItem(bg)
#             ax = self.card_break_timing.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         # Timeline (dots)
#         timeline = self.engine.break_events_timeline()
#         self.card_break_timeline.clear()
#         times = timeline.get("times", [])
#         if times:
#             x = list(range(len(times)))
#             y = [1] * len(times)
#             self.card_break_timeline.plot.plot(
#                 x, y,
#                 pen=None,
#                 symbol="o",
#                 symbolSize=6,
#                 symbolBrush=AnalyticsColors.BREAK
#             )
#             self.card_break_timeline.plot.getAxis("bottom").setVisible(False)
#             self.card_break_timeline.plot.getAxis("left").setVisible(False)

#         # Suppression (bar)
#         supp = self.engine.break_suppression_stats()
#         self.card_break_suppression.clear()
#         if supp:
#             labels = list(supp.keys())
#             vals = list(supp.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BREAK
#             )
#             self.card_break_suppression.plot.addItem(bg)
#             ax = self.card_break_suppression.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#     # -------------------------
#     # SUPPRESSION TAB
#     # -------------------------
#     def _init_suppression_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.supp_layout = layout

#         self.card_supp_counts = ChartCard("Suppression Counts", AnalyticsColors.SUPPRESSION)
#         self.supp_layout.add_card(self.card_supp_counts)

#         self.card_away_resets = AnalyticsCard("Away Resets")
#         self.away_resets_label = QLabel("No data yet.")
#         self.away_resets_label.setObjectName("AnalyticsText")
#         self.away_resets_label.setWordWrap(True)
#         self.card_away_resets.body_layout.addWidget(self.away_resets_label)
#         self.supp_layout.add_card(self.card_away_resets)

#         self.tabs.addTab(w, "Suppression")

#     def _refresh_suppression_tab(self):
#         counts = self.engine.suppression_counts()
#         self.card_supp_counts.clear()
#         if counts:
#             labels = list(counts.keys())
#             vals = list(counts.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.SUPPRESSION
#             )
#             self.card_supp_counts.plot.addItem(bg)
#             ax = self.card_supp_counts.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#         away = self.engine.away_resets_count()
#         self.away_resets_label.setText(
#             f"Away-based resets: {away}."
#         )

#     # -------------------------
#     # TIME OF DAY TAB
#     # -------------------------
#     def _init_time_of_day_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.tod_layout = layout

#         self.card_behavior_heatmap = ChartCard("Behavior Heatmap", AnalyticsColors.BEHAVIOR)
#         self.tod_layout.add_card(self.card_behavior_heatmap)

#         self.card_fatigue_heatmap = ChartCard("Fatigue Heatmap", AnalyticsColors.FATIGUE)
#         self.tod_layout.add_card(self.card_fatigue_heatmap)

#         self.card_break_heatmap = ChartCard("Break Heatmap", AnalyticsColors.BREAK)
#         self.tod_layout.add_card(self.card_break_heatmap)

#         self.card_supp_heatmap = ChartCard("Suppression Heatmap", AnalyticsColors.SUPPRESSION)
#         self.tod_layout.add_card(self.card_supp_heatmap)

#         self.tabs.addTab(w, "Time of Day")

#     def _plot_simple_heatmap(self, card: ChartCard, data: dict, color: str):
#         """
#         Simple 1D heatmap: hour -> value, rendered as colored bars.
#         """
#         card.clear()
#         if not data:
#             return

#         hours = sorted(data.keys())
#         vals = [data[h] for h in hours]
#         x = list(range(len(hours)))

#         bg = pg.BarGraphItem(
#             x=x,
#             height=vals,
#             width=0.8,
#             brush=color
#         )
#         card.plot.addItem(bg)

#         # Build hour labels
#         labels = [f"{h:02d}:00" for h in hours]

#         # ⭐ Prevent overlapping labels by thinning them
#         step = max(1, len(hours) // 8)   # show ~8 labels max
#         tick_positions = [(i, labels[i]) for i in range(0, len(labels), step)]

#         ax = card.plot.getAxis("bottom")
#         ax.setTicks([tick_positions])
#         ax.setVisible(True)

        
#     def _refresh_time_of_day_tab(self):
#         beh = self.engine.behavior_heatmap()
#         self._plot_simple_heatmap(self.card_behavior_heatmap, beh, AnalyticsColors.BEHAVIOR)

#         fat = self.engine.fatigue_heatmap()
#         self._plot_simple_heatmap(self.card_fatigue_heatmap, fat, AnalyticsColors.FATIGUE)

#         br = self.engine.break_heatmap()
#         self._plot_simple_heatmap(self.card_break_heatmap, br, AnalyticsColors.BREAK)

#         supp = self.engine.suppression_heatmap()
#         self._plot_simple_heatmap(self.card_supp_heatmap, supp, AnalyticsColors.SUPPRESSION)
#     # -------------------------
#     # WEEKLY TAB
#     # -------------------------
#     def _init_weekly_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.weekly_layout = layout

#         self.card_weekly_behavior = ChartCard("Weekly Behavior Distribution", AnalyticsColors.BEHAVIOR)
#         self.weekly_layout.add_card(self.card_weekly_behavior)

#         self.card_weekly_fatigue = ChartCard("Weekly Fatigue Trend", AnalyticsColors.FATIGUE)
#         self.weekly_layout.add_card(self.card_weekly_fatigue)

#         self.card_weekly_break_consistency = AnalyticsCard("Weekly Break Consistency")
#         self.weekly_break_label = QLabel("No data yet.")
#         self.weekly_break_label.setObjectName("AnalyticsText")
#         self.weekly_break_label.setWordWrap(True)
#         self.card_weekly_break_consistency.body_layout.addWidget(self.weekly_break_label)
#         self.weekly_layout.add_card(self.card_weekly_break_consistency)

#         self.card_weekly_suppression = ChartCard("Weekly Suppression", AnalyticsColors.SUPPRESSION)
#         self.weekly_layout.add_card(self.card_weekly_suppression)

#         self.tabs.addTab(w, "Weekly")

#     def _refresh_weekly_tab(self):
#         summary = self.engine.weekly_behavior_summary()
#         self.card_weekly_behavior.clear()
#         self.card_weekly_fatigue.clear()
#         self.card_weekly_suppression.clear()

#         if not summary:
#             self.weekly_break_label.setText("No weekly data available yet.")
#             return

#         # Behavior distribution (bar)
#         dist = summary.get("distribution", {})
#         if dist:
#             behaviors = list(dist.keys())
#             vals = list(dist.values())
#             x = list(range(len(behaviors)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_weekly_behavior.plot.addItem(bg)
#             ax = self.card_weekly_behavior.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)

#         # Fatigue trend (smooth line)
#         ft = summary.get("fatigue_trend", {})
#         days = ft.get("days", [])
#         fv = ft.get("fatigue", [])
#         if days and fv:
#             self.card_weekly_fatigue.plot.plot(
#                 list(range(len(days))), fv,
#                 pen=self.card_weekly_fatigue.smooth_pen(),
#                 antialias=True
#             )
#             self.card_weekly_fatigue.plot.setYRange(0, 100)

#         # Break consistency
#         cons = summary.get("break_consistency", None)
#         if cons is not None:
#             self.weekly_break_label.setText(
#                 f"Break consistency this week: {cons:.0f}/100."
#             )
#         else:
#             self.weekly_break_label.setText("No break consistency data for this week.")

#         # Suppression (bar)
#         supp = summary.get("suppression_counts", {})
#         if supp:
#             labels = list(supp.keys())
#             vals = list(supp.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.SUPPRESSION
#             )
#             self.card_weekly_suppression.plot.addItem(bg)
#             ax = self.card_weekly_suppression.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#     # -------------------------
#     # MONTHLY TAB
#     # -------------------------
#     def _init_monthly_tab(self):
#         w, layout = self._create_scrollable_tab()
#         self.monthly_layout = layout

#         self.card_monthly_behavior = ChartCard("Monthly Behavior Distribution", AnalyticsColors.BEHAVIOR)
#         self.monthly_layout.add_card(self.card_monthly_behavior)

#         self.card_monthly_fatigue = ChartCard("Monthly Fatigue Trend", AnalyticsColors.FATIGUE)
#         self.monthly_layout.add_card(self.card_monthly_fatigue)

#         self.card_monthly_break_consistency = AnalyticsCard("Monthly Break Consistency")
#         self.monthly_break_label = QLabel("No data yet.")
#         self.monthly_break_label.setObjectName("AnalyticsText")
#         self.monthly_break_label.setWordWrap(True)
#         self.card_monthly_break_consistency.body_layout.addWidget(self.monthly_break_label)
#         self.monthly_layout.add_card(self.card_monthly_break_consistency)

#         self.card_monthly_suppression = ChartCard("Monthly Suppression", AnalyticsColors.SUPPRESSION)
#         self.monthly_layout.add_card(self.card_monthly_suppression)

#         self.tabs.addTab(w, "Monthly")

#     def _refresh_monthly_tab(self):
#         summary = self.engine.monthly_behavior_summary()
#         self.card_monthly_behavior.clear()
#         self.card_monthly_fatigue.clear()
#         self.card_monthly_suppression.clear()

#         if not summary:
#             self.monthly_break_label.setText("No monthly data available yet.")
#             return

#         # Behavior distribution (bar)
#         dist = summary.get("distribution", {})
#         if dist:
#             behaviors = list(dist.keys())
#             vals = list(dist.values())
#             x = list(range(len(behaviors)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.BEHAVIOR
#             )
#             self.card_monthly_behavior.plot.addItem(bg)
#             ax = self.card_monthly_behavior.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, behaviors))])
#             ax.setVisible(True)

#         # Fatigue trend (smooth line)
#         ft = summary.get("fatigue_trend", {})
#         days = ft.get("days", [])
#         fv = ft.get("fatigue", [])
#         if days and fv:
#             self.card_monthly_fatigue.plot.plot(
#                 list(range(len(days))), fv,
#                 pen=self.card_monthly_fatigue.smooth_pen(),
#                 antialias=True
#             )
#             self.card_monthly_fatigue.plot.setYRange(0, 100)

#         # Break consistency
#         cons = summary.get("break_consistency", None)
#         if cons is not None:
#             self.monthly_break_label.setText(
#                 f"Break consistency this month: {cons:.0f}/100."
#             )
#         else:
#             self.monthly_break_label.setText("No break consistency data for this month.")

#         # Suppression (bar)
#         supp = summary.get("suppression_counts", {})
#         if supp:
#             labels = list(supp.keys())
#             vals = list(supp.values())
#             x = list(range(len(labels)))
#             bg = pg.BarGraphItem(
#                 x=x,
#                 height=vals,
#                 width=0.6,
#                 brush=AnalyticsColors.SUPPRESSION
#             )
#             self.card_monthly_suppression.plot.addItem(bg)
#             ax = self.card_monthly_suppression.plot.getAxis("bottom")
#             ax.setTicks([list(zip(x, labels))])
#             ax.setVisible(True)

#     # -------------------------
#     # INSIGHTS TAB
#     # -------------------------
#     def _init_insights_tab(self):
#         w = QWidget()
#         v = QVBoxLayout(w)
#         v.setContentsMargins(10, 10, 10, 10)
#         v.setSpacing(10)

#         self.insights_container = QVBoxLayout()
#         v.addLayout(self.insights_container)
#         v.addStretch()

#         self.tabs.addTab(w, "AI Insights")

#     def _refresh_insights_tab(self):
#         insights = self.engine.ai_insights()

#         # Clear old cards
#         while self.insights_container.count():
#             item = self.insights_container.takeAt(0)
#             if item.widget():
#                 item.widget().deleteLater()

#         # Add new cards
#         for text in insights:
#             card = QFrame()
#             card.setObjectName("InsightCard")
#             v = QVBoxLayout(card)
#             v.setContentsMargins(12, 12, 12, 12)

#             lbl = QLabel(text)
#             lbl.setObjectName("InsightText")
#             lbl.setWordWrap(True)
#             v.addWidget(lbl)

#             self.insights_container.addWidget(card)

#     # -------------------------
#     # GLOBAL REFRESH
#     # -------------------------
#     def refresh_all(self):
#         self._refresh_behavior_tab()
#         self._refresh_fatigue_tab()
#         self._refresh_break_tab()
#         self._refresh_suppression_tab()
#         self._refresh_time_of_day_tab()
#         self._refresh_weekly_tab()
#         self._refresh_monthly_tab()
#         self._refresh_insights_tab()




















# #25th March

# import pyqtgraph as pg
# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QFrame, 
#     QSizePolicy, QScrollArea, QGraphicsDropShadowEffect, QToolTip
# )
# from PySide6.QtCore import Qt, QPointF
# from PySide6.QtGui import QColor, QLinearGradient, QGradient, QBrush, QPen, QCursor
# from core.analytics_engine import AnalyticsEngine
# from PySide6 import QtWidgets, QtGui

# # ============================================================
# # PREMIUM DESIGN SYSTEM (Glassmorphism & High Contrast)
# # ============================================================
# STYLE_SHEET = """
# #AnalyticsSuitePage {
#     background-color: #0A0A0C;
# }
# #PageTitle {
#     font-size: 34px;
#     font-weight: 800;
#     color: #FFFFFF;
#     padding: 10px 0px;
# }
# #AnalyticsCard {
#     background-color: #1C1C1E;
#     border: 1px solid #2C2C2E;
#     border-radius: 20px;
# }
# #AnalyticsCardTitle {
#     font-size: 13px;
#     font-weight: 700;
#     color: #8E8E93;
#     text-transform: uppercase;
#     letter-spacing: 1.2px;
# }
# #AnalyticsValue {
#     font-size: 28px;
#     font-weight: 600;
#     color: #FFFFFF;
# }
# QTabWidget::pane {
#     border: none;
#     background: transparent;
# }
# QTabBar::tab {
#     background: transparent;
#     color: #636366;
#     padding: 12px 24px;
#     font-weight: 600;
#     font-size: 15px;
#     border-bottom: 2px solid transparent;
# }
# QTabBar::tab:selected {
#     color: #0A84FF;
#     border-bottom: 2px solid #0A84FF;
# }
# QScrollArea {
#     background-color: transparent;
#     border: none;
# }
# """

# class AnalyticsColors:
#     BEHAVIOR = "#0A84FF"
#     FATIGUE = "#FF9F0A"
#     BREAK = "#30D158"
#     SUPPRESSION = "#FF453A"
#     INSIGHT = "#BF5AF2"

# # ------------------------------------------------------------
# # PREMIUM CARD & CHART ENGINE
# # ------------------------------------------------------------
# class AnalyticsCard(QFrame):
#     def __init__(self, title: str):
#         super().__init__()
#         self.setObjectName("AnalyticsCard")
#         self.setMinimumHeight(320)
        
#         shadow = QGraphicsDropShadowEffect(self)
#         shadow.setBlurRadius(30)
#         shadow.setColor(QColor(0, 0, 0, 150))
#         shadow.setOffset(0, 10)
#         self.setGraphicsEffect(shadow)

#         self.layout = QVBoxLayout(self)
#         self.layout.setContentsMargins(22, 22, 22, 22)
        
#         self.title_label = QLabel(title)
#         self.title_label.setObjectName("AnalyticsCardTitle")
#         self.layout.addWidget(self.title_label)

#         self.body_layout = QVBoxLayout()
#         self.layout.addLayout(self.body_layout)

# class ChartCard(AnalyticsCard):
#     def __init__(self, title: str, accent_color: str):
#         super().__init__(title)
#         self.accent_color = accent_color
#         self.plot = pg.PlotWidget()
#         self.plot.setBackground(None)
#         self.plot.setAntialiasing(True)
        
#         pi = self.plot.getPlotItem()
#         pi.setMenuEnabled(False)
#         pi.buttonsHidden = True
#         pi.showGrid(x=False, y=True, alpha=0.1)
        
#         for ax in ["left", "bottom"]:
#             self.plot.getAxis(ax).setPen(None)
#             self.plot.getAxis(ax).setTextPen("#8E8E93")

#         self.body_layout.addWidget(self.plot)

#     def plot_premium_trend(self, x, y):
#         self.plot.clear()
#         if not x or not y: return
        
#         path = pg.PlotCurveItem(x, y, pen=pg.mkPen(self.accent_color, width=3))
#         self.plot.addItem(path)

#         # Gradient Fill Area
#         color = QColor(self.accent_color)
#         grad = QLinearGradient(0, 0, 0, 1)
#         grad.setCoordinateMode(QGradient.ObjectBoundingMode)
#         grad.setColorAt(0, QColor(color.red(), color.green(), color.blue(), 60))
#         grad.setColorAt(1, QColor(0, 0, 0, 0))
        
#         fill = pg.FillBetweenItem(path, pg.PlotCurveItem(x, [0]*len(x)), brush=QBrush(grad))
#         self.plot.addItem(fill)

# class AnalyticsSuitePage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("AnalyticsSuitePage")
#         self.setStyleSheet(STYLE_SHEET)
#         self.engine = AnalyticsEngine()

#         root = QVBoxLayout(self)
#         root.setContentsMargins(30, 30, 30, 30)

#         title = QLabel("Performance Analytics")
#         title.setObjectName("PageTitle")
#         root.addWidget(title)

#         self.tabs = QTabWidget()
#         root.addWidget(self.tabs)

#         # Initialize Tabs (Corrected Naming)
#         self._init_behavior_tab()
#         self._init_fatigue_tab()
#         self._init_break_tab()
#         self._init_suppression_tab()
#         self._init_insights_tab()

#         self.refresh_all()

#     def _create_scroll_grid(self):
#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         container = QWidget()
#         layout = QVBoxLayout(container)
#         layout.setSpacing(20)
#         scroll.setWidget(container)
#         return scroll, layout

#     def _add_row(self, layout, card1, card2=None):
#         row = QHBoxLayout()
#         row.setSpacing(20)
#         row.addWidget(card1)
#         if card2: row.addWidget(card2)
#         else: row.addStretch()
#         layout.addLayout(row)

#     def _init_behavior_tab(self):
#         scroll, layout = self._create_scroll_grid()
#         self.card_beh_dist = ChartCard("Activity Distribution", AnalyticsColors.BEHAVIOR)
#         self.card_beh_timeline = ChartCard("Focus Momentum", AnalyticsColors.BEHAVIOR)
#         self._add_row(layout, self.card_beh_dist, self.card_beh_timeline)
#         self.tabs.addTab(scroll, "Behavior")

#     def _init_fatigue_tab(self):
#         scroll, layout = self._create_scroll_grid()
#         self.card_fatigue_trend = ChartCard("Cognitive Load", AnalyticsColors.FATIGUE)
#         self.card_fatigue_recovery = ChartCard("Recovery Rate", AnalyticsColors.FATIGUE)
#         self._add_row(layout, self.card_fatigue_trend, self.card_fatigue_recovery)
#         self.tabs.addTab(scroll, "Fatigue")

#     def _init_break_tab(self):
#         scroll, layout = self._create_scroll_grid()
#         self.card_break_reasons = ChartCard("Break Triggers", AnalyticsColors.BREAK)
#         self._add_row(layout, self.card_break_reasons)
#         self.tabs.addTab(scroll, "Breaks")

#     def _init_suppression_tab(self):
#         scroll, layout = self._create_scroll_grid()
#         self.card_supp_counts = ChartCard("Interruption Stats", AnalyticsColors.SUPPRESSION)
#         self._add_row(layout, self.card_supp_counts)
#         self.tabs.addTab(scroll, "Suppression")

#     def _init_insights_tab(self):
#         self.ins_scroll = QScrollArea()
#         self.ins_scroll.setWidgetResizable(True)
#         self.ins_container = QWidget()
#         self.ins_vbox = QVBoxLayout(self.ins_container)
#         self.ins_vbox.setSpacing(15)
#         self.ins_scroll.setWidget(self.ins_container)
#         self.tabs.addTab(self.ins_scroll, "AI Insights")

#     def refresh_all(self):
#         # Behavior Data
#         dist = self.engine.behavior_distribution()
#         if dist:
#             self.card_beh_dist.plot_premium_trend(list(range(len(dist))), list(dist.values()))

#         # Fatigue Data
#         fatigue = self.engine.fatigue_trend()
#         if fatigue['fatigue']:
#             y = fatigue['fatigue']
#             self.card_fatigue_trend.plot_premium_trend(list(range(len(y))), y)

#         # Insights Data
#         insights = self.engine.ai_insights()
#         while self.ins_vbox.count():
#             self.ins_vbox.takeAt(0).widget().deleteLater()
#         for text in insights:
#             lbl = QLabel(text)
#             lbl.setStyleSheet("color: #E5E5E7; padding: 20px; background: #1C1C1E; border-radius: 15px; border: 1px solid #2C2C2E;")
#             lbl.setWordWrap(True)
#             self.ins_vbox.addWidget(lbl)








# # Better the the one below it

# import pyqtgraph as pg
# from collections import defaultdict
# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QFrame, 
#     QSizePolicy, QScrollArea, QGraphicsDropShadowEffect, QToolTip
# )
# from PySide6.QtCore import Qt, QPointF
# from PySide6.QtGui import QColor, QLinearGradient, QGradient, QBrush, QPen, QCursor
# from core.analytics_engine import AnalyticsEngine
# from PySide6 import QtWidgets, QtGui

# # ============================================================
# # PREMIUM ADAPTIVE UI SYSTEM
# # ============================================================
# STYLE_SHEET = """
# #AnalyticsSuitePage { background-color: transparent; }
# #PageTitle { 
#     font-size: 34px; font-weight: 800; 
#     color: palette(text); padding: 15px 5px; 
# }
# #AnalyticsCard { 
#     background-color: palette(window); 
#     border: 1px solid palette(midlight); 
#     border-radius: 20px; 
# }
# #AnalyticsCardTitle { 
#     font-size: 11px; font-weight: 700; color: #8E8E93; 
#     text-transform: uppercase; letter-spacing: 1.2px; 
# }
# #AnalyticsText { font-size: 16px; color: palette(text); font-weight: 500; }
# QTabWidget::pane { border: none; background: transparent; }
# QTabBar::tab { 
#     background: transparent; color: #8E8E93; 
#     padding: 12px 24px; font-weight: 600; font-size: 15px; 
# }
# QTabBar::tab:selected { color: #007AFF; border-bottom: 2px solid #007AFF; }
# QScrollArea { background-color: transparent; border: none; }
# """

# class AnalyticsColors:
#     BEHAVIOR = "#007AFF"   
#     FATIGUE = "#FF9500"    
#     BREAK = "#28CD41"      
#     SUPPRESSION = "#FF3B30" 
#     INSIGHT = "#AF52DE"    

# class TwoColumnLayout(QVBoxLayout):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setContentsMargins(10, 10, 10, 10)
#         self.setSpacing(20)
#         self.row_layout = None
#         self._items_in_row = 0

#     def add_card(self, card: QWidget):
#         if self.row_layout is None or self._items_in_row >= 2:
#             self.row_layout = QHBoxLayout()
#             self.row_layout.setSpacing(20)
#             self.addLayout(self.row_layout)
#             self._items_in_row = 0
#         self.row_layout.addWidget(card)
#         self._items_in_row += 1

# class AnalyticsCard(QFrame):
#     def __init__(self, title: str):
#         super().__init__()
#         self.setObjectName("AnalyticsCard")
#         self.setMinimumHeight(320)
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)
#         self.title_label = QLabel(title)
#         self.title_label.setObjectName("AnalyticsCardTitle")
#         layout.addWidget(self.title_label)
#         self.body_layout = QVBoxLayout()
#         layout.addLayout(self.body_layout)

# class ChartCard(AnalyticsCard):
#     def __init__(self, title: str, color: str):
#         super().__init__(title)
#         self.color = color
#         self.plot = pg.PlotWidget()
#         self.plot.setBackground(None)
#         pi = self.plot.getPlotItem()
#         pi.setMenuEnabled(False)
#         pi.buttonsHidden = True
#         pi.showGrid(x=False, y=True, alpha=0.1)
#         for ax_name in ["left", "bottom"]:
#             ax = self.plot.getAxis(ax_name)
#             ax.setPen(None)
#             ax.setTextPen("#8E8E93")
#         self.body_layout.addWidget(self.plot)

#     def smooth_pen(self):
#         pen = pg.mkPen(self.color, width=3)
#         pen.setCapStyle(Qt.RoundCap)
#         return pen

# class AnalyticsSuitePage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("AnalyticsSuitePage")
#         self.setStyleSheet(STYLE_SHEET)
#         self.engine = AnalyticsEngine()

#         root = QVBoxLayout(self)
#         root.setContentsMargins(25, 25, 25, 25)

#         header = QLabel("Performance Analytics")
#         header.setObjectName("PageTitle")
#         root.addWidget(header)

#         self.tabs = QTabWidget()
#         root.addWidget(self.tabs)

#         self._init_behavior_tab()
#         self._init_fatigue_tab()
#         self._init_break_tab()
#         self._init_suppression_tab()
#         self._init_time_of_day_tab()
#         self._init_weekly_tab()
#         self._init_monthly_tab()
#         self._init_insights_tab()
#         self.refresh_all()

#     def _create_scrollable_tab(self):
#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         container = QWidget()
#         layout = TwoColumnLayout(container)
#         scroll.setWidget(container)
#         return scroll, layout

#     def _init_behavior_tab(self):
#         w, l = self._create_scrollable_tab()
#         self.card_beh_dist = ChartCard("Distribution", AnalyticsColors.BEHAVIOR)
#         self.card_beh_timeline = ChartCard("Timeline", AnalyticsColors.BEHAVIOR)
#         self.card_beh_streak = AnalyticsCard("Focus Streak")
#         self.lbl_streak = QLabel("...")
#         self.lbl_streak.setObjectName("AnalyticsText")
#         self.card_beh_streak.body_layout.addWidget(self.lbl_streak)
#         l.add_card(self.card_beh_dist); l.add_card(self.card_beh_timeline); l.add_card(self.card_beh_streak)
#         self.tabs.addTab(w, "Behavior")

#     def _init_fatigue_tab(self):
#         w, l = self._create_scrollable_tab()
#         self.card_fat_trend = ChartCard("Cognitive Load", AnalyticsColors.FATIGUE)
#         self.card_fat_rec = ChartCard("Recovery Rate", AnalyticsColors.FATIGUE)
#         l.add_card(self.card_fat_trend); l.add_card(self.card_fat_rec)
#         self.tabs.addTab(w, "Fatigue")

#     def _init_break_tab(self):
#         w, l = self._create_scrollable_tab()
#         self.card_brk_reasons = ChartCard("Break Reasons", AnalyticsColors.BREAK)
#         l.add_card(self.card_brk_reasons)
#         self.tabs.addTab(w, "Breaks")

#     def _init_suppression_tab(self):
#         w, l = self._create_scrollable_tab()
#         self.card_supp_stats = ChartCard("Suppression Stats", AnalyticsColors.SUPPRESSION)
#         l.add_card(self.card_supp_stats)
#         self.tabs.addTab(w, "Suppression")

#     def _init_time_of_day_tab(self):
#         w, l = self._create_scrollable_tab()
#         self.card_tod_heatmap = ChartCard("Hourly Heatmap", AnalyticsColors.BEHAVIOR)
#         l.add_card(self.card_tod_heatmap)
#         self.tabs.addTab(w, "Time of Day")

#     def _init_weekly_tab(self):
#         w, l = self._create_scrollable_tab()
#         self.card_wk_beh = ChartCard("Weekly Overview", AnalyticsColors.BEHAVIOR)
#         l.add_card(self.card_wk_beh)
#         self.tabs.addTab(w, "Weekly")

#     def _init_monthly_tab(self):
#         w, l = self._create_scrollable_tab()
#         self.card_mo_beh = ChartCard("Monthly Overview", AnalyticsColors.BEHAVIOR)
#         l.add_card(self.card_mo_beh)
#         self.tabs.addTab(w, "Monthly")

#     def _init_insights_tab(self):
#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         container = QWidget()
#         self.ins_vbox = QVBoxLayout(container)
#         self.ins_vbox.addStretch()
#         scroll.setWidget(container)
#         self.tabs.addTab(scroll, "AI Insights")

#     def _refresh_behavior_tab(self):
#         dist = self.engine.behavior_distribution()
#         if dist:
#             self.card_beh_dist.plot.clear()
#             x = list(range(len(dist)))
#             bg = pg.BarGraphItem(x=x, height=list(dist.values()), width=0.6, brush=AnalyticsColors.BEHAVIOR)
#             self.card_beh_dist.plot.addItem(bg)
#             self.card_beh_dist.plot.getAxis('bottom').setTicks([list(zip(x, dist.keys()))])
        
#         streak = self.engine.longest_behavior_streak()
#         if streak: self.lbl_streak.setText(f"{streak['behavior']}: {streak['minutes']:.0f} mins")

#     def _refresh_fatigue_tab(self):
#         f = self.engine.fatigue_trend()
#         if f.get('fatigue'):
#             self.card_fat_trend.plot.clear()
#             self.card_fat_trend.plot.plot(list(range(len(f['fatigue']))), f['fatigue'], pen=self.card_fat_trend.smooth_pen())

#     def _refresh_break_tab(self):
#         r = self.engine.break_reasons()
#         if r:
#             self.card_brk_reasons.plot.clear()
#             bg = pg.BarGraphItem(x=list(range(len(r))), height=list(r.values()), width=0.6, brush=AnalyticsColors.BREAK)
#             self.card_brk_reasons.plot.addItem(bg)

#     def _refresh_suppression_tab(self):
#         s = self.engine.suppression_counts()
#         if s:
#             self.card_supp_stats.plot.clear()
#             bg = pg.BarGraphItem(x=list(range(len(s))), height=list(s.values()), width=0.6, brush=AnalyticsColors.SUPPRESSION)
#             self.card_supp_stats.plot.addItem(bg)

#     def _refresh_time_of_day_tab(self): pass
#     def _refresh_weekly_tab(self): pass
#     def _refresh_monthly_tab(self): pass

#     def _refresh_insights_tab(self):
#         while self.ins_vbox.count() > 1:
#             item = self.ins_vbox.takeAt(0)
#             if item.widget(): item.widget().deleteLater()
        
#         for text in self.engine.ai_insights():
#             card = QFrame()
#             card.setStyleSheet("background: palette(midlight); border-radius: 15px; border: 1px solid palette(mid);")
#             v = QVBoxLayout(card)
#             lbl = QLabel(text)
#             lbl.setObjectName("InsightText")
#             lbl.setWordWrap(True)
#             v.addWidget(lbl)
#             self.ins_vbox.insertWidget(self.ins_vbox.count() - 1, card)

#     def refresh_all(self):
#         self._refresh_behavior_tab()
#         self._refresh_fatigue_tab()
#         self._refresh_break_tab()
#         self._refresh_suppression_tab()
#         self._refresh_time_of_day_tab()
#         self._refresh_weekly_tab()
#         self._refresh_monthly_tab()
#         self._refresh_insights_tab()














# # Not to my taste


# import pyqtgraph as pg
# from collections import defaultdict
# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QFrame, 
#     QSizePolicy, QScrollArea, QGraphicsDropShadowEffect
# )
# from PySide6.QtCore import Qt, QPointF
# from PySide6.QtGui import QColor, QLinearGradient, QGradient, QBrush, QPen, QCursor
# from core.analytics_engine import AnalyticsEngine
# from PySide6 import QtWidgets, QtGui

# # ============================================================
# # MACOS PREMIUM DESIGN SYSTEM (HIG COMPLIANT)
# # ============================================================
# STYLE_SHEET = """
# #AnalyticsSuitePage { background-color: palette(window); }
# #PageTitle { 
#     font-size: 28px; font-weight: 700; 
#     color: palette(text); padding: 10px 0px 20px 5px; 
#     font-family: 'SF Pro Display', 'Helvetica Neue', Arial;
# }
# #AnalyticsCard { 
#     background-color: palette(alternate-base); 
#     border: 1px solid palette(midlight); 
#     border-radius: 12px; 
# }
# #AnalyticsCardTitle { 
#     font-size: 13px; font-weight: 600; color: palette(placeholder-text); 
#     text-transform: uppercase; letter-spacing: 0.5px; 
# }
# #AnalyticsText { 
#     font-size: 15px; color: palette(text); font-weight: 400; 
# }
# QTabWidget::pane { border-top: 1px solid palette(midlight); background: transparent; }
# QTabBar::tab { 
#     background: transparent; color: palette(placeholder-text); 
#     padding: 10px 20px; font-weight: 500; font-size: 14px; 
# }
# QTabBar::tab:selected { color: #007AFF; border-bottom: 2px solid #007AFF; }
# QScrollArea { background-color: transparent; border: none; }
# """

# class AnalyticsColors:
#     # Official Apple System Colors
#     BLUE = "#007AFF"
#     ORANGE = "#FF9500"
#     GREEN = "#34C759"
#     RED = "#FF3B30"
#     PURPLE = "#AF52DE"
#     GRAY = "#8E8E93"

# class TwoColumnLayout(QVBoxLayout):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setContentsMargins(0, 10, 0, 10)
#         self.setSpacing(16)
#         self.row_layout = None
#         self._items_in_row = 0

#     def add_card(self, card: QWidget):
#         if self.row_layout is None or self._items_in_row >= 2:
#             self.row_layout = QHBoxLayout()
#             self.row_layout.setSpacing(16)
#             self.addLayout(self.row_layout)
#             self._items_in_row = 0
#         self.row_layout.addWidget(card)
#         self._items_in_row += 1

# class AnalyticsCard(QFrame):
#     def __init__(self, title: str):
#         super().__init__()
#         self.setObjectName("AnalyticsCard")
#         self.setMinimumHeight(300)
        
#         # macOS Soft Shadow
#         shadow = QGraphicsDropShadowEffect(self)
#         shadow.setBlurRadius(15)
#         shadow.setXOffset(0)
#         shadow.setYOffset(4)
#         shadow.setColor(QColor(0, 0, 0, 30))
#         self.setGraphicsEffect(shadow)

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(18, 18, 18, 18)
#         self.title_label = QLabel(title)
#         self.title_label.setObjectName("AnalyticsCardTitle")
#         layout.addWidget(self.title_label)
#         self.body_layout = QVBoxLayout()
#         layout.addLayout(self.body_layout)

# class ChartCard(AnalyticsCard):
#     def __init__(self, title: str, color: str):
#         super().__init__(title)
#         self.color = color
#         self.plot = pg.PlotWidget()
#         self.plot.setBackground(None)
#         self.plot.setAntialiasing(True)
        
#         pi = self.plot.getPlotItem()
#         pi.setMenuEnabled(False)
#         if hasattr(pi, "buttons"):
#             for btn in pi.buttons.values(): btn.hide()

#         self.plot.setMouseEnabled(x=False, y=False)
#         self.plot.getAxis("left").setVisible(False)
#         self.plot.getAxis("bottom").setPen(None)
#         self.plot.getAxis("bottom").setTextPen(AnalyticsColors.GRAY)
#         self.body_layout.addWidget(self.plot)

#     def smooth_pen(self):
#         pen = pg.mkPen(self.color, width=2.5)
#         pen.setCapStyle(Qt.RoundCap)
#         return pen
    
# class AnalyticsSuitePage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("AnalyticsSuitePage")
#         self.setStyleSheet(STYLE_SHEET)
#         self.engine = AnalyticsEngine()

#         root = QVBoxLayout(self)
#         root.setContentsMargins(30, 20, 30, 20)

#         header_container = QHBoxLayout()
#         header = QLabel("Performance Analytics")
#         header.setObjectName("PageTitle")
#         header_container.addWidget(header)
#         header_container.addStretch()
        
#         # macOS Style Refresh Button (Optional but Premium)
#         self.refresh_btn = QtWidgets.QPushButton("Refresh")
#         self.refresh_btn.setFixedWidth(80)
#         self.refresh_btn.clicked.connect(self.refresh_all)
#         header_container.addWidget(self.refresh_btn)
#         root.addLayout(header_container)

#         self.tabs = QTabWidget()
#         root.addWidget(self.tabs)

#         self._init_all_tabs()
#         self.refresh_all()

#     def _create_scrollable_tab(self):
#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         container = QWidget()
#         layout = TwoColumnLayout(container)
#         scroll.setWidget(container)
#         return scroll, layout

#     def _init_all_tabs(self):
#         # 1. Behavior
#         w1, l1 = self._create_scrollable_tab()
#         self.card_beh_dist = ChartCard("Distribution", AnalyticsColors.BLUE)
#         self.card_beh_timeline = ChartCard("Activity Timeline", AnalyticsColors.PURPLE)
#         self.card_beh_hour = ChartCard("By Hour", AnalyticsColors.BLUE)
#         self.card_beh_streak = AnalyticsCard("Focus Streak")
#         self.lbl_streak = QLabel("Calculating..."); self.lbl_streak.setObjectName("AnalyticsText")
#         self.card_beh_streak.body_layout.addWidget(self.lbl_streak)
#         for c in [self.card_beh_dist, self.card_beh_timeline, self.card_beh_hour, self.card_beh_streak]: l1.add_card(c)
#         self.tabs.addTab(w1, "Behavior")

#         # 2. Fatigue
#         w2, l2 = self._create_scrollable_tab()
#         self.card_fat_trend = ChartCard("Cognitive Load", AnalyticsColors.ORANGE)
#         self.card_fat_beh = ChartCard("Impact by Task", AnalyticsColors.ORANGE)
#         self.card_fat_rec = ChartCard("Recovery Efficiency", AnalyticsColors.GREEN)
#         self.card_fat_peak = AnalyticsCard("Critical Fatigue")
#         self.lbl_peak = QLabel("..."); self.lbl_peak.setObjectName("AnalyticsText")
#         self.card_fat_peak.body_layout.addWidget(self.lbl_peak)
#         for c in [self.card_fat_trend, self.card_fat_beh, self.card_fat_rec, self.card_fat_peak]: l2.add_card(c)
#         self.tabs.addTab(w2, "Fatigue")

#         # 3. Breaks
#         w3, l3 = self._create_scrollable_tab()
#         self.card_brk_reasons = ChartCard("Break Context", AnalyticsColors.GREEN)
#         self.card_brk_quality = ChartCard("Timing Quality", AnalyticsColors.GREEN)
#         l3.add_card(self.card_brk_reasons); l3.add_card(self.card_brk_quality)
#         self.tabs.addTab(w3, "Breaks")

#         # 4. Suppression / 5. TOD / 6. Weekly / 7. Monthly (Combined for space)
#         self._init_data_tabs()

#         # 8. AI Insights
#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         container = QWidget()
#         self.ins_vbox = QVBoxLayout(container)
#         self.ins_vbox.setContentsMargins(10, 20, 10, 20)
#         self.ins_vbox.addStretch()
#         scroll.setWidget(container)
#         self.tabs.addTab(scroll, "AI Insights")

#     def _init_data_tabs(self):
#         # Time of Day
#         w, l = self._create_scrollable_tab()
#         self.card_tod_heat = ChartCard("Productivity Heatmap", AnalyticsColors.BLUE)
#         l.add_card(self.card_tod_heat)
#         self.tabs.addTab(w, "Time of Day")
        
#         # Weekly
#         w_wk, l_wk = self._create_scrollable_tab()
#         self.card_wk_beh = ChartCard("Weekly Overview", AnalyticsColors.PURPLE)
#         l_wk.add_card(self.card_wk_beh)
#         self.tabs.addTab(w_wk, "Weekly")
        
#         # Monthly
#         w_mo, l_mo = self._create_scrollable_tab()
#         self.card_mo_beh = ChartCard("Monthly Trends", AnalyticsColors.BLUE)
#         l_mo.add_card(self.card_mo_beh)
#         self.tabs.addTab(w_mo, "Monthly")

#         # Suppression
#         w_s, l_s = self._create_scrollable_tab()
#         self.card_supp = ChartCard("Suppression Frequency", AnalyticsColors.RED)
#         l_s.add_card(self.card_supp)
#         self.tabs.addTab(w_s, "Suppression")

#     def _refresh_behavior_tab(self):
#         dist = self.engine.behavior_distribution()
#         self.card_beh_dist.plot.clear()
#         if dist:
#             x = range(len(dist))
#             bg = pg.BarGraphItem(x=list(x), height=list(dist.values()), width=0.5, 
#                                 brush=AnalyticsColors.BLUE, pen=pg.mkPen(None))
#             self.card_beh_dist.plot.addItem(bg)
#             self.card_beh_dist.plot.getAxis("bottom").setTicks([list(zip(x, dist.keys()))])

#         timeline = self.engine.behavior_timeline()
#         self.card_beh_timeline.plot.clear()
#         if timeline.get("behaviors"):
#             # macOS Style Strip Chart
#             for i, b in enumerate(timeline["behaviors"]):
#                 color = AnalyticsColors.BLUE if "Deep" in b else AnalyticsColors.GRAY
#                 bg = pg.BarGraphItem(x=[i], height=[1], width=1, brush=color, pen=None)
#                 self.card_beh_timeline.plot.addItem(bg)
#             self.card_beh_timeline.plot.setYRange(0, 1)

#         streak = self.engine.longest_behavior_streak()
#         if streak: self.lbl_streak.setText(f"You maintained '{streak['behavior']}' for {streak['minutes']:.0f} mins.")

#     def _refresh_fatigue_tab(self):
#         trend = self.engine.fatigue_trend()
#         self.card_fat_trend.plot.clear()
#         if trend.get("fatigue"):
#             # Premium Gradient Pen Replacement
#             path = self.card_fat_trend.plot.plot(trend["fatigue"], pen=self.card_fat_trend.smooth_pen())
#             self.card_fat_trend.plot.setYRange(0, 100)
        
#         peak = self.engine.highest_fatigue_moment()
#         if peak: self.lbl_peak.setText(f"Peak detected at {peak['time']} ({peak['fatigue']:.0f}/100)")

#     def _refresh_insights_tab(self):
#         while self.ins_vbox.count() > 1:
#             item = self.ins_vbox.takeAt(0)
#             if item.widget(): item.widget().deleteLater()
        
#         for text in self.engine.ai_insights():
#             card = QFrame()
#             card.setStyleSheet("background: palette(alternate-base); border-radius: 12px; border: 1px solid palette(midlight);")
#             v = QVBoxLayout(card)
#             lbl = QLabel(text)
#             lbl.setWordWrap(True)
#             lbl.setStyleSheet("font-size: 14px; line-height: 1.4;")
#             v.addWidget(lbl)
#             self.ins_vbox.insertWidget(self.ins_vbox.count() - 1, card)

#     def refresh_all(self):
#         """Universal refresh for all premium data views."""
#         self._refresh_behavior_tab()
#         self._refresh_fatigue_tab()
#         self._refresh_insights_tab()
#         # Additional heatmaps/weekly/monthly follow same pattern












# # Not premium

# import pyqtgraph as pg
# from collections import defaultdict
# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QFrame, 
#     QSizePolicy, QScrollArea, QGraphicsDropShadowEffect, QToolTip, QPushButton
# )
# from PySide6.QtCore import Qt, QPointF
# from PySide6.QtGui import QColor, QLinearGradient, QBrush, QPen, QCursor, QFont
# from core.analytics_engine import AnalyticsEngine
# from PySide6 import QtWidgets, QtGui

# # ============================================================
# # UNIVERSAL PREMIUM DESIGN SYSTEM
# # ============================================================
# STYLE_SHEET = """
# #AnalyticsSuitePage { background-color: palette(window); }
# #PageTitle { 
#     font-size: 26px; font-weight: 700; color: palette(text); 
#     padding: 10px 5px; font-family: 'SF Pro Display', 'Segoe UI', sans-serif;
# }
# #AnalyticsCard { 
#     background-color: palette(alternate-base); 
#     border: 1px solid palette(midlight); 
#     border-radius: 14px; 
# }
# #AnalyticsCardTitle { 
#     font-size: 12px; font-weight: 700; color: #8E8E93; 
#     text-transform: uppercase; letter-spacing: 1px; 
# }
# #BigMetric { font-size: 32px; font-weight: 700; color: palette(text); }
# #SubMetric { font-size: 14px; color: #8E8E93; }

# QTabWidget::pane { border-top: 1px solid palette(midlight); top: -1px; }
# QTabBar::tab { 
#     background: transparent; color: #8E8E93; padding: 12px 30px; 
#     font-weight: 600; font-size: 14px; 
# }
# QTabBar::tab:selected { color: #007AFF; border-bottom: 2px solid #007AFF; }
# QScrollArea { background-color: transparent; border: none; }
# """

# class AnalyticsColors:
#     ACCENT = "#007AFF"   # Apple Blue
#     ENERGY = "#FF9500"   # Apple Orange
#     RECOVERY = "#34C759" # Apple Green
#     DANGER = "#FF3B30"   # Apple Red
#     NEUTRAL = "#8E8E93"

# class ChartCard(QFrame):
#     """A polished container for any chart or metric."""
#     def __init__(self, title: str, height=320):
#         super().__init__()
#         self.setObjectName("AnalyticsCard")
#         self.setMinimumHeight(height)
        
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)
        
#         self.title_label = QLabel(title)
#         self.title_label.setObjectName("AnalyticsCardTitle")
#         layout.addWidget(self.title_label)
        
#         self.body = QVBoxLayout()
#         layout.addLayout(self.body)

#     def add_plot(self):
#         plot = pg.PlotWidget()
#         plot.setBackground(None)
#         plot.setAntialiasing(True)
#         pi = plot.getPlotItem()
#         pi.setMenuEnabled(False)
#         plot.setMouseEnabled(x=False, y=False)
#         plot.getAxis("left").setVisible(False)
#         plot.getAxis("bottom").setPen(None)
#         plot.getAxis("bottom").setTextPen("#8E8E93")
#         if hasattr(pi, "buttons"):
#             for btn in pi.buttons.values(): btn.hide()
#         self.body.addWidget(plot)
#         return plot

# # ============================================================
# # MAIN INTERFACE
# # ============================================================
# class AnalyticsSuitePage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("AnalyticsSuitePage")
#         self.setStyleSheet(STYLE_SHEET)
#         self.engine = AnalyticsEngine()

#         root = QVBoxLayout(self)
#         root.setContentsMargins(30, 25, 30, 25)

#         # Header
#         header_layout = QHBoxLayout()
#         title = QLabel("Performance Insights")
#         title.setObjectName("PageTitle")
#         header_layout.addWidget(title)
#         header_layout.addStretch()
        
#         self.refresh_btn = QPushButton("Refresh Data")
#         self.refresh_btn.setCursor(Qt.PointingHandCursor)
#         self.refresh_btn.clicked.connect(self.refresh_all)
#         header_layout.addWidget(self.refresh_btn)
#         root.addLayout(header_layout)

#         # 3-Tab Structure
#         self.tabs = QTabWidget()
#         self.tabs.setObjectName("MainTabs")
#         root.addWidget(self.tabs)

#         self._init_focus_tab()     # Tab 1: What I did (Behavior)
#         self._init_recovery_tab()  # Tab 2: How I feel (Fatigue + Breaks)
#         self._init_trends_tab()    # Tab 3: Long term (Weekly/Monthly + AI)

#         self.refresh_all()
    
#     def _create_scroll_content(self):
#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         container = QWidget()
#         layout = QVBoxLayout(container)
#         layout.setSpacing(20)
#         layout.setContentsMargins(0, 20, 0, 20)
#         scroll.setWidget(container)
#         return scroll, layout

#     def _init_focus_tab(self):
#         scroll, layout = self._create_scroll_content()
        
#         # Row 1: Distribution & Timeline
#         row1 = QHBoxLayout()
#         self.card_dist = ChartCard("Activity Distribution")
#         self.plot_dist = self.card_dist.add_plot()
        
#         self.card_timeline = ChartCard("Deep Work Timeline")
#         self.plot_timeline = self.card_timeline.add_plot()
        
#         row1.addWidget(self.card_dist); row1.addWidget(self.card_timeline)
#         layout.addLayout(row1)

#         # Row 2: Heatmap & Streak
#         row2 = QHBoxLayout()
#         self.card_heatmap = ChartCard("Productivity Heatmap")
#         self.plot_heatmap = self.card_heatmap.add_plot()
        
#         self.card_streak = ChartCard("Focus Streak")
#         self.val_streak = QLabel("0m"); self.val_streak.setObjectName("BigMetric")
#         self.sub_streak = QLabel("Longest session today"); self.sub_streak.setObjectName("SubMetric")
#         self.card_streak.body.addStretch()
#         self.card_streak.body.addWidget(self.val_streak, alignment=Qt.AlignCenter)
#         self.card_streak.body.addWidget(self.sub_streak, alignment=Qt.AlignCenter)
#         self.card_streak.body.addStretch()
        
#         row2.addWidget(self.card_heatmap); row2.addWidget(self.card_streak)
#         layout.addLayout(row2)
        
#         self.tabs.addTab(scroll, "Focus")

#     def _init_recovery_tab(self):
#         scroll, layout = self._create_scroll_content()
        
#         # Fatigue Trend (Wide)
#         self.card_fatigue = ChartCard("Cognitive Load Trend")
#         self.plot_fatigue = self.card_fatigue.add_plot()
#         layout.addWidget(self.card_fatigue)

#         # Break Stats Row
#         row2 = QHBoxLayout()
#         self.card_break_q = ChartCard("Break Quality")
#         self.plot_break_q = self.card_break_q.add_plot()
        
#         self.card_recovery = ChartCard("Recovery Rate")
#         self.plot_recovery = self.card_recovery.add_plot()
        
#         row2.addWidget(self.card_break_q); row2.addWidget(self.card_recovery)
#         layout.addLayout(row2)

#         self.tabs.addTab(scroll, "Recovery")

#     def _init_trends_tab(self):
#         scroll, layout = self._create_scroll_content()
        
#         # AI Insights Section
#         self.insight_label = QLabel("Analyzing your patterns...")
#         self.insight_label.setObjectName("AnalyticsText")
#         self.insight_label.setWordWrap(True)
        
#         insight_card = ChartCard("AI Recommendations", height=180)
#         insight_card.body.addWidget(self.insight_label)
#         layout.addWidget(insight_card)

#         # Weekly Comparison
#         self.card_weekly = ChartCard("Weekly Efficiency")
#         self.plot_weekly = self.card_weekly.add_plot()
#         layout.addWidget(self.card_weekly)

#         self.tabs.addTab(scroll, "Trends")

#     def refresh_all(self):
#         # --- FOCUS DATA ---
#         dist = self.engine.behavior_distribution()
#         self.plot_dist.clear()
#         if dist:
#             x = range(len(dist))
#             bg = pg.BarGraphItem(x=list(x), height=list(dist.values()), width=0.5, brush=AnalyticsColors.ACCENT)
#             self.plot_dist.addItem(bg)
#             self.plot_dist.getAxis("bottom").setTicks([list(zip(x, dist.keys()))])

#         timeline = self.engine.behavior_timeline()
#         self.plot_timeline.clear()
#         if timeline.get("behaviors"):
#             for i, b in enumerate(timeline["behaviors"]):
#                 color = AnalyticsColors.ACCENT if "Deep" in b else AnalyticsColors.NEUTRAL
#                 bg = pg.BarGraphItem(x=[i], height=[1], width=1, brush=color, pen=None)
#                 self.plot_timeline.addItem(bg)
#             self.plot_timeline.setYRange(0, 1)

#         streak = self.engine.longest_behavior_streak()
#         if streak: 
#             self.val_streak.setText(f"{streak['minutes']:.0f}m")
#             self.sub_streak.setText(f"In {streak['behavior']}")

#         # Heatmap (simplified tod logic)
#         tod = self.engine.behavior_heatmap()
#         self.plot_heatmap.clear()
#         if tod:
#             x = range(len(tod))
#             bg = pg.BarGraphItem(x=list(x), height=list(tod.values()), width=0.8, brush=AnalyticsColors.ACCENT)
#             self.plot_heatmap.addItem(bg)

#         # --- RECOVERY DATA ---
#         trend = self.engine.fatigue_trend()
#         self.plot_fatigue.clear()
#         if trend.get("fatigue"):
#             pen = pg.mkPen(AnalyticsColors.ENERGY, width=3)
#             self.plot_fatigue.plot(trend["fatigue"], pen=pen)
#             self.plot_fatigue.setYRange(0, 100)

#         # --- TRENDS DATA ---
#         summary = self.engine.weekly_behavior_summary()
#         self.plot_weekly.clear()
#         if summary and "distribution" in summary:
#             w_dist = summary["distribution"]
#             x = range(len(w_dist))
#             bg = pg.BarGraphItem(x=list(x), height=list(w_dist.values()), width=0.6, brush="#AF52DE")
#             self.plot_weekly.addItem(bg)

#         insights = self.engine.ai_insights()
#         if insights:
#             self.insight_label.setText(" • " + "\n • ".join(insights[:3]))


































# import pyqtgraph as pg
# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, 
#     QFrame, QScrollArea, QPushButton, QApplication
# )
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtGui import QColor

# # --- ENGINE IMPORT ---
# try:
#     from core.analytics_engine import AnalyticsEngine
# except ImportError:
#     class AnalyticsEngine:
#         def behavior_distribution(self): return {"Deep Work": 60, "Reading": 25, "Browsing": 15}
#         def fatigue_trend(self): return {"fatigue": [20, 22, 35, 50, 45, 30]}
#         def longest_behavior_streak(self): return {"minutes": 110, "behavior": "Deep Work"}
#         def ai_insights(self): return ["Focus is highly optimized.", "Fatigue spike detected at 11 AM."]

# # ============================================================
# # UPDATED COMPONENT WRAPPER
# # ============================================================
# class FluentAnalyticsCard(QFrame):
#     def __init__(self, title):
#         super().__init__()
#         self.setObjectName("FluentCard") 
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)
        
#         self.title_lbl = QLabel(title)
#         self.title_lbl.setObjectName("AnalyticsCardTitle") 
#         layout.addWidget(self.title_lbl)
        
#         self.body = QVBoxLayout()
#         layout.addLayout(self.body)

#     def add_fluent_plot(self, mode="dark"):
#         plot = pg.PlotWidget()
#         plot.setBackground(None) 
#         plot.setAntialiasing(True)
#         plot.setMenuEnabled(False)
#         plot.setMouseEnabled(x=False, y=False)
#         plot.hideButtons()
        
#         # Explicit QColor objects to prevent ValueError
#         if mode == "blue":
#             text_color = QColor("#E0F2FF")
#             axis_pen = QColor(0, 87, 217, 40) # Soft blue stroke
#         elif mode == "light":
#             text_color = QColor("#1A1A1A")
#             axis_pen = QColor(0, 0, 0, 20)    # Very faint black
#         else: # Dark
#             text_color = QColor("#E4E7F2")
#             axis_pen = QColor(255, 255, 255, 30) # Soft white stroke
        
#         ax = plot.getAxis('bottom')
#         ax.setPen(axis_pen)
#         ax.setTextPen(text_color)
#         plot.getAxis('left').hide()
        
#         self.body.addWidget(plot)
#         return plot

# # ============================================================
# # UPDATED MAIN PAGE LOGIC
# # ============================================================
# class AnalyticsSuitePage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.engine = AnalyticsEngine()
        
#         # 1. IDENTIFY MODE
#         # We check your specific background colors from the CSS
#         current_bg = self.palette().window().color().name().upper()
#         if current_bg == "#F2F6FC":
#             self.mode = "blue"
#             self.accent = "#0057D9"
#         elif current_bg == "#161618":
#             self.mode = "dark"
#             self.accent = "#4DA3FF"
#         else:
#             self.mode = "light"
#             self.accent = "#0057D9"
            
#         self.setup_ui()
#         QTimer.singleShot(100, self.refresh_all)

#     def setup_ui(self):
#         # Apply the layout exactly as your Fluent style demands
#         root = QVBoxLayout(self)
#         root.setContentsMargins(35, 30, 35, 30)
#         root.setSpacing(25)

#         header = QHBoxLayout()
#         title = QLabel("Performance Insights")
#         title.setObjectName("PageTitle")
#         header.addWidget(title)
#         header.addStretch()
        
#         refresh = QPushButton("Sync Data")
#         refresh.setObjectName("PrimaryButton")
#         refresh.clicked.connect(self.refresh_all)
#         header.addWidget(refresh)
#         root.addLayout(header)

#         self.tabs = QTabWidget()
#         self.tabs.setObjectName("AnalyticsTabs")
#         root.addWidget(self.tabs)

#         self._setup_focus_view()
#         self._setup_recovery_view()
#         self._setup_trends_view()

#     def _setup_focus_view(self):
#         container = QWidget()
#         layout = QVBoxLayout(container)
#         layout.setContentsMargins(0, 15, 0, 0)
        
#         row = QHBoxLayout()
#         self.card_dist = FluentAnalyticsCard("Focus Distribution")
#         self.plot_dist = self.card_dist.add_fluent_plot(self.mode)
        
#         self.card_streak = FluentAnalyticsCard("Longest Session")
#         self.streak_val = QLabel("0m")
#         self.streak_val.setObjectName("CardValue")
#         self.streak_val.setStyleSheet("font-size: 44px; font-weight: 800;")
        
#         self.streak_sub = QLabel("Analyzing...")
#         self.streak_sub.setObjectName("InsightText")
        
#         self.card_streak.body.addStretch()
#         self.card_streak.body.addWidget(self.streak_val, alignment=Qt.AlignCenter)
#         self.card_streak.body.addWidget(self.streak_sub, alignment=Qt.AlignCenter)
#         self.card_streak.body.addStretch()
        
#         row.addWidget(self.card_dist, 2)
#         row.addWidget(self.card_streak, 1)
#         layout.addLayout(row)
#         self.tabs.addTab(container, "Focus")

#     def _setup_recovery_view(self):
#         container = QWidget()
#         layout = QVBoxLayout(container)
#         layout.setContentsMargins(0, 15, 0, 0)
        
#         self.card_fatigue = FluentAnalyticsCard("Cognitive Load")
#         self.card_fatigue.setFixedHeight(400)
#         self.plot_fatigue = self.card_fatigue.add_fluent_plot(self.mode)
#         layout.addWidget(self.card_fatigue)
        
#         self.tabs.addTab(container, "Recovery")

#     def _setup_trends_view(self):
#         container = QWidget()
#         layout = QVBoxLayout(container)
#         layout.setContentsMargins(0, 15, 0, 0)
        
#         self.card_ai = FluentAnalyticsCard("Executive AI Summary")
#         self.card_ai.setFixedHeight(450) # Taller for more presence
        
#         # New inner layout for better structure
#         self.ai_content_layout = QVBoxLayout()
#         self.ai_content_layout.setSpacing(15)
        
#         # Add a subtle subtitle or "Last Updated" timestamp
#         self.update_time_lbl = QLabel("Updated just now")
#         self.update_time_lbl.setObjectName("InsightText")
#         self.update_time_lbl.setStyleSheet("opacity: 0.6; font-style: italic;")
#         self.ai_content_layout.addWidget(self.update_time_lbl)

#         # The main text container
#         self.ai_lbl = QLabel("Fetching engine synchronization data...")
#         self.ai_lbl.setObjectName("InsightText")
#         self.ai_lbl.setWordWrap(True)
#         # Add line-height and padding via stylesheet
#         self.ai_lbl.setStyleSheet("""
#             font-size: 15px; 
#             line-height: 160%; 
#             padding: 10px;
#         """)
        
#         self.ai_content_layout.addWidget(self.ai_lbl)
#         self.ai_content_layout.addStretch() # Pushes content to the top
        
#         self.card_ai.body.addLayout(self.ai_content_layout)
#         layout.addWidget(self.card_ai)
#         self.tabs.addTab(container, "Trends")

#     def refresh_all(self):
#         from datetime import datetime
        
#         # 1. FOCUS TAB: Distribution Bars
#         dist = self.engine.behavior_distribution()
#         self.plot_dist.clear()
#         if dist:
#             x = range(len(dist))
#             bg = pg.BarGraphItem(x=list(x), height=list(dist.values()), width=0.6, brush=self.accent, pen=None)
#             self.plot_dist.addItem(bg)
#             self.plot_dist.getAxis('bottom').setTicks([list(zip(x, dist.keys()))])

#         # 2. RECOVERY TAB: Fatigue Sparkline
#         fat_data = self.engine.fatigue_trend().get("fatigue", [])
#         self.plot_fatigue.clear()
#         if fat_data:
#             line_color = "#FF9500" if self.mode != "dark" else "#FF9F0A"
#             curve = self.plot_fatigue.plot(fat_data, pen=pg.mkPen(QColor(line_color), width=4), antialias=True)
            
#             fill_color = QColor(line_color)
#             fill_color.setAlpha(30)
#             fill = pg.FillBetweenItem(pg.PlotDataItem(y=[0]*len(fat_data)), curve, brush=fill_color)
#             self.plot_fatigue.addItem(fill)
#             self.plot_fatigue.enableAutoRange()

#         # 3. TRENDS TAB: Executive Summary & AI
#         insights = self.engine.ai_insights()
#         if insights:
#             formatted_text = ""
#             for i in insights:
#                 formatted_text += f"• {i}\n\n"
#             self.ai_lbl.setText(formatted_text.strip())
#             self.update_time_lbl.setText(f"Last analysis: {datetime.now().strftime('%H:%M:%S')}")

#         # 4. OVERVIEW: Focus Streak
#         streak = self.engine.longest_behavior_streak()
#         if streak:
#             self.streak_val.setText(f"{int(streak['minutes'])}m")
#             self.streak_sub.setText(f"Active in {streak['behavior']}")



















# import pyqtgraph as pg
# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, 
#     QFrame, QScrollArea, QPushButton, QApplication
# )
# from PySide6.QtCore import Qt, QTimer, QVariantAnimation
# from PySide6.QtGui import QColor
# from datetime import datetime

# # --- ENGINE IMPORT ---
# try:
#     from core.analytics_engine import AnalyticsEngine
# except ImportError:
#     class AnalyticsEngine:
#         def behavior_distribution(self): return {"Deep Work": 60, "Reading": 25, "Browsing": 15}
#         def fatigue_trend(self): return {"fatigue": [20, 22, 35, 50, 45, 30, 40, 55, 35, 42]}
#         def longest_behavior_streak(self): return {"minutes": 110, "behavior": "Deep Work"}
#         def ai_insights(self): return ["Focus is highly optimized.", "Fatigue spike detected at 11 AM."]

# # ============================================================
# # UPDATED COMPONENT WRAPPER
# # ============================================================
# class FluentAnalyticsCard(QFrame):
#     def __init__(self, title):
#         super().__init__()
#         self.setObjectName("FluentCard") 
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)
        
#         self.title_lbl = QLabel(title)
#         self.title_lbl.setObjectName("AnalyticsCardTitle") 
#         layout.addWidget(self.title_lbl)
        
#         self.body = QVBoxLayout()
#         layout.addLayout(self.body)

#     def add_fluent_plot(self, mode="dark"):
#         plot = pg.PlotWidget()
#         plot.setBackground(None) 
#         plot.setAntialiasing(True)
#         plot.setMenuEnabled(False)
#         plot.setMouseEnabled(x=False, y=False)
#         plot.hideButtons()
        
#         # Explicit QColor objects to prevent ValueError
#         if mode == "blue":
#             text_color = QColor("#E0F2FF")
#             axis_pen = QColor(0, 87, 217, 40) # Soft blue stroke
#         elif mode == "light":
#             text_color = QColor("#1A1A1A")
#             axis_pen = QColor(0, 0, 0, 20)    # Very faint black
#         else: # Dark
#             text_color = QColor("#E4E7F2")
#             axis_pen = QColor(255, 255, 255, 30) # Soft white stroke
        
#         ax = plot.getAxis('bottom')
#         ax.setPen(axis_pen)
#         ax.setTextPen(text_color)
#         plot.getAxis('left').hide()
        
#         self.body.addWidget(plot)
#         return plot

# # ============================================================
# # UPDATED MAIN PAGE LOGIC
# # ============================================================
# class AnalyticsSuitePage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.engine = AnalyticsEngine()
        
#         # 1. IDENTIFY MODE
#         current_bg = self.palette().window().color().name().upper()
#         if current_bg == "#F2F6FC":
#             self.mode = "blue"
#             self.accent = "#0057D9"
#         elif current_bg == "#161618":
#             self.mode = "dark"
#             self.accent = "#4DA3FF"
#         else:
#             self.mode = "light"
#             self.accent = "#0057D9"
            
#         self.setup_ui()
#         # Initial data sync
#         QTimer.singleShot(100, self.refresh_all)

#     def setup_ui(self):
#         root = QVBoxLayout(self)
#         root.setContentsMargins(35, 30, 35, 30)
#         root.setSpacing(25)

#         # --- HEADER ---
#         header = QHBoxLayout()
#         title = QLabel("Performance Insights")
#         title.setObjectName("PageTitle")
#         header.addWidget(title)
#         header.addStretch()
        
#         self.refresh_button = QPushButton("Sync Data")
#         self.refresh_button.setObjectName("PrimaryButton")
#         self.refresh_button.clicked.connect(self.refresh_all)
#         header.addWidget(self.refresh_button)
#         root.addLayout(header)

#         # --- TABS ---
#         self.tabs = QTabWidget()
#         self.tabs.setObjectName("AnalyticsTabs")
#         root.addWidget(self.tabs)

#         self._setup_focus_view()
#         self._setup_recovery_view()
#         self._setup_trends_view()

#     def _setup_focus_view(self):
#         container = QWidget()
#         layout = QVBoxLayout(container)
#         layout.setContentsMargins(0, 15, 0, 0)
        
#         row = QHBoxLayout()
#         self.card_dist = FluentAnalyticsCard("Focus Distribution")
#         self.plot_dist = self.card_dist.add_fluent_plot(self.mode)
        
#         self.card_streak = FluentAnalyticsCard("Longest Session")
#         self.streak_val = QLabel("0m")
#         self.streak_val.setObjectName("CardValue")
#         self.streak_val.setStyleSheet("font-size: 44px; font-weight: 800;")
        
#         self.streak_sub = QLabel("Analyzing...")
#         self.streak_sub.setObjectName("InsightText")
        
#         self.card_streak.body.addStretch()
#         self.card_streak.body.addWidget(self.streak_val, alignment=Qt.AlignCenter)
#         self.card_streak.body.addWidget(self.streak_sub, alignment=Qt.AlignCenter)
#         self.card_streak.body.addStretch()
        
#         row.addWidget(self.card_dist, 2)
#         row.addWidget(self.card_streak, 1)
#         layout.addLayout(row)
#         self.tabs.addTab(container, "Focus")

#     def _setup_recovery_view(self):
#         container = QWidget()
#         layout = QVBoxLayout(container)
#         layout.setContentsMargins(0, 15, 0, 0)
        
#         self.card_fatigue = FluentAnalyticsCard("Cognitive Load")
#         self.card_fatigue.setFixedHeight(400)
#         self.plot_fatigue = self.card_fatigue.add_fluent_plot(self.mode)
#         layout.addWidget(self.card_fatigue)
        
#         self.tabs.addTab(container, "Recovery")

#     def _setup_trends_view(self):
#         container = QWidget()
#         layout = QVBoxLayout(container)
#         layout.setContentsMargins(0, 15, 0, 0)
        
#         self.card_ai = FluentAnalyticsCard("Executive AI Summary")
#         self.card_ai.setFixedHeight(450)
        
#         self.ai_content_layout = QVBoxLayout()
#         self.ai_content_layout.setSpacing(15)
        
#         self.update_time_lbl = QLabel("Updated just now")
#         self.update_time_lbl.setObjectName("InsightText")
#         self.update_time_lbl.setStyleSheet("opacity: 0.6; font-style: italic;")
#         self.ai_content_layout.addWidget(self.update_time_lbl)

#         self.ai_lbl = QLabel("Fetching engine synchronization data...")
#         self.ai_lbl.setObjectName("InsightText")
#         self.ai_lbl.setWordWrap(True)
#         self.ai_lbl.setStyleSheet("""
#             font-size: 15px; 
#             line-height: 160%; 
#             padding: 10px;
#         """)
        
#         self.ai_content_layout.addWidget(self.ai_lbl)
#         self.ai_content_layout.addStretch()
        
#         self.card_ai.body.addLayout(self.ai_content_layout)
#         layout.addWidget(self.card_ai)
#         self.tabs.addTab(container, "Trends")

#     def animate_sync_button(self):
#         """Premium Pulse Animation"""
#         base_color = QColor(self.accent)
#         glow_color = base_color.lighter(140)

#         self.pulse_anim = QVariantAnimation(self)
#         self.pulse_anim.setDuration(500)
#         self.pulse_anim.setStartValue(glow_color)
#         self.pulse_anim.setEndValue(base_color)
        
#         def set_button_color(color):
#             self.refresh_button.setStyleSheet(f"background-color: {color.name()}; color: white; border-radius: 8px; padding: 10px 18px; font-weight: 600;")

#         self.pulse_anim.valueChanged.connect(set_button_color)
#         self.pulse_anim.start()

#     def refresh_all(self):
#         # 1. FOCUS TAB
#         dist = self.engine.behavior_distribution()
#         self.plot_dist.clear()
#         if dist:
#             x = range(len(dist))
#             bg = pg.BarGraphItem(x=list(x), height=list(dist.values()), width=0.6, brush=self.accent, pen=None)
#             self.plot_dist.addItem(bg)
#             self.plot_dist.getAxis('bottom').setTicks([list(zip(x, dist.keys()))])

#         # 2. RECOVERY TAB
#         fat_data = self.engine.fatigue_trend().get("fatigue", [])
#         self.plot_fatigue.clear()
#         if fat_data:
#             line_color = "#FF9500" if self.mode != "dark" else "#FF9F0A"
#             curve = self.plot_fatigue.plot(fat_data, pen=pg.mkPen(QColor(line_color), width=4), antialias=True)
            
#             fill_color = QColor(line_color)
#             fill_color.setAlpha(30)
#             fill = pg.FillBetweenItem(pg.PlotDataItem(y=[0]*len(fat_data)), curve, brush=fill_color)
#             self.plot_fatigue.addItem(fill)
#             self.plot_fatigue.enableAutoRange()

#         # 3. TRENDS TAB
#         insights = self.engine.ai_insights()
#         if insights:
#             formatted_text = ""
#             for i in insights:
#                 # Premium formatting: detect numbers and round them
#                 formatted_text += f"• {i}\n\n"
#             self.ai_lbl.setText(formatted_text.strip())
#             self.update_time_lbl.setText(f"Last analysis: {datetime.now().strftime('%H:%M:%S')}")

#         # 4. OVERVIEW
#         streak = self.engine.longest_behavior_streak()
#         if streak:
#             minutes = streak['minutes']
#             # Rounded formatting for Executive view
#             self.streak_val.setText(f"{int(minutes):,}m")
#             self.streak_sub.setText(f"Active in {streak['behavior']}")

#         # Trigger Premium Pulse
#         self.animate_sync_button()

# # For standalone testing
# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     window = AnalyticsSuitePage()
#     window.show()
#     sys.exit(app.exec())












# # Adding auto sync
# import pyqtgraph as pg
# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, 
#     QFrame, QScrollArea, QPushButton, QApplication
# )
# from PySide6.QtCore import Qt, QTimer, QVariantAnimation
# from PySide6.QtGui import QColor
# from datetime import datetime

# # --- ENGINE IMPORT ---
# try:
#     from core.analytics_engine import AnalyticsEngine
# except ImportError:
#     class AnalyticsEngine:
#         def behavior_distribution(self): return {"Deep Work": 60, "Reading": 25, "Browsing": 15}
#         def fatigue_trend(self): return {"fatigue": [20, 22, 35, 50, 45, 30, 40, 55, 35, 42]}
#         def longest_behavior_streak(self): return {"minutes": 110, "behavior": "Deep Work"}
#         def ai_insights(self): return ["Focus is highly optimized.", "Fatigue spike detected at 11 AM."]

# # ============================================================
# # PREMIUM COMPONENT: FLUENT CARD
# # ============================================================
# class FluentAnalyticsCard(QFrame):
#     def __init__(self, title):
#         super().__init__()
#         self.setObjectName("FluentCard") 
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)
        
#         self.title_lbl = QLabel(title)
#         self.title_lbl.setObjectName("AnalyticsCardTitle") 
#         layout.addWidget(self.title_lbl)
        
#         self.body = QVBoxLayout()
#         layout.addLayout(self.body)

#     # def add_fluent_plot(self, mode="dark"):
#     #     plot = pg.PlotWidget()
#     #     plot.setBackground(None) 
#     #     plot.setAntialiasing(True)
#     #     plot.setMenuEnabled(False)
#     #     plot.setMouseEnabled(x=False, y=False)
#     #     plot.hideButtons()
        
#     #     # Robust QColor handling for theme stability
#     #     if mode == "blue":
#     #         text_color = QColor("#E0F2FF")
#     #         axis_pen = QColor(0, 87, 217, 40)
#     #     elif mode == "light":
#     #         text_color = QColor("#1A1A1A")
#     #         axis_pen = QColor(0, 0, 0, 20)
#     #     else: # Dark
#     #         text_color = QColor("#F5EDE2")
#     #         axis_pen = QColor(255, 255, 255, 30)
        
#     #     ax = plot.getAxis('bottom')
#     #     ax.setPen(axis_pen)
#     #     ax.setTextPen(text_color)
#     #     plot.getAxis('left').hide()
        
#     #     self.body.addWidget(plot)
#     #     return plot


#     def add_fluent_plot(self, mode="dark"):
#         plot = pg.PlotWidget()
#         plot.setBackground(None)
#         plot.setAntialiasing(True)
#         plot.setMenuEnabled(False)
#         plot.setMouseEnabled(x=False, y=False)
#         plot.hideButtons()

#         # X‑axis text color only
#         if mode == "blue":
#             text_color = QColor("#003A8C")      # Deep blue
#         elif mode == "light":
#             text_color = QColor("#000000")      # Black
#         else:  # DARK MODE
#             text_color = QColor("#F5EDE2")      # Cream white

#         # Baseline stays whatever PyQtGraph already uses
#         axis_pen = plot.getAxis('bottom').pen()

#         ax = plot.getAxis('bottom')
#         ax.setTextPen(text_color)   # ← ONLY text color
#         ax.setPen(axis_pen)         # ← baseline unchanged

#         plot.getAxis('left').hide()
#         self.body.addWidget(plot)
#         return plot

# # ============================================================
# # EXECUTIVE DASHBOARD PAGE
# # ============================================================
# class AnalyticsSuitePage(QWidget):
#     def __init__(self, theme="light"):
#         super().__init__()
#         self.engine = AnalyticsEngine()
        
#         # 1. THEME ENGINE DETECTION
#         current_bg = self.palette().window().color().name().upper()
#         # if current_bg == "#F2F6FC":
#         #     self.mode = "blue"
#         #     self.accent = "#0057D9"
#         # elif current_bg == "#161618":
#         #     self.mode = "dark"
#         #     self.accent = "#4DA3FF"
#         # else:
#         #     self.mode = "light"
#         #     self.accent = "#0057D9"
#         t = theme.lower()

#         if "dark" in t:
#             self.mode = "dark"
#             self.accent = "#F5EDE2"
#         elif "blue" in t:
#             self.mode = "blue"
#             self.accent = "#0057D9"
#         else:
#             self.mode = "light"
#             self.accent = "#0057D9"


            
#         self.setup_ui()

#         # 2. AUTO-SYNC TIMER (Every 60 Seconds)
#         self.autosync_timer = QTimer(self)
#         self.autosync_timer.timeout.connect(self.refresh_all)
#         self.autosync_timer.start(60000) # 60,000ms = 1 minute
        
#         # Initial boot-up sync
#         QTimer.singleShot(100, self.refresh_all)

#     def setup_ui(self):
#         root = QVBoxLayout(self)
#         root.setContentsMargins(35, 30, 35, 30)
#         root.setSpacing(25)

#         # --- PREMIUM HEADER ---
#         header = QHBoxLayout()
#         title_container = QVBoxLayout()
        
#         self.title_lbl = QLabel("Performance Insights")
#         self.title_lbl.setObjectName("PageTitle")
        
#         self.live_status = QLabel("● LIVE AUTO-SYNC ACTIVE")
#         self.live_status.setStyleSheet(f"color: {self.accent}; font-size: 10px; font-weight: bold; letter-spacing: 1px;")
        
#         title_container.addWidget(self.title_lbl)
#         title_container.addWidget(self.live_status)
#         header.addLayout(title_container)
#         header.addStretch()
        
#         self.refresh_button = QPushButton("Sync Now")
#         self.refresh_button.setObjectName("PrimaryButton")
#         self.refresh_button.setCursor(Qt.PointingHandCursor)
#         self.refresh_button.clicked.connect(self.refresh_all)
#         header.addWidget(self.refresh_button)
#         root.addLayout(header)

#         # --- NAVIGATION TABS ---
#         self.tabs = QTabWidget()
#         self.tabs.setObjectName("AnalyticsTabs")
#         root.addWidget(self.tabs)

#         self._setup_focus_view()
#         self._setup_recovery_view()
#         self._setup_trends_view()

#     def _setup_focus_view(self):
#         container = QWidget()
#         layout = QVBoxLayout(container)
#         layout.setContentsMargins(0, 15, 0, 0)
        
#         row = QHBoxLayout()
#         self.card_dist = FluentAnalyticsCard("Focus Distribution")
#         self.plot_dist = self.card_dist.add_fluent_plot(self.mode)
        
#         self.card_streak = FluentAnalyticsCard("Peak Performance")
#         self.streak_val = QLabel("0m")
#         self.streak_val.setObjectName("CardValue")
#         self.streak_val.setStyleSheet("font-size: 48px; font-weight: 800;")
        
#         self.streak_sub = QLabel("Monitoring focus states...")
#         self.streak_sub.setObjectName("InsightText")
        
#         self.card_streak.body.addStretch()
#         self.card_streak.body.addWidget(self.streak_val, alignment=Qt.AlignCenter)
#         self.card_streak.body.addWidget(self.streak_sub, alignment=Qt.AlignCenter)
#         self.card_streak.body.addStretch()
        
#         row.addWidget(self.card_dist, 2)
#         row.addWidget(self.card_streak, 1)
#         layout.addLayout(row)
#         self.tabs.addTab(container, "Focus")

#     def _setup_recovery_view(self):
#         container = QWidget()
#         layout = QVBoxLayout(container)
#         layout.setContentsMargins(0, 15, 0, 0)
        
#         self.card_fatigue = FluentAnalyticsCard("Cognitive Load Analysis")
#         self.card_fatigue.setFixedHeight(400)
#         self.plot_fatigue = self.card_fatigue.add_fluent_plot(self.mode)
#         layout.addWidget(self.card_fatigue)
        
#         self.tabs.addTab(container, "Recovery")

#     def _setup_trends_view(self):
#         container = QWidget()
#         layout = QVBoxLayout(container)
#         layout.setContentsMargins(0, 15, 0, 0)
        
#         self.card_ai = FluentAnalyticsCard("Executive AI Briefing")
#         self.card_ai.setFixedHeight(450)
        
#         self.ai_content_layout = QVBoxLayout()
#         self.ai_content_layout.setSpacing(15)
        
#         self.update_time_lbl = QLabel("Awaiting synchronization...")
#         self.update_time_lbl.setObjectName("InsightText")
#         self.update_time_lbl.setStyleSheet("opacity: 0.6; font-style: italic;")
#         self.ai_content_layout.addWidget(self.update_time_lbl)

#         self.ai_lbl = QLabel("Processing behavioral patterns...")
#         self.ai_lbl.setObjectName("InsightText")
#         self.ai_lbl.setWordWrap(True)
#         self.ai_lbl.setStyleSheet("font-size: 15px; line-height: 160%; padding: 10px;")
        
#         self.ai_content_layout.addWidget(self.ai_lbl)
#         self.ai_content_layout.addStretch()
        
#         self.card_ai.body.addLayout(self.ai_content_layout)
#         layout.addWidget(self.card_ai)
#         self.tabs.addTab(container, "Trends")

#     def animate_sync_pulse(self):
#         """Executive Button Pulse Effect"""
#         base_color = QColor(self.accent)
#         glow_color = base_color.lighter(150)

#         self.pulse_anim = QVariantAnimation(self)
#         self.pulse_anim.setDuration(600)
#         self.pulse_anim.setStartValue(glow_color)
#         self.pulse_anim.setEndValue(base_color)
        
#         def set_button_style(color):
#             self.refresh_button.setStyleSheet(f"""
#                 QPushButton {{
#                     background-color: {color.name()};
#                     color: white;
#                     border-radius: 8px;
#                     padding: 10px 20px;
#                     font-weight: 600;
#                     border: none;
#                 }}
#             """)

#         self.pulse_anim.valueChanged.connect(set_button_style)
#         self.pulse_anim.start()

#     def refresh_all(self):
#         # 1. Update Distribution
#         dist = self.engine.behavior_distribution()
#         self.plot_dist.clear()
#         if dist:
#             x = range(len(dist))
#             bg = pg.BarGraphItem(
#                 x=list(x),
#                 height=list(dist.values()),
#                 width=0.6,
#                 brush=self.accent,
#                 pen=None
#             )
#             self.plot_dist.addItem(bg)

#             # Apply ticks
#             self.plot_dist.getAxis('bottom').setTicks([list(zip(x, dist.keys()))])

#             # ⭐ CRITICAL FIX: Re-apply x-axis text color AFTER ticks
#             ax = self.plot_dist.getAxis('bottom')
#             if self.mode == "dark":
#                 ax.setTextPen(QColor("#F5EDE2"))      # Cream white
#             elif self.mode == "blue":
#                 ax.setTextPen(QColor("#003A8C"))      # Deep blue
#             else:
#                 ax.setTextPen(QColor("#000000"))      # Black

#         # 2. Update Fatigue Sparkline
#         fat_data = self.engine.fatigue_trend().get("fatigue", [])
#         self.plot_fatigue.clear()
#         if fat_data:
#             line_color = "#FF9500" if self.mode != "dark" else "#FF9F0A"
#             curve = self.plot_fatigue.plot(
#                 fat_data,
#                 pen=pg.mkPen(QColor(line_color), width=4),
#                 antialias=True
#             )

#             fill_color = QColor(line_color)
#             fill_color.setAlpha(35)
#             fill = pg.FillBetweenItem(
#                 pg.PlotDataItem(y=[0] * len(fat_data)),
#                 curve,
#                 brush=fill_color
#             )
#             self.plot_fatigue.addItem(fill)
#             self.plot_fatigue.enableAutoRange()

#         # 3. Update AI Summary
#         insights = self.engine.ai_insights()
#         if insights:
#             self.ai_lbl.setText("\n\n".join([f"• {i}" for i in insights]))
#             self.update_time_lbl.setText(
#                 f"Last updated: {datetime.now().strftime('%H:%M:%S')}"
#             )

#         # 4. Update Overview Values
#         streak = self.engine.longest_behavior_streak()
#         if streak:
#             self.streak_val.setText(f"{int(streak['minutes']):,}m")
#             self.streak_sub.setText(f"Peak: {streak['behavior']}")

#         # Visual Confirmation
#         self.animate_sync_pulse()




















# 29th March
# Adding auto sync
import pyqtgraph as pg
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, 
    QFrame, QScrollArea, QPushButton, QApplication
)
from PySide6.QtCore import Qt, QTimer, QVariantAnimation
from PySide6.QtGui import QColor
from datetime import datetime

# --- ENGINE IMPORT ---
try:
    from core.analytics_engine import AnalyticsEngine
except ImportError:
    class AnalyticsEngine:
        def behavior_distribution(self): return {"Deep Work": 60, "Reading": 25, "Browsing": 15}
        def fatigue_trend(self): return {"fatigue": [20, 22, 35, 50, 45, 30, 40, 55, 35, 42]}
        def longest_behavior_streak(self): return {"minutes": 110, "behavior": "Deep Work"}
        def ai_insights(self): return ["Focus is highly optimized.", "Fatigue spike detected at 11 AM."]

# ============================================================
# PREMIUM COMPONENT: FLUENT CARD
# ============================================================
class FluentAnalyticsCard(QFrame):
    def __init__(self, title):
        super().__init__()
        self.setObjectName("FluentCard") 
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.title_lbl = QLabel(title)
        self.title_lbl.setObjectName("AnalyticsCardTitle") 
        layout.addWidget(self.title_lbl)
        
        self.body = QVBoxLayout()
        layout.addLayout(self.body)

    def add_fluent_plot(self, mode="dark"):
        plot = pg.PlotWidget()
        plot.setBackground(None)
        plot.setAntialiasing(True)
        plot.setMenuEnabled(False)
        plot.setMouseEnabled(x=False, y=False)
        plot.hideButtons()

        # Apply initial theme colors
        self.apply_theme_to_axis(plot, mode)

        plot.getAxis('left').hide()
        self.body.addWidget(plot)
        return plot

    def apply_theme_to_axis(self, plot, mode):
        """Helper to ensure text color is consistent across all modes"""
        if mode == "blue":
            text_color = QColor("#003A8C")      # Deep blue
        elif mode == "light":
            text_color = QColor("#0057D9")      # Black
        else:  # DARK MODE
            text_color = QColor("#0057D9")      # Cream white

        ax = plot.getAxis('bottom')
        ax.setTextPen(text_color)
        # Also set the pen for the line itself to keep it subtle
        ax.setPen(pg.mkPen(text_color, width=1, cosmetic=True))

# ============================================================
# EXECUTIVE DASHBOARD PAGE
# ============================================================
class AnalyticsSuitePage(QWidget):
    def __init__(self, theme="light"):
        super().__init__()
        self.engine = AnalyticsEngine()
        
        t = theme.lower()
        if "dark" in t:
            self.mode = "dark"
            self.accent = "#0057D9"
        elif "blue" in t:
            self.mode = "blue"
            self.accent = "#0057D9"
        else:
            self.mode = "light"
            self.accent = "#0057D9"
            
        self.setup_ui()

        # 2. AUTO-SYNC TIMER (Every 60 Seconds)
        self.autosync_timer = QTimer(self)
        self.autosync_timer.timeout.connect(self.refresh_all)
        self.autosync_timer.start(60000) 
        
        QTimer.singleShot(100, self.refresh_all)

    def setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(35, 30, 35, 30)
        root.setSpacing(25)

        # --- PREMIUM HEADER ---
        header = QHBoxLayout()
        title_container = QVBoxLayout()
        
        self.title_lbl = QLabel("Performance Insights")
        self.title_lbl.setObjectName("PageTitle")
        
        self.live_status = QLabel("● LIVE AUTO-SYNC ACTIVE")
        self.live_status.setStyleSheet(f"color: {self.accent}; font-size: 10px; font-weight: bold; letter-spacing: 1px;")
        
        title_container.addWidget(self.title_lbl)
        title_container.addWidget(self.live_status)
        header.addLayout(title_container)
        header.addStretch()
        
        self.refresh_button = QPushButton("Sync Now")
        self.refresh_button.setObjectName("PrimaryButton")
        self.refresh_button.setCursor(Qt.PointingHandCursor)
        self.refresh_button.clicked.connect(self.refresh_all)
        header.addWidget(self.refresh_button)
        root.addLayout(header)

        # --- NAVIGATION TABS ---
        self.tabs = QTabWidget()
        self.tabs.setObjectName("AnalyticsTabs")
        root.addWidget(self.tabs)

        self._setup_focus_view()
        self._setup_recovery_view()
        self._setup_trends_view()

    def _setup_focus_view(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 15, 0, 0)
        
        row = QHBoxLayout()
        self.card_dist = FluentAnalyticsCard("Focus Distribution")
        self.plot_dist = self.card_dist.add_fluent_plot(self.mode)
        
        self.card_streak = FluentAnalyticsCard("Peak Performance")
        self.streak_val = QLabel("0m")
        self.streak_val.setObjectName("CardValue")
        self.streak_val.setStyleSheet("font-size: 48px; font-weight: 800;")
        
        self.streak_sub = QLabel("Monitoring focus states...")
        self.streak_sub.setObjectName("InsightText")
        
        self.card_streak.body.addStretch()
        self.card_streak.body.addWidget(self.streak_val, alignment=Qt.AlignCenter)
        self.card_streak.body.addWidget(self.streak_sub, alignment=Qt.AlignCenter)
        self.card_streak.body.addStretch()
        
        row.addWidget(self.card_dist, 2)
        row.addWidget(self.card_streak, 1)
        layout.addLayout(row)
        self.tabs.addTab(container, "Focus")

    def _setup_recovery_view(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 15, 0, 0)
        
        self.card_fatigue = FluentAnalyticsCard("Cognitive Load Analysis")
        self.card_fatigue.setFixedHeight(400)
        self.plot_fatigue = self.card_fatigue.add_fluent_plot(self.mode)
        layout.addWidget(self.card_fatigue)
        
        self.tabs.addTab(container, "Recovery")

    def _setup_trends_view(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 15, 0, 0)
        
        self.card_ai = FluentAnalyticsCard("Executive AI Briefing")
        self.card_ai.setFixedHeight(450)
        
        self.ai_content_layout = QVBoxLayout()
        self.ai_content_layout.setSpacing(15)
        
        self.update_time_lbl = QLabel("Awaiting synchronization...")
        self.update_time_lbl.setObjectName("InsightText")
        self.update_time_lbl.setStyleSheet("opacity: 0.6; font-style: italic;")
        self.ai_content_layout.addWidget(self.update_time_lbl)

        self.ai_lbl = QLabel("Processing behavioral patterns...")
        self.ai_lbl.setObjectName("InsightText")
        self.ai_lbl.setWordWrap(True)
        self.ai_lbl.setStyleSheet("font-size: 15px; line-height: 160%; padding: 10px;")
        
        self.ai_content_layout.addWidget(self.ai_lbl)
        self.ai_content_layout.addStretch()
        
        self.card_ai.body.addLayout(self.ai_content_layout)
        layout.addWidget(self.card_ai)
        self.tabs.addTab(container, "Trends")

    def animate_sync_pulse(self):
        base_color = QColor(self.accent)
        glow_color = base_color.lighter(150)

        self.pulse_anim = QVariantAnimation(self)
        self.pulse_anim.setDuration(600)
        self.pulse_anim.setStartValue(glow_color)
        self.pulse_anim.setEndValue(base_color)
        
        def set_button_style(color):
            self.refresh_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color.name()};
                    color: white;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-weight: 600;
                    border: none;
                }}
            """)

        self.pulse_anim.valueChanged.connect(set_button_style)
        self.pulse_anim.start()

    def refresh_all(self):
        # 1. Update Distribution
        dist = self.engine.behavior_distribution()
        self.plot_dist.clear()
        if dist:
            x = range(len(dist))
            bg = pg.BarGraphItem(
                x=list(x),
                height=list(dist.values()),
                width=0.6,
                brush=self.accent,
                pen=None
            )
            self.plot_dist.addItem(bg)
            self.plot_dist.getAxis('bottom').setTicks([list(zip(x, dist.keys()))])
            
            # Re-apply color theme to fix potential reset after clear()
            self.card_dist.apply_theme_to_axis(self.plot_dist, self.mode)

        # 2. Update Fatigue Sparkline
        fat_data = self.engine.fatigue_trend().get("fatigue", [])
        self.plot_fatigue.clear()
        if fat_data:
            line_color = "#FF9500" if self.mode != "dark" else "#FF9F0A"
            curve = self.plot_fatigue.plot(
                fat_data,
                pen=pg.mkPen(QColor(line_color), width=4),
                antialias=True
            )

            fill_color = QColor(line_color)
            fill_color.setAlpha(35)
            fill = pg.FillBetweenItem(
                pg.PlotDataItem(y=[0] * len(fat_data)),
                curve,
                brush=fill_color
            )
            self.plot_fatigue.addItem(fill)
            
            # FIX: Re-apply color theme to Fatigue plot axis text
            self.card_fatigue.apply_theme_to_axis(self.plot_fatigue, self.mode)
            self.plot_fatigue.enableAutoRange()

        # 3. Update AI Summary
        insights = self.engine.ai_insights()
        if insights:
            self.ai_lbl.setText("\n\n".join([f"• {i}" for i in insights]))
            self.update_time_lbl.setText(
                f"Last updated: {datetime.now().strftime('%H:%M:%S')}"
            )

        # 4. Update Overview Values
        streak = self.engine.longest_behavior_streak()
        if streak:
            self.streak_val.setText(f"{int(streak['minutes']):,}m")
            self.streak_sub.setText(f"Peak: {streak['behavior']}")

        self.animate_sync_pulse()