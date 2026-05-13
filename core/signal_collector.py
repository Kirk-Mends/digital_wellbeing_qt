# signal_collector.py
# This file collects all the signals we need for behavior detection.
# It tracks typing, mouse movement, scrolling, window changes, etc.

# import time
# from collections import deque
# import keyboard
# import mouse
# import ctypes
# from dataclasses import dataclass

# # Windows API for window info
# user32 = ctypes.windll.user32


# # get the title of the active window
# def get_active_window_title() -> str:
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return ""
#     length = user32.GetWindowTextLengthW(hwnd)
#     buff = ctypes.create_unicode_buffer(length + 1)
#     user32.GetWindowTextW(hwnd, buff, length + 1)
#     return buff.value or ""


# # get window rectangle (used for fullscreen check)
# def get_window_rect(hwnd):
#     rect = ctypes.wintypes.RECT()
#     user32.GetWindowRect(hwnd, ctypes.byref(rect))
#     return rect.left, rect.top, rect.right, rect.bottom


# # check if the active window is fullscreen
# def is_fullscreen() -> bool:
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return False
#     left, top, right, bottom = get_window_rect(hwnd)
#     screen_w = user32.GetSystemMetrics(0)
#     screen_h = user32.GetSystemMetrics(1)
#     return left <= 0 and top <= 0 and right >= screen_w and bottom >= screen_h


# @dataclass
# class ActivitySnapshot:
#     idle_seconds: float
#     active_window: str
#     is_fullscreen: bool
#     screen_locked: bool
#     screen_dimmed: bool
#     has_audio: bool
#     keypress_rate: float
#     mouse_move_rate: float
#     scroll_rate: float
#     window_switch_rate: float


# class SignalCollector:
#     """
#     Modern signal collector for the hybrid SmartBreakEngine.
#     Tracks:
#     - keypress rate
#     - mouse movement rate
#     - scroll rate
#     - window switch rate
#     - idle time
#     - fullscreen
#     - active window
#     """

#     def __init__(self, history_seconds: float = 60.0):
#         # how long we keep event history
#         self.history_seconds = history_seconds

#         # last time user touched keyboard/mouse
#         self.last_activity = time.time()

#         # event history queues
#         self.key_times = deque()
#         self.mouse_move_times = deque()
#         self.scroll_times = deque()
#         self.window_switch_times = deque()

#         # track active window name
#         self.last_window = get_active_window_title()

#         # input detection flag
#         self.input_detected = False

#         # hook keyboard and mouse
#         keyboard.on_press(self._on_key)
#         mouse.hook(self._on_mouse)

#     # when user presses a key
#     def _on_key(self, event):
#         now = time.time()
#         self.last_activity = now
#         self.key_times.append(now)
#         self.input_detected = True

#     # when user moves mouse or scrolls
#     def _on_mouse(self, event):
#         now = time.time()
#         self.last_activity = now
#         et = getattr(event, "event_type", "")
#         if et == "move":
#             self.mouse_move_times.append(now)
#         elif et == "wheel":
#             self.scroll_times.append(now)
#         self.input_detected = True

#     # remove old events from history
#     def _prune(self, dq: deque):
#         cutoff = time.time() - self.history_seconds
#         while dq and dq[0] < cutoff:
#             dq.popleft()

#     # detect window switching
#     def _update_window_switch(self):
#         now = time.time()
#         current = get_active_window_title()
#         if current != self.last_window:
#             self.window_switch_times.append(now)
#             self.last_window = current

#     # NEW: update internal state every cycle
#     def update(self):
#         """
#         Called once per engine loop (every 1 second).
#         Cleans history, updates window switch, and resets input flag.
#         """
#         now = time.time()

#         # prune old events
#         self._prune(self.key_times)
#         self._prune(self.mouse_move_times)
#         self._prune(self.scroll_times)
#         self._update_window_switch()
#         self._prune(self.window_switch_times)

#         # reset input flag for next cycle
#         self.input_detected = False

#     # NEW: convert current signals to dictionary for SmartBreakEngine
#     def to_dict(self):
#         now = time.time()
#         idle_seconds = now - self.last_activity

#         # convert counts to rates per minute
#         window_seconds = max(self.history_seconds, 1.0)

#         keypress_rate = len(self.key_times) * 60.0 / window_seconds
#         mouse_move_rate = len(self.mouse_move_times) * 60.0 / window_seconds
#         scroll_rate = len(self.scroll_times) * 60.0 / window_seconds
#         window_switch_rate = len(self.window_switch_times) * 60.0 / window_seconds

#         return {
#             "idle_seconds": idle_seconds,
#             "active_window": self.last_window or "",
#             "fullscreen": is_fullscreen(),
#             "screen_locked": False,   # placeholder
#             "screen_dimmed": False,   # placeholder
#             "audio_playing": False,   # placeholder
#             "keypress_rate": keypress_rate,
#             "mouse_rate": mouse_move_rate,
#             "scroll_rate": scroll_rate,
#             "window_switches": window_switch_rate,
#         }

#     # compatibility with old code (optional)
#     def get_snapshot(self):
#         d = self.to_dict()
#         return ActivitySnapshot(
#             idle_seconds=d["idle_seconds"],
#             active_window=d["active_window"],
#             is_fullscreen=d["fullscreen"],
#             screen_locked=d["screen_locked"],
#             screen_dimmed=d["screen_dimmed"],
#             has_audio=d["audio_playing"],
#             keypress_rate=d["keypress_rate"],
#             mouse_move_rate=d["mouse_rate"],
#             scroll_rate=d["scroll_rate"],
#             window_switch_rate=d["window_switches"],
#         )






# from microphone_detector import is_microphone_in_use
# from webcam_detector import is_webcam_in_use
# from pynput import keyboard, mouse
# import time
# from collections import deque
# import ctypes

# user32 = ctypes.windll.user32

# def get_active_window_title():
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return ""
#     length = user32.GetWindowTextLengthW(hwnd)
#     buff = ctypes.create_unicode_buffer(length + 1)
#     user32.GetWindowTextW(hwnd, buff, length + 1)
#     return buff.value or ""

# def is_fullscreen():
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return False
#     rect = ctypes.wintypes.RECT()
#     user32.GetWindowRect(hwnd, ctypes.byref(rect))
#     screen_w = user32.GetSystemMetrics(0)
#     screen_h = user32.GetSystemMetrics(1)
#     return rect.left <= 0 and rect.top <= 0 and rect.right >= screen_w and rect.bottom >= screen_h

# class SignalCollector:
#     def __init__(self, history_seconds=60):
#         self.history_seconds = history_seconds
#         self.last_activity = time.time()

#         self.key_times = deque()
#         self.mouse_move_times = deque()
#         self.scroll_times = deque()
#         self.window_switch_times = deque()

#         self.last_window = get_active_window_title()
#         self.input_detected = False

#         # start listeners
#         self.k_listener = keyboard.Listener(on_press=self._on_key)
#         self.k_listener.start()

#         self.m_listener = mouse.Listener(
#             on_move=self._on_move,
#             on_scroll=self._on_scroll
#         )
#         self.m_listener.start()

#     def _on_key(self, key):
#         now = time.time()
#         self.last_activity = now
#         self.key_times.append(now)
#         self.input_detected = True

#     def _on_move(self, x, y):
#         now = time.time()
#         self.last_activity = now
#         self.mouse_move_times.append(now)
#         self.input_detected = True

#     def _on_scroll(self, x, y, dx, dy):
#         now = time.time()
#         self.last_activity = now
#         self.scroll_times.append(now)
#         self.input_detected = True

#     def _prune(self, dq):
#         cutoff = time.time() - self.history_seconds
#         while dq and dq[0] < cutoff:
#             dq.popleft()

#     def update(self):
#         self._prune(self.key_times)
#         self._prune(self.mouse_move_times)
#         self._prune(self.scroll_times)
#         self._prune(self.window_switch_times)

#         current = get_active_window_title()
#         if current != self.last_window:
#             self.window_switch_times.append(time.time())
#             self.last_window = current

#     def to_dict(self):
#         now = time.time()
#         idle_seconds = now - self.last_activity
#         window_seconds = max(self.history_seconds, 1)

#         return {
#             "idle_seconds": idle_seconds,
#             "active_window": self.last_window,
#             "fullscreen": is_fullscreen(),
#             "screen_locked": False,
#             "screen_dimmed": False,
#             "audio_playing": False,
#             "keypress_rate": len(self.key_times) * 60 / window_seconds,
#             "mouse_rate": len(self.mouse_move_times) * 60 / window_seconds,
#             "scroll_rate": len(self.scroll_times) * 60 / window_seconds,
#             "window_switches": len(self.window_switch_times) * 60 / window_seconds,
#             "webcam_active": is_webcam_in_use(),
#             "microphone_active": is_microphone_in_use(),
#         }














# THIS IS THE CODE USED TO TEST FOR WEBCAM ON BUT WORKED WITH AI FALSE


# import time
# import ctypes
# from collections import deque

# # ------------------------------------------------------------
# # SAFE IMPORTS (bulletproof)
# # ------------------------------------------------------------

# # --- Webcam / Microphone detectors ---
# try:
#     from webcam_detector import is_webcam_in_use
# except:
#     def is_webcam_in_use():
#         return False

# try:
#     from microphone_detector import is_microphone_in_use
# except:
#     def is_microphone_in_use():
#         return False

# # --- Audio detection (pycaw) ---
# try:
#     from pycaw.pycaw import AudioUtilities
# except:
#     AudioUtilities = None

# # --- WMI for screen brightness ---
# try:
#     import wmi
#     wmi_obj = wmi.WMI(namespace='wmi')
# except:
#     wmi_obj = None

# # --- Hybrid input detection ---
# USE_PYNPUT = True
# try:
#     from pynput import keyboard, mouse
# except:
#     USE_PYNPUT = False
#     try:
#         import keyboard as kb_fallback
#         import mouse as ms_fallback
#     except:
#         kb_fallback = None
#         ms_fallback = None

# # ------------------------------------------------------------
# # WINDOWS API HELPERS
# # ------------------------------------------------------------

# user32 = ctypes.windll.user32

# def get_active_window_title():
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return ""
#     length = user32.GetWindowTextLengthW(hwnd)
#     buff = ctypes.create_unicode_buffer(length + 1)
#     user32.GetWindowTextW(hwnd, buff, length + 1)
#     return buff.value or ""

# def is_fullscreen():
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return False
#     rect = ctypes.wintypes.RECT()
#     user32.GetWindowRect(hwnd, ctypes.byref(rect))
#     screen_w = user32.GetSystemMetrics(0)
#     screen_h = user32.GetSystemMetrics(1)
#     return rect.left <= 0 and rect.top <= 0 and rect.right >= screen_w and rect.bottom >= screen_h

# def is_screen_locked():
#     # Windows reports 0 when locked
#     return user32.GetForegroundWindow() == 0

# def get_screen_brightness():
#     if not wmi_obj:
#         return None
#     try:
#         methods = wmi_obj.WmiMonitorBrightness()[0]
#         return methods.CurrentBrightness
#     except:
#         return None

# # ------------------------------------------------------------
# # ACTIVE WINDOW CATEGORY (simple heuristic)
# # ------------------------------------------------------------

# def categorize_window(title: str):
#     t = title.lower()

#     if any(x in t for x in ["chrome", "edge", "firefox"]):
#         return "browser"
#     if any(x in t for x in ["word", "excel", "powerpoint"]):
#         return "office"
#     if "zoom" in t or "teams" in t or "meet" in t:
#         return "meeting"
#     if any(x in t for x in ["youtube", "vlc", "player"]):
#         return "video"
#     if any(x in t for x in ["vs code", "pycharm", "visual studio"]):
#         return "coding"
#     if any(x in t for x in ["game", "steam", "epic"]):
#         return "gaming"

