# # fatigue_model.py

# class FatiguePredictionModel:
#     """
#     Simple rule-based fatigue score (0–100).
#     Higher = more fatigued.
#     AI-ready: you can later replace this with a learned model.
#     """

#     def compute_fatigue(self, signals: dict, behavior: str) -> float:
#         idle = signals.get("idle_seconds", 0)
#         key_rate = signals.get("keypress_rate", 0)
#         mouse_rate = signals.get("mouse_rate", 0)
#         scroll_rate = signals.get("scroll_rate", 0)
#         micro_pause_rate = signals.get("micro_pause_rate", 0)
#         mouse_smoothness = signals.get("mouse_smoothness_avg", 0)
#         window_switches = signals.get("window_switches", 0)
#         screen_brightness = signals.get("screen_brightness", 50)

#         score = 0.0

#         # Long continuous activity
#         if idle < 30 and (key_rate + mouse_rate + scroll_rate) > 50:
#             score += 25

#         # Many micro-pauses (early fatigue)
#         if micro_pause_rate > 10:
#             score += 20

#         # Mouse jitter (reduced precision)
#         if mouse_smoothness > 50:
#             score += 15

#         # High context switching (mental fatigue)
#         if window_switches > 15:
#             score += 15

#         # Bright screen for long periods
#         if screen_brightness is not None and screen_brightness > 70:
#             score += 10

#         # Behavior-specific adjustments
#         if behavior == "meeting":
#             score += 10
#         if behavior == "deep_work":
#             score += 10
#         if behavior == "watching":
#             score += 5

#         # Clamp 0–100
#         return max(0.0, min(100.0, score))












# 1st update on 17t March
# fatigue_model.py

class FatiguePredictionModel:
    """
    Simple rule-based fatigue score (0–100).
    Higher = more fatigued.
    Now supports optional adaptive multipliers learned by AI Mode.
    """

    def __init__(self, rise_multiplier=1.0, recovery_multiplier=1.0):
        self.rise_multiplier = rise_multiplier
        self.recovery_multiplier = recovery_multiplier

    def compute_fatigue(self, signals: dict, behavior: str) -> float:
        idle = signals.get("idle_seconds", 0)
        key_rate = signals.get("keypress_rate", 0)
        mouse_rate = signals.get("mouse_rate", 0)
        scroll_rate = signals.get("scroll_rate", 0)
        micro_pause_rate = signals.get("micro_pause_rate", 0)
        mouse_smoothness = signals.get("mouse_smoothness_avg", 0)
        window_switches = signals.get("window_switches", 0)
        screen_brightness = signals.get("screen_brightness", 50)

        score = 0.0

        # Long continuous activity
        if idle < 30 and (key_rate + mouse_rate + scroll_rate) > 50:
            score += 25

        # Many micro-pauses (early fatigue)
        if micro_pause_rate > 10:
            score += 20

        # Mouse jitter (reduced precision)
        if mouse_smoothness > 50:
            score += 15

        # High context switching (mental fatigue)
        if window_switches > 15:
            score += 15

        # Bright screen for long periods
        if screen_brightness is not None and screen_brightness > 70:
            score += 10

        # Behavior-specific adjustments
        if behavior == "meeting":
            score += 10
        if behavior == "deep_work":
            score += 10
        if behavior == "watching":
            score += 5

        # Apply adaptive multipliers
        score *= float(self.rise_multiplier)

        # Clamp 0–100
        return max(0.0, min(100.0, score))
