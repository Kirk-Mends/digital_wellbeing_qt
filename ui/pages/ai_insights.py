

# 5 new design

# import csv
# from datetime import datetime
# from collections import Counter, defaultdict
# from statistics import mean

# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
# from PySide6.QtCore import Qt


# class AIInsightsPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("AIInsightsPage")

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 6, 20, 20)
#         layout.setSpacing(20)

#         title = QLabel("AI Insights")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         self.insight_container = QVBoxLayout()
#         layout.addLayout(self.insight_container)

#         self.generate_insights()

#     # -------------------------
#     # CARD FACTORY
#     # -------------------------
#     def make_card(self, text: str) -> QFrame:
#         frame = QFrame()
#         frame.setObjectName("InsightCard")

#         v = QVBoxLayout(frame)
#         v.setContentsMargins(16, 16, 16, 16)

#         label = QLabel(text)
#         label.setWordWrap(True)
#         label.setObjectName("InsightText")

#         v.addWidget(label)
#         return frame

#     # -------------------------
#     # MAIN ENTRY
#     # -------------------------
#     def generate_insights(self):
#         insights = []

#         data = self.load_usage()
#         if not data:
#             insights.append("Insights will appear here after you’ve used the assistant for a little while.")
#         else:
#             insights.extend(self.analyze_usage(data))

#         # Clear old cards
#         while self.insight_container.count():
#             item = self.insight_container.takeAt(0)
#             if item.widget():
#                 item.widget().deleteLater()

#         # Add new cards
#         for text in insights:
#             self.insight_container.addWidget(self.make_card(text))

#     # -------------------------
#     # LOAD CSV
#     # -------------------------
#     def load_usage(self):
#         try:
#             with open("usage_log.csv", "r", encoding="utf-8") as f:
#                 reader = csv.DictReader(f)
#                 rows = []
#                 for r in reader:
#                     try:
#                         ts = datetime.fromisoformat(r.get("timestamp") or r.get("date"))
#                         behavior = (r.get("behavior") or "Activity").strip()
#                         fatigue = float(r.get("fatigue_score") or 0.0)
#                         brk = str(r.get("break_triggered") or "0").lower() in ["1", "true", "yes"]
#                         reason = (r.get("break_reason") or "").strip()
#                         rows.append({
#                             "timestamp": ts,
#                             "behavior": behavior,
#                             "fatigue": fatigue,
#                             "break_triggered": brk,
#                             "break_reason": reason,
#                         })
#                     except Exception:
#                         continue
#                 return rows
#         except FileNotFoundError:
#             return []

#     # -------------------------
#     # HYBRID INSIGHTS
#     # -------------------------
#     def analyze_usage(self, rows):
#         insights = []

#         if not rows:
#             return ["Not enough data to generate insights yet."]

#         # Behavior stats
#         behavior_counts = Counter(r["behavior"] for r in rows)
#         most_common_behavior, most_common_count = behavior_counts.most_common(1)[0]

#         # Time-of-day buckets
#         by_hour = defaultdict(list)
#         for r in rows:
#             by_hour[r["timestamp"].hour].append(r)

#         # Break stats
#         breaks = [r for r in rows if r["break_triggered"]]
#         break_reasons = Counter(r["break_reason"] for r in breaks if r["break_reason"])

#         # Fatigue stats
#         fatigue_values = [r["fatigue"] for r in rows if r["fatigue"] > 0]
#         avg_fatigue = mean(fatigue_values) if fatigue_values else 0
#         max_fatigue = max(fatigue_values) if fatigue_values else 0

#         # Behavior → fatigue mapping
#         fatigue_by_behavior = defaultdict(list)
#         for r in rows:
#             if r["fatigue"] > 0:
#                 fatigue_by_behavior[r["behavior"]].append(r["fatigue"])

#         # -------------------------
#         # 1) Most common behavior
#         # -------------------------
#         insights.append(
#             f"You spend most of your focused time in {most_common_behavior.lower()}."
#         )

#         # -------------------------
#         # 2) Time-of-day pattern
#         # -------------------------
#         if by_hour:
#             # Morning: 6–12, Afternoon: 12–18, Evening: 18–24
#             morning = sum(len(by_hour[h]) for h in range(6, 12))
#             afternoon = sum(len(by_hour[h]) for h in range(12, 18))
#             evening = sum(len(by_hour[h]) for h in range(18, 24))

