


# # I changed the summary card
# # ui/pages/smart_mode.py

# import time
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
# from PySide6.QtCore import Qt

# from ui.pages.shared.fluent_card import FluentCard
# from ui.widgets.fluent_blur import FluentBlur
# from ui.core.theme import AppColors
# from ui.animations import (
#     FadeInAnimator, SlideInAnimator, SparklineAnimator,
#     ValueAnimator, PulseAnimator
# )


# class SmartModePage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.setObjectName("SmartModePage")

#         self.behavior_trend = []
#         self.fatigue_trend = []
#         self.interval_trend = []

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)
#         layout.setSpacing(20)

#         # ============================================
#         # TOP ROW — Timer + Behavior + Fatigue
#         # ============================================
#         top_row = QHBoxLayout()
#         top_row.setSpacing(20)

#         self.card_timer = FluentCard("K-Mends Mode Timer", AppColors.BREAK, has_spark=False)
#         self.card_timer.setMinimumHeight(260)
#         top_row.addWidget(self._wrap_blur(self.card_timer))

#         self.card_behavior = FluentCard("Behavior", AppColors.BEHAVIOR)
#         self.card_behavior.setMinimumHeight(260)
#         top_row.addWidget(self._wrap_blur(self.card_behavior))

#         self.card_fatigue = FluentCard("Fatigue", AppColors.FATIGUE)
#         self.card_fatigue.setMinimumHeight(260)
#         top_row.addWidget(self._wrap_blur(self.card_fatigue))

#         layout.addLayout(top_row)

#         # ============================================
#         # ROW 2 — Next Break + Reason + Suppression
#         # ============================================
#         row2 = QHBoxLayout()
#         row2.setSpacing(20)

#         self.card_next_break = FluentCard("Next Break", AppColors.BREAK)
#         self.card_next_break.setMinimumHeight(150)
#         self.card_next_break.setMaximumHeight(180)
#         row2.addWidget(self._wrap_blur(self.card_next_break), 1)

#         self.card_reason = FluentCard("Reason", AppColors.INSIGHT, has_spark=False)
#         self.card_reason.setMinimumHeight(300)
#         row2.addWidget(self._wrap_blur(self.card_reason), 2)

#         self.card_suppression = FluentCard("Suppression", AppColors.SUPPRESSION, has_spark=False)
#         self.card_suppression.setMinimumHeight(180)
#         row2.addWidget(self._wrap_blur(self.card_suppression), 1)

#         layout.addLayout(row2)

#         # ============================================
#         # INSIGHT (Slim, professional summary)
#         # ============================================
#         self.card_insight = FluentCard("Insight", AppColors.INSIGHT, has_spark=False)
#         self.card_insight.setMinimumHeight(140)
#         layout.addWidget(self._wrap_blur(self.card_insight))

#         layout.addStretch()

#         # BUTTON
#         self.btn_toggle = QPushButton("Start K-Mends Mode")
#         self.btn_toggle.setObjectName("PrimaryButton")
#         self.btn_toggle.setFixedHeight(44)
#         self.btn_toggle.clicked.connect(self.on_toggle_clicked)
#         layout.addWidget(self.btn_toggle, 0, Qt.AlignLeft)

#     def _wrap_blur(self, card: FluentCard) -> FluentBlur:
#         blur = FluentBlur(radius=25, opacity=0.30)
#         blur.layout.addWidget(card)
#         return blur

#     def on_toggle_clicked(self):
#         self.main.show_smart()
#         self.main.toggle_monitoring()
#         self.btn_toggle.setText("Stop K-Mends Mode" if self.main.monitoring else "Start K-Mends Mode")

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
#     def update_smart_status(self, behavior, fatigue, reason, trigger, next_break_seconds):
#         #print(f"[PAGE] UI received next_break_seconds={next_break_seconds}")

#         engine = self.main.hybrid_engine

