

# # I added PDF's to it for reading
# # core/behavior_classifier.py

# from dataclasses import dataclass
# from typing import Dict, Callable, List

# DEFAULT_THRESHOLDS = {
#     "away_idle": 120,
#     "idle": 60,
#     "low_typing": 5,
#     "medium_typing": 20,
#     "high_typing": 40,
#     "low_mouse": 10,
#     "high_mouse": 40,
#     "brightness_high": 80,
#     "deep_reading_scroll_max": 25,
#     "deep_reading_mouse_max": 40,
#     "deep_reading_switch_max": 3,
# }

# @dataclass
# class BehaviorResult:
#     category: str
#     confidence: float
#     signals: Dict

# class BehaviorClassifier:
#     """
#     Premium production-grade classifier:
#     - Deterministic, priority-ordered
#     - Detects reading, deep reading, writing, coding, browsing
#     - Detects PDF/Word/PPT environments
#     - Aligns with Smart Mode + AI Mode
#     """

#     def __init__(self, thresholds: Dict = None):
#         self.t = thresholds or DEFAULT_THRESHOLDS

#         self.rules: List[Callable[[Dict], BehaviorResult | None]] = [
#             self._rule_away,
#             self._rule_meeting,
#             self._rule_eye_strain_risk,
#             self._rule_pdf_word_ppt_reading,
#             self._rule_browser_pdf_reading,
#             self._rule_watching,
#             self._rule_coding_writing,
#             self._rule_deep_work,
#             self._rule_multitasking,
#             self._rule_heavy_browsing,
#             self._rule_light_browsing,
#             self._rule_posture_risk,
#             self._rule_fatigued_activity,
#             self._rule_idle,
#         ]

#     def classify(self, signals: Dict) -> BehaviorResult:
#         s = self._normalize(signals)

#         for rule in self.rules:
#             result = rule(s)
#             if result:
#                 return result

#         return BehaviorResult("General Activity", 0.3, s)

#     def _normalize(self, s: Dict) -> Dict:
#         title = (s.get("active_window") or "").lower()

#         return {
#             "title": title,
#             "window": s.get("window_category", "other"),
#             "typing": float(s.get("keypress_rate", 0)),
#             "mouse": float(s.get("mouse_rate", 0)),
#             "scroll": float(s.get("scroll_rate", 0)),
#             "switches": float(s.get("window_switches", 0)),
#             "idle": float(s.get("idle_seconds", 0)),
#             "brightness": float(s.get("screen_brightness", 50)),
#             "webcam": bool(s.get("webcam_active", False)),
#             "audio": bool(s.get("audio_playing", False)),
#             "fullscreen": bool(s.get("fullscreen", False)),
#         }

#     # RULES ---------------------------------------------------

#     def _rule_away(self, s):
#         if s["idle"] > self.t["away_idle"]:
#             return BehaviorResult("Away", 0.95, s)

#     def _rule_meeting(self, s):
#         if s["webcam"] or s["window"] == "meeting":
#             return BehaviorResult("Meeting", 0.9, s)

#     def _rule_eye_strain_risk(self, s):
#         if s["brightness"] > self.t["brightness_high"] and s["idle"] < self.t["idle"]:
#             return BehaviorResult("Eye Strain Risk", 0.85, s)

#     # --- PDF / Word / PowerPoint reading ---------------------

#     def _rule_pdf_word_ppt_reading(self, s):
#         title = s["title"]

#         is_pdf = ".pdf" in title
#         is_word = "word" in title or title.endswith(".doc") or title.endswith(".docx")
#         is_ppt = "powerpoint" in title or title.endswith(".ppt") or title.endswith(".pptx")

#         in_doc_env = is_pdf or is_word or is_ppt or s["window"] == "office"

#         if not in_doc_env:
#             return None

#         # Writing in Word
#         if is_word and s["typing"] > self.t["high_typing"]:
#             return BehaviorResult("Writing", 0.9, s)

#         # Slide reading
#         if is_ppt:
#             if s["typing"] < 20 and s["scroll"] < 15 and s["switches"] < 5:
#                 if s["typing"] < 10 and s["mouse"] < 20 and s["switches"] < 2:
#                     return BehaviorResult("Deep Reading", 0.9, s)
#                 return BehaviorResult("Reading", 0.85, s)

#         # PDF / Word reading
#         if s["scroll"] > 5 and s["typing"] < 30 and s["switches"] < 8:
#             # Deep reading
#             if (
#                 s["scroll"] < self.t["deep_reading_scroll_max"]
#                 and s["mouse"] < self.t["deep_reading_mouse_max"]
#                 and s["switches"] < self.t["deep_reading_switch_max"]
#                 and s["typing"] < 15
#             ):
#                 return BehaviorResult("Deep Reading", 0.9, s)
#             return BehaviorResult("Reading", 0.85, s)

#     # --- Browser PDF reading ---------------------------------

#     def _rule_browser_pdf_reading(self, s):
#         if ".pdf" not in s["title"]:
#             return None

