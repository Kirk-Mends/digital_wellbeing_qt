# # core/daily_summary_engine.py

# import time
# from datetime import datetime, timedelta
# from core.storage_manager import StorageManager


# class DailySummaryEngine:
#     """
#     Converts raw logs (behavior timeline + break events)
#     into a single daily summary row stored in SQLite.
#     """

#     def __init__(self):
#         # Delay StorageManager creation to avoid circular import timing issues
#         self._storage = None

#     def _get_storage(self):
#         if self._storage is None:
#             self._storage = StorageManager()
#         return self._storage

#     # ---------------------------------------------------------
#     # PUBLIC: Generate summary for a given date (YYYY-MM-DD)
#     # ---------------------------------------------------------
#     def generate_for_date(self, date_str: str):
#         storage = self._get_storage()

#         behavior_rows = storage.get_behavior_for_day(date_str)
#         break_rows = storage.get_breaks_for_day(date_str)

#         if not behavior_rows:
#             summary = {
#                 "date": date_str,
#                 "total_focus": 0,
#                 "deep_work": 0,
#                 "deep_reading": 0,
#                 "focused_interaction": 0,
#                 "breaks": len(break_rows),
#                 "avg_fatigue": 0.0
#             }
#             storage.save_daily_summary(summary)
#             return summary

#         # -----------------------------------------------------
#         # COMPUTE METRICS
#         # -----------------------------------------------------
#         total_focus = 0
#         deep_work = 0
#         deep_reading = 0
#         focused_interaction = 0

#         fatigue_values = []

#         for ts, behavior, fatigue, mode in behavior_rows:
#             behavior = (behavior or "").lower()

#             if behavior in ["reading", "deep_reading", "deep_work", "focused_interaction", "writing"]:
#                 total_focus += 1

#             if behavior == "deep_work":
#                 deep_work += 1
#             elif behavior == "deep_reading":
#                 deep_reading += 1
#             elif behavior == "focused_interaction":
#                 focused_interaction += 1

#             try:
#                 fatigue_values.append(float(fatigue))
#             except:
#                 pass

#         avg_fatigue = sum(fatigue_values) / len(fatigue_values) if fatigue_values else 0.0

#         summary = {
#             "date": date_str,
#             "total_focus": total_focus,
#             "deep_work": deep_work,
#             "deep_reading": deep_reading,
#             "focused_interaction": focused_interaction,
#             "breaks": len(break_rows),
#             "avg_fatigue": avg_fatigue
#         }

#         storage.save_daily_summary(summary)
#         return summary

#     # ---------------------------------------------------------
#     # PUBLIC: Generate summary for yesterday
#     # ---------------------------------------------------------
#     def generate_yesterday(self):
#         yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
#         return self.generate_for_date(yesterday)

#     # ---------------------------------------------------------
#     # PUBLIC: Generate summary for today (useful on shutdown)
#     # ---------------------------------------------------------
#     def generate_today(self):
#         today = datetime.now().strftime("%Y-%m-%d")
#         return self.generate_for_date(today)













# core/daily_summary_engine.py

import time
from datetime import datetime, timedelta
from core.storage_manager import StorageManager


class DailySummaryEngine:
    """
    Converts raw logs (behavior timeline + break events)
    into a single daily summary row stored in SQLite.
    """

    def __init__(self):
        self._storage = None

    def _get_storage(self):
        if self._storage is None:
            self._storage = StorageManager()
        return self._storage

    # ---------------------------------------------------------
    # PUBLIC: Generate summary for a given date (YYYY-MM-DD)
    # ---------------------------------------------------------
    def generate_for_date(self, date_str: str):
        storage = self._get_storage()

        behavior_rows = storage.get_behavior_for_day(date_str)
        break_rows = storage.get_breaks_for_day(date_str)

        # If no behavior logs exist for this day
        if not behavior_rows:
            summary = {
                "date": date_str,
                "total_focus": 0,
                "deep_work": 0,
                "deep_reading": 0,
                "focused_interaction": 0,
                "breaks": len(break_rows),
                "avg_fatigue": 0.0
            }
            storage.save_daily_summary(summary)
            return summary

        # -----------------------------------------------------
        # COMPUTE METRICS
        # -----------------------------------------------------
        total_focus = 0
        deep_work = 0
        deep_reading = 0
        focused_interaction = 0

        fatigue_values = []

        # behavior_rows returns: (timestamp, behavior, fatigue_at_event, mode)
        for ts, behavior, fatigue, mode in behavior_rows:
            behavior = (behavior or "").lower()

            # Focus time = any productive behavior
            if behavior in ["reading", "deep_reading", "deep_work", "focused_interaction", "writing"]:
                total_focus += 1

            if behavior == "deep_work":
                deep_work += 1
            elif behavior == "deep_reading":
                deep_reading += 1
            elif behavior == "focused_interaction":
                focused_interaction += 1

            try:
                fatigue_values.append(float(fatigue))
            except:
                pass

        avg_fatigue = sum(fatigue_values) / len(fatigue_values) if fatigue_values else 0.0

        summary = {
            "date": date_str,
            "total_focus": total_focus,
            "deep_work": deep_work,
            "deep_reading": deep_reading,
            "focused_interaction": focused_interaction,
            "breaks": len(break_rows),
            "avg_fatigue": avg_fatigue
        }

        storage.save_daily_summary(summary)
        return summary

    # ---------------------------------------------------------
    # PUBLIC: Generate summary for yesterday
    # ---------------------------------------------------------
    def generate_yesterday(self):
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        return self.generate_for_date(yesterday)

    # ---------------------------------------------------------
    # PUBLIC: Generate summary for today (useful on shutdown)
    # ---------------------------------------------------------
    def generate_today(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return self.generate_for_date(today)