#         # TIMER
#         elapsed = 0
#         if engine.session_start and self.main.monitoring and self.main.active_monitoring_mode == "Smart Mode":
#             elapsed = int(time.time() - engine.session_start)
#         self.card_timer.update_value(time.strftime("%H:%M:%S", time.gmtime(elapsed)))

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
#         self.interval_trend.append(nb)
#         self.interval_trend = self.interval_trend[-30:]
#         SparklineAnimator(self.card_next_break.spark, AppColors.BREAK).animate(self.interval_trend)

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
#             self.card_timer, self.card_behavior, self.card_fatigue,
#             self.card_reason, self.card_next_break, self.card_suppression,
#             self.card_insight
#         ]:
#             FadeInAnimator(card).start()
#             SlideInAnimator(card.accent).start()

#     def _fatigue_value(self):
#         text = self.card_fatigue.value_label.text().replace("%", "").strip()
#         return int(text) if text.isdigit() else 0


























# This is 29th update

# ui/pages/smart_mode.py

import time
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt

from ui.pages.shared.fluent_card import FluentCard
from ui.widgets.fluent_blur import FluentBlur
from ui.core.theme import AppColors
from ui.animations import (
    FadeInAnimator, SlideInAnimator, SparklineAnimator,
    ValueAnimator, PulseAnimator
)