#         if s["scroll"] > 5 and s["typing"] < 30 and s["switches"] < 8:
#             if (
#                 s["scroll"] < self.t["deep_reading_scroll_max"]
#                 and s["mouse"] < self.t["deep_reading_mouse_max"]
#                 and s["switches"] < self.t["deep_reading_switch_max"]
#                 and s["typing"] < 15
#             ):
#                 return BehaviorResult("Deep Reading", 0.9, s)
#             return BehaviorResult("Reading", 0.85, s)

#     # --- Watching --------------------------------------------

#     def _rule_watching(self, s):
#         if s["window"] == "video" and s["typing"] < self.t["low_typing"]:
#             return BehaviorResult("Watching", 0.85, s)

#     # --- Coding / Writing ------------------------------------

#     def _rule_coding_writing(self, s):
#         if s["typing"] > self.t["high_typing"]:
#             if s["window"] == "coding":
#                 return BehaviorResult("Coding", 0.9, s)
#             return BehaviorResult("Writing", 0.85, s)

#     # --- Deep Work -------------------------------------------

#     def _rule_deep_work(self, s):
#         if s["typing"] > self.t["medium_typing"] and s["mouse"] < self.t["medium_typing"]:
#             if s["switches"] < 5:
#                 return BehaviorResult("Deep Work", 0.8, s)

#     # --- Multitasking ----------------------------------------

#     def _rule_multitasking(self, s):
#         if s["mouse"] > self.t["high_mouse"] and s["typing"] > self.t["medium_typing"]:
#             return BehaviorResult("Multitasking", 0.8, s)

#     # --- Browsing --------------------------------------------

#     def _rule_heavy_browsing(self, s):
#         if s["window"] == "browser" and s["typing"] >= self.t["medium_typing"]:
#             return BehaviorResult("Heavy Browsing", 0.75, s)

#     def _rule_light_browsing(self, s):
#         if s["window"] == "browser" and s["typing"] < self.t["medium_typing"]:
#             return BehaviorResult("Light Browsing", 0.7, s)

#     # --- Posture Risk ----------------------------------------

#     def _rule_posture_risk(self, s):
#         if s["idle"] > 45 and s["typing"] > self.t["medium_typing"]:
#             return BehaviorResult("Posture Risk", 0.7, s)

#     # --- Fatigued Activity -----------------------------------

#     def _rule_fatigued_activity(self, s):
#         if (
#             s["typing"] < self.t["low_typing"]
#             and s["mouse"] < self.t["low_mouse"]
#             and s["idle"] < self.t["idle"]
#         ):
#             return BehaviorResult("Fatigued Activity", 0.6, s)

#     # --- Idle -------------------------------------------------

#     def _rule_idle(self, s):
#         if s["typing"] == 0 and s["mouse"] == 0:
#             return BehaviorResult("Idle", 0.6, s)









# Added Chatgpt, germini and others as focused interraction

# from dataclasses import dataclass
# from typing import Dict, Callable, List

# DEFAULT_THRESHOLDS = {
#     "away_idle": 120,
#     "idle": 60,
#     "low_typing": 5,
#     "medium_typing": 20,
#     "high_typing": 40,
#     "low_mouse": 10,
#     "high_mouse": 40,
#     "brightness_high": 80,
#     "deep_reading_scroll_max": 25,
#     "deep_reading_mouse_max": 40,
#     "deep_reading_switch_max": 3,
# }

# @dataclass
# class BehaviorResult:
#     category: str
#     confidence: float
#     signals: Dict

# class BehaviorClassifier:
#     """
#     Premium production-grade classifier:
#     - Deterministic, priority-ordered
#     - Detects reading, deep reading, writing, coding, browsing
#     - Detects PDF/Word/PPT environments
#     - Detects AI-assistant focused interaction
#     - Aligns with Smart Mode + AI Mode
#     """

#     def __init__(self, thresholds: Dict = None):
#         self.t = thresholds or DEFAULT_THRESHOLDS

#         self.rules: List[Callable[[Dict], BehaviorResult | None]] = [
#             self._rule_away,
#             self._rule_meeting,
#             self._rule_eye_strain_risk,
#             self._rule_pdf_word_ppt_reading,
#             self._rule_browser_pdf_reading,
#             self._rule_watching,
#             self._rule_coding_writing,
#             self._rule_deep_work,
#             self._rule_multitasking,
#             self._rule_focused_interaction,   # NEW: AI tools like Copilot / ChatGPT / Gemini
#             self._rule_heavy_browsing,
#             self._rule_light_browsing,
#             self._rule_posture_risk,
#             self._rule_fatigued_activity,
#             self._rule_idle,
#         ]

#     def classify(self, signals: Dict) -> BehaviorResult:
#         s = self._normalize(signals)

#         for rule in self.rules:
#             result = rule(s)
#             if result:
#                 return result

#         return BehaviorResult("General Activity", 0.3, s)

#     def _normalize(self, s: Dict) -> Dict:
#         title = (s.get("active_window") or "").lower()