#             segment_counts = {
#                 "morning": morning,
#                 "afternoon": afternoon,
#                 "evening": evening,
#             }
#             best_segment = max(segment_counts, key=segment_counts.get)
#             if segment_counts[best_segment] > 0:
#                 insights.append(
#                     f"Your activity is strongest in the {best_segment}."
#                 )

#         # -------------------------
#         # 3) Break reasons
#         # -------------------------
#         if breaks:
#             total_breaks = len(breaks)
#             insights.append(
#                 f"You have taken {total_breaks} breaks during your recent sessions."
#             )

#             if break_reasons:
#                 top_reason, _ = break_reasons.most_common(1)[0]
#                 if top_reason:
#                     insights.append(
#                         f"Most of your breaks are triggered when the system notices {top_reason.lower()}."
#                     )

#         # -------------------------
#         # 4) Fatigue levels
#         # -------------------------
#         if fatigue_values:
#             insights.append(
#                 f"On average, your fatigue level before a break is around {avg_fatigue:.0f} out of 100."
#             )
#             insights.append(
#                 f"Your highest recorded fatigue recently reached about {max_fatigue:.0f} out of 100."
#             )

#         # -------------------------
#         # 5) Behavior that drives fatigue
#         # -------------------------
#         if fatigue_by_behavior:
#             avg_by_behavior = {
#                 b: mean(vals) for b, vals in fatigue_by_behavior.items() if vals
#             }
#             if avg_by_behavior:
#                 top_fatigue_behavior = max(avg_by_behavior, key=avg_by_behavior.get)
#                 insights.append(
#                     f"Your fatigue tends to rise the most during {top_fatigue_behavior.lower()} sessions."
#                 )

#         # Fallback if somehow we generated nothing
#         if not insights:
#             insights.append("Insights will appear here as you spend more time using the assistant.")

#         return insights















# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
# from PySide6.QtCore import Qt
# from statistics import mean
# from collections import Counter, defaultdict


# class AIInsightsPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("AIInsightsPage")

#         # MAIN LAYOUT
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)   # reduced top margin
#         layout.setSpacing(20)
#         layout.setAlignment(Qt.AlignTop)


#         # TITLE
#         title = QLabel("AI Insights")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # CONTAINER FOR INSIGHT CARDS
#         self.insight_container = QVBoxLayout()
#         self.insight_container.setSpacing(12)
#         layout.addLayout(self.insight_container)

#         # Placeholder until data arrives
#         self.update_insights([])

#     # -------------------------------------------------------
#     # PUBLIC METHOD CALLED BY MAINWINDOW
#     # -------------------------------------------------------
#     def update_insights(self, history):
#         """
#         history = list of dicts:
#         {
#             "timestamp": datetime,
#             "behavior": str,
#             "fatigue": int,
#             "break_triggered": bool,
#             "break_reason": str,
#             "suppression": bool
#         }
#         """
#         insights = self.generate_insight_text(history)

#         # Clear old cards
#         while self.insight_container.count():
#             item = self.insight_container.takeAt(0)
#             if item.widget():
#                 item.widget().deleteLater()

#         # Add new cards
#         for text in insights:
#             self.insight_container.addWidget(self.make_card(text))

#     # -------------------------------------------------------
#     # CARD FACTORY
#     # -------------------------------------------------------
#     def make_card(self, text: str) -> QFrame:
#         frame = QFrame()
#         frame.setObjectName("InsightCard")

#         v = QVBoxLayout(frame)
#         v.setContentsMargins(16, 16, 16, 16)

#         label = QLabel(text)
#         label.setWordWrap(True)
#         label.setObjectName("InsightText")

#         v.addWidget(label)
#         return frame

#     # -------------------------------------------------------
#     # INSIGHT GENERATION (NO CSV)
#     # -------------------------------------------------------
#     def generate_insight_text(self, rows):
#         if not rows:
#             return [
#                 "Insights will appear here after you’ve spent some time using Smart Mode or AI Mode."
#             ]

#         insights = []

#         # -------------------------
#         # Behavior patterns
#         # -------------------------
#         behaviors = [r["behavior"] for r in rows if r.get("behavior")]
#         if behaviors:
#             most_common, count = Counter(behaviors).most_common(1)[0]
#             insights.append(
#                 f"You spend most of your focused time in {most_common.lower()}."
#             )

