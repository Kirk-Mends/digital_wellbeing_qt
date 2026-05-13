
# # new architectural version

# from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame
# from PySide6.QtGui import QIcon


# class Sidebar(QWidget):
#     def __init__(self, main_window):
#         super().__init__()
#         self.main = main_window

#         # Sidebar state
#         self.expanded_width = 200
#         self.collapsed_width = 56
#         self.is_expanded = True

#         self.setMinimumWidth(self.expanded_width)
#         self.setObjectName("Sidebar")

#         # -------------------------
#         # MAIN LAYOUT
#         # -------------------------
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

#         # -------------------------
#         # HAMBURGER BUTTON
#         # -------------------------
#         self.btn_toggle = QPushButton()
#         self.btn_toggle.setIcon(QIcon("assets/icons/hamburger.svg"))
#         self.btn_toggle.setIconSize(QSize(20, 20))
#         self.btn_toggle.setObjectName("HamburgerButton")
#         self.btn_toggle.clicked.connect(self.toggle_sidebar)
#         self.btn_toggle.setCursor(Qt.PointingHandCursor)
#         layout.addWidget(self.btn_toggle)

#         # -------------------------
#         # NAVIGATION BUTTONS
#         # -------------------------
#         self.btn_dashboard = self.make_button(
#             "Dashboard", "assets/icons/dashboard.svg", self.main.show_dashboard
#         )
#         self.btn_smart = self.make_button(
#             "Smart Mode", "assets/icons/smart_mode.svg", self.main.show_smart
#         )
#         self.btn_ai = self.make_button(
#             "AI Mode", "assets/icons/ai_mode.svg", self.main.show_ai
#         )

#         layout.addWidget(self.btn_dashboard)
#         layout.addWidget(self.btn_smart)
#         layout.addWidget(self.btn_ai)

  
#         # -------------------------
#         # ANALYTICS SECTION
#         # -------------------------
#         self.btn_analytics = self.make_button(
#             "Analytics", "assets/icons/analytics.svg", self.main.show_analytics
#         )
#         self.btn_weekly = self.make_button(
#             "Weekly Analytics", "assets/icons/weekly_report.svg", self.main.show_weekly
#         )
#         self.btn_insights = self.make_button(
#             "AI Insights", "assets/icons/ai_mode.svg", self.main.show_insights
#         )
#         self.btn_weekly_report = self.make_button(
#             "Weekly Report", "assets/icons/weekly_report.svg", self.main.show_weekly_report
#         )
#         self.btn_monthly_report = self.make_button(
#             "Monthly Report", "assets/icons/monthly_report.svg", self.main.show_monthly_report
#         )

#         layout.addWidget(self.btn_analytics)
#         layout.addWidget(self.btn_weekly)
#         layout.addWidget(self.btn_insights)
#         layout.addWidget(self.btn_weekly_report)
#         layout.addWidget(self.btn_monthly_report)

#         layout.addStretch()

#         # -------------------------
#         # SETTINGS BUTTON
#         # -------------------------
#         self.btn_settings = self.make_button(
#             "Settings", "assets/icons/settings.svg", self.main.show_settings
#         )
#         layout.addWidget(self.btn_settings)

#         # -------------------------
#         # STORE BUTTONS FOR ACTIVE/HOVER LOGIC
#         # -------------------------
#         self.buttons = [
#             self.btn_dashboard,
#             self.btn_smart,
#             self.btn_ai,
#             self.btn_analytics,
#             self.btn_weekly,
#             self.btn_insights,
#             self.btn_weekly_report,
#             self.btn_monthly_report,
#             self.btn_settings
#         ]

#         # Store full text for collapse mode
#         for btn in self.buttons:
#             btn.setProperty("full_text", btn.text())

#     # -------------------------------------------------------
#     # CREATE A NAVIGATION BUTTON
#     # -------------------------------------------------------
#     def make_button(self, text, icon_path, callback):
#         btn = QPushButton(text)
#         btn.setIcon(QIcon(icon_path))
#         btn.setIconSize(QSize(20, 20))
#         btn.setCursor(Qt.PointingHandCursor)
#         btn.setObjectName("SidebarButton")

#         # Hover glow
#         btn.setProperty("hover", False)
#         btn.enterEvent = lambda e, b=btn: self.on_hover(b, True)
#         btn.leaveEvent = lambda e, b=btn: self.on_hover(b, False)

