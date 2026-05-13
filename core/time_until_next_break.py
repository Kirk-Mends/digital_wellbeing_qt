






# import tkinter as tk

# class TimeUntilBreak(tk.Frame):
#     def __init__(self, master, engine, app, update_ms=1000):
#         super().__init__(master)

#         self.engine = engine      # break engine reference
#         self.app = app            # app reference (for settings)

#         # default colors
#         self.bg = "#F5F7FA"
#         self.fg = "#333333"

#         self.label = tk.Label(
#             self,
#             text="Next break in: --:--",
#             font=("Segoe UI", 10),
#             bg=self.bg,
#             fg=self.fg
#         )
#         self.label.pack()

#         self.update_ms = update_ms
#         self.after(self.update_ms, self.refresh)

#     # simple time formatter
#     def fmt(self, sec):
#         m = int(sec // 60)
#         s = int(sec % 60)
#         return f"{m:02d}:{s:02d}"

#     def refresh(self):
#         # read break mode safely
#         try:
#             mode = self.app.settings.get("break_mode")
#         except:
#             mode = "hybrid"

#         # STRICT MODE → real time only
#         if mode == "strict":
#             try:
#                 interval_sec = int(self.app.settings.get("break_interval_minutes")) * 60
#             except:
#                 interval_sec = 20 * 60  # fallback

#             # remaining time until break
#             remaining = max(0, interval_sec - self.engine.real_time)

#         else:
#             # HYBRID MODE → adaptive thresholds
#             real_threshold = self.engine.config.base_real_time * self.engine.real_factor
#             active_threshold = self.engine.config.base_active_time * self.engine.active_factor

#             real_left = max(0, real_threshold - self.engine.real_time)
#             active_left = max(0, active_threshold - self.engine.active_time)

#             # next break is whichever threshold is reached first
#             remaining = min(real_left, active_left)

#         # update label text
#         self.label.config(text=f"Next break in: {self.fmt(remaining)}")

#         # schedule next update
#         self.after(self.update_ms, self.refresh)

#     # allow theme updates from app.py
#     def apply_theme(self, bg, fg):
#         self.bg = bg
#         self.fg = fg
#         self.configure(bg=bg)
#         self.label.configure(bg=bg, fg=fg)






# THE CODE ABOVE WORKED PERFECTLY WITH NO ISSUES--------------
# THE CODE ABOVE WORKED PERFECTLY WITH NO ISSUES--------------  



# THIS IS FOR DESIGN REFERENCE ONLY. DO NOT SUGGEST ANY CHANGES TO IT.
import tkinter as tk
import math

class TimeUntilBreak(tk.Frame):
    def __init__(self, master, engine, app, update_ms=1000):
        super().__init__(master)

        self.engine = engine
        self.app = app

        self.bg = "#F5F7FA"
        self.fg = "#333333"

        self.label = tk.Label(
            self,
            text="Next break in: --:--",
            font=("Segoe UI", 10),
            bg=self.bg,
            fg=self.fg
        )
        self.label.pack()

        self.update_ms = update_ms
        self.after(self.update_ms, self.refresh)

    def fmt(self, sec):
        sec = max(0, int(sec))
        m = sec // 60
        s = sec % 60
        return f"{m:02d}:{s:02d}"

    def refresh(self):
        try:
            mode = self.app.settings.get("break_mode")  # "classic", "smart", "intelligent"
        except:
            mode = "smart"

        remaining = 0
        label_text = "Next break in: --:--"

        if mode == "classic":
            # fixed interval in minutes
            try:
                interval_sec = int(self.app.settings.get("break_interval_minutes")) * 60
            except:
                interval_sec = 20 * 60
            remaining = max(0, interval_sec - self.engine.real_time)
            label_text = f"Next break in: {self.fmt(remaining)}"

        elif mode == "smart":
            # adaptive thresholds (real + active)
            real_threshold = self.engine.config.base_real_time * self.engine.real_factor
            active_threshold = self.engine.config.base_active_time * self.engine.active_factor

            real_left = max(0, real_threshold - self.engine.real_time)
            active_left = max(0, active_threshold - self.engine.active_time)

            remaining = min(real_left, active_left)
            label_text = f"Next break in: {self.fmt(remaining)}"

        elif mode == "intelligent":
            # AI‑adaptive interval estimate
            interval_sec = None
            try:
                decision = getattr(self.engine, "last_decision", None) or getattr(self.engine, "decision", None)
                if decision and "interval_used" in decision:
                    interval_sec = decision["interval_used"]
            except:
                interval_sec = None

            if interval_sec is None:
                # fallback: simple estimate
                interval_sec = 15 * 60

            # estimate remaining based on real_time
            remaining = max(0, interval_sec - self.engine.real_time)
            approx_min = max(1, math.ceil(remaining / 60))
            label_text = f"Next break: ~{approx_min} minutes"

        self.label.config(text=label_text)
        self.after(self.update_ms, self.refresh)

    def apply_theme(self, bg, fg):
        self.bg = bg
        self.fg = fg
        self.configure(bg=bg)
        self.label.configure(bg=bg, fg=fg)



# THE CODE ABOVE WORKED PERFECTLY WITH NO ISSUES--------------
# THE CODE ABOVE WORKED PERFECTLY WITH NO ISSUES--------------  























