













# # #I ADDED THE AI SETTINGS TO THIS VERSION. KEEPING FOR REFERENCE.
# # import json
# # import os
# # import tkinter as tk
# # from tkinter import ttk

# # # ------------------------------------------------------------
# # # DEFAULT SETTINGS
# # # ------------------------------------------------------------

# # DEFAULT_SETTINGS = {
# #     "break_interval_minutes": 30,
# #     "sound_on": True,
# #     "dark_mode": False,
# #     "break_mode": "hybrid",   # strict | hybrid | ai
# # }

# # SETTINGS_FILE = "settings.json"


# # # ------------------------------------------------------------
# # # SETTINGS MANAGER
# # # ------------------------------------------------------------

# # class SettingsManager:
# #     def __init__(self):
# #         self.settings = DEFAULT_SETTINGS.copy()
# #         self.load()

# #     def load(self):
# #         if os.path.exists(SETTINGS_FILE):
# #             try:
# #                 with open(SETTINGS_FILE, "r") as f:
# #                     data = json.load(f)
# #                     self.settings.update(data)
# #             except Exception:
# #                 self.settings = DEFAULT_SETTINGS.copy()

# #     def save(self):
# #         with open(SETTINGS_FILE, "w") as f:
# #             json.dump(self.settings, f, indent=4)

# #     def get(self, key):
# #         return self.settings.get(key, DEFAULT_SETTINGS.get(key))

# #     def set(self, key, value):
# #         self.settings[key] = value
# #         self.save()


# # # ------------------------------------------------------------
# # # SETTINGS WINDOW
# # # ------------------------------------------------------------

# # class SettingsWindow:
# #     def __init__(self, parent, settings_manager: SettingsManager, apply_callback=None):
# #         self.parent = parent
# #         self.settings_manager = settings_manager
# #         self.apply_callback = apply_callback

# #         self.window = tk.Toplevel(parent)
# #         self.window.title("Settings")
# #         self.window.geometry("360x300")
# #         self.window.resizable(False, False)

# #         self.build_ui()

# #     def build_ui(self):
# #         frame = ttk.Frame(self.window, padding=15)
# #         frame.pack(fill="both", expand=True)

# #         # --------------------------------------------------------
# #         # BREAK MODE
# #         # --------------------------------------------------------
# #         ttk.Label(frame, text="Break Mode:").grid(row=0, column=0, sticky="w", pady=(0, 5))

# #         self.break_mode_var = tk.StringVar(value=self.settings_manager.get("break_mode"))
# #         self.break_mode_combo = ttk.Combobox(
# #             frame,
# #             textvariable=self.break_mode_var,
# #             values=["Classic", "Smart", "Intelligent"],   # AI MODE ADDED
# #             state="readonly",
# #             width=12
# #         )
# #         self.break_mode_combo.grid(row=0, column=1, sticky="w", pady=(0, 5), padx=(10, 0))
# #         self.break_mode_combo.bind("<<ComboboxSelected>>", lambda e: self._toggle_interval_visibility())

# #         # --------------------------------------------------------
# #         # BREAK INTERVAL (Strict Mode Only)
# #         # --------------------------------------------------------
# #         ttk.Label(frame, text="Break interval (minutes):").grid(row=1, column=0, sticky="w", pady=(0, 5))

# #         self.interval_var = tk.IntVar(value=int(self.settings_manager.get("break_interval_minutes")))
# #         self.interval_spin = ttk.Spinbox(
# #             frame,
# #             from_=1,
# #             to=1440,
# #             increment=1,
# #             textvariable=self.interval_var,
# #             width=6
# #         )
# #         self.interval_spin.grid(row=1, column=1, sticky="w", pady=(0, 5), padx=(10, 0))

# #         # --------------------------------------------------------
# #         # SOUND
# #         # --------------------------------------------------------
# #         self.sound_var = tk.BooleanVar(value=bool(self.settings_manager.get("sound_on")))
# #         self.sound_check = ttk.Checkbutton(frame, text="Enable notification sound", variable=self.sound_var)
# #         self.sound_check.grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

# #         # --------------------------------------------------------
# #         # DARK MODE
# #         # --------------------------------------------------------
# #         self.dark_var = tk.BooleanVar(value=bool(self.settings_manager.get("dark_mode")))
# #         self.dark_check = ttk.Checkbutton(frame, text="Enable dark mode", variable=self.dark_var)
# #         self.dark_check.grid(row=3, column=0, columnspan=2, sticky="w", pady=5)

# #         # --------------------------------------------------------
# #         # BUTTONS
# #         # --------------------------------------------------------
# #         btn_frame = ttk.Frame(frame)
# #         btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

# #         ttk.Button(btn_frame, text="Apply", command=self.apply).grid(row=0, column=0, padx=5)
# #         ttk.Button(btn_frame, text="Close", command=self.window.destroy).grid(row=0, column=1, padx=5)

# #         # Initial visibility
# #         self._toggle_interval_visibility()

# #     # ------------------------------------------------------------
# #     # SHOW/HIDE INTERVAL BASED ON MODE
# #     # ------------------------------------------------------------
# #     def _toggle_interval_visibility(self):
# #         mode = self.break_mode_var.get()

# #         # Only Strict Mode uses a fixed interval
# #         if mode == "strict":
# #             self.interval_spin.grid()
# #         else:
# #             self.interval_spin.grid_remove()