#         # Active highlight
#         btn.clicked.connect(lambda: self.set_active(btn, callback))

#         return btn

#     # -------------------------------------------------------
#     # HOVER EFFECT
#     # -------------------------------------------------------
#     def on_hover(self, btn, state):
#         btn.setProperty("hover", state)
#         btn.style().unpolish(btn)
#         btn.style().polish(btn)

#     # -------------------------------------------------------
#     # SET ACTIVE BUTTON (ACCENT BAR)
#     # -------------------------------------------------------
#     def set_active(self, btn, callback):
#         for b in self.buttons:
#             b.setProperty("active", False)
#             b.style().unpolish(b)
#             b.style().polish(b)

#         btn.setProperty("active", True)
#         btn.style().unpolish(btn)
#         btn.style().polish(btn)

#         callback()

#     # -------------------------------------------------------
#     # ANIMATE SIDEBAR WIDTH
#     # -------------------------------------------------------
#     def animate_width(self, start, end, duration=250):
#         self.anim = QPropertyAnimation(self, b"minimumWidth")
#         self.anim.setDuration(duration)
#         self.anim.setStartValue(start)
#         self.anim.setEndValue(end)
#         self.anim.setEasingCurve(QEasingCurve.InOutCubic)
#         self.anim.start()

#     # -------------------------------------------------------
#     # COLLAPSE / EXPAND SIDEBAR
#     # -------------------------------------------------------
#     def toggle_sidebar(self):
#         target_width = self.collapsed_width if self.is_expanded else self.expanded_width
#         self.is_expanded = not self.is_expanded

#         # Animate width
#         self.animate_width(self.width(), target_width)

#         # Hide/show text on buttons
#         for btn in self.buttons:
#             full_text = btn.property("full_text")
#             btn.setText(full_text if self.is_expanded else "")

#     # -------------------------------------------------------
#     # MEETING MODE HIGHLIGHT
#     # -------------------------------------------------------
#     def set_meeting_mode(self, active: bool):
#         # Highlight Smart Mode + AI Mode buttons during meetings
#         self.btn_smart.setProperty("meeting", active)
#         self.btn_ai.setProperty("meeting", active)

#         for btn in (self.btn_smart, self.btn_ai):
#             btn.style().unpolish(btn)
#             btn.style().polish(btn)











# THIS IS PERFECT
# Changing to brand name K-Mends


# # new architectural version

# from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame
# from PySide6.QtGui import QIcon


# class Sidebar(QWidget):
#     def __init__(self, main_window):
#         super().__init__()
#         self.main = main_window

#         # Sidebar state
#         self.expanded_width = 200
#         self.collapsed_width = 56
#         self.is_expanded = True

#         self.setMinimumWidth(self.expanded_width)
#         self.setObjectName("Sidebar")

#         # -------------------------
#         # MAIN LAYOUT
#         # -------------------------
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

#         # -------------------------
#         # HAMBURGER BUTTON
#         # -------------------------
#         self.btn_toggle = QPushButton()
#         self.btn_toggle.setIcon(QIcon("assets/icons/hamburger.svg"))
#         self.btn_toggle.setIconSize(QSize(20, 20))
#         self.btn_toggle.setObjectName("HamburgerButton")
#         self.btn_toggle.clicked.connect(self.toggle_sidebar)
#         self.btn_toggle.setCursor(Qt.PointingHandCursor)
#         layout.addWidget(self.btn_toggle)

#         # -------------------------
#         # NAVIGATION BUTTONS
#         # -------------------------
#         self.btn_dashboard = self.make_button(
#             "Dashboard", "assets/icons/dashboard.svg", self.main.show_dashboard
#         )
#         self.btn_smart = self.make_button(
#             "K‑Mends Mode", "assets/icons/smart_mode.svg", self.main.show_smart
#         )
#         self.btn_ai = self.make_button(
#             "K‑Mends AI", "assets/icons/ai_mode.svg", self.main.show_ai
#         )

#         layout.addWidget(self.btn_dashboard)
#         layout.addWidget(self.btn_smart)
#         layout.addWidget(self.btn_ai)

