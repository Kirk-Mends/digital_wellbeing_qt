# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
# from PySide6.QtCore import Qt

# from core.weekly_summary_engine import WeeklySummaryEngine
# from core.weekly_report_generator import WeeklyReportGenerator


# class WeeklyReportPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("WeeklyReportPage")

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 20, 20, 20)
#         layout.setSpacing(20)
        

#         title = QLabel("Weekly Summary Report")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # Card container
#         self.card = QFrame()
#         self.card.setObjectName("ReportCard")

#         card_layout = QVBoxLayout(self.card)
#         card_layout.setContentsMargins(16, 16, 16, 16)

#         self.text_label = QLabel()
#         self.text_label.setObjectName("ReportText")
#         self.text_label.setWordWrap(True)

#         card_layout.addWidget(self.text_label)
#         layout.addWidget(self.card)

#         # Generate report
#         self.refresh()

#     def refresh(self):
#         from core.weekly_summary_engine import WeeklySummaryEngine
#         from core.weekly_report_generator import WeeklyReportGenerator

#         engine = WeeklySummaryEngine()
#         summary = engine.generate_last_week()

#         generator = WeeklyReportGenerator()
#         report = generator.generate(summary)

#         self.text_label.setText(report)















# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
# from PySide6.QtCore import Qt

# from core.weekly_summary_engine import WeeklySummaryEngine
# from core.weekly_report_generator import WeeklyReportGenerator


# class WeeklyReportPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("WeeklyReportPage")

#         # MAIN LAYOUT
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(20, 24, 20, 20)   # premium top spacing
#         layout.setSpacing(20)
#         layout.setAlignment(Qt.AlignTop)

#         # TITLE
#         title = QLabel("Weekly Summary Report")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # CARD CONTAINER
#         self.card = QFrame()
#         self.card.setObjectName("ReportCard")

#         card_layout = QVBoxLayout(self.card)
#         card_layout.setContentsMargins(16, 16, 16, 16)

#         # REPORT TEXT LABEL
#         self.text_label = QLabel()
#         self.text_label.setObjectName("ReportText")
#         self.text_label.setWordWrap(True)
#         self.text_label.setTextFormat(Qt.RichText)   # allow HTML formatting

#         card_layout.addWidget(self.text_label)
#         layout.addWidget(self.card)

#         # Generate report
#         self.refresh()

#     def refresh(self):
#         engine = WeeklySummaryEngine()
#         summary = engine.generate_last_week()

#         generator = WeeklyReportGenerator()
#         report = generator.generate(summary)

#         self.text_label.setText(report)






































































# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
# from PySide6.QtCore import Qt

# from core.weekly_summary_engine import WeeklySummaryEngine
# from core.weekly_report_generator import WeeklyReportGenerator


# class WeeklyReportPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("WeeklyReportPage")

#         # MAIN LAYOUT
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(20)
#         layout.setAlignment(Qt.AlignTop)

#         # TITLE
#         title = QLabel("Weekly Summary Report")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # CARD CONTAINER
#         self.card = QFrame()
#         self.card.setObjectName("ReportCard")

#         card_layout = QVBoxLayout(self.card)
#         card_layout.setContentsMargins(30, 30, 30, 30)

#         # REPORT TEXT LABEL
#         self.text_label = QLabel()
#         self.text_label.setObjectName("ReportText")
#         self.text_label.setWordWrap(True)
#         self.text_label.setTextFormat(Qt.RichText)

#         card_layout.addWidget(self.text_label)
#         layout.addWidget(self.card)

#         self.refresh()

#     def refresh(self):
#         # --- THE FIX: THEME DETECTION ---
#         # Detect if the current window background is dark
#         bg_color = self.palette().window().color().name().upper()
#         is_dark = bg_color in ["#161618", "#000000"]
        
#         # Define colors based on theme
#         text_color = "#E4E7F2" if is_dark else "#1A1A1A"
#         accent_color = "#4DA3FF" if is_dark else "#0057D9"
        
#         engine = WeeklySummaryEngine()
#         summary = engine.generate_last_week()

#         generator = WeeklyReportGenerator()
#         # Pass the theme state to the generator
#         report = generator.generate(summary, is_dark_mode=is_dark)

#         # Inject a CSS block to control the classes used in the generator
#         styled_report = f"""
#         <style>
#             .accent-text {{ color: {accent_color}; }}
#             .stats-box {{ border-color: {accent_color}44; color: {text_color}; }}
#             h2, h3, b {{ color: {text_color}; }}
#         </style>
#         <div style="color: {text_color};">
#             {report}
#         </div>
#         """
#         self.text_label.setText(styled_report)


















# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
# from PySide6.QtCore import Qt
# from core.weekly_summary_engine import WeeklySummaryEngine
# from core.weekly_report_generator import WeeklyReportGenerator

# class WeeklyReportPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("WeeklyReportPage")

#         layout = QVBoxLayout(self)
#         # Increased left margin (60) to provide a "Premium" gutter from the sidebar
#         layout.setContentsMargins(60, 40, 40, 40) 
#         layout.setSpacing(0)
#         layout.setAlignment(Qt.AlignTop)

#         self.card = QFrame()
#         self.card.setObjectName("ReportCard")
#         # No internal margins here; the HTML will handle spacing
#         card_layout = QVBoxLayout(self.card)
#         card_layout.setContentsMargins(0, 0, 0, 0)

#         self.text_label = QLabel()
#         self.text_label.setWordWrap(True)
#         self.text_label.setTextFormat(Qt.RichText)

#         card_layout.addWidget(self.text_label)
#         layout.addWidget(self.card)
#         self.refresh()

#     def refresh(self):
#         bg_color = self.palette().window().color().name().upper()
#         is_dark = bg_color in ["#161618", "#000000"]
        
#         # Match the background to the sidebar for a "seamless" look
#         page_bg = "#161618" if is_dark else "#FFFFFF"
#         self.setStyleSheet(f"#WeeklyReportPage {{ background-color: {page_bg}; }} #ReportCard {{ background: transparent; border: none; }}")

#         summary = WeeklySummaryEngine().generate_last_week()
#         report_html = WeeklyReportGenerator().generate(summary, is_dark_mode=is_dark)
#         self.text_label.setText(report_html)
















# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
# from PySide6.QtCore import Qt
# from core.weekly_summary_engine import WeeklySummaryEngine
# from core.weekly_report_generator import WeeklyReportGenerator

# class WeeklyReportPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("WeeklyReportPage")

#         # MAIN LAYOUT
#         layout = QVBoxLayout(self)
#         # 60px left margin creates the "Premium Gutter"
#         layout.setContentsMargins(60, 40, 40, 40) 
#         layout.setSpacing(0)
#         layout.setAlignment(Qt.AlignTop)

#         # PAGE TITLE - Restored and Styled for Premium Feel
#         self.title_lbl = QLabel("Weekly Report")
#         self.title_lbl.setObjectName("PageTitle")
#         layout.addWidget(self.title_lbl)

#         # CONTENT CONTAINER
#         self.card = QFrame()
#         self.card.setObjectName("ReportCard")
#         card_layout = QVBoxLayout(self.card)
#         card_layout.setContentsMargins(0, 0, 0, 0)

#         self.text_label = QLabel()
#         self.text_label.setObjectName("ReportText")
#         self.text_label.setWordWrap(True)
#         self.text_label.setTextFormat(Qt.RichText)

#         card_layout.addWidget(self.text_label)
#         layout.addWidget(self.card)
        
#         self.refresh()

#     def refresh(self):
#         # Detect Theme
#         bg_color = self.palette().window().color().name().upper()
#         is_dark = bg_color in ["#161618", "#000000"]
        
#         # Define dynamic colors
#         page_bg = "#161618" if is_dark else "#FFFFFF"
#         text_primary = "#E4E7F2" if is_dark else "#1A1A1A"
        
#         # Apply Stylesheet
#         self.setStyleSheet(f"""
#             #WeeklyReportPage {{ background-color: {page_bg}; }}
#             #ReportCard {{ background: transparent; border: none; }}
#             #PageTitle {{ color: {text_primary}; }}
#             #ReportText {{ color: {text_primary}; }}
#         """)

#         # Fetch and Generate Report
#         engine = WeeklySummaryEngine()
#         summary = engine.generate_last_week()
        
#         generator = WeeklyReportGenerator()
#         report_html = generator.generate(summary, is_dark_mode=is_dark)
        
#         self.text_label.setText(report_html)











# # THIS IS PERFECT 

# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
# from PySide6.QtCore import Qt
# from core.weekly_summary_engine import WeeklySummaryEngine
# from core.weekly_report_generator import WeeklyReportGenerator

# class WeeklyReportPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("WeeklyReportPage")

#         # 1. MATCH THE MAIN MARGINS AND SPACING (30, 30, 30, 30)
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(25) 
#         layout.setAlignment(Qt.AlignTop)

#         # --- HEADER (Matches the 'track' of WeeklyAnalyticsPage) ---
#         header = QHBoxLayout()
        
