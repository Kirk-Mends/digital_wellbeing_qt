

# # I changed summary card
# # ui/pages/ai_mode.py

# from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
# from PySide6.QtCore import Qt

# from ui.pages.shared.fluent_card import FluentCard
# from ui.widgets.fluent_blur import FluentBlur
# from ui.core.theme import AppColors
# from ui.animations import (
#     FadeInAnimator, SlideInAnimator, SparklineAnimator,
#     ValueAnimator, PulseAnimator
# )


# class AIModePage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.setObjectName("AIModePage")

#         self.behavior_trend = []
#         self.fatigue_trend = []
#         self.break_trend = []

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)
#         layout.setSpacing(20)

#         # ============================================
#         # ROW 1 — Behavior + Fatigue
#         # ============================================
#         row1 = QHBoxLayout()
#         row1.setSpacing(20)

#         self.card_behavior = FluentCard("Behavior", AppColors.BEHAVIOR)
#         self.card_fatigue = FluentCard("Fatigue", AppColors.FATIGUE)

#         self.card_behavior.setMinimumHeight(260)
#         self.card_fatigue.setMinimumHeight(260)

#         row1.addWidget(self._wrap_blur(self.card_behavior))
#         row1.addWidget(self._wrap_blur(self.card_fatigue))
#         layout.addLayout(row1)

#         # ============================================
#         # ROW 2 — Next Break + Reason + Suppression
#         # ============================================
#         row2 = QHBoxLayout()
#         row2.setSpacing(20)

#         self.card_next_break = FluentCard("Next Break", AppColors.BREAK)
#         self.card_reason = FluentCard("Reason", AppColors.INSIGHT, has_spark=False)
#         self.card_suppression = FluentCard("Suppression", AppColors.SUPPRESSION, has_spark=False)

#         self.card_next_break.setMinimumHeight(150)
#         self.card_reason.setMinimumHeight(300)
#         self.card_suppression.setMinimumHeight(180)
#         self.card_next_break.setMaximumHeight(180)

#         row2.addWidget(self._wrap_blur(self.card_next_break), 1)
#         row2.addWidget(self._wrap_blur(self.card_reason), 2)
#         row2.addWidget(self._wrap_blur(self.card_suppression), 1)
#         layout.addLayout(row2)

#         # ============================================
#         # INSIGHT (Slim, professional summary)
#         # ============================================
#         self.card_insight = FluentCard("Insight", AppColors.INSIGHT, has_spark=False)
#         self.card_insight.setMinimumHeight(140)
#         layout.addWidget(self._wrap_blur(self.card_insight))

#         layout.addStretch()

#         # BUTTON — Left aligned
#         self.btn_toggle = QPushButton("Start K-Mends AI")
#         self.btn_toggle.setObjectName("PrimaryButton")
#         self.btn_toggle.setFixedHeight(44)
#         self.btn_toggle.clicked.connect(self.on_toggle_clicked)
#         layout.addWidget(self.btn_toggle, 0, Qt.AlignLeft)

#     def _wrap_blur(self, card: FluentCard) -> FluentBlur:
#         blur = FluentBlur(radius=25, opacity=0.30)
#         blur.layout.addWidget(card)
#         return blur

#     def on_toggle_clicked(self):
#         self.main.show_ai()
#         self.main.toggle_monitoring()
#         self.btn_toggle.setText("Stop K-Mends AI" if self.main.monitoring else "Start K-Mends AI")

#     # ============================================
#     # PROFESSIONAL INSIGHT GENERATOR
#     # ============================================
#     def _generate_insight(self, behavior, fatigue, reason, next_break_seconds):
#         fatigue = int(fatigue)
#         nb_min = max(1, next_break_seconds // 60)

#         if "meeting" in behavior.lower():
#             return "You appear to be in a meeting. Break reminders are paused."

#         if "watch" in behavior.lower():
#             return "You’re watching content. Monitoring will resume when activity changes."

