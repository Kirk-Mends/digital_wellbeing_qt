# import csv
# from datetime import datetime, timedelta
# from statistics import mean


# class AnalyticsEngine:
#     def __init__(self, csv_path="usage_log.csv"):
#         self.csv_path = csv_path

#     # ---------- LOW-LEVEL LOADING ----------

#     def _load_range(self, days_back: int):
#         today = datetime.now().date()
#         start = today - timedelta(days=days_back - 1)

#         entries = []
#         try:
#             with open(self.csv_path, "r") as f:
#                 reader = csv.DictReader(f)
#                 for row in reader:
#                     date = datetime.fromisoformat(row["date"]).date()
#                     if start <= date <= today:
#                         entries.append({
#                             "date": date,
#                             "active": float(row["active_minutes"])
#                         })
#         except FileNotFoundError:
#             return []

#         return entries

#     def _aggregate_daily(self, entries):
#         daily = {}
#         for e in entries:
#             daily.setdefault(e["date"], 0)
#             daily[e["date"]] += e["active"]
#         days = sorted(daily.keys())
#         values = [daily[d] for d in days]
#         return days, values, daily

#     # ---------- WEEKLY SUMMARY ----------

#     def weekly_summary(self):
#         entries = self._load_range(7)
#         if not entries:
#             return None

#         days, values, daily = self._aggregate_daily(entries)

#         avg = mean(values)
#         total = sum(values)
#         best_day = days[values.index(max(values))].strftime("%A")
#         worst_day = days[values.index(min(values))].strftime("%A")
#         trend = "up" if values[-1] > values[0] else "down"

#         return {
#             "avg": avg,
#             "total": total,
#             "best_day": best_day,
#             "worst_day": worst_day,
#             "trend": trend,
#             "daily": daily,
#         }

#     # ---------- MONTHLY SUMMARY ----------

#     def monthly_summary(self):
#         entries = self._load_range(30)
#         if not entries:
#             return None

#         days, values, daily = self._aggregate_daily(entries)

#         avg = mean(values)
#         total = sum(values)
#         best_day = days[values.index(max(values))].strftime("%A")
#         worst_day = days[values.index(min(values))].strftime("%A")

#         # weekly breakdown
#         weeks = []
#         for i in range(0, len(values), 7):
#             week_vals = values[i:i + 7]
#             if week_vals:
#                 weeks.append(sum(week_vals))

#         best_week = max(weeks) if weeks else 0
#         worst_week = min(weeks) if weeks else 0

#         trend = "up" if values[-1] > values[0] else "down"

#         diffs = []
#         for i in range(1, len(values)):
#             diffs.append(abs(values[i] - values[i - 1]))
#         consistency = max(0, 100 - mean(diffs)) if diffs else 100

#         return {
#             "avg": avg,
#             "total": total,
#             "best_day": best_day,
#             "worst_day": worst_day,
#             "best_week": best_week,
#             "worst_week": worst_week,
#             "trend": trend,
#             "consistency": consistency,
#             "daily": daily,
#         }

#     # ---------- AI INSIGHTS (LIGHTWEIGHT) ----------

#     def ai_insights(self):
#         entries = self._load_range(30)
#         if not entries:
#             return ["No activity data available yet."]

#         parsed = entries
#         insights = []

#         avg = mean([p["active"] for p in parsed])
#         insights.append(f"Your average active time per day is {avg:.1f} minutes.")

#         # best day of week
#         by_day = {}
#         for p in parsed:
#             day = p["date"].strftime("%A")
#             by_day.setdefault(day, []).append(p["active"])
#         best_day = max(by_day, key=lambda d: mean(by_day[d]))
#         insights.append(f"Your most productive day is typically {best_day}.")

#         # evening drop
#         evening = [p for p in parsed if p["date"].weekday() < 5 and p["date"].day == p["date"].day and p["date"]]
#         # (we’ll keep this simple: skip evening detail if messy)
#         # weekend pattern
#         weekend = [p for p in parsed if p["date"].weekday() >= 5]
#         if weekend:
#             avg_weekend = mean([p["active"] for p in weekend])
#             if avg_weekend < avg * 0.7:
#                 insights.append("You tend to be less active on weekends.")

#         # consistency
#         daily = {}
#         for p in parsed:
#             d = p["date"]
#             daily.setdefault(d, 0)
#             daily[d] += p["active"]
#         if len(daily) >= 5:
#             days = sorted(daily.keys())
#             vals = [daily[d] for d in days]
#             diffs = [abs(vals[i] - vals[i - 1]) for i in range(1, len(vals))]
#             consistency = max(0, 100 - mean(diffs))
#             insights.append(f"Your break consistency score is {consistency:.0f}/100.")

#         return insights

#     # ---------- HEATMAP DATA ----------

#     def heatmap_data(self):
#         # simple: day-of-week vs total active minutes
#         entries = self._load_range(30)
#         if not entries:
#             return None

#         by_dow = {i: 0 for i in range(7)}  # 0=Mon
#         for e in entries:
#             dow = e["date"].weekday()
#             by_dow[dow] += e["active"]

#         return by_dow

#     # ---------- BREAK QUALITY SCORE ----------
#     def break_quality_score(self):
#         """
#         Computes a 0–100 score based on:
#         - Break frequency
#         - Break timing (not too late)
#         - Fatigue recovery patterns
#         - Meeting-mode interruptions
#         - Consistency across days
#         """

#         entries = self._load_range(7)  # last 7 days
#         if not entries:
#             return None

#         # Aggregate daily totals
#         days, values, daily = self._aggregate_daily(entries)

#         # 1. Frequency score (ideal: 3–6 breaks/day)
#         freq_scores = []
#         for d in days:
#             # You can later replace this with real break count from your engine
#             active = daily[d]
#             est_breaks = max(1, active // 45)  # rough estimate
#             if 3 <= est_breaks <= 6:
#                 freq_scores.append(100)
#             else:
#                 freq_scores.append(max(0, 100 - abs(est_breaks - 4) * 20))

#         freq_score = mean(freq_scores)

#         # 2. Consistency score (similar to monthly logic)
#         diffs = [abs(values[i] - values[i - 1]) for i in range(1, len(values))]
#         consistency = max(0, 100 - mean(diffs)) if diffs else 100

#         # 3. Timing score (reward shorter days with more breaks)
#         timing_score = 100 if mean(values) < 120 else 70

#         # Final weighted score
#         final = (
#             freq_score * 0.45 +
#             consistency * 0.35 +
#             timing_score * 0.20
#         )

#         return {
#             "score": round(final),
#             "frequency": round(freq_score),
#             "consistency": round(consistency),
#             "timing": round(timing_score),
#         }



























# # 5 
# # upgraded 
# # core/analytics_engine.py

# from datetime import datetime
# from typing import Dict, List, Any, Optional


# class AnalyticsEngine:
#     """
#     Premium, behavior-aware analytics engine interface.

#     This class is intentionally structured and future-proof:
#     - You can back it with a local DB, JSON, CSV, or cloud sync later.
#     - The UI (AnalyticsSuitePage) and ExportManager depend only on this API.
#     - All methods return simple Python structures (dicts, lists, primitives).
#     """

#     def __init__(self):
#         # In the future, you can inject a storage / repository here.
#         # Example: self.store = SomeDataStore(...)
#         pass

#     # -------------------------------------------------
#     # BEHAVIOR
#     # -------------------------------------------------
#     def behavior_distribution(self) -> Dict[str, float]:
#         """
#         Returns total time per behavior for the current period (e.g., today).
#         Example: {"Reading": 120, "Coding": 90, "Watching": 45}
#         """
#         return {}

#     def behavior_timeline(self) -> Dict[str, List[Any]]:
#         """
#         Returns a timeline of behaviors across the day.

#         Expected structure:
#         {
#             "times": [datetime, datetime, ...],
#             "behaviors": ["Reading", "Coding", ...]
#         }
#         """
#         return {"times": [], "behaviors": []}

#     def behavior_by_hour(self) -> Dict[int, Dict[str, float]]:
#         """
#         Returns behavior distribution by hour of day.

#         Example:
#         {
#             9: {"Reading": 30, "Coding": 10},
#             10: {"Reading": 15, "Watching": 20},
#             ...
#         }
#         """
#         return {}