# #     # ------------------------------------------------------------
# #     # APPLY SETTINGS
# #     # ------------------------------------------------------------
# #     def apply(self):
# #         # Validate interval
# #         try:
# #             interval = int(self.interval_var.get())
# #             if interval < 1:
# #                 interval = 1
# #         except Exception:
# #             interval = int(DEFAULT_SETTINGS["break_interval_minutes"])

# #         # Save settings
# #         self.settings_manager.set("break_interval_minutes", interval)
# #         self.settings_manager.set("sound_on", bool(self.sound_var.get()))
# #         self.settings_manager.set("dark_mode", bool(self.dark_var.get()))
# #         self.settings_manager.set("break_mode", self.break_mode_var.get())

# #         # Callback to update app immediately
# #         if self.apply_callback:
# #             try:
# #                 self.apply_callback()
# #             except Exception:
# #                 pass

# #         try:
# #             self.window.destroy()
# #         except Exception:
# #             pass


# # --------THE CODE ABOVE WORKED PERFECTLY WITH NO ISSUES--------------
# # --------THE CODE ABOVE WORKED PERFECTLY WITH NO ISSUES--------------
# # --------THE CODE ABOVE WORKED PERFECTLY WITH NO ISSUES--------------
# # --------THE CODE ABOVE WORKED PERFECTLY WITH NO ISSUES--------------




# # # ============================================================
# # # settings.py — Modern Settings Window with Theme Support
# # # ============================================================

# # import json
# # import os
# # import tkinter as tk
# # from tkinter import ttk
# # from themes import get_theme

# # DEFAULT_SETTINGS = {
# #     "break_interval_minutes": 30,
# #     "sound_on": True,
# #     "theme": "light",
# #     "break_mode": "hybrid",
# # }

# # SETTINGS_FILE = "settings.json"


# # class SettingsManager:
# #     def __init__(self):
# #         self.settings = DEFAULT_SETTINGS.copy()
# #         self.load()

# #     def load(self):
# #         if os.path.exists(SETTINGS_FILE):
# #             try:
# #                 with open(SETTINGS_FILE, "r") as f:
# #                     data = json.load(f)
# #                     self.settings.update(data)
# #             except Exception:
# #                 self.settings = DEFAULT_SETTINGS.copy()

# #     def save(self):
# #         with open(SETTINGS_FILE, "w") as f:
# #             json.dump(self.settings, f, indent=4)

# #     def get(self, key):
# #         return self.settings.get(key, DEFAULT_SETTINGS.get(key))

# #     def set(self, key, value):
# #         self.settings[key] = value
# #         self.save()


# # class SettingsWindow:
# #     BASE_WIDTH = 420
# #     BASE_HEIGHT = 360

# #     def __init__(self, parent, settings_manager: SettingsManager, apply_callback=None):
# #         self.parent = parent
# #         self.settings_manager = settings_manager
# #         self.apply_callback = apply_callback

# #         self.window = tk.Toplevel(parent)
# #         self.window.title("Settings")
# #         self.window.geometry(f"{self.BASE_WIDTH}x{self.BASE_HEIGHT}")
# #         self.window.resizable(True, True)

# #         self.window.bind("<Configure>", self.on_resize)
# #         self.scale = 1.0

# #         self.build_ui()

# #     def on_resize(self, event):
# #         w = self.window.winfo_width()
# #         h = self.window.winfo_height()
# #         self.scale = min(w / self.BASE_WIDTH, h / self.BASE_HEIGHT)
# #         self.update_scaling()

# #     def update_scaling(self):
# #         font_size = int(12 * self.scale)
# #         for widget in self.window.winfo_children():
# #             try:
# #                 widget.configure(font=("Segoe UI", font_size))
# #             except:
# #                 pass

# #     def build_ui(self):
# #         theme = get_theme(self.settings_manager.get("theme"))

# #         self.window.configure(bg=theme["bg"])

# #         # Floating card panel
# #         card = tk.Frame(
# #             self.window,
# #             bg=theme["panel"],
# #             bd=0,
# #             highlightthickness=1,
# #             highlightbackground=theme["border"]
# #         )
# #         card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.88)

# #         # Title
# #         tk.Label(
# #             card,
# #             text="Settings",
# #             font=("Segoe UI Semibold", 16),
# #             bg=theme["panel"],
# #             fg=theme["text"]
# #         ).pack(pady=10)

# #         # Break Mode
# #         tk.Label(card, text="Break Mode:", bg=theme["panel"], fg=theme["text"]).pack(anchor="w", padx=20)
# #         self.break_mode_var = tk.StringVar(value=self.settings_manager.get("break_mode"))
# #         ttk.Combobox(
# #             card,
# #             textvariable=self.break_mode_var,
# #             values=["Classic", "Smart", "Intelligent"],
# #             state="readonly",
# #             width=15
# #         ).pack(padx=20, pady=5, anchor="w")

# #         # Interval
# #         tk.Label(card, text="Break Interval (minutes):", bg=theme["panel"], fg=theme["text"]).pack(anchor="w", padx=20)
# #         self.interval_var = tk.IntVar(value=int(self.settings_manager.get("break_interval_minutes")))
# #         ttk.Spinbox(card, from_=1, to=1440, textvariable=self.interval_var, width=10).pack(padx=20, pady=5, anchor="w")

# #         # Sound
# #         self.sound_var = tk.BooleanVar(value=bool(self.settings_manager.get("sound_on")))
# #         tk.Checkbutton(
# #             card,
# #             text="Enable notification sound",
# #             variable=self.sound_var,
# #             bg=theme["panel"],
# #             fg=theme["text"],
# #             selectcolor=theme["card"]
# #         ).pack(anchor="w", padx=20, pady=5)