#         # MAIN TITLE - Uses your existing QSS (#PageTitle)
#         self.title_lbl = QLabel("Weekly Summary Report")
#         self.title_lbl.setObjectName("PageTitle")
        
#         header.addWidget(self.title_lbl)
#         header.addStretch() # This ensures the horizontal alignment matches other pages
#         layout.addLayout(header)

#         # --- CONTENT SECTION ---
#         self.card = QFrame()
#         self.card.setObjectName("ReportCard")
#         # Keep background transparent for the "Premium" look
#         self.card.setStyleSheet("background: transparent; border: none;")
        
#         card_layout = QVBoxLayout(self.card)
#         card_layout.setContentsMargins(0, 0, 0, 0)

#         self.text_label = QLabel()
#         self.text_label.setObjectName("ReportText")
#         self.text_label.setWordWrap(True)
#         self.text_label.setTextFormat(Qt.RichText)

#         card_layout.addWidget(self.text_label)
#         layout.addWidget(self.card)
        
#         self.refresh()

#     def refresh(self):
#         # THEME DETECTION
#         current_bg = self.palette().window().color().name().upper()
#         is_dark = current_bg == "#161618"
        
#         page_bg = "#161618" if is_dark else "#FFFFFF"
#         text_primary = "#E4E7F2" if is_dark else "#1A1A1A"
        
#         # Apply theme colors
#         self.setStyleSheet(f"""
#             #WeeklyReportPage {{ background-color: {page_bg}; }}
#             #PageTitle {{ color: {text_primary}; }}
#             #ReportText {{ color: {text_primary}; }}
#         """)

#         # Fetch and Generate
#         engine = WeeklySummaryEngine()
#         summary = engine.generate_last_week()
        
#         generator = WeeklyReportGenerator()
#         report_html = generator.generate(summary, is_dark_mode=is_dark)
        
#         self.text_label.setText(report_html)










# # mADE IT SHIFT TO RIGHT A BIT
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
# from PySide6.QtCore import Qt
# from core.weekly_summary_engine import WeeklySummaryEngine
# from core.weekly_report_generator import WeeklyReportGenerator

# class WeeklyReportPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("WeeklyReportPage")

#         # 1. MAIN OUTER LAYOUT
#         # Margins (30, 30, 30, 30) keep the TITLE anchored to the same spot as Analytics
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(0) 
#         layout.setAlignment(Qt.AlignTop)

#         # --- HEADER (Anchored at 30px left) ---
#         header = QHBoxLayout()
#         self.title_lbl = QLabel("Weekly Summary Report")
#         self.title_lbl.setObjectName("PageTitle")
#         header.addWidget(self.title_lbl)
#         header.addStretch()
#         layout.addLayout(header)

#         # 2. SPACER BETWEEN TITLE AND CONTENT
#         layout.addSpacing(25) # Matches the layout spacing of the Analytics page

#         # --- THE SHIFTED CONTENT SECTION ---
#         self.card = QFrame()
#         self.card.setObjectName("ReportCard")
#         self.card.setStyleSheet("background: transparent; border: none;")
        
#         card_layout = QVBoxLayout(self.card)
#         # 3. ADDING THE SHIFT: 
#         # We add 15px-20px of extra left margin to the card so the data
#         # aligns with the "Daily Average" cards in the Analytics page.
#         card_layout.setContentsMargins(15, 0, 0, 0) 
#         card_layout.setSpacing(0)

#         self.text_label = QLabel()
#         self.text_label.setObjectName("ReportText")
#         self.text_label.setWordWrap(True)
#         self.text_label.setTextFormat(Qt.RichText)

#         card_layout.addWidget(self.text_label)
#         layout.addWidget(self.card)
        
#         self.refresh()

#     def refresh(self):
#         current_bg = self.palette().window().color().name().upper()
#         is_dark = current_bg == "#161618"
        
#         page_bg = "#161618" if is_dark else "#FFFFFF"
#         text_primary = "#E4E7F2" if is_dark else "#1A1A1A"
        
#         self.setStyleSheet(f"""
#             #WeeklyReportPage {{ background-color: {page_bg}; }}
#             #PageTitle {{ color: {text_primary}; }}
#             #ReportText {{ color: {text_primary}; }}
#         """)

#         engine = WeeklySummaryEngine()
#         summary = engine.generate_last_week()
        
#         generator = WeeklyReportGenerator()
#         report_html = generator.generate(summary, is_dark_mode=is_dark)
        
#         self.text_label.setText(report_html)









