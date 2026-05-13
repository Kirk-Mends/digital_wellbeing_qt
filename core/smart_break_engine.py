


# Trying to fix next time

# # core/smart_break_engine.py

# import time
# from dataclasses import dataclass
# from core.behavior_classifier import BehaviorClassifier
# from core.meeting_mode import MeetingMode
# from core.fatigue_model import FatiguePredictionModel
# from core.storage_manager import StorageManager


# @dataclass
# class SmartConfig:
#     base_interval: float = 20 * 60.0      # 20 minutes
#     min_interval: float = 8 * 60.0        # 8 minutes
#     max_interval: float = 45 * 60.0       # 45 minutes
#     away_threshold: float = 120.0         # 2 minutes away


# class SmartBreakEngine:
#     """
#     Premium Smart Mode (v3):
#     - Predictable, fixed-interval timer
#     - Behavior-aware, meeting-aware, entertainment-aware
#     - Fatigue-aware, posture/eye-strain aware
#     - Supports accurate countdown via next_break_seconds
#     """

#     def __init__(self, config: SmartConfig):
#         self.config = config

#         # REQUIRED for MainWindow compatibility
#         self.base_interval = config.base_interval
#         self.storage = StorageManager()
#         self.session_start = time.time()
#         self.last_break_time = time.time()
#         self.last_behavior = "Idle"
#         self.last_fatigue = 0.0

#         self.behavior_classifier = BehaviorClassifier()
#         self.meeting_mode = MeetingMode()
#         self.fatigue_model = FatiguePredictionModel()

#     def handle_sleep(self):
#         now = time.time()
#         self.session_start = now
#         self.last_break_time = now - self.config.min_interval
#         self.last_behavior = "Idle"
#         self.last_fatigue = 0.0

#     # ---------------------------------------------------------
#     # CLEAN LABELS
#     # ---------------------------------------------------------
#     def _clean_label(self, text):
#         if hasattr(text, "category"):
#             text = text.category

#         if not isinstance(text, str):
#             return "Activity"

#         cleaned = text.replace("_", " ").title()
#         if cleaned.lower() in ["unknown", ""]:
#             return "Activity"
#         return cleaned

#     def _behavior_key(self, text):
#         if hasattr(text, "category"):
#             text = text.category
#         if not isinstance(text, str):
#             return "activity"
#         return text.strip().lower().replace(" ", "_")

#     # ---------------------------------------------------------
#     # SMART MODE MESSAGES
#     # ---------------------------------------------------------
#     SMART_MESSAGES = {
#         "meeting_suppressed": "You’re in a call. Breaks will resume afterward.",
#         "watching_suppressed": "Enjoy your video. Breaks are paused while you’re watching.",
#         "gaming_suppressed": "You’re in the middle of a game. Breaks will wait for you.",
#         "away_reset": "Welcome back. Take a moment to settle in.",
#         "strain_risk": "Your eyes have been working hard. A short pause could help.",
#         "fatigue_early": "You’ve been focused for a while. A brief stretch may feel good.",
#         "interval_reached": "You’ve been going for a bit. This is a good moment to pause.",
#         "recent_break": "You just took a break recently.",
#         "not_due": "You’re good to continue.",
#     }

#     # ---------------------------------------------------------
#     # MAIN DECISION LOGIC
#     # ---------------------------------------------------------
#     def should_trigger_break(self, signals: dict) -> dict:
#         now = time.time()
#         idle = signals.get("idle_seconds", 0.0)

#         # 1. Classify behavior
#         behavior_result = self.behavior_classifier.classify(signals)
#         raw_behavior = behavior_result.category
#         behavior_key = self._behavior_key(raw_behavior)
#         clean_behavior = self._clean_label(raw_behavior)

#         # -----------------------------------------------------
#         # Compute interval + remaining time (countdown)
#         # -----------------------------------------------------
#         # Base interval with fatigue scaling
#         fatigue_score = self.fatigue_model.compute_fatigue(signals, behavior_key)
#         interval = self.config.base_interval

#         if fatigue_score > 70:
#             interval *= 0.7
#         elif fatigue_score > 50:
#             interval *= 0.85
#         elif fatigue_score < 20:
#             interval *= 1.15

#         interval = max(self.config.min_interval, min(self.config.max_interval, interval))

#         # Countdown calculation
#         elapsed_since_session = now - self.session_start
#         remaining = max(0, interval - elapsed_since_session)

#         # -----------------------------------------------------
#         # 2. Away detection (freeze countdown)
#         # -----------------------------------------------------
#         if idle > self.config.away_threshold or signals.get("screen_locked", False):
#             self.session_start = now
#             self.last_behavior = "Away"
#             self.last_fatigue = 0.0

#             return {
#                 "trigger": False,
#                 "behavior": "Away",
#                 "reason": "Away Reset",
#                 "message": self.SMART_MESSAGES["away_reset"],
#                 "fatigue_score": 0.0,
#                 "interval_used": self.config.base_interval,
#                 "next_break_seconds": self.config.base_interval
#             }

#         # -----------------------------------------------------
#         # 3. Meeting suppression (freeze countdown)
#         # -----------------------------------------------------
#         if self.meeting_mode.should_suppress_breaks(signals, behavior_key):
#             self.last_behavior = "Meeting"
#             self.last_fatigue = 0.0

#             return {
#                 "trigger": False,
#                 "behavior": "Meeting",
#                 "reason": "Meeting Suppressed",
#                 "message": self.SMART_MESSAGES["meeting_suppressed"],
#                 "fatigue_score": 0.0,
#                 "interval_used": self.config.base_interval,
#                 "next_break_seconds": self.config.base_interval
#             }