#         # -------------------------
#         # Time-of-day activity
#         # -------------------------
#         by_hour = defaultdict(int)
#         for r in rows:
#             by_hour[r["timestamp"].hour] += 1

#         morning = sum(by_hour[h] for h in range(6, 12))
#         afternoon = sum(by_hour[h] for h in range(12, 18))
#         evening = sum(by_hour[h] for h in range(18, 24))

#         segments = {"morning": morning, "afternoon": afternoon, "evening": evening}
#         best_segment = max(segments, key=segments.get)
#         if segments[best_segment] > 0:
#             insights.append(f"Your activity is strongest in the {best_segment}.")

#         # -------------------------
#         # Break patterns
#         # -------------------------
#         breaks = [r for r in rows if r.get("break_triggered")]
#         if breaks:
#             insights.append(
#                 f"You’ve taken {len(breaks)} breaks during your recent sessions."
#             )

#             reasons = [r["break_reason"] for r in breaks if r.get("break_reason")]
#             if reasons:
#                 top_reason, _ = Counter(reasons).most_common(1)[0]
#                 insights.append(
#                     f"Most of your breaks are triggered when the system detects {top_reason.lower()}."
#                 )

#         # -------------------------
#         # Fatigue patterns
#         # -------------------------
#         fatigue_values = [r["fatigue"] for r in rows if r.get("fatigue", 0) > 0]
#         if fatigue_values:
#             avg_fatigue = mean(fatigue_values)
#             max_fatigue = max(fatigue_values)

#             insights.append(
#                 f"Your average fatigue level before breaks is around {avg_fatigue:.0f} out of 100."
#             )
#             insights.append(
#                 f"Your highest recent fatigue level reached about {max_fatigue:.0f}."
#             )

#         # -------------------------
#         # Behavior → fatigue mapping
#         # -------------------------
#         fatigue_by_behavior = defaultdict(list)
#         for r in rows:
#             if r.get("fatigue", 0) > 0:
#                 fatigue_by_behavior[r["behavior"]].append(r["fatigue"])

#         if fatigue_by_behavior:
#             avg_map = {b: mean(vals) for b, vals in fatigue_by_behavior.items()}
#             top_behavior = max(avg_map, key=avg_map.get)
#             insights.append(
#                 f"Your fatigue tends to rise the most during {top_behavior.lower()} sessions."
#             )

#         return insights



























# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
# from PySide6.QtCore import Qt
# from statistics import mean
# from collections import Counter, defaultdict


# class AIInsightsPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("AIInsightsPage")

#         # MAIN LAYOUT
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 24, 20, 20)   # premium top spacing
#         layout.setSpacing(20)
#         layout.setAlignment(Qt.AlignTop)

#         # TITLE
#         title = QLabel("AI Insights")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # CONTAINER FOR INSIGHT CARDS
#         self.insight_container = QVBoxLayout()
#         self.insight_container.setSpacing(8)
#         layout.addLayout(self.insight_container)

#         # Placeholder until data arrives
#         self.update_insights([])

#     # -------------------------------------------------------
#     # PUBLIC METHOD CALLED BY MAINWINDOW
#     # -------------------------------------------------------
#     def update_insights(self, history):
#         """
#         history = list of dicts:
#         {
#             "timestamp": datetime,
#             "behavior": str,
#             "fatigue": int,
#             "break_triggered": bool,
#             "break_reason": str,
#             "suppression": bool
#         }
#         """
#         insights = self.generate_insight_text(history)

#         # Clear old cards
#         while self.insight_container.count():
#             item = self.insight_container.takeAt(0)
#             if item.widget():
#                 item.widget().deleteLater()

#         # Add new cards
#         for text in insights:
#             self.insight_container.addWidget(self.make_card(text))

#     # -------------------------------------------------------
#     # CARD FACTORY
#     # -------------------------------------------------------
#     def make_card(self, text: str) -> QFrame:
#         frame = QFrame()
#         frame.setObjectName("InsightCard")

#         v = QVBoxLayout(frame)
#         v.setContentsMargins(12, 12, 12, 12)

#         label = QLabel(text)
#         label.setWordWrap(True)
#         label.setObjectName("InsightText")
#         label.setTextFormat(Qt.RichText)   # IMPORTANT: enable HTML formatting

#         v.addWidget(label)
#         return frame

