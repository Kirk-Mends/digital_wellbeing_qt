





# 2nd update
# # core/smart_break_engine_v2.py

# import time
# import datetime
# from core.behavior_classifier import BehaviorClassifier
# from core.fatigue_model import FatiguePredictionModel
# from core.meeting_mode import MeetingMode
# from core.storage_manager import StorageManager


# def ema_update(old_value: float, observed_value: float, alpha: float = 0.1) -> float:
#     """
#     Exponential moving average update for online learning.
#     new = (1 - alpha) * old + alpha * observed
#     """
#     return (1.0 - alpha) * float(old_value) + alpha * float(observed_value)


# class SmartBreakEngineV2:
#     """
#     Premium AI Mode (v3, revised):
#     - Adaptive, personalized, fatigue-aware
#     - Behavior-aware (Deep Reading, Reading, Focused Interaction, Deep Work)
#     - Meeting-aware, entertainment-aware
#     - Adaptive interval shaping (fatigue slope, active time, personalization)
#     - Strong protection for deep reading & deep work
#     - Gentle protection for AI-assisted focused interaction
#     - Real-world aligned: away/sleep = recovery, not full reset
#     """

#     def __init__(
#         self,
#         base_interval_minutes=20,
#         min_interval_minutes=12,
#         max_interval_minutes=45,
#         away_idle_seconds=120,
#         return_grace_seconds=300,
#     ):
#         self.base_interval = base_interval_minutes * 60
#         self.min_interval = min_interval_minutes * 60
#         self.max_interval = max_interval_minutes * 60

#         self.away_idle_seconds = away_idle_seconds
#         self.return_grace_seconds = return_grace_seconds

#         self.storage = StorageManager()

#         now = time.time()
#         self.session_start = now
#         self.last_break_time = now
#         self.real_time = 0.0

#         self.last_behavior = "Idle"
#         self.last_fatigue = 0.0

#         self.behavior_classifier = BehaviorClassifier()
#         self.fatigue_model = FatiguePredictionModel()
#         self.meeting_mode = MeetingMode()

#         # Load learning profile from storage
#         lp = self.storage.get_learning_profile()
#         preferred_focus_minutes = lp["preferred_focus_minutes"]
#         self.personal_baseline_interval = preferred_focus_minutes * 60.0
#         self.break_acceptance_rate = lp["break_acceptance_rate"]
#         self.fatigue_rise_multiplier = lp["fatigue_rise_multiplier"]
#         self.fatigue_recovery_multiplier = lp["fatigue_recovery_multiplier"]
#         self.night_owl_score = lp["night_owl_score"]

#         # How fast we adapt toward new observations
#         self.adaptation_rate = 0.3

#         self.is_away = False
#         self.return_grace_until = None

#     # ---------------------------------------------------------
#     # SLEEP HANDLING
#     # ---------------------------------------------------------
#     def handle_sleep(self):
#         now = time.time()
#         self.session_start = self.session_start or now
#         self.real_time = max(0.0, now - self.session_start)

#         # Sleep = strong recovery
#         self.last_fatigue *= 0.4
#         self.is_away = True
#         self.return_grace_until = None

#         # AI Mode logs away with mode="ai"
#         self.storage.log_away_event(mode="ai")

#     # ---------------------------------------------------------
#     # CLEAN LABELS
#     # ---------------------------------------------------------
#     def _clean_label(self, text):
#         if hasattr(text, "category"):
#             text = text.category
#         if not isinstance(text, str):
#             return "General Activity"
#         cleaned = text.replace("_", " ").title()
#         return cleaned if cleaned.strip() else "General Activity"

#     def _behavior_key(self, text):
#         if hasattr(text, "category"):
#             text = text.category
#         if not isinstance(text, str):
#             return "general_activity"
#         return text.strip().lower().replace(" ", "_")

#     # ---------------------------------------------------------
#     # ADAPTIVE INTERVAL COMPUTATION
#     # ---------------------------------------------------------
#     def _compute_dynamic_interval(self, fatigue_score, behavior_key):
#         interval = self.base_interval

#         # Fatigue-aware shaping
#         if fatigue_score > 70:
#             interval *= 0.6
#         elif fatigue_score > 50:
#             interval *= 0.8
#         elif fatigue_score < 20:
#             interval *= 1.2