class SmartModePage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setObjectName("SmartModePage")

        self.behavior_trend = []
        self.fatigue_trend = []
        self.interval_trend = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # ============================================
        # TOP ROW — Timer + Behavior + Fatigue
        # ============================================
        top_row = QHBoxLayout()
        top_row.setSpacing(20)

        self.card_timer = FluentCard("K-Mends Mode Timer", AppColors.BREAK, has_spark=False)
        self.card_timer.setMinimumHeight(260)
        top_row.addWidget(self._wrap_blur(self.card_timer))

        self.card_behavior = FluentCard("Behavior", AppColors.BEHAVIOR)
        self.card_behavior.setMinimumHeight(260)
        top_row.addWidget(self._wrap_blur(self.card_behavior))

        self.card_fatigue = FluentCard("Fatigue", AppColors.FATIGUE)
        self.card_fatigue.setMinimumHeight(260)
        top_row.addWidget(self._wrap_blur(self.card_fatigue))

        layout.addLayout(top_row)

        # ============================================
        # ROW 2 — Next Break + Reason + Suppression
        # ============================================
        row2 = QHBoxLayout()
        row2.setSpacing(20)

        self.card_next_break = FluentCard("Next Break", AppColors.BREAK)
        self.card_next_break.setMinimumHeight(150)
        self.card_next_break.setMaximumHeight(180)
        row2.addWidget(self._wrap_blur(self.card_next_break), 1)

        self.card_reason = FluentCard("Reason", AppColors.INSIGHT, has_spark=False)
        self.card_reason.setMinimumHeight(300)
        row2.addWidget(self._wrap_blur(self.card_reason), 2)

        self.card_suppression = FluentCard("Suppression", AppColors.SUPPRESSION, has_spark=False)
        self.card_suppression.setMinimumHeight(180)
        row2.addWidget(self._wrap_blur(self.card_suppression), 1)

        layout.addLayout(row2)

        # ============================================
        # INSIGHT (Slim, professional summary)
        # ============================================
        self.card_insight = FluentCard("Insight", AppColors.INSIGHT, has_spark=False)
        self.card_insight.setMinimumHeight(140)
        layout.addWidget(self._wrap_blur(self.card_insight))

        layout.addStretch()

        # BUTTON
        self.btn_toggle = QPushButton("Start K-Mends Mode")
        self.btn_toggle.setObjectName("PrimaryButton")
        self.btn_toggle.setFixedHeight(44)
        self.btn_toggle.clicked.connect(self.on_toggle_clicked)
        layout.addWidget(self.btn_toggle, 0, Qt.AlignLeft)

    def _wrap_blur(self, card: FluentCard) -> FluentBlur:
        blur = FluentBlur(radius=25, opacity=0.30)
        blur.layout.addWidget(card)
        return blur

    def on_toggle_clicked(self):
        self.main.show_smart()
        self.main.toggle_monitoring()
        self.btn_toggle.setText("Stop K-Mends Mode" if self.main.monitoring else "Start K-Mends Mode")

    # ============================================
    # PROFESSIONAL INSIGHT GENERATOR
    # ============================================
    def _generate_insight(self, behavior, fatigue, reason, next_break_minutes):
        fatigue = int(fatigue) if fatigue is not None else 0
        nb_min = max(1, int(next_break_minutes))  # Already minutes now

        # 1. ACTIVITY STATE
        if "meeting" in behavior.lower():
            return "You appear to be in a meeting. Break reminders are paused to respect your flow."

        if "watch" in behavior.lower():
            return "Entertainment mode detected. Monitoring will resume shortly."

        if "suppressed" in reason.lower():
            return "Active engagement detected. We'll hold off on reminders for now."

        # 2. PHYSICAL STATE
        if fatigue >= 70:
            return "Fatigue levels are significant. Consider a brief reset to maintain clarity."

        if fatigue >= 40:
            return "Energy is dipping slightly. A break in the near future would be beneficial."

        # 3. TIMELINE STATE
        if nb_min <= 1:
            return "Your scheduled wellness break is starting shortly."

        if nb_min <= 3:
            return f"You’ve been focused for a productive stretch. A break is approaching in {nb_min} minutes."

        # 4. DEFAULT
        return f"Focus is consistent. Your next optimal break window is in approximately {nb_min} minutes."

    # ============================================
    # UPDATE UI
    # ============================================
    def update_smart_status(self, behavior, fatigue, reason, trigger, next_break_minutes):
        engine = self.main.hybrid_engine

        # TIMER (H:M:S)
        elapsed = 0
        if engine.session_start and self.main.monitoring and self.main.active_monitoring_mode == "Smart Mode":
            elapsed = int(time.time() - engine.session_start)
        self.card_timer.update_value(time.strftime("%H:%M:%S", time.gmtime(elapsed)))

        # BEHAVIOR
        self.card_behavior.update_value(behavior)
        self.behavior_trend.append(len(self.behavior_trend) % 5)
        self.behavior_trend = self.behavior_trend[-30:]
        SparklineAnimator(self.card_behavior.spark, AppColors.BEHAVIOR).animate(self.behavior_trend)

        # FATIGUE
        f_val = int(fatigue) if fatigue is not None else 0
        self.card_fatigue.update_value(f"{f_val}%")
        self.fatigue_trend.append(f_val)
        self.fatigue_trend = self.fatigue_trend[-30:]
        SparklineAnimator(self.card_fatigue.spark, AppColors.FATIGUE).animate(self.fatigue_trend)

        # REASON
        self.card_reason.update_value(reason)

        # NEXT BREAK (now in minutes)
        nb = max(0, int(next_break_minutes))
        display_time = f"{nb}m" if nb > 0 else "—"

        self.card_next_break.update_value(display_time)

        # Sparkline expects a descending curve → convert minutes back to seconds
        self.interval_trend.append(nb * 60)
        self.interval_trend = self.interval_trend[-30:]
        SparklineAnimator(self.card_next_break.spark, AppColors.BREAK).animate(self.interval_trend)

        # SUPPRESSION
        if "suppressed" in reason.lower():
            self.card_suppression.update_value("Active")
            PulseAnimator(self.card_suppression).start()
        else:
            self.card_suppression.update_value("None")

        # INSIGHT
        insight_text = self._generate_insight(behavior, f_val, reason, nb)
        self.card_insight.update_value(insight_text)

        # ANIMATIONS
        for card in [
            self.card_timer, self.card_behavior, self.card_fatigue,
            self.card_reason, self.card_next_break, self.card_suppression,
            self.card_insight
        ]:
            FadeInAnimator(card).start()
            SlideInAnimator(card.accent).start()

    def _fatigue_value(self):
        text = self.card_fatigue.value_label.text().replace("%", "").strip()
        return int(text) if text.isdigit() else 0








