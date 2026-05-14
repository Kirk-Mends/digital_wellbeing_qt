


# 29th March
# Adding auto sync
import pyqtgraph as pg
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, 
    QFrame, QScrollArea, QPushButton, QApplication
)
from PySide6.QtCore import Qt, QTimer, QVariantAnimation
from PySide6.QtGui import QColor
from datetime import datetime

# --- ENGINE IMPORT ---
try:
    from core.analytics_engine import AnalyticsEngine
except ImportError:
    class AnalyticsEngine:
        def behavior_distribution(self): return {"Deep Work": 60, "Reading": 25, "Browsing": 15}
        def fatigue_trend(self): return {"fatigue": [20, 22, 35, 50, 45, 30, 40, 55, 35, 42]}
        def longest_behavior_streak(self): return {"minutes": 110, "behavior": "Deep Work"}
        def ai_insights(self): return ["Focus is highly optimized.", "Fatigue spike detected at 11 AM."]

# ============================================================
# PREMIUM COMPONENT: FLUENT CARD
# ============================================================
class FluentAnalyticsCard(QFrame):
    def __init__(self, title):
        super().__init__()
        self.setObjectName("FluentCard") 
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        self.title_lbl = QLabel(title)
        self.title_lbl.setObjectName("AnalyticsCardTitle") 
        layout.addWidget(self.title_lbl)
        
        self.body = QVBoxLayout()
        layout.addLayout(self.body)

    def add_fluent_plot(self, mode="dark"):
        plot = pg.PlotWidget()
        plot.setBackground(None)
        plot.setAntialiasing(True)
        plot.setMenuEnabled(False)
        plot.setMouseEnabled(x=False, y=False)
        plot.hideButtons()

        # Apply initial theme colors
        self.apply_theme_to_axis(plot, mode)

        plot.getAxis('left').hide()
        self.body.addWidget(plot)
        return plot

    def apply_theme_to_axis(self, plot, mode):
        """Helper to ensure text color is consistent across all modes"""
        if mode == "blue":
            text_color = QColor("#003A8C")      # Deep blue
        elif mode == "light":
            text_color = QColor("#0057D9")      # Black
        else:  # DARK MODE
            text_color = QColor("#0057D9")      # Cream white

        ax = plot.getAxis('bottom')
        ax.setTextPen(text_color)
        # Also set the pen for the line itself to keep it subtle
        ax.setPen(pg.mkPen(text_color, width=1, cosmetic=True))