# #         # Theme
# #         tk.Label(card, text="Theme:", bg=theme["panel"], fg=theme["text"]).pack(anchor="w", padx=20)
# #         self.theme_var = tk.StringVar(value=self.settings_manager.get("theme"))
# #         ttk.Combobox(
# #             card,
# #             textvariable=self.theme_var,
# #             values=["light", "dark", "gray", "blue", "teal", "purple"],
# #             state="readonly",
# #             width=15
# #         ).pack(padx=20, pady=5, anchor="w")

# #         # Buttons
# #         btn_frame = tk.Frame(card, bg=theme["panel"])
# #         btn_frame.pack(pady=20)

# #         ttk.Button(btn_frame, text="Apply", command=self.apply).pack(side="left", padx=10)
# #         ttk.Button(btn_frame, text="Close", command=self.window.destroy).pack(side="left", padx=10)

# #     def apply(self):
# #         interval = max(1, int(self.interval_var.get()))
# #         self.settings_manager.set("break_interval_minutes", interval)
# #         self.settings_manager.set("sound_on", bool(self.sound_var.get()))
# #         self.settings_manager.set("theme", self.theme_var.get())
# #         self.settings_manager.set("break_mode", self.break_mode_var.get())

# #         if self.apply_callback:
# #             self.apply_callback()

# #         self.window.destroy()








# # Note that I started the updates from here 


















# # # ============================================================
# # # settings.py — Modern Settings Window with Theme + Mode
# # # ============================================================

# # import json
# # import os
# # import tkinter as tk
# # from tkinter import ttk
# # from themes import get_theme

# # # ------------------------------------------------------------
# # # DEFAULT SETTINGS
# # # ------------------------------------------------------------

# # DEFAULT_SETTINGS = {
# #     "break_interval_minutes": 30,
# #     "sound_on": True,
# #     "theme": "light",          # light | dark | gray | blue | teal | purple
# #     "break_mode": "hybrid",    # strict | hybrid | ai
# # }

# # SETTINGS_FILE = "settings.json"


# # # ------------------------------------------------------------
# # # SETTINGS MANAGER
# # # ------------------------------------------------------------

# # class SettingsManager:
# #     def __init__(self):
# #         self.settings = DEFAULT_SETTINGS.copy()
# #         self.load()

# #     def load(self):
# #         if os.path.exists(SETTINGS_FILE):
# #             try:
# #                 with open(SETTINGS_FILE, "r") as f:
# #                     data = json.load(f)
# #                     self.settings.update(data)
# #             except Exception:
# #                 self.settings = DEFAULT_SETTINGS.copy()

# #     def save(self):
# #         with open(SETTINGS_FILE, "w") as f:
# #             json.dump(self.settings, f, indent=4)

# #     def get(self, key):
# #         return self.settings.get(key, DEFAULT_SETTINGS.get(key))

# #     def set(self, key, value):
# #         self.settings[key] = value
# #         self.save()


# # # ------------------------------------------------------------
# # # SETTINGS WINDOW
# # # ------------------------------------------------------------

# # class SettingsWindow:
# #     BASE_WIDTH = 420
# #     BASE_HEIGHT = 360

# #     def __init__(self, parent, settings_manager: SettingsManager, apply_callback=None):
# #         self.parent = parent
# #         self.settings_manager = settings_manager
# #         self.apply_callback = apply_callback

# #         self.window = tk.Toplevel(parent)
# #         self.window.title("Settings")
# #         self.window.geometry(f"{self.BASE_WIDTH}x{self.BASE_HEIGHT}")
# #         self.window.resizable(True, True)

# #         self.window.bind("<Configure>", self.on_resize)
# #         self.scale = 1.0

# #         self.build_ui()

# #     # ---------------- SCALING ----------------

# #     def on_resize(self, event):
# #         w = self.window.winfo_width()
# #         h = self.window.winfo_height()
# #         self.scale = min(w / self.BASE_WIDTH, h / self.BASE_HEIGHT)
# #         self.update_scaling()

# #     def update_scaling(self):
# #         font_size = int(12 * self.scale)
# #         for widget in self.window.winfo_children():
# #             try:
# #                 widget.configure(font=("Segoe UI", font_size))
# #             except:
# #                 pass

# #     # ---------------- MODE MAPPING ----------------

# #     def _mode_to_display(self, mode_internal: str) -> str:
# #         mapping = {
# #             "strict": "Classic",
# #             "hybrid": "Smart",
# #             "ai": "Intelligent"
# #         }
# #         return mapping.get(mode_internal, "Smart")

# #     def _display_to_mode(self, display: str) -> str:
# #         display = display.lower()
# #         if display == "classic":
# #             return "strict"
# #         if display == "smart":
# #             return "hybrid"
# #         if display == "intelligent":
# #             return "ai"
# #         return "hybrid"

# #     # ---------------- UI BUILD ----------------

# #     def build_ui(self):
# #         theme = get_theme(self.settings_manager.get("theme"))

# #         self.window.configure(bg=theme["bg"])

# #         # Floating card panel with tighter spacing
# #         card = tk.Frame(
# #             self.window,
# #             bg=theme["panel"],
# #             bd=0,
# #             highlightthickness=1,
# #             highlightbackground=theme["border"]
# #         )
# #         card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.88)