#     # -------------------------------------------------------
#     # UPDATED INSIGHT GENERATION (HTML + percentages)
#     # -------------------------------------------------------
#     def generate_insight_text(self, rows):
#         if not rows:
#             return [
#                 "<i>Insights will appear here after you’ve spent some time using Smart Mode or AI Mode.</i>"
#             ]

#         insights = []

#         # -------------------------
#         # Behavior patterns
#         # -------------------------
#         behaviors = [r["behavior"] for r in rows if r.get("behavior")]
#         if behaviors:
#             most_common, count = Counter(behaviors).most_common(1)[0]
#             insights.append(
#                 f"You spend most of your focused time in <b>{most_common.lower()}</b>."
#             )

#         # -------------------------
#         # Time-of-day activity
#         # -------------------------
#         by_hour = defaultdict(int)
#         for r in rows:
#             by_hour[r["timestamp"].hour] += 1

#         morning = sum(by_hour[h] for h in range(6, 12))
#         afternoon = sum(by_hour[h] for h in range(12, 18))
#         evening = sum(by_hour[h] for h in range(18, 24))

#         segments = {"morning": morning, "afternoon": afternoon, "evening": evening}
#         best_segment = max(segments, key=segments.get)
#         if segments[best_segment] > 0:
#             insights.append(
#                 f"Your activity is strongest in the <b>{best_segment}</b>."
#             )

#         # -------------------------
#         # Break patterns
#         # -------------------------
#         breaks = [r for r in rows if r.get("break_triggered")]
#         if breaks:
#             insights.append(
#                 f"You’ve taken <b>{len(breaks)}</b> breaks during your recent sessions."
#             )

#             reasons = [r["break_reason"] for r in breaks if r.get("break_reason")]
#             if reasons:
#                 top_reason, _ = Counter(reasons).most_common(1)[0]
#                 insights.append(
#                     f"Most of your breaks are triggered when the system detects <b>{top_reason.lower()}</b>."
#                 )

#         # -------------------------
#         # Fatigue patterns
#         # -------------------------
#         fatigue_values = [r["fatigue"] for r in rows if r.get("fatigue", 0) > 0]
#         if fatigue_values:
#             avg_fatigue = mean(fatigue_values)
#             max_fatigue = max(fatigue_values)

#             insights.append(
#                 f"Your average fatigue level before breaks is around <b>{avg_fatigue:.0f}%</b>."
#             )
#             insights.append(
#                 f"Your highest recent fatigue level reached about <b>{max_fatigue:.0f}%</b>."
#             )

#         # -------------------------
#         # Behavior → fatigue mapping
#         # -------------------------
#         fatigue_by_behavior = defaultdict(list)
#         for r in rows:
#             if r.get("fatigue", 0) > 0:
#                 fatigue_by_behavior[r["behavior"]].append(r["fatigue"])

#         if fatigue_by_behavior:
#             avg_map = {b: mean(vals) for b, vals in fatigue_by_behavior.items()}
#             top_behavior = max(avg_map, key=avg_map.get)
#             insights.append(
#                 f"Your fatigue tends to rise the most during <b>{top_behavior.lower()}</b> sessions."
#             )

#         return insights


















#25th March

# from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea
# from PySide6.QtCore import Qt
# from statistics import mean
# from collections import Counter, defaultdict

# class AIInsightsPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("AIInsightsPage")

#         # MAIN LAYOUT
#         self.main_layout = QVBoxLayout(self)
#         self.main_layout.setContentsMargins(30, 30, 30, 30)
#         self.main_layout.setSpacing(0)
#         self.main_layout.setAlignment(Qt.AlignTop)

#         # HEADER SECTION (Consistency with Reports)
#         header_container = QVBoxLayout()
#         header_container.setSpacing(8)
        
#         subtitle = QLabel("AI ANALYSIS")
#         subtitle.setStyleSheet("color: #4DA3FF; font-weight: 800; font-size: 11px; letter-spacing: 1.5px;")
        
#         title = QLabel("Focus Intelligence")
#         title.setStyleSheet("color: #E4E7F2; font-size: 32px; font-weight: 800; margin-bottom: 20px; letter-spacing: -1px;")
        
#         header_container.addWidget(subtitle)
#         header_container.addWidget(title)
#         self.main_layout.addLayout(header_container)

#         # SCROLL AREA (In case insights get long)
#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         scroll.setFrameShape(QFrame.NoFrame)
#         scroll.setStyleSheet("background: transparent;")
        