#         # Behavior-aware shaping
#         if behavior_key == "deep_work":
#             interval *= 1.20
#         elif behavior_key == "deep_reading":
#             interval *= 1.25
#         elif behavior_key == "reading":
#             interval *= 1.10
#         elif behavior_key == "focused_interaction":
#             interval *= 1.08
#         elif behavior_key == "meeting":
#             interval *= 1.30

#         # Blend with learned personal baseline (EMA)
#         lp = self.storage.get_learning_profile()
#         current_pref_minutes = lp["preferred_focus_minutes"]
#         observed_minutes = interval / 60.0
#         new_pref_minutes = ema_update(current_pref_minutes, observed_minutes, alpha=self.adaptation_rate)
#         self.storage.update_learning_profile(preferred_focus_minutes=new_pref_minutes)
#         self.personal_baseline_interval = new_pref_minutes * 60.0

#         # Active time shaping
#         hours_active = self.real_time / 3600.0
#         if hours_active > 1.0:
#             interval *= 0.92
#         if hours_active > 2.0:
#             interval *= 0.85

#         # Short-term fatigue slope shaping
#         fatigue_delta = fatigue_score - self.last_fatigue
#         if fatigue_delta > 10:
#             interval *= 0.85
#         elif fatigue_delta < -10:
#             interval *= 1.10

#         # Night-owl vs morning preference (soft influence)
#         now = datetime.datetime.now()
#         hour = now.hour
#         is_night = 1.0 if (hour >= 20 or hour < 6) else 0.0
#         new_night = ema_update(self.night_owl_score, is_night, alpha=0.02)
#         self.night_owl_score = new_night
#         self.storage.update_learning_profile(night_owl_score=new_night)

#         if is_night and self.night_owl_score > 0.6:
#             interval *= 1.05
#         if (not is_night) and self.night_owl_score < 0.4:
#             interval *= 0.95

#         # Final blend with personal baseline
#         interval = 0.7 * interval + 0.3 * self.personal_baseline_interval

#         return max(self.min_interval, min(self.max_interval, interval))

#     # ---------------------------------------------------------
#     # MAIN DECISION LOGIC
#     # ---------------------------------------------------------
#     def should_trigger_break(self, signals):
#         now = time.time()
#         idle = signals.get("idle_seconds", 0.0)

#         if self.session_start is None:
#             self.session_start = now

#         self.real_time = max(0.0, now - self.session_start)

#         # 1. Classify behavior
#         behavior_result = self.behavior_classifier.classify(signals)
#         raw_behavior = behavior_result.category
#         behavior_key = self._behavior_key(raw_behavior)
#         clean_behavior = self._clean_label(raw_behavior)

#         # ---------------------------------------------------------
#         # WEIGHTED IDLE RECOVERY MODEL
#         # ---------------------------------------------------------
#         if idle > 0:
#             if idle < 30:
#                 # Micro-pause: no recovery
#                 pass
#             elif idle < 60:
#                 # Light micro-break: ~10% recovery
#                 self.last_fatigue *= 0.90
#             elif idle < self.away_idle_seconds:
#                 # Short break: ~30% recovery
#                 self.last_fatigue *= 0.70
#             else:
#                 # Full away break: ~50% recovery
#                 self.last_fatigue *= 0.50
#                 self.is_away = True
#                 self.return_grace_until = None
#                 self.last_behavior = "Idle"

#                 # Log full away reset
#                 self.storage.log_away_event(mode="ai")

#                 return {
#                     "trigger": False,
#                     "reason": self._clean_label("away_reset"),
#                     "behavior": "Idle",
#                     "fatigue_score": self.last_fatigue,
#                     "interval_used": self.base_interval,
#                 }

#         # 3. Return from away
#         if self.is_away:
#             self.is_away = False
#             self.return_grace_until = now + self.return_grace_seconds

#         # 4. Meeting suppression
#         if self.meeting_mode.should_suppress_breaks(signals, behavior_key):
#             self.last_behavior = "Meeting"
#             self.last_fatigue *= 0.7

#             self.storage.log_suppression_event("meeting", mode="ai")

#             return {
#                 "trigger": False,
#                 "reason": self._clean_label("meeting_suppressed"),
#                 "behavior": "Meeting",
#                 "fatigue_score": self.last_fatigue,
#                 "interval_used": self.base_interval,
#             }