#         # -------------------------
#         # ANALYTICS SECTION
#         # -------------------------
#         self.btn_analytics = self.make_button(
#             "Analytics", "assets/icons/analytics.svg", self.main.show_analytics
#         )
#         self.btn_weekly = self.make_button(
#             "Weekly Analytics", "assets/icons/weekly_report.svg", self.main.show_weekly
#         )
#         self.btn_insights = self.make_button(
#             "Insights", "assets/icons/ai_mode.svg", self.main.show_insights
#         )
#         self.btn_weekly_report = self.make_button(
#             "Weekly Report", "assets/icons/weekly_report.svg", self.main.show_weekly_report
#         )
#         self.btn_monthly_report = self.make_button(
#             "Monthly Report", "assets/icons/monthly_report.svg", self.main.show_monthly_report
#         )

#         layout.addWidget(self.btn_analytics)
#         layout.addWidget(self.btn_weekly)
#         layout.addWidget(self.btn_insights)
#         layout.addWidget(self.btn_weekly_report)
#         layout.addWidget(self.btn_monthly_report)

#         layout.addStretch()

#         # -------------------------
#         # SETTINGS BUTTON
#         # -------------------------
#         self.btn_settings = self.make_button(
#             "Settings", "assets/icons/settings.svg", self.main.show_settings
#         )
#         layout.addWidget(self.btn_settings)

#         # -------------------------
#         # STORE BUTTONS FOR ACTIVE/HOVER LOGIC
#         # -------------------------
#         self.buttons = [
#             self.btn_dashboard,
#             self.btn_smart,
#             self.btn_ai,
#             self.btn_analytics,
#             self.btn_weekly,
#             self.btn_insights,
#             self.btn_weekly_report,
#             self.btn_monthly_report,
#             self.btn_settings
#         ]

#         # Store full text for collapse mode
#         for btn in self.buttons:
#             btn.setProperty("full_text", btn.text())

#     # -------------------------------------------------------
#     # CREATE A NAVIGATION BUTTON
#     # -------------------------------------------------------
#     def make_button(self, text, icon_path, callback):
#         btn = QPushButton(text)
#         btn.setIcon(QIcon(icon_path))
#         btn.setIconSize(QSize(20, 20))
#         btn.setCursor(Qt.PointingHandCursor)
#         btn.setObjectName("SidebarButton")

#         # Hover glow
#         btn.setProperty("hover", False)
#         btn.enterEvent = lambda e, b=btn: self.on_hover(b, True)
#         btn.leaveEvent = lambda e, b=btn: self.on_hover(b, False)

#         # Active highlight
#         btn.clicked.connect(lambda: self.set_active(btn, callback))

#         return btn

#     # -------------------------------------------------------
#     # HOVER EFFECT
#     # -------------------------------------------------------
#     def on_hover(self, btn, state):
#         btn.setProperty("hover", state)
#         btn.style().unpolish(btn)
#         btn.style().polish(btn)

#     # -------------------------------------------------------
#     # SET ACTIVE BUTTON (ACCENT BAR)
#     # -------------------------------------------------------
#     def set_active(self, btn, callback):
#         for b in self.buttons:
#             b.setProperty("active", False)
#             b.style().unpolish(b)
#             b.style().polish(b)

#         btn.setProperty("active", True)
#         btn.style().unpolish(btn)
#         btn.style().polish(btn)

#         callback()

#     # -------------------------------------------------------
#     # ANIMATE SIDEBAR WIDTH
#     # -------------------------------------------------------
#     def animate_width(self, start, end, duration=250):
#         self.anim = QPropertyAnimation(self, b"minimumWidth")
#         self.anim.setDuration(duration)
#         self.anim.setStartValue(start)
#         self.anim.setEndValue(end)
#         self.anim.setEasingCurve(QEasingCurve.InOutCubic)
#         self.anim.start()

#     # -------------------------------------------------------
#     # COLLAPSE / EXPAND SIDEBAR
#     # -------------------------------------------------------
#     def toggle_sidebar(self):
#         target_width = self.collapsed_width if self.is_expanded else self.expanded_width
#         self.is_expanded = not self.is_expanded

#         # Animate width
#         self.animate_width(self.width(), target_width)

#         # Hide/show text on buttons
#         for btn in self.buttons:
#             full_text = btn.property("full_text")
#             btn.setText(full_text if self.is_expanded else "")

#     # -------------------------------------------------------
#     # MEETING MODE HIGHLIGHT
#     # -------------------------------------------------------
#     def set_meeting_mode(self, active: bool):
#         self.btn_smart.setProperty("meeting", active)
#         self.btn_ai.setProperty("meeting", active)