#     def longest_behavior_streak(self) -> Optional[Dict[str, Any]]:
#         """
#         Returns info about the longest continuous streak of a single behavior.

#         Example:
#         {
#             "behavior": "Reading",
#             "minutes": 42
#         }

#         Return None if no data.
#         """
#         return None

#     # -------------------------------------------------
#     # FATIGUE
#     # -------------------------------------------------
#     def fatigue_trend(self) -> Dict[str, List[Any]]:
#         """
#         Returns fatigue values over time.

#         Expected structure:
#         {
#             "times": [datetime, datetime, ...],
#             "fatigue": [0-100, 0-100, ...]
#         }
#         """
#         return {"times": [], "fatigue": []}

#     def fatigue_by_behavior(self) -> Dict[str, float]:
#         """
#         Returns average fatigue per behavior.

#         Example:
#         {
#             "Reading": 35.2,
#             "Coding": 62.7,
#             "Watching": 28.1
#         }
#         """
#         return {}

#     def fatigue_recovery_after_breaks(self) -> Dict[str, List[Any]]:
#         """
#         Returns fatigue values around breaks (before/after).

#         Expected structure:
#         {
#             "times": [datetime, ...],
#             "fatigue": [0-100, ...]
#         }
#         """
#         return {"times": [], "fatigue": []}

#     def highest_fatigue_moment(self) -> Optional[Dict[str, Any]]:
#         """
#         Returns the highest fatigue moment.

#         Example:
#         {
#             "time": datetime,
#             "fatigue": 87.0
#         }

#         Return None if no data.
#         """
#         return None

#     # -------------------------------------------------
#     # BREAKS
#     # -------------------------------------------------
#     def break_reasons(self) -> Dict[str, int]:
#         """
#         Returns counts of break reasons.

#         Example:
#         {
#             "Strain Risk": 5,
#             "Fatigue Early": 3,
#             "Interval Reached": 4
#         }
#         """
#         return {}

#     def break_timing_quality(self) -> Dict[str, int]:
#         """
#         Returns counts of break timing quality.

#         Expected keys:
#         - "early"
#         - "on_time"
#         - "late"

#         Example:
#         {
#             "early": 2,
#             "on_time": 6,
#             "late": 1
#         }
#         """
#         return {}

#     def break_events_timeline(self) -> Dict[str, List[Any]]:
#         """
#         Returns timestamps of breaks.

#         Expected structure:
#         {
#             "times": [datetime, datetime, ...]
#         }
#         """
#         return {"times": []}

#     def break_suppression_stats(self) -> Dict[str, int]:
#         """
#         Returns counts of break suppression by type.

#         Example:
#         {
#             "Meeting": 4,
#             "Watching": 2,
#             "Gaming": 1
#         }
#         """
#         return {}

#     # -------------------------------------------------
#     # SUPPRESSION
#     # -------------------------------------------------
#     def suppression_counts(self) -> Dict[str, int]:
#         """
#         Returns counts of suppression events by type.

#         Example:
#         {
#             "Meeting": 10,
#             "Watching": 6,
#             "Gaming": 3
#         }
#         """
#         return {}

#     def away_resets_count(self) -> int:
#         """
#         Returns number of away-based resets.
#         """
#         return 0

#     # -------------------------------------------------
#     # TIME OF DAY (HEATMAPS)
#     # -------------------------------------------------
#     def behavior_heatmap(self) -> Dict[int, float]:
#         """
#         Returns behavior intensity by hour.

#         Simple 1D heatmap structure:
#         {
#             hour (0-23): value,
#             ...
#         }
#         """
#         return {}

#     def fatigue_heatmap(self) -> Dict[int, float]:
#         """
#         Returns fatigue intensity by hour.

#         Same structure as behavior_heatmap.
#         """
#         return {}

#     def break_heatmap(self) -> Dict[int, float]:
#         """
#         Returns break frequency by hour.

#         Same structure as behavior_heatmap.
#         """
#         return {}

#     def suppression_heatmap(self) -> Dict[int, float]:
#         """
#         Returns suppression intensity by hour.

#         Same structure as behavior_heatmap.
#         """
#         return {}

#     # -------------------------------------------------
#     # WEEKLY / MONTHLY
#     # -------------------------------------------------
#     def weekly_behavior_summary(self) -> Optional[Dict[str, Any]]:
#         """
#         Returns a weekly summary with behavior, fatigue, breaks, suppression.

#         Expected structure:
#         {
#             "distribution": {behavior: minutes},
#             "fatigue_trend": {
#                 "days": [date, ...],
#                 "fatigue": [0-100, ...]
#             },
#             "break_consistency": 0-100,
#             "suppression_counts": {type: count}
#         }

#         Return None if no data.
#         """
#         return None

#     def monthly_behavior_summary(self) -> Optional[Dict[str, Any]]:
#         """
#         Same idea as weekly_behavior_summary, but for the month.
#         """
#         return None

#     # -------------------------------------------------
#     # AI INSIGHTS
#     # -------------------------------------------------
#     def ai_insights(self) -> List[str]:
#         """
#         Returns a list of short, warm, behavior-aware insights.

#         Example:
#         [
#             "Your longest deep work streak this week was 42 minutes in Coding.",
#             "Afternoon fatigue tends to rise after long Watching sessions."
#         ]
#         """
#         # Placeholder so the UI shows something instead of being empty.
#         return ["Analytics are setting up. Once you’ve used the app a bit more, you’ll see rich insights here."]

#     # -------------------------------------------------
#     # EXPORT AGGREGATION
#     # -------------------------------------------------
#     def export_all_data(self) -> Dict[str, Dict[str, Any]]:
#         """
#         Collects all key analytics into a single structure for export.

#         This is what ExportManager uses to generate CSV / Excel / PDF.
#         """
#         weekly = self.weekly_behavior_summary() or {}
#         monthly = self.monthly_behavior_summary() or {}

#         return {
#             "Behavior Distribution": self.behavior_distribution(),
#             "Behavior Timeline": self.behavior_timeline(),
#             "Fatigue Trend": self.fatigue_trend(),
#             "Fatigue by Behavior": self.fatigue_by_behavior(),
#             "Break Reasons": self.break_reasons(),
#             "Break Timing": self.break_timing_quality(),
#             "Break Suppression": self.break_suppression_stats(),
#             "Suppression Counts": self.suppression_counts(),
#             "Weekly Summary": weekly,
#             "Monthly Summary": monthly,
#             "AI Insights": {"insights": self.ai_insights()},
#         }













# updated
# # core/analytics_engine.py

# from datetime import datetime, timedelta
# from typing import Dict, List, Any, Optional

# from core.storage_manager import StorageManager
# from core.weekly_summary_engine import WeeklySummaryEngine
# from core.monthly_summary_engine import MonthlySummaryEngine


# class AnalyticsEngine:
#     """
#     Premium, behavior-aware analytics engine interface.

#     Backed by:
#     - Daily summaries (via StorageManager)
#     - WeeklySummaryEngine
#     - MonthlySummaryEngine

#     This keeps the architecture stable, fast, and future-proof.
#     """

#     def __init__(self):
#         self.storage = StorageManager()
#         self.weekly_engine = WeeklySummaryEngine()
#         self.monthly_engine = MonthlySummaryEngine()

#     # -------------------------------------------------
#     # HELPERS
#     # -------------------------------------------------
#     def _get_daily_summary(self, date: datetime) -> Optional[Dict[str, Any]]:
#         date_str = date.strftime("%Y-%m-%d")
#         row = self.storage.get_daily_summary(date_str)
#         if not row:
#             return None

#         # row = (date, total_focus, deep_work, deep_reading,
#         #        focused_interaction, breaks, avg_fatigue)
#         return {
#             "date": row[0],
#             "total_focus": row[1],
#             "deep_work": row[2],
#             "deep_reading": row[3],
#             "focused_interaction": row[4],
#             "breaks": row[5],
#             "avg_fatigue": row[6],
#         }

#     # -------------------------------------------------
#     # BEHAVIOR
#     # -------------------------------------------------
#     def behavior_distribution(self) -> Dict[str, float]:
#         """
#         Returns total time per behavior for TODAY,
#         based on the daily summary.
#         """
#         today = datetime.now()
#         summary = self._get_daily_summary(today)
#         if not summary:
#             return {}

