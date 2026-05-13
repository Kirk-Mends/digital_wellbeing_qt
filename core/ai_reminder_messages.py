




# Upgraded with light and heavy browsing
# ai_reminder_messages.py
# Premium, warm-tone, behavior-aware AI message generator

class AIMessageGenerator:
    """
    Generates warm, human-friendly messages for AI Mode.
    These messages are behavior-aware and fatigue-aware,
    and designed to match the premium reminder popup.
    """

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # MAIN ENTRY
    # ---------------------------------------------------------
    def generate(self, behavior: str, reason: str, fatigue: float) -> str:
        """
        Returns a warm, human-friendly message body.
        The reminder popup will handle the headline and timing.
        """
        behavior_key = behavior.lower().replace(" ", "_")

        # Fatigue overrides (AI Mode is more adaptive)
        if fatigue >= 85:
            return "You’ve been pushing yourself hard. Take a moment to reset."
        if fatigue >= 70:
            return "Your focus has been strong. A short pause will help you stay sharp."

        # Behavior-specific messages
        if behavior_key in ["reading"]:
            return "Your eyes have been working steadily. A short pause could help them recover."

        if behavior_key in ["coding", "deep_work", "writing"]:
            return "You’ve been deeply focused. A brief stretch can help you keep your flow."

        if behavior_key in ["browsing", "light_browsing", "heavy_browsing"]:
            return "You’ve been scrolling for a while. Take a moment to relax your eyes."

        if behavior_key in ["watching", "video"]:
            return "Enjoy your video. Breaks will resume afterward."

        if behavior_key in ["gaming"]:
            return "You’re in the middle of a game. Breaks will wait for you."

        if behavior_key in ["meeting", "call"]:
            return "You’re in a call right now. Breaks will resume when you’re done."

        if behavior_key in ["eye_strain_risk"]:
            return "Your eyes could use a moment of rest."

        if behavior_key in ["posture_risk"]:
            return "A quick stretch may help you feel more comfortable."

        if behavior_key in ["idle", "away"]:
            return "Welcome back. Take a moment to settle in."

        # Fallback (rare)
        return "You’ve been going for a while. A short pause could feel good."