#         # -----------------------------------------------------
#         # 4. Entertainment suppression (freeze countdown)
#         # -----------------------------------------------------
#         if behavior_key in ["watching", "video"]:
#             return {
#                 "trigger": False,
#                 "behavior": "Watching",
#                 "reason": "Watching Suppressed",
#                 "message": self.SMART_MESSAGES["watching_suppressed"],
#                 "fatigue_score": 0.0,
#                 "interval_used": self.config.base_interval,
#                 "next_break_seconds": self.config.base_interval
#             }

#         if behavior_key == "gaming":
#             return {
#                 "trigger": False,
#                 "behavior": "Gaming",
#                 "reason": "Gaming Suppressed",
#                 "message": self.SMART_MESSAGES["gaming_suppressed"],
#                 "fatigue_score": 0.0,
#                 "interval_used": self.config.base_interval,
#                 "next_break_seconds": self.config.base_interval
#             }

#         # -----------------------------------------------------
#         # 5. Update last behavior/fatigue
#         # -----------------------------------------------------
#         self.last_behavior = clean_behavior
#         self.last_fatigue = fatigue_score

#         # -----------------------------------------------------
#         # 6. Minimum spacing
#         # -----------------------------------------------------
#         elapsed_since_break = now - self.last_break_time
#         if elapsed_since_break < self.config.min_interval:
#             return {
#                 "trigger": False,
#                 "behavior": clean_behavior,
#                 "reason": "Recent Break",
#                 "message": self.SMART_MESSAGES["recent_break"],
#                 "fatigue_score": fatigue_score,
#                 "interval_used": interval,
#                 "next_break_seconds": remaining
#             }

#         # -----------------------------------------------------
#         # 7. Protected states
#         # -----------------------------------------------------
#         if behavior_key in ["deep_work", "deep_reading", "focused_interaction"]:
#             if fatigue_score < 50:
#                 if elapsed_since_session >= interval:
#                     return {
#                         "trigger": False,
#                         "behavior": clean_behavior,
#                         "reason": "Not Due",
#                         "message": self.SMART_MESSAGES["not_due"],
#                         "fatigue_score": fatigue_score,
#                         "interval_used": interval,
#                         "next_break_seconds": remaining
#                     }

#         # -----------------------------------------------------
#         # 8. Hard interval reached
#         # -----------------------------------------------------
#         if elapsed_since_session >= interval:
#             self.last_break_time = now

#             self.storage.log_break(
#                 reason="Interval Reached",
#                 behavior=clean_behavior,
#                 fatigue=fatigue_score,
#                 interval_used=interval
#             )

#             return {
#                 "trigger": True,
#                 "behavior": clean_behavior,
#                 "reason": "Interval Reached",
#                 "message": self.SMART_MESSAGES["interval_reached"],
#                 "fatigue_score": fatigue_score,
#                 "interval_used": interval
#             }

#         # -----------------------------------------------------
#         # 9. Fatigue early break
#         # -----------------------------------------------------
#         if fatigue_score >= 75:
#             self.last_break_time = now

#             self.storage.log_break(
#                 reason="Fatigue Early",
#                 behavior=clean_behavior,
#                 fatigue=fatigue_score,
#                 interval_used=interval
#             )

#             return {
#                 "trigger": True,
#                 "behavior": clean_behavior,
#                 "reason": "Fatigue Early",
#                 "message": self.SMART_MESSAGES["fatigue_early"],
#                 "fatigue_score": fatigue_score,
#                 "interval_used": interval
#             }

#         # -----------------------------------------------------
#         # 10. Strain risk
#         # -----------------------------------------------------
#         if clean_behavior in ["Eye Strain Risk", "Posture Risk"]:
#             if fatigue_score >= 55:
#                 self.last_break_time = now

#                 self.storage.log_break(
#                     reason="Strain Risk",
#                     behavior=clean_behavior,
#                     fatigue=fatigue_score,
#                     interval_used=interval
#                 )

#                 return {
#                     "trigger": True,
#                     "behavior": clean_behavior,
#                     "reason": "Strain Risk",
#                     "message": self.SMART_MESSAGES["strain_risk"],
#                     "fatigue_score": fatigue_score,
#                     "interval_used": interval
#                 }

#         # -----------------------------------------------------
#         # 11. No break (normal countdown)
#         # -----------------------------------------------------
#         return {
#             "trigger": False,
#             "behavior": clean_behavior,
#             "reason": "Not Due",
#             "message": self.SMART_MESSAGES["not_due"],
#             "fatigue_score": fatigue_score,
#             "interval_used": interval,
#             "next_break_seconds": remaining
#         }

#     # ---------------------------------------------------------
#     # UPDATE WRAPPER
#     # ---------------------------------------------------------
#     def update(self, signals, dt):
#         return self.should_trigger_break(signals)

#     # ---------------------------------------------------------
#     # RESET
#     # ---------------------------------------------------------
#     def reset_after_break(self):
#         now = time.time()
#         self.session_start = now
#         self.last_break_time = now
#         self.last_behavior = "Idle"
#         self.last_fatigue = 0.0

















# I fixed idel and away so that it will restart

# # core/smart_break_engine.py

# import time
# from dataclasses import dataclass
# from core.behavior_classifier import BehaviorClassifier
# from core.meeting_mode import MeetingMode
# from core.fatigue_model import FatiguePredictionModel
# from core.storage_manager import StorageManager