#         return {
#             "title": title,
#             "window": s.get("window_category", "other"),
#             "typing": float(s.get("keypress_rate", 0)),
#             "mouse": float(s.get("mouse_rate", 0)),
#             "scroll": float(s.get("scroll_rate", 0)),
#             "switches": float(s.get("window_switches", 0)),
#             "idle": float(s.get("idle_seconds", 0)),
#             "brightness": float(s.get("screen_brightness", 50)),
#             "webcam": bool(s.get("webcam_active", False)),
#             "audio": bool(s.get("audio_playing", False)),
#             "fullscreen": bool(s.get("fullscreen", False)),
#         }

#     # RULES ---------------------------------------------------

#     def _rule_away(self, s):
#         if s["idle"] > self.t["away_idle"]:
#             return BehaviorResult("Away", 0.95, s)

#     def _rule_meeting(self, s):
#         if s["webcam"] or s["window"] == "meeting":
#             return BehaviorResult("Meeting", 0.9, s)

#     def _rule_eye_strain_risk(self, s):
#         if s["brightness"] > self.t["brightness_high"] and s["idle"] < self.t["idle"]:
#             return BehaviorResult("Eye Strain Risk", 0.85, s)

#     # --- PDF / Word / PowerPoint reading ---------------------

#     def _rule_pdf_word_ppt_reading(self, s):
#         title = s["title"]

#         is_pdf = ".pdf" in title
#         is_word = "word" in title or title.endswith(".doc") or title.endswith(".docx")
#         is_ppt = "powerpoint" in title or title.endswith(".ppt") or title.endswith(".pptx")

#         in_doc_env = is_pdf or is_word or is_ppt or s["window"] == "office"

#         if not in_doc_env:
#             return None

#         # Writing in Word
#         if is_word and s["typing"] > self.t["high_typing"]:
#             return BehaviorResult("Writing", 0.9, s)

#         # Slide reading
#         if is_ppt:
#             if s["typing"] < 20 and s["scroll"] < 15 and s["switches"] < 5:
#                 if s["typing"] < 10 and s["mouse"] < 20 and s["switches"] < 2:
#                     return BehaviorResult("Deep Reading", 0.9, s)
#                 return BehaviorResult("Reading", 0.85, s)

#         # PDF / Word reading
#         if s["scroll"] > 5 and s["typing"] < 30 and s["switches"] < 8:
#             # Deep reading
#             if (
#                 s["scroll"] < self.t["deep_reading_scroll_max"]
#                 and s["mouse"] < self.t["deep_reading_mouse_max"]
#                 and s["switches"] < self.t["deep_reading_switch_max"]
#                 and s["typing"] < 15
#             ):
#                 return BehaviorResult("Deep Reading", 0.9, s)
#             return BehaviorResult("Reading", 0.85, s)

#     # --- Browser PDF reading ---------------------------------

#     def _rule_browser_pdf_reading(self, s):
#         if ".pdf" not in s["title"]:
#             return None

#         if s["scroll"] > 5 and s["typing"] < 30 and s["switches"] < 8:
#             if (
#                 s["scroll"] < self.t["deep_reading_scroll_max"]
#                 and s["mouse"] < self.t["deep_reading_mouse_max"]
#                 and s["switches"] < self.t["deep_reading_switch_max"]
#                 and s["typing"] < 15
#             ):
#                 return BehaviorResult("Deep Reading", 0.9, s)
#             return BehaviorResult("Reading", 0.85, s)

#     # --- Watching --------------------------------------------

#     def _rule_watching(self, s):
#         if s["window"] == "video" and s["typing"] < self.t["low_typing"]:
#             return BehaviorResult("Watching", 0.85, s)

#     # --- Coding / Writing ------------------------------------

#     def _rule_coding_writing(self, s):
#         if s["typing"] > self.t["high_typing"]:
#             if s["window"] == "coding":
#                 return BehaviorResult("Coding", 0.9, s)
#             return BehaviorResult("Writing", 0.85, s)

#     # --- Deep Work -------------------------------------------

#     def _rule_deep_work(self, s):
#         if s["typing"] > self.t["medium_typing"] and s["mouse"] < self.t["medium_typing"]:
#             if s["switches"] < 5:
#                 return BehaviorResult("Deep Work", 0.8, s)

#     # --- Multitasking ----------------------------------------

#     def _rule_multitasking(self, s):
#         if s["mouse"] > self.t["high_mouse"] and s["typing"] > self.t["medium_typing"]:
#             return BehaviorResult("Multitasking", 0.8, s)

#     # --- Focused Interaction (AI assistants) -----------------

#     def _rule_focused_interaction(self, s):
#         title = s["title"]
#         if not any(
#             kw in title
#             for kw in ["chatgpt", "copilot", "gemini", "claude", "bard", "perplexity"]
#         ):
#             return None

#         # Hybrid pattern: moderate typing/scroll, low switches, anchored in one window
#         if 5 <= s["typing"] <= 40 and 5 <= s["scroll"] <= 40 and s["switches"] < 8:
#             if s["mouse"] < 40:
#                 return BehaviorResult("Focused Interaction", 0.85, s)

