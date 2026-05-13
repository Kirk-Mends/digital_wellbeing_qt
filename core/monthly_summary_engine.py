# core/monthly_summary_engine.py

from datetime import datetime, timedelta
from core.storage_manager import StorageManager


class MonthlySummaryEngine:
    """
    Aggregates daily summaries into a premium monthly summary.
    Uses calendar months (1st → last day), matching global standards.
    """

    def __init__(self):
        self.storage = StorageManager()

    # ---------------------------------------------------------
    # GET MONTH RANGE (1st → last day)
    # ---------------------------------------------------------
    def _get_month_range(self, any_date: datetime):
        first = any_date.replace(day=1)
        if any_date.month == 12:
            next_month = any_date.replace(year=any_date.year + 1, month=1, day=1)
        else:
            next_month = any_date.replace(month=any_date.month + 1, day=1)
        last = next_month - timedelta(days=1)
        return first, last

    # ---------------------------------------------------------
    # LOAD DAILY SUMMARIES FOR THE MONTH
    # ---------------------------------------------------------
    def _load_daily_summaries(self, first: datetime, last: datetime):
        summaries = []
        current = first

        while current <= last:
            date_str = current.strftime("%Y-%m-%d")
            row = self.storage.get_daily_summary(date_str)
            if row:
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
    # PUBLIC: Generate monthly summary for a given date
    # ---------------------------------------------------------
    def generate_for_date(self, date_str: str):
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        first, last = self._get_month_range(target_date)

        daily_summaries = self._load_daily_summaries(first, last)

        if not daily_summaries:
            return {
                "month_start": first.strftime("%Y-%m-%d"),
                "month_end": last.strftime("%Y-%m-%d"),
                "total_focus": 0,
                "deep_work": 0,
                "deep_reading": 0,
                "focused_interaction": 0,
                "breaks": 0,
                "avg_fatigue": 0.0,
                "insights": ["No data recorded this month."]
            }

        # -----------------------------------------------------
        # AGGREGATE MONTHLY TOTALS
        # -----------------------------------------------------
        total_focus = sum(d["total_focus"] for d in daily_summaries)
        deep_work = sum(d["deep_work"] for d in daily_summaries)
        deep_reading = sum(d["deep_reading"] for d in daily_summaries)
        focused_interaction = sum(d["focused_interaction"] for d in daily_summaries)
        breaks = sum(d["breaks"] for d in daily_summaries)

        fatigue_values = [d["avg_fatigue"] for d in daily_summaries if d["avg_fatigue"] > 0]
        avg_fatigue = sum(fatigue_values) / len(fatigue_values) if fatigue_values else 0.0

        # -----------------------------------------------------
        # PREMIUM MONTHLY INSIGHTS
        # -----------------------------------------------------
        insights = []

        if deep_work > 400:
            insights.append("Exceptional deep work this month — strong sustained focus.")

        if deep_reading > 300:
            insights.append("High-quality reading time — excellent cognitive recovery.")

        if avg_fatigue > 60:
            insights.append("Fatigue was elevated this month. Consider lighter sessions or more breaks.")

        if breaks < 40:
            insights.append("Very few breaks — adding short pauses may improve energy balance.")

        if total_focus > 1200:
            insights.append("Strong overall productivity — consistent daily engagement.")

        if not insights:
            insights.append("A balanced, steady month overall.")

        return {
            "month_start": first.strftime("%Y-%m-%d"),
            "month_end": last.strftime("%Y-%m-%d"),
            "total_focus": total_focus,
            "deep_work": deep_work,
            "deep_reading": deep_reading,
            "focused_interaction": focused_interaction,
            "breaks": breaks,
            "avg_fatigue": avg_fatigue,
            "insights": insights
        }

    # ---------------------------------------------------------
    # PUBLIC: Generate summary for the current month
    # ---------------------------------------------------------
    def generate_this_month(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return self.generate_for_date(today)

    # ---------------------------------------------------------
    # PUBLIC: Generate summary for last month
    # ---------------------------------------------------------
    def generate_last_month(self):
        today = datetime.now()
        if today.month == 1:
            last_month_date = today.replace(year=today.year - 1, month=12, day=15)
        else:
            last_month_date = today.replace(month=today.month - 1, day=15)
        return self.generate_for_date(last_month_date.strftime("%Y-%m-%d"))
