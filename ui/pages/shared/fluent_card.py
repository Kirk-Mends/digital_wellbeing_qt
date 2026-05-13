# # ui/pages/shared/fluent_card.py

# from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
# import pyqtgraph as pg

# from ui.theme import AppMetrics, AppFonts


# class FluentCard(QFrame):
#     """
#     Universal Fluent card used by Smart Mode and AI Mode.
#     Automatically styled by QSS via:
#         #FluentCard
#         #CardTitle
#         #CardValue
#     """

#     def __init__(self, title, accent_color, value_font=None, has_spark=True):
#         super().__init__()

#         # QSS hook
#         self.setObjectName("FluentCard")

#         self.accent_color = accent_color
#         self.setMinimumHeight(AppMetrics.CARD_HEIGHT)

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(
#             AppMetrics.CARD_PADDING,
#             AppMetrics.CARD_PADDING,
#             AppMetrics.CARD_PADDING,
#             AppMetrics.CARD_PADDING,
#         )
#         layout.setSpacing(AppMetrics.GAP_SMALL)

#         # Accent bar
#         self.accent = QFrame()
#         self.accent.setFixedHeight(4)
#         self.accent.setStyleSheet(f"background-color: {accent_color}; border-radius: 2px;")
#         layout.addWidget(self.accent)

#         # Title
#         self.title_label = QLabel(title)
#         self.title_label.setObjectName("CardTitle")
#         self.title_label.setFont(AppFonts.card_title())
#         layout.addWidget(self.title_label)

#         # Value
#         self.value_label = QLabel("—")
#         self.value_label.setObjectName("CardValue")
#         self.value_label.setFont(value_font or AppFonts.primary_value())
#         self.value_label.setWordWrap(True)
#         self.value_label.setContentsMargins(0, 6, 0, 0)
#         layout.addWidget(self.value_label)

#         # Sparkline
#         self.spark = None
#         if has_spark:
#             self.spark = pg.PlotWidget()
#             self.spark.setFixedHeight(60)
#             self.spark.setBackground(None)
#             self.spark.hideAxis("left")
#             self.spark.hideAxis("bottom")
#             layout.addWidget(self.spark)

#         layout.addStretch()

#     def update_value(self, text):
#         self.value_label.setText(text)












# from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
# import pyqtgraph as pg

# from ui.core.theme import AppMetrics


# class FluentCard(QFrame):
#     """
#     Universal Fluent card used by Smart Mode and AI Mode.
#     Styled entirely by QSS via:
#         #FluentCard
#         #CardTitle
#         #CardValue
#     """

#     def __init__(self, title, accent_color, value_font=None, has_spark=True):
#         super().__init__()

#         # QSS hook
#         self.setObjectName("FluentCard")

#         # Ensure card height is never collapsed by QSS
#         self.setMinimumHeight(AppMetrics.CARD_HEIGHT)

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(
#             AppMetrics.CARD_PADDING,
#             AppMetrics.CARD_PADDING,
#             AppMetrics.CARD_PADDING,
#             AppMetrics.CARD_PADDING,
#         )
#         layout.setSpacing(AppMetrics.GAP_SMALL)

#         # Accent bar
#         self.accent = QFrame()
#         self.accent.setFixedHeight(4)
#         self.accent.setStyleSheet(f"background-color: {accent_color}; border-radius: 2px;")
#         layout.addWidget(self.accent)

#         # Title (QSS controls font)
#         self.title_label = QLabel(title)
#         self.title_label.setObjectName("CardTitle")
#         layout.addWidget(self.title_label)

#         # Value (QSS controls font)
#         self.value_label = QLabel("—")
#         self.value_label.setObjectName("CardValue")
#         self.value_label.setWordWrap(True)
#         self.value_label.setContentsMargins(0, 6, 0, 0)
#         layout.addWidget(self.value_label)

#         # Sparkline (protected height)
#         self.spark = None
#         if has_spark:
#             self.spark = pg.PlotWidget()
#             self.spark.setFixedHeight(60)  # prevents collapse
#             self.spark.setBackground(None)
#             self.spark.hideAxis("left")
#             self.spark.hideAxis("bottom")
#             layout.addWidget(self.spark)

#         layout.addStretch()

#     def update_value(self, text):
#         self.value_label.setText(text)





# from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QColor

# from pyqtgraph import PlotWidget  # PySide6-compatible

# from ui.core.theme import AppMetrics


# class FluentCard(QFrame):
#     def __init__(self, title, accent_color, value_font=None, has_spark=True):
#         super().__init__()

#         self.setObjectName("FluentCard")
#         self.setMinimumHeight(AppMetrics.CARD_HEIGHT)

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(
#             AppMetrics.CARD_PADDING,
#             AppMetrics.CARD_PADDING,
#             AppMetrics.CARD_PADDING,
#             AppMetrics.CARD_PADDING,
#         )
#         layout.setSpacing(AppMetrics.GAP_SMALL)

#         self.accent = QFrame()
#         self.accent.setFixedHeight(4)
#         self.accent.setStyleSheet(
#             f"background-color: {accent_color}; border-radius: 2px;"
#         )
#         layout.addWidget(self.accent)

#         self.title_label = QLabel(title)
#         self.title_label.setObjectName("CardTitle")
#         layout.addWidget(self.title_label)

#         self.value_label = QLabel("—")
#         self.value_label.setObjectName("CardValue")
#         self.value_label.setWordWrap(True)
#         self.value_label.setContentsMargins(0, 6, 0, 0)
#         layout.addWidget(self.value_label)

#         self.spark = None
#         if has_spark:
#             self.spark = PlotWidget()
#             self.spark.setFixedHeight(60)
#             self.spark.setBackground(None)
#             self.spark.hideAxis("left")
#             self.spark.hideAxis("bottom")
#             layout.addWidget(self.spark)

#         layout.addStretch()

#     def update_value(self, text):
#         self.value_label.setText(text)

















# from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QColor

# from pyqtgraph import PlotWidget  # PySide6-compatible

# from ui.core.theme import AppMetrics


# class FluentCard(QFrame):
#     def __init__(self, title, accent_color, value_font=None, has_spark=True):
#         super().__init__()

#         # --- CARD BASE ---
#         self.setObjectName("FluentCard")
#         self.setMinimumHeight(AppMetrics.CARD_HEIGHT)
#         self.setFocusPolicy(Qt.NoFocus)
#         self.setAttribute(Qt.WA_NoMousePropagation)

#         # --- LAYOUT ---
#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(
#             AppMetrics.CARD_PADDING,
#             AppMetrics.CARD_PADDING,
#             AppMetrics.CARD_PADDING,
#             AppMetrics.CARD_PADDING,
#         )
#         layout.setSpacing(AppMetrics.GAP_SMALL)

#         # --- ACCENT BAR ---
#         self.accent = QFrame()
#         self.accent.setFixedHeight(4)
#         self.accent.setStyleSheet(
#             f"background-color: {accent_color}; border-radius: 2px;"
#         )
#         layout.addWidget(self.accent)  # , alignment=Qt.AlignRight

#         # --- TITLE ---
#         self.title_label = QLabel(title)
#         self.title_label.setObjectName("CardTitle")
#         self.title_label.setMinimumHeight(20)
#         layout.addWidget(self.title_label)

#         # --- VALUE ---
#         self.value_label = QLabel("—")
#         self.value_label.setObjectName("CardValue")
#         self.value_label.setWordWrap(True)
#         self.value_label.setContentsMargins(0, 6, 0, 0)
#         self.value_label.setMinimumHeight(22)
#         layout.addWidget(self.value_label)

#         # --- SPARKLINE ---
#         self.spark = None
#         if has_spark:
#             self.spark = PlotWidget()
#             self.spark.setFixedHeight(60)
#             self.spark.setBackground(None)
#             self.spark.hideAxis("left")
#             self.spark.hideAxis("bottom")

#             # Disable all mouse interaction (fixes shrinking + “A” glyph)
#             self.spark.setMouseEnabled(x=False, y=False)
#             self.spark.setMenuEnabled(False)

#             vb = self.spark.getViewBox()
#             vb.setMouseEnabled(x=False, y=False)
#             vb.setMenuEnabled(False)
#             vb.setLimits(minXRange=1, minYRange=1)

#             layout.addWidget(self.spark)

#         layout.addStretch()

#     # --- BLOCK WHEEL EVENTS COMPLETELY ---
#     def wheelEvent(self, event):
#         event.ignore()

#     # --- UPDATE VALUE ---
#     def update_value(self, text):
#         self.value_label.setText(text)










from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from pyqtgraph import PlotWidget

from ui.core.theme import AppMetrics


class FluentCard(QFrame):
    """
    Premium Fluent-style card:
      - Fluent SVG icon (razor sharp)
      - Title
      - Value
      - Optional sparkline
      - Accent bar
      - No info icon
    """

    def __init__(self, title, accent_color="#4A90E2",
                 value_font=None, has_spark=True, icon_path=None):
        super().__init__()

        # --- CARD BASE ---
        self.setObjectName("FluentCard")
        self.setMinimumHeight(AppMetrics.CARD_HEIGHT)
        self.setFocusPolicy(Qt.NoFocus)
        self.setAttribute(Qt.WA_NoMousePropagation)

        # --- LAYOUT ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            AppMetrics.CARD_PADDING,
            AppMetrics.CARD_PADDING,
            AppMetrics.CARD_PADDING,
            AppMetrics.CARD_PADDING,
        )
        layout.setSpacing(AppMetrics.GAP_SMALL)

        # --- ACCENT BAR ---
        self.accent = QFrame()
        self.accent.setFixedHeight(4)
        self.accent.setStyleSheet(
            f"background-color: {accent_color}; border-radius: 2px;"
        )
        layout.addWidget(self.accent)

        # ============================================================
        # HEADER ROW (Fluent SVG Icon + Title)
        # ============================================================
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(6)

        # --- LEFT ICON (Fluent SVG, razor sharp) ---
        if icon_path:
            self.left_icon = QSvgWidget(icon_path)
            self.left_icon.setFixedSize(20, 20)  # Fluent UI native size
            header.addWidget(self.left_icon)
        else:
            self.left_icon = None

        # --- TITLE ---
        self.title_label = QLabel(title)
        self.title_label.setObjectName("CardTitle")
        header.addWidget(self.title_label)

        header.addStretch()
        layout.addLayout(header)

        # ============================================================
        # VALUE LABEL
        # ============================================================
        self.value_label = QLabel("—")
        self.value_label.setObjectName("CardValue")
        self.value_label.setWordWrap(True)
        self.value_label.setContentsMargins(0, 6, 0, 0)
        layout.addWidget(self.value_label)

        # ============================================================
        # SPARKLINE (optional)
        # ============================================================
        self.spark = None
        if has_spark:
            self.spark = PlotWidget()
            self.spark.setFixedHeight(60)
            self.spark.setBackground(None)
            self.spark.hideAxis("left")
            self.spark.hideAxis("bottom")

            # Disable all mouse interaction
            self.spark.setMouseEnabled(x=False, y=False)
            self.spark.setMenuEnabled(False)

            vb = self.spark.getViewBox()
            vb.setMouseEnabled(x=False, y=False)
            vb.setMenuEnabled(False)
            vb.setLimits(minXRange=1, minYRange=1)

            layout.addWidget(self.spark)

        layout.addStretch()

    # --- BLOCK WHEEL EVENTS ---
    def wheelEvent(self, event):
        event.ignore()

    # --- UPDATE VALUE ---
    def update_value(self, text):
        self.value_label.setText(text)