#     # --- Browsing --------------------------------------------

#     def _rule_heavy_browsing(self, s):
#         if s["window"] == "browser" and s["typing"] >= self.t["medium_typing"]:
#             return BehaviorResult("Heavy Browsing", 0.75, s)

#     def _rule_light_browsing(self, s):
#         if s["window"] == "browser" and s["typing"] < self.t["medium_typing"]:
#             return BehaviorResult("Light Browsing", 0.7, s)

#     # --- Posture Risk ----------------------------------------

#     def _rule_posture_risk(self, s):
#         if s["idle"] > 45 and s["typing"] > self.t["medium_typing"]:
#             return BehaviorResult("Posture Risk", 0.7, s)

#     # --- Fatigued Activity -----------------------------------

#     def _rule_fatigued_activity(self, s):
#         if (
#             s["typing"] < self.t["low_typing"]
#             and s["mouse"] < self.t["low_mouse"]
#             and s["idle"] < self.t["idle"]
#         ):
#             return BehaviorResult("Fatigued Activity", 0.6, s)

#     # --- Idle -------------------------------------------------

#     def _rule_idle(self, s):
#         if s["typing"] == 0 and s["mouse"] == 0:
#             return BehaviorResult("Idle", 0.6, s)

















# I expanded the search

# from dataclasses import dataclass
# from typing import Dict, Callable, List

# DEFAULT_THRESHOLDS = {
#     "away_idle": 120,
#     "idle": 60,
#     "low_typing": 5,
#     "medium_typing": 20,
#     "high_typing": 40,
#     "low_mouse": 10,
#     "high_mouse": 40,
#     "brightness_high": 80,
#     "deep_reading_scroll_max": 25,
#     "deep_reading_mouse_max": 40,
#     "deep_reading_switch_max": 3,
# }

# # NEW: Expanded coding/deep-work app detection
# CODING_KEYWORDS = [
#     "rstudio", "jupyter", "spyder", "matlab", "visual studio", "eclipse",
#     "netbeans", "android studio", "codeblocks", "sublime", "atom",
#     "notepad++", "webstorm", "phpstorm", "rubymine", "goland", "clion",
#     "stata", "spss", "sas", "minitab", "mathematica", "wolfram",
#     "maple", "solidworks", "autocad", "fusion 360", "texstudio",
#     "texmaker", "lyx"
# ]

# @dataclass
# class BehaviorResult:
#     category: str
#     confidence: float
#     signals: Dict

# class BehaviorClassifier:
#     """
#     Premium production-grade classifier:
#     - Deterministic, priority-ordered
#     - Detects reading, deep reading, writing, coding, browsing
#     - Detects PDF/Word/PPT environments
#     - Detects AI-assistant focused interaction
#     - Aligns with Smart Mode + AI Mode
#     """

#     def __init__(self, thresholds: Dict = None):
#         self.t = thresholds or DEFAULT_THRESHOLDS

#         self.rules: List[Callable[[Dict], BehaviorResult | None]] = [
#             self._rule_away,
#             self._rule_meeting,
#             self._rule_eye_strain_risk,
#             self._rule_pdf_word_ppt_reading,
#             self._rule_browser_pdf_reading,
#             self._rule_watching,
#             self._rule_coding_writing,   # UPDATED
#             self._rule_deep_work,        # UPDATED
#             self._rule_multitasking,
#             self._rule_focused_interaction,
#             self._rule_heavy_browsing,
#             self._rule_light_browsing,
#             self._rule_posture_risk,
#             self._rule_fatigued_activity,
#             self._rule_idle,
#         ]

#     def classify(self, signals: Dict) -> BehaviorResult:
#         s = self._normalize(signals)

#         for rule in self.rules:
#             result = rule(s)
#             if result:
#                 return result

#         return BehaviorResult("General Activity", 0.3, s)

#     def _normalize(self, s: Dict) -> Dict:
#         title = (s.get("active_window") or "").lower()

#         return {
#             "title": title,
#             "window": s.get("window_category", "other"),
#             "typing": float(s.get("keypress_rate", 0)),
#             "mouse": float(s.get("mouse_rate", 0)),
#             "scroll": float(s.get("scroll_rate", 0)),
#             "switches": float(s.get("window_switches", 0)),
#             "idle": float(s.get("idle_seconds", 0)),
#             "brightness": float(s.get("screen_brightness", 50)),
#             "webcam": bool(s.get("webcam_active", False)),
#             "audio": bool(s.get("audio_playing", False)),
#             "fullscreen": bool(s.get("fullscreen", False)),
#         }
#     # RULES ---------------------------------------------------

#     def _rule_away(self, s):
#         if s["idle"] > self.t["away_idle"]:
#             return BehaviorResult("Away", 0.95, s)

#     def _rule_meeting(self, s):
#         if s["webcam"] or s["window"] == "meeting":
#             return BehaviorResult("Meeting", 0.9, s)