# #         # Title
# #         tk.Label(
# #             card,
# #             text="Settings",
# #             font=("Segoe UI Semibold", 16),
# #             bg=theme["panel"],
# #             fg=theme["text"]
# #         ).pack(pady=10)

# #         # -------- Break Mode --------
# #         tk.Label(
# #             card,
# #             text="Break Mode:",
# #             bg=theme["panel"],
# #             fg=theme["text"]
# #         ).pack(anchor="w", padx=20)

# #         current_mode_internal = self.settings_manager.get("break_mode")
# #         current_mode_display = self._mode_to_display(current_mode_internal)

# #         self.break_mode_var = tk.StringVar(value=current_mode_display)
# #         self.break_mode_combo = ttk.Combobox(
# #             card,
# #             textvariable=self.break_mode_var,
# #             values=["Classic", "Smart", "Intelligent"],
# #             state="readonly",
# #             width=15
# #         )
# #         self.break_mode_combo.pack(padx=20, pady=5, anchor="w")
# #         self.break_mode_combo.bind("<<ComboboxSelected>>", lambda e: self._toggle_interval_visibility())

# #         # -------- Break Interval (Classic only) --------
# #         self.interval_label = tk.Label(
# #             card,
# #             text="Break Interval (minutes):",
# #             bg=theme["panel"],
# #             fg=theme["text"]
# #         )
# #         self.interval_var = tk.IntVar(value=int(self.settings_manager.get("break_interval_minutes")))
# #         self.interval_spin = ttk.Spinbox(
# #             card,
# #             from_=1,
# #             to=1440,
# #             textvariable=self.interval_var,
# #             width=10
# #         )

# #         # -------- Sound --------
# #         self.sound_var = tk.BooleanVar(value=bool(self.settings_manager.get("sound_on")))
# #         tk.Checkbutton(
# #             card,
# #             text="Enable notification sound",
# #             variable=self.sound_var,
# #             bg=theme["panel"],
# #             fg=theme["text"],
# #             selectcolor=theme["card"],
# #             activebackground=theme["panel"],
# #             activeforeground=theme["text"]
# #         ).pack(anchor="w", padx=20, pady=5)

# #         # -------- Theme --------
# #         tk.Label(
# #             card,
# #             text="Theme:",
# #             bg=theme["panel"],
# #             fg=theme["text"]
# #         ).pack(anchor="w", padx=20)

# #         self.theme_var = tk.StringVar(value=self.settings_manager.get("theme"))
# #         self.theme_combo = ttk.Combobox(
# #             card,
# #             textvariable=self.theme_var,
# #             values=["light", "dark", "gray", "blue", "teal", "purple"],
# #             state="readonly",
# #             width=15
# #         )
# #         self.theme_combo.pack(padx=20, pady=5, anchor="w")

# #         # -------- Buttons --------
# #         btn_frame = tk.Frame(card, bg=theme["panel"])
# #         btn_frame.pack(pady=15)

# #         ttk.Button(btn_frame, text="Apply", command=self.apply).pack(side="left", padx=10)
# #         ttk.Button(btn_frame, text="Close", command=self.window.destroy).pack(side="left", padx=10)

# #         # Initial visibility for interval
# #         self._toggle_interval_visibility()

# #     # ---------------- INTERVAL VISIBILITY ----------------

# #     def _toggle_interval_visibility(self):
# #         mode_display = self.break_mode_var.get().lower()
# #         if mode_display == "classic":
# #             self.interval_label.pack(anchor="w", padx=20)
# #             self.interval_spin.pack(anchor="w", padx=20, pady=5)
# #         else:
# #             self.interval_label.pack_forget()
# #             self.interval_spin.pack_forget()

# #     # ---------------- APPLY ----------------

# #     def apply(self):
# #         # Interval (only relevant for Classic, but we store it anyway)
# #         try:
# #             interval = int(self.interval_var.get())
# #             if interval < 1:
# #                 interval = 1
# #         except Exception:
# #             interval = int(DEFAULT_SETTINGS["break_interval_minutes"])

# #         # Mode mapping
# #         mode_internal = self._display_to_mode(self.break_mode_var.get())

# #         # Save settings
# #         self.settings_manager.set("break_interval_minutes", interval)
# #         self.settings_manager.set("sound_on", bool(self.sound_var.get()))
# #         self.settings_manager.set("theme", self.theme_var.get())
# #         self.settings_manager.set("break_mode", mode_internal)

# #         # Callback to update app immediately
# #         if self.apply_callback:
# #             try:
# #                 self.apply_callback()
# #             except Exception:
# #                 pass

# #         try:
# #             self.window.destroy()
# #         except Exception:
# #             pass












# # ============================================================
# # settings.py — Modern Settings Window with Theme + Mode
# # ============================================================

# import json
# import os
# import tkinter as tk
# from tkinter import ttk
# from core.themes import get_theme


# # ------------------------------------------------------------
# # DEFAULT SETTINGS
# # ------------------------------------------------------------

# DEFAULT_SETTINGS = {
#     "break_interval_minutes": 30,
#     "sound_on": True,
#     "theme": "light",          # light | dark | gray | blue | teal | purple
#     "break_mode": "hybrid",    # strict | hybrid | ai
# }

# SETTINGS_FILE = "settings.json"


# # ------------------------------------------------------------
# # SETTINGS MANAGER
# # ------------------------------------------------------------

# class SettingsManager:
#     def __init__(self):
#         self.settings = DEFAULT_SETTINGS.copy()
#         self.load()