#         return {
#             "Deep Work": summary["deep_work"],
#             "Deep Reading": summary["deep_reading"],
#             "Focused Interaction": summary["focused_interaction"],
#         }

#     def behavior_timeline(self) -> Dict[str, List[Any]]:
#         """
#         Requires raw behavior logs (per-interval events).
#         Left as a placeholder until behavior log schema is finalized.
#         """
#         return {"times": [], "behaviors": []}

#     def behavior_by_hour(self) -> Dict[int, Dict[str, float]]:
#         """
#         Requires per-interval behavior logs with timestamps.
#         Placeholder for now.
#         """
#         return {}

#     def longest_behavior_streak(self) -> Optional[Dict[str, Any]]:
#         """
#         Requires contiguous behavior segments from raw logs.
#         Placeholder for now.
#         """
#         return None

#     # -------------------------------------------------
#     # FATIGUE
#     # -------------------------------------------------
#     def fatigue_trend(self) -> Dict[str, List[Any]]:
#         """
#         Returns fatigue values over the last 7 days,
#         using daily summaries.
#         """
#         times: List[datetime] = []
#         values: List[float] = []

#         today = datetime.now().date()
#         for i in range(6, -1, -1):
#             day = today - timedelta(days=i)
#             summary = self._get_daily_summary(datetime.combine(day, datetime.min.time()))
#             if summary and summary["avg_fatigue"] > 0:
#                 times.append(datetime.combine(day, datetime.min.time()))
#                 values.append(summary["avg_fatigue"])

#         return {"times": times, "fatigue": values}

#     def fatigue_by_behavior(self) -> Dict[str, float]:
#         """
#         Requires per-interval fatigue + behavior logs.
#         Placeholder for now.
#         """
#         return {}

#     def fatigue_recovery_after_breaks(self) -> Dict[str, List[Any]]:
#         """
#         Requires fatigue values around break timestamps.
#         Placeholder for now.
#         """
#         return {"times": [], "fatigue": []}

#     def highest_fatigue_moment(self) -> Optional[Dict[str, Any]]:
#         """
#         Uses daily summaries to find the highest daily average fatigue
#         over the last 14 days.
#         """
#         highest = None
#         today = datetime.now().date()

#         for i in range(0, 14):
#             day = today - timedelta(days=i)
#             summary = self._get_daily_summary(datetime.combine(day, datetime.min.time()))
#             if summary and summary["avg_fatigue"] > 0:
#                 if highest is None or summary["avg_fatigue"] > highest["fatigue"]:
#                     highest = {
#                         "time": datetime.combine(day, datetime.min.time()),
#                         "fatigue": summary["avg_fatigue"],
#                     }

#         return highest

#     # -------------------------------------------------
#     # BREAKS
#     # -------------------------------------------------
#     def break_reasons(self) -> Dict[str, int]:
#         """
#         Requires detailed break log with reasons.
#         Placeholder for now.
#         """
#         return {}

#     def break_timing_quality(self) -> Dict[str, int]:
#         """
#         Requires break timing classification (early/on_time/late).
#         Placeholder for now.
#         """
#         return {}

#     def break_events_timeline(self) -> Dict[str, List[Any]]:
#         """
#         Requires raw break timestamps.
#         Placeholder for now.
#         """
#         return {"times": []}

#     def break_suppression_stats(self) -> Dict[str, int]:
#         """
#         Requires suppression events tied to breaks.
#         Placeholder for now.
#         """
#         return {}

#     # -------------------------------------------------
#     # SUPPRESSION
#     # -------------------------------------------------
#     def suppression_counts(self) -> Dict[str, int]:
#         """
#         Requires suppression event log.
#         Placeholder for now.
#         """
#         return {}

#     def away_resets_count(self) -> int:
#         """
#         Requires away-reset events.
#         Placeholder for now.
#         """
#         return 0

#     # -------------------------------------------------
#     # TIME OF DAY (HEATMAPS)
#     # -------------------------------------------------
#     def behavior_heatmap(self) -> Dict[int, float]:
#         """
#         Could be derived from behavior logs by hour.
#         Placeholder for now.
#         """
#         return {}

#     def fatigue_heatmap(self) -> Dict[int, float]:
#         """
#         Could be derived from fatigue logs by hour.
#         Placeholder for now.
#         """
#         return {}

#     def break_heatmap(self) -> Dict[int, float]:
#         """
#         Could be derived from break logs by hour.
#         Placeholder for now.
#         """
#         return {}

#     def suppression_heatmap(self) -> Dict[int, float]:
#         """
#         Could be derived from suppression logs by hour.
#         Placeholder for now.
#         """
#         return {}

#     # -------------------------------------------------
#     # WEEKLY / MONTHLY
#     # -------------------------------------------------
#     def weekly_behavior_summary(self) -> Optional[Dict[str, Any]]:
#         """
#         Wraps WeeklySummaryEngine for the current week.
#         """
#         summary = self.weekly_engine.generate_this_week()
#         if not summary:
#             return None

#         return summary

#     def monthly_behavior_summary(self) -> Optional[Dict[str, Any]]:
#         """
#         Wraps MonthlySummaryEngine for the current month.
#         """
#         summary = self.monthly_engine.generate_this_month()
#         if not summary:
#             return None

#         return summary

#     # -------------------------------------------------
#     # AI INSIGHTS
#     # -------------------------------------------------
#     def ai_insights(self) -> List[str]:
#         """
#         Uses weekly + monthly summaries to generate warm, behavior-aware insights.
#         """
#         insights: List[str] = []

#         weekly = self.weekly_behavior_summary()
#         monthly = self.monthly_behavior_summary()

#         if weekly:
#             if weekly["deep_work"] > 0:
#                 insights.append(
#                     f"Your deep work time this week reached {weekly['deep_work']} minutes — strong focused effort."
#                 )
#             if weekly["avg_fatigue"] > 60:
#                 insights.append(
#                     "Fatigue was elevated this week. Consider lighter sessions or more frequent short breaks."
#                 )

#         if monthly:
#             if monthly["total_focus"] > 0:
#                 insights.append(
#                     f"This month you accumulated {monthly['total_focus']} focused minutes — steady engagement over time."
#                 )
#             if monthly["breaks"] < 20:
#                 insights.append(
#                     "Breaks were relatively rare this month. Adding short pauses may support better recovery."
#                 )

#         if not insights:
#             insights.append(
#                 "Analytics are setting up. Once you’ve used the app a bit more, you’ll see rich insights here."
#             )

#         return insights

#     # -------------------------------------------------
#     # EXPORT AGGREGATION
#     # -------------------------------------------------
#     def export_all_data(self) -> Dict[str, Dict[str, Any]]:
#         """
#         Collects all key analytics into a single structure for export.

#         This is what ExportManager uses to generate CSV / Excel / PDF.
#         """
#         weekly = self.weekly_behavior_summary() or {}
#         monthly = self.monthly_behavior_summary() or {}

#         return {
#             "Behavior Distribution": self.behavior_distribution(),
#             "Behavior Timeline": self.behavior_timeline(),
#             "Fatigue Trend": self.fatigue_trend(),
#             "Fatigue by Behavior": self.fatigue_by_behavior(),
#             "Break Reasons": self.break_reasons(),
#             "Break Timing": self.break_timing_quality(),
#             "Break Suppression": self.break_suppression_stats(),
#             "Suppression Counts": self.suppression_counts(),
#             "Weekly Summary": weekly,
#             "Monthly Summary": monthly,
#             "AI Insights": {"insights": self.ai_insights()},
#         }





















# # core/analytics_engine.py

# from datetime import datetime, timedelta
# from typing import Dict, List, Any, Optional
# from collections import defaultdict, Counter

# from core.storage_manager import StorageManager
# from core.weekly_summary_engine import WeeklySummaryEngine
# from core.monthly_summary_engine import MonthlySummaryEngine


# class AnalyticsEngine:
#     """
#     Premium, behavior-aware analytics engine.

#     Hybrid model:
#     - Today → raw logs (behavior, fatigue, breaks, suppression)
#     - Last 7 days → heatmaps
#     - Weekly / Monthly → summary engines
#     - AI Insights → weekly + monthly + last 7 days logs
#     """