# # MADE IT SHIFT TO RIGHT A BIT
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
# from PySide6.QtCore import Qt
# from core.weekly_summary_engine import WeeklySummaryEngine
# from core.weekly_report_generator import WeeklyReportGenerator

# class WeeklyReportPage(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setObjectName("WeeklyReportPage")

#         # 1. MAIN OUTER LAYOUT
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(0) 
#         layout.setAlignment(Qt.AlignTop)

#         # --- HEADER ---
#         header = QHBoxLayout()
#         self.title_lbl = QLabel("Weekly Summary Report")
#         self.title_lbl.setObjectName("PageTitle") # External QSS will now control this
#         header.addWidget(self.title_lbl)
#         header.addStretch()
#         layout.addLayout(header)

#         layout.addSpacing(25) 

#         # --- THE SHIFTED CONTENT SECTION ---
#         self.card = QFrame()
#         self.card.setObjectName("ReportCard")
#         self.card.setStyleSheet("background: transparent; border: none;")
        
#         card_layout = QVBoxLayout(self.card)
#         card_layout.setContentsMargins(15, 0, 0, 0) 
#         card_layout.setSpacing(0)

#         self.text_label = QLabel()
#         self.text_label.setObjectName("ReportText")
#         self.text_label.setWordWrap(True)
#         self.text_label.setTextFormat(Qt.RichText)

#         card_layout.addWidget(self.text_label)
#         layout.addWidget(self.card)
        
#         self.refresh()

#     def refresh(self):
#         current_bg = self.palette().window().color().name().upper()
#         is_dark = current_bg == "#161618"
        
#         page_bg = "#161618" if is_dark else "#FFFFFF"
#         text_primary = "#E4E7F2" if is_dark else "#1A1A1A"
        
#         # --- THE FIX: Removed #PageTitle from this block ---
#         # This allows the external .qss file to set the color for #PageTitle
#         self.setStyleSheet(f"""
#             #WeeklyReportPage {{ background-color: {page_bg}; }}
#             #ReportText {{ color: {text_primary}; }}
#         """)

#         engine = WeeklySummaryEngine()
#         summary = engine.generate_last_week()
        
#         generator = WeeklyReportGenerator()
#         report_html = generator.generate(summary, is_dark_mode=is_dark)
        
#         self.text_label.setText(report_html)




# Changing the color for the titles



# MADE IT SHIFT TO RIGHT A BIT
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PySide6.QtCore import Qt
from core.weekly_summary_engine import WeeklySummaryEngine
from core.weekly_report_generator import WeeklyReportGenerator

class WeeklyReportPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("WeeklyReportPage")

        # 1. MAIN OUTER LAYOUT
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(0) 
        layout.setAlignment(Qt.AlignTop)

        # --- HEADER ---
        header = QHBoxLayout()
        self.title_lbl = QLabel("Weekly Summary Report")
        self.title_lbl.setObjectName("PageTitle") # External QSS will now control this
        header.addWidget(self.title_lbl)
        header.addStretch()
        layout.addLayout(header)

        layout.addSpacing(25) 

        # --- THE SHIFTED CONTENT SECTION ---
        self.card = QFrame()
        self.card.setObjectName("ReportCard")
        self.card.setStyleSheet("background: transparent; border: none;")
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(15, 0, 0, 0) 
        card_layout.setSpacing(0)

        self.text_label = QLabel()
        self.text_label.setObjectName("ReportText")
        self.text_label.setWordWrap(True)
        self.text_label.setTextFormat(Qt.RichText)

        card_layout.addWidget(self.text_label)
        layout.addWidget(self.card)
        
        self.refresh()

    def refresh(self):
        current_bg = self.palette().window().color().name().upper()
        is_dark = current_bg == "#161618"
        
        # 1. Grab the ACTUAL color of the title label as defined by QSS
        qss_title_color = self.title_lbl.palette().color(self.title_lbl.foregroundRole()).name()

        # 2. Update the page-wide styles
        page_bg = "#161618" if is_dark else "#FFFFFF"
        text_primary = "#E4E7F2" if is_dark else "#1A1A1A"
        
        self.setStyleSheet(f"""
            #WeeklyReportPage {{ background-color: {page_bg}; }}
            #ReportText {{ color: {text_primary}; }}
        """)

        engine = WeeklySummaryEngine()
        summary = engine.generate_last_week()
        
        generator = WeeklyReportGenerator()
        # 3. Pass the QSS color into the generator
        report_html = generator.generate(
            summary, 
            title_color=qss_title_color, 
            is_dark_mode=is_dark
        )
        
        self.text_label.setText(report_html)