#     def load(self):
#         if os.path.exists(SETTINGS_FILE):
#             try:
#                 with open(SETTINGS_FILE, "r") as f:
#                     data = json.load(f)
#                     self.settings.update(data)
#             except Exception:
#                 self.settings = DEFAULT_SETTINGS.copy()

#     def save(self):
#         with open(SETTINGS_FILE, "w") as f:
#             json.dump(self.settings, f, indent=4)

#     def get(self, key):
#         return self.settings.get(key, DEFAULT_SETTINGS.get(key))

#     def set(self, key, value):
#         self.settings[key] = value
#         self.save()


# # ------------------------------------------------------------
# # SETTINGS WINDOW
# # ------------------------------------------------------------

# class SettingsWindow:
#     BASE_WIDTH = 420
#     BASE_HEIGHT = 360

#     def __init__(self, parent, settings_manager: SettingsManager, apply_callback=None):
#         self.parent = parent
#         self.settings_manager = settings_manager
#         self.apply_callback = apply_callback

#         self.window = tk.Toplevel(parent)
#         self.window.title("Settings")
#         self.window.geometry(f"{self.BASE_WIDTH}x{self.BASE_HEIGHT}")
#         self.window.resizable(True, True)

#         self.window.bind("<Configure>", self.on_resize)
#         self.scale = 1.0

#         self.build_ui()

#     # ---------------- SCALING ----------------

#     def on_resize(self, event):
#         w = self.window.winfo_width()
#         h = self.window.winfo_height()
#         self.scale = min(w / self.BASE_WIDTH, h / self.BASE_HEIGHT)
#         self.update_scaling()

#     def update_scaling(self):
#         font_size = int(12 * self.scale)
#         for widget in self.window.winfo_children():
#             try:
#                 widget.configure(font=("Segoe UI", font_size))
#             except:
#                 pass

#     # ---------------- MODE MAPPING ----------------

#     def _mode_to_display(self, mode_internal: str) -> str:
#         mapping = {
#             "strict": "Classic",
#             "hybrid": "Smart",
#             "ai": "Intelligent"
#         }
#         return mapping.get(mode_internal, "Smart")

#     def _display_to_mode(self, display: str) -> str:
#         display = display.lower()
#         if display == "classic":
#             return "strict"
#         if display == "smart":
#             return "hybrid"
#         if display == "intelligent":
#             return "ai"
#         return "hybrid"

#     # ---------------- UI BUILD ----------------

#     def build_ui(self):
#         theme = get_theme(self.settings_manager.get("theme"))

#         self.window.configure(bg=theme["bg"])

#         # Floating card panel with tighter spacing
#         card = tk.Frame(
#             self.window,
#             bg=theme["panel"],
#             bd=0,
#             highlightthickness=1,
#             highlightbackground=theme["border"]
#         )
#         card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.88)

#         # Title
#         tk.Label(
#             card,
#             text="Settings",
#             font=("Segoe UI Semibold", 16),
#             bg=theme["panel"],
#             fg=theme["text"]
#         ).pack(pady=10)

#         # -------- Break Mode --------
#         tk.Label(
#             card,
#             text="Break Mode:",
#             bg=theme["panel"],
#             fg=theme["text"]
#         ).pack(anchor="w", padx=20)

#         current_mode_internal = self.settings_manager.get("break_mode")
#         current_mode_display = self._mode_to_display(current_mode_internal)

#         self.break_mode_var = tk.StringVar(value=current_mode_display)
#         self.break_mode_combo = ttk.Combobox(
#             card,
#             textvariable=self.break_mode_var,
#             values=["Classic", "Smart", "Intelligent"],
#             state="readonly",
#             width=15
#         )
#         self.break_mode_combo.pack(padx=20, pady=5, anchor="w")
#         self.break_mode_combo.bind("<<ComboboxSelected>>", lambda e: self._toggle_interval_visibility())

#         # -------- Break Interval (Classic only, directly under Break Mode) --------
#         self.interval_label = tk.Label(
#             card,
#             text="Break Interval (minutes):",
#             bg=theme["panel"],
#             fg=theme["text"]
#         )
#         self.interval_var = tk.IntVar(value=int(self.settings_manager.get("break_interval_minutes")))
#         self.interval_spin = ttk.Spinbox(
#             card,
#             from_=1,
#             to=1440,
#             textvariable=self.interval_var,
#             width=10
#         )

#         # Set initial visibility *before* other controls so order is correct
#         self._toggle_interval_visibility()

#         # -------- Sound --------
#         self.sound_var = tk.BooleanVar(value=bool(self.settings_manager.get("sound_on")))
#         tk.Checkbutton(
#             card,
#             text="Enable notification sound",
#             variable=self.sound_var,
#             bg=theme["panel"],
#             fg=theme["text"],
#             selectcolor=theme["card"],
#             activebackground=theme["panel"],
#             activeforeground=theme["text"]
#         ).pack(anchor="w", padx=20, pady=5)

#         # -------- Theme --------
#         tk.Label(
#             card,
#             text="Theme:",
#             bg=theme["panel"],
#             fg=theme["text"]
#         ).pack(anchor="w", padx=20)

#         self.theme_var = tk.StringVar(value=self.settings_manager.get("theme"))
#         self.theme_combo = ttk.Combobox(
#             card,
#             textvariable=self.theme_var,
#             values=["light", "dark", "gray", "blue", "teal", "purple"],
#             state="readonly",
#             width=15
#         )
#         self.theme_combo.pack(padx=20, pady=5, anchor="w")