#         if "suppressed" in reason.lower():
#             return "Current activity suggests a break isn’t appropriate. Monitoring continues."

#         if fatigue >= 70:
#             return "Fatigue is elevated. A short pause soon may help maintain clarity."

#         if fatigue >= 40:
#             return "Fatigue is rising gradually. A break will be helpful in the next period."

#         if nb_min <= 3:
#             return "You’ve been active for a while. A break is coming up shortly."

#         return f"Focus is steady and fatigue remains low. Your next break is in about {nb_min} minutes."

#     # ============================================
#     # UPDATE UI
#     # ============================================
#     def update_ai_status(self, behavior, fatigue, reason, trigger, next_break_seconds):
#         # BEHAVIOR
#         self.card_behavior.update_value(behavior)
#         self.behavior_trend.append(len(self.behavior_trend) % 5)
#         self.behavior_trend = self.behavior_trend[-30:]
#         SparklineAnimator(self.card_behavior.spark, AppColors.BEHAVIOR).animate(self.behavior_trend)

#         # FATIGUE
#         # Convert fatigue to a clean string immediately
#         if fatigue is None:
#             self.card_fatigue.update_value("0%")
#         else:
#             self.card_fatigue.update_value(f"{int(fatigue)}%")


#         self.fatigue_trend.append(int(fatigue))
#         self.fatigue_trend = self.fatigue_trend[-30:]
#         SparklineAnimator(self.card_fatigue.spark, AppColors.FATIGUE).animate(self.fatigue_trend)

#         # REASON
#         self.card_reason.update_value(reason)

#         # NEXT BREAK
#         nb = max(0, int(next_break_seconds))
#         self.card_next_break.update_value(f"{nb}m" if nb else "—")
#         self.break_trend.append(nb)
#         self.break_trend = self.break_trend[-30:]
#         SparklineAnimator(self.card_next_break.spark, AppColors.BREAK).animate(self.break_trend)

#         # SUPPRESSION
#         if "suppressed" in reason.lower():
#             self.card_suppression.update_value("Active")
#             PulseAnimator(self.card_suppression).start()
#         else:
#             self.card_suppression.update_value("None")

#         # INSIGHT (Professional tone)
#         insight = self._generate_insight(behavior, fatigue, reason, nb)
#         self.card_insight.update_value(insight)

#         # ANIMATIONS
#         for card in [
#             self.card_behavior, self.card_fatigue, self.card_reason,
#             self.card_next_break, self.card_suppression, self.card_insight
#         ]:
#             FadeInAnimator(card).start()
#             SlideInAnimator(card.accent).start()

#     def _fatigue_value(self):
#         text = self.card_fatigue.value_label.text().replace("%", "").strip()
#         return int(text) if text.isdigit() else 0














# # 29th March updated to correct minutes from sec
# # ui/pages/ai_mode.py

# from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
# from PySide6.QtCore import Qt

# from ui.pages.shared.fluent_card import FluentCard
# from ui.widgets.fluent_blur import FluentBlur
# from ui.core.theme import AppColors
# from ui.animations import (
#     FadeInAnimator, SlideInAnimator, SparklineAnimator,
#     ValueAnimator, PulseAnimator
# )


# class AIModePage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.setObjectName("AIModePage")

#         self.behavior_trend = []
#         self.fatigue_trend = []
#         self.break_trend = []

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)
#         layout.setSpacing(20)

#         # ============================================
#         # ROW 1 — Behavior + Fatigue
#         # ============================================
#         row1 = QHBoxLayout()
#         row1.setSpacing(20)

#         self.card_behavior = FluentCard("Behavior", AppColors.BEHAVIOR)
#         self.card_fatigue = FluentCard("Fatigue", AppColors.FATIGUE)

#         self.card_behavior.setMinimumHeight(260)
#         self.card_fatigue.setMinimumHeight(260)

#         row1.addWidget(self._wrap_blur(self.card_behavior))
#         row1.addWidget(self._wrap_blur(self.card_fatigue))
#         layout.addLayout(row1)