#     def __init__(self):
#         self.storage = StorageManager()
#         self.weekly_engine = WeeklySummaryEngine()
#         self.monthly_engine = MonthlySummaryEngine()

#         # Premium behavior category mapping
#         self.behavior_map = {
#             "deep_work": "Deep Work",
#             "coding": "Deep Work",
#             "writing": "Deep Work",
#             "multitasking": "Deep Work",

#             "reading": "Deep Reading",

#             "meeting": "Focused Interaction",
#             "focused_interaction": "Focused Interaction",
#             "heavy_browsing": "Focused Interaction",
#         }

#     # -------------------------------------------------
#     # INTERNAL HELPERS
#     # -------------------------------------------------
#     def _today_bounds(self):
#         today = datetime.now().date()
#         start = datetime.combine(today, datetime.min.time())
#         end = start + timedelta(days=1)
#         return start, end

#     def _last_7_days_bounds(self):
#         end = datetime.now()
#         start = end - timedelta(days=7)
#         return start, end

#     def _categorize_behavior(self, raw: str) -> Optional[str]:
#         return self.behavior_map.get(raw, None)

#     # -------------------------------------------------
#     # BEHAVIOR
#     # -------------------------------------------------
#     def behavior_distribution(self) -> Dict[str, float]:
#         """
#         Total minutes per behavior category for TODAY.
#         """
#         start, end = self._today_bounds()
#         events = self.storage.get_behavior_events(start, end)

#         totals = Counter()

#         for ts, behavior, duration, fatigue, mode in events:
#             cat = self._categorize_behavior(behavior)
#             if not cat:
#                 continue

#             # Duration may be None (event-based logging)
#             if duration:
#                 totals[cat] += duration
#             else:
#                 totals[cat] += 1  # assume 1-minute minimum

#         return dict(totals)

#     def behavior_timeline(self) -> Dict[str, List[Any]]:
#         """
#         Returns a stepped timeline for TODAY.
#         """
#         start, end = self._today_bounds()
#         events = self.storage.get_behavior_events(start, end)

#         times = []
#         behaviors = []

#         for ts, behavior, duration, fatigue, mode in events:
#             cat = self._categorize_behavior(behavior)
#             if not cat:
#                 continue
#             times.append(ts)
#             behaviors.append(cat)

#         return {"times": times, "behaviors": behaviors}

#     def behavior_by_hour(self) -> Dict[int, Dict[str, float]]:
#         """
#         Returns behavior minutes grouped by hour for TODAY.
#         """
#         start, end = self._today_bounds()
#         events = self.storage.get_behavior_events(start, end)

#         hourly = defaultdict(lambda: Counter())

#         for ts, behavior, duration, fatigue, mode in events:
#             cat = self._categorize_behavior(behavior)
#             if not cat:
#                 continue

#             dt = datetime.fromisoformat(ts)
#             hour = dt.hour

#             if duration:
#                 hourly[hour][cat] += duration
#             else:
#                 hourly[hour][cat] += 1

#         return {h: dict(c) for h, c in hourly.items()}

#     def longest_behavior_streak(self) -> Optional[Dict[str, Any]]:
#         """
#         Longest contiguous streak of the same behavior TODAY.
#         """
#         start, end = self._today_bounds()
#         events = self.storage.get_behavior_events(start, end)

#         last_cat = None
#         current_len = 0
#         best_cat = None
#         best_len = 0

#         for ts, behavior, duration, fatigue, mode in events:
#             cat = self._categorize_behavior(behavior)
#             if not cat:
#                 continue

#             if cat == last_cat:
#                 current_len += duration or 1
#             else:
#                 current_len = duration or 1
#                 last_cat = cat

#             if current_len > best_len:
#                 best_len = current_len
#                 best_cat = cat

#         if not best_cat:
#             return None

#         return {"behavior": best_cat, "minutes": best_len}

#     # -------------------------------------------------
#     # FATIGUE
#     # -------------------------------------------------
#     def fatigue_trend(self) -> Dict[str, List[Any]]:
#         """
#         Fatigue values for TODAY (minute-based).
#         """
#         start, end = self._today_bounds()
#         events = self.storage.get_fatigue_events(start, end)

#         times = [ts for ts, f in events]
#         values = [f for ts, f in events]

#         return {"times": times, "fatigue": values}

#     def fatigue_by_behavior(self) -> Dict[str, float]:
#         """
#         Average fatigue per behavior category TODAY.
#         """
#         start, end = self._today_bounds()
#         beh = self.storage.get_behavior_events(start, end)

#         totals = Counter()
#         counts = Counter()

#         for ts, behavior, duration, fatigue, mode in beh:
#             cat = self._categorize_behavior(behavior)
#             if not cat:
#                 continue
#             if fatigue is None:
#                 continue

#             totals[cat] += fatigue
#             counts[cat] += 1

#         return {cat: totals[cat] / counts[cat] for cat in totals}

#     def fatigue_recovery_after_breaks(self) -> Dict[str, List[Any]]:
#         """
#         Fatigue values around break timestamps TODAY.
#         """
#         start, end = self._today_bounds()
#         breaks = self.storage.get_break_events(start, end)
#         fatigue = self.storage.get_fatigue_events(start, end)

#         if not breaks or not fatigue:
#             return {"times": [], "fatigue": []}

#         # Simple model: fatigue values 10 minutes after each break
#         times = []
#         values = []

#         fatigue_points = [(datetime.fromisoformat(ts), f) for ts, f in fatigue]

#         for ts, reason, behavior, f, interval_used, tq in breaks:
#             bt = datetime.fromisoformat(ts)
#             window_end = bt + timedelta(minutes=10)

#             window_vals = [fv for t, fv in fatigue_points if bt <= t <= window_end]
#             if window_vals:
#                 times.append(ts)
#                 values.append(sum(window_vals) / len(window_vals))

#         return {"times": times, "fatigue": values}

#     def highest_fatigue_moment(self) -> Optional[Dict[str, Any]]:
#         """
#         Highest fatigue value TODAY.
#         """
#         start, end = self._today_bounds()
#         events = self.storage.get_fatigue_events(start, end)

#         if not events:
#             return None

#         ts, f = max(events, key=lambda x: x[1])
#         return {"time": ts, "fatigue": f}

#     # -------------------------------------------------
#     # BREAKS
#     # -------------------------------------------------
#     def break_reasons(self) -> Dict[str, int]:
#         start, end = self._today_bounds()
#         events = self.storage.get_break_events(start, end)
#         return dict(Counter(reason for ts, reason, b, f, i, tq, mode in events))

#     def break_timing_quality(self) -> Dict[str, int]:
#         start, end = self._today_bounds()
#         events = self.storage.get_break_events(start, end)
#         return dict(Counter(tq for ts, r, b, f, i, tq, mode in events))

#     def break_events_timeline(self) -> Dict[str, List[Any]]:
#         start, end = self._today_bounds()
#         events = self.storage.get_break_events(start, end)
#         times = [ts for ts, r, b, f, i, tq, mode in events]
#         return {"times": times}

#     def break_suppression_stats(self) -> Dict[str, int]:
#         """
#         Counts suppression types TODAY.
#         """
#         start, end = self._today_bounds()
#         events = self.storage.get_suppression_events(start, end)
#         return dict(Counter(t for ts, t, is_reset in events))

#     # -------------------------------------------------
#     # SUPPRESSION
#     # -------------------------------------------------
#     def suppression_counts(self) -> Dict[str, int]:
#         start, end = self._today_bounds()
#         events = self.storage.get_suppression_events(start, end)
#         return dict(Counter(t for ts, t, is_reset in events))

#     def away_resets_count(self) -> int:
#         start, end = self._today_bounds()
#         events = self.storage.get_suppression_events(start, end)
#         return sum(1 for ts, t, is_reset in events if is_reset)

#     # -------------------------------------------------
#     # TIME OF DAY (HEATMAPS)
#     # -------------------------------------------------
#     def behavior_heatmap(self) -> Dict[int, float]:
#         """
#         Last 7 days: minutes per hour.
#         """
#         start, end = self._last_7_days_bounds()
#         events = self.storage.get_behavior_events(start, end)

#         hourly = Counter()