#     def _rule_eye_strain_risk(self, s):
#         if s["brightness"] > self.t["brightness_high"] and s["idle"] < self.t["idle"]:
#             return BehaviorResult("Eye Strain Risk", 0.85, s)

#     # --- PDF / Word / PowerPoint reading ---------------------

#     def _rule_pdf_word_ppt_reading(self, s):
#         title = s["title"]

#         is_pdf = ".pdf" in title
#         is_word = "word" in title or title.endswith(".doc") or title.endswith(".docx")
#         is_ppt = "powerpoint" in title or title.endswith(".ppt") or title.endswith(".pptx")

#         in_doc_env = is_pdf or is_word or is_ppt or s["window"] == "office"

#         if not in_doc_env:
#             return None

#         # Writing in Word
#         if is_word and s["typing"] > self.t["high_typing"]:
#             return BehaviorResult("Writing", 0.9, s)

#         # Slide reading
#         if is_ppt:
#             if s["typing"] < 20 and s["scroll"] < 15 and s["switches"] < 5:
#                 if s["typing"] < 10 and s["mouse"] < 20 and s["switches"] < 2:
#                     return BehaviorResult("Deep Reading", 0.9, s)
#                 return BehaviorResult("Reading", 0.85, s)

#         # PDF / Word reading
#         if s["scroll"] > 5 and s["typing"] < 30 and s["switches"] < 8:
#             if (
#                 s["scroll"] < self.t["deep_reading_scroll_max"]
#                 and s["mouse"] < self.t["deep_reading_mouse_max"]
#                 and s["switches"] < self.t["deep_reading_switch_max"]
#                 and s["typing"] < 15
#             ):
#                 return BehaviorResult("Deep Reading", 0.9, s)
#             return BehaviorResult("Reading", 0.85, s)

#     # --- Browser PDF reading ---------------------------------

#     def _rule_browser_pdf_reading(self, s):
#         if ".pdf" not in s["title"]:
#             return None

#         if s["scroll"] > 5 and s["typing"] < 30 and s["switches"] < 8:
#             if (
#                 s["scroll"] < self.t["deep_reading_scroll_max"]
#                 and s["mouse"] < self.t["deep_reading_mouse_max"]
#                 and s["switches"] < self.t["deep_reading_switch_max"]
#                 and s["typing"] < 15
#             ):
#                 return BehaviorResult("Deep Reading", 0.9, s)
#             return BehaviorResult("Reading", 0.85, s)

#     # --- Watching --------------------------------------------

#     def _rule_watching(self, s):
#         if s["window"] == "video" and s["typing"] < self.t["low_typing"]:
#             return BehaviorResult("Watching", 0.85, s)

#     # --- Coding / Writing (UPDATED with student tools) -------

#     def _rule_coding_writing(self, s):
#         title = s["title"]

#         # NEW: Detect coding/data-science/math tools by window title
#         if any(kw in title for kw in CODING_KEYWORDS):
#             if s["typing"] > self.t["low_typing"]:
#                 return BehaviorResult("Coding", 0.9, s)
#             else:
#                 return BehaviorResult("Deep Work", 0.8, s)

#         # Existing logic: high typing in coding window
#         if s["typing"] > self.t["high_typing"]:
#             if s["window"] == "coding":
#                 return BehaviorResult("Coding", 0.9, s)
#             return BehaviorResult("Writing", 0.85, s)

#     # --- Deep Work (UPDATED to include coding tools) ---------

#     def _rule_deep_work(self, s):
#         title = s["title"]

#         # NEW: Deep work triggered by coding/data-science/math tools
#         if any(kw in title for kw in CODING_KEYWORDS):
#             if s["typing"] > self.t["medium_typing"] and s["switches"] < 5:
#                 return BehaviorResult("Deep Work", 0.85, s)

#         # Existing deep work logic
#         if s["typing"] > self.t["medium_typing"] and s["mouse"] < self.t["medium_typing"]:
#             if s["switches"] < 5:
#                 return BehaviorResult("Deep Work", 0.8, s)

#     # --- Multitasking ----------------------------------------

#     def _rule_multitasking(self, s):
#         if s["mouse"] > self.t["high_mouse"] and s["typing"] > self.t["medium_typing"]:
#             return BehaviorResult("Multitasking", 0.8, s)

#     # --- Focused Interaction (AI assistants) -----------------

#     def _rule_focused_interaction(self, s):
#         title = s["title"]
#         if not any(
#             kw in title
#             for kw in ["chatgpt", "copilot", "gemini", "claude", "bard", "perplexity"]
#         ):
#             return None

#         if 5 <= s["typing"] <= 40 and 5 <= s["scroll"] <= 40 and s["switches"] < 8:
#             if s["mouse"] < 40:
#                 return BehaviorResult("Focused Interaction", 0.85, s)

#     # --- Browsing --------------------------------------------