#         # ============================================
#         # ROW 2 — Next Break + Reason + Suppression
#         # ============================================
#         row2 = QHBoxLayout()
#         row2.setSpacing(20)

#         self.card_next_break = FluentCard("Next Break", AppColors.BREAK)
#         self.card_reason = FluentCard("Reason", AppColors.INSIGHT, has_spark=False)
#         self.card_suppression = FluentCard("Suppression", AppColors.SUPPRESSION, has_spark=False)

#         self.card_next_break.setMinimumHeight(150)
#         self.card_reason.setMinimumHeight(300)
#         self.card_suppression.setMinimumHeight(180)
#         self.card_next_break.setMaximumHeight(180)

#         row2.addWidget(self._wrap_blur(self.card_next_break), 1)
#         row2.addWidget(self._wrap_blur(self.card_reason), 2)
#         row2.addWidget(self._wrap_blur(self.card_suppression), 1)
#         layout.addLayout(row2)

#         # ============================================
#         # INSIGHT (Slim, professional summary)
#         # ============================================
#         self.card_insight = FluentCard("Insight", AppColors.INSIGHT, has_spark=False)
#         self.card_insight.setMinimumHeight(140)
#         layout.addWidget(self._wrap_blur(self.card_insight))

#         layout.addStretch()

#         # BUTTON — Left aligned
#         self.btn_toggle = QPushButton("Start K-Mends AI")
#         self.btn_toggle.setObjectName("PrimaryButton")
#         self.btn_toggle.setFixedHeight(44)
#         self.btn_toggle.clicked.connect(self.on_toggle_clicked)
#         layout.addWidget(self.btn_toggle, 0, Qt.AlignLeft)

#     def _wrap_blur(self, card: FluentCard) -> FluentBlur:
#         blur = FluentBlur(radius=25, opacity=0.30)
#         blur.layout.addWidget(card)
#         return blur

#     def on_toggle_clicked(self):
#         self.main.show_ai()
#         self.main.toggle_monitoring()
#         self.btn_toggle.setText("Stop K-Mends AI" if self.main.monitoring else "Start K-Mends AI")

#     # ============================================
#     # PROFESSIONAL INSIGHT GENERATOR
#     # ============================================
#     def _generate_insight(self, behavior, fatigue, reason, next_break_minutes):
#         fatigue = int(fatigue)
#         nb_min = max(1, int(next_break_minutes))  # FIXED: already minutes

#         if "meeting" in behavior.lower():
#             return "You appear to be in a meeting. Break reminders are paused."

#         if "watch" in behavior.lower():
#             return "You’re watching content. Monitoring will resume when activity changes."

#         if "suppressed" in reason.lower():
#             return "Current activity suggests a break isn’t appropriate. Monitoring continues."

#         if fatigue >= 70:
#             return "Fatigue is elevated. A short pause soon may help maintain clarity."

#         if fatigue >= 40:
#             return "Fatigue is rising gradually. A break will be helpful in the next period."

#         if nb_min <= 3:
#             return "You’ve been active for a while. A break is coming up shortly."

#         return f"Focus is steady and fatigue remains low. Your next break is in about {nb_min} minutes."

#     # ============================================
#     # UPDATE UI
#     # ============================================
#     def update_ai_status(self, behavior, fatigue, reason, trigger, next_break_minutes):

#         # BEHAVIOR
#         self.card_behavior.update_value(behavior)
#         self.behavior_trend.append(len(self.behavior_trend) % 5)
#         self.behavior_trend = self.behavior_trend[-30:]
#         SparklineAnimator(self.card_behavior.spark, AppColors.BEHAVIOR).animate(self.behavior_trend)

#         # FATIGUE
#         if fatigue is None:
#             self.card_fatigue.update_value("0%")
#         else:
#             self.card_fatigue.update_value(f"{int(fatigue)}%")

#         self.fatigue_trend.append(int(fatigue))
#         self.fatigue_trend = self.fatigue_trend[-30:]
#         SparklineAnimator(self.card_fatigue.spark, AppColors.FATIGUE).animate(self.fatigue_trend)