# 25th March

# # ui/pages/smart_mode.py

# import time
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
# from PySide6.QtCore import Qt

# from ui.pages.shared.fluent_card import FluentCard
# from ui.widgets.fluent_blur import FluentBlur
# from ui.core.theme import AppColors
# from ui.animations import (
#     FadeInAnimator, SlideInAnimator, SparklineAnimator,
#     ValueAnimator, PulseAnimator
# )


# class SmartModePage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.setObjectName("SmartModePage")

#         self.behavior_trend = []
#         self.fatigue_trend = []
#         self.interval_trend = []

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)
#         layout.setSpacing(20)

#         # ============================================
#         # TOP ROW — Timer + Behavior + Fatigue
#         # ============================================
#         top_row = QHBoxLayout()
#         top_row.setSpacing(20)

#         self.card_timer = FluentCard("K-Mends Mode Timer", AppColors.BREAK, has_spark=False)
#         self.card_timer.setMinimumHeight(260)
#         top_row.addWidget(self._wrap_blur(self.card_timer))

#         self.card_behavior = FluentCard("Behavior", AppColors.BEHAVIOR)
#         self.card_behavior.setMinimumHeight(260)
#         top_row.addWidget(self._wrap_blur(self.card_behavior))

#         self.card_fatigue = FluentCard("Fatigue", AppColors.FATIGUE)
#         self.card_fatigue.setMinimumHeight(260)
#         top_row.addWidget(self._wrap_blur(self.card_fatigue))

#         layout.addLayout(top_row)

#         # ============================================
#         # ROW 2 — Next Break + Reason + Suppression
#         # ============================================
#         row2 = QHBoxLayout()
#         row2.setSpacing(20)

#         self.card_next_break = FluentCard("Next Break", AppColors.BREAK)
#         self.card_next_break.setMinimumHeight(150)
#         self.card_next_break.setMaximumHeight(180)
#         row2.addWidget(self._wrap_blur(self.card_next_break), 1)

#         self.card_reason = FluentCard("Reason", AppColors.INSIGHT, has_spark=False)
#         self.card_reason.setMinimumHeight(300)
#         row2.addWidget(self._wrap_blur(self.card_reason), 2)

#         self.card_suppression = FluentCard("Suppression", AppColors.SUPPRESSION, has_spark=False)
#         self.card_suppression.setMinimumHeight(180)
#         row2.addWidget(self._wrap_blur(self.card_suppression), 1)

#         layout.addLayout(row2)

#         # ============================================
#         # INSIGHT (Slim, professional summary)
#         # ============================================
#         self.card_insight = FluentCard("Insight", AppColors.INSIGHT, has_spark=False)
#         self.card_insight.setMinimumHeight(140)
#         layout.addWidget(self._wrap_blur(self.card_insight))

#         layout.addStretch()

#         # BUTTON
#         self.btn_toggle = QPushButton("Start K-Mends Mode")
#         self.btn_toggle.setObjectName("PrimaryButton")
#         self.btn_toggle.setFixedHeight(44)
#         self.btn_toggle.clicked.connect(self.on_toggle_clicked)
#         layout.addWidget(self.btn_toggle, 0, Qt.AlignLeft)

#     def _wrap_blur(self, card: FluentCard) -> FluentBlur:
#         blur = FluentBlur(radius=25, opacity=0.30)
#         blur.layout.addWidget(card)
#         return blur

#     def on_toggle_clicked(self):
#         self.main.show_smart()
#         self.main.toggle_monitoring()
#         self.btn_toggle.setText("Stop K-Mends Mode" if self.main.monitoring else "Start K-Mends Mode")

#     # ============================================
#     # PROFESSIONAL INSIGHT GENERATOR
#     # ============================================
#     def _generate_insight(self, behavior, fatigue, reason, next_break_seconds):
#         fatigue = int(fatigue) if fatigue is not None else 0
#         nb_min = next_break_seconds // 60