#     def _rule_heavy_browsing(self, s):
#         if s["window"] == "browser" and s["typing"] >= self.t["medium_typing"]:
#             return BehaviorResult("Heavy Browsing", 0.75, s)

#     def _rule_light_browsing(self, s):
#         if s["window"] == "browser" and s["typing"] < self.t["medium_typing"]:
#             return BehaviorResult("Light Browsing", 0.7, s)

#     # --- Posture Risk ----------------------------------------

#     def _rule_posture_risk(self, s):
#         if s["idle"] > 45 and s["typing"] > self.t["medium_typing"]:
#             return BehaviorResult("Posture Risk", 0.7, s)

#     # --- Fatigued Activity -----------------------------------

#     def _rule_fatigued_activity(self, s):
#         if (
#             s["typing"] < self.t["low_typing"]
#             and s["mouse"] < self.t["low_mouse"]
#             and s["idle"] < self.t["idle"]
#         ):
#             return BehaviorResult("Fatigued Activity", 0.6, s)

#     # --- Idle -------------------------------------------------

#     def _rule_idle(self, s):
#         if s["typing"] == 0 and s["mouse"] == 0:
#             return BehaviorResult("Idle", 0.6, s)




















# I expanded even further to add gaming and music production and video editing

from dataclasses import dataclass
from typing import Dict, Callable, List

DEFAULT_THRESHOLDS = {
    "away_idle": 120,
    "idle": 60,
    "low_typing": 5,
    "medium_typing": 20,
    "high_typing": 40,
    "low_mouse": 10,
    "high_mouse": 40,
    "brightness_high": 80,
    "deep_reading_scroll_max": 25,
    "deep_reading_mouse_max": 40,
    "deep_reading_switch_max": 3,
}

# Expanded coding/deep-work app detection
CODING_KEYWORDS = [
    "rstudio", "jupyter", "spyder", "matlab", "visual studio", "eclipse",
    "netbeans", "android studio", "codeblocks", "sublime", "atom",
    "notepad++", "webstorm", "phpstorm", "rubymine", "goland", "clion",
    "stata", "spss", "sas", "minitab", "mathematica", "wolfram",
    "maple", "solidworks", "autocad", "fusion 360", "texstudio",
    "texmaker", "lyx", "colab", "jupyterhub", "overleaf", "replit",
    "codepen", "jsfiddle"
]

# Expanded browsing / research / social / learning tools
BROWSING_KEYWORDS = [
    "notion", "obsidian", "roam", "onenote", "evernote", "google docs",
    "dropbox paper", "github", "gitlab", "bitbucket", "stackoverflow",
    "stackexchange", "reddit", "medium", "wikipedia", "quora", "linkedin",
    "twitter", "x.com", "facebook", "instagram", "tiktok", "canvas",
    "blackboard", "moodle", "coursera", "udemy", "edx", "khan academy",
    "researchgate", "semantic scholar", "google scholar", "pubmed",
    "jstor", "arxiv", "ssrn", "mendeley", "zotero", "endnote"
]

# Expanded watching / streaming platforms
WATCHING_KEYWORDS = [
    "youtube", "netflix", "prime video", "amazon prime", "disney+",
    "hulu", "hbo", "max", "apple tv", "crunchyroll", "vimeo",
    "twitch", "tiktok", "instagram video"
]

# Gaming detection
GAMING_KEYWORDS = [
    "steam", "epic games", "riot client", "league of legends", "valorant",
    "fortnite", "minecraft", "roblox", "battle.net", "overwatch",
    "call of duty", "csgo", "counter-strike", "gta v", "elden ring"
]

# Music production tools
MUSIC_KEYWORDS = [
    "ableton", "fl studio", "logic pro", "pro tools", "cubase",
    "reaper", "garageband", "studio one", "reason", "bitwig"
]

# Video editing tools
VIDEO_EDITING_KEYWORDS = [
    "premiere", "after effects", "davinci resolve", "final cut",
    "filmora", "vegas pro", "hitfilm", "capcut"
]

@dataclass
class BehaviorResult:
    category: str
    confidence: float
    signals: Dict