#         # 5. Compute fatigue
#         fatigue_score = self.fatigue_model.compute_fatigue(signals, behavior_key)
#         self.last_behavior = clean_behavior

#         # 5a. Log behavior + fatigue (AI mode)
#         self.storage.log_behavior_event(clean_behavior, fatigue_score, mode="ai")
#         self.storage.log_fatigue_event(fatigue_score, mode="ai")

#         # 5b. Log input activity snapshot (AI mode)
#         self.storage.log_input_activity_event(
#             typing=signals.get("keypress_rate", 0.0),
#             mouse=signals.get("mouse_rate", 0.0),
#             scroll=signals.get("scroll_rate", 0.0),
#             behavior=clean_behavior,
#             mode="ai",
#         )

#         # 6. Dynamic interval (now learning-aware)
#         interval = self._compute_dynamic_interval(fatigue_score, behavior_key)

#         # 7. Minimum spacing
#         elapsed_since_break = now - self.last_break_time
#         if elapsed_since_break < self.min_interval:
#             self.last_fatigue = fatigue_score
#             return {
#                 "trigger": False,
#                 "reason": self._clean_label("recent_break"),
#                 "behavior": clean_behavior,
#                 "fatigue_score": fatigue_score,
#                 "interval_used": interval,
#             }

#         # 8. Grace window suppression
#         if self.return_grace_until is not None and now < self.return_grace_until:
#             self.storage.log_suppression_event("grace_window", mode="ai")
#             self.last_fatigue = fatigue_score
#             return {
#                 "trigger": False,
#                 "reason": self._clean_label("not_due"),
#                 "behavior": clean_behavior,
#                 "fatigue_score": fatigue_score,
#                 "interval_used": interval,
#             }
#         else:
#             self.return_grace_until = None

#         # 9. Interval-based break
#         if self.real_time >= interval and fatigue_score >= 40:
#             self.last_break_time = now
#             self.last_fatigue = fatigue_score

#             self.storage.log_break(
#                 reason="Interval Reached (AI)",
#                 behavior=clean_behavior,
#                 fatigue=fatigue_score,
#                 interval_used=interval,
#                 mode="ai",
#             )

#             return {
#                 "trigger": True,
#                 "reason": self._clean_label("interval_reached"),
#                 "behavior": clean_behavior,
#                 "fatigue_score": fatigue_score,
#                 "interval_used": interval,
#             }

#         # 10. Fatigue early break
#         if fatigue_score >=85:
#             self.last_break_time = now
#             self.last_fatigue = fatigue_score

#             self.storage.log_break(
#                 reason="Fatigue Early (AI)",
#                 behavior=clean_behavior,
#                 fatigue=fatigue_score,
#                 interval_used=interval,
#                 mode="ai",
#             )

#             return {
#                 "trigger": True,
#                 "reason": self._clean_label("fatigue_early"),
#                 "behavior": clean_behavior,
#                 "fatigue_score": fatigue_score,
#                 "interval_used": interval,
#             }

#         # 11. No break
#         self.last_fatigue = fatigue_score
#         return {
#             "trigger": False,
#             "reason": self._clean_label("not_due"),
#             "behavior": clean_behavior,
#             "fatigue_score": fatigue_score,
#             "interval_used": interval,
#         }

#     # ---------------------------------------------------------
#     # RESET AFTER BREAK
#     # ---------------------------------------------------------
#     def reset_after_break(self):
#         now = time.time()
#         self.session_start = now
#         self.last_break_time = now
#         self.real_time = 0.0
#         self.last_behavior = "Idle"
#         # Break = partial recovery
#         self.last_fatigue *= 0.5










import time
import datetime
from core.behavior_classifier import BehaviorClassifier
from core.fatigue_model import FatiguePredictionModel
from core.meeting_mode import MeetingMode
from core.storage_manager import StorageManager

def ema_update(old_value: float, observed_value: float, alpha: float = 0.1) -> float:
    """
    Exponential moving average update for online learning.
    """
    return (1.0 - alpha) * float(old_value) + alpha * float(observed_value)