# @dataclass
# class SmartConfig:
#     base_interval: float = 20 * 60.0      # 20 minutes
#     min_interval: float = 8 * 60.0        # 8 minutes
#     max_interval: float = 45 * 60.0       # 45 minutes
#     away_threshold: float = 120.0         # 2 minutes away


# class SmartBreakEngine:
#     """
#     Premium Smart Mode (v3):
#     - Predictable, fixed-interval timer
#     - Behavior-aware, meeting-aware, entertainment-aware
#     - Fatigue-aware, posture/eye-strain aware
#     - Supports accurate countdown via next_break_seconds
#     """

#     def __init__(self, config: SmartConfig):
#         self.config = config

#         # REQUIRED for MainWindow compatibility
#         self.base_interval = config.base_interval
#         self.storage = StorageManager()
#         now = time.time()
#         self.session_start = now
#         self.last_break_time = now
#         self.last_behavior = "Idle"
#         self.last_fatigue = 0.0

#         self.behavior_classifier = BehaviorClassifier()
#         self.meeting_mode = MeetingMode()
#         self.fatigue_model = FatiguePredictionModel()

#     def handle_sleep(self):
#         # Treat sleep as "away" / natural break: restart session
#         now = time.time()
#         self.session_start = now
#         self.last_break_time = now
#         self.last_behavior = "Idle"
#         self.last_fatigue = 0.0

#     # ---------------------------------------------------------
#     # CLEAN LABELS
#     # ---------------------------------------------------------
#     def _clean_label(self, text):
#         if hasattr(text, "category"):
#             text = text.category

#         if not isinstance(text, str):
#             return "Activity"

#         cleaned = text.replace("_", " ").title()
#         if cleaned.lower() in ["unknown", ""]:
#             return "Activity"
#         return cleaned

#     def _behavior_key(self, text):
#         if hasattr(text, "category"):
#             text = text.category
#         if not isinstance(text, str):
#             return "activity"
#         return text.strip().lower().replace(" ", "_")

#     # ---------------------------------------------------------
#     # SMART MODE MESSAGES
#     # ---------------------------------------------------------
#     SMART_MESSAGES = {
#         "meeting_suppressed": "You’re in a call. Breaks will resume afterward.",
#         "watching_suppressed": "Enjoy your video. Breaks are paused while you’re watching.",
#         "gaming_suppressed": "You’re in the middle of a game. Breaks will wait for you.",
#         "away_reset": "Welcome back. Take a moment to settle in.",
#         "strain_risk": "Your eyes have been working hard. A short pause could help.",
#         "fatigue_early": "You’ve been focused for a while. A brief stretch may feel good.",
#         "interval_reached": "You’ve been going for a bit. This is a good moment to pause.",
#         "recent_break": "You just took a break recently.",
#         "not_due": "You’re good to continue.",
#     }

#     # ---------------------------------------------------------
#     # MAIN DECISION LOGIC
#     # ---------------------------------------------------------
#     def should_trigger_break(self, signals: dict) -> dict:
#         now = time.time()
#         idle = signals.get("idle_seconds", 0.0)

#         # 1. Classify behavior
#         behavior_result = self.behavior_classifier.classify(signals)
#         raw_behavior = behavior_result.category
#         behavior_key = self._behavior_key(raw_behavior)
#         clean_behavior = self._clean_label(raw_behavior)

#         # 2. Compute interval (fatigue-aware, but fixed for this session)
#         fatigue_score = self.fatigue_model.compute_fatigue(signals, behavior_key)
#         interval = self.config.base_interval

#         if fatigue_score > 70:
#             interval *= 0.7
#         elif fatigue_score > 50:
#             interval *= 0.85
#         elif fatigue_score < 20:
#             interval *= 1.15

#         interval = max(self.config.min_interval, min(self.config.max_interval, interval))

#         # 3. Compute elapsed + remaining for countdown
#         elapsed_since_session = now - self.session_start
#         elapsed_since_break = now - self.last_break_time
#         remaining = max(0, interval - elapsed_since_session)

#         # -----------------------------------------------------
#         # 4. Away detection (idle / lock / sleep) = natural break
#         #    - Reset session + break time
#         #    - Freeze countdown at full interval
#         # -----------------------------------------------------
#         if idle > self.config.away_threshold or signals.get("screen_locked", False):
#             self.session_start = now
#             self.last_break_time = now
#             self.last_behavior = "Away"
#             self.last_fatigue = 0.0

#             return {
#                 "trigger": False,
#                 "behavior": "Away",
#                 "reason": "Away Reset",
#                 "message": self.SMART_MESSAGES["away_reset"],
#                 "fatigue_score": 0.0,
#                 "interval_used": self.config.base_interval,
#                 "next_break_seconds": self.config.base_interval
#             }

#         # -----------------------------------------------------
#         # 5. Meeting suppression (no reset, just suppress + freeze)
#         # -----------------------------------------------------
#         if self.meeting_mode.should_suppress_breaks(signals, behavior_key):
#             self.last_behavior = "Meeting"
#             self.last_fatigue = 0.0

#             return {
#                 "trigger": False,
#                 "behavior": "Meeting",
#                 "reason": "Meeting Suppressed",
#                 "message": self.SMART_MESSAGES["meeting_suppressed"],
#                 "fatigue_score": 0.0,
#                 "interval_used": self.config.base_interval,
#                 "next_break_seconds": self.config.base_interval
#             }