#     return "other"

# # ------------------------------------------------------------
# # SIGNAL COLLECTOR V2
# # ------------------------------------------------------------

# class SignalCollector:
#     def __init__(self, history_seconds=60):
#         self.history_seconds = history_seconds
#         self.last_activity = time.time()

#         # Raw event timestamps
#         self.key_times = deque()
#         self.mouse_move_times = deque()
#         self.scroll_times = deque()
#         self.window_switch_times = deque()

#         # Advanced signals
#         self.typing_bursts = deque()
#         self.mouse_smoothness = deque()
#         self.micro_pauses = deque()

#         self.last_window = get_active_window_title()
#         self.last_mouse_pos = None
#         self.last_key_time = None
#         self.last_move_time = None

#         # Start listeners
#         if USE_PYNPUT:
#             self.k_listener = keyboard.Listener(on_press=self._on_key)
#             self.k_listener.start()

#             self.m_listener = mouse.Listener(
#                 on_move=self._on_move,
#                 on_scroll=self._on_scroll
#             )
#             self.m_listener.start()
#         else:
#             # Fallback listeners
#             if kb_fallback:
#                 kb_fallback.on_press(self._on_key)
#             if ms_fallback:
#                 ms_fallback.on_move(self._on_move)
#                 ms_fallback.on_scroll(self._on_scroll)

#     # --------------------------------------------------------
#     # INPUT HANDLERS
#     # --------------------------------------------------------

#     def _on_key(self, key):
#         now = time.time()
#         self.last_activity = now
#         self.key_times.append(now)

#         # Typing burst detection
#         if self.last_key_time:
#             interval = now - self.last_key_time
#             if interval < 0.4:  # fast typing
#                 self.typing_bursts.append(now)
#         self.last_key_time = now

#     def _on_move(self, x, y):
#         now = time.time()
#         self.last_activity = now
#         self.mouse_move_times.append(now)

#         # Mouse smoothness detection
#         if self.last_mouse_pos:
#             dx = x - self.last_mouse_pos[0]
#             dy = y - self.last_mouse_pos[1]
#             dist = (dx*dx + dy*dy)**0.5
#             self.mouse_smoothness.append(dist)
#         self.last_mouse_pos = (x, y)

#     def _on_scroll(self, x, y, dx, dy):
#         now = time.time()
#         self.last_activity = now
#         self.scroll_times.append(now)

#     # --------------------------------------------------------
#     # INTERNAL HELPERS
#     # --------------------------------------------------------

#     def _prune(self, dq):
#         cutoff = time.time() - self.history_seconds
#         while dq and dq[0] < cutoff:
#             dq.popleft()

#     def _detect_micro_pause(self):
#         now = time.time()
#         idle = now - self.last_activity
#         if 1 <= idle <= 10:
#             self.micro_pauses.append(now)

#     # --------------------------------------------------------
#     # UPDATE LOOP
#     # --------------------------------------------------------

#     def update(self):
#         # Prune all queues
#         for dq in [
#             self.key_times,
#             self.mouse_move_times,
#             self.scroll_times,
#             self.window_switch_times,
#             self.typing_bursts,
#             self.mouse_smoothness,
#             self.micro_pauses
#         ]:
#             self._prune(dq)

#         # Window switching
#         current = get_active_window_title()
#         if current != self.last_window:
#             self.window_switch_times.append(time.time())
#             self.last_window = current

#         # Micro-pause detection
#         self._detect_micro_pause()

#     # --------------------------------------------------------
#     # OUTPUT SNAPSHOT
#     # --------------------------------------------------------

#     def to_dict(self):
#         now = time.time()
#         idle_seconds = now - self.last_activity
#         window_seconds = max(self.history_seconds, 1)

#         # Audio detection
#         audio_playing = False
#         if AudioUtilities:
#             try:
#                 sessions = AudioUtilities.GetAllSessions()
#                 audio_playing = any(s.SimpleAudioVolume.GetMasterVolume() > 0 for s in sessions)
#             except:
#                 audio_playing = False

#         brightness = get_screen_brightness()

#         return {
#             # Core signals
#             "idle_seconds": idle_seconds,
#             "active_window": self.last_window,
#             "window_category": categorize_window(self.last_window),
#             "fullscreen": is_fullscreen(),

#             # System signals
#             "screen_locked": is_screen_locked(),
#             "screen_brightness": brightness,
#             "screen_dimmed": brightness is not None and brightness < 20,

#             # Audio / video
#             "audio_playing": audio_playing,
#             "webcam_active": is_webcam_in_use(),
#             "microphone_active": is_microphone_in_use(),

#             # Rates
#             "keypress_rate": len(self.key_times) * 60 / window_seconds,
#             "mouse_rate": len(self.mouse_move_times) * 60 / window_seconds,
#             "scroll_rate": len(self.scroll_times) * 60 / window_seconds,
#             "window_switches": len(self.window_switch_times) * 60 / window_seconds,

#             # Advanced signals
#             "typing_burst_rate": len(self.typing_bursts) * 60 / window_seconds,
#             "mouse_smoothness_avg": (
#                 sum(self.mouse_smoothness) / len(self.mouse_smoothness)
#                 if self.mouse_smoothness else 0
#             ),
#             "micro_pause_rate": len(self.micro_pauses) * 60 / window_seconds,
#         }









# # TESTING 1
# import time
# import ctypes
# from collections import deque

# # ------------------------------------------------------------
# # SAFE IMPORTS (bulletproof)
# # ------------------------------------------------------------

# try:
#     from webcam_detector import is_webcam_in_use
# except:
#     def is_webcam_in_use():
#         return False

# try:
#     from microphone_detector import is_microphone_in_use
# except:
#     def is_microphone_in_use():
#         return False

# try:
#     from pycaw.pycaw import AudioUtilities
# except:
#     AudioUtilities = None

# try:
#     import wmi
#     wmi_obj = wmi.WMI(namespace='wmi')
# except:
#     wmi_obj = None

# USE_PYNPUT = True
# try:
#     from pynput import keyboard, mouse
# except:
#     USE_PYNPUT = False
#     try:
#         import keyboard as kb_fallback
#         import mouse as ms_fallback
#     except:
#         kb_fallback = None
#         ms_fallback = None

# # ------------------------------------------------------------
# # WINDOWS API HELPERS
# # ------------------------------------------------------------

# user32 = ctypes.windll.user32

# def get_active_window_title():
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return ""
#     length = user32.GetWindowTextLengthW(hwnd)
#     buff = ctypes.create_unicode_buffer(length + 1)
#     user32.GetWindowTextW(hwnd, buff, length + 1)
#     return buff.value or ""

# def is_fullscreen():
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return False
#     rect = ctypes.wintypes.RECT()
#     user32.GetWindowRect(hwnd, ctypes.byref(rect))
#     screen_w = user32.GetSystemMetrics(0)
#     screen_h = user32.GetSystemMetrics(1)
#     return rect.left <= 0 and rect.top <= 0 and rect.right >= screen_w and rect.bottom >= screen_h

# def is_screen_locked():
#     return user32.GetForegroundWindow() == 0

# def get_screen_brightness():
#     if not wmi_obj:
#         return None
#     try:
#         methods = wmi_obj.WmiMonitorBrightness()[0]
#         return methods.CurrentBrightness
#     except:
#         return None

# # ------------------------------------------------------------
# # ACTIVE WINDOW CATEGORY (simple heuristic)
# # ------------------------------------------------------------

# def categorize_window(title: str):
#     t = title.lower()

#     if any(x in t for x in ["chrome", "edge", "firefox"]):
#         return "browser"
#     if any(x in t for x in ["word", "excel", "powerpoint"]):
#         return "office"
#     if "zoom" in t or "teams" in t or "meet" in t:
#         return "meeting"
#     if any(x in t for x in ["youtube", "vlc", "player"]):
#         return "video"
#     if any(x in t for x in ["vs code", "pycharm", "visual studio"]):
#         return "coding"
#     if any(x in t for x in ["game", "steam", "epic"]):
#         return "gaming"

#     return "other"

# # ------------------------------------------------------------
# # SIGNAL COLLECTOR V2 (PATCHED)
# # ------------------------------------------------------------

# class SignalCollector:
#     def __init__(self, history_seconds=60):
#         self.history_seconds = history_seconds
#         self.last_activity = time.time()

#         # Raw event timestamps
#         self.key_times = deque()
#         self.mouse_move_times = deque()
#         self.scroll_times = deque()
#         self.window_switch_times = deque()

#         # Advanced signals
#         self.typing_bursts = deque()
#         self.mouse_smoothness = deque()
#         self.micro_pauses = deque()

#         self.last_window = get_active_window_title()
#         self.last_mouse_pos = None
#         self.last_key_time = None

#         # NEW: flag for v1 engine
#         self.input_detected = False

#         # Start listeners
#         if USE_PYNPUT:
#             self.k_listener = keyboard.Listener(on_press=self._on_key)
#             self.k_listener.start()

#             self.m_listener = mouse.Listener(
#                 on_move=self._on_move,
#                 on_scroll=self._on_scroll
#             )
#             self.m_listener.start()
#         else:
#             if kb_fallback:
#                 kb_fallback.on_press(self._on_key)
#             if ms_fallback:
#                 ms_fallback.on_move(self._on_move)
#                 ms_fallback.on_scroll(self._on_scroll)

#     # --------------------------------------------------------
#     # INPUT HANDLERS (PATCHED)
#     # --------------------------------------------------------

#     def _on_key(self, key):
#         now = time.time()
#         self.last_activity = now
#         self.key_times.append(now)
#         self.input_detected = True

#         if self.last_key_time:
#             interval = now - self.last_key_time
#             if interval < 0.4:  # fast typing
#                 self.typing_bursts.append(now)
#         self.last_key_time = now

#     def _on_move(self, x, y):
#         now = time.time()
#         self.last_activity = now
#         self.mouse_move_times.append(now)
#         self.input_detected = True

#         if self.last_mouse_pos:
#             dx = x - self.last_mouse_pos[0]
#             dy = y - self.last_mouse_pos[1]
#             dist = (dx*dx + dy*dy)**0.5
#             self.mouse_smoothness.append(dist)
#         self.last_mouse_pos = (x, y)

#     def _on_scroll(self, x, y, dx, dy):
#         now = time.time()
#         self.last_activity = now
#         self.scroll_times.append(now)
#         self.input_detected = True

#     # --------------------------------------------------------
#     # INTERNAL HELPERS
#     # --------------------------------------------------------

#     def _prune(self, dq):
#         cutoff = time.time() - self.history_seconds
#         while dq and dq[0] < cutoff:
#             dq.popleft()

#     def _detect_micro_pause(self):
#         now = time.time()
#         idle = now - self.last_activity
#         if 1 <= idle <= 10:
#             self.micro_pauses.append(now)

#     # --------------------------------------------------------
#     # UPDATE LOOP (PATCHED)
#     # --------------------------------------------------------

#     def update(self):
#         # reset input flag for this cycle
#         self.input_detected = False

#         for dq in [
#             self.key_times,
#             self.mouse_move_times,
#             self.scroll_times,
#             self.window_switch_times,
#             self.typing_bursts,
#             self.mouse_smoothness,
#             self.micro_pauses
#         ]:
#             self._prune(dq)

#         current = get_active_window_title()
#         if current != self.last_window:
#             self.window_switch_times.append(time.time())
#             self.last_window = current

#         self._detect_micro_pause()

#     # --------------------------------------------------------
#     # OUTPUT SNAPSHOT
#     # --------------------------------------------------------