#         for btn in (self.btn_smart, self.btn_ai):
#             btn.style().unpolish(btn)
#             btn.style().polish(btn)











# # 26th arch to use the resource qrc
# import os
# import sys
# from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
# from PySide6.QtGui import QIcon

# # --- DYNAMIC PATH LOGIC (FIX FOR EXE) ---
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# class Sidebar(QWidget):
#     def __init__(self, main_window):
#         super().__init__()
#         self.main = main_window

#         # Sidebar state
#         self.expanded_width = 200
#         self.collapsed_width = 56
#         self.is_expanded = True

#         self.setMinimumWidth(self.expanded_width)
#         self.setObjectName("Sidebar")

#         # -------------------------
#         # MAIN LAYOUT
#         # -------------------------
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setSpacing(0)

#         # -------------------------
#         # HAMBURGER BUTTON
#         # -------------------------
#         self.btn_toggle = QPushButton()
#         # FIXED: Wrapped icon path in resource_path
#         hamb_icon = resource_path(os.path.join("assets", "icons", "hamburger.svg"))
#         self.btn_toggle.setIcon(QIcon(hamb_icon))
        
#         self.btn_toggle.setIconSize(QSize(20, 20))
#         self.btn_toggle.setObjectName("HamburgerButton")
#         self.btn_toggle.clicked.connect(self.toggle_sidebar)
#         self.btn_toggle.setCursor(Qt.PointingHandCursor)
#         layout.addWidget(self.btn_toggle)

#         # -------------------------
#         # NAVIGATION BUTTONS
#         # -------------------------
#         self.btn_dashboard = self.make_button(
#             "Dashboard", "assets/icons/dashboard.svg", self.main.show_dashboard
#         )
#         self.btn_smart = self.make_button(
#             "K‑Mends Mode", "assets/icons/smart_mode.svg", self.main.show_smart
#         )
#         self.btn_ai = self.make_button(
#             "K‑Mends AI", "assets/icons/ai_mode.svg", self.main.show_ai
#         )

#         layout.addWidget(self.btn_dashboard)
#         layout.addWidget(self.btn_smart)
#         layout.addWidget(self.btn_ai)

#         # -------------------------
#         # ANALYTICS SECTION
#         # -------------------------
#         self.btn_analytics = self.make_button(
#             "Analytics", "assets/icons/analytics.svg", self.main.show_analytics
#         )
#         self.btn_weekly = self.make_button(
#             "Weekly Analytics", "assets/icons/weekly_report.svg", self.main.show_weekly
#         )
#         self.btn_insights = self.make_button(
#             "Insights", "assets/icons/ai_mode.svg", self.main.show_insights
#         )
#         self.btn_weekly_report = self.make_button(
#             "Weekly Report", "assets/icons/weekly_report.svg", self.main.show_weekly_report
#         )
#         self.btn_monthly_report = self.make_button(
#             "Monthly Report", "assets/icons/monthly_report.svg", self.main.show_monthly_report
#         )

#         layout.addWidget(self.btn_analytics)
#         layout.addWidget(self.btn_weekly)
#         layout.addWidget(self.btn_insights)
#         layout.addWidget(self.btn_weekly_report)
#         layout.addWidget(self.btn_monthly_report)

#         layout.addStretch()

#         # -------------------------
#         # SETTINGS BUTTON
#         # -------------------------
#         self.btn_settings = self.make_button(
#             "Settings", "assets/icons/settings.svg", self.main.show_settings
#         )
#         layout.addWidget(self.btn_settings)

#         # -------------------------
#         # STORE BUTTONS FOR ACTIVE/HOVER LOGIC
#         # -------------------------
#         self.buttons = [
#             self.btn_dashboard,
#             self.btn_smart,
#             self.btn_ai,
#             self.btn_analytics,
#             self.btn_weekly,
#             self.btn_insights,
#             self.btn_weekly_report,
#             self.btn_monthly_report,
#             self.btn_settings
#         ]

#         # Store full text for collapse mode
#         for btn in self.buttons:
#             btn.setProperty("full_text", btn.text())

#     # -------------------------------------------------------
#     # CREATE A NAVIGATION BUTTON
#     # -------------------------------------------------------
#     def make_button(self, text, icon_path, callback):
#         btn = QPushButton(text)
        