#         # REASON
#         self.card_reason.update_value(reason)

#         # NEXT BREAK (now in minutes)
#         nb = max(0, int(next_break_minutes))
#         self.card_next_break.update_value(f"{nb}m" if nb else "—")

#         # FIXED: sparkline expects seconds for smooth animation
#         self.break_trend.append(nb * 60)
#         self.break_trend = self.break_trend[-30:]
#         SparklineAnimator(self.card_next_break.spark, AppColors.BREAK).animate(self.break_trend)

#         # SUPPRESSION
#         if "suppressed" in reason.lower():
#             self.card_suppression.update_value("Active")
#             PulseAnimator(self.card_suppression).start()
#         else:
#             self.card_suppression.update_value("None")

#         # INSIGHT
#         insight = self._generate_insight(behavior, fatigue, reason, nb)
#         self.card_insight.update_value(insight)

#         # ANIMATIONS
#         for card in [
#             self.card_behavior, self.card_fatigue, self.card_reason,
#             self.card_next_break, self.card_suppression, self.card_insight
#         ]:
#             FadeInAnimator(card).start()
#             SlideInAnimator(card.accent).start()

#     def _fatigue_value(self):
#         text = self.card_fatigue.value_label.text().replace("%", "").strip()
#         return int(text) if text.isdigit() else 0

    

















# 29th March updated to correct minutes from sec
# ui/pages/ai_mode.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt

from ui.pages.shared.fluent_card import FluentCard
from ui.widgets.fluent_blur import FluentBlur
from ui.core.theme import AppColors
from ui.animations import (
    FadeInAnimator, SlideInAnimator, SparklineAnimator,
    ValueAnimator, PulseAnimator
)