#     def to_dict(self):
#         now = time.time()
#         idle_seconds = now - self.last_activity
#         window_seconds = max(self.history_seconds, 1)

#         audio_playing = False
#         if AudioUtilities:
#             try:
#                 sessions = AudioUtilities.GetAllSessions()
#                 audio_playing = any(s.SimpleAudioVolume.GetMasterVolume() > 0 for s in sessions)
#             except:
#                 audio_playing = False

#         brightness = get_screen_brightness()

#         return {
#             "idle_seconds": idle_seconds,
#             "active_window": self.last_window,
#             "window_category": categorize_window(self.last_window),
#             "fullscreen": is_fullscreen(),
#             "screen_locked": is_screen_locked(),
#             "screen_brightness": brightness,
#             "screen_dimmed": brightness is not None and brightness < 20,
#             "audio_playing": audio_playing,
#             "webcam_active": is_webcam_in_use(),
#             "microphone_active": is_microphone_in_use(),
#             "keypress_rate": len(self.key_times) * 60 / window_seconds,
#             "mouse_rate": len(self.mouse_move_times) * 60 / window_seconds,
#             "scroll_rate": len(self.scroll_times) * 60 / window_seconds,
#             "window_switches": len(self.window_switch_times) * 60 / window_seconds,
#             "typing_burst_rate": len(self.typing_bursts) * 60 / window_seconds,
#             "mouse_smoothness_avg": (
#                 sum(self.mouse_smoothness) / len(self.mouse_smoothness)
#                 if self.mouse_smoothness else 0
#             ),
#             "micro_pause_rate": len(self.micro_pauses) * 60 / window_seconds,
#         }









# #TEST 2
# import time
# import ctypes
# from collections import deque

# # ------------------------------------------------------------
# # SAFE IMPORTS (bulletproof)
# # ------------------------------------------------------------

# try:
#     from webcam_detector import is_webcam_in_use
# except:
#     def is_webcam_in_use():
#         return False

# try:
#     from microphone_detector import is_microphone_in_use
# except:
#     def is_microphone_in_use():
#         return False

# try:
#     from pycaw.pycaw import AudioUtilities
# except:
#     AudioUtilities = None

# try:
#     import wmi
#     wmi_obj = wmi.WMI(namespace='wmi')
# except:
#     wmi_obj = None

# USE_PYNPUT = True
# try:
#     from pynput import keyboard, mouse
# except:
#     USE_PYNPUT = False
#     try:
#         import keyboard as kb_fallback
#         import mouse as ms_fallback
#     except:
#         kb_fallback = None
#         ms_fallback = None

# # ------------------------------------------------------------
# # WINDOWS API HELPERS
# # ------------------------------------------------------------

# user32 = ctypes.windll.user32

# def get_active_window_title():
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return ""
#     length = user32.GetWindowTextLengthW(hwnd)
#     buff = ctypes.create_unicode_buffer(length + 1)
#     user32.GetWindowTextW(hwnd, buff, length + 1)
#     return buff.value or ""

# def is_fullscreen():
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return False
#     rect = ctypes.wintypes.RECT()
#     user32.GetWindowRect(hwnd, ctypes.byref(rect))
#     screen_w = user32.GetSystemMetrics(0)
#     screen_h = user32.GetSystemMetrics(1)
#     return rect.left <= 0 and rect.top <= 0 and rect.right >= screen_w and rect.bottom >= screen_h

# def is_screen_locked():
#     return user32.GetForegroundWindow() == 0

# def get_screen_brightness():
#     if not wmi_obj:
#         return None
#     try:
#         methods = wmi_obj.WmiMonitorBrightness()[0]
#         return methods.CurrentBrightness
#     except:
#         return None

# # ------------------------------------------------------------
# # ACTIVE WINDOW CATEGORY
# # ------------------------------------------------------------

# def categorize_window(title: str):
#     t = title.lower()

#     if any(x in t for x in ["chrome", "edge", "firefox"]):
#         return "browser"
#     if any(x in t for x in ["word", "excel", "powerpoint"]):
#         return "office"
#     if "zoom" in t or "teams" in t or "meet" in t:
#         return "meeting"
#     if any(x in t for x in ["youtube", "vlc", "player"]):
#         return "video"
#     if any(x in t for x in ["vs code", "pycharm", "visual studio"]):
#         return "coding"
#     if any(x in t for x in ["game", "steam", "epic"]):
#         return "gaming"

#     return "other"

# # ------------------------------------------------------------
# # SIGNAL COLLECTOR V2
# # ------------------------------------------------------------

# class SignalCollector:
#     def __init__(self, history_seconds=60):
#         self.history_seconds = history_seconds
#         self.last_activity = time.time()

#         # Raw event timestamps
#         self.key_times = deque()
#         self.mouse_move_times = deque()
#         self.scroll_times = deque()
#         self.window_switch_times = deque()

#         # Advanced signals
#         self.typing_bursts = deque()
#         self.mouse_smoothness = deque()
#         self.micro_pauses = deque()

#         self.last_window = get_active_window_title()
#         self.last_mouse_pos = None
#         self.last_key_time = None

#         # Flag used by SmartBreakEngine v1
#         self.input_detected = False

#         # Start listeners
#         if USE_PYNPUT:
#             self.k_listener = keyboard.Listener(on_press=self._on_key)
#             self.k_listener.start()

#             self.m_listener = mouse.Listener(
#                 on_move=self._on_move,
#                 on_scroll=self._on_scroll
#             )
#             self.m_listener.start()
#         else:
#             if kb_fallback:
#                 kb_fallback.on_press(self._on_key)
#             if ms_fallback:
#                 ms_fallback.on_move(self._on_move)
#                 ms_fallback.on_scroll(self._on_scroll)

#     # --------------------------------------------------------
#     # INPUT HANDLERS
#     # --------------------------------------------------------

#     def _on_key(self, key):
#         now = time.time()
#         self.last_activity = now
#         self.key_times.append(now)
#         self.input_detected = True

#         if self.last_key_time:
#             interval = now - self.last_key_time
#             if interval < 0.4:
#                 self.typing_bursts.append(now)
#         self.last_key_time = now

#     def _on_move(self, x, y):
#         now = time.time()
#         self.last_activity = now
#         self.mouse_move_times.append(now)
#         self.input_detected = True

#         if self.last_mouse_pos:
#             dx = x - self.last_mouse_pos[0]
#             dy = y - self.last_mouse_pos[1]
#             dist = (dx*dx + dy*dy)**0.5
#             self.mouse_smoothness.append(dist)
#         self.last_mouse_pos = (x, y)

#     def _on_scroll(self, x, y, dx, dy):
#         now = time.time()
#         self.last_activity = now
#         self.scroll_times.append(now)
#         self.input_detected = True

#     # --------------------------------------------------------
#     # INTERNAL HELPERS
#     # --------------------------------------------------------

#     def _prune(self, dq):
#         cutoff = time.time() - self.history_seconds
#         while dq and dq[0] < cutoff:
#             dq.popleft()

#     def _detect_micro_pause(self):
#         now = time.time()
#         idle = now - self.last_activity
#         if 1 <= idle <= 10:
#             self.micro_pauses.append(now)

#     # --------------------------------------------------------
#     # UPDATE LOOP
#     # --------------------------------------------------------

#     def update(self):
#         # reset input flag each cycle
#         self.input_detected = False

#         for dq in [
#             self.key_times,
#             self.mouse_move_times,
#             self.scroll_times,
#             self.window_switch_times,
#             self.typing_bursts,
#             self.mouse_smoothness,
#             self.micro_pauses
#         ]:
#             self._prune(dq)

#         current = get_active_window_title()
#         if current != self.last_window:
#             self.window_switch_times.append(time.time())
#             self.last_window = current

#         self._detect_micro_pause()

#     # --------------------------------------------------------
#     # OUTPUT SNAPSHOT
#     # --------------------------------------------------------

#     def to_dict(self):
#         now = time.time()
#         idle_seconds = now - self.last_activity
#         window_seconds = max(self.history_seconds, 1)

#         audio_playing = False
#         if AudioUtilities:
#             try:
#                 sessions = AudioUtilities.GetAllSessions()
#                 audio_playing = any(s.SimpleAudioVolume.GetMasterVolume() > 0 for s in sessions)
#             except:
#                 audio_playing = False

#         brightness = get_screen_brightness()

#         return {
#             "idle_seconds": idle_seconds,
#             "active_window": self.last_window,
#             "window_category": categorize_window(self.last_window),
#             "fullscreen": is_fullscreen(),
#             "screen_locked": is_screen_locked(),
#             "screen_brightness": brightness,
#             "screen_dimmed": brightness is not None and brightness < 20,
#             "audio_playing": audio_playing,
#             "webcam_active": is_webcam_in_use(),
#             "microphone_active": is_microphone_in_use(),
#             "keypress_rate": len(self.key_times) * 60 / window_seconds,
#             "mouse_rate": len(self.mouse_move_times) * 60 / window_seconds,
#             "scroll_rate": len(self.scroll_times) * 60 / window_seconds,
#             "window_switches": len(self.window_switch_times) * 60 / window_seconds,
#             "typing_burst_rate": len(self.typing_bursts) * 60 / window_seconds,
#             "mouse_smoothness_avg": (
#                 sum(self.mouse_smoothness) / len(self.mouse_smoothness)
#                 if self.mouse_smoothness else 0
#             ),
#             "micro_pause_rate": len(self.micro_pauses) * 60 / window_seconds,
#         }


































# ---------------------------------------------------------------------WORKED PERFECTLY

# import time
# import ctypes
# from collections import deque

# # ------------------------------------------------------------
# # SAFE IMPORTS (bulletproof)
# # ------------------------------------------------------------

# # --- STRICT MEETING DETECTION (replaces webcam_detector) ---
# import psutil
# import win32gui

# MEETING_APPS = [
#     "Zoom.exe",
#     "Skype.exe",
#     "Webex.exe"
# ]

# # Titles that appear ONLY during real meetings
# MEETING_PATTERNS = [
#     "Zoom Meeting",
#     "Zoom -",
#     "Google Meet",
#     "Meet -",
#     "Microsoft Teams",
#     "Teams Meeting",
#     "Webex Meeting",
#     "Webex -"
# ]

   
# def is_webcam_in_use():
#     """
#     STRICT meeting detection:
#     - Detects REAL meetings only
#     - Zoom/Webex/Skype via process names
#     - Microsoft Teams ONLY when actually in a call/meeting
#     - Browser-based meetings via strict window-title patterns
#     - Ignores background processes, login pages, and non-meeting tabs
#     """
#     #print(">>> STRICT DETECTOR ACTIVE <<<")

#     # 1. Desktop meeting apps (except Teams)
#     for proc in psutil.process_iter(['name']):
#         try:
#             if proc.info['name'] in MEETING_APPS:
#                 return True
#         except:
#             pass

#     # 2. Active window title
#     try:
#         hwnd = win32gui.GetForegroundWindow()
#         title = win32gui.GetWindowText(hwnd).lower()

#         # 2a. Real Teams meeting detection
#         if "microsoft teams" in title and (
#             "meeting" in title or
#             "call" in title or
#             "in a call" in title or
#             "video call" in title or
#             "audio call" in title
#         ):
#             return True

#         # 2b. Strict browser-based meeting detection
#         return any(pattern.lower() in title for pattern in MEETING_PATTERNS)

#     except:
#         return False


# # --- Microphone detector ---
# try:
#     from microphone_detector import is_microphone_in_use
# except:
#     def is_microphone_in_use():
#         return False

# # --- Audio detection (pycaw) ---
# try:
#     from pycaw.pycaw import AudioUtilities
# except:
#     AudioUtilities = None

# # --- WMI for screen brightness ---
# try:
#     import wmi
#     wmi_obj = wmi.WMI(namespace='wmi')
# except:
#     wmi_obj = None