#         # -------- Buttons --------
#         btn_frame = tk.Frame(card, bg=theme["panel"])
#         btn_frame.pack(pady=15)

#         ttk.Button(btn_frame, text="Apply", command=self.apply).pack(side="left", padx=10)
#         ttk.Button(btn_frame, text="Close", command=self.window.destroy).pack(side="left", padx=10)

#     # ---------------- INTERVAL VISIBILITY ----------------

#     def _toggle_interval_visibility(self):
#         mode_display = self.break_mode_var.get().lower()
#         if mode_display == "classic":
#             # Pack right under Break Mode
#             self.interval_label.pack(anchor="w", padx=20)
#             self.interval_spin.pack(anchor="w", padx=20, pady=5)
#         else:
#             self.interval_label.pack_forget()
#             self.interval_spin.pack_forget()

#     # ---------------- APPLY ----------------

#     def apply(self):
#         try:
#             interval = int(self.interval_var.get())
#             if interval < 1:
#                 interval = 1
#         except Exception:
#             interval = int(DEFAULT_SETTINGS["break_interval_minutes"])

#         mode_internal = self._display_to_mode(self.break_mode_var.get())

#         self.settings_manager.set("break_interval_minutes", interval)
#         self.settings_manager.set("sound_on", bool(self.sound_var.get()))
#         self.settings_manager.set("theme", self.theme_var.get())
#         self.settings_manager.set("break_mode", mode_internal)

#         if self.apply_callback:
#             try:
#                 self.apply_callback()
#             except Exception:
#                 pass

#         try:
#             self.window.destroy()
#         except Exception:
#             pass
















# new architecture

# core/settings.py

# import json
# import os

# SETTINGS_FILE = "settings.json"

# # ------------------------------------------------------------
# # DEFAULT SETTINGS (new architecture)
# # ------------------------------------------------------------

# DEFAULT_SETTINGS = {
#     "theme": "light",                 # light | dark | system
#     "sound_enabled": True,            # play sound on break
#     "notifications_enabled": True     # show break popups
# }


# # ------------------------------------------------------------
# # SETTINGS MANAGER
# # ------------------------------------------------------------

# class SettingsManager:
#     def __init__(self):
#         self.settings = DEFAULT_SETTINGS.copy()
#         self.load()
#         self.migrate()
#         self.validate()
#         self.save()

#     # --------------------------------------------------------
#     # LOAD SETTINGS FROM FILE
#     # --------------------------------------------------------
#     def load(self):
#         if os.path.exists(SETTINGS_FILE):
#             try:
#                 with open(SETTINGS_FILE, "r") as f:
#                     data = json.load(f)
#                     self.settings.update(data)
#             except Exception:
#                 # If corrupted, reset to defaults
#                 self.settings = DEFAULT_SETTINGS.copy()

#     # --------------------------------------------------------
#     # MIGRATE OLD SETTINGS → NEW ARCHITECTURE
#     # --------------------------------------------------------
#     def migrate(self):
#         old = self.settings

#         # Rename old keys
#         if "sound_on" in old:
#             old["sound_enabled"] = bool(old["sound_on"])
#             del old["sound_on"]

#         # Remove deprecated keys
#         deprecated = [
#             "break_mode",
#             "break_interval_minutes",
#             "dark_mode"
#         ]
#         for key in deprecated:
#             if key in old:
#                 del old[key]

#         self.settings = old

#     # --------------------------------------------------------
#     # VALIDATE SETTINGS (ensure all keys exist)
#     # --------------------------------------------------------
#     def validate(self):
#         for key, default_value in DEFAULT_SETTINGS.items():
#             if key not in self.settings:
#                 self.settings[key] = default_value

#     # --------------------------------------------------------
#     # SAVE SETTINGS TO FILE
#     # --------------------------------------------------------
#     def save(self):
#         try:
#             with open(SETTINGS_FILE, "w") as f:
#                 json.dump(self.settings, f, indent=4)
#         except Exception:
#             pass

#     # --------------------------------------------------------
#     # GET SETTING (supports default value)
#     # --------------------------------------------------------
#     def get(self, key, default=None):
#         return self.settings.get(key, default)

#     # --------------------------------------------------------
#     # SET SETTING
#     # --------------------------------------------------------
#     def set(self, key, value):
#         self.settings[key] = value
#         self.save()

#     # --------------------------------------------------------
#     # RESET TO DEFAULTS
#     # --------------------------------------------------------
#     def reset(self):
#         self.settings = DEFAULT_SETTINGS.copy()
#         self.save()











# # core/settings.py

# import json
# import os
# from typing import Dict, Any

# # -----------------------------
# # GLOBAL CONSTANTS
# # -----------------------------

# APP_SETTINGS_FILE = "settings.json"      # stores app-wide meta (current profile, etc.)
# PROFILES_DIR = "profiles"                # each profile has its own settings.json

# DEFAULT_SETTINGS: Dict[str, Any] = {
#     "theme": "light",                 # light | dark | system
#     "sound_enabled": True,            # play sound on break
#     "notifications_enabled": True     # show break popups
# }

# DEFAULT_PROFILE_NAME = "default"


# # -----------------------------
# # SETTINGS MANAGER
# # -----------------------------

# class SettingsManager:
#     def __init__(self):
#         # Ensure profiles directory exists
#         os.makedirs(PROFILES_DIR, exist_ok=True)

