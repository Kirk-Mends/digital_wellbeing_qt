

# # core/storage_manager.py

# import os
# import sqlite3
# import json
# from datetime import datetime, date, timedelta
# from pathlib import Path


# class StorageManager:
#     """
#     Premium local storage engine (SQLite) with mode support.
#     - behavior_log (mode-tagged)
#     - fatigue_log (mode-tagged)
#     - break_log (mode-tagged)
#     - suppression_log (mode-tagged)
#     - input_activity_log (legacy Smart Mode)
#     """

#     def __init__(self):
#         self.db_path = self._get_db_path()
#         self._ensure_database()
#         self._run_migrations()

#     # ---------------------------------------------------------
#     # PATHS
#     # ---------------------------------------------------------
#     def _get_db_path(self):
#         appdata = Path(os.getenv("APPDATA"))
#         folder = appdata / "YourApp"
#         folder.mkdir(exist_ok=True)
#         return folder / "user_data.db"

#     def _connect(self):
#         return sqlite3.connect(self.db_path)

#     # ---------------------------------------------------------
#     # DATABASE INIT
#     # ---------------------------------------------------------
#     def _ensure_database(self):
#         conn = self._connect()
#         c = conn.cursor()

#         # Behavior log
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS behavior_log (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 behavior TEXT NOT NULL,
#                 duration INTEGER,
#                 fatigue_at_event REAL,
#                 mode TEXT DEFAULT 'ai'
#             )
#         """)

#         # Fatigue log
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS fatigue_log (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 fatigue REAL NOT NULL,
#                 mode TEXT DEFAULT 'ai'
#             )
#         """)

#         # Break log
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS break_log (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 reason TEXT NOT NULL,
#                 behavior TEXT,
#                 fatigue REAL,
#                 interval_used REAL,
#                 timing_quality TEXT,
#                 mode TEXT DEFAULT 'ai'
#             )
#         """)

#         # Suppression log
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS suppression_log (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 type TEXT NOT NULL,
#                 is_away_reset INTEGER NOT NULL,
#                 mode TEXT DEFAULT 'ai'
#             )
#         """)

#         # Input activity log (legacy Smart Mode)
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS input_activity_log (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 window TEXT,
#                 typing REAL,
#                 mouse REAL,
#                 scroll REAL
#             )
#         """)

#         # Daily summary (clean schema)
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS daily_summary (
#                 date TEXT PRIMARY KEY,
#                 total_focus INTEGER,
#                 deep_work INTEGER,
#                 deep_reading INTEGER,
#                 focused_interaction INTEGER,
#                 breaks INTEGER,
#                 avg_fatigue REAL
#             )
#         """)

#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # MIGRATIONS
#     # ---------------------------------------------------------
#     def _run_migrations(self):
#         conn = self._connect()
#         c = conn.cursor()

#         # Ensure mode column exists on logs (for older DBs)
#         c.execute("PRAGMA table_info(behavior_log)")
#         cols = [col[1] for col in c.fetchall()]
#         if "mode" not in cols:
#             c.execute("ALTER TABLE behavior_log ADD COLUMN mode TEXT DEFAULT 'ai'")

#         c.execute("PRAGMA table_info(fatigue_log)")
#         cols = [col[1] for col in c.fetchall()]
#         if "mode" not in cols:
#             c.execute("ALTER TABLE fatigue_log ADD COLUMN mode TEXT DEFAULT 'ai'")

#         c.execute("PRAGMA table_info(break_log)")
#         cols = [col[1] for col in c.fetchall()]
#         if "mode" not in cols:
#             c.execute("ALTER TABLE break_log ADD COLUMN mode TEXT DEFAULT 'ai'")

#         c.execute("PRAGMA table_info(suppression_log)")
#         cols = [col[1] for col in c.fetchall()]
#         if "mode" not in cols:
#             c.execute("ALTER TABLE suppression_log ADD COLUMN mode TEXT DEFAULT 'ai'")

#         # Ensure daily_summary has correct columns
#         c.execute("PRAGMA table_info(daily_summary)")
#         cols = [col[1] for col in c.fetchall()]
#         required = [
#             "date", "total_focus", "deep_work", "deep_reading",
#             "focused_interaction", "breaks", "avg_fatigue"
#         ]
#         for col in required:
#             if col not in cols:
#                 # types are fine as TEXT for added columns; existing rows stay valid
#                 c.execute(f"ALTER TABLE daily_summary ADD COLUMN {col} TEXT")

#         conn.commit()
#         conn.close()
#     # ---------------------------------------------------------
#     # LEGACY SMART MODE LOGGING
#     # ---------------------------------------------------------
#     def log_behavior(self, behavior, fatigue, window, typing, mouse, scroll):
#         """
#         Legacy Smart Mode logging: behavior_log + input_activity_log.
#         """
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()

#         c.execute("""
#             INSERT INTO behavior_log (timestamp, behavior, duration, fatigue_at_event, mode)
#             VALUES (?, ?, ?, ?, ?)
#         """, (now, behavior, None, fatigue, "smart"))

#         c.execute("""
#             INSERT INTO input_activity_log (timestamp, window, typing, mouse, scroll)
#             VALUES (?, ?, ?, ?, ?)
#         """, (now, window, typing, mouse, scroll))

#         conn.commit()
#         conn.close()

#     def log_fatigue(self, fatigue):
#         """
#         Legacy Smart Mode fatigue logging.
#         """
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO fatigue_log (timestamp, fatigue, mode)
#             VALUES (?, ?, ?)
#         """, (now, float(fatigue), "smart"))
#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # BREAK LOGGING (shared)
#     # ---------------------------------------------------------
#     def log_break(self, reason, behavior, fatigue, interval_used, mode="ai"):
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO break_log (timestamp, reason, behavior, fatigue, interval_used, timing_quality, mode)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (now, reason, behavior, fatigue, interval_used, "on_time", mode))
#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # NEW CLEAN LOGGING FOR AI MODE + SMART MODE
#     # ---------------------------------------------------------
#     def log_behavior_event(self, behavior, fatigue, mode):
#         """
#         Unified behavior event logging (AI + Smart).
#         """
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO behavior_log (timestamp, behavior, duration, fatigue_at_event, mode)
#             VALUES (?, ?, ?, ?, ?)
#         """, (now, behavior, None, fatigue, mode))
#         conn.commit()
#         conn.close()

#     def log_fatigue_event(self, fatigue, mode):
#         """
#         Unified fatigue event logging (AI + Smart).
#         """
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO fatigue_log (timestamp, fatigue, mode)
#             VALUES (?, ?, ?)
#         """, (now, float(fatigue), mode))
#         conn.commit()
#         conn.close()

#     def log_away_event(self, mode):
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO suppression_log (timestamp, type, is_away_reset, mode)
#             VALUES (?, ?, ?, ?)
#         """, (now, "away", 1, mode))
#         conn.commit()
#         conn.close()

#     def log_suppression_event(self, type, mode):
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO suppression_log (timestamp, type, is_away_reset, mode)
#             VALUES (?, ?, ?, ?)
#         """, (now, type, 0, mode))
#         conn.commit()
#         conn.close()

#     def log_input_activity_event(self, typing, mouse, scroll, behavior, mode):
#         """
#         Unified input activity logging (for analytics / ML).
#         """
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO input_activity_log (timestamp, window, typing, mouse, scroll)
#             VALUES (?, ?, ?, ?, ?)
#         """, (now, behavior, typing, mouse, scroll))
#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # DAILY SUMMARY
#     # ---------------------------------------------------------
#     def save_daily_summary(self, summary):
#         conn = self._connect()
#         c = conn.cursor()

#         c.execute("""
#             INSERT OR REPLACE INTO daily_summary
#             (date, total_focus, deep_work, deep_reading,
#              focused_interaction, breaks, avg_fatigue)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (
#             summary["date"],
#             summary["total_focus"],
#             summary["deep_work"],
#             summary["deep_reading"],
#             summary["focused_interaction"],
#             summary["breaks"],
#             summary["avg_fatigue"]
#         ))

#         conn.commit()
#         conn.close()

#     def get_daily_summary(self, date_str):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT date, total_focus, deep_work, deep_reading,
#                    focused_interaction, breaks, avg_fatigue
#             FROM daily_summary
#             WHERE date = ?
#         """, (date_str,))
#         row = c.fetchone()
#         conn.close()
#         return row

#     # ---------------------------------------------------------
#     # SETTINGS / PERSONALIZATION
#     # ---------------------------------------------------------
#     def get_personalization(self, key):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("SELECT value FROM personalization WHERE key = ?", (key,))
#         row = c.fetchone()
#         conn.close()
#         return row[0] if row else None

#     def get_setting(self, key):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("SELECT value FROM settings WHERE key = ?", (key,))
#         row = c.fetchone()
#         conn.close()
#         return json.loads(row[0]) if row else None
#     # ---------------------------------------------------------
#     # AGGREGATION HELPERS (DAY-LEVEL)
#     # ---------------------------------------------------------
#     def _day_bounds_iso(self, date_str):
#         start_dt = datetime.strptime(date_str, "%Y-%m-%d")
#         end_dt = start_dt + timedelta(days=1)
#         return start_dt.isoformat(), end_dt.isoformat()

#     def get_behavior_for_day(self, date_str):
#         start_dt = datetime.strptime(date_str, "%Y-%m-%d")
#         end_dt = start_dt + timedelta(days=1)

#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, behavior, fatigue_at_event, mode
#             FROM behavior_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_breaks_for_day(self, date_str):
#         start_dt = datetime.strptime(date_str, "%Y-%m-%d")
#         end_dt = start_dt + timedelta(days=1)

#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, reason, behavior, fatigue, mode
#             FROM break_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     # ---------------------------------------------------------
#     # RANGE HELPERS FOR ANALYTICS ENGINE
#     # ---------------------------------------------------------
#     def get_behavior_events(self, start_dt: datetime, end_dt: datetime):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, behavior, duration, fatigue_at_event, mode
#             FROM behavior_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_fatigue_events(self, start_dt: datetime, end_dt: datetime):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, fatigue, mode
#             FROM fatigue_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_break_events(self, start_dt: datetime, end_dt: datetime):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, reason, behavior, fatigue, interval_used, timing_quality, mode
#             FROM break_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_suppression_events(self, start_dt: datetime, end_dt: datetime):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, type, is_away_reset, mode
#             FROM suppression_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_input_activity_events(self, start_dt: datetime, end_dt: datetime):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, window, typing, mouse, scroll
#             FROM input_activity_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows















# 1st update on 17th March
# # core/storage_manager.py

# import os
# import sqlite3
# import json
# from datetime import datetime, date, timedelta
# from pathlib import Path


# class StorageManager:
#     """
#     Premium local storage engine (SQLite) with mode support.
#     - behavior_log (mode-tagged)
#     - fatigue_log (mode-tagged)
#     - break_log (mode-tagged)
#     - suppression_log (mode-tagged)
#     - input_activity_log (legacy Smart Mode)
#     - learning_profile (per-user adaptive AI parameters)
#     """

#     def __init__(self):
#         self.db_path = self._get_db_path()
#         self._ensure_database()
#         self._run_migrations()

#     # ---------------------------------------------------------
#     # PATHS
#     # ---------------------------------------------------------
#     def _get_db_path(self):
#         appdata = Path(os.getenv("APPDATA"))
#         folder = appdata / "YourApp"
#         folder.mkdir(exist_ok=True)
#         return folder / "user_data.db"

#     def _connect(self):
#         return sqlite3.connect(self.db_path)

#     # ---------------------------------------------------------
#     # DATABASE INIT
#     # ---------------------------------------------------------
#     def _ensure_database(self):
#         conn = self._connect()
#         c = conn.cursor()

#         # Behavior log
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS behavior_log (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 behavior TEXT NOT NULL,
#                 duration INTEGER,
#                 fatigue_at_event REAL,
#                 mode TEXT DEFAULT 'ai'
#             )
#         """)

#         # Fatigue log
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS fatigue_log (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 fatigue REAL NOT NULL,
#                 mode TEXT DEFAULT 'ai'
#             )
#         """)

#         # Break log
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS break_log (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 reason TEXT NOT NULL,
#                 behavior TEXT,
#                 fatigue REAL,
#                 interval_used REAL,
#                 timing_quality TEXT,
#                 mode TEXT DEFAULT 'ai'
#             )
#         """)

#         # Suppression log
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS suppression_log (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 type TEXT NOT NULL,
#                 is_away_reset INTEGER NOT NULL,
#                 mode TEXT DEFAULT 'ai'
#             )
#         """)

#         # Input activity log (legacy Smart Mode)
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS input_activity_log (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 window TEXT,
#                 typing REAL,
#                 mouse REAL,
#                 scroll REAL
#             )
#         """)

#         # Daily summary (clean schema)
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS daily_summary (
#                 date TEXT PRIMARY KEY,
#                 total_focus INTEGER,
#                 deep_work INTEGER,
#                 deep_reading INTEGER,
#                 focused_interaction INTEGER,
#                 breaks INTEGER,
#                 avg_fatigue REAL
#             )
#         """)

#         # Learning profile (single row, id=1)
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS learning_profile (
#                 id INTEGER PRIMARY KEY CHECK (id = 1),
#                 preferred_focus_minutes REAL,
#                 break_acceptance_rate REAL,
#                 fatigue_rise_multiplier REAL,
#                 fatigue_recovery_multiplier REAL,
#                 night_owl_score REAL
#             )
#         """)

#         # Ensure there is always exactly one row
#         c.execute("SELECT id FROM learning_profile WHERE id = 1")
#         row = c.fetchone()
#         if row is None:
#             c.execute("""
#                 INSERT INTO learning_profile
#                 (id, preferred_focus_minutes, break_acceptance_rate,
#                  fatigue_rise_multiplier, fatigue_recovery_multiplier, night_owl_score)
#                 VALUES (1, ?, ?, ?, ?, ?)
#             """, (
#                 20.0,   # preferred_focus_minutes default
#                 0.5,    # break_acceptance_rate default
#                 1.0,    # fatigue_rise_multiplier default
#                 1.0,    # fatigue_recovery_multiplier default
#                 0.5,    # night_owl_score default
#             ))

#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # MIGRATIONS
#     # ---------------------------------------------------------
#     def _run_migrations(self):
#         conn = self._connect()
#         c = conn.cursor()

#         # Ensure mode column exists on logs (for older DBs)
#         c.execute("PRAGMA table_info(behavior_log)")
#         cols = [col[1] for col in c.fetchall()]
#         if "mode" not in cols:
#             c.execute("ALTER TABLE behavior_log ADD COLUMN mode TEXT DEFAULT 'ai'")

#         c.execute("PRAGMA table_info(fatigue_log)")
#         cols = [col[1] for col in c.fetchall()]
#         if "mode" not in cols:
#             c.execute("ALTER TABLE fatigue_log ADD COLUMN mode TEXT DEFAULT 'ai'")

#         c.execute("PRAGMA table_info(break_log)")
#         cols = [col[1] for col in c.fetchall()]
#         if "mode" not in cols:
#             c.execute("ALTER TABLE break_log ADD COLUMN mode TEXT DEFAULT 'ai'")

#         c.execute("PRAGMA table_info(suppression_log)")
#         cols = [col[1] for col in c.fetchall()]
#         if "mode" not in cols:
#             c.execute("ALTER TABLE suppression_log ADD COLUMN mode TEXT DEFAULT 'ai'")

#         # Ensure daily_summary has correct columns
#         c.execute("PRAGMA table_info(daily_summary)")
#         cols = [col[1] for col in c.fetchall()]
#         required = [
#             "date", "total_focus", "deep_work", "deep_reading",
#             "focused_interaction", "breaks", "avg_fatigue"
#         ]
#         for col in required:
#             if col not in cols:
#                 c.execute(f"ALTER TABLE daily_summary ADD COLUMN {col} TEXT")

#         # Ensure learning_profile has all columns (for future migrations)
#         c.execute("PRAGMA table_info(learning_profile)")
#         cols = [col[1] for col in c.fetchall()]
#         lp_required = [
#             "preferred_focus_minutes",
#             "break_acceptance_rate",
#             "fatigue_rise_multiplier",
#             "fatigue_recovery_multiplier",
#             "night_owl_score",
#         ]
#         for col in lp_required:
#             if col not in cols:
#                 c.execute(f"ALTER TABLE learning_profile ADD COLUMN {col} REAL")

#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # LEGACY SMART MODE LOGGING
#     # ---------------------------------------------------------
#     def log_behavior(self, behavior, fatigue, window, typing, mouse, scroll):
#         """
#         Legacy Smart Mode logging: behavior_log + input_activity_log.
#         """
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()

#         c.execute("""
#             INSERT INTO behavior_log (timestamp, behavior, duration, fatigue_at_event, mode)
#             VALUES (?, ?, ?, ?, ?)
#         """, (now, behavior, None, fatigue, "smart"))

#         c.execute("""
#             INSERT INTO input_activity_log (timestamp, window, typing, mouse, scroll)
#             VALUES (?, ?, ?, ?, ?)
#         """, (now, window, typing, mouse, scroll))

#         conn.commit()
#         conn.close()

#     def log_fatigue(self, fatigue):
#         """
#         Legacy Smart Mode fatigue logging.
#         """
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO fatigue_log (timestamp, fatigue, mode)
#             VALUES (?, ?, ?)
#         """, (now, float(fatigue), "smart"))
#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # BREAK LOGGING (shared)
#     # ---------------------------------------------------------
#     def log_break(self, reason, behavior, fatigue, interval_used, mode="ai"):
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO break_log (timestamp, reason, behavior, fatigue, interval_used, timing_quality, mode)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (now, reason, behavior, fatigue, interval_used, "on_time", mode))
#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # NEW CLEAN LOGGING FOR AI MODE + SMART MODE
#     # ---------------------------------------------------------
#     def log_behavior_event(self, behavior, fatigue, mode):
#         """
#         Unified behavior event logging (AI + Smart).
#         """
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO behavior_log (timestamp, behavior, duration, fatigue_at_event, mode)
#             VALUES (?, ?, ?, ?, ?)
#         """, (now, behavior, None, fatigue, mode))
#         conn.commit()
#         conn.close()

#     def log_fatigue_event(self, fatigue, mode):
#         """
#         Unified fatigue event logging (AI + Smart).
#         """
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO fatigue_log (timestamp, fatigue, mode)
#             VALUES (?, ?, ?)
#         """, (now, float(fatigue), mode))
#         conn.commit()
#         conn.close()

#     def log_away_event(self, mode):
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO suppression_log (timestamp, type, is_away_reset, mode)
#             VALUES (?, ?, ?, ?)
#         """, (now, "away", 1, mode))
#         conn.commit()
#         conn.close()

#     def log_suppression_event(self, type, mode):
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO suppression_log (timestamp, type, is_away_reset, mode)
#             VALUES (?, ?, ?, ?)
#         """, (now, type, 0, mode))
#         conn.commit()
#         conn.close()

#     def log_input_activity_event(self, typing, mouse, scroll, behavior, mode):
#         """
#         Unified input activity logging (for analytics / ML).
#         """
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO input_activity_log (timestamp, window, typing, mouse, scroll)
#             VALUES (?, ?, ?, ?, ?)
#         """, (now, behavior, typing, mouse, scroll))
#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # DAILY SUMMARY
#     # ---------------------------------------------------------
#     def save_daily_summary(self, summary):
#         conn = self._connect()
#         c = conn.cursor()

#         c.execute("""
#             INSERT OR REPLACE INTO daily_summary
#             (date, total_focus, deep_work, deep_reading,
#              focused_interaction, breaks, avg_fatigue)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (
#             summary["date"],
#             summary["total_focus"],
#             summary["deep_work"],
#             summary["deep_reading"],
#             summary["focused_interaction"],
#             summary["breaks"],
#             summary["avg_fatigue"]
#         ))

#         conn.commit()
#         conn.close()

#     def get_daily_summary(self, date_str):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT date, total_focus, deep_work, deep_reading,
#                    focused_interaction, breaks, avg_fatigue
#             FROM daily_summary
#             WHERE date = ?
#         """, (date_str,))
#         row = c.fetchone()
#         conn.close()
#         return row

#     # ---------------------------------------------------------
#     # SETTINGS / PERSONALIZATION
#     # ---------------------------------------------------------
#     def get_personalization(self, key):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("SELECT value FROM personalization WHERE key = ?", (key,))
#         row = c.fetchone()
#         conn.close()
#         return row[0] if row else None

#     def get_setting(self, key):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("SELECT value FROM settings WHERE key = ?", (key,))
#         row = c.fetchone()
#         conn.close()
#         return json.loads(row[0]) if row else None

#     # ---------------------------------------------------------
#     # LEARNING PROFILE HELPERS
#     # ---------------------------------------------------------
#     def get_learning_profile(self):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT preferred_focus_minutes,
#                    break_acceptance_rate,
#                    fatigue_rise_multiplier,
#                    fatigue_recovery_multiplier,
#                    night_owl_score
#             FROM learning_profile
#             WHERE id = 1
#         """)
#         row = c.fetchone()
#         conn.close()

#         if not row:
#             # Fallback defaults (should not happen because we seed row)
#             return {
#                 "preferred_focus_minutes": 20.0,
#                 "break_acceptance_rate": 0.5,
#                 "fatigue_rise_multiplier": 1.0,
#                 "fatigue_recovery_multiplier": 1.0,
#                 "night_owl_score": 0.5,
#             }

#         return {
#             "preferred_focus_minutes": row[0] if row[0] is not None else 20.0,
#             "break_acceptance_rate": row[1] if row[1] is not None else 0.5,
#             "fatigue_rise_multiplier": row[2] if row[2] is not None else 1.0,
#             "fatigue_recovery_multiplier": row[3] if row[3] is not None else 1.0,
#             "night_owl_score": row[4] if row[4] is not None else 0.5,
#         }

#     def update_learning_profile(self, **kwargs):
#         if not kwargs:
#             return
#         conn = self._connect()
#         c = conn.cursor()

#         sets = []
#         values = []
#         for key, value in kwargs.items():
#             sets.append(f"{key} = ?")
#             values.append(float(value))
#         values.append(1)  # id = 1

#         sql = f"UPDATE learning_profile SET {', '.join(sets)} WHERE id = ?"
#         c.execute(sql, values)
#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # AGGREGATION HELPERS (DAY-LEVEL)
#     # ---------------------------------------------------------
#     def _day_bounds_iso(self, date_str):
#         start_dt = datetime.strptime(date_str, "%Y-%m-%d")
#         end_dt = start_dt + timedelta(days=1)
#         return start_dt.isoformat(), end_dt.isoformat()

#     def get_behavior_for_day(self, date_str):
#         start_dt = datetime.strptime(date_str, "%Y-%m-%d")
#         end_dt = start_dt + timedelta(days=1)

#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, behavior, fatigue_at_event, mode
#             FROM behavior_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_breaks_for_day(self, date_str):
#         start_dt = datetime.strptime(date_str, "%Y-%m-%d")
#         end_dt = start_dt + timedelta(days=1)

#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, reason, behavior, fatigue, mode
#             FROM break_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     # ---------------------------------------------------------
#     # RANGE HELPERS FOR ANALYTICS ENGINE
#     # ---------------------------------------------------------
#     def get_behavior_events(self, start_dt: datetime, end_dt: datetime):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, behavior, duration, fatigue_at_event, mode
#             FROM behavior_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_fatigue_events(self, start_dt: datetime, end_dt: datetime):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, fatigue, mode
#             FROM fatigue_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_break_events(self, start_dt: datetime, end_dt: datetime):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, reason, behavior, fatigue, interval_used, timing_quality, mode
#             FROM break_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_suppression_events(self, start_dt: datetime, end_dt: datetime):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, type, is_away_reset, mode
#             FROM suppression_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_input_activity_events(self, start_dt: datetime, end_dt: datetime):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, window, typing, mouse, scroll
#             FROM input_activity_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows













# # 2nd update on 17th March

# # core/storage_manager.py

# import os
# import sqlite3
# import json
# from datetime import datetime, date, timedelta
# from pathlib import Path


# class StorageManager:
#     """
#     Premium local storage engine (SQLite) with mode support.
#     - behavior_log (mode-tagged)
#     - fatigue_log (mode-tagged)
#     - break_log (mode-tagged)
#     - suppression_log (mode-tagged)
#     - input_activity_log (legacy Smart Mode)
#     - learning_profile (per-user adaptive AI parameters)
#     """

#     def __init__(self):
#         self.db_path = self._get_db_path()
#         self._ensure_database()
#         self._run_migrations()

#     # ---------------------------------------------------------
#     # PATHS
#     # ---------------------------------------------------------
#     def _get_db_path(self):
#         appdata = Path(os.getenv("APPDATA"))
#         folder = appdata / "YourApp"
#         folder.mkdir(exist_ok=True)
#         return folder / "user_data.db"

#     def _connect(self):
#         return sqlite3.connect(self.db_path)

#     # ---------------------------------------------------------
#     # DATABASE INIT
#     # ---------------------------------------------------------
#     def _ensure_database(self):
#         conn = self._connect()
#         c = conn.cursor()

#         # Behavior log
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS behavior_log (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 behavior TEXT NOT NULL,
#                 duration INTEGER,
#                 fatigue_at_event REAL,
#                 mode TEXT DEFAULT 'ai'
#             )
#         """)

#         # Fatigue log
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS fatigue_log (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 fatigue REAL NOT NULL,
#                 mode TEXT DEFAULT 'ai'
#             )
#         """)

#         # Break log
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS break_log (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 reason TEXT NOT NULL,
#                 behavior TEXT,
#                 fatigue REAL,
#                 interval_used REAL,
#                 timing_quality TEXT,
#                 mode TEXT DEFAULT 'ai'
#             )
#         """)

#         # Suppression log
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS suppression_log (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 type TEXT NOT NULL,
#                 is_away_reset INTEGER NOT NULL,
#                 mode TEXT DEFAULT 'ai'
#             )
#         """)

#         # Input activity log (legacy Smart Mode)
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS input_activity_log (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 timestamp TEXT NOT NULL,
#                 window TEXT,
#                 typing REAL,
#                 mouse REAL,
#                 scroll REAL
#             )
#         """)

#         # Daily summary (clean schema)
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS daily_summary (
#                 date TEXT PRIMARY KEY,
#                 total_focus INTEGER,
#                 deep_work INTEGER,
#                 deep_reading INTEGER,
#                 focused_interaction INTEGER,
#                 breaks INTEGER,
#                 avg_fatigue REAL
#             )
#         """)

#         # Learning profile (single row, id=1)
#         c.execute("""
#             CREATE TABLE IF NOT EXISTS learning_profile (
#                 id INTEGER PRIMARY KEY CHECK (id = 1),
#                 preferred_focus_minutes REAL,
#                 break_acceptance_rate REAL,
#                 fatigue_rise_multiplier REAL,
#                 fatigue_recovery_multiplier REAL,
#                 night_owl_score REAL
#             )
#         """)

#         # Ensure there is always exactly one row
#         c.execute("SELECT id FROM learning_profile WHERE id = 1")
#         row = c.fetchone()
#         if row is None:
#             c.execute("""
#                 INSERT INTO learning_profile
#                 (id, preferred_focus_minutes, break_acceptance_rate,
#                  fatigue_rise_multiplier, fatigue_recovery_multiplier, night_owl_score)
#                 VALUES (1, ?, ?, ?, ?, ?)
#             """, (
#                 20.0,   # preferred_focus_minutes default
#                 0.5,    # break_acceptance_rate default
#                 1.0,    # fatigue_rise_multiplier default
#                 1.0,    # fatigue_recovery_multiplier default
#                 0.5,    # night_owl_score default
#             ))

#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # MIGRATIONS
#     # ---------------------------------------------------------
#     def _run_migrations(self):
#         conn = self._connect()
#         c = conn.cursor()

#         # Ensure mode column exists on logs (for older DBs)
#         c.execute("PRAGMA table_info(behavior_log)")
#         cols = [col[1] for col in c.fetchall()]
#         if "mode" not in cols:
#             c.execute("ALTER TABLE behavior_log ADD COLUMN mode TEXT DEFAULT 'ai'")

#         c.execute("PRAGMA table_info(fatigue_log)")
#         cols = [col[1] for col in c.fetchall()]
#         if "mode" not in cols:
#             c.execute("ALTER TABLE fatigue_log ADD COLUMN mode TEXT DEFAULT 'ai'")

#         c.execute("PRAGMA table_info(break_log)")
#         cols = [col[1] for col in c.fetchall()]
#         if "mode" not in cols:
#             c.execute("ALTER TABLE break_log ADD COLUMN mode TEXT DEFAULT 'ai'")

#         c.execute("PRAGMA table_info(suppression_log)")
#         cols = [col[1] for col in c.fetchall()]
#         if "mode" not in cols:
#             c.execute("ALTER TABLE suppression_log ADD COLUMN mode TEXT DEFAULT 'ai'")

#         # Ensure daily_summary has correct columns
#         c.execute("PRAGMA table_info(daily_summary)")
#         cols = [col[1] for col in c.fetchall()]
#         required = [
#             "date", "total_focus", "deep_work", "deep_reading",
#             "focused_interaction", "breaks", "avg_fatigue"
#         ]
#         for col in required:
#             if col not in cols:
#                 c.execute(f"ALTER TABLE daily_summary ADD COLUMN {col} TEXT")

#         # Ensure learning_profile has all columns (for future migrations)
#         c.execute("PRAGMA table_info(learning_profile)")
#         cols = [col[1] for col in c.fetchall()]
#         lp_required = [
#             "preferred_focus_minutes",
#             "break_acceptance_rate",
#             "fatigue_rise_multiplier",
#             "fatigue_recovery_multiplier",
#             "night_owl_score",
#         ]
#         for col in lp_required:
#             if col not in cols:
#                 c.execute(f"ALTER TABLE learning_profile ADD COLUMN {col} REAL")

#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # LEGACY SMART MODE LOGGING
#     # ---------------------------------------------------------
#     def log_behavior(self, behavior, fatigue, window, typing, mouse, scroll):
#         """
#         Legacy Smart Mode logging: behavior_log + input_activity_log.
#         """
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()

#         c.execute("""
#             INSERT INTO behavior_log (timestamp, behavior, duration, fatigue_at_event, mode)
#             VALUES (?, ?, ?, ?, ?)
#         """, (now, behavior, None, fatigue, "smart"))

#         c.execute("""
#             INSERT INTO input_activity_log (timestamp, window, typing, mouse, scroll)
#             VALUES (?, ?, ?, ?, ?)
#         """, (now, window, typing, mouse, scroll))

#         conn.commit()
#         conn.close()

#     def log_fatigue(self, fatigue):
#         """
#         Legacy Smart Mode fatigue logging.
#         """
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO fatigue_log (timestamp, fatigue, mode)
#             VALUES (?, ?, ?)
#         """, (now, float(fatigue), "smart"))
#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # BREAK LOGGING (shared)
#     # ---------------------------------------------------------
#     def log_break(self, reason, behavior, fatigue, interval_used, mode="ai"):
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO break_log (timestamp, reason, behavior, fatigue, interval_used, timing_quality, mode)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (now, reason, behavior, fatigue, interval_used, "on_time", mode))
#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # NEW CLEAN LOGGING FOR AI MODE + SMART MODE
#     # ---------------------------------------------------------
#     def log_behavior_event(self, behavior, fatigue, mode):
#         """
#         Unified behavior event logging (AI + Smart).
#         """
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO behavior_log (timestamp, behavior, duration, fatigue_at_event, mode)
#             VALUES (?, ?, ?, ?, ?)
#         """, (now, behavior, None, fatigue, mode))
#         conn.commit()
#         conn.close()

#     def log_fatigue_event(self, fatigue, mode):
#         """
#         Unified fatigue event logging (AI + Smart).
#         """
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO fatigue_log (timestamp, fatigue, mode)
#             VALUES (?, ?, ?)
#         """, (now, float(fatigue), mode))
#         conn.commit()
#         conn.close()

#     def log_away_event(self, mode):
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO suppression_log (timestamp, type, is_away_reset, mode)
#             VALUES (?, ?, ?, ?)
#         """, (now, "away", 1, mode))
#         conn.commit()
#         conn.close()

#     def log_suppression_event(self, type, mode):
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO suppression_log (timestamp, type, is_away_reset, mode)
#             VALUES (?, ?, ?, ?)
#         """, (now, type, 0, mode))
#         conn.commit()
#         conn.close()

#     def log_input_activity_event(self, typing, mouse, scroll, behavior, mode):
#         """
#         Unified input activity logging (for analytics / ML).
#         """
#         now = datetime.now().isoformat()
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             INSERT INTO input_activity_log (timestamp, window, typing, mouse, scroll)
#             VALUES (?, ?, ?, ?, ?)
#         """, (now, behavior, typing, mouse, scroll))
#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # DAILY SUMMARY
#     # ---------------------------------------------------------
#     def save_daily_summary(self, summary):
#         conn = self._connect()
#         c = conn.cursor()

#         c.execute("""
#             INSERT OR REPLACE INTO daily_summary
#             (date, total_focus, deep_work, deep_reading,
#              focused_interaction, breaks, avg_fatigue)
#             VALUES (?, ?, ?, ?, ?, ?, ?)
#         """, (
#             summary["date"],
#             summary["total_focus"],
#             summary["deep_work"],
#             summary["deep_reading"],
#             summary["focused_interaction"],
#             summary["breaks"],
#             summary["avg_fatigue"]
#         ))

#         conn.commit()
#         conn.close()

#     def get_daily_summary(self, date_str):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT date, total_focus, deep_work, deep_reading,
#                    focused_interaction, breaks, avg_fatigue
#             FROM daily_summary
#             WHERE date = ?
#         """, (date_str,))
#         row = c.fetchone()
#         conn.close()
#         return row

#     # ---------------------------------------------------------
#     # SETTINGS / PERSONALIZATION
#     # ---------------------------------------------------------
#     def get_personalization(self, key):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("SELECT value FROM personalization WHERE key = ?", (key,))
#         row = c.fetchone()
#         conn.close()
#         return row[0] if row else None

#     def get_setting(self, key):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("SELECT value FROM settings WHERE key = ?", (key,))
#         row = c.fetchone()
#         conn.close()
#         return json.loads(row[0]) if row else None

#     # ---------------------------------------------------------
#     # LEARNING PROFILE HELPERS
#     # ---------------------------------------------------------
#     def get_learning_profile(self):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT preferred_focus_minutes,
#                    break_acceptance_rate,
#                    fatigue_rise_multiplier,
#                    fatigue_recovery_multiplier,
#                    night_owl_score
#             FROM learning_profile
#             WHERE id = 1
#         """)
#         row = c.fetchone()
#         conn.close()

#         if not row:
#             return {
#                 "preferred_focus_minutes": 20.0,
#                 "break_acceptance_rate": 0.5,
#                 "fatigue_rise_multiplier": 1.0,
#                 "fatigue_recovery_multiplier": 1.0,
#                 "night_owl_score": 0.5,
#             }

#         return {
#             "preferred_focus_minutes": row[0] if row[0] is not None else 20.0,
#             "break_acceptance_rate": row[1] if row[1] is not None else 0.5,
#             "fatigue_rise_multiplier": row[2] if row[2] is not None else 1.0,
#             "fatigue_recovery_multiplier": row[3] if row[3] is not None else 1.0,
#             "night_owl_score": row[4] if row[4] is not None else 0.5,
#         }

#     def update_learning_profile(self, **kwargs):
#         if not kwargs:
#             return
#         conn = self._connect()
#         c = conn.cursor()

#         sets = []
#         values = []
#         for key, value in kwargs.items():
#             sets.append(f"{key} = ?")
#             values.append(float(value))
#         values.append(1)  # id = 1

#         sql = f"UPDATE learning_profile SET {', '.join(sets)} WHERE id = ?"
#         c.execute(sql, values)
#         conn.commit()
#         conn.close()

#     # ---------------------------------------------------------
#     # AGGREGATION HELPERS (DAY-LEVEL)
#     # ---------------------------------------------------------
#     def _day_bounds_iso(self, date_str):
#         start_dt = datetime.strptime(date_str, "%Y-%m-%d")
#         end_dt = start_dt + timedelta(days=1)
#         return start_dt.isoformat(), end_dt.isoformat()

#     def get_behavior_for_day(self, date_str):
#         start_dt = datetime.strptime(date_str, "%Y-%m-%d")
#         end_dt = start_dt + timedelta(days=1)

#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, behavior, fatigue_at_event, mode
#             FROM behavior_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_breaks_for_day(self, date_str):
#         start_dt = datetime.strptime(date_str, "%Y-%m-%d")
#         end_dt = start_dt + timedelta(days=1)

#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, reason, behavior, fatigue, mode
#             FROM break_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     # ---------------------------------------------------------
#     # RANGE HELPERS FOR ANALYTICS ENGINE
#     # ---------------------------------------------------------
#     def get_behavior_events(self, start_dt: datetime, end_dt: datetime):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, behavior, duration, fatigue_at_event, mode
#             FROM behavior_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_fatigue_events(self, start_dt: datetime, end_dt: datetime):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, fatigue, mode
#             FROM fatigue_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_break_events(self, start_dt: datetime, end_dt: datetime):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, reason, behavior, fatigue, interval_used, timing_quality, mode
#             FROM break_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_suppression_events(self, start_dt: datetime, end_dt: datetime):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, type, is_away_reset, mode
#             FROM suppression_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows

#     def get_input_activity_events(self, start_dt: datetime, end_dt: datetime):
#         conn = self._connect()
#         c = conn.cursor()
#         c.execute("""
#             SELECT timestamp, window, typing, mouse, scroll
#             FROM input_activity_log
#             WHERE timestamp BETWEEN ? AND ?
#             ORDER BY timestamp ASC
#         """, (start_dt.isoformat(), end_dt.isoformat()))
#         rows = c.fetchall()
#         conn.close()
#         return rows









#MacOS version

# core/storage_manager.py

import os
import sqlite3
import json
import platform
from datetime import datetime, date, timedelta
from pathlib import Path


class StorageManager:
    """
    Premium local storage engine (SQLite) with mode support.
    - behavior_log (mode-tagged)
    - fatigue_log (mode-tagged)
    - break_log (mode-tagged)
    - suppression_log (mode-tagged)
    - input_activity_log (legacy Smart Mode)
    - learning_profile (per-user adaptive AI parameters)
    """

    def __init__(self):
        self.db_path = self._get_db_path()
        self._ensure_database()
        self._run_migrations()

    # ---------------------------------------------------------
    # PATHS (Updated for macOS Compatibility)
    # ---------------------------------------------------------
    def _get_db_path(self):
        """
        Determines the database location based on the Operating System.
        """
        if platform.system() == "Windows":
            # Windows: C:\Users\Name\AppData\Roaming
            base_dir = Path(os.getenv("APPDATA", os.path.expanduser("~")))
        elif platform.system() == "Darwin":
            # macOS: /Users/Name/Library/Application Support
            base_dir = Path(os.path.expanduser("~/Library/Application Support"))
        else:
            # Linux/Others: Home folder
            base_dir = Path(os.path.expanduser("~"))

        folder = base_dir / "K-Mends"
        folder.mkdir(parents=True, exist_ok=True)
        return folder / "user_data.db"

    def _connect(self):
        return sqlite3.connect(self.db_path)

    # ---------------------------------------------------------
    # DATABASE INIT
    # ---------------------------------------------------------
    def _ensure_database(self):
        conn = self._connect()
        c = conn.cursor()

        # Behavior log
        c.execute("""
            CREATE TABLE IF NOT EXISTS behavior_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                behavior TEXT NOT NULL,
                duration INTEGER,
                fatigue_at_event REAL,
                mode TEXT DEFAULT 'ai'
            )
        """)

        # Fatigue log
        c.execute("""
            CREATE TABLE IF NOT EXISTS fatigue_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                fatigue REAL NOT NULL,
                mode TEXT DEFAULT 'ai'
            )
        """)

        # Break log
        c.execute("""
            CREATE TABLE IF NOT EXISTS break_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                reason TEXT NOT NULL,
                behavior TEXT,
                fatigue REAL,
                interval_used REAL,
                timing_quality TEXT,
                mode TEXT DEFAULT 'ai'
            )
        """)

        # Suppression log
        c.execute("""
            CREATE TABLE IF NOT EXISTS suppression_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                type TEXT NOT NULL,
                is_away_reset INTEGER NOT NULL,
                mode TEXT DEFAULT 'ai'
            )
        """)

        # Input activity log (legacy Smart Mode)
        c.execute("""
            CREATE TABLE IF NOT EXISTS input_activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                window TEXT,
                typing REAL,
                mouse REAL,
                scroll REAL
            )
        """)

        # Daily summary (clean schema)
        c.execute("""
            CREATE TABLE IF NOT EXISTS daily_summary (
                date TEXT PRIMARY KEY,
                total_focus INTEGER,
                deep_work INTEGER,
                deep_reading INTEGER,
                focused_interaction INTEGER,
                breaks INTEGER,
                avg_fatigue REAL
            )
        """)

        # Learning profile (single row, id=1)
        c.execute("""
            CREATE TABLE IF NOT EXISTS learning_profile (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                preferred_focus_minutes REAL,
                break_acceptance_rate REAL,
                fatigue_rise_multiplier REAL,
                fatigue_recovery_multiplier REAL,
                night_owl_score REAL
            )
        """)

        # Ensure there is always exactly one row
        c.execute("SELECT id FROM learning_profile WHERE id = 1")
        row = c.fetchone()
        if row is None:
            c.execute("""
                INSERT INTO learning_profile
                (id, preferred_focus_minutes, break_acceptance_rate,
                 fatigue_rise_multiplier, fatigue_recovery_multiplier, night_owl_score)
                VALUES (1, ?, ?, ?, ?, ?)
            """, (
                20.0,   # preferred_focus_minutes default
                0.5,    # break_acceptance_rate default
                1.0,    # fatigue_rise_multiplier default
                1.0,    # fatigue_recovery_multiplier default
                0.5,    # night_owl_score default
            ))

        conn.commit()
        conn.close()

    # ---------------------------------------------------------
    # MIGRATIONS
    # ---------------------------------------------------------
    def _run_migrations(self):
        conn = self._connect()
        c = conn.cursor()

        # Ensure mode column exists on logs (for older DBs)
        c.execute("PRAGMA table_info(behavior_log)")
        cols = [col[1] for col in c.fetchall()]
        if "mode" not in cols:
            c.execute("ALTER TABLE behavior_log ADD COLUMN mode TEXT DEFAULT 'ai'")

        c.execute("PRAGMA table_info(fatigue_log)")
        cols = [col[1] for col in c.fetchall()]
        if "mode" not in cols:
            c.execute("ALTER TABLE fatigue_log ADD COLUMN mode TEXT DEFAULT 'ai'")

        c.execute("PRAGMA table_info(break_log)")
        cols = [col[1] for col in c.fetchall()]
        if "mode" not in cols:
            c.execute("ALTER TABLE break_log ADD COLUMN mode TEXT DEFAULT 'ai'")

        c.execute("PRAGMA table_info(suppression_log)")
        cols = [col[1] for col in c.fetchall()]
        if "mode" not in cols:
            c.execute("ALTER TABLE suppression_log ADD COLUMN mode TEXT DEFAULT 'ai'")

        # Ensure daily_summary has correct columns
        c.execute("PRAGMA table_info(daily_summary)")
        cols = [col[1] for col in c.fetchall()]
        required = [
            "date", "total_focus", "deep_work", "deep_reading",
            "focused_interaction", "breaks", "avg_fatigue"
        ]
        for col in required:
            if col not in cols:
                c.execute(f"ALTER TABLE daily_summary ADD COLUMN {col} TEXT")

        # Ensure learning_profile has all columns (for future migrations)
        c.execute("PRAGMA table_info(learning_profile)")
        cols = [col[1] for col in c.fetchall()]
        lp_required = [
            "preferred_focus_minutes",
            "break_acceptance_rate",
            "fatigue_rise_multiplier",
            "fatigue_recovery_multiplier",
            "night_owl_score",
        ]
        for col in lp_required:
            if col not in cols:
                c.execute(f"ALTER TABLE learning_profile ADD COLUMN {col} REAL")

        conn.commit()
        conn.close()

    # ---------------------------------------------------------
    # LEGACY SMART MODE LOGGING
    # ---------------------------------------------------------
    def log_behavior(self, behavior, fatigue, window, typing, mouse, scroll):
        """
        Legacy Smart Mode logging: behavior_log + input_activity_log.
        """
        now = datetime.now().isoformat()
        conn = self._connect()
        c = conn.cursor()

        c.execute("""
            INSERT INTO behavior_log (timestamp, behavior, duration, fatigue_at_event, mode)
            VALUES (?, ?, ?, ?, ?)
        """, (now, behavior, None, fatigue, "smart"))

        c.execute("""
            INSERT INTO input_activity_log (timestamp, window, typing, mouse, scroll)
            VALUES (?, ?, ?, ?, ?)
        """, (now, window, typing, mouse, scroll))

        conn.commit()
        conn.close()

    def log_fatigue(self, fatigue):
        """
        Legacy Smart Mode fatigue logging.
        """
        now = datetime.now().isoformat()
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            INSERT INTO fatigue_log (timestamp, fatigue, mode)
            VALUES (?, ?, ?)
        """, (now, float(fatigue), "smart"))
        conn.commit()
        conn.close()

    # ---------------------------------------------------------
    # BREAK LOGGING (shared)
    # ---------------------------------------------------------
    def log_break(self, reason, behavior, fatigue, interval_used, mode="ai"):
        now = datetime.now().isoformat()
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            INSERT INTO break_log (timestamp, reason, behavior, fatigue, interval_used, timing_quality, mode)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (now, reason, behavior, fatigue, interval_used, "on_time", mode))
        conn.commit()
        conn.close()

    # ---------------------------------------------------------
    # NEW CLEAN LOGGING FOR AI MODE + SMART MODE
    # ---------------------------------------------------------
    def log_behavior_event(self, behavior, fatigue, mode):
        """
        Unified behavior event logging (AI + Smart).
        """
        now = datetime.now().isoformat()
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            INSERT INTO behavior_log (timestamp, behavior, duration, fatigue_at_event, mode)
            VALUES (?, ?, ?, ?, ?)
        """, (now, behavior, None, fatigue, mode))
        conn.commit()
        conn.close()

    def log_fatigue_event(self, fatigue, mode):
        """
        Unified fatigue event logging (AI + Smart).
        """
        now = datetime.now().isoformat()
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            INSERT INTO fatigue_log (timestamp, fatigue, mode)
            VALUES (?, ?, ?)
        """, (now, float(fatigue), mode))
        conn.commit()
        conn.close()

    def log_away_event(self, mode):
        now = datetime.now().isoformat()
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            INSERT INTO suppression_log (timestamp, type, is_away_reset, mode)
            VALUES (?, ?, ?, ?)
        """, (now, "away", 1, mode))
        conn.commit()
        conn.close()

    def log_suppression_event(self, type, mode):
        now = datetime.now().isoformat()
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            INSERT INTO suppression_log (timestamp, type, is_away_reset, mode)
            VALUES (?, ?, ?, ?)
        """, (now, type, 0, mode))
        conn.commit()
        conn.close()

    def log_input_activity_event(self, typing, mouse, scroll, behavior, mode):
        """
        Unified input activity logging (for analytics / ML).
        """
        now = datetime.now().isoformat()
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            INSERT INTO input_activity_log (timestamp, window, typing, mouse, scroll)
            VALUES (?, ?, ?, ?, ?)
        """, (now, behavior, typing, mouse, scroll))
        conn.commit()
        conn.close()

    # ---------------------------------------------------------
    # DAILY SUMMARY
    # ---------------------------------------------------------
    def save_daily_summary(self, summary):
        conn = self._connect()
        c = conn.cursor()

        c.execute("""
            INSERT OR REPLACE INTO daily_summary
            (date, total_focus, deep_work, deep_reading,
             focused_interaction, breaks, avg_fatigue)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            summary["date"],
            summary["total_focus"],
            summary["deep_work"],
            summary["deep_reading"],
            summary["focused_interaction"],
            summary["breaks"],
            summary["avg_fatigue"]
        ))

        conn.commit()
        conn.close()

    def get_daily_summary(self, date_str):
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            SELECT date, total_focus, deep_work, deep_reading,
                   focused_interaction, breaks, avg_fatigue
            FROM daily_summary
            WHERE date = ?
        """, (date_str,))
        row = c.fetchone()
        conn.close()
        return row

    # ---------------------------------------------------------
    # SETTINGS / PERSONALIZATION
    # ---------------------------------------------------------
    def get_personalization(self, key):
        conn = self._connect()
        c = conn.cursor()
        # Note: If you don't have a 'personalization' table created in _ensure_database,
        # this might need a CREATE TABLE statement there too.
        try:
            c.execute("SELECT value FROM personalization WHERE key = ?", (key,))
            row = c.fetchone()
        except sqlite3.OperationalError:
            row = None
        conn.close()
        return row[0] if row else None

    def get_setting(self, key):
        conn = self._connect()
        c = conn.cursor()
        # Note: Similar to personalization, ensure 'settings' table exists.
        try:
            c.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = c.fetchone()
        except sqlite3.OperationalError:
            row = None
        conn.close()
        return json.loads(row[0]) if row else None

    # ---------------------------------------------------------
    # LEARNING PROFILE HELPERS
    # ---------------------------------------------------------
    def get_learning_profile(self):
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            SELECT preferred_focus_minutes,
                   break_acceptance_rate,
                   fatigue_rise_multiplier,
                   fatigue_recovery_multiplier,
                   night_owl_score
            FROM learning_profile
            WHERE id = 1
        """)
        row = c.fetchone()
        conn.close()

        if not row:
            return {
                "preferred_focus_minutes": 20.0,
                "break_acceptance_rate": 0.5,
                "fatigue_rise_multiplier": 1.0,
                "fatigue_recovery_multiplier": 1.0,
                "night_owl_score": 0.5,
            }

        return {
            "preferred_focus_minutes": row[0] if row[0] is not None else 20.0,
            "break_acceptance_rate": row[1] if row[1] is not None else 0.5,
            "fatigue_rise_multiplier": row[2] if row[2] is not None else 1.0,
            "fatigue_recovery_multiplier": row[3] if row[3] is not None else 1.0,
            "night_owl_score": row[4] if row[4] is not None else 0.5,
        }

    def update_learning_profile(self, **kwargs):
        if not kwargs:
            return
        conn = self._connect()
        c = conn.cursor()

        sets = []
        values = []
        for key, value in kwargs.items():
            sets.append(f"{key} = ?")
            values.append(float(value))
        values.append(1)  # id = 1

        sql = f"UPDATE learning_profile SET {', '.join(sets)} WHERE id = ?"
        c.execute(sql, values)
        conn.commit()
        conn.close()

    # ---------------------------------------------------------
    # AGGREGATION HELPERS (DAY-LEVEL)
    # ---------------------------------------------------------
    def _day_bounds_iso(self, date_str):
        start_dt = datetime.strptime(date_str, "%Y-%m-%d")
        end_dt = start_dt + timedelta(days=1)
        return start_dt.isoformat(), end_dt.isoformat()

    def get_behavior_for_day(self, date_str):
        start_dt = datetime.strptime(date_str, "%Y-%m-%d")
        end_dt = start_dt + timedelta(days=1)

        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            SELECT timestamp, behavior, fatigue_at_event, mode
            FROM behavior_log
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp ASC
        """, (start_dt.isoformat(), end_dt.isoformat()))
        rows = c.fetchall()
        conn.close()
        return rows

    def get_breaks_for_day(self, date_str):
        start_dt = datetime.strptime(date_str, "%Y-%m-%d")
        end_dt = start_dt + timedelta(days=1)

        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            SELECT timestamp, reason, behavior, fatigue, mode
            FROM break_log
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp ASC
        """, (start_dt.isoformat(), end_dt.isoformat()))
        rows = c.fetchall()
        conn.close()
        return rows

    # ---------------------------------------------------------
    # RANGE HELPERS FOR ANALYTICS ENGINE
    # ---------------------------------------------------------
    def get_behavior_events(self, start_dt: datetime, end_dt: datetime):
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            SELECT timestamp, behavior, duration, fatigue_at_event, mode
            FROM behavior_log
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp ASC
        """, (start_dt.isoformat(), end_dt.isoformat()))
        rows = c.fetchall()
        conn.close()
        return rows

    def get_fatigue_events(self, start_dt: datetime, end_dt: datetime):
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            SELECT timestamp, fatigue, mode
            FROM fatigue_log
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp ASC
        """, (start_dt.isoformat(), end_dt.isoformat()))
        rows = c.fetchall()
        conn.close()
        return rows

    def get_break_events(self, start_dt: datetime, end_dt: datetime):
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            SELECT timestamp, reason, behavior, fatigue, interval_used, timing_quality, mode
            FROM break_log
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp ASC
        """, (start_dt.isoformat(), end_dt.isoformat()))
        rows = c.fetchall()
        conn.close()
        return rows

    def get_suppression_events(self, start_dt: datetime, end_dt: datetime):
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            SELECT timestamp, type, is_away_reset, mode
            FROM suppression_log
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp ASC
        """, (start_dt.isoformat(), end_dt.isoformat()))
        rows = c.fetchall()
        conn.close()
        return rows

    def get_input_activity_events(self, start_dt: datetime, end_dt: datetime):
        conn = self._connect()
        c = conn.cursor()
        c.execute("""
            SELECT timestamp, window, typing, mouse, scroll
            FROM input_activity_log
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp ASC
        """, (start_dt.isoformat(), end_dt.isoformat()))
        rows = c.fetchall()
        conn.close()
        return rows



    # ---------------------------------------------------------
    # RESEARCH DATA PORTABILITY (EXPORT/IMPORT)
    # ---------------------------------------------------------
    
    def export_all_data(self, path):
        """
        Exports every table in the DB to a single JSON file.
        """
        conn = self._connect()
        conn.row_factory = sqlite3.Row # Returns rows as dict-like objects
        c = conn.cursor()

        export = {}
        tables = [
            "behavior_log", "fatigue_log", "break_log", 
            "suppression_log", "input_activity_log", 
            "daily_summary", "learning_profile"
        ]

        for table in tables:
            try:
                c.execute(f"SELECT * FROM {table}")
                rows = c.fetchall()
                export[table] = [dict(row) for row in rows]
            except sqlite3.OperationalError:
                export[table] = [] # Handle case where table hasn't been created yet

        conn.close()

        with open(path, "w", encoding="utf-8") as f:
            json.dump(export, f, indent=4)

    def import_all_data(self, path):
        """
        Wipes current DB and replaces it with data from a JSON file.
        Useful for pilot recovery or researcher analysis.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        conn = self._connect()
        c = conn.cursor()

        try:
            for table, rows in data.items():
                # 1. Clear current table data
                c.execute(f"DELETE FROM {table}")

                if not rows:
                    continue

                # 2. Prepare dynamic SQL
                cols = rows[0].keys()
                col_list = ", ".join(cols)
                placeholders = ", ".join(["?"] * len(cols))
                
                # 3. Insert new data
                for row in rows:
                    values = [row[col] for col in cols]
                    c.execute(
                        f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})",
                        values
                    )
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Import failed: {e}")
            return False
        finally:
            conn.close()

    