# ============================================================
# EXECUTIVE DASHBOARD PAGE
# ============================================================
class AnalyticsSuitePage(QWidget):
    def __init__(self, theme="light"):
        super().__init__()
        self.engine = AnalyticsEngine()
        
        t = theme.lower()
        if "dark" in t:
            self.mode = "dark"
            self.accent = "#0057D9"
        elif "blue" in t:
            self.mode = "blue"
            self.accent = "#0057D9"
        else:
            self.mode = "light"
            self.accent = "#0057D9"
            
        self.setup_ui()

        # 2. AUTO-SYNC TIMER (Every 60 Seconds)
        self.autosync_timer = QTimer(self)
        self.autosync_timer.timeout.connect(self.refresh_all)
        self.autosync_timer.start(60000) 
        
        QTimer.singleShot(100, self.refresh_all)

    def setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(35, 30, 35, 30)
        root.setSpacing(25)

        # --- PREMIUM HEADER ---
        header = QHBoxLayout()
        title_container = QVBoxLayout()
        
        self.title_lbl = QLabel("Performance Insights")
        self.title_lbl.setObjectName("PageTitle")
        
        self.live_status = QLabel("● LIVE AUTO-SYNC ACTIVE")
        self.live_status.setStyleSheet(f"color: {self.accent}; font-size: 10px; font-weight: bold; letter-spacing: 1px;")
        
        title_container.addWidget(self.title_lbl)
        title_container.addWidget(self.live_status)
        header.addLayout(title_container)
        header.addStretch()
        
        self.refresh_button = QPushButton("Sync Now")
        self.refresh_button.setObjectName("PrimaryButton")
        self.refresh_button.setCursor(Qt.PointingHandCursor)
        self.refresh_button.clicked.connect(self.refresh_all)
        header.addWidget(self.refresh_button)
        root.addLayout(header)

        # --- NAVIGATION TABS ---
        self.tabs = QTabWidget()
        self.tabs.setObjectName("AnalyticsTabs")
        root.addWidget(self.tabs)

        self._setup_focus_view()
        self._setup_recovery_view()
        self._setup_trends_view()

    def _setup_focus_view(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 15, 0, 0)
        
        row = QHBoxLayout()
        self.card_dist = FluentAnalyticsCard("Focus Distribution")
        self.plot_dist = self.card_dist.add_fluent_plot(self.mode)
        
        self.card_streak = FluentAnalyticsCard("Peak Performance")
        self.streak_val = QLabel("0m")
        self.streak_val.setObjectName("CardValue")
        self.streak_val.setStyleSheet("font-size: 48px; font-weight: 800;")
        
        self.streak_sub = QLabel("Monitoring focus states...")
        self.streak_sub.setObjectName("InsightText")
        
        self.card_streak.body.addStretch()
        self.card_streak.body.addWidget(self.streak_val, alignment=Qt.AlignCenter)
        self.card_streak.body.addWidget(self.streak_sub, alignment=Qt.AlignCenter)
        self.card_streak.body.addStretch()
        
        row.addWidget(self.card_dist, 2)
        row.addWidget(self.card_streak, 1)
        layout.addLayout(row)
        self.tabs.addTab(container, "Focus")

    def _setup_recovery_view(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 15, 0, 0)
        
        self.card_fatigue = FluentAnalyticsCard("Cognitive Load Analysis")
        self.card_fatigue.setFixedHeight(400)
        self.plot_fatigue = self.card_fatigue.add_fluent_plot(self.mode)
        layout.addWidget(self.card_fatigue)
        
        self.tabs.addTab(container, "Recovery")

    def _setup_trends_view(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 15, 0, 0)
        
        self.card_ai = FluentAnalyticsCard("Executive AI Briefing")
        self.card_ai.setFixedHeight(450)
        
        self.ai_content_layout = QVBoxLayout()
        self.ai_content_layout.setSpacing(15)
        
        self.update_time_lbl = QLabel("Awaiting synchronization...")
        self.update_time_lbl.setObjectName("InsightText")
        self.update_time_lbl.setStyleSheet("opacity: 0.6; font-style: italic;")
        self.ai_content_layout.addWidget(self.update_time_lbl)

        self.ai_lbl = QLabel("Processing behavioral patterns...")
        self.ai_lbl.setObjectName("InsightText")
        self.ai_lbl.setWordWrap(True)
        self.ai_lbl.setStyleSheet("font-size: 15px; line-height: 160%; padding: 10px;")
        
        self.ai_content_layout.addWidget(self.ai_lbl)
        self.ai_content_layout.addStretch()
        
        self.card_ai.body.addLayout(self.ai_content_layout)
        layout.addWidget(self.card_ai)
        self.tabs.addTab(container, "Trends")

    def animate_sync_pulse(self):
        base_color = QColor(self.accent)
        glow_color = base_color.lighter(150)

        self.pulse_anim = QVariantAnimation(self)
        self.pulse_anim.setDuration(600)
        self.pulse_anim.setStartValue(glow_color)
        self.pulse_anim.setEndValue(base_color)
        
        def set_button_style(color):
            self.refresh_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color.name()};
                    color: white;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-weight: 600;
                    border: none;
                }}
            """)

        self.pulse_anim.valueChanged.connect(set_button_style)
        self.pulse_anim.start()

    def refresh_all(self):
        # 1. Update Distribution
        dist = self.engine.behavior_distribution()
        self.plot_dist.clear()
        if dist:
            x = range(len(dist))
            bg = pg.BarGraphItem(
                x=list(x),
                height=list(dist.values()),
                width=0.6,
                brush=self.accent,
                pen=None
            )
            self.plot_dist.addItem(bg)
            self.plot_dist.getAxis('bottom').setTicks([list(zip(x, dist.keys()))])
            
            # Re-apply color theme to fix potential reset after clear()
            self.card_dist.apply_theme_to_axis(self.plot_dist, self.mode)

        # 2. Update Fatigue Sparkline
        fat_data = self.engine.fatigue_trend().get("fatigue", [])
        self.plot_fatigue.clear()
        if fat_data:
            line_color = "#FF9500" if self.mode != "dark" else "#FF9F0A"
            curve = self.plot_fatigue.plot(
                fat_data,
                pen=pg.mkPen(QColor(line_color), width=4),
                antialias=True
            )

            fill_color = QColor(line_color)
            fill_color.setAlpha(35)
            fill = pg.FillBetweenItem(
                pg.PlotDataItem(y=[0] * len(fat_data)),
                curve,
                brush=fill_color
            )
            self.plot_fatigue.addItem(fill)
            
            # FIX: Re-apply color theme to Fatigue plot axis text
            self.card_fatigue.apply_theme_to_axis(self.plot_fatigue, self.mode)
            self.plot_fatigue.enableAutoRange()

        # 3. Update AI Summary
        insights = self.engine.ai_insights()
        if insights:
            self.ai_lbl.setText("\n\n".join([f"• {i}" for i in insights]))
            self.update_time_lbl.setText(
                f"Last updated: {datetime.now().strftime('%H:%M:%S')}"
            )

        # 4. Update Overview Values
        streak = self.engine.longest_behavior_streak()
        if streak:
            self.streak_val.setText(f"{int(streak['minutes']):,}m")
            self.streak_sub.setText(f"Peak: {streak['behavior']}")

        self.animate_sync_pulse()