#         # -----------------------------------------------------
#         # 6. Entertainment suppression (no reset, just suppress + freeze)
#         # -----------------------------------------------------
#         if behavior_key in ["watching", "video"]:
#             return {
#                 "trigger": False,
#                 "behavior": "Watching",
#                 "reason": "Watching Suppressed",
#                 "message": self.SMART_MESSAGES["watching_suppressed"],
#                 "fatigue_score": 0.0,
#                 "interval_used": self.config.base_interval,
#                 "next_break_seconds": self.config.base_interval
#             }

#         if behavior_key == "gaming":
#             return {
#                 "trigger": False,
#                 "behavior": "Gaming",
#                 "reason": "Gaming Suppressed",
#                 "message": self.SMART_MESSAGES["gaming_suppressed"],
#                 "fatigue_score": 0.0,
#                 "interval_used": self.config.base_interval,
#                 "next_break_seconds": self.config.base_interval
#             }

#         # -----------------------------------------------------
#         # 7. Update last behavior/fatigue (active states)
#         # -----------------------------------------------------
#         self.last_behavior = clean_behavior
#         self.last_fatigue = fatigue_score

#         # -----------------------------------------------------
#         # 8. Minimum spacing after any break
#         # -----------------------------------------------------
#         if elapsed_since_break < self.config.min_interval:
#             return {
#                 "trigger": False,
#                 "behavior": clean_behavior,
#                 "reason": "Recent Break",
#                 "message": self.SMART_MESSAGES["recent_break"],
#                 "fatigue_score": fatigue_score,
#                 "interval_used": interval,
#                 "next_break_seconds": remaining
#             }

#         # -----------------------------------------------------
#         # 9. Protected states (deep work / deep reading / focused)
#         # -----------------------------------------------------
#         if behavior_key in ["deep_work", "deep_reading", "focused_interaction"]:
#             if fatigue_score < 50:
#                 if elapsed_since_session >= interval:
#                     # Protect session: no break yet, but keep countdown honest
#                     return {
#                         "trigger": False,
#                         "behavior": clean_behavior,
#                         "reason": "Not Due",
#                         "message": self.SMART_MESSAGES["not_due"],
#                         "fatigue_score": fatigue_score,
#                         "interval_used": interval,
#                         "next_break_seconds": remaining
#                     }

#         # -----------------------------------------------------
#         # 10. Hard interval reached
#         # -----------------------------------------------------
#         if elapsed_since_session >= interval:
#             self.last_break_time = now

#             self.storage.log_break(
#                 reason="Interval Reached",
#                 behavior=clean_behavior,
#                 fatigue=fatigue_score,
#                 interval_used=interval
#             )

#             return {
#                 "trigger": True,
#                 "behavior": clean_behavior,
#                 "reason": "Interval Reached",
#                 "message": self.SMART_MESSAGES["interval_reached"],
#                 "fatigue_score": fatigue_score,
#                 "interval_used": interval
#             }

#         # -----------------------------------------------------
#         # 11. Fatigue early break
#         # -----------------------------------------------------
#         if fatigue_score >= 75:
#             self.last_break_time = now

#             self.storage.log_break(
#                 reason="Fatigue Early",
#                 behavior=clean_behavior,
#                 fatigue=fatigue_score,
#                 interval_used=interval
#             )

#             return {
#                 "trigger": True,
#                 "behavior": clean_behavior,
#                 "reason": "Fatigue Early",
#                 "message": self.SMART_MESSAGES["fatigue_early"],
#                 "fatigue_score": fatigue_score,
#                 "interval_used": interval
#             }

#         # -----------------------------------------------------
#         # 12. Strain risk
#         # -----------------------------------------------------
#         if clean_behavior in ["Eye Strain Risk", "Posture Risk"]:
#             if fatigue_score >= 55:
#                 self.last_break_time = now

#                 self.storage.log_break(
#                     reason="Strain Risk",
#                     behavior=clean_behavior,
#                     fatigue=fatigue_score,
#                     interval_used=interval
#                 )

#                 return {
#                     "trigger": True,
#                     "behavior": clean_behavior,
#                     "reason": "Strain Risk",
#                     "message": self.SMART_MESSAGES["strain_risk"],
#                     "fatigue_score": fatigue_score,
#                     "interval_used": interval
#                 }

#         # -----------------------------------------------------
#         # 13. No break (normal countdown)
#         # -----------------------------------------------------
#         return {
#             "trigger": False,
#             "behavior": clean_behavior,
#             "reason": "Not Due",
#             "message": self.SMART_MESSAGES["not_due"],
#             "fatigue_score": fatigue_score,
#             "interval_used": interval,
#             "next_break_seconds": remaining
#         }

#     # ---------------------------------------------------------
#     # UPDATE WRAPPER
#     # ---------------------------------------------------------
#     def update(self, signals, dt):
#         return self.should_trigger_break(signals)

#     # ---------------------------------------------------------
#     # RESET
#     # ---------------------------------------------------------
#     def reset_after_break(self):
#         now = time.time()
#         self.session_start = now
#         self.last_break_time = now
#         self.last_behavior = "Idle"
#         self.last_fatigue = 0.0




















# I seperated the storage for analytics

# # core/smart_break_engine.py

# import time
# from dataclasses import dataclass
# from core.behavior_classifier import BehaviorClassifier
# from core.meeting_mode import MeetingMode
# from core.fatigue_model import FatiguePredictionModel
# from core.storage_manager import StorageManager