#         # FIXED: Every icon path now goes through resource_path
#         fixed_icon_path = resource_path(icon_path)
#         btn.setIcon(QIcon(fixed_icon_path))
        
#         btn.setIconSize(QSize(20, 20))
#         btn.setCursor(Qt.PointingHandCursor)
#         btn.setObjectName("SidebarButton")

#         # Hover glow
#         btn.setProperty("hover", False)
#         btn.enterEvent = lambda e, b=btn: self.on_hover(b, True)
#         btn.leaveEvent = lambda e, b=btn: self.on_hover(b, False)

#         # Active highlight
#         btn.clicked.connect(lambda: self.set_active(btn, callback))

#         return btn

#     # -------------------------------------------------------
#     # HOVER EFFECT
#     # -------------------------------------------------------
#     def on_hover(self, btn, state):
#         btn.setProperty("hover", state)
#         btn.style().unpolish(btn)
#         btn.style().polish(btn)

#     # -------------------------------------------------------
#     # SET ACTIVE BUTTON (ACCENT BAR)
#     # -------------------------------------------------------
#     def set_active(self, btn, callback):
#         for b in self.buttons:
#             b.setProperty("active", False)
#             b.style().unpolish(b)
#             b.style().polish(b)

#         btn.setProperty("active", True)
#         btn.style().unpolish(btn)
#         btn.style().polish(btn)

#         callback()

#     # -------------------------------------------------------
#     # ANIMATE SIDEBAR WIDTH
#     # -------------------------------------------------------
#     def animate_width(self, start, end, duration=250):
#         self.anim = QPropertyAnimation(self, b"minimumWidth")
#         self.anim.setDuration(duration)
#         self.anim.setStartValue(start)
#         self.anim.setEndValue(end)
#         self.anim.setEasingCurve(QEasingCurve.InOutCubic)
#         self.anim.start()

#     # -------------------------------------------------------
#     # COLLAPSE / EXPAND SIDEBAR
#     # -------------------------------------------------------
#     def toggle_sidebar(self):
#         target_width = self.collapsed_width if self.is_expanded else self.expanded_width
#         self.is_expanded = not self.is_expanded

#         # Animate width
#         self.animate_width(self.width(), target_width)

#         # Hide/show text on buttons
#         for btn in self.buttons:
#             full_text = btn.property("full_text")
#             btn.setText(full_text if self.is_expanded else "")

#     # -------------------------------------------------------
#     # MEETING MODE HIGHLIGHT
#     # -------------------------------------------------------
#     def set_meeting_mode(self, active: bool):
#         self.btn_smart.setProperty("meeting", active)
#         self.btn_ai.setProperty("meeting", active)

#         for btn in (self.btn_smart, self.btn_ai):
#             btn.style().unpolish(btn)
#             btn.style().polish(btn)









# Mac and windows

# 26th arch to use the resource qrc - Fixed for macOS Black Box 30th March
import os
import sys
from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon

# --- DYNAMIC PATH LOGIC (FIX FOR EXE) ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Sidebar(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        # Sidebar state
        self.expanded_width = 200
        self.collapsed_width = 56
        self.is_expanded = True

        self.setMinimumWidth(self.expanded_width)
        self.setObjectName("Sidebar")

        # -------------------------
        # MAIN LAYOUT
        # -------------------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # -------------------------
        # HAMBURGER BUTTON (Fixed for macOS Black Box)
        # -------------------------
        self.btn_toggle = QPushButton()
        hamb_icon = resource_path(os.path.join("assets", "icons", "hamburger.svg"))
        self.btn_toggle.setIcon(QIcon(hamb_icon))
        
        self.btn_toggle.setIconSize(QSize(20, 20))
        # Updated name to match the specific macOS QSS fix
        self.btn_toggle.setObjectName("MenuToggleButton") 
        
        # CRITICAL MAC FIX: Prevents the black focus square
        self.btn_toggle.setFocusPolicy(Qt.NoFocus) 
        
        self.btn_toggle.clicked.connect(self.toggle_sidebar)
        self.btn_toggle.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.btn_toggle)

        # -------------------------
        # NAVIGATION BUTTONS
        # -------------------------
        self.btn_dashboard = self.make_button(
            "Dashboard", "assets/icons/dashboard.svg", self.main.show_dashboard
        )
        self.btn_smart = self.make_button(
            "K‑Mends Mode", "assets/icons/smart_mode.svg", self.main.show_smart
        )
        # This calls main.show_ai(), which is now linked to self.ai_mode_page
        self.btn_ai = self.make_button(
            "K‑Mends AI", "assets/icons/ai_mode.svg", self.main.show_ai
        )

        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_smart)
        layout.addWidget(self.btn_ai)

        # -------------------------
        # ANALYTICS SECTION
        # -------------------------
        self.btn_analytics = self.make_button(
            "Analytics", "assets/icons/analytics.svg", self.main.show_analytics
        )
        self.btn_weekly = self.make_button(
            "Weekly Analytics", "assets/icons/weekly_report.svg", self.main.show_weekly
        )
        self.btn_insights = self.make_button(
            "Insights", "assets/icons/ai_mode.svg", self.main.show_insights
        )
        self.btn_weekly_report = self.make_button(
            "Weekly Report", "assets/icons/weekly_report.svg", self.main.show_weekly_report
        )
        self.btn_monthly_report = self.make_button(
            "Monthly Report", "assets/icons/monthly_report.svg", self.main.show_monthly_report
        )

        layout.addWidget(self.btn_analytics)
        layout.addWidget(self.btn_weekly)
        layout.addWidget(self.btn_insights)
        layout.addWidget(self.btn_weekly_report)
        layout.addWidget(self.btn_monthly_report)

        layout.addStretch()

        # -------------------------
        # SETTINGS BUTTON
        # -------------------------
        self.btn_settings = self.make_button(
            "Settings", "assets/icons/settings.svg", self.main.show_settings
        )
        layout.addWidget(self.btn_settings)

        # -------------------------
        # STORE BUTTONS FOR ACTIVE/HOVER LOGIC
        # -------------------------
        self.buttons = [
            self.btn_dashboard,
            self.btn_smart,
            self.btn_ai,
            self.btn_analytics,
            self.btn_weekly,
            self.btn_insights,
            self.btn_weekly_report,
            self.btn_monthly_report,
            self.btn_settings
        ]

        # Store full text for collapse mode
        for btn in self.buttons:
            btn.setProperty("full_text", btn.text())

    # -------------------------------------------------------
    # CREATE A NAVIGATION BUTTON
    # -------------------------------------------------------
    def make_button(self, text, icon_path, callback):
        btn = QPushButton(text)
        fixed_icon_path = resource_path(icon_path)
        btn.setIcon(QIcon(fixed_icon_path))
        
        btn.setIconSize(QSize(20, 20))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setObjectName("SidebarButton")
        
        # Extra safety for navigation buttons on macOS
        btn.setFocusPolicy(Qt.NoFocus)

        # Hover glow
        btn.setProperty("hover", False)
        btn.enterEvent = lambda e, b=btn: self.on_hover(b, True)
        btn.leaveEvent = lambda e, b=btn: self.on_hover(b, False)

        # Active highlight
        btn.clicked.connect(lambda: self.set_active(btn, callback))

        return btn

    # ... [Rest of the helper functions remain the same] ...
    def on_hover(self, btn, state):
        btn.setProperty("hover", state)
        btn.style().unpolish(btn)
        btn.style().polish(btn)

    def set_active(self, btn, callback):
        for b in self.buttons:
            b.setProperty("active", False)
            b.style().unpolish(b)
            b.style().polish(b)

        btn.setProperty("active", True)
        btn.style().unpolish(btn)
        btn.style().polish(btn)

        callback()

    def animate_width(self, start, end, duration=250):
        self.anim = QPropertyAnimation(self, b"minimumWidth")
        self.anim.setDuration(duration)
        self.anim.setStartValue(start)
        self.anim.setEndValue(end)
        self.anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.anim.start()

    def toggle_sidebar(self):
        target_width = self.collapsed_width if self.is_expanded else self.expanded_width
        self.is_expanded = not self.is_expanded
        self.animate_width(self.width(), target_width)
        for btn in self.buttons:
            full_text = btn.property("full_text")
            btn.setText(full_text if self.is_expanded else "")

    def set_meeting_mode(self, active: bool):
        self.btn_smart.setProperty("meeting", active)
        self.btn_ai.setProperty("meeting", active)
        for btn in (self.btn_smart, self.btn_ai):
            btn.style().unpolish(btn)
            btn.style().polish(btn)