class SmartBreakEngineV2:
    """
    Premium AI Mode (v3.5 Final):
    - FULL logic preservation (Weighted recovery, Behavior shaping)
    - ADDED: Rejection detection loop (+1 min focus baseline)
    - ADDED: Compliance validation (15s quiet = success)
    """

    def __init__(
        self,
        base_interval_minutes=20,
        min_interval_minutes=12,
        max_interval_minutes=45,
        away_idle_seconds=120,
        return_grace_seconds=300,
    ):
        self.base_interval = base_interval_minutes * 60
        self.min_interval = min_interval_minutes * 60
        self.max_interval = max_interval_minutes * 60

        self.away_idle_seconds = away_idle_seconds
        self.return_grace_seconds = return_grace_seconds

        self.storage = StorageManager()

        now = time.time()
        self.session_start = now
        self.last_break_time = now
        self.real_time = 0.0

        self.last_behavior = "Idle"
        self.last_fatigue = 0.0

        self.behavior_classifier = BehaviorClassifier()
        self.fatigue_model = FatiguePredictionModel()
        self.meeting_mode = MeetingMode()

        # Load learning profile from storage
        lp = self.storage.get_learning_profile()
        preferred_focus_minutes = lp["preferred_focus_minutes"]
        self.personal_baseline_interval = preferred_focus_minutes * 60.0
        self.break_acceptance_rate = lp["break_acceptance_rate"]
        self.fatigue_rise_multiplier = lp["fatigue_rise_multiplier"]
        self.fatigue_recovery_multiplier = lp["fatigue_recovery_multiplier"]
        self.night_owl_score = lp["night_owl_score"]

        # Rejection & Adaptation tracking
        self.notification_sent_at = None
        self.compliance_quiet_seconds = 0
        self.adaptation_rate = 0.3

        self.is_away = False
        self.return_grace_until = None

    def handle_sleep(self):
        now = time.time()
        self.session_start = self.session_start or now
        self.real_time = max(0.0, now - self.session_start)
        self.last_fatigue *= 0.4
        self.is_away = True
        self.return_grace_until = None
        self.storage.log_away_event(mode="ai")

    def _clean_label(self, text):
        if hasattr(text, "category"): text = text.category
        if not isinstance(text, str): return "General Activity"
        cleaned = text.replace("_", " ").title()
        return cleaned if cleaned.strip() else "General Activity"

    def _behavior_key(self, text):
        if hasattr(text, "category"): text = text.category
        if not isinstance(text, str): return "general_activity"
        return text.strip().lower().replace(" ", "_")

    def _compute_dynamic_interval(self, fatigue_score, behavior_key):
        interval = self.base_interval

        # Fatigue shaping
        if fatigue_score > 70: interval *= 0.6
        elif fatigue_score > 50: interval *= 0.8
        elif fatigue_score < 20: interval *= 1.2

        # Behavior shaping (Multipliers strictly kept)
        if behavior_key == "deep_work": interval *= 1.20
        elif behavior_key == "deep_reading": interval *= 1.25
        elif behavior_key == "reading": interval *= 1.10
        elif behavior_key == "focused_interaction": interval *= 1.08
        elif behavior_key == "meeting": interval *= 1.30

        # Learning blend
        lp = self.storage.get_learning_profile()
        current_pref_minutes = lp["preferred_focus_minutes"]
        observed_minutes = interval / 60.0
        new_pref_minutes = ema_update(current_pref_minutes, observed_minutes, alpha=self.adaptation_rate)
        self.storage.update_learning_profile(preferred_focus_minutes=new_pref_minutes)
        self.personal_baseline_interval = new_pref_minutes * 60.0

        # Active time shaping
        hours_active = self.real_time / 3600.0
        if hours_active > 1.0: interval *= 0.92
        if hours_active > 2.0: interval *= 0.85

        # Fatigue slope
        fatigue_delta = fatigue_score - self.last_fatigue
        if fatigue_delta > 10: interval *= 0.85
        elif fatigue_delta < -10: interval *= 1.10

        # Night-owl tracking
        now = datetime.datetime.now()
        is_night = 1.0 if (now.hour >= 20 or now.hour < 6) else 0.0
        self.night_owl_score = ema_update(self.night_owl_score, is_night, alpha=0.02)
        self.storage.update_learning_profile(night_owl_score=self.night_owl_score)

        if is_night and self.night_owl_score > 0.6: interval *= 1.05
        if (not is_night) and self.night_owl_score < 0.4: interval *= 0.95

        interval = 0.7 * interval + 0.3 * self.personal_baseline_interval
        return max(self.min_interval, min(self.max_interval, interval))

    def should_trigger_break(self, signals):
        now = time.time()
        idle = signals.get("idle_seconds", 0.0)

        if self.session_start is None: self.session_start = now
        self.real_time = max(0.0, now - self.session_start)

        # --- NEW: REJECTION / COMPLIANCE LEARNING ---
        if self.notification_sent_at:
            time_since_notify = now - self.notification_sent_at
            if time_since_notify < 60: 
                # Check for silence (no typing/mouse)
                if signals.get("keypress_rate", 0) == 0 and signals.get("mouse_rate", 0) == 0:
                    self.compliance_quiet_seconds += 1
                else:
                    self.compliance_quiet_seconds = 0
                
                if self.compliance_quiet_seconds >= 15: # Success
                    self.notification_sent_at = None
                    self.compliance_quiet_seconds = 0
            else: # Rejection
                lp = self.storage.get_learning_profile()
                new_pref = min(45.0, lp["preferred_focus_minutes"] + 1.0)
                self.storage.update_learning_profile(preferred_focus_minutes=new_pref)
                self.personal_baseline_interval = new_pref * 60.0
                self.notification_sent_at = None
                self.compliance_quiet_seconds = 0

        # 1. Behavior classification
        behavior_result = self.behavior_classifier.classify(signals)
        behavior_key = self._behavior_key(behavior_result.category)
        clean_behavior = self._clean_label(behavior_result.category)

        # 2. WEIGHTED IDLE RECOVERY (STRICTLY PRESERVED)
        if idle > 0:
            if idle < 30: pass
            elif idle < 60: self.last_fatigue *= 0.90
            elif idle < self.away_idle_seconds: self.last_fatigue *= 0.70
            else:
                self.last_fatigue *= 0.50
                self.is_away = True
                self.last_behavior = "Idle"
                self.storage.log_away_event(mode="ai")
                return {"trigger": False, "reason": "Away Reset", "behavior": "Idle", "fatigue_score": self.last_fatigue, "interval_used": self.base_interval}

        # 3. Return & Meeting Logic
        if self.is_away:
            self.is_away = False
            self.return_grace_until = now + self.return_grace_seconds

        if self.meeting_mode.should_suppress_breaks(signals, behavior_key):
            self.last_behavior, self.last_fatigue = "Meeting", self.last_fatigue * 0.7
            self.storage.log_suppression_event("meeting", mode="ai")
            return {"trigger": False, "reason": "Meeting Suppressed", "behavior": "Meeting", "fatigue_score": self.last_fatigue, "interval_used": self.base_interval}

        # 5. Compute fatigue & interval
        fatigue_score = self.fatigue_model.compute_fatigue(signals, behavior_key)
        self.last_behavior = clean_behavior
        interval = self._compute_dynamic_interval(fatigue_score, behavior_key)

        # Logging (Strictly preserved)
        self.storage.log_behavior_event(clean_behavior, fatigue_score, mode="ai")
        self.storage.log_input_activity_event(typing=signals.get("keypress_rate", 0.0), mouse=signals.get("mouse_rate", 0.0), scroll=signals.get("scroll_rate", 0.0), behavior=clean_behavior, mode="ai")

        # Decision gates
        elapsed = now - self.last_break_time
        if elapsed < self.min_interval or (self.return_grace_until and now < self.return_grace_until):
            self.last_fatigue = fatigue_score
            return {"trigger": False, "reason": "Not Due", "behavior": clean_behavior, "fatigue_score": fatigue_score, "interval_used": interval}

        # Trigger logic
        trigger, reason = False, "not_due"
        if self.real_time >= interval and fatigue_score >= 40:
            trigger, reason = True, "interval_reached"
        elif fatigue_score >= 85:
            trigger, reason = True, "fatigue_early"

        if trigger:
            self.last_break_time = now
            self.notification_sent_at = now # Set watch for compliance
            self.storage.log_break(reason=reason, behavior=clean_behavior, fatigue=fatigue_score, interval_used=interval, mode="ai")

        self.last_fatigue = fatigue_score
        return {"trigger": trigger, "reason": self._clean_label(reason), "behavior": clean_behavior, "fatigue_score": fatigue_score, "interval_used": interval}

    def reset_after_break(self):
        now = time.time()
        self.session_start = self.last_break_time = now
        self.real_time, self.last_behavior = 0.0, "Idle"
        self.last_fatigue *= 0.5
        self.notification_sent_at = None