# @dataclass
# class SmartConfig:
#     base_interval: float = 20 * 60.0      # 20 minutes
#     min_interval: float = 8 * 60.0        # 8 minutes
#     max_interval: float = 45 * 60.0       # 45 minutes
#     away_threshold: float = 120.0         # 2 minutes away


# class SmartBreakEngine:
#     """
#     Premium Smart Mode (v3):
#     - Predictable, fixed-interval timer
#     - Behavior-aware, meeting-aware, entertainment-aware
#     - Fatigue-aware, posture/eye-strain aware
#     - Supports accurate countdown via next_break_seconds
#     - Now logs analytics with mode='smart'
#     """

#     def __init__(self, config: SmartConfig):
#         self.config = config

#         # REQUIRED for MainWindow compatibility
#         self.base_interval = config.base_interval
#         self.storage = StorageManager()
#         now = time.time()
#         self.session_start = now
#         self.last_break_time = now
#         self.last_behavior = "Idle"
#         self.last_fatigue = 0.0

#         self.behavior_classifier = BehaviorClassifier()
#         self.meeting_mode = MeetingMode()
#         self.fatigue_model = FatiguePredictionModel()

#     def handle_sleep(self):
#         # Treat sleep as "away" / natural break: restart session
#         now = time.time()
#         self.session_start = now
#         self.last_break_time = now
#         self.last_behavior = "Idle"
#         self.last_fatigue = 0.0

#         # Log as away-style reset for analytics
#         self.storage.log_away_event(mode="smart")

#     # ---------------------------------------------------------
#     # CLEAN LABELS
#     # ---------------------------------------------------------
#     def _clean_label(self, text):
#         if hasattr(text, "category"):
#             text = text.category

#         if not isinstance(text, str):
#             return "Activity"

#         cleaned = text.replace("_", " ").title()
#         if cleaned.lower() in ["unknown", ""]:
#             return "Activity"
#         return cleaned

#     def _behavior_key(self, text):
#         if hasattr(text, "category"):
#             text = text.category
#         if not isinstance(text, str):
#             return "activity"
#         return text.strip().lower().replace(" ", "_")

#     # ---------------------------------------------------------
#     # SMART MODE MESSAGES
#     # ---------------------------------------------------------
#     SMART_MESSAGES = {
#         "meeting_suppressed": "You’re in a call. Breaks will resume afterward.",
#         "watching_suppressed": "Enjoy your video. Breaks are paused while you’re watching.",
#         "gaming_suppressed": "You’re in the middle of a game. Breaks will wait for you.",
#         "away_reset": "Welcome back. Take a moment to settle in.",
#         "strain_risk": "Your eyes have been working hard. A short pause could help.",
#         "fatigue_early": "You’ve been focused for a while. A brief stretch may feel good.",
#         "interval_reached": "You’ve been going for a bit. This is a good moment to pause.",
#         "recent_break": "You just took a break recently.",
#         "not_due": "You’re good to continue.",
#     }
#     # ---------------------------------------------------------
#     # MAIN DECISION LOGIC
#     # ---------------------------------------------------------
#     def should_trigger_break(self, signals: dict) -> dict:
#         now = time.time()
#         idle = signals.get("idle_seconds", 0.0)

#         # 1. Classify behavior
#         behavior_result = self.behavior_classifier.classify(signals)
#         raw_behavior = behavior_result.category
#         behavior_key = self._behavior_key(raw_behavior)
#         clean_behavior = self._clean_label(raw_behavior)

#         # 2. Compute interval (fatigue-aware, but fixed for this session)
#         fatigue_score = self.fatigue_model.compute_fatigue(signals, behavior_key)
#         interval = self.config.base_interval

#         if fatigue_score > 70:
#             interval *= 0.7
#         elif fatigue_score > 50:
#             interval *= 0.85
#         elif fatigue_score < 20:
#             interval *= 1.15

#         interval = max(self.config.min_interval, min(self.config.max_interval, interval))

#         # 3. Compute elapsed + remaining for countdown
#         elapsed_since_session = now - self.session_start
#         elapsed_since_break = now - self.last_break_time
#         remaining = max(0, interval - elapsed_since_session)

#         # -----------------------------------------------------
#         # 4. Away detection (idle / lock / sleep) = natural break
#         #    - Reset session + break time
#         #    - Freeze countdown at full interval
#         # -----------------------------------------------------
#         if idle > self.config.away_threshold or signals.get("screen_locked", False):
#             self.session_start = now
#             self.last_break_time = now
#             self.last_behavior = "Away"
#             self.last_fatigue = 0.0

#             # Log away reset for Smart Mode
#             self.storage.log_away_event(mode="smart")

#             return {
#                 "trigger": False,
#                 "behavior": "Away",
#                 "reason": "Away Reset",
#                 "message": self.SMART_MESSAGES["away_reset"],
#                 "fatigue_score": 0.0,
#                 "interval_used": self.config.base_interval,
#                 "next_break_seconds": self.config.base_interval
#             }

#         # -----------------------------------------------------
#         # 5. Meeting suppression (no reset, just suppress + freeze)
#         # -----------------------------------------------------
#         if self.meeting_mode.should_suppress_breaks(signals, behavior_key):
#             self.last_behavior = "Meeting"
#             self.last_fatigue = 0.0

#             # Log meeting-based suppression for Smart Mode
#             self.storage.log_suppression_event("meeting", mode="smart")

#             return {
#                 "trigger": False,
#                 "behavior": "Meeting",
#                 "reason": "Meeting Suppressed",
#                 "message": self.SMART_MESSAGES["meeting_suppressed"],
#                 "fatigue_score": 0.0,
#                 "interval_used": self.config.base_interval,
#                 "next_break_seconds": self.config.base_interval
#             }