# # --- Hybrid input detection ---
# USE_PYNPUT = True
# try:
#     from pynput import keyboard, mouse
# except:
#     USE_PYNPUT = False
#     try:
#         import keyboard as kb_fallback
#         import mouse as ms_fallback
#     except:
#         kb_fallback = None
#         ms_fallback = None

# # ------------------------------------------------------------
# # WINDOWS API HELPERS
# # ------------------------------------------------------------

# user32 = ctypes.windll.user32

# def get_active_window_title():
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return ""
#     length = user32.GetWindowTextLengthW(hwnd)
#     buff = ctypes.create_unicode_buffer(length + 1)
#     user32.GetWindowTextW(hwnd, buff, length + 1)
#     return buff.value or ""

# def is_fullscreen():
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return False
#     rect = ctypes.wintypes.RECT()
#     user32.GetWindowRect(hwnd, ctypes.byref(rect))
#     screen_w = user32.GetSystemMetrics(0)
#     screen_h = user32.GetSystemMetrics(1)
#     return rect.left <= 0 and rect.top <= 0 and rect.right >= screen_w and rect.bottom >= screen_h

# def is_screen_locked():
#     return user32.GetForegroundWindow() == 0

# def get_screen_brightness():
#     if not wmi_obj:
#         return None
#     try:
#         methods = wmi_obj.WmiMonitorBrightness()[0]
#         return methods.CurrentBrightness
#     except:
#         return None

# # ------------------------------------------------------------
# # ACTIVE WINDOW CATEGORY
# # ------------------------------------------------------------

# def categorize_window(title: str):
#     t = title.lower()

#     if any(x in t for x in ["chrome", "edge", "firefox"]):
#         return "browser"
#     if any(x in t for x in ["word", "excel", "powerpoint"]):
#         return "office"
#     if any(x in t for x in [
#         "zoom meeting",
#         "google meet",
#         "microsoft teams",
#         "teams meeting",
#         "webex meeting"
#     ]):
#         return "meeting"

#     if any(x in t for x in ["youtube", "vlc", "player"]):
#         return "video"
#     if any(x in t for x in ["vs code", "pycharm", "visual studio"]):
#         return "coding"
#     if any(x in t for x in ["game", "steam", "epic"]):
#         return "gaming"

#     return "other"

# # ------------------------------------------------------------
# # SIGNAL COLLECTOR V2
# # ------------------------------------------------------------

# class SignalCollector:
#     def __init__(self, history_seconds=60):
#         self.history_seconds = history_seconds
#         self.last_activity = time.time()

#         # Raw event timestamps
#         self.key_times = deque()
#         self.mouse_move_times = deque()
#         self.scroll_times = deque()
#         self.window_switch_times = deque()

#         # Advanced signals
#         self.typing_bursts = deque()
#         self.mouse_smoothness = deque()
#         self.micro_pauses = deque()

#         self.last_window = get_active_window_title()
#         self.last_mouse_pos = None
#         self.last_key_time = None
#         self.last_move_time = None

#         # Start listeners
#         if USE_PYNPUT:
#             self.k_listener = keyboard.Listener(on_press=self._on_key)
#             self.k_listener.start()

#             self.m_listener = mouse.Listener(
#                 on_move=self._on_move,
#                 on_scroll=self._on_scroll
#             )
#             self.m_listener.start()
#         else:
#             if kb_fallback:
#                 kb_fallback.on_press(self._on_key)
#             if ms_fallback:
#                 ms_fallback.on_move(self._on_move)
#                 ms_fallback.on_scroll(self._on_scroll)

#     # --------------------------------------------------------
#     # INPUT HANDLERS
#     # --------------------------------------------------------

#     def _on_key(self, key):
#         now = time.time()
#         self.last_activity = now
#         self.key_times.append(now)

#         if self.last_key_time:
#             interval = now - self.last_key_time
#             if interval < 0.4:
#                 self.typing_bursts.append(now)
#         self.last_key_time = now

#     def _on_move(self, x, y):
#         now = time.time()
#         self.last_activity = now
#         self.mouse_move_times.append(now)

#         if self.last_mouse_pos:
#             dx = x - self.last_mouse_pos[0]
#             dy = y - self.last_mouse_pos[1]
#             dist = (dx*dx + dy*dy)**0.5
#             self.mouse_smoothness.append(dist)
#         self.last_mouse_pos = (x, y)

#     def _on_scroll(self, x, y, dx, dy):
#         now = time.time()
#         self.last_activity = now
#         self.scroll_times.append(now)

#     # --------------------------------------------------------
#     # INTERNAL HELPERS
#     # --------------------------------------------------------

#     def _prune(self, dq):
#         cutoff = time.time() - self.history_seconds
#         while dq and dq[0] < cutoff:
#             dq.popleft()

#     def _detect_micro_pause(self):
#         now = time.time()
#         idle = now - self.last_activity
#         if 1 <= idle <= 10:
#             self.micro_pauses.append(now)

#     # --------------------------------------------------------
#     # UPDATE LOOP
#     # --------------------------------------------------------

#     def update(self):
#         for dq in [
#             self.key_times,
#             self.mouse_move_times,
#             self.scroll_times,
#             self.window_switch_times,
#             self.typing_bursts,
#             self.mouse_smoothness,
#             self.micro_pauses
#         ]:
#             self._prune(dq)

#         current = get_active_window_title()
#         if current != self.last_window:
#             self.window_switch_times.append(time.time())
#             self.last_window = current

#         self._detect_micro_pause()

#     # --------------------------------------------------------
#     # OUTPUT SNAPSHOT
#     # --------------------------------------------------------

#     def to_dict(self):
#         now = time.time()
#         idle_seconds = now - self.last_activity
#         window_seconds = max(self.history_seconds, 1)

#         audio_playing = False
#         if AudioUtilities:
#             try:
#                 sessions = AudioUtilities.GetAllSessions()
#                 audio_playing = any(s.SimpleAudioVolume.GetMasterVolume() > 0 for s in sessions)
#             except:
#                 audio_playing = False

#         brightness = get_screen_brightness()

#         return {
#             "idle_seconds": idle_seconds,
#             "active_window": self.last_window,
#             "window_category": categorize_window(self.last_window),
#             "fullscreen": is_fullscreen(),

#             "screen_locked": is_screen_locked(),
#             "screen_brightness": brightness,
#             "screen_dimmed": brightness is not None and brightness < 20,

#             "audio_playing": audio_playing,
#             "webcam_active": is_webcam_in_use(),  # STRICT meeting detection
#             "microphone_active": is_microphone_in_use(),

#             "keypress_rate": len(self.key_times) * 60 / window_seconds,
#             "mouse_rate": len(self.mouse_move_times) * 60 / window_seconds,
#             "scroll_rate": len(self.scroll_times) * 60 / window_seconds,
#             "window_switches": len(self.window_switch_times) * 60 / window_seconds,

#             "typing_burst_rate": len(self.typing_bursts) * 60 / window_seconds,
#             "mouse_smoothness_avg": (
#                 sum(self.mouse_smoothness) / len(self.mouse_smoothness)
#                 if self.mouse_smoothness else 0
#             ),
#             "micro_pause_rate": len(self.micro_pauses) * 60 / window_seconds,
#         }

# --------THE CODE ABOVE WORKED PERFECTLY WITH NO ISSUES--------------
# --------THE CODE ABOVE WORKED PERFECTLY WITH NO ISSUES--------------
# --------THE CODE ABOVE WORKED PERFECTLY WITH NO ISSUES--------------
# --------THE CODE ABOVE WORKED PERFECTLY WITH NO ISSUES--------------
# --------THE CODE ABOVE WORKED PERFECTLY WITH NO ISSUES--------------

# BUT THERE IS ONE ISSUE, THE MEETING STARTS ALRIGHT BUT NEVER DEACTIVATES WHEN MEETING ENDS





















# import time
# import ctypes
# from collections import deque

# # ------------------------------------------------------------
# # SAFE IMPORTS (bulletproof)
# # ------------------------------------------------------------

# # --- STRICT MEETING DETECTION (replaces webcam_detector) ---
# import psutil
# import win32gui

# MEETING_APPS = [
#     "Zoom.exe",
#     "Skype.exe",
#     "Webex.exe"
# ]

# # Titles that appear ONLY during real meetings
# MEETING_PATTERNS = [
#     "Zoom Meeting",
#     "Zoom -",
#     "Google Meet",
#     "Meet -",
#     "Microsoft Teams",
#     "Teams Meeting",
#     "Webex Meeting",
#     "Webex -"
# ]


# def is_webcam_in_use():
#     """
#     STRICT meeting detection (foreground-only):
#     - Detects REAL meetings only
#     - Uses active window title + strict patterns
#     - Ignores background Zoom/Webex/Skype processes
#     - Ignores login pages, idle apps, and non-meeting tabs
#     """
#     try:
#         hwnd = win32gui.GetForegroundWindow()
#         if not hwnd:
#             return False

#         title = win32gui.GetWindowText(hwnd).lower()

#         # Real Teams meeting detection
#         if "microsoft teams" in title and (
#             "meeting" in title
#             or "call" in title
#             or "in a call" in title
#             or "video call" in title
#             or "audio call" in title
#         ):
#             return True

#         # Strict browser/desktop meeting patterns
#         for pattern in MEETING_PATTERNS:
#             if pattern.lower() in title:
#                 return True

#         # If the foreground window is clearly a meeting app window
#         # (Zoom/Webex/Skype) AND looks like a call/meeting
#         for proc in psutil.process_iter(['name']):
#             try:
#                 if proc.info['name'] in MEETING_APPS:
#                     # Only treat as meeting if the active window title
#                     # also looks like a meeting context
#                     if any(p.lower() in title for p in ["meeting", "webinar", "call"]):
#                         return True
#             except:
#                 continue

#         return False

#     except:
#         return False


# # --- Microphone detector ---
# try:
#     from microphone_detector import is_microphone_in_use
# except:
#     def is_microphone_in_use():
#         return False

# # --- Audio detection (pycaw) ---
# try:
#     from pycaw.pycaw import AudioUtilities
# except:
#     AudioUtilities = None

# # --- WMI for screen brightness ---
# try:
#     import wmi
#     wmi_obj = wmi.WMI(namespace='wmi')
# except:
#     wmi_obj = None

# # --- Hybrid input detection ---
# USE_PYNPUT = True
# try:
#     from pynput import keyboard, mouse
# except:
#     USE_PYNPUT = False
#     try:
#         import keyboard as kb_fallback
#         import mouse as ms_fallback
#     except:
#         kb_fallback = None
#         ms_fallback = None

# # ------------------------------------------------------------
# # WINDOWS API HELPERS
# # ------------------------------------------------------------

# user32 = ctypes.windll.user32

# def get_active_window_title():
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return ""
#     length = user32.GetWindowTextLengthW(hwnd)
#     buff = ctypes.create_unicode_buffer(length + 1)
#     user32.GetWindowTextW(hwnd, buff, length + 1)
#     return buff.value or ""

# def is_fullscreen():
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return False
#     rect = ctypes.wintypes.RECT()
#     user32.GetWindowRect(hwnd, ctypes.byref(rect))
#     screen_w = user32.GetSystemMetrics(0)
#     screen_h = user32.GetSystemMetrics(1)
#     return rect.left <= 0 and rect.top <= 0 and rect.right >= screen_w and rect.bottom >= screen_h

# def is_screen_locked():
#     return user32.GetForegroundWindow() == 0

# def get_screen_brightness():
#     if not wmi_obj:
#         return None
#     try:
#         methods = wmi_obj.WmiMonitorBrightness()[0]
#         return methods.CurrentBrightness
#     except:
#         return None