#         self.scroll_content = QWidget()
#         self.insight_container = QVBoxLayout(self.scroll_content)
#         self.insight_container.setSpacing(12) # Tight, snappy spacing
#         self.insight_container.setAlignment(Qt.AlignTop)
#         self.insight_container.setContentsMargins(0, 0, 0, 0)
        
#         scroll.setWidget(self.scroll_content)
#         self.main_layout.addWidget(scroll)

#         # Placeholder
#         self.update_insights([])

#     def update_insights(self, history):
#         insights_data = self.generate_insight_data(history)

#         # Clear old cards
#         while self.insight_container.count():
#             item = self.insight_container.takeAt(0)
#             if item.widget():
#                 item.widget().deleteLater()

#         # Add new "Premium" cards
#         for category, text in insights_data:
#             self.insight_container.addWidget(self.make_premium_card(category, text))

#     def make_premium_card(self, category: str, text: str) -> QFrame:
#         frame = QFrame()
#         # Ensure your CSS has styles for #InsightCard
#         frame.setObjectName("InsightCard")
#         frame.setStyleSheet("""
#             #InsightCard {
#                 background-color: rgba(255, 255, 255, 0.03);
#                 border: 1px solid rgba(255, 255, 255, 0.08);
#                 border-radius: 8px;
#             }
#         """)

#         layout = QVBoxLayout(frame)
#         layout.setContentsMargins(16, 16, 16, 16)
#         layout.setSpacing(6)

#         cat_label = QLabel(category.upper())
#         cat_label.setStyleSheet("color: rgba(228, 231, 242, 0.4); font-weight: 700; font-size: 9px; letter-spacing: 1px;")
        
#         content_label = QLabel(text)
#         content_label.setWordWrap(True)
#         content_label.setTextFormat(Qt.RichText)
#         content_label.setStyleSheet("color: #E4E7F2; font-size: 14px; font-weight: 400; line-height: 1.4;")

#         layout.addWidget(cat_label)
#         layout.addWidget(content_label)
#         return frame

#     def generate_insight_data(self, rows):
#         """Returns a list of tuples: (Category, Text)"""
#         if not rows:
#             return [("Status", "<i>Insufficient data. Start a session to generate AI insights.</i>")]

#         data = []

#         # 1. Patterns
#         behaviors = [r["behavior"] for r in rows if r.get("behavior")]
#         if behaviors:
#             most_common, _ = Counter(behaviors).most_common(1)[0]
#             data.append(("Core Pattern", f"Your focus is primarily centered on <b>{most_common.lower()}</b> tasks."))

#         # 2. Peak Time
#         by_hour = defaultdict(int)
#         for r in rows: by_hour[r["timestamp"].hour] += 1
#         segments = {
#             "Morning": sum(by_hour[h] for h in range(6, 12)),
#             "Afternoon": sum(by_hour[h] for h in range(12, 18)),
#             "Evening": sum(by_hour[h] for h in range(18, 24))
#         }
#         best_segment = max(segments, key=segments.get)
#         if segments[best_segment] > 0:
#             data.append(("Peak Activity", f"Analysis shows your cognitive endurance peaks during the <b>{best_segment}</b>."))

#         # 3. Fatigue Efficiency
#         fatigue_values = [r["fatigue"] for r in rows if r.get("fatigue", 0) > 0]
#         if fatigue_values:
#             avg_f = mean(fatigue_values)
#             data.append(("Fatigue", f"Average session strain is <b>{avg_f:.0f}%</b>. Breaks are currently optimized for this threshold."))

#         # 4. Critical Trigger
#         breaks = [r for r in rows if r.get("break_triggered")]
#         if breaks:
#             reasons = [r["break_reason"] for r in breaks if r.get("break_reason")]
#             if reasons:
#                 top_reason, _ = Counter(reasons).most_common(1)[0]
#                 data.append(("Triggers", f"Most breaks are preemptively triggered by <b>{top_reason.lower()}</b> detection."))

#         return data









# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QFont

# class AIInsightsPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("AIInsightsPage")

#         # MAIN LAYOUT
#         self.main_layout = QVBoxLayout(self)
#         self.main_layout.setContentsMargins(30, 30, 30, 30)
#         self.main_layout.setSpacing(0)
#         self.main_layout.setAlignment(Qt.AlignTop)