#         # -----------------------------------------------------
#         # 6. Entertainment suppression (no reset, just suppress + freeze)
#         # -----------------------------------------------------
#         if behavior_key in ["watching", "video"]:
#             # Log suppression as 'watching' for Smart Mode
#             self.storage.log_suppression_event("watching", mode="smart")

#             return {
#                 "trigger": False,
#                 "behavior": "Watching",
#                 "reason": "Watching Suppressed",
#                 "message": self.SMART_MESSAGES["watching_suppressed"],
#                 "fatigue_score": 0.0,
#                 "interval_used": self.config.base_interval,
#                 "next_break_seconds": self.config.base_interval
#             }

#         if behavior_key == "gaming":
#             # Log suppression as 'gaming' for Smart Mode
#             self.storage.log_suppression_event("gaming", mode="smart")

#             return {
#                 "trigger": False,
#                 "behavior": "Gaming",
#                 "reason": "Gaming Suppressed",
#                 "message": self.SMART_MESSAGES["gaming_suppressed"],
#                 "fatigue_score": 0.0,
#                 "interval_used": self.config.base_interval,
#                 "next_break_seconds": self.config.base_interval
#             }

#         # -----------------------------------------------------
#         # 7. Update last behavior/fatigue (active states)
#         #    + log behavior & fatigue for Smart Mode analytics
#         # -----------------------------------------------------
#         self.last_behavior = clean_behavior
#         self.last_fatigue = fatigue_score

#         self.storage.log_behavior_event(clean_behavior, fatigue_score, mode="smart")
#         self.storage.log_fatigue_event(fatigue_score, mode="smart")

#         # -----------------------------------------------------
#         # 8. Minimum spacing after any break
#         # -----------------------------------------------------
#         if elapsed_since_break < self.config.min_interval:
#             return {
#                 "trigger": False,
#                 "behavior": clean_behavior,
#                 "reason": "Recent Break",
#                 "message": self.SMART_MESSAGES["recent_break"],
#                 "fatigue_score": fatigue_score,
#                 "interval_used": interval,
#                 "next_break_seconds": remaining
#             }

#         # -----------------------------------------------------
#         # 9. Protected states (deep work / deep reading / focused)
#         # -----------------------------------------------------
#         if behavior_key in ["deep_work", "deep_reading", "focused_interaction"]:
#             if fatigue_score < 50:
#                 if elapsed_since_session >= interval:
#                     # Protect session: no break yet, but keep countdown honest
#                     return {
#                         "trigger": False,
#                         "behavior": clean_behavior,
#                         "reason": "Not Due",
#                         "message": self.SMART_MESSAGES["not_due"],
#                         "fatigue_score": fatigue_score,
#                         "interval_used": interval,
#                         "next_break_seconds": remaining
#                     }

#         # -----------------------------------------------------
#         # 10. Hard interval reached
#         # -----------------------------------------------------
#         if elapsed_since_session >= interval:
#             self.last_break_time = now

#             self.storage.log_break(
#                 reason="Interval Reached",
#                 behavior=clean_behavior,
#                 fatigue=fatigue_score,
#                 interval_used=interval,
#                 mode="smart"
#             )

#             return {
#                 "trigger": True,
#                 "behavior": clean_behavior,
#                 "reason": "Interval Reached",
#                 "message": self.SMART_MESSAGES["interval_reached"],
#                 "fatigue_score": fatigue_score,
#                 "interval_used": interval
#             }

#         # -----------------------------------------------------
#         # 11. Fatigue early break
#         # -----------------------------------------------------
#         if fatigue_score >= 75:
#             self.last_break_time = now

#             self.storage.log_break(
#                 reason="Fatigue Early",
#                 behavior=clean_behavior,
#                 fatigue=fatigue_score,
#                 interval_used=interval,
#                 mode="smart"
#             )

#             return {
#                 "trigger": True,
#                 "behavior": clean_behavior,
#                 "reason": "Fatigue Early",
#                 "message": self.SMART_MESSAGES["fatigue_early"],
#                 "fatigue_score": fatigue_score,
#                 "interval_used": interval
#             }

#         # -----------------------------------------------------
#         # 12. Strain risk
#         # -----------------------------------------------------
#         if clean_behavior in ["Eye Strain Risk", "Posture Risk"]:
#             if fatigue_score >= 55:
#                 self.last_break_time = now

#                 self.storage.log_break(
#                     reason="Strain Risk",
#                     behavior=clean_behavior,
#                     fatigue=fatigue_score,
#                     interval_used=interval,
#                     mode="smart"
#                 )

#                 return {
#                     "trigger": True,
#                     "behavior": clean_behavior,
#                     "reason": "Strain Risk",
#                     "message": self.SMART_MESSAGES["strain_risk"],
#                     "fatigue_score": fatigue_score,
#                     "interval_used": interval
#                 }

#         # -----------------------------------------------------
#         # 13. No break (normal countdown)
#         # -----------------------------------------------------
#         return {
#             "trigger": False,
#             "behavior": clean_behavior,
#             "reason": "Not Due",
#             "message": self.SMART_MESSAGES["not_due"],
#             "fatigue_score": fatigue_score,
#             "interval_used": interval,
#             "next_break_seconds": remaining
#         }
#     # ---------------------------------------------------------
#     # UPDATE WRAPPER
#     # ---------------------------------------------------------
#     def update(self, signals, dt):
#         return self.should_trigger_break(signals)

