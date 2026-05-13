# visualizer.py
# This file reads the usage_log.csv file and draws simple charts.
# It uses matplotlib to show daily active minutes and reminders.

# import csv
# import matplotlib.pyplot as plt
# from datetime import datetime

# class UsageVisualizer:
#     def __init__(self, filename="usage_log.csv"):
#         # store the CSV file name
#         self.filename = filename

#     def load_data(self):
#         # lists to store data from CSV
#         dates = []
#         active_minutes = []
#         reminders = []

#         # open the CSV and read each row
#         with open(self.filename, "r") as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 # convert date string to datetime object
#                 dates.append(datetime.fromisoformat(row["date"]))
#                 # convert numbers to float/int
#                 active_minutes.append(float(row["active_minutes"]))
#                 reminders.append(int(row["reminders"]))

#         return dates, active_minutes, reminders

#     def plot_daily_usage(self):
#         # load data from file
#         dates, active_minutes, reminders = self.load_data()

#         # create a line chart
#         plt.figure(figsize=(10, 5))
#         plt.plot(dates, active_minutes, marker="o", label="Active Minutes")
#         plt.title("Daily Screen-Time")
#         plt.xlabel("Date")
#         plt.ylabel("Active Minutes")
#         plt.grid(True)
#         plt.legend()
#         plt.tight_layout()
#         plt.show()

#     def plot_reminders(self):
#         # load data from file
#         dates, active_minutes, reminders = self.load_data()

#         # create a bar chart
#         plt.figure(figsize=(10, 5))
#         plt.bar(dates, reminders, color="orange")
#         plt.title("Daily Break Reminders")
#         plt.xlabel("Date")
#         plt.ylabel("Number of Reminders")
#         plt.tight_layout()
#         plt.show()










import csv
import matplotlib.pyplot as plt
from matplotlib import ticker
from datetime import datetime
import numpy as np


class UsageVisualizer:
    def __init__(self, filename="usage_log.csv"):
        self.filename = filename

        # apply a modern style to all charts
        plt.style.use("seaborn-v0_8-whitegrid")

        # custom modern palette
        self.accent = "#4A90E2"
        self.accent_soft = "#A7C4F2"
        self.orange = "#FF9F43"
        self.bg = "#F5F7FA"

    def load_data(self):
        dates = []
        active_minutes = []
        reminders = []

        with open(self.filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                dates.append(datetime.fromisoformat(row["date"]))
                active_minutes.append(float(row["active_minutes"]))
                reminders.append(int(row["reminders"]))

        return dates, active_minutes, reminders

    # -------------------------------
    # Modern Daily Usage Chart
    # -------------------------------
    def plot_daily_usage(self):
        dates, active_minutes, reminders = self.load_data()

        fig, ax = plt.subplots(figsize=(11, 5))
        fig.patch.set_facecolor(self.bg)
        ax.set_facecolor("white")

        # smooth line
        ax.plot(
            dates,
            active_minutes,
            color=self.accent,
            linewidth=3,
            marker="o",
            markersize=6,
            markerfacecolor="white",
            markeredgewidth=2,
        )

        # gradient fill under line
        ax.fill_between(
            dates,
            active_minutes,
            color=self.accent_soft,
            alpha=0.35
        )

        # modern title
        ax.set_title(
            "Daily Active Screen-Time",
            fontsize=18,
            fontweight="semibold",
            color="#333333",
            pad=20
        )

        # clean labels
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Active Minutes", fontsize=12)

        # rotate dates
        plt.xticks(rotation=30, ha="right")

        # remove top + right borders
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        # grid styling
        ax.grid(alpha=0.25)

        plt.tight_layout()
        plt.show()

    # -------------------------------
    # Modern Reminders Chart
    # -------------------------------
    def plot_reminders(self):
        dates, active_minutes, reminders = self.load_data()

        fig, ax = plt.subplots(figsize=(11, 5))
        fig.patch.set_facecolor(self.bg)
        ax.set_facecolor("white")

        # modern rounded bars
        ax.bar(
            dates,
            reminders,
            color=self.orange,
            width=0.6,
            edgecolor="none"
        )

        # modern title
        ax.set_title(
            "Daily Break Reminders",
            fontsize=18,
            fontweight="semibold",
            color="#333333",
            pad=20
        )

        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Reminders", fontsize=12)

        plt.xticks(rotation=30, ha="right")

        # remove top + right borders
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.grid(alpha=0.25)

        plt.tight_layout()
        plt.show()

    # -------------------------------
    # NEW: Weekly Summary Card Chart
    # -------------------------------
    def plot_weekly_summary(self):
        dates, active_minutes, reminders = self.load_data()

        # compute weekly totals
        total_active = sum(active_minutes)
        total_rem = sum(reminders)
        avg_active = np.mean(active_minutes)

        labels = ["Total Active (min)", "Avg Active (min)", "Total Reminders"]
        values = [total_active, avg_active, total_rem]
        colors = [self.accent, self.accent_soft, self.orange]

        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor(self.bg)
        ax.set_facecolor("white")

        bars = ax.bar(labels, values, color=colors, width=0.6)

        # add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 1,
                f"{height:.1f}",
                ha="center",
                fontsize=11,
                fontweight="semibold"
            )

        ax.set_title(
            "Weekly Summary",
            fontsize=18,
            fontweight="semibold",
            color="#333333",
            pad=20
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(alpha=0.25)

        plt.tight_layout()
        plt.show()