class BehaviorClassifier:
    """
    Premium production-grade classifier:
    - Deterministic, priority-ordered
    - Detects reading, deep reading, writing, coding, browsing
    - Detects PDF/Word/PPT environments
    - Detects AI-assistant focused interaction
    - Detects gaming, music production, video editing
    - Aligns with Smart Mode + AI Mode
    """

    def __init__(self, thresholds: Dict = None):
        self.t = thresholds or DEFAULT_THRESHOLDS

        self.rules: List[Callable[[Dict], BehaviorResult | None]] = [
            self._rule_away,
            self._rule_meeting,
            self._rule_eye_strain_risk,
            self._rule_gaming,
            self._rule_music_production,
            self._rule_video_editing,
            self._rule_pdf_word_ppt_reading,
            self._rule_browser_pdf_reading,
            self._rule_watching,
            self._rule_coding_writing,
            self._rule_deep_work,
            self._rule_multitasking,
            self._rule_focused_interaction,
            self._rule_heavy_browsing,
            self._rule_light_browsing,
            self._rule_posture_risk,
            self._rule_fatigued_activity,
            self._rule_idle,
        ]

    def classify(self, signals: Dict) -> BehaviorResult:
        s = self._normalize(signals)

        for rule in self.rules:
            result = rule(s)
            if result:
                return result

        return BehaviorResult("General Activity", 0.3, s)

    # def _normalize(self, s: Dict) -> Dict:
    #     title = (s.get("active_window") or "").lower()

    #     return {
    #         "title": title,
    #         "window": s.get("window_category", "other"),
    #         "typing": float(s.get("keypress_rate", 0)),
    #         "mouse": float(s.get("mouse_rate", 0)),
    #         "scroll": float(s.get("scroll_rate", 0)),
    #         "switches": float(s.get("window_switches", 0)),
    #         "idle": float(s.get("idle_seconds", 0)),
    #         "brightness": float(s.get("screen_brightness", 50)),
    #         "webcam": bool(s.get("webcam_active", False)),
    #         "audio": bool(s.get("audio_playing", False)),
    #         "fullscreen": bool(s.get("fullscreen", False)),
    #     }
    def _normalize(self, s: Dict) -> Dict:
        title = (s.get("active_window") or "").lower()

        # --- Safe brightness normalization ---
        brightness_raw = s.get("screen_brightness", 50)
        try:
            brightness = float(brightness_raw) if brightness_raw is not None else 50
        except Exception:
            brightness = 50

        return {
            "title": title,
            "window": s.get("window_category", "other"),
            "typing": float(s.get("keypress_rate", 0)),
            "mouse": float(s.get("mouse_rate", 0)),
            "scroll": float(s.get("scroll_rate", 0)),
            "switches": float(s.get("window_switches", 0)),
            "idle": float(s.get("idle_seconds", 0)),
            "brightness": brightness,   # ← safe value
            "webcam": bool(s.get("webcam_active", False)),
            "audio": bool(s.get("audio_playing", False)),
            "fullscreen": bool(s.get("fullscreen", False)),
        }

    # RULES ---------------------------------------------------

    def _rule_away(self, s):
        if s["idle"] > self.t["away_idle"]:
            return BehaviorResult("Away", 0.95, s)

    def _rule_meeting(self, s):
        if s["webcam"] or s["window"] == "meeting":
            return BehaviorResult("Meeting", 0.9, s)

    def _rule_eye_strain_risk(self, s):
        if s["brightness"] > self.t["brightness_high"] and s["idle"] < self.t["idle"]:
            return BehaviorResult("Eye Strain Risk", 0.85, s)

    # --- Gaming ----------------------------------------------

    def _rule_gaming(self, s):
        title = s["title"]
        if any(kw in title for kw in GAMING_KEYWORDS):
            # Low typing, moderate mouse, often fullscreen
            if s["typing"] < self.t["low_typing"] and s["mouse"] >= self.t["low_mouse"]:
                return BehaviorResult("Gaming", 0.9, s)

    # --- Music Production ------------------------------------

    def _rule_music_production(self, s):
        title = s["title"]
        if any(kw in title for kw in MUSIC_KEYWORDS):
            # Moderate mouse, low typing, often audio playing
            if s["mouse"] >= self.t["low_mouse"] and s["typing"] < self.t["medium_typing"]:
                return BehaviorResult("Music Production", 0.85, s)

    # --- Video Editing ---------------------------------------

    def _rule_video_editing(self, s):
        title = s["title"]
        if any(kw in title for kw in VIDEO_EDITING_KEYWORDS):
            # High mouse, low typing, often fullscreen or video window
            if s["mouse"] >= self.t["low_mouse"] and s["typing"] < self.t["medium_typing"]:
                return BehaviorResult("Video Editing", 0.85, s)

    # --- PDF / Word / PowerPoint reading ---------------------

    def _rule_pdf_word_ppt_reading(self, s):
        title = s["title"]

        is_pdf = ".pdf" in title
        is_word = "word" in title or title.endswith(".doc") or title.endswith(".docx")
        is_ppt = "powerpoint" in title or title.endswith(".ppt") or title.endswith(".pptx")

        in_doc_env = is_pdf or is_word or is_ppt or s["window"] == "office"

        if not in_doc_env:
            return None

        # Writing in Word
        if is_word and s["typing"] > self.t["high_typing"]:
            return BehaviorResult("Writing", 0.9, s)

        # Slide reading
        if is_ppt:
            if s["typing"] < 20 and s["scroll"] < 15 and s["switches"] < 5:
                if s["typing"] < 10 and s["mouse"] < 20 and s["switches"] < 2:
                    return BehaviorResult("Deep Reading", 0.9, s)
                return BehaviorResult("Reading", 0.85, s)

        # PDF / Word reading
        if s["scroll"] > 5 and s["typing"] < 30 and s["switches"] < 8:
            if (
                s["scroll"] < self.t["deep_reading_scroll_max"]
                and s["mouse"] < self.t["deep_reading_mouse_max"]
                and s["switches"] < self.t["deep_reading_switch_max"]
                and s["typing"] < 15
            ):
                return BehaviorResult("Deep Reading", 0.9, s)
            return BehaviorResult("Reading", 0.85, s)

    # --- Browser PDF reading ---------------------------------

    def _rule_browser_pdf_reading(self, s):
        if ".pdf" not in s["title"]:
            return None

        if s["scroll"] > 5 and s["typing"] < 30 and s["switches"] < 8:
            if (
                s["scroll"] < self.t["deep_reading_scroll_max"]
                and s["mouse"] < self.t["deep_reading_mouse_max"]
                and s["switches"] < self.t["deep_reading_switch_max"]
                and s["typing"] < 15
            ):
                return BehaviorResult("Deep Reading", 0.9, s)
            return BehaviorResult("Reading", 0.85, s)

    # --- Watching (expanded) ---------------------------------

    def _rule_watching(self, s):
        title = s["title"]

        if any(kw in title for kw in WATCHING_KEYWORDS):
            if s["typing"] < self.t["low_typing"]:
                return BehaviorResult("Watching", 0.9, s)

        if s["window"] == "video" and s["typing"] < self.t["low_typing"]:
            return BehaviorResult("Watching", 0.85, s)

    # --- Coding / Writing (expanded) -------------------------

    def _rule_coding_writing(self, s):
        title = s["title"]

        # Coding / data-science / math tools
        if any(kw in title for kw in CODING_KEYWORDS):
            if s["typing"] > self.t["low_typing"]:
                return BehaviorResult("Coding", 0.9, s)
            else:
                return BehaviorResult("Deep Work", 0.8, s)

        # High typing in coding window
        if s["typing"] > self.t["high_typing"]:
            if s["window"] == "coding":
                return BehaviorResult("Coding", 0.9, s)
            return BehaviorResult("Writing", 0.85, s)

    # --- Deep Work (expanded) --------------------------------

    def _rule_deep_work(self, s):
        title = s["title"]

        # Deep work in coding / data-science / math tools
        if any(kw in title for kw in CODING_KEYWORDS):
            if s["typing"] > self.t["medium_typing"] and s["switches"] < 5:
                return BehaviorResult("Deep Work", 0.85, s)

        # Generic deep work pattern
        if s["typing"] > self.t["medium_typing"] and s["mouse"] < self.t["medium_typing"]:
            if s["switches"] < 5:
                return BehaviorResult("Deep Work", 0.8, s)

    # --- Multitasking ----------------------------------------

    def _rule_multitasking(self, s):
        if s["mouse"] > self.t["high_mouse"] and s["typing"] > self.t["medium_typing"]:
            return BehaviorResult("Multitasking", 0.8, s)

    # --- Focused Interaction (AI assistants) -----------------

    def _rule_focused_interaction(self, s):
        title = s["title"]
        if not any(
            kw in title
            for kw in ["chatgpt", "copilot", "gemini", "claude", "bard", "perplexity"]
        ):
            return None

        if 5 <= s["typing"] <= 40 and 5 <= s["scroll"] <= 40 and s["switches"] < 8:
            if s["mouse"] < 40:
                return BehaviorResult("Focused Interaction", 0.85, s)
    # --- Browsing (expanded) ---------------------------------

    def _rule_heavy_browsing(self, s):
        title = s["title"]

        # Research / writing / dev / social / learning tools
        if any(kw in title for kw in BROWSING_KEYWORDS):
            if s["typing"] >= self.t["medium_typing"]:
                return BehaviorResult("Heavy Browsing", 0.8, s)

        # Generic heavy browsing
        if s["window"] == "browser" and s["typing"] >= self.t["medium_typing"]:
            return BehaviorResult("Heavy Browsing", 0.75, s)

    def _rule_light_browsing(self, s):
        title = s["title"]

        # Research / writing / dev / social / learning tools
        if any(kw in title for kw in BROWSING_KEYWORDS):
            if s["typing"] < self.t["medium_typing"]:
                return BehaviorResult("Light Browsing", 0.75, s)

        # Generic light browsing
        if s["window"] == "browser" and s["typing"] < self.t["medium_typing"]:
            return BehaviorResult("Light Browsing", 0.7, s)

    # --- Posture Risk ----------------------------------------

    def _rule_posture_risk(self, s):
        if s["idle"] > 45 and s["typing"] > self.t["medium_typing"]:
            return BehaviorResult("Posture Risk", 0.7, s)

    # --- Fatigued Activity -----------------------------------

    def _rule_fatigued_activity(self, s):
        if (
            s["typing"] < self.t["low_typing"]
            and s["mouse"] < self.t["low_mouse"]
            and s["idle"] < self.t["idle"]
        ):
            return BehaviorResult("Fatigued Activity", 0.6, s)

    # --- Idle -------------------------------------------------

    def _rule_idle(self, s):
        if s["typing"] == 0 and s["mouse"] == 0:
            return BehaviorResult("Idle", 0.6, s)
