# from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
# from PySide6.QtGui import QPainter, QColor, QLinearGradient
# from PySide6.QtCore import Qt, QRect


# class BottomBar(QWidget):
#     def __init__(self, theme, parent=None):
#         super().__init__(parent)
#         self.theme = theme
#         self.setFixedHeight(50)
#         self.setAutoFillBackground(False)

#         layout = QHBoxLayout(self)
#         layout.setContentsMargins(24, 0, 24, 0)
#         layout.setSpacing(0)

#         self.startStopButton = QPushButton("Start")
#         self.startStopButton.setObjectName("primaryButton")
#         layout.addWidget(self.startStopButton, alignment=Qt.AlignLeft)

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)

#         # FluentBlur background
#         blurColor = QColor(self.theme.panelColor)
#         blurColor.setAlphaF(self.theme.blurOpacity)
#         painter.fillRect(self.contentsRect(), blurColor)

#         # Gradient divider line
#         grad = QLinearGradient(0, 0, self.width(), 0)
#         lineColor = QColor(self.theme.dividerColor)
#         lineColor.setAlphaF(0.18)
#         grad.setColorAt(0.0, Qt.transparent)
#         grad.setColorAt(0.5, lineColor)
#         grad.setColorAt(1.0, Qt.transparent)
#         painter.fillRect(QRect(0, 0, self.width(), 1), grad)

#         # Soft shadow
#         shadowGrad = QLinearGradient(0, 1, 0, 12)
#         shadowColor = QColor(self.theme.shadowColor)
#         shadowColor.setAlphaF(0.22)
#         shadowGrad.setColorAt(0.0, shadowColor)
#         shadowGrad.setColorAt(1.0, Qt.transparent)
#         painter.fillRect(QRect(0, 1, self.width(), 12), shadowGrad)












from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtGui import QPainter, QColor, QLinearGradient
from PySide6.QtCore import Qt, QRect


class BottomBar(QWidget):
    def __init__(self, theme, parent=None):
        super().__init__(parent)
        self.theme = theme

        # Smaller, premium height
        self.setFixedHeight(40)
        self.setAutoFillBackground(False)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(0)

        # Real clickable button
        self.startStopButton = QPushButton("Start")
        self.startStopButton.setObjectName("primaryButton")
        layout.addWidget(self.startStopButton, alignment=Qt.AlignLeft)

        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Theme-aware tint (same blue as sidebar hover)
        tint = QColor(self.theme.accentColor)
        tint.setAlphaF(0.08)  # soft, premium tint

        # Paint only background behind widgets
        painter.fillRect(self.contentsRect(), tint)

        # Divider line
        grad = QLinearGradient(0, 0, self.width(), 0)
        lineColor = QColor(self.theme.accentColor)
        lineColor.setAlphaF(0.25)
        grad.setColorAt(0.0, Qt.transparent)
        grad.setColorAt(0.5, lineColor)
        grad.setColorAt(1.0, Qt.transparent)
        painter.fillRect(QRect(0, 0, self.width(), 1), grad)

        # Soft shadow
        shadowGrad = QLinearGradient(0, 1, 0, 10)
        shadowColor = QColor(self.theme.shadowColor)
        shadowColor.setAlphaF(0.15)
        shadowGrad.setColorAt(0.0, shadowColor)
        shadowGrad.setColorAt(1.0, Qt.transparent)
        painter.fillRect(QRect(0, 1, self.width(), 10), shadowGrad)
