# from PySide6.QtWidgets import QLabel
# from PySide6.QtCore import Qt, QPropertyAnimation, QByteArray
# from PySide6.QtGui import QColor

# class MeetingBadge(QLabel):
#     def __init__(self):
#         super().__init__("🟣 In a meeting")
#         self.setObjectName("MeetingBadge")
#         self.setVisible(False)

#         # Fade animation
#         self.anim = QPropertyAnimation(self, b"windowOpacity")
#         self.anim.setDuration(250)

#     def show_badge(self):
#         self.setVisible(True)
#         self.anim.stop()
#         self.anim.setStartValue(0.0)
#         self.anim.setEndValue(1.0)
#         self.anim.start()

#     def hide_badge(self):
#         self.anim.stop()
#         self.anim.setStartValue(1.0)
#         self.anim.setEndValue(0.0)
#         self.anim.start()
#         self.anim.finished.connect(lambda: self.setVisible(False))













# 26th 
from PySide6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QPropertyAnimation

class MeetingBadge(QLabel):
    def __init__(self):
        super().__init__("In a meeting")
        self.setObjectName("MeetingBadge")
        
        # 1. Premium Styling (Pill shape)
        self.setStyleSheet("""
            #MeetingBadge {
                background-color: rgba(145, 71, 255, 0.2); /* Soft Purple */
                color: #BF94FF; 
                border: 1px solid rgba(145, 71, 255, 0.5);
                border-radius: 10px;
                padding: 2px 8px;
                font-weight: bold;
                font-size: 11px;
            }
        """)
        
        # 2. Setup Opacity Effect (The right way to fade child widgets)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)
        self.hide()

        # 3. Fade Animation
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(300)

    def show_badge(self):
        self.show()
        self.anim.stop()
        self.anim.setDirection(QPropertyAnimation.Forward)
        self.anim.setStartValue(self.opacity_effect.opacity())
        self.anim.setEndValue(1.0)
        self.anim.start()

    def hide_badge(self):
        self.anim.stop()
        self.anim.setDirection(QPropertyAnimation.Backward)
        self.anim.setStartValue(self.opacity_effect.opacity())
        self.anim.setEndValue(0.0)
        self.anim.finished.connect(self.hide)
        self.anim.start()