# # ------------------------------------------------------------
# # ACTIVE WINDOW CATEGORY
# # ------------------------------------------------------------

# def categorize_window(title: str):
#     t = title.lower()

#     if any(x in t for x in ["chrome", "edge", "firefox"]):
#         return "browser"
#     if any(x in t for x in ["word", "excel", "powerpoint"]):
#         return "office"
#     if any(x in t for x in [
#         "zoom meeting",
#         "google meet",
#         "microsoft teams",
#         "teams meeting",
#         "webex meeting"
#     ]):
#         return "meeting"

#     if any(x in t for x in ["youtube", "vlc", "player"]):
#         return "video"
#     if any(x in t for x in ["vs code", "pycharm", "visual studio"]):
#         return "coding"
#     if any(x in t for x in ["game", "steam", "epic"]):
#         return "gaming"

#     return "other"

# # ------------------------------------------------------------
# # SIGNAL COLLECTOR V2
# # ------------------------------------------------------------

# class SignalCollector:
#     def __init__(self, history_seconds=60):
#         self.history_seconds = history_seconds
#         self.last_activity = time.time()

#         # Raw event timestamps
#         self.key_times = deque()
#         self.mouse_move_times = deque()
#         self.scroll_times = deque()
#         self.window_switch_times = deque()

#         # Advanced signals
#         self.typing_bursts = deque()
#         self.mouse_smoothness = deque()
#         self.micro_pauses = deque()

#         self.last_window = get_active_window_title()
#         self.last_mouse_pos = None
#         self.last_key_time = None
#         self.last_move_time = None

#         # Start listeners
#         if USE_PYNPUT:
#             self.k_listener = keyboard.Listener(on_press=self._on_key)
#             self.k_listener.start()

#             self.m_listener = mouse.Listener(
#                 on_move=self._on_move,
#                 on_scroll=self._on_scroll
#             )
#             self.m_listener.start()
#         else:
#             if kb_fallback:
#                 kb_fallback.on_press(self._on_key)
#             if ms_fallback:
#                 ms_fallback.on_move(self._on_move)
#                 ms_fallback.on_scroll(self._on_scroll)
            
#         print("Using pynput:", USE_PYNPUT)


#     # --------------------------------------------------------
#     # INPUT HANDLERS
#     # --------------------------------------------------------

#     def _on_key(self, key):
#         now = time.time()
#         self.last_activity = now
#         self.key_times.append(now)

#         if self.last_key_time:
#             interval = now - self.last_key_time
#             if interval < 0.4:
#                 self.typing_bursts.append(now)
#         self.last_key_time = now

#     def _on_move(self, x, y):
#         now = time.time()
#         self.last_activity = now
#         self.mouse_move_times.append(now)

#         if self.last_mouse_pos:
#             dx = x - self.last_mouse_pos[0]
#             dy = y - self.last_mouse_pos[1]
#             dist = (dx*dx + dy*dy)**0.5
#             self.mouse_smoothness.append(dist)
#         self.last_mouse_pos = (x, y)

#     def _on_scroll(self, x, y, dx, dy):
#         now = time.time()
#         self.last_activity = now
#         self.scroll_times.append(now)

#     # --------------------------------------------------------
#     # INTERNAL HELPERS
#     # --------------------------------------------------------

#     def _prune(self, dq):
#         cutoff = time.time() - self.history_seconds
#         while dq and dq[0] < cutoff:
#             dq.popleft()

#     def _detect_micro_pause(self):
#         now = time.time()
#         idle = now - self.last_activity
#         if 1 <= idle <= 10:
#             self.micro_pauses.append(now)

#     # --------------------------------------------------------
#     # UPDATE LOOP
#     # --------------------------------------------------------

#     def update(self):
#         for dq in [
#             self.key_times,
#             self.mouse_move_times,
#             self.scroll_times,
#             self.window_switch_times,
#             self.typing_bursts,
#             self.mouse_smoothness,
#             self.micro_pauses
#         ]:
#             self._prune(dq)

#         current = get_active_window_title()
#         if current != self.last_window:
#             self.window_switch_times.append(time.time())
#             self.last_window = current

#         self._detect_micro_pause()

#     # --------------------------------------------------------
#     # OUTPUT SNAPSHOT
#     # --------------------------------------------------------

#     def to_dict(self):
#         now = time.time()
#         idle_seconds = now - self.last_activity
#         window_seconds = max(self.history_seconds, 1)

#         audio_playing = False
#         if AudioUtilities:
#             try:
#                 sessions = AudioUtilities.GetAllSessions()
#                 audio_playing = any(s.SimpleAudioVolume.GetMasterVolume() > 0 for s in sessions)
#             except:
#                 audio_playing = False

#         brightness = get_screen_brightness()

#         return {
#             "idle_seconds": idle_seconds,
#             "active_window": self.last_window,
#             "window_category": categorize_window(self.last_window),
#             "fullscreen": is_fullscreen(),

#             "screen_locked": is_screen_locked(),
#             "screen_brightness": brightness,
#             "screen_dimmed": brightness is not None and brightness < 20,

#             "audio_playing": audio_playing,
#             "webcam_active": is_webcam_in_use(),  # STRICT, foreground-based
#             "microphone_active": is_microphone_in_use(),

#             "keypress_rate": len(self.key_times) * 60 / window_seconds,
#             "mouse_rate": len(self.mouse_move_times) * 60 / window_seconds,
#             "scroll_rate": len(self.scroll_times) * 60 / window_seconds,
#             "window_switches": len(self.window_switch_times) * 60 / window_seconds,

#             "typing_burst_rate": len(self.typing_bursts) * 60 / window_seconds,
#             "mouse_smoothness_avg": (
#                 sum(self.mouse_smoothness) / len(self.mouse_smoothness)
#                 if self.mouse_smoothness else 0
#             ),
#             "micro_pause_rate": len(self.micro_pauses) * 60 / window_seconds,
#         }

#     def is_user_away(self):
#         """
#         User is considered 'away' if no input for > 120 seconds.
#         Uses the existing idle_seconds value from to_dict().
#         """
#         try:
#             idle = self.to_dict().get("idle_seconds", 0)
#             return idle > 120
#         except:
#             return False

















# 2

# # signal_collector.py

# import time
# import ctypes
# from collections import deque

# # ------------------------------------------------------------
# # SAFE IMPORTS (bulletproof)
# # ------------------------------------------------------------

# # --- STRICT MEETING DETECTION (foreground-only) ---
# import psutil
# import win32gui

# MEETING_APPS = ["Zoom.exe", "Skype.exe", "Webex.exe"]
# MEETING_PATTERNS = [
#     "Zoom Meeting", "Zoom -", "Google Meet", "Meet -",
#     "Microsoft Teams", "Teams Meeting",
#     "Webex Meeting", "Webex -"
# ]


# def is_webcam_in_use():
#     """
#     Detects real meetings using active window title.
#     Ignores background apps or idle windows.
#     """
#     try:
#         hwnd = win32gui.GetForegroundWindow()
#         if not hwnd:
#             return False

#         title = win32gui.GetWindowText(hwnd).lower()

#         if "microsoft teams" in title and any(
#             kw in title for kw in ["meeting", "call", "in a call", "video call", "audio call"]
#         ):
#             return True

#         for pattern in MEETING_PATTERNS:
#             if pattern.lower() in title:
#                 return True

#         for proc in psutil.process_iter(['name']):
#             try:
#                 if proc.info['name'] in MEETING_APPS:
#                     if any(p.lower() in title for p in ["meeting", "webinar", "call"]):
#                         return True
#             except:
#                 continue
#         return False

#     except:
#         return False


# # --- Microphone detector ---
# try:
#     from microphone_detector import is_microphone_in_use
# except:
#     def is_microphone_in_use():
#         return False


# # --- Audio detection (pycaw) ---
# try:
#     from pycaw.pycaw import AudioUtilities
# except:
#     AudioUtilities = None


# # --- WMI for screen brightness ---
# try:
#     import wmi
#     wmi_obj = wmi.WMI(namespace='wmi')
# except:
#     wmi_obj = None


# # --- Hybrid input detection ---
# USE_PYNPUT = True
# try:
#     from pynput import keyboard, mouse
# except:
#     USE_PYNPUT = False
#     try:
#         import keyboard as kb_fallback
#         import mouse as ms_fallback
#     except:
#         kb_fallback = None
#         ms_fallback = None


# # ------------------------------------------------------------
# # WINDOWS API HELPERS
# # ------------------------------------------------------------

# user32 = ctypes.windll.user32

# def get_active_window_title():
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return ""
#     length = user32.GetWindowTextLengthW(hwnd)
#     buff = ctypes.create_unicode_buffer(length + 1)
#     user32.GetWindowTextW(hwnd, buff, length + 1)
#     return buff.value or ""


# def is_fullscreen():
#     hwnd = user32.GetForegroundWindow()
#     if not hwnd:
#         return False
#     rect = ctypes.wintypes.RECT()
#     user32.GetWindowRect(hwnd, ctypes.byref(rect))
#     screen_w = user32.GetSystemMetrics(0)
#     screen_h = user32.GetSystemMetrics(1)
#     return rect.left <= 0 and rect.top <= 0 and rect.right >= screen_w and rect.bottom >= screen_h


# def is_screen_locked():
#     return user32.GetForegroundWindow() == 0


# def get_screen_brightness():
#     if not wmi_obj:
#         return None
#     try:
#         methods = wmi_obj.WmiMonitorBrightness()[0]
#         return methods.CurrentBrightness
#     except:
#         return None


# # ------------------------------------------------------------
# # ACTIVE WINDOW CATEGORY
# # ------------------------------------------------------------

# def categorize_window(title: str):
#     t = title.lower()
#     if any(x in t for x in ["chrome", "edge", "firefox"]):
#         return "browser"
#     if any(x in t for x in ["word", "excel", "powerpoint"]):
#         return "office"
#     if any(x in t for x in [
#         "zoom meeting", "google meet", "microsoft teams", "teams meeting", "webex meeting"
#     ]):
#         return "meeting"
#     if any(x in t for x in ["youtube", "vlc", "player"]):
#         return "video"
#     if any(x in t for x in ["vs code", "pycharm", "visual studio"]):
#         return "coding"
#     if any(x in t for x in ["game", "steam", "epic"]):
#         return "gaming"
#     return "other"


# # ------------------------------------------------------------
# # SIGNAL COLLECTOR
# # ------------------------------------------------------------

# class SignalCollector:
#     def __init__(self, history_seconds=60):
#         self.history_seconds = history_seconds
#         self.last_activity = time.time()

#         # Raw event timestamps
#         self.key_times = deque()
#         self.mouse_move_times = deque()
#         self.scroll_times = deque()
#         self.window_switch_times = deque()

#         # Advanced signals
#         self.typing_bursts = deque()
#         self.mouse_smoothness = deque()
#         self.micro_pauses = deque()

#         self.last_window = get_active_window_title()
#         self.last_mouse_pos = None
#         self.last_key_time = None

#         # Start listeners
#         if USE_PYNPUT:
#             self.k_listener = keyboard.Listener(on_press=self._on_key)
#             self.k_listener.start()
#             self.m_listener = mouse.Listener(on_move=self._on_move, on_scroll=self._on_scroll)
#             self.m_listener.start()
#         else:
#             if kb_fallback:
#                 kb_fallback.on_press(self._on_key)
#             if ms_fallback:
#                 ms_fallback.on_move(self._on_move)
#                 ms_fallback.on_scroll(self._on_scroll)

#         print("Using pynput:", USE_PYNPUT)