#         # -------------------------------------------------------
#         # MAIN TITLE: "Insights" (Stays Left Aligned)
#         # -------------------------------------------------------
#         self.title = QLabel("Insights")
#         self.title.setObjectName("PageTitle") 
#         self.main_layout.addWidget(self.title)

#         # SCROLL AREA
#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         scroll.setFrameShape(QFrame.NoFrame)
#         scroll.setStyleSheet("background: transparent;")
        
#         self.scroll_content = QWidget()
#         self.scroll_content.setObjectName("ScrollContent")
        
#         # CONTAINER FOR CARDS
#         self.insight_container = QVBoxLayout(self.scroll_content)
#         self.insight_container.setSpacing(0) 
#         self.insight_container.setAlignment(Qt.AlignTop)
        
#         # SHIFT TO THE RIGHT: Added 20px left margin here
#         # This indents all insights without moving the main "Insights" title
#         self.insight_container.setContentsMargins(20, 40, 0, 40) 
        
#         scroll.setWidget(self.scroll_content)
#         self.main_layout.addWidget(scroll)

#         self.update_insights([])

#     def make_card(self, category: str, text: str) -> QFrame:
#         frame = QFrame()
#         # Cleaned up the border-top to prevent it from clashing with the title
#         frame.setStyleSheet("""
#             QFrame {
#                 border-top: 1px solid #E2E8F0;
#                 padding-top: 20px;
#                 padding-bottom: 20px;
#                 background: transparent;
#             }
#         """)

#         layout = QVBoxLayout(frame)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(6)

#         # CATEGORY
#         cat_label = QLabel(category.upper())
#         cat_font = QFont("Segoe UI", 9)
#         cat_font.setWeight(QFont.Bold)
#         cat_font.setLetterSpacing(QFont.AbsoluteSpacing, 0.5)
#         cat_label.setFont(cat_font)
#         cat_label.setStyleSheet("color: #64748B; border: none;")
        
#         # CONTENT
#         content_label = QLabel(text)
#         content_label.setWordWrap(True)
#         content_label.setTextFormat(Qt.RichText)
#         content_font = QFont("Segoe UI", 12)
#         content_label.setFont(content_font)
#         content_label.setStyleSheet("color: #1A1A1A; border: none; line-height: 140%;")

#         layout.addWidget(cat_label)
#         layout.addWidget(content_label)
#         return frame

#     def update_insights(self, history):
#         while self.insight_container.count():
#             item = self.insight_container.takeAt(0)
#             if item.widget(): item.widget().deleteLater()
        
#         # Example card
#         self.insight_container.addWidget(
#             self.make_card("Status", "Insufficient data. Start a session to generate insights.")
#         )


















# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QFont

# class AIInsightsPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("AIInsightsPage")

#         # MAIN LAYOUT
#         self.main_layout = QVBoxLayout(self)
#         self.main_layout.setContentsMargins(30, 30, 30, 30)
#         self.main_layout.setSpacing(0)
#         self.main_layout.setAlignment(Qt.AlignTop)

#         # --- MAIN TITLE: "Insights" ---
#         self.title = QLabel("Insights")
#         self.title.setObjectName("PageTitle") # Styled by external QSS
#         self.main_layout.addWidget(self.title)

#         # SCROLL AREA
#         scroll = QScrollArea()
#         scroll.setWidgetResizable(True)
#         scroll.setFrameShape(QFrame.NoFrame)
#         scroll.setStyleSheet("background: transparent;")
        
#         self.scroll_content = QWidget()
#         self.scroll_content.setObjectName("ScrollContent")
        
#         self.insight_container = QVBoxLayout(self.scroll_content)
#         self.insight_container.setSpacing(0) 
#         self.insight_container.setAlignment(Qt.AlignTop)
#         self.insight_container.setContentsMargins(20, 40, 0, 40) 
        
#         scroll.setWidget(self.scroll_content)
#         self.main_layout.addWidget(scroll)

#         # Initial call
#         self.update_insights([])

#     def make_card(self, category: str, text: str, title_color: str) -> QFrame:
#         frame = QFrame()
#         # You may want to change the border color to match your theme (e.g., #333333 for dark)
#         frame.setStyleSheet("""
#             QFrame {
#                 border-top: 1px solid #E2E8F0;
#                 padding-top: 20px;
#                 padding-bottom: 20px;
#                 background: transparent;
#             }
#         """)