#     # ---------------------------------------------------------
#     # RESET
#     # ---------------------------------------------------------
#     def reset_after_break(self):
#         now = time.time()
#         self.session_start = now
#         self.last_break_time = now
#         self.last_behavior = "Idle"
#         self.last_fatigue = 0.0













# 1st update on 17th March

# core/smart_break_engine.py

import time
from dataclasses import dataclass
from core.behavior_classifier import BehaviorClassifier
from core.meeting_mode import MeetingMode
from core.fatigue_model import FatiguePredictionModel
from core.storage_manager import StorageManager


@dataclass
class SmartConfig:
    base_interval: float = 20 * 60.0      # 20 minutes
    min_interval: float = 8 * 60.0        # 8 minutes
    max_interval: float = 45 * 60.0       # 45 minutes
    away_threshold: float = 120.0         # 2 minutes away


class SmartBreakEngine:
    """
    Premium Smart Mode (v3):
    - Predictable, fixed-interval timer
    - Behavior-aware, meeting-aware, entertainment-aware
    - Fatigue-aware, posture/eye-strain aware
    - Supports accurate countdown via next_break_seconds
    - Now logs analytics with mode='smart'
    """

    def __init__(self, config: SmartConfig):
        self.config = config

        # REQUIRED for MainWindow compatibility
        self.base_interval = config.base_interval
        self.storage = StorageManager()
        now = time.time()
        self.session_start = now
        self.last_break_time = now
        self.last_behavior = "Idle"
        self.last_fatigue = 0.0

        self.behavior_classifier = BehaviorClassifier()
        self.meeting_mode = MeetingMode()
        self.fatigue_model = FatiguePredictionModel()

    def handle_sleep(self):
        # Treat sleep as "away" / natural break: restart session
        now = time.time()
        self.session_start = now
        self.last_break_time = now
        self.last_behavior = "Idle"
        self.last_fatigue = 0.0

        # Log as away-style reset for analytics
        self.storage.log_away_event(mode="smart")

    # ---------------------------------------------------------
    # CLEAN LABELS
    # ---------------------------------------------------------
    def _clean_label(self, text):
        if hasattr(text, "category"):
            text = text.category

        if not isinstance(text, str):
            return "Activity"

        cleaned = text.replace("_", " ").title()
        if cleaned.lower() in ["unknown", ""]:
            return "Activity"
        return cleaned

    def _behavior_key(self, text):
        if hasattr(text, "category"):
            text = text.category
        if not isinstance(text, str):
            return "activity"
        return text.strip().lower().replace(" ", "_")

    # ---------------------------------------------------------
    # SMART MODE MESSAGES
    # ---------------------------------------------------------
    SMART_MESSAGES = {
        "meeting_suppressed": "You’re in a call. Breaks will resume afterward.",
        "watching_suppressed": "Enjoy your video. Breaks are paused while you’re watching.",
        "gaming_suppressed": "You’re in the middle of a game. Breaks will wait for you.",
        "away_reset": "Welcome back. Take a moment to settle in.",
        "strain_risk": "Your eyes have been working hard. A short pause could help.",
        "fatigue_early": "You’ve been focused for a while. A brief stretch may feel good.",
        "interval_reached": "You’ve been going for a bit. This is a good moment to pause.",
        "recent_break": "You just took a break recently.",
        "not_due": "You’re good to continue.",
    }
    # ---------------------------------------------------------
    # MAIN DECISION LOGIC
    # ---------------------------------------------------------
    def should_trigger_break(self, signals: dict) -> dict:
        now = time.time()
        idle = signals.get("idle_seconds", 0.0)

        # 1. Classify behavior
        behavior_result = self.behavior_classifier.classify(signals)
        raw_behavior = behavior_result.category
        behavior_key = self._behavior_key(raw_behavior)
        clean_behavior = self._clean_label(raw_behavior)

        # 2. Compute interval (fatigue-aware, but fixed for this session)
        fatigue_score = self.fatigue_model.compute_fatigue(signals, behavior_key)
        interval = self.config.base_interval

        if fatigue_score > 70:
            interval *= 0.7
        elif fatigue_score > 50:
            interval *= 0.85
        elif fatigue_score < 20:
            interval *= 1.15

        interval = max(self.config.min_interval, min(self.config.max_interval, interval))

        # 3. Compute elapsed + remaining for countdown
        elapsed_since_session = now - self.session_start
        elapsed_since_break = now - self.last_break_time
        remaining = max(0, interval - elapsed_since_session)

        # -----------------------------------------------------
        # 4. Away detection (idle / lock / sleep)
        # -----------------------------------------------------
        if idle > self.config.away_threshold or signals.get("screen_locked", False):
            self.session_start = now
            self.last_break_time = now
            self.last_behavior = "Away"
            self.last_fatigue = 0.0

            self.storage.log_away_event(mode="smart")

            return {
                "trigger": False,
                "behavior": "Away",
                "reason": "Away Reset",
                "message": self.SMART_MESSAGES["away_reset"],
                "fatigue_score": 0.0,
                "interval_used": self.config.base_interval,
                "next_break_seconds": self.config.base_interval
            }

        # -----------------------------------------------------
        # 5. Meeting suppression
        # -----------------------------------------------------
        if self.meeting_mode.should_suppress_breaks(signals, behavior_key):
            self.last_behavior = "Meeting"
            self.last_fatigue = 0.0

            self.storage.log_suppression_event("meeting", mode="smart")

            return {
                "trigger": False,
                "behavior": "Meeting",
                "reason": "Meeting Suppressed",
                "message": self.SMART_MESSAGES["meeting_suppressed"],
                "fatigue_score": 0.0,
                "interval_used": self.config.base_interval,
                "next_break_seconds": self.config.base_interval
            }

        # -----------------------------------------------------
        # 6. Entertainment suppression
        # -----------------------------------------------------
        if behavior_key in ["watching", "video"]:
            self.storage.log_suppression_event("watching", mode="smart")

            return {
                "trigger": False,
                "behavior": "Watching",
                "reason": "Watching Suppressed",
                "message": self.SMART_MESSAGES["watching_suppressed"],
                "fatigue_score": 0.0,
                "interval_used": self.config.base_interval,
                "next_break_seconds": self.config.base_interval
            }

        if behavior_key == "gaming":
            self.storage.log_suppression_event("gaming", mode="smart")

            return {
                "trigger": False,
                "behavior": "Gaming",
                "reason": "Gaming Suppressed",
                "message": self.SMART_MESSAGES["gaming_suppressed"],
                "fatigue_score": 0.0,
                "interval_used": self.config.base_interval,
                "next_break_seconds": self.config.base_interval
            }

        # -----------------------------------------------------
        # 7. Log behavior, fatigue, AND input activity
        # -----------------------------------------------------
        self.last_behavior = clean_behavior
        self.last_fatigue = fatigue_score

        self.storage.log_behavior_event(clean_behavior, fatigue_score, mode="smart")
        self.storage.log_fatigue_event(fatigue_score, mode="smart")

        # NEW: Input activity logging for Smart Mode
        self.storage.log_input_activity_event(
            typing=signals.get("keypress_rate", 0.0),
            mouse=signals.get("mouse_rate", 0.0),
            scroll=signals.get("scroll_rate", 0.0),
            behavior=clean_behavior,
            mode="smart",
        )

        # -----------------------------------------------------
        # 8. Minimum spacing after break
        # -----------------------------------------------------
        if elapsed_since_break < self.config.min_interval:
            return {
                "trigger": False,
                "behavior": clean_behavior,
                "reason": "Recent Break",
                "message": self.SMART_MESSAGES["recent_break"],
                "fatigue_score": fatigue_score,
                "interval_used": interval,
                "next_break_seconds": remaining
            }
        # -----------------------------------------------------
        # 9. Protected states
        # -----------------------------------------------------
        if behavior_key in ["deep_work", "deep_reading", "focused_interaction"]:
            if fatigue_score < 50:
                if elapsed_since_session >= interval:
                    return {
                        "trigger": False,
                        "behavior": clean_behavior,
                        "reason": "Not Due",
                        "message": self.SMART_MESSAGES["not_due"],
                        "fatigue_score": fatigue_score,
                        "interval_used": interval,
                        "next_break_seconds": remaining
                    }

        # -----------------------------------------------------
        # 10. Hard interval reached
        # -----------------------------------------------------
        if elapsed_since_session >= interval:
            self.last_break_time = now

            self.storage.log_break(
                reason="Interval Reached",
                behavior=clean_behavior,
                fatigue=fatigue_score,
                interval_used=interval,
                mode="smart"
            )

            return {
                "trigger": True,
                "behavior": clean_behavior,
                "reason": "Interval Reached",
                "message": self.SMART_MESSAGES["interval_reached"],
                "fatigue_score": fatigue_score,
                "interval_used": interval
            }

        # -----------------------------------------------------
        # 11. Fatigue early break
        # -----------------------------------------------------
        if fatigue_score >= 75:
            self.last_break_time = now

            self.storage.log_break(
                reason="Fatigue Early",
                behavior=clean_behavior,
                fatigue=fatigue_score,
                interval_used=interval,
                mode="smart"
            )

            return {
                "trigger": True,
                "behavior": clean_behavior,
                "reason": "Fatigue Early",
                "message": self.SMART_MESSAGES["fatigue_early"],
                "fatigue_score": fatigue_score,
                "interval_used": interval
            }

        # -----------------------------------------------------
        # 12. Strain risk
        # -----------------------------------------------------
        if clean_behavior in ["Eye Strain Risk", "Posture Risk"]:
            if fatigue_score >= 55:
                self.last_break_time = now

                self.storage.log_break(
                    reason="Strain Risk",
                    behavior=clean_behavior,
                    fatigue=fatigue_score,
                    interval_used=interval,
                    mode="smart"
                )

                return {
                    "trigger": True,
                    "behavior": clean_behavior,
                    "reason": "Strain Risk",
                    "message": self.SMART_MESSAGES["strain_risk"],
                    "fatigue_score": fatigue_score,
                    "interval_used": interval
                }

        # -----------------------------------------------------
        # 13. No break
        # -----------------------------------------------------
        return {
            "trigger": False,
            "behavior": clean_behavior,
            "reason": "Not Due",
            "message": self.SMART_MESSAGES["not_due"],
            "fatigue_score": fatigue_score,
            "interval_used": interval,
            "next_break_seconds": remaining
        }

    # ---------------------------------------------------------
    # UPDATE WRAPPER
    # ---------------------------------------------------------
    def update(self, signals, dt):
        return self.should_trigger_break(signals)

    # ---------------------------------------------------------
    # RESET
    # ---------------------------------------------------------
    def reset_after_break(self):
        now = time.time()
        self.session_start = now
        self.last_break_time = now
        self.last_behavior = "Idle"
        self.last_fatigue = 0.0
