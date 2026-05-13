





from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PySide6.QtCore import Qt
from core.monthly_summary_engine import MonthlySummaryEngine
from core.monthly_report_generator import MonthlyReportGenerator

class MonthlyReportPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MonthlyReportPage")

        # 1. MAIN OUTER LAYOUT
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(0) 
        layout.setAlignment(Qt.AlignTop)

        # --- HEADER ---
        header = QHBoxLayout()
        self.title_lbl = QLabel("Monthly Summary Report")
        self.title_lbl.setObjectName("PageTitle") 
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
        # Theme Detection
        current_bg = self.palette().window().color().name().upper()
        is_dark = current_bg == "#161618"
        
        # --- THE LINK TO QSS ---
        # We grab the color assigned to the PageTitle by the QSS file
        qss_title_color = self.title_lbl.palette().color(self.title_lbl.foregroundRole()).name()
        
        page_bg = "#161618" if is_dark else "#FFFFFF"
        text_primary = "#E4E7F2" if is_dark else "#1A1A1A"
        
        self.setStyleSheet(f"""
            #MonthlyReportPage {{ background-color: {page_bg}; }}
            #ReportText {{ color: {text_primary}; }}
        """)

        engine = MonthlySummaryEngine()
        this_month = engine.generate_this_month()
        last_month = engine.generate_last_month()

        generator = MonthlyReportGenerator()
        # --- THE FIX ---
        # We pass title_color to the generator so t_primary can use it
        report = generator.generate(
            this_month, 
            last_month, 
            is_dark_mode=is_dark,
            title_color=qss_title_color
        )

        self.text_label.setText(report)