#     # -------------------------
#     # INPUT HANDLERS
#     # -------------------------
#     def _on_key(self, key):
#         now = time.time()
#         self.last_activity = now
#         self.key_times.append(now)
#         if self.last_key_time:
#             if now - self.last_key_time < 0.4:
#                 self.typing_bursts.append(now)
#         self.last_key_time = now

#     def _on_move(self, x, y):
#         now = time.time()
#         self.last_activity = now
#         self.mouse_move_times.append(now)
#         if self.last_mouse_pos:
#             dx = x - self.last_mouse_pos[0]
#             dy = y - self.last_mouse_pos[1]
#             self.mouse_smoothness.append((dx*dx + dy*dy)**0.5)
#         self.last_mouse_pos = (x, y)

#     def _on_scroll(self, x, y, dx, dy):
#         now = time.time()
#         self.last_activity = now
#         self.scroll_times.append(now)

#     # -------------------------
#     # INTERNAL HELPERS
#     # -------------------------
#     def _prune(self, dq):
#         cutoff = time.time() - self.history_seconds
#         while dq and dq[0] < cutoff:
#             dq.popleft()

#     def _detect_micro_pause(self):
#         idle = time.time() - self.last_activity
#         if 1 <= idle <= 10:
#             self.micro_pauses.append(time.time())

#     # -------------------------
#     # UPDATE LOOP
#     # -------------------------
#     def update(self):
#         for dq in [
#             self.key_times, self.mouse_move_times, self.scroll_times,
#             self.window_switch_times, self.typing_bursts, self.mouse_smoothness,
#             self.micro_pauses
#         ]:
#             self._prune(dq)

#         current = get_active_window_title()
#         if current != self.last_window:
#             self.window_switch_times.append(time.time())
#             self.last_window = current

#         self._detect_micro_pause()

#     # -------------------------
#     # OUTPUT SNAPSHOT
#     # -------------------------
#     def to_dict(self):
#         now = time.time()
#         idle_seconds = now - self.last_activity
#         window_seconds = max(self.history_seconds, 1)

#         audio_playing = False
#         if AudioUtilities:
#             try:
#                 sessions = AudioUtilities.GetAllSessions()
#                 audio_playing = any(s.SimpleAudioVolume.GetMasterVolume() > 0 for s in sessions)
#             except:
#                 audio_playing = False

#         brightness = get_screen_brightness()

#         return {
#             "idle_seconds": idle_seconds,
#             "active_window": self.last_window,
#             "window_category": categorize_window(self.last_window),
#             "fullscreen": is_fullscreen(),
#             "screen_locked": is_screen_locked(),
#             "screen_brightness": brightness,
#             "screen_dimmed": brightness is not None and brightness < 20,
#             "audio_playing": audio_playing,
#             "webcam_active": is_webcam_in_use(),
#             "microphone_active": is_microphone_in_use(),
#             "keypress_rate": len(self.key_times)*60/window_seconds,
#             "mouse_rate": len(self.mouse_move_times)*60/window_seconds,
#             "scroll_rate": len(self.scroll_times)*60/window_seconds,
#             "window_switches": len(self.window_switch_times)*60/window_seconds,
#             "typing_burst_rate": len(self.typing_bursts)*60/window_seconds,
#             "mouse_smoothness_avg": sum(self.mouse_smoothness)/len(self.mouse_smoothness) if self.mouse_smoothness else 0,
#             "micro_pause_rate": len(self.micro_pauses)*60/window_seconds
#         }

#     # -------------------------
#     # AWAY DETECTION
#     # -------------------------
#     def is_user_away(self):
#         """User is away if no input > 120 seconds or screen locked."""
#         try:
#             return self.to_dict().get("idle_seconds", 0) > 120 or is_screen_locked()
#         except:
#             return False












# # MacOS version

# import time
# import sys
# import platform
# from collections import deque

# # --- OS DETECTION ---
# IS_WINDOWS = sys.platform == "win32"
# IS_MAC = sys.platform == "darwin"

# # --- CONDITIONAL IMPORTS (Prevents Mac Crashes) ---
# if IS_WINDOWS:
#     import ctypes
#     from ctypes import wintypes
#     try:
#         import win32gui
#     except ImportError:
#         pass
#     user32 = ctypes.windll.user32
# else:
#     user32 = None

# if IS_MAC:
#     try:
#         from AppKit import NSWorkspace
#         from Quartz import (
#             CGWindowListCopyWindowInfo, 
#             kCGWindowListOptionOnScreenOnly, 
#             kCGNullWindowID
#         )
#     except ImportError:
#         NSWorkspace = None

# # --- CROSS-PLATFORM INPUT ---
# try:
#     from pynput import keyboard, mouse
#     USE_PYNPUT = True
# except:
#     USE_PYNPUT = False

# # ------------------------------------------------------------
# # HELPERS
# # ------------------------------------------------------------

# def get_active_window_title():
#     if IS_WINDOWS and user32:
#         try:
#             hwnd = user32.GetForegroundWindow()
#             length = user32.GetWindowTextLengthW(hwnd)
#             buff = ctypes.create_unicode_buffer(length + 1)
#             user32.GetWindowTextW(hwnd, buff, length + 1)
#             return buff.value or "Desktop"
#         except: return "Windows"
#     elif IS_MAC:
#         try:
#             window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
#             for window in window_list:
#                 if window.get('kCGWindowLayer') == 0:
#                     return window.get('kCGWindowTitle', window.get('kCGWindowOwnerName', 'Unknown'))
#         except: return "Mac Protected"
#     return "Unknown"

# def categorize_window(title: str):
#     t = title.lower()
#     if any(x in t for x in ["chrome", "edge", "firefox", "safari"]): return "browser"
#     if any(x in t for x in ["word", "excel", "powerpoint", "pages", "numbers"]): return "office"
#     if any(x in t for x in ["zoom", "meet", "teams", "webex", "facetime"]): return "meeting"
#     if any(x in t for x in ["vs code", "pycharm", "terminal", "xcode"]): return "coding"
#     return "other"

# # ------------------------------------------------------------
# # SIGNAL COLLECTOR CLASS
# # ------------------------------------------------------------

# class SignalCollector:
#     def __init__(self, history_seconds=60):
#         self.history_seconds = history_seconds
#         self.last_activity = time.time()
#         self.key_times = deque(maxlen=500)
#         self.mouse_move_times = deque(maxlen=500)
#         self.typing_bursts = deque(maxlen=100)
#         self.window_switch_count = 0
        
#         self.last_window = get_active_window_title()
#         self.last_mouse_pos = None
#         self.last_key_time = None

#         if USE_PYNPUT:
#             self.k_listener = keyboard.Listener(on_press=self._on_key)
#             self.m_listener = mouse.Listener(on_move=self._on_move)
#             self.k_listener.start()
#             self.m_listener.start()

#     def _on_key(self, key):
#         now = time.time()
#         self.last_activity = now
#         self.key_times.append(now)
#         if self.last_key_time and now - self.last_key_time < 0.4:
#             self.typing_bursts.append(now)
#         self.last_key_time = now

#     def _on_move(self, x, y):
#         now = time.time()
#         self.last_activity = now
#         self.mouse_move_times.append(now)
#         self.last_mouse_pos = (x, y)

#     def update(self):
#         current = get_active_window_title()
#         if current != self.last_window:
#             self.window_switch_count += 1
#             self.last_window = current

#     def to_dict(self):
#         now = time.time()
#         return {
#             "idle_seconds": int(now - self.last_activity),
#             "active_window": self.last_window,
#             "window_category": categorize_window(self.last_window),
#             "webcam_active": categorize_window(self.last_window) == "meeting",
#             "keypress_rate": len(self.key_times),
#             "mouse_rate": len(self.mouse_move_times),
#             "typing_intensity": len(self.typing_bursts),
#             "window_switches": self.window_switch_count
#         }











# # Idle corrected for macOS
# # core/signal_collector.py (MacOS & Windows Cross-Functional)

# import time
# import sys
# import platform
# import subprocess  # Added for Mac hardware idle check
# from collections import deque

# # --- OS DETECTION ---
# IS_WINDOWS = sys.platform == "win32"
# IS_MAC = sys.platform == "darwin"

# # --- CONDITIONAL IMPORTS (Prevents Mac Crashes) ---
# if IS_WINDOWS:
#     import ctypes
#     from ctypes import wintypes
#     try:
#         import win32gui
#     except ImportError:
#         pass
#     user32 = ctypes.windll.user32
# else:
#     user32 = None

# if IS_MAC:
#     try:
#         from AppKit import NSWorkspace
#         from Quartz import (
#             CGWindowListCopyWindowInfo, 
#             kCGWindowListOptionOnScreenOnly, 
#             kCGNullWindowID
#         )
#     except ImportError:
#         NSWorkspace = None

# # --- CROSS-PLATFORM INPUT ---
# try:
#     from pynput import keyboard, mouse
#     USE_PYNPUT = True
# except:
#     USE_PYNPUT = False

# # ------------------------------------------------------------
# # HELPERS
# # ------------------------------------------------------------

# def get_active_window_title():
#     if IS_WINDOWS and user32:
#         try:
#             hwnd = user32.GetForegroundWindow()
#             length = user32.GetWindowTextLengthW(hwnd)
#             buff = ctypes.create_unicode_buffer(length + 1)
#             user32.GetWindowTextW(hwnd, buff, length + 1)
#             return buff.value or "Desktop"
#         except: return "Windows"
#     elif IS_MAC:
#         try:
#             # Note: Requires 'Screen Recording' or 'Accessibility' permission on newer macOS
#             window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
#             for window in window_list:
#                 if window.get('kCGWindowLayer') == 0:
#                     return window.get('kCGWindowTitle', window.get('kCGWindowOwnerName', 'Unknown'))
#         except: return "Mac Protected"
#     return "Unknown"

# def categorize_window(title: str):
#     t = title.lower()
#     if any(x in t for x in ["chrome", "edge", "firefox", "safari"]): return "browser"
#     if any(x in t for x in ["word", "excel", "powerpoint", "pages", "numbers"]): return "office"
#     if any(x in t for x in ["zoom", "meet", "teams", "webex", "facetime"]): return "meeting"
#     if any(x in t for x in ["vs code", "pycharm", "terminal", "xcode"]): return "coding"
#     return "other"

# # ------------------------------------------------------------
# # SIGNAL COLLECTOR CLASS
# # ------------------------------------------------------------

# class SignalCollector:
#     def __init__(self, history_seconds=60):
#         self.history_seconds = history_seconds
#         self.last_activity = time.time()
#         self.key_times = deque(maxlen=500)
#         self.mouse_move_times = deque(maxlen=500)
#         self.typing_bursts = deque(maxlen=100)
#         self.window_switch_count = 0
        
#         self.last_window = get_active_window_title()
#         self.last_mouse_pos = None
#         self.last_key_time = None

#         if USE_PYNPUT:
#             # We use daemon=True to ensure threads don't block app exit
#             self.k_listener = keyboard.Listener(on_press=self._on_key)
#             self.m_listener = mouse.Listener(on_move=self._on_move)
#             self.k_listener.start()
#             self.m_listener.start()

#     def _on_key(self, key):
#         now = time.time()
#         self.last_activity = now
#         self.key_times.append(now)
#         if self.last_key_time and now - self.last_key_time < 0.4:
#             self.typing_bursts.append(now)
#         self.last_key_time = now

#     def _on_move(self, x, y):
#         now = time.time()
#         self.last_activity = now
#         self.mouse_move_times.append(now)
#         self.last_mouse_pos = (x, y)