class AIModePage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setObjectName("AIModePage")

        self.behavior_trend = []
        self.fatigue_trend = []
        self.break_trend = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # ============================================
        # ROW 1 — Behavior + Fatigue
        # ============================================
        row1 = QHBoxLayout()
        row1.setSpacing(20)

        self.card_behavior = FluentCard("Behavior", AppColors.BEHAVIOR)
        self.card_fatigue = FluentCard("Fatigue", AppColors.FATIGUE)

        self.card_behavior.setMinimumHeight(260)
        self.card_fatigue.setMinimumHeight(260)

        row1.addWidget(self._wrap_blur(self.card_behavior))
        row1.addWidget(self._wrap_blur(self.card_fatigue))
        layout.addLayout(row1)

        # ============================================
        # ROW 2 — Next Break + Reason + Suppression
        # ============================================
        row2 = QHBoxLayout()
        row2.setSpacing(20)

        self.card_next_break = FluentCard("Next Break", AppColors.BREAK)
        self.card_reason = FluentCard("Reason", AppColors.INSIGHT, has_spark=False)
        self.card_suppression = FluentCard("Suppression", AppColors.SUPPRESSION, has_spark=False)

        self.card_next_break.setMinimumHeight(150)
        self.card_reason.setMinimumHeight(300)
        self.card_suppression.setMinimumHeight(180)
        self.card_next_break.setMaximumHeight(180)

        row2.addWidget(self._wrap_blur(self.card_next_break), 1)
        row2.addWidget(self._wrap_blur(self.card_reason), 2)
        row2.addWidget(self._wrap_blur(self.card_suppression), 1)
        layout.addLayout(row2)

        # ============================================
        # INSIGHT (Slim, professional summary)
        # ============================================
        self.card_insight = FluentCard("Insight", AppColors.INSIGHT, has_spark=False)
        self.card_insight.setMinimumHeight(140)
        layout.addWidget(self._wrap_blur(self.card_insight))

        layout.addStretch()

        # BUTTON — Left aligned
        self.btn_toggle = QPushButton("Start K-Mends AI")
        self.btn_toggle.setObjectName("PrimaryButton")
        self.btn_toggle.setFixedHeight(44)
        self.btn_toggle.clicked.connect(self.on_toggle_clicked)
        layout.addWidget(self.btn_toggle, 0, Qt.AlignLeft)

    def _wrap_blur(self, card: FluentCard) -> FluentBlur:
        blur = FluentBlur(radius=25, opacity=0.30)
        blur.layout.addWidget(card)
        return blur

    def on_toggle_clicked(self):
        self.main.show_ai()
        self.main.toggle_monitoring()
        self.btn_toggle.setText("Stop K-Mends AI" if self.main.monitoring else "Start K-Mends AI")

    # ============================================
    # PROFESSIONAL INSIGHT GENERATOR
    # ============================================
    def _generate_insight(self, behavior, fatigue, reason, next_break_minutes):
        fatigue = int(fatigue)
        nb_min = max(1, int(next_break_minutes))  # FIXED: already minutes

        if "meeting" in behavior.lower():
            return "You appear to be in a meeting. Break reminders are paused."

        if "watch" in behavior.lower():
            return "You’re watching content. Monitoring will resume when activity changes."

        if "suppressed" in reason.lower():
            return "Current activity suggests a break isn’t appropriate. Monitoring continues."

        if fatigue >= 70:
            return "Fatigue is elevated. A short pause soon may help maintain clarity."

        if fatigue >= 40:
            return "Fatigue is rising gradually. A break will be helpful in the next period."

        if nb_min <= 3:
            return "You’ve been active for a while. A break is coming up shortly."

        return f"Focus is steady and fatigue remains low. Your next break is in about {nb_min} minutes."

    # ============================================
    # UPDATE UI
    # ============================================
    def update_ai_status(self, behavior, fatigue, reason, trigger, next_break_minutes):

        # BEHAVIOR
        self.card_behavior.update_value(behavior)
        self.behavior_trend.append(len(self.behavior_trend) % 5)
        self.behavior_trend = self.behavior_trend[-30:]
        SparklineAnimator(self.card_behavior.spark, AppColors.BEHAVIOR).animate(self.behavior_trend)

        # FATIGUE
        if fatigue is None:
            self.card_fatigue.update_value("0%")
        else:
            self.card_fatigue.update_value(f"{int(fatigue)}%")

        self.fatigue_trend.append(int(fatigue))
        self.fatigue_trend = self.fatigue_trend[-30:]
        SparklineAnimator(self.card_fatigue.spark, AppColors.FATIGUE).animate(self.fatigue_trend)

        # REASON
        self.card_reason.update_value(reason)

        # NEXT BREAK (now in minutes)
        nb = max(0, int(next_break_minutes))
        self.card_next_break.update_value(f"{nb}m" if nb else "—")

        # FIXED: sparkline expects seconds for smooth animation
        self.break_trend.append(nb * 60)
        self.break_trend = self.break_trend[-30:]
        SparklineAnimator(self.card_next_break.spark, AppColors.BREAK).animate(self.break_trend)

        # SUPPRESSION
        if "suppressed" in reason.lower():
            self.card_suppression.update_value("Active")
            PulseAnimator(self.card_suppression).start()
        else:
            self.card_suppression.update_value("None")

        # INSIGHT
        insight = self._generate_insight(behavior, fatigue, reason, nb)
        self.card_insight.update_value(insight)

        # ANIMATIONS
        for card in [
            self.card_behavior, self.card_fatigue, self.card_reason,
            self.card_next_break, self.card_suppression, self.card_insight
        ]:
            FadeInAnimator(card).start()
            SlideInAnimator(card.accent).start()

    def _fatigue_value(self):
        text = self.card_fatigue.value_label.text().replace("%", "").strip()
        return int(text) if text.isdigit() else 0

    def sync_button_state(self):
        """Ensure the button text matches the actual monitoring state."""
        if self.main.monitoring:
            self.btn_toggle.setText("Stop K-Mends AI")
        else:
            self.btn_toggle.setText("Start K-Mends AI")