#         # Load app meta (current profile)
#         self.app_meta = self._load_app_meta()

#         # Active profile name
#         self.current_profile = self.app_meta.get("current_profile", DEFAULT_PROFILE_NAME)

#         # Load profile settings
#         self.settings = DEFAULT_SETTINGS.copy()
#         self.load()
#         self.migrate()
#         self.validate()
#         self.save()

#     # -------------------------
#     # APP META (current profile)
#     # -------------------------
#     def _load_app_meta(self) -> Dict[str, Any]:
#         if os.path.exists(APP_SETTINGS_FILE):
#             try:
#                 with open(APP_SETTINGS_FILE, "r") as f:
#                     return json.load(f)
#             except Exception:
#                 pass
#         return {"current_profile": DEFAULT_PROFILE_NAME}

#     def _save_app_meta(self):
#         self.app_meta["current_profile"] = self.current_profile
#         try:
#             with open(APP_SETTINGS_FILE, "w") as f:
#                 json.dump(self.app_meta, f, indent=4)
#         except Exception:
#             pass

#     # -------------------------
#     # PROFILE PATH
#     # -------------------------
#     def _profile_path(self, profile_name: str) -> str:
#         return os.path.join(PROFILES_DIR, f"{profile_name}.json")

#     # -------------------------
#     # LOAD PROFILE SETTINGS
#     # -------------------------
#     def load(self):
#         path = self._profile_path(self.current_profile)
#         if os.path.exists(path):
#             try:
#                 with open(path, "r") as f:
#                     data = json.load(f)
#                     self.settings.update(data)
#             except Exception:
#                 self.settings = DEFAULT_SETTINGS.copy()
#         else:
#             self.settings = DEFAULT_SETTINGS.copy()

#     # -------------------------
#     # SAVE PROFILE SETTINGS
#     # -------------------------
#     def save(self):
#         path = self._profile_path(self.current_profile)
#         try:
#             with open(path, "w") as f:
#                 json.dump(self.settings, f, indent=4)
#         except Exception:
#             pass
#         self._save_app_meta()

#     # -------------------------
#     # MIGRATE OLD KEYS
#     # -------------------------
#     def migrate(self):
#         old = self.settings

#         # Rename old keys
#         if "sound_on" in old:
#             old["sound_enabled"] = bool(old["sound_on"])
#             del old["sound_on"]

#         # Remove deprecated keys
#         deprecated = [
#             "break_mode",
#             "break_interval_minutes",
#             "dark_mode"
#         ]
#         for key in deprecated:
#             if key in old:
#                 del old[key]

#         self.settings = old

#     # -------------------------
#     # VALIDATE SETTINGS
#     # -------------------------
#     def validate(self):
#         for key, default_value in DEFAULT_SETTINGS.items():
#             if key not in self.settings:
#                 self.settings[key] = default_value

#     # -------------------------
#     # BASIC GET / SET
#     # -------------------------
#     def get(self, key: str, default=None):
#         return self.settings.get(key, default)

#     def set(self, key: str, value: Any):
#         self.settings[key] = value
#         self.save()

#     # -------------------------
#     # RESET CURRENT PROFILE
#     # -------------------------
#     def reset(self):
#         self.settings = DEFAULT_SETTINGS.copy()
#         self.save()

#     # -------------------------
#     # EXPORT / IMPORT SETTINGS
#     # -------------------------
#     def export_settings(self, export_path: str):
#         """Export current profile settings to a JSON file."""
#         try:
#             with open(export_path, "w") as f:
#                 json.dump(self.settings, f, indent=4)
#         except Exception:
#             pass

#     def import_settings(self, import_path: str):
#         """Import settings from a JSON file into current profile."""
#         if not os.path.exists(import_path):
#             return
#         try:
#             with open(import_path, "r") as f:
#                 data = json.load(f)
#             # Merge, then validate
#             self.settings.update(data)
#             self.migrate()
#             self.validate()
#             self.save()
#         except Exception:
#             pass

#     # -------------------------
#     # PROFILE MANAGEMENT
#     # -------------------------
#     def list_profiles(self):
#         """Return a list of available profile names."""
#         profiles = []
#         for fname in os.listdir(PROFILES_DIR):
#             if fname.endswith(".json"):
#                 profiles.append(os.path.splitext(fname)[0])
#         if DEFAULT_PROFILE_NAME not in profiles:
#             profiles.append(DEFAULT_PROFILE_NAME)
#         return sorted(set(profiles))

#     def switch_profile(self, profile_name: str):
#         """Switch to another profile (creates it if missing)."""
#         if not profile_name:
#             profile_name = DEFAULT_PROFILE_NAME

#         self.current_profile = profile_name
#         self.load()
#         self.migrate()
#         self.validate()
#         self.save()

#     def delete_profile(self, profile_name: str):
#         """Delete a profile (except the default)."""
#         if profile_name == DEFAULT_PROFILE_NAME:
#             return
#         path = self._profile_path(profile_name)
#         if os.path.exists(path):
#             try:
#                 os.remove(path)
#             except Exception:
#                 pass
#         # If we deleted the active profile, fall back to default
#         if self.current_profile == profile_name:
#             self.current_profile = DEFAULT_PROFILE_NAME
#             self.load()
#             self.migrate()
#             self.validate()
#             self.save()










# core/settings.py

import json
import os
import sys
from typing import Dict, Any
from PySide6.QtCore import QStandardPaths

