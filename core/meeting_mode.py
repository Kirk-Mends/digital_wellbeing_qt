# # meeting_mode.py

# class MeetingMode:
#     """
#     Determines if we should suppress breaks due to meetings / presentations.
#     """

#     def is_meeting_active(self, signals: dict, behavior: str) -> bool:
#         window_cat = signals.get("window_category", "other")
#         fullscreen = signals.get("fullscreen", False)
#         webcam = signals.get("webcam_active", False)
#         mic = signals.get("microphone_active", False)
#         audio_playing = signals.get("audio_playing", False)
#         key_rate = signals.get("keypress_rate", 0)

#         # Explicit meeting classification
#         if behavior == "meeting":
#             return True

#         # Heuristic: video call / webinar / presentation
#         if window_cat in ["meeting", "video"] and fullscreen and (webcam or mic or audio_playing) and key_rate < 5:
#             return True

#         return False

#     def should_suppress_breaks(self, signals: dict, behavior: str) -> bool:
#         # For now, same as is_meeting_active, but you can extend later
#         return self.is_meeting_active(signals, behavior)











# Only problem is that meeting is on when mic is active, even if it's not a meeting. You could add more conditions to reduce false positives, e.g.:

# # meeting_mode.py

# class MeetingMode:
#     """
#     Determines if we should suppress breaks due to meetings / presentations.
#     """

#     def is_meeting_active(self, signals: dict, behavior: str) -> bool:
#         window_cat = signals.get("window_category", "other")
#         webcam = signals.get("webcam_active", False)
#         audio_playing = signals.get("audio_playing", False)

#         # 1. Explicit behavior classification
#         if behavior == "meeting":
#             return True

#         # 2. Foreground-based meeting detection
#         #    - Webcam ON → meeting
#         #    - Meeting window → meeting
#         #    - Audio + meeting window → meeting
#         #    - Audio alone → NOT a meeting
#         #    - Microphone alone → NOT a meeting
#         if webcam:
#             return True

#         if window_cat == "meeting":
#             return True

#         if audio_playing and window_cat == "meeting":
#             return True

#         return False

#     def should_suppress_breaks(self, signals: dict, behavior: str) -> bool:
#         return self.is_meeting_active(signals, behavior)













# meeting_mode.py
# included screen sharing and presentation mode detection

# meeting_mode.py

class MeetingMode:
    """
    Determines if we should suppress breaks due to meetings / presentations.
    """

    def is_meeting_active(self, signals: dict, behavior_key: str) -> bool:
        window_cat = signals.get("window_category", "other")
        webcam = signals.get("webcam_active", False)
        audio_playing = signals.get("audio_playing", False)
        fullscreen = signals.get("fullscreen", False)
        idle = signals.get("idle_seconds", 0.0)

        # 1. Explicit behavior classification
        if behavior_key == "meeting":
            return True

        # 2. Webcam ON → strong meeting signal
        if webcam:
            return True

        # 3. Foreground-based meeting detection
        if window_cat == "meeting":
            return True

        # 4. Audio + meeting window → meeting
        if audio_playing and window_cat == "meeting":
            return True

        # 5. Screen-sharing / presentation heuristics
        if window_cat == "meeting" and fullscreen:
            return True

        if window_cat == "meeting" and idle > 20:
            return True

        return False

    def should_suppress_breaks(self, signals: dict, behavior_key: str) -> bool:
        return self.is_meeting_active(signals, behavior_key)