#         layout = QVBoxLayout(frame)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(6)

#         # CATEGORY (Stay Gray/Slate)
#         cat_label = QLabel(category.upper())
#         cat_font = QFont("Segoe UI", 9)
#         cat_font.setWeight(QFont.Bold)
#         cat_label.setFont(cat_font)
#         cat_label.setStyleSheet("color: #64748B; border: none;")
        
#         # CONTENT (The Result Text)
#         content_label = QLabel(text)
#         content_label.setWordWrap(True)
#         content_label.setTextFormat(Qt.RichText)
#         content_font = QFont("Segoe UI", 12)
#         content_label.setFont(content_font)
        
#         # --- THE FIX ---
#         # We apply the QSS title_color here so it matches the PageTitle
#         content_label.setStyleSheet(f"color: {title_color}; border: none; line-height: 140%;")

#         layout.addWidget(cat_label)
#         layout.addWidget(content_label)
#         return frame

#     def update_insights(self, history):
#         # 1. Grab the ACTUAL color from the QSS-styled title
#         qss_title_color = self.title.palette().color(self.title.foregroundRole()).name()

#         # 2. Clear previous items
#         while self.insight_container.count():
#             item = self.insight_container.takeAt(0)
#             if item.widget(): item.widget().deleteLater()
        
#         # 3. Pass the color into the card creator
#         self.insight_container.addWidget(
#             self.make_card(
#                 "Status", 
#                 "Insufficient data. Start a session to generate insights.",
#                 title_color=qss_title_color
#             )
#         )









# mac and windows and linux version

import platform  # Added for cross-platform font detection
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# --- CROSS-PLATFORM FONT LOGIC ---
if platform.system() == "Darwin":
    UI_FONT = ".AppleSystemUIFont"
else:
    UI_FONT = "Segoe UI"

class AIInsightsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("AIInsightsPage")

        # MAIN LAYOUT
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignTop)

        # --- MAIN TITLE: "Insights" ---
        self.title = QLabel("Insights")
        self.title.setObjectName("PageTitle") # Styled by external QSS
        self.main_layout.addWidget(self.title)

        # SCROLL AREA
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        self.scroll_content = QWidget()
        self.scroll_content.setObjectName("ScrollContent")
        
        self.insight_container = QVBoxLayout(self.scroll_content)
        self.insight_container.setSpacing(0) 
        self.insight_container.setAlignment(Qt.AlignTop)
        self.insight_container.setContentsMargins(20, 40, 0, 40) 
        
        scroll.setWidget(self.scroll_content)
        self.main_layout.addWidget(scroll)

        # Initial call
        self.update_insights([])

    def make_card(self, category: str, text: str, title_color: str) -> QFrame:
        frame = QFrame()
        # You may want to change the border color to match your theme (e.g., #333333 for dark)
        frame.setStyleSheet("""
            QFrame {
                border-top: 1px solid #E2E8F0;
                padding-top: 20px;
                padding-bottom: 20px;
                background: transparent;
            }
        """)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # CATEGORY (Stay Gray/Slate)
        cat_label = QLabel(category.upper())
        # Corrected: Use UI_FONT variable
        cat_font = QFont(UI_FONT, 9)
        cat_font.setWeight(QFont.Bold)
        cat_label.setFont(cat_font)
        cat_label.setStyleSheet("color: #64748B; border: none;")
        
        # CONTENT (The Result Text)
        content_label = QLabel(text)
        content_label.setWordWrap(True)
        content_label.setTextFormat(Qt.RichText)
        # Corrected: Use UI_FONT variable
        content_font = QFont(UI_FONT, 12)
        content_label.setFont(content_font)
        
        # --- THE FIX ---
        # We apply the QSS title_color here so it matches the PageTitle
        content_label.setStyleSheet(f"color: {title_color}; border: none; line-height: 140%;")

        layout.addWidget(cat_label)
        layout.addWidget(content_label)
        return frame

    def update_insights(self, history):
        # 1. Grab the ACTUAL color from the QSS-styled title
        qss_title_color = self.title.palette().color(self.title.foregroundRole()).name()

        # 2. Clear previous items
        while self.insight_container.count():
            item = self.insight_container.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        
        # 3. Pass the color into the card creator
        self.insight_container.addWidget(
            self.make_card(
                "Status", 
                "Insufficient data. Start a session to generate insights.",
                title_color=qss_title_color
            )
        )