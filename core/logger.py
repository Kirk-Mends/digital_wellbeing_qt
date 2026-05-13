# import csv
# import datetime

# class UsageLogger:
#     def __init__(self, filename="usage_log.csv"):
#         self.filename = filename
#         self.ensure_file_exists()

#     def ensure_file_exists(self):
#         try:
#             with open(self.filename, "x", newline="") as f:
#                 writer = csv.writer(f)
#                 writer.writerow(["date", "active_minutes", "reminders"])
#         except FileExistsError:
#             pass

#     def log(self, active_minutes, reminders):
#         today = datetime.date.today().isoformat()
#         with open(self.filename, "a", newline="") as f:
#             writer = csv.writer(f)
#             writer.writerow([today, round(active_minutes, 2), reminders])






# logger.py
# This file saves and reads usage data (active minutes + reminders)
# from a CSV file. It also calculates daily and weekly stats.

import csv
from datetime import datetime, date, timedelta

class UsageLogger:
    def __init__(self, filename="usage_log.csv"):
        # store file name
        self.filename = filename
        # make sure file exists with correct header
        self.ensure_file_exists()

    def ensure_file_exists(self):
        # create file only if it doesn't exist
        try:
            with open(self.filename, "x", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["date", "active_minutes", "reminders"])
        except FileExistsError:
            # file already exists, do nothing
            pass

    def log(self, active_minutes, reminders):
        # write today's usage to the CSV
        today = date.today().isoformat()
        with open(self.filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([today, round(active_minutes, 2), int(reminders)])

    def _read_logs(self):
        # read all rows from the CSV and return clean tuples
        rows = []
        try:
            with open(self.filename, "r", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row:
                        continue
                    # skip header row
                    if row[0].lower() == "date":
                        continue
                    if len(row) >= 3:
                        d, active, rem = row[0], row[1], row[2]
                        try:
                            # convert strings to proper types
                            parsed_date = datetime.strptime(d, "%Y-%m-%d").date()
                            parsed_active = float(active)
                            parsed_rem = int(rem)
                            rows.append((parsed_date, parsed_active, parsed_rem))
                        except Exception:
                            # skip bad rows
                            continue
        except FileNotFoundError:
            # no file yet, return empty list
            pass
        return rows

    def get_today_active(self):
        # sum all active minutes for today
        today = date.today()
        logs = self._read_logs()
        total = sum(active for d, active, _ in logs if d == today)
        return round(total, 2)

    def get_today_reminders(self):
        # sum all reminders for today
        today = date.today()
        logs = self._read_logs()
        return sum(rem for d, _, rem in logs if d == today)

    def get_weekly_avg(self):
        # average active minutes for the last 7 days
        today = date.today()
        week_ago = today - timedelta(days=6)  # 7‑day window
        logs = self._read_logs()

        # group active minutes by day
        per_day = {}
        for d, active, _ in logs:
            if week_ago <= d <= today:
                per_day.setdefault(d, 0.0)
                per_day[d] += active

        if not per_day:
            return 0

        avg = sum(per_day.values()) / len(per_day)
        return round(avg, 2)

    def get_weekly_reminders(self):
        # total reminders for the last 7 days
        today = date.today()
        week_ago = today - timedelta(days=6)
        logs = self._read_logs()
        return sum(rem for d, _, rem in logs if week_ago <= d <= today)