#     def get_mac_system_idle(self):
#         """
#         Directly queries the macOS HID system for the hardware idle timer.
#         This is the 'True' idle time that works even if listeners are suspended.
#         """
#         try:
#             # Queries IOKit for the nanoseconds since last hardware input
#             cmd = "ioreg -c IOHIDSystem | awk '/HIDIdleTime/ {print $NF/1000000000; exit}'"
#             output = subprocess.check_output(cmd, shell=True).decode().strip()
#             return float(output) if output else 0.0
#         except:
#             return 0.0

#     def update(self):
#         current = get_active_window_title()
#         if current != self.last_window:
#             self.window_switch_count += 1
#             self.last_window = current

#     def to_dict(self):
#         now = time.time()
        
#         # --- IDLE LOGIC ---
#         if IS_MAC:
#             # On Mac, we use the Hardware Timer as the source of truth
#             system_idle = self.get_mac_system_idle()
            
#             # If system says we are active (idle < 1s) but pynput missed the event,
#             # sync the internal last_activity so the behavior classifier wakes up.
#             if system_idle < 1.0 and (now - self.last_activity) > 1.5:
#                 self.last_activity = now
                
#             idle_val = int(system_idle)
#         else:
#             # On Windows, the listener timestamp is generally reliable
#             idle_val = int(now - self.last_activity)

#         return {
#             "idle_seconds": idle_val,
#             "active_window": self.last_window,
#             "window_category": categorize_window(self.last_window),
#             "webcam_active": categorize_window(self.last_window) == "meeting",
#             "keypress_rate": len(self.key_times),
#             "mouse_rate": len(self.mouse_move_times),
#             "typing_intensity": len(self.typing_bursts),
#             "window_switches": self.window_switch_count
#         }
    





# # restored for macOS and WINdows

# import time
# import sys
# import platform
# import subprocess
# import ctypes
# from collections import deque

# # --- OS DETECTION ---
# IS_WINDOWS = sys.platform == "win32"
# IS_MAC = sys.platform == "darwin"

# # --- CONDITIONAL IMPORTS ---
# if IS_WINDOWS:
#     try:
#         import win32gui
#         import psutil
#         import wmi
#         from pycaw.pycaw import AudioUtilities
#         wmi_obj = wmi.WMI(namespace='wmi')
#     except ImportError:
#         win32gui = psutil = wmi_obj = AudioUtilities = None
#     user32 = ctypes.windll.user32
# else:
#     import psutil # psutil works on Mac
#     user32 = wmi_obj = AudioUtilities = None

# if IS_MAC:
#     try:
#         from Quartz import (
#             CGWindowListCopyWindowInfo, 
#             kCGWindowListOptionOnScreenOnly, 
#             kCGNullWindowID
#         )
#     except ImportError:
#         pass

# try:
#     from pynput import keyboard, mouse
#     USE_PYNPUT = True
# except:
#     USE_PYNPUT = False

# # ------------------------------------------------------------
# # CONSTANTS & HELPERS
# # ------------------------------------------------------------
# MEETING_PATTERNS = [
#     "Zoom Meeting", "Zoom -", "Google Meet", "Meet -",
#     "Microsoft Teams", "Teams Meeting", "Webex", "FaceTime"
# ]

# def get_active_window_title():
#     if IS_WINDOWS and user32:
#         try:
#             hwnd = user32.GetForegroundWindow()
#             length = user32.GetWindowTextLengthW(hwnd)
#             buff = ctypes.create_unicode_buffer(length + 1)
#             user32.GetWindowTextW(hwnd, buff, length + 1)
#             return buff.value or "Desktop"
#         except: return "Windows"
#     elif IS_MAC:
#         try:
#             window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
#             for window in window_list:
#                 if window.get('kCGWindowLayer') == 0:
#                     return window.get('kCGWindowTitle', window.get('kCGWindowOwnerName', 'Unknown'))
#         except: return "Mac Protected"
#     return "Unknown"

# def categorize_window(title: str):
#     t = title.lower()
#     if any(x in t for x in ["chrome", "edge", "firefox", "safari"]): return "browser"
#     if any(x in t for x in ["word", "excel", "powerpoint", "pages", "numbers"]): return "office"
#     if any(x in t for x in ["zoom", "meet", "teams", "webex", "facetime"]): return "meeting"
#     if any(x in t for x in ["youtube", "vlc", "player", "netflix"]): return "video"
#     if any(x in t for x in ["vs code", "pycharm", "terminal", "xcode", "visual studio", "sublime"]): return "coding"
#     if any(x in t for x in ["game", "steam", "epic", "minecraft"]): return "gaming"
#     return "other"

# # ------------------------------------------------------------
# # SIGNAL COLLECTOR CLASS
# # ------------------------------------------------------------

# class SignalCollector:
#     def __init__(self, history_seconds=60):
#         self.history_seconds = history_seconds
#         self.last_activity = time.time()
        
#         # RESTORED: All deques from your original code
#         self.key_times = deque()
#         self.mouse_move_times = deque()
#         self.scroll_times = deque()
#         self.window_switch_times = deque()
#         self.typing_bursts = deque()
#         self.mouse_smoothness = deque()
#         self.micro_pauses = deque()

#         self.last_window = get_active_window_title()
#         self.last_mouse_pos = None
#         self.last_key_time = None

#         if USE_PYNPUT:
#             self.k_listener = keyboard.Listener(on_press=self._on_key)
#             self.m_listener = mouse.Listener(on_move=self._on_move, on_scroll=self._on_scroll)
#             self.k_listener.start()
#             self.m_listener.start()

#     def _on_key(self, key):
#         now = time.time()
#         self.last_activity = now
#         self.key_times.append(now)
#         if self.last_key_time and now - self.last_key_time < 0.4:
#             self.typing_bursts.append(now)
#         self.last_key_time = now

#     def _on_move(self, x, y):
#         now = time.time()
#         self.last_activity = now
#         self.mouse_move_times.append(now)
#         if self.last_mouse_pos:
#             dx = x - self.last_mouse_pos[0]
#             dy = y - self.last_mouse_pos[1]
#             self.mouse_smoothness.append((dx*dx + dy*dy)**0.5)
#         self.last_mouse_pos = (x, y)

#     def _on_scroll(self, x, y, dx, dy):
#         now = time.time()
#         self.last_activity = now
#         self.scroll_times.append(now)

#     def get_mac_system_idle(self):
#         try:
#             cmd = "ioreg -c IOHIDSystem | awk '/HIDIdleTime/ {print $NF/1000000000; exit}'"
#             output = subprocess.check_output(cmd, shell=True).decode().strip()
#             return float(output) if output else 0.0
#         except: return 0.0

#     def _prune(self, dq):
#         cutoff = time.time() - self.history_seconds
#         while dq and dq[0] < cutoff:
#             dq.popleft()

#     def _detect_micro_pause(self):
#         idle = time.time() - self.last_activity
#         if 1 <= idle <= 10:
#             self.micro_pauses.append(time.time())

#     def update(self):
#         for dq in [self.key_times, self.mouse_move_times, self.scroll_times, 
#                    self.window_switch_times, self.typing_bursts, 
#                    self.mouse_smoothness, self.micro_pauses]:
#             self._prune(dq)

#         current = get_active_window_title()
#         if current != self.last_window:
#             self.window_switch_times.append(time.time())
#             self.last_window = current
#         self._detect_micro_pause()

#     def to_dict(self):
#         now = time.time()
#         window_seconds = max(self.history_seconds, 1)
        
#         if IS_MAC:
#             system_idle = self.get_mac_system_idle()
#             if system_idle < 1.0 and (now - self.last_activity) > 1.5:
#                 self.last_activity = now
#             idle_val = system_idle
#         else:
#             idle_val = now - self.last_activity

#         return {
#             "idle_seconds": int(idle_val),
#             "active_window": self.last_window,
#             "window_category": categorize_window(self.last_window),
#             "webcam_active": any(p.lower() in self.last_window.lower() for p in MEETING_PATTERNS),
#             "keypress_rate": len(self.key_times) * 60 / window_seconds,
#             "mouse_rate": len(self.mouse_move_times) * 60 / window_seconds,
#             "scroll_rate": len(self.scroll_times) * 60 / window_seconds,
#             "window_switches": len(self.window_switch_times) * 60 / window_seconds,
#             "typing_burst_rate": len(self.typing_bursts) * 60 / window_seconds,
#             "mouse_smoothness_avg": sum(self.mouse_smoothness)/len(self.mouse_smoothness) if self.mouse_smoothness else 0,
#             "micro_pause_rate": len(self.micro_pauses) * 60 / window_seconds
#         }












# # restored for macOS and WINdows

# import time
# import sys
# import platform
# import subprocess
# import ctypes
# from collections import deque

# # --- OS DETECTION ---
# IS_WINDOWS = sys.platform == "win32"
# IS_MAC = sys.platform == "darwin"

# # --- CONDITIONAL IMPORTS ---
# if IS_WINDOWS:
#     try:
#         import win32gui
#         import psutil
#         import wmi
#         from pycaw.pycaw import AudioUtilities
#         wmi_obj = wmi.WMI(namespace='wmi')
#     except ImportError:
#         win32gui = psutil = wmi_obj = AudioUtilities = None
#     user32 = ctypes.windll.user32
# else:
#     import psutil # psutil works on Mac
#     user32 = wmi_obj = AudioUtilities = None

# if IS_MAC:
#     try:
#         from Quartz import (
#             CGWindowListCopyWindowInfo, 
#             kCGWindowListOptionOnScreenOnly, 
#             kCGNullWindowID
#         )
#     except ImportError:
#         pass

# try:
#     from pynput import keyboard, mouse
#     USE_PYNPUT = True
# except:
#     USE_PYNPUT = False

# # ------------------------------------------------------------
# # CONSTANTS & HELPERS
# # ------------------------------------------------------------
# MEETING_PATTERNS = [
#     "Zoom Meeting", "Zoom -", "Google Meet", "Meet -",
#     "Microsoft Teams", "Teams Meeting", "Webex", "FaceTime"
# ]

# def get_active_window_title():
#     if IS_WINDOWS and user32:
#         try:
#             hwnd = user32.GetForegroundWindow()
#             length = user32.GetWindowTextLengthW(hwnd)
#             buff = ctypes.create_unicode_buffer(length + 1)
#             user32.GetWindowTextW(hwnd, buff, length + 1)
#             return buff.value or "Desktop"
#         except: return "Windows"
#     elif IS_MAC:
#         try:
#             window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
#             for window in window_list:
#                 if window.get('kCGWindowLayer') == 0:
#                     return window.get('kCGWindowTitle', window.get('kCGWindowOwnerName', 'Unknown'))
#         except: return "Mac Protected"
#     return "Unknown"

# def categorize_window(title: str):
#     t = title.lower()
    
#     # 1. MEETINGS (High Priority - Overrides Browser if in a Meet tab)
#     if any(x in t for x in ["zoom", "meet.google", "teams", "webex", "facetime", "slack call"]): 
#         return "meeting"
    
#     # 2. CODING (Mac + Windows IDEs & Terminals)
#     # Note: we use "visual studio code" before "code" to be precise
#     if any(x in t for x in ["vs code", "visual studio", "pycharm", "xcode", "sublime", "intellij", "android studio"]): 
#         return "coding"
#     if any(x in t for x in ["terminal", "iterm", "powershell", "command prompt", "cmd.exe"]):
#         return "coding"
#     # Specific Mac check: VS Code often just shows as "filename — Code"
#     if t.endswith("— code") or t.endswith("- code") or t == "code":
#         return "coding"

#     # 3. VIDEO & ENTERTAINMENT
#     if any(x in t for x in ["youtube", "vlc", "player", "netflix", "hulu", "disney+", "twitch"]): 
#         return "video"
    
#     # 4. BROWSERS
#     if any(x in t for x in ["chrome", "edge", "firefox", "safari", "brave"]): 
#         return "browser"
    