#         # 1. ACTIVITY STATE
#         if "meeting" in behavior.lower():
#             return "You appear to be in a meeting. Break reminders are paused to respect your flow."
#         if "watch" in behavior.lower():
#             return "Entertainment mode detected. Wellbeing monitoring will resume shortly."
#         if "suppressed" in reason.lower():
#             return "Active engagement detected. We'll hold off on reminders for now."

#         # 2. PHYSICAL STATE
#         if fatigue >= 70:
#             return "Fatigue levels are significant. Consider a brief reset to maintain peak performance."
#         if fatigue >= 40:
#             return "Energy is dipping slightly. A break in the near future would be beneficial."

#         # 3. TIMELINE STATE
#         if next_break_seconds < 60:
#             return "Your scheduled wellness break is starting in just a few seconds."
        
#         if nb_min <= 3:
#             return f"You’ve been focused for a productive stretch. A break is approaching in {nb_min} minutes."

#         # 4. DEFAULT
#         return f"Focus is consistent. Your next optimal break window is in approximately {nb_min} minutes."
#     # ============================================
#     # UPDATE UI
#     # ============================================
#     def update_smart_status(self, behavior, fatigue, reason, trigger, next_break_seconds):
#         engine = self.main.hybrid_engine

#         # TIMER (H:M:S)
#         elapsed = 0
#         if engine.session_start and self.main.monitoring and self.main.active_monitoring_mode == "Smart Mode":
#             elapsed = int(time.time() - engine.session_start)
#         self.card_timer.update_value(time.strftime("%H:%M:%S", time.gmtime(elapsed)))

#         # BEHAVIOR
#         self.card_behavior.update_value(behavior)
#         self.behavior_trend.append(len(self.behavior_trend) % 5)
#         self.behavior_trend = self.behavior_trend[-30:]
#         SparklineAnimator(self.card_behavior.spark, AppColors.BEHAVIOR).animate(self.behavior_trend)

#         # FATIGUE
#         f_val = int(fatigue) if fatigue is not None else 0
#         self.card_fatigue.update_value(f"{f_val}%")
#         self.fatigue_trend.append(f_val)
#         self.fatigue_trend = self.fatigue_trend[-30:]
#         SparklineAnimator(self.card_fatigue.spark, AppColors.FATIGUE).animate(self.fatigue_trend)

#         # REASON
#         self.card_reason.update_value(reason)

#         # NEXT BREAK (PREMIUM FORMATTING)
#         nb_raw = max(0, int(next_break_seconds))
        
#         if nb_raw == 0:
#             display_time = "—"
#         elif nb_raw < 60:
#             display_time = f"{nb_raw}s"
#         else:
#             nb_display_min = round(nb_raw / 60)
#             display_time = f"{nb_display_min}m"

#         self.card_next_break.update_value(display_time)
#         self.interval_trend.append(nb_raw)
#         self.interval_trend = self.interval_trend[-30:]
#         SparklineAnimator(self.card_next_break.spark, AppColors.BREAK).animate(self.interval_trend)

#         # SUPPRESSION
#         if "suppressed" in reason.lower():
#             self.card_suppression.update_value("Active")
#             PulseAnimator(self.card_suppression).start()
#         else:
#             self.card_suppression.update_value("None")

#         # INSIGHT (Corrected variable passing)
#         insight_text = self._generate_insight(behavior, f_val, reason, nb_raw)
#         self.card_insight.update_value(insight_text)

#         # ANIMATIONS
#         for card in [
#             self.card_timer, self.card_behavior, self.card_fatigue,
#             self.card_reason, self.card_next_break, self.card_suppression,
#             self.card_insight
#         ]:
#             FadeInAnimator(card).start()
#             SlideInAnimator(card.accent).start()
            
#     def _fatigue_value(self):
#         text = self.card_fatigue.value_label.text().replace("%", "").strip()
#         return int(text) if text.isdigit() else 0
