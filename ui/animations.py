
# ui/animations.py

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QObject, Property, Qt
from PySide6.QtWidgets import QWidget
import pyqtgraph as pg


# ============================================================
# GLOBAL RENDERING IMPROVEMENTS (smooth lines everywhere)
# ============================================================
#pg.setConfigOptions(useOpenGL=True)
#pg.setConfigOptions(antialias=True)



class FadeInAnimator(QObject):
    def __init__(self, widget: QWidget, duration=450):
        super().__init__()
        self.widget = widget
        self.anim = QPropertyAnimation(widget, b"windowOpacity")
        self.anim.setDuration(duration)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)

    def start(self):
        self.anim.start()



class SlideInAnimator(QObject):
    def __init__(self, widget: QWidget, offset=20, duration=350):
        super().__init__()
        self.widget = widget
        self.offset = offset
        self.duration = duration

    def start(self):
        start_geo = self.widget.geometry()
        end_geo = self.widget.geometry()
        start_geo.setX(start_geo.x() - self.offset)

        anim = QPropertyAnimation(self.widget, b"geometry")
        anim.setDuration(self.duration)
        anim.setStartValue(start_geo)
        anim.setEndValue(end_geo)
        anim.setEasingCurve(QEasingCurve.InOutCubic)
        anim.start()



class ValueAnimator(QObject):
    def __init__(self, start_value, end_value, duration=500, callback=None):
        super().__init__()
        self._value = start_value
        self.callback = callback

        self.anim = QPropertyAnimation(self, b"value")
        self.anim.setDuration(duration)
        self.anim.setStartValue(start_value)
        self.anim.setEndValue(end_value)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.valueChanged.connect(self._on_value_changed)

    def _on_value_changed(self, val):
        if self.callback:
            self.callback(val)

    def start(self):
        self.anim.start()

    def get_value(self):
        return self._value

    def set_value(self, val):
        self._value = val

    value = Property(float, get_value, set_value)



class SparklineAnimator:
    """
    Smooth, anti-aliased sparkline animation.
    """
    def __init__(self, plot_widget: pg.PlotWidget, color: str, duration=600):
        self.plot_widget = plot_widget
        self.color = color
        self.duration = duration

        # Disable downsampling globally for this widget
        self.plot_widget.setDownsampling(mode=None)

    def animate(self, values):
        self.plot_widget.clear()
        if not values:
            return

        x = list(range(len(values)))
        y = [0] * len(values)

        # Smooth pen
        pen = pg.mkPen(color=self.color, width=2, cosmetic=True)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)

        curve = self.plot_widget.plot(
            x, y,
            pen=pen,
            antialias=True
        )

        def update_curve(val):
            idx = int(val)
            if 0 <= idx < len(values):
                y[idx] = values[idx]
                curve.setData(x, y)

        anim = ValueAnimator(0, len(values) - 1, duration=self.duration, callback=update_curve)
        anim.start()



class PulseAnimator(QObject):
    def __init__(self, widget: QWidget, min_opacity=0.6, max_opacity=1.0, duration=700):
        super().__init__()
        self.widget = widget
        self.anim = QPropertyAnimation(widget, b"windowOpacity")
        self.anim.setDuration(duration)
        self.anim.setStartValue(min_opacity)
        self.anim.setEndValue(max_opacity)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.setLoopCount(-1)

    def start(self):
        self.anim.start()

