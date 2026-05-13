# core/weekly_summary_engine.py

from datetime import datetime, timedelta
from core.storage_manager import StorageManager


class WeeklySummaryEngine:
    """
    Aggregates 7 daily summaries (Monday → Sunday)
    into a premium weekly summary with insights.
    """

    def __init__(self):
        self.storage = StorageManager()

    # ---------------------------------------------------------
    # GET WEEK RANGE (Monday → Sunday)
    # ---------------------------------------------------------
    def _get_week_range(self, any_date: datetime):
        weekday = any_date.weekday()  # Monday = 0, Sunday = 6
        monday = any_date - timedelta(days=weekday)
        sunday = monday + timedelta(days=6)
        return monday, sunday

    # ---------------------------------------------------------
    # LOAD DAILY SUMMARIES FOR THE WEEK
    # ---------------------------------------------------------
    def _load_daily_summaries(self, monday: datetime, sunday: datetime):
        summaries = []
        current = monday

        while current <= sunday:
            date_str = current.strftime("%Y-%m-%d")
            row = self.storage.get_daily_summary(date_str)
            if row:
                # row = (date, total_focus, deep_work, deep_reading, focused_interaction, breaks, avg_fatigue)
                summaries.append({
                    "date": row[0],
                    "total_focus": row[1],
                    "deep_work": row[2],
                    "deep_reading": row[3],
                    "focused_interaction": row[4],
                    "breaks": row[5],
                    "avg_fatigue": row[6],
                })
            current += timedelta(days=1)

        return summaries

    # ---------------------------------------------------------
    # PUBLIC: Generate weekly summary for the week of a date
    # ---------------------------------------------------------
    def generate_for_date(self, date_str: str):
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        monday, sunday = self._get_week_range(target_date)

        daily_summaries = self._load_daily_summaries(monday, sunday)

        if not daily_summaries:
            return {
                "week_start": monday.strftime("%Y-%m-%d"),
                "week_end": sunday.strftime("%Y-%m-%d"),
                "total_focus": 0,
                "deep_work": 0,
                "deep_reading": 0,
                "focused_interaction": 0,
                "breaks": 0,
                "avg_fatigue": 0.0,
                "insights": ["No data recorded this week."]
            }

        # -----------------------------------------------------
        # AGGREGATE WEEKLY TOTALS
        # -----------------------------------------------------
        total_focus = sum(d["total_focus"] for d in daily_summaries)
        deep_work = sum(d["deep_work"] for d in daily_summaries)
        deep_reading = sum(d["deep_reading"] for d in daily_summaries)
        focused_interaction = sum(d["focused_interaction"] for d in daily_summaries)
        breaks = sum(d["breaks"] for d in daily_summaries)

        fatigue_values = [d["avg_fatigue"] for d in daily_summaries if d["avg_fatigue"] > 0]
        avg_fatigue = sum(fatigue_values) / len(fatigue_values) if fatigue_values else 0.0

        # -----------------------------------------------------
        # PREMIUM WEEKLY INSIGHTS
        # -----------------------------------------------------
        insights = []

        if deep_work > 120:
            insights.append("Strong deep work week — excellent sustained focus.")

        if deep_reading > 90:
            insights.append("High-quality reading time — great for cognitive recovery.")

        if avg_fatigue > 60:
            insights.append("Fatigue was elevated this week. Consider lighter sessions.")

        if breaks < 10:
            insights.append("Very few breaks — try adding short pauses to stay balanced.")

        if not insights:
            insights.append("A steady, balanced week overall.")

        return {
            "week_start": monday.strftime("%Y-%m-%d"),
            "week_end": sunday.strftime("%Y-%m-%d"),
            "total_focus": total_focus,
            "deep_work": deep_work,
            "deep_reading": deep_reading,
            "focused_interaction": focused_interaction,
            "breaks": breaks,
            "avg_fatigue": avg_fatigue,
            "insights": insights
        }

    # ---------------------------------------------------------
    # PUBLIC: Generate summary for the current week
    # ---------------------------------------------------------
    def generate_this_week(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return self.generate_for_date(today)

    # ---------------------------------------------------------
    # PUBLIC: Generate summary for last week
    # ---------------------------------------------------------
    def generate_last_week(self):
        last_week_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        return self.generate_for_date(last_week_date)