#         for ts, behavior, duration, fatigue, mode in events:
#             cat = self._categorize_behavior(behavior)
#             if not cat:
#                 continue
#             dt = datetime.fromisoformat(ts)
#             hourly[dt.hour] += duration or 1

#         return dict(hourly)

#     def fatigue_heatmap(self) -> Dict[int, float]:
#         start, end = self._last_7_days_bounds()
#         events = self.storage.get_fatigue_events(start, end)

#         hourly = defaultdict(list)

#         for ts, f in events:
#             dt = datetime.fromisoformat(ts)
#             hourly[dt.hour].append(f)

#         return {h: sum(v) / len(v) for h, v in hourly.items()}

#     def break_heatmap(self) -> Dict[int, float]:
#         start, end = self._last_7_days_bounds()
#         events = self.storage.get_break_events(start, end)

#         hourly = Counter()

#         for ts, r, b, f, i, tq in events:
#             dt = datetime.fromisoformat(ts)
#             hourly[dt.hour] += 1

#         return dict(hourly)

#     def suppression_heatmap(self) -> Dict[int, float]:
#         start, end = self._last_7_days_bounds()
#         events = self.storage.get_suppression_events(start, end)

#         hourly = Counter()

#         for ts, t, is_reset in events:
#             dt = datetime.fromisoformat(ts)
#             hourly[dt.hour] += 1

#         return dict(hourly)

#     # -------------------------------------------------
#     # WEEKLY / MONTHLY
#     # -------------------------------------------------
#     def weekly_behavior_summary(self) -> Optional[Dict[str, Any]]:
#         return self.weekly_engine.generate_this_week()

#     def monthly_behavior_summary(self) -> Optional[Dict[str, Any]]:
#         return self.monthly_engine.generate_this_month()

#     # -------------------------------------------------
#     # AI INSIGHTS
#     # -------------------------------------------------
#     def ai_insights(self) -> List[str]:
#         insights = []

#         weekly = self.weekly_behavior_summary()
#         monthly = self.monthly_behavior_summary()

#         # Weekly insights
#         if weekly:
#             if weekly.get("deep_work", 0) > 0:
#                 insights.append(
#                     f"You spent {weekly['deep_work']} minutes in deep work this week — strong focused effort."
#                 )
#             if weekly.get("avg_fatigue", 0) > 60:
#                 insights.append(
#                     "Fatigue was elevated this week. Consider lighter sessions or more frequent short breaks."
#                 )

#         # Monthly insights
#         if monthly:
#             if monthly.get("total_focus", 0) > 0:
#                 insights.append(
#                     f"This month you accumulated {monthly['total_focus']} focused minutes — steady engagement."
#                 )
#             if monthly.get("breaks", 0) < 20:
#                 insights.append(
#                     "Breaks were relatively rare this month. Adding short pauses may support better recovery."
#                 )

#         # If nothing else
#         if not insights:
#             insights.append(
#                 "Analytics are warming up. As you use the app more, richer insights will appear."
#             )

#         return insights

#     # -------------------------------------------------
#     # EXPORT
#     # -------------------------------------------------
#     def export_all_data(self) -> Dict[str, Dict[str, Any]]:
#         weekly = self.weekly_behavior_summary() or {}
#         monthly = self.monthly_behavior_summary() or {}

#         return {
#             "Behavior Distribution": self.behavior_distribution(),
#             "Behavior Timeline": self.behavior_timeline(),
#             "Fatigue Trend": self.fatigue_trend(),
#             "Fatigue by Behavior": self.fatigue_by_behavior(),
#             "Break Reasons": self.break_reasons(),
#             "Break Timing": self.break_timing_quality(),
#             "Break Suppression": self.break_suppression_stats(),
#             "Suppression Counts": self.suppression_counts(),
#             "Weekly Summary": weekly,
#             "Monthly Summary": monthly,
#             "AI Insights": {"insights": self.ai_insights()},
#         }





















# # core/analytics_engine.py

# from datetime import datetime, timedelta
# from typing import Dict, List, Any, Optional
# from collections import defaultdict, Counter

# from core.storage_manager import StorageManager
# from core.weekly_summary_engine import WeeklySummaryEngine
# from core.monthly_summary_engine import MonthlySummaryEngine


# class AnalyticsEngine:
#     """
#     Premium, behavior-aware analytics engine.

#     Hybrid model:
#     - Today → raw logs (behavior, fatigue, breaks, suppression)
#     - Last 7 days → heatmaps
#     - Weekly / Monthly → summary engines
#     - AI Insights → weekly + monthly + last 7 days logs
#     """

#     def __init__(self):
#         self.storage = StorageManager()
#         self.weekly_engine = WeeklySummaryEngine()
#         self.monthly_engine = MonthlySummaryEngine()

#         # Premium behavior category mapping
#         self.behavior_map = {
#             # Deep Work
#             "deep_work": "Deep Work",
#             "Deep Work": "Deep Work",
#             "coding": "Deep Work",
#             "writing": "Deep Work",
#             "multitasking": "Deep Work",

#             # Deep Reading
#             "reading": "Deep Reading",
#             "deep_reading": "Deep Reading",

#             # Focused Interaction
#             "meeting": "Focused Interaction",
#             "focused_interaction": "Focused Interaction",
#             "Focused Interaction": "Focused Interaction",
#             "heavy_browsing": "Focused Interaction",

#             # General Activity
#             "General Activity": "General Activity",
#             "Browsing": "General Activity",
#             "Activity": "General Activity",

#             # Idle
#             "Idle": "Idle",
#         }


#     # -------------------------------------------------
#     # INTERNAL HELPERS
#     # -------------------------------------------------
#     def _today_bounds(self):
#         today = datetime.now().date()
#         start = datetime.combine(today, datetime.min.time())
#         end = start + timedelta(days=1)
#         return start, end

#     def _last_7_days_bounds(self):
#         end = datetime.now()
#         start = end - timedelta(days=7)
#         return start, end

#     def _categorize_behavior(self, raw: str) -> Optional[str]:
#         return self.behavior_map.get(raw, None)

#     # -------------------------------------------------
#     # BEHAVIOR
#     # -------------------------------------------------
#     def behavior_distribution(self) -> Dict[str, float]:
#         """
#         Total minutes per behavior category for TODAY.
#         """
#         start, end = self._today_bounds()
#         events = self.storage.get_behavior_events(start, end)

#         totals = Counter()

#         # behavior_events: (timestamp, behavior, duration, fatigue_at_event, mode)
#         for ts, behavior, duration, fatigue, mode in events:
#             cat = self._categorize_behavior(behavior)
#             if not cat:
#                 continue

#             if duration:
#                 totals[cat] += duration
#             else:
#                 totals[cat] += 1  # assume 1-minute minimum

#         return dict(totals)

#     def behavior_timeline(self) -> Dict[str, List[Any]]:
#         """
#         Returns a stepped timeline for TODAY.
#         """
#         start, end = self._today_bounds()
#         events = self.storage.get_behavior_events(start, end)

#         times = []
#         behaviors = []

#         for ts, behavior, duration, fatigue, mode in events:
#             cat = self._categorize_behavior(behavior)
#             if not cat:
#                 continue
#             times.append(ts)
#             behaviors.append(cat)

#         return {"times": times, "behaviors": behaviors}

#     def behavior_by_hour(self) -> Dict[int, Dict[str, float]]:
#         """
#         Returns behavior minutes grouped by hour for TODAY.
#         """
#         start, end = self._today_bounds()
#         events = self.storage.get_behavior_events(start, end)

#         hourly = defaultdict(lambda: Counter())

#         for ts, behavior, duration, fatigue, mode in events:
#             cat = self._categorize_behavior(behavior)
#             if not cat:
#                 continue

#             dt = datetime.fromisoformat(ts)
#             hour = dt.hour

#             if duration:
#                 hourly[hour][cat] += duration
#             else:
#                 hourly[hour][cat] += 1

#         return {h: dict(c) for h, c in hourly.items()}

#     def longest_behavior_streak(self) -> Optional[Dict[str, Any]]:
#         """
#         Longest contiguous streak of the same behavior TODAY.
#         """
#         start, end = self._today_bounds()
#         events = self.storage.get_behavior_events(start, end)

#         last_cat = None
#         current_len = 0
#         best_cat = None
#         best_len = 0

