# core/ai_mode_engine.py

import time
from core.smart_break_engine_v2 import SmartBreakEngineV2


class AIModeEngine:
    """
    Wrapper that turns SmartBreakEngineV2 into a clean AI Mode snapshot.
    """

    def __init__(self):
        self.engine = SmartBreakEngineV2()

    def ai_mode_snapshot(self, signals: dict) -> dict:
        """
        Returns a clean, UI-friendly snapshot for AI Mode.
        """
        result = self.engine.should_trigger_break(signals)

        # Compute next break countdown
        interval = result["interval_used"]
        now = time.time()
        next_break = int(interval - (now - self.engine.session_start))
        next_break = max(0, next_break)

        # Detect suppression
        suppressed = "suppressed" in result["reason"].lower()

        return {
            "behavior": result["behavior"],
            "fatigue": int(result["fatigue_score"]),
            "reason": result["reason"],
            "message": result.get("message", ""),
            "next_break": next_break,
            "trigger": "Suppressed" if suppressed else ("Break" if result["trigger"] else "None"),
        }
