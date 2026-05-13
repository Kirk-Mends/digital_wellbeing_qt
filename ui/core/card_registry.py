# ui/core/card_registry.py

class CardRegistry:
    cards = []

    @classmethod
    def register(cls, card):
        print("REGISTERED:", type(card).__name__)
        cls.cards.append(card)

    @classmethod
    def unregister(cls, card):
        if card in cls.cards:
            cls.cards.remove(card)

    @classmethod
    def update_all(cls, behavior, fatigue, reason, trigger, next_break_seconds, session_start, monitoring):
        for card in cls.cards:
            if hasattr(card, "update_from_engine"):
                card.update_from_engine(
                    behavior=behavior,
                    fatigue=fatigue,
                    reason=reason,
                    trigger=trigger,
                    next_break_seconds=next_break_seconds,
                    session_start=session_start,
                    monitoring=monitoring,
                )