#         for ts, behavior, duration, fatigue, mode in events:
#             cat = self._categorize_behavior(behavior)
#             if not cat:
#                 continue

#             if cat == last_cat:
#                 current_len += duration or 1
#             else:
#                 current_len = duration or 1
#                 last_cat = cat

#             if current_len > best_len:
#                 best_len = current_len
#                 best_cat = cat

#         if not best_cat:
#             return None

#         return {"behavior": best_cat, "minutes": best_len}
#     # -------------------------------------------------
#     # FATIGUE
#     # -------------------------------------------------
#     # def fatigue_trend(self) -> Dict[str, List[Any]]:
#     #     """
#     #     Fatigue values for TODAY (minute-based).
#     #     """
#     #     start, end = self._today_bounds()
#     #     events = self.storage.get_fatigue_events(start, end)
#     #     # fatigue_events: (timestamp, fatigue, mode)

#     #     times = [ts for ts, f, mode in events]
#     #     values = [f for ts, f, mode in events]

#     #     return {"times": times, "fatigue": values}

#     def fatigue_trend(self) -> Dict[str, List[Any]]:
#         """
#         Fatigue values for TODAY, aggregated by minute.
#         Prevents thousands of raw logs from collapsing the graph.
#         """
#         start, end = self._today_bounds()
#         events = self.storage.get_fatigue_events(start, end)

#         if not events:
#             return {"times": [], "fatigue": []}

#         # Convert to datetime objects
#         points = [(datetime.fromisoformat(ts), f) for ts, f, mode in events]

#         # Group by minute
#         buckets = {}
#         for t, f in points:
#             minute = t.replace(second=0, microsecond=0)
#             buckets.setdefault(minute, []).append(f)

#         # Sort by time
#         times = sorted(buckets.keys())
#         values = [sum(v) / len(v) for v in (buckets[t] for t in times)]

#         return {
#             "times": [t.isoformat() for t in times],
#             "fatigue": values
#         }


#     def fatigue_by_behavior(self) -> Dict[str, float]:
#         """
#         Average fatigue per behavior category TODAY.
#         """
#         start, end = self._today_bounds()
#         beh = self.storage.get_behavior_events(start, end)

#         totals = Counter()
#         counts = Counter()

#         for ts, behavior, duration, fatigue, mode in beh:
#             cat = self._categorize_behavior(behavior)
#             if not cat:
#                 continue
#             if fatigue is None:
#                 continue

#             totals[cat] += fatigue
#             counts[cat] += 1

#         return {cat: totals[cat] / counts[cat] for cat in totals}

#     def fatigue_recovery_after_breaks(self) -> Dict[str, List[Any]]:
#         """
#         Fatigue values around break timestamps TODAY.
#         """
#         start, end = self._today_bounds()
#         breaks = self.storage.get_break_events(start, end)
#         fatigue = self.storage.get_fatigue_events(start, end)

#         if not breaks or not fatigue:
#             return {"times": [], "fatigue": []}

#         times = []
#         values = []

#         # fatigue_events: (timestamp, fatigue, mode)
#         fatigue_points = [(datetime.fromisoformat(ts), f) for ts, f, mode in fatigue]

#         # break_events: (timestamp, reason, behavior, fatigue, interval_used, timing_quality, mode)
#         for ts, reason, behavior, f, interval_used, tq, mode in breaks:
#             bt = datetime.fromisoformat(ts)
#             window_end = bt + timedelta(minutes=10)

#             window_vals = [fv for t, fv in fatigue_points if bt <= t <= window_end]
#             if window_vals:
#                 times.append(ts)
#                 values.append(sum(window_vals) / len(window_vals))

#         return {"times": times, "fatigue": values}

#     def highest_fatigue_moment(self) -> Optional[Dict[str, Any]]:
#         """
#         Highest fatigue value TODAY.
#         """
#         start, end = self._today_bounds()
#         events = self.storage.get_fatigue_events(start, end)

#         if not events:
#             return None

#         # events: (timestamp, fatigue, mode)
#         ts, f, mode = max(events, key=lambda x: x[1])
#         return {"time": ts, "fatigue": f}

#     # -------------------------------------------------
#     # BREAKS
#     # -------------------------------------------------
#     def break_reasons(self) -> Dict[str, int]:
#         start, end = self._today_bounds()
#         events = self.storage.get_break_events(start, end)
#         # (timestamp, reason, behavior, fatigue, interval_used, timing_quality, mode)
#         return dict(Counter(reason for ts, reason, b, f, i, tq, mode in events))

#     def break_timing_quality(self) -> Dict[str, int]:
#         start, end = self._today_bounds()
#         events = self.storage.get_break_events(start, end)
#         return dict(Counter(tq for ts, r, b, f, i, tq, mode in events))

#     def break_events_timeline(self) -> Dict[str, List[Any]]:
#         start, end = self._today_bounds()
#         events = self.storage.get_break_events(start, end)
#         times = [ts for ts, r, b, f, i, tq, mode in events]
#         return {"times": times}

#     def break_suppression_stats(self) -> Dict[str, int]:
#         """
#         Counts suppression types TODAY.
#         """
#         start, end = self._today_bounds()
#         events = self.storage.get_suppression_events(start, end)
#         # suppression_log: (timestamp, type, is_away_reset, mode)
#         return dict(Counter(t for ts, t, is_reset, mode in events))

#     # -------------------------------------------------
#     # SUPPRESSION
#     # -------------------------------------------------
#     def suppression_counts(self) -> Dict[str, int]:
#         start, end = self._today_bounds()
#         events = self.storage.get_suppression_events(start, end)
#         return dict(Counter(t for ts, t, is_reset, mode in events))

#     def away_resets_count(self) -> int:
#         start, end = self._today_bounds()
#         events = self.storage.get_suppression_events(start, end)
#         return sum(1 for ts, t, is_reset, mode in events if is_reset)
#     # -------------------------------------------------
#     # TIME OF DAY (HEATMAPS)
#     # -------------------------------------------------
#     def behavior_heatmap(self) -> Dict[int, float]:
#         """
#         Last 7 days: minutes per hour.
#         """
#         start, end = self._last_7_days_bounds()
#         events = self.storage.get_behavior_events(start, end)

#         hourly = Counter()

#         for ts, behavior, duration, fatigue, mode in events:
#             cat = self._categorize_behavior(behavior)
#             if not cat:
#                 continue
#             dt = datetime.fromisoformat(ts)
#             hourly[dt.hour] += duration or 1

#         return dict(hourly)

#     def fatigue_heatmap(self) -> Dict[int, float]:
#         start, end = self._last_7_days_bounds()
#         events = self.storage.get_fatigue_events(start, end)

#         hourly = defaultdict(list)

#         # (timestamp, fatigue, mode)
#         for ts, f, mode in events:
#             dt = datetime.fromisoformat(ts)
#             hourly[dt.hour].append(f)

#         return {h: sum(v) / len(v) for h, v in hourly.items()}

#     def break_heatmap(self) -> Dict[int, float]:
#         start, end = self._last_7_days_bounds()
#         events = self.storage.get_break_events(start, end)

#         hourly = Counter()

#         # (timestamp, reason, behavior, fatigue, interval_used, timing_quality, mode)
#         for ts, r, b, f, i, tq, mode in events:
#             dt = datetime.fromisoformat(ts)
#             hourly[dt.hour] += 1

#         return dict(hourly)

#     def suppression_heatmap(self) -> Dict[int, float]:
#         start, end = self._last_7_days_bounds()
#         events = self.storage.get_suppression_events(start, end)

#         hourly = Counter()

#         # (timestamp, type, is_away_reset, mode)
#         for ts, t, is_reset, mode in events:
#             dt = datetime.fromisoformat(ts)
#             hourly[dt.hour] += 1

#         return dict(hourly)

#     # -------------------------------------------------
#     # WEEKLY / MONTHLY
#     # -------------------------------------------------
#     def weekly_behavior_summary(self) -> Optional[Dict[str, Any]]:
#         return self.weekly_engine.generate_this_week()

#     def monthly_behavior_summary(self) -> Optional[Dict[str, Any]]:
#         return self.monthly_engine.generate_this_month()

#     # -------------------------------------------------
#     # AI INSIGHTS
#     # -------------------------------------------------
#     def ai_insights(self) -> List[str]:
#         insights = []