#     # 5. OFFICE & DOCS
#     if any(x in t for x in ["word", "excel", "powerpoint", "pages", "numbers", "keynote", "notion", "obsidian"]): 
#         return "office"
    
#     # 6. GAMING
#     if any(x in t for x in ["game", "steam", "epic", "minecraft", "roblox", "unity"]): 
#         return "gaming"

#     # 7. COMMUNICATION (Prevents these from being "Other")
#     if any(x in t for x in ["slack", "discord", "whatsapp", "messenger", "telegram"]):
#         return "communication"
        
#     return "other"
# # ------------------------------------------------------------
# # SIGNAL COLLECTOR CLASS
# # ------------------------------------------------------------

# class SignalCollector:
#     def __init__(self, history_seconds=60):
#         self.history_seconds = history_seconds
#         self.last_activity = time.time()
        
#         # RESTORED: All deques from your original code
#         self.key_times = deque()
#         self.mouse_move_times = deque()
#         self.scroll_times = deque()
#         self.window_switch_times = deque()
#         self.typing_bursts = deque()
#         self.mouse_smoothness = deque()
#         self.micro_pauses = deque()

#         self.last_window = get_active_window_title()
#         self.last_mouse_pos = None
#         self.last_key_time = None

#         if USE_PYNPUT:
#             self.k_listener = keyboard.Listener(on_press=self._on_key)
#             self.m_listener = mouse.Listener(on_move=self._on_move, on_scroll=self._on_scroll)
#             self.k_listener.start()
#             self.m_listener.start()

#     def _on_key(self, key):
#         now = time.time()
#         self.last_activity = now
#         self.key_times.append(now)
#         if self.last_key_time and now - self.last_key_time < 0.4:
#             self.typing_bursts.append(now)
#         self.last_key_time = now

#     def _on_move(self, x, y):
#         now = time.time()
#         self.last_activity = now
#         self.mouse_move_times.append(now)
#         if self.last_mouse_pos:
#             dx = x - self.last_mouse_pos[0]
#             dy = y - self.last_mouse_pos[1]
#             self.mouse_smoothness.append((dx*dx + dy*dy)**0.5)
#         self.last_mouse_pos = (x, y)

#     def _on_scroll(self, x, y, dx, dy):
#         now = time.time()
#         self.last_activity = now
#         self.scroll_times.append(now)

#     def get_mac_system_idle(self):
#         try:
#             cmd = "ioreg -c IOHIDSystem | awk '/HIDIdleTime/ {print $NF/1000000000; exit}'"
#             output = subprocess.check_output(cmd, shell=True).decode().strip()
#             return float(output) if output else 0.0
#         except: return 0.0

#     def _prune(self, dq):
#         cutoff = time.time() - self.history_seconds
#         while dq and dq[0] < cutoff:
#             dq.popleft()

#     def _detect_micro_pause(self):
#         idle = time.time() - self.last_activity
#         if 1 <= idle <= 10:
#             self.micro_pauses.append(time.time())

#     def update(self):
#         for dq in [self.key_times, self.mouse_move_times, self.scroll_times, 
#                    self.window_switch_times, self.typing_bursts, 
#                    self.mouse_smoothness, self.micro_pauses]:
#             self._prune(dq)

#         current = get_active_window_title()
#         if current != self.last_window:
#             self.window_switch_times.append(time.time())
#             self.last_window = current
#         self._detect_micro_pause()

#     def to_dict(self):
#         now = time.time()
#         window_seconds = max(self.history_seconds, 1)
        
#         if IS_MAC:
#             system_idle = self.get_mac_system_idle()
#             if system_idle < 1.0 and (now - self.last_activity) > 1.5:
#                 self.last_activity = now
#             idle_val = system_idle
#         else:
#             idle_val = now - self.last_activity

#         return {
#             "idle_seconds": int(idle_val),
#             "active_window": self.last_window,
#             "window_category": categorize_window(self.last_window),
#             "webcam_active": any(p.lower() in self.last_window.lower() for p in MEETING_PATTERNS),
#             "keypress_rate": len(self.key_times) * 60 / window_seconds,
#             "mouse_rate": len(self.mouse_move_times) * 60 / window_seconds,
#             "scroll_rate": len(self.scroll_times) * 60 / window_seconds,
#             "window_switches": len(self.window_switch_times) * 60 / window_seconds,
#             "typing_burst_rate": len(self.typing_bursts) * 60 / window_seconds,
#             "mouse_smoothness_avg": sum(self.mouse_smoothness)/len(self.mouse_smoothness) if self.mouse_smoothness else 0,
#             "micro_pause_rate": len(self.micro_pauses) * 60 / window_seconds
#         }








import time
import sys
import platform
import subprocess
import ctypes
from collections import deque

# --- OS DETECTION ---
IS_WINDOWS = sys.platform == "win32"
IS_MAC = sys.platform == "darwin"

# --- CONDITIONAL IMPORTS ---
if IS_WINDOWS:
    try:
        import win32gui
        import psutil
        import wmi
        from pycaw.pycaw import AudioUtilities
        wmi_obj = wmi.WMI(namespace='wmi')
    except ImportError:
        win32gui = psutil = wmi_obj = AudioUtilities = None
    user32 = ctypes.windll.user32
else:
    import psutil # Works on Mac
    user32 = wmi_obj = AudioUtilities = None

if IS_MAC:
    try:
        from Quartz import (
            CGWindowListCopyWindowInfo, 
            kCGWindowListOptionOnScreenOnly, 
            kCGNullWindowID
        )
    except ImportError:
        pass

try:
    from pynput import keyboard, mouse
    USE_PYNPUT = True
except:
    USE_PYNPUT = False

# ------------------------------------------------------------
# CONSTANTS & HELPERS
# ------------------------------------------------------------
MEETING_PATTERNS = [
    "zoom", "google meet", "microsoft teams", "teams meeting", 
    "webex", "facetime", "slack call", "meet.google"
]

def get_active_window_title():
    if IS_WINDOWS and user32:
        try:
            hwnd = user32.GetForegroundWindow()
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            return buff.value or "Desktop"
        except: return "Windows"
    elif IS_MAC:
        try:
            window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
            for window in window_list:
                if window.get('kCGWindowLayer') == 0:
                    title = window.get('kCGWindowTitle', '')
                    owner = window.get('kCGWindowOwnerName', '')
                    return f"{title} — {owner}" if title else owner
        except: return "Mac Protected"
    return "Unknown"

def categorize_window(title: str):
    t = title.lower()
    
    # 1. MEETINGS (High Priority)
    if any(x in t for x in MEETING_PATTERNS): return "meeting"
    
    # 2. CODING (Mac + Windows IDEs)
    if any(x in t for x in ["vs code", "visual studio", "pycharm", "xcode", "sublime", "intellij", "android studio"]): 
        return "coding"
    if any(x in t for x in ["terminal", "iterm", "powershell", "command prompt", "cmd.exe"]):
        return "coding"
    if t.endswith("— code") or t.endswith("- code") or " — code" in t:
        return "coding"

    # 3. VIDEO
    if any(x in t for x in ["youtube", "vlc", "player", "netflix", "hulu", "disney+", "twitch"]): 
        return "video"
    
    # 4. BROWSERS
    if any(x in t for x in ["chrome", "edge", "firefox", "safari", "brave"]): 
        return "browser"
    
    # 5. OFFICE & DOCS
    if any(x in t for x in ["word", "excel", "powerpoint", "pages", "numbers", "keynote", "notion", "obsidian"]): 
        return "office"
    
    # 6. GAMING
    if any(x in t for x in ["game", "steam", "epic", "minecraft", "roblox", "unity"]): 
        return "gaming"

    # 7. COMMUNICATION
    if any(x in t for x in ["slack", "discord", "whatsapp", "messenger", "telegram"]):
        return "communication"
        
    return "other"

# ------------------------------------------------------------
# SIGNAL COLLECTOR CLASS
# ------------------------------------------------------------

class SignalCollector:
    def __init__(self, history_seconds=60):
        self.history_seconds = history_seconds
        self.last_activity = time.time()
        
        # RESTORED: All deques from original
        self.key_times = deque()
        self.mouse_move_times = deque()
        self.scroll_times = deque()
        self.window_switch_times = deque()
        self.typing_bursts = deque()
        self.mouse_smoothness = deque()
        self.micro_pauses = deque()

        self.last_window = get_active_window_title()
        self.last_mouse_pos = None
        self.last_key_time = None

        # Python 3.14 Safety Shield
        if USE_PYNPUT:
            try:
                self.k_listener = keyboard.Listener(on_press=self._on_key)
                self.m_listener = mouse.Listener(on_move=self._on_move, on_scroll=self._on_scroll)
                self.k_listener.start()
                self.m_listener.start()
            except Exception as e:
                print(f"SENSOR WARNING (Python 3.14 compatibility): {e}")
                print("Falling back to hardware-only idle tracking.")

    def _on_key(self, key):
        now = time.time()
        self.last_activity = now
        self.key_times.append(now)
        if self.last_key_time and now - self.last_key_time < 0.4:
            self.typing_bursts.append(now)
        self.last_key_time = now

    def _on_move(self, x, y):
        now = time.time()
        self.last_activity = now
        self.mouse_move_times.append(now)
        if self.last_mouse_pos:
            dx = x - self.last_mouse_pos[0]
            dy = y - self.last_mouse_pos[1]
            self.mouse_smoothness.append((dx*dx + dy*dy)**0.5)
        self.last_mouse_pos = (x, y)

    def _on_scroll(self, x, y, dx, dy):
        now = time.time()
        self.last_activity = now
        self.scroll_times.append(now)

    def get_mac_system_idle(self):
        try:
            cmd = "ioreg -c IOHIDSystem | awk '/HIDIdleTime/ {print $NF/1000000000; exit}'"
            output = subprocess.check_output(cmd, shell=True).decode().strip()
            return float(output) if output else 0.0
        except: return 0.0

    def _prune(self, dq):
        cutoff = time.time() - self.history_seconds
        while dq and dq[0] < cutoff:
            dq.popleft()

    def _detect_micro_pause(self):
        idle = time.time() - self.last_activity
        if 1 <= idle <= 10:
            self.micro_pauses.append(time.time())

    def update(self):
        for dq in [self.key_times, self.mouse_move_times, self.scroll_times, 
                   self.window_switch_times, self.typing_bursts, 
                   self.mouse_smoothness, self.micro_pauses]:
            self._prune(dq)

        current = get_active_window_title()
        if current != self.last_window:
            self.window_switch_times.append(time.time())
            self.last_window = current
        self._detect_micro_pause()

    def to_dict(self):
        now = time.time()
        window_seconds = max(self.history_seconds, 1)
        
        if IS_MAC:
            system_idle = self.get_mac_system_idle()
            if system_idle < 1.0 and (now - self.last_activity) > 1.5:
                self.last_activity = now
            idle_val = system_idle
        else:
            idle_val = now - self.last_activity

        return {
            "idle_seconds": int(idle_val),
            "active_window": self.last_window,
            "window_category": categorize_window(self.last_window),
            "webcam_active": categorize_window(self.last_window) == "meeting",
            "keypress_rate": len(self.key_times) * 60 / window_seconds,
            "mouse_rate": len(self.mouse_move_times) * 60 / window_seconds,
            "scroll_rate": len(self.scroll_times) * 60 / window_seconds,
            "window_switches": len(self.window_switch_times) * 60 / window_seconds,
            "typing_burst_rate": len(self.typing_bursts) * 60 / window_seconds,
            "mouse_smoothness_avg": sum(self.mouse_smoothness)/len(self.mouse_smoothness) if self.mouse_smoothness else 0,
            "micro_pause_rate": len(self.micro_pauses) * 60 / window_seconds
        }