# -----------------------------
# DYNAMIC PATH HELPER
# -----------------------------
def get_base_save_path():
    """ 
    Ensures settings are saved in:
    /Users/username/Library/Application Support/KMends/
    """
    # This creates the path based on your App Name
    path = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path

BASE_PATH = get_base_save_path()

# Update these to use the BASE_PATH
APP_SETTINGS_FILE = os.path.join(BASE_PATH, "settings.json")
PROFILES_DIR = os.path.join(BASE_PATH, "profiles")

# -----------------------------
# GLOBAL CONSTANTS
# -----------------------------
DEFAULT_SETTINGS: Dict[str, Any] = {
    "theme": "light",
    "sound_enabled": True,
    "notifications_enabled": True
}

DEFAULT_PROFILE_NAME = "default"

# ... the rest of your SettingsManager class remains the same ...

# -----------------------------
# SETTINGS MANAGER
# -----------------------------

class SettingsManager:
    def __init__(self):
        # Ensure profiles directory exists
        os.makedirs(PROFILES_DIR, exist_ok=True)

        # Load app meta (current profile)
        self.app_meta = self._load_app_meta()

        # Active profile name
        self.current_profile = self.app_meta.get("current_profile", DEFAULT_PROFILE_NAME)

        # Load profile settings
        self.settings = DEFAULT_SETTINGS.copy()
        self.load()
        self.migrate()
        self.validate()
        self.save()

    # -------------------------
    # APP META (current profile)
    # -------------------------
    def _load_app_meta(self) -> Dict[str, Any]:
        if os.path.exists(APP_SETTINGS_FILE):
            try:
                with open(APP_SETTINGS_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"current_profile": DEFAULT_PROFILE_NAME}

    def _save_app_meta(self):
        self.app_meta["current_profile"] = self.current_profile
        try:
            with open(APP_SETTINGS_FILE, "w") as f:
                json.dump(self.app_meta, f, indent=4)
        except Exception:
            pass

    # -------------------------
    # PROFILE PATH
    # -------------------------
    def _profile_path(self, profile_name: str) -> str:
        return os.path.join(PROFILES_DIR, f"{profile_name}.json")

    # -------------------------
    # LOAD PROFILE SETTINGS
    # -------------------------
    def load(self):
        path = self._profile_path(self.current_profile)
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    self.settings.update(data)
            except Exception:
                self.settings = DEFAULT_SETTINGS.copy()
        else:
            self.settings = DEFAULT_SETTINGS.copy()

    # -------------------------
    # SAVE PROFILE SETTINGS
    # -------------------------
    def save(self):
        path = self._profile_path(self.current_profile)
        try:
            with open(path, "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception:
            pass
        self._save_app_meta()

    # -------------------------
    # MIGRATE OLD KEYS
    # -------------------------
    def migrate(self):
        old = self.settings

        # Rename old keys
        if "sound_on" in old:
            old["sound_enabled"] = bool(old["sound_on"])
            del old["sound_on"]

        # Remove deprecated keys
        deprecated = [
            "break_mode",
            "break_interval_minutes",
            "dark_mode"
        ]
        for key in deprecated:
            if key in old:
                del old[key]

        self.settings = old

    # -------------------------
    # VALIDATE SETTINGS
    # -------------------------
    def validate(self):
        for key, default_value in DEFAULT_SETTINGS.items():
            if key not in self.settings:
                self.settings[key] = default_value

    # -------------------------
    # BASIC GET / SET
    # -------------------------
    def get(self, key: str, default=None):
        return self.settings.get(key, default)

    def set(self, key: str, value: Any):
        self.settings[key] = value
        self.save()

    # -------------------------
    # RESET CURRENT PROFILE
    # -------------------------
    def reset(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.save()

    # -------------------------
    # EXPORT / IMPORT SETTINGS
    # -------------------------
    def export_settings(self, export_path: str):
        """Export current profile settings to a JSON file."""
        try:
            with open(export_path, "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception:
            pass

    def import_settings(self, import_path: str):
        """Import settings from a JSON file into current profile."""
        if not os.path.exists(import_path):
            return
        try:
            with open(import_path, "r") as f:
                data = json.load(f)
            # Merge, then validate
            self.settings.update(data)
            self.migrate()
            self.validate()
            self.save()
        except Exception:
            pass

    # -------------------------
    # PROFILE MANAGEMENT
    # -------------------------
    def list_profiles(self):
        """Return a list of available profile names."""
        profiles = []
        for fname in os.listdir(PROFILES_DIR):
            if fname.endswith(".json"):
                profiles.append(os.path.splitext(fname)[0])
        if DEFAULT_PROFILE_NAME not in profiles:
            profiles.append(DEFAULT_PROFILE_NAME)
        return sorted(set(profiles))

    def switch_profile(self, profile_name: str):
        """Switch to another profile (creates it if missing)."""
        if not profile_name:
            profile_name = DEFAULT_PROFILE_NAME

        self.current_profile = profile_name
        self.load()
        self.migrate()
        self.validate()
        self.save()

    def delete_profile(self, profile_name: str):
        """Delete a profile (except the default)."""
        if profile_name == DEFAULT_PROFILE_NAME:
            return
        path = self._profile_path(profile_name)
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass
        # If we deleted the active profile, fall back to default
        if self.current_profile == profile_name:
            self.current_profile = DEFAULT_PROFILE_NAME
            self.load()
            self.migrate()
            self.validate()
            self.save()