#         weekly = self.weekly_behavior_summary()
#         monthly = self.monthly_behavior_summary()

#         # Weekly insights
#         if weekly:
#             if weekly.get("deep_work", 0) > 0:
#                 insights.append(
#                     f"You spent {weekly['deep_work']} minutes in deep work this week — strong focused effort."
#                 )
#             if weekly.get("avg_fatigue", 0) > 60:
#                 insights.append(
#                     "Fatigue was elevated this week. Consider lighter sessions or more frequent short breaks."
#                 )

#         # Monthly insights
#         if monthly:
#             if monthly.get("total_focus", 0) > 0:
#                 insights.append(
#                     f"This month you accumulated {monthly['total_focus']} focused minutes — steady engagement."
#                 )
#             if monthly.get("breaks", 0) < 20:
#                 insights.append(
#                     "Breaks were relatively rare this month. Adding short pauses may support better recovery."
#                 )

#         if not insights:
#             insights.append(
#                 "Analytics are warming up. As you use the app more, richer insights will appear."
#             )

#         return insights

#     # -------------------------------------------------
#     # EXPORT
#     # -------------------------------------------------
#     def export_all_data(self) -> Dict[str, Dict[str, Any]]:
#         weekly = self.weekly_behavior_summary() or {}
#         monthly = self.monthly_behavior_summary() or {}

#         return {
#             "Behavior Distribution": self.behavior_distribution(),
#             "Behavior Timeline": self.behavior_timeline(),
#             "Fatigue Trend": self.fatigue_trend(),
#             "Fatigue by Behavior": self.fatigue_by_behavior(),
#             "Break Reasons": self.break_reasons(),
#             "Break Timing": self.break_timing_quality(),
#             "Break Suppression": self.break_suppression_stats(),
#             "Suppression Counts": self.suppression_counts(),
#             "Weekly Summary": weekly,
#             "Monthly Summary": monthly,
#             "AI Insights": {"insights": self.ai_insights()},
#         }























# core/analytics_engine.py

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter

from core.storage_manager import StorageManager
from core.weekly_summary_engine import WeeklySummaryEngine
from core.monthly_summary_engine import MonthlySummaryEngine


class AnalyticsEngine:
    """
    Premium, behavior-aware analytics engine.

    Hybrid model:
    - Today → raw logs (behavior, fatigue, breaks, suppression)
    - Last 7 days → heatmaps
    - Weekly / Monthly → summary engines
    - AI Insights → weekly + monthly + last 7 days logs
    """

    def __init__(self):
        self.storage = StorageManager()
        self.weekly_engine = WeeklySummaryEngine()
        self.monthly_engine = MonthlySummaryEngine()

        # Premium behavior category mapping
        self.behavior_map = {
            # Deep Work
            "deep_work": "Deep Work",
            "Deep Work": "Deep Work",
            "coding": "Deep Work",
            "writing": "Deep Work",
            "multitasking": "Deep Work",

            # Deep Reading
            "reading": "Deep Reading",
            "deep_reading": "Deep Reading",

            # Focused Interaction
            "meeting": "Focused Interaction",
            "focused_interaction": "Focused Interaction",
            "Focused Interaction": "Focused Interaction",
            "heavy_browsing": "Focused Interaction",

            # General Activity
            "General Activity": "General Activity",
            "Browsing": "General Activity",
            "Activity": "General Activity",

            # Idle
            "Idle": "Idle",
        }


    # -------------------------------------------------
    # INTERNAL HELPERS
    # -------------------------------------------------
    def _today_bounds(self):
        today = datetime.now().date()
        start = datetime.combine(today, datetime.min.time())
        end = start + timedelta(days=1)
        return start, end

    def _last_7_days_bounds(self):
        end = datetime.now()
        start = end - timedelta(days=7)
        return start, end

    def _categorize_behavior(self, raw: str) -> Optional[str]:
        return self.behavior_map.get(raw, None)

    # -------------------------------------------------
    # BEHAVIOR
    # -------------------------------------------------
    def behavior_distribution(self) -> Dict[str, float]:
        """
        Total minutes per behavior category for TODAY.
        """
        start, end = self._today_bounds()
        events = self.storage.get_behavior_events(start, end)

        totals = Counter()

        # behavior_events: (timestamp, behavior, duration, fatigue_at_event, mode)
        for ts, behavior, duration, fatigue, mode in events:
            cat = self._categorize_behavior(behavior)
            if not cat:
                continue

            if duration:
                totals[cat] += duration
            else:
                totals[cat] += 1  # assume 1-minute minimum

        return dict(totals)

    def behavior_timeline(self) -> Dict[str, List[Any]]:
        """
        Returns a 5-minute smoothed behavior timeline for TODAY.
        Each 5-minute window is assigned the dominant behavior.
        """
        start, end = self._today_bounds()
        events = self.storage.get_behavior_events(start, end)

        if not events:
            return {"times": [], "behaviors": []}

        # Convert to (minute, category)
        points = []
        for ts, behavior, duration, fatigue, mode in events:
            cat = self._categorize_behavior(behavior)
            if not cat:
                continue
            dt = datetime.fromisoformat(ts)
            minute = dt.replace(second=0, microsecond=0)
            points.append((minute, cat))

        # Group into 5-minute buckets
        buckets = {}
        for minute, cat in points:
            floored = minute.replace(minute=(minute.minute // 5) * 5)
            buckets.setdefault(floored, []).append(cat)

        # Pick dominant behavior per bucket
        smoothed_times = sorted(buckets.keys())
        smoothed_behaviors = []
        for t in smoothed_times:
            window_behaviors = buckets[t]
            dominant = max(set(window_behaviors), key=window_behaviors.count)
            smoothed_behaviors.append(dominant)

        return {
            "times": [t.isoformat() for t in smoothed_times],
            "behaviors": smoothed_behaviors
        }

    def behavior_by_hour(self) -> Dict[int, Dict[str, float]]:
        """
        Returns behavior minutes grouped by hour for TODAY.
        """
        start, end = self._today_bounds()
        events = self.storage.get_behavior_events(start, end)

        hourly = defaultdict(lambda: Counter())

        for ts, behavior, duration, fatigue, mode in events:
            cat = self._categorize_behavior(behavior)
            if not cat:
                continue

            dt = datetime.fromisoformat(ts)
            hour = dt.hour

            if duration:
                hourly[hour][cat] += duration
            else:
                hourly[hour][cat] += 1

        return {h: dict(c) for h, c in hourly.items()}

    def longest_behavior_streak(self) -> Optional[Dict[str, Any]]:
        """
        Longest contiguous streak of the same behavior TODAY.
        """
        start, end = self._today_bounds()
        events = self.storage.get_behavior_events(start, end)

        last_cat = None
        current_len = 0
        best_cat = None
        best_len = 0

        for ts, behavior, duration, fatigue, mode in events:
            cat = self._categorize_behavior(behavior)
            if not cat:
                continue

            if cat == last_cat:
                current_len += duration or 1
            else:
                current_len = duration or 1
                last_cat = cat

            if current_len > best_len:
                best_len = current_len
                best_cat = cat

        if not best_cat:
            return None

        return {"behavior": best_cat, "minutes": best_len}
    # -------------------------------------------------
    # FATIGUE
    # -------------------------------------------------
    # def fatigue_trend(self) -> Dict[str, List[Any]]:
    #     """
    #     Fatigue values for TODAY (minute-based).
    #     """
    #     start, end = self._today_bounds()
    #     events = self.storage.get_fatigue_events(start, end)
    #     # fatigue_events: (timestamp, fatigue, mode)

    #     times = [ts for ts, f, mode in events]
    #     values = [f for ts, f, mode in events]

    #     return {"times": times, "fatigue": values}

    def fatigue_trend(self) -> Dict[str, List[Any]]:
        """
        Fatigue values for TODAY, aggregated into 5-minute windows.
        Prevents thousands of raw logs from collapsing the graph.
        """
        start, end = self._today_bounds()
        events = self.storage.get_fatigue_events(start, end)

        if not events:
            return {"times": [], "fatigue": []}

        # Convert to datetime + fatigue
        points = [(datetime.fromisoformat(ts), f) for ts, f, mode in events]

        # Group into 5-minute buckets
        buckets = {}
        for t, f in points:
            floored = t.replace(minute=(t.minute // 5) * 5, second=0, microsecond=0)
            buckets.setdefault(floored, []).append(f)

        # Sort buckets
        times = sorted(buckets.keys())
        values = [sum(v) / len(v) for v in (buckets[t] for t in times)]

        return {
            "times": [t.isoformat() for t in times],
            "fatigue": values
        }


    def fatigue_by_behavior(self) -> Dict[str, float]:
        """
        Average fatigue per behavior category TODAY.
        """
        start, end = self._today_bounds()
        beh = self.storage.get_behavior_events(start, end)

        totals = Counter()
        counts = Counter()

        for ts, behavior, duration, fatigue, mode in beh:
            cat = self._categorize_behavior(behavior)
            if not cat:
                continue
            if fatigue is None:
                continue

            totals[cat] += fatigue
            counts[cat] += 1

        return {cat: totals[cat] / counts[cat] for cat in totals}

    def fatigue_recovery_after_breaks(self) -> Dict[str, List[Any]]:
        """
        Fatigue values around break timestamps TODAY.
        """
        start, end = self._today_bounds()
        breaks = self.storage.get_break_events(start, end)
        fatigue = self.storage.get_fatigue_events(start, end)

        if not breaks or not fatigue:
            return {"times": [], "fatigue": []}

        times = []
        values = []

        # fatigue_events: (timestamp, fatigue, mode)
        fatigue_points = [(datetime.fromisoformat(ts), f) for ts, f, mode in fatigue]

        # break_events: (timestamp, reason, behavior, fatigue, interval_used, timing_quality, mode)
        for ts, reason, behavior, f, interval_used, tq, mode in breaks:
            bt = datetime.fromisoformat(ts)
            window_end = bt + timedelta(minutes=10)

            window_vals = [fv for t, fv in fatigue_points if bt <= t <= window_end]
            if window_vals:
                times.append(ts)
                values.append(sum(window_vals) / len(window_vals))

        return {"times": times, "fatigue": values}

    def highest_fatigue_moment(self) -> Optional[Dict[str, Any]]:
        """
        Highest fatigue value TODAY.
        """
        start, end = self._today_bounds()
        events = self.storage.get_fatigue_events(start, end)

        if not events:
            return None

        # events: (timestamp, fatigue, mode)
        ts, f, mode = max(events, key=lambda x: x[1])
        return {"time": ts, "fatigue": f}

    # -------------------------------------------------
    # BREAKS
    # -------------------------------------------------
    def break_reasons(self) -> Dict[str, int]:
        start, end = self._today_bounds()
        events = self.storage.get_break_events(start, end)
        # (timestamp, reason, behavior, fatigue, interval_used, timing_quality, mode)
        return dict(Counter(reason for ts, reason, b, f, i, tq, mode in events))

    def break_timing_quality(self) -> Dict[str, int]:
        start, end = self._today_bounds()
        events = self.storage.get_break_events(start, end)
        return dict(Counter(tq for ts, r, b, f, i, tq, mode in events))

    def break_events_timeline(self) -> Dict[str, List[Any]]:
        start, end = self._today_bounds()
        events = self.storage.get_break_events(start, end)
        times = [ts for ts, r, b, f, i, tq, mode in events]
        return {"times": times}

    def break_suppression_stats(self) -> Dict[str, int]:
        """
        Counts suppression types TODAY.
        """
        start, end = self._today_bounds()
        events = self.storage.get_suppression_events(start, end)
        # suppression_log: (timestamp, type, is_away_reset, mode)
        return dict(Counter(t for ts, t, is_reset, mode in events))

    # -------------------------------------------------
    # SUPPRESSION
    # -------------------------------------------------
    def suppression_counts(self) -> Dict[str, int]:
        start, end = self._today_bounds()
        events = self.storage.get_suppression_events(start, end)
        return dict(Counter(t for ts, t, is_reset, mode in events))

    def away_resets_count(self) -> int:
        start, end = self._today_bounds()
        events = self.storage.get_suppression_events(start, end)
        return sum(1 for ts, t, is_reset, mode in events if is_reset)
    # -------------------------------------------------
    # TIME OF DAY (HEATMAPS)
    # -------------------------------------------------
    def behavior_heatmap(self) -> Dict[int, float]:
        """
        Last 7 days: minutes per hour.
        """
        start, end = self._last_7_days_bounds()
        events = self.storage.get_behavior_events(start, end)

        hourly = Counter()

        for ts, behavior, duration, fatigue, mode in events:
            cat = self._categorize_behavior(behavior)
            if not cat:
                continue
            dt = datetime.fromisoformat(ts)
            hourly[dt.hour] += duration or 1

        return dict(hourly)

    def fatigue_heatmap(self) -> Dict[int, float]:
        start, end = self._last_7_days_bounds()
        events = self.storage.get_fatigue_events(start, end)

        hourly = defaultdict(list)

        # (timestamp, fatigue, mode)
        for ts, f, mode in events:
            dt = datetime.fromisoformat(ts)
            hourly[dt.hour].append(f)

        return {h: sum(v) / len(v) for h, v in hourly.items()}

    def break_heatmap(self) -> Dict[int, float]:
        start, end = self._last_7_days_bounds()
        events = self.storage.get_break_events(start, end)

        hourly = Counter()

        # (timestamp, reason, behavior, fatigue, interval_used, timing_quality, mode)
        for ts, r, b, f, i, tq, mode in events:
            dt = datetime.fromisoformat(ts)
            hourly[dt.hour] += 1

        return dict(hourly)

    def suppression_heatmap(self) -> Dict[int, float]:
        start, end = self._last_7_days_bounds()
        events = self.storage.get_suppression_events(start, end)

        hourly = Counter()

        # (timestamp, type, is_away_reset, mode)
        for ts, t, is_reset, mode in events:
            dt = datetime.fromisoformat(ts)
            hourly[dt.hour] += 1

        return dict(hourly)

    # -------------------------------------------------
    # WEEKLY / MONTHLY
    # -------------------------------------------------
    def weekly_behavior_summary(self) -> Optional[Dict[str, Any]]:
        return self.weekly_engine.generate_this_week()

    def monthly_behavior_summary(self) -> Optional[Dict[str, Any]]:
        return self.monthly_engine.generate_this_month()

    # -------------------------------------------------
    # AI INSIGHTS
    # -------------------------------------------------
    def ai_insights(self) -> List[str]:
        insights = []

        weekly = self.weekly_behavior_summary()
        monthly = self.monthly_behavior_summary()

        # Weekly insights
        if weekly:
            if weekly.get("deep_work", 0) > 0:
                insights.append(
                    f"You spent {weekly['deep_work']} minutes in deep work this week — strong focused effort."
                )
            if weekly.get("avg_fatigue", 0) > 60:
                insights.append(
                    "Fatigue was elevated this week. Consider lighter sessions or more frequent short breaks."
                )

        # Monthly insights
        if monthly:
            if monthly.get("total_focus", 0) > 0:
                insights.append(
                    f"This month you accumulated {monthly['total_focus']} focused minutes — steady engagement."
                )
            if monthly.get("breaks", 0) < 20:
                insights.append(
                    "Breaks were relatively rare this month. Adding short pauses may support better recovery."
                )

        if not insights:
            insights.append(
                "Analytics are warming up. As you use the app more, richer insights will appear."
            )

        return insights

    # -------------------------------------------------
    # EXPORT
    # -------------------------------------------------
    def export_all_data(self) -> Dict[str, Dict[str, Any]]:
        weekly = self.weekly_behavior_summary() or {}
        monthly = self.monthly_behavior_summary() or {}

        return {
            "Behavior Distribution": self.behavior_distribution(),
            "Behavior Timeline": self.behavior_timeline(),
            "Fatigue Trend": self.fatigue_trend(),
            "Fatigue by Behavior": self.fatigue_by_behavior(),
            "Break Reasons": self.break_reasons(),
            "Break Timing": self.break_timing_quality(),
            "Break Suppression": self.break_suppression_stats(),
            "Suppression Counts": self.suppression_counts(),
            "Weekly Summary": weekly,
            "Monthly Summary": monthly,
            "AI Insights": {"insights": self.ai_insights()},
        }
