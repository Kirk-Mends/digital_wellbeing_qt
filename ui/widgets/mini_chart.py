





# # ui/widgets/mini_chart.py

# import pyqtgraph as pg
# from PySide6.QtWidgets import QWidget, QVBoxLayout
# from PySide6.QtCore import QTimer, QEasingCurve, Qt, QObject, QEvent


# class MiniChart(QWidget):
#     """
#     Premium mini sparkline chart with:
#       - smooth anti-aliased line
#       - soft glow
#       - gradient fill
#       - easing animation for single-point updates
#       - instant redraw for batch updates (daily trend)
#       - no axes or borders
#       - wheel/zoom disabled to prevent shrinking + 'A' artifacts
#     """

#     def __init__(self, color="#4A90E2"):
#         super().__init__()

#         self.data = []
#         self.max_points = 40
#         self.color = color

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(0, 0, 0, 0)

#         # Create plot
#         self.plot = pg.PlotWidget()
#         self.plot.setBackground(None)
#         self.plot.setFixedHeight(70)

#         # Remove axes
#         self.plot.hideAxis("left")
#         self.plot.hideAxis("bottom")

#         # Disable downsampling for smoothness
#         self.plot.setDownsampling(mode=None)

#         # Disable menu + mouse interaction on the viewbox
#         self.plot.setMenuEnabled(False)

#         vb = self.plot.getPlotItem().getViewBox()
#         vb.setMouseEnabled(x=False, y=False)
#         vb.setMenuEnabled(False)
#         vb.setLimits(minXRange=1, minYRange=1)

#         # Swallow wheel events
#         self.plot.setFocusPolicy(Qt.NoFocus)
#         self.plot.setAttribute(Qt.WA_NoMousePropagation)
#         self.plot.installEventFilter(self)

#         # Smooth premium pen
#         pen = pg.mkPen(color, width=2, cosmetic=True)
#         pen.setCapStyle(Qt.RoundCap)
#         pen.setJoinStyle(Qt.RoundJoin)

#         self.curve = self.plot.plot([], pen=pen, antialias=True)

#         # Glow effect
#         glow_pen = pg.mkPen(color, width=8, cosmetic=True)
#         glow_pen.setColor(pg.mkColor(color).lighter(150))
#         glow_pen.setCapStyle(Qt.RoundCap)
#         glow_pen.setJoinStyle(Qt.RoundJoin)

#         self.glow = self.plot.plot([], pen=glow_pen, antialias=True)

#         # Gradient fill under line
#         self.fill_bottom = pg.PlotCurveItem([], pen=None)
#         self.fill = pg.FillBetweenItem(
#             self.curve,
#             self.fill_bottom,
#             brush=pg.mkBrush(pg.mkColor(color).lighter(180))
#         )
#         self.plot.addItem(self.fill)

#         layout.addWidget(self.plot)

#         # Animation timer
#         self.anim_timer = QTimer()
#         self.anim_timer.setInterval(16)  # ~60 FPS
#         self.anim_timer.timeout.connect(self.animate_step)

#         self.anim_progress = 0
#         self.anim_start = []
#         self.anim_end = []

#     # Swallow wheel events so zoom never triggers
#     def eventFilter(self, obj: QObject, event: QEvent) -> bool:
#         if obj is self.plot and event.type() == QEvent.Wheel:
#             return True
#         return super().eventFilter(obj, event)

#     def wheelEvent(self, event):
#         event.ignore()

#     # ---------------------------------------------------------
#     # Add a new point with animation (real-time mode)
#     # ---------------------------------------------------------
#     def add_point(self, value):
#         try:
#             value = float(value)
#         except Exception:
#             return

#         self.data.append(value)
#         if len(self.data) > self.max_points:
#             self.data.pop(0)

#         ydata = self.curve.getData()[1]
#         self.anim_start = ydata.tolist() if ydata is not None else []
#         self.anim_end = self.data.copy()
#         self.anim_progress = 0

#         self.anim_timer.start()

#     # ---------------------------------------------------------
#     # NEW: Set full dataset instantly (daily trend mode)
#     # ---------------------------------------------------------
#     def set_points(self, points):
#         """
#         Replace the entire dataset and redraw instantly.
#         Used for daily fatigue trend (batch updates).
#         """
#         try:
#             self.data = [float(v) for v in points]
#         except Exception:
#             return

#         x = list(range(len(self.data)))
#         self.curve.setData(x, self.data)
#         self.glow.setData(x, self.data)
#         self.fill_bottom.setData(x, [0] * len(self.data))

#     # ---------------------------------------------------------
#     # Animation step for add_point()
#     # ---------------------------------------------------------
#     def animate_step(self):
#         if not self.anim_start:
#             self.anim_start = [0] * len(self.anim_end)

#         self.anim_progress += 0.08
#         if self.anim_progress >= 1:
#             self.anim_progress = 1
#             self.anim_timer.stop()

#         easing = QEasingCurve(QEasingCurve.OutCubic)
#         eased = easing.valueForProgress(self.anim_progress)

#         interp = []
#         for i in range(len(self.anim_end)):
#             start = self.anim_start[i] if i < len(self.anim_start) else self.anim_end[i]
#             end = self.anim_end[i]
#             interp.append(start + (end - start) * eased)

#         x = list(range(len(interp)))
#         self.curve.setData(x, interp)
#         self.glow.setData(x, interp)
#         self.fill_bottom.setData(x, [0] * len(interp))














import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QTimer, QEasingCurve, Qt, QObject, QEvent
from PySide6.QtGui import QColor, QGradient, QLinearGradient

class MiniChart(QWidget):
    """
    Premium mini sparkline chart:
    - Explicitly hides 'A' button and context menus.
    - Smooth anti-aliased lines with rounded caps.
    - Linear gradient fill for a modern dashboard look.
    - 60FPS easing animations for point updates.
    """

    def __init__(self, color="#0A84FF"): # Default to Apple Blue
        super().__init__()

        self.data = []
        self.max_points = 40
        self.color = color

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 0) # Top margin for breathing room

        # --- PLOT CONFIG ---
        self.plot = pg.PlotWidget()
        self.plot.setBackground(None)
        self.plot.setFixedHeight(80) # Increased slightly for better visibility
        self.plot.setAntialiasing(True)

        # 1. THE "A" BUTTON KILLER (Crucial)
        self.plot_item = self.plot.getPlotItem()
        self.plot_item.setMenuEnabled(False)  # Disables right-click menu
        self.plot_item.hideButtons()          # DISABLES THE 'A' BUTTON PERMANENTLY
        
        # Remove axes
        self.plot.hideAxis("left")
        self.plot.hideAxis("bottom")

        # ViewBox Interaction Lock
        vb = self.plot_item.getViewBox()
        vb.setMouseEnabled(x=False, y=False)
        vb.setMenuEnabled(False)
        vb.setLimits(minXRange=1, minYRange=1)
        
        # 2. PREMIUM PEN STYLING
        # Using a slightly thicker line (2.5) with RoundCaps for a 'soft' look
        self.pen = pg.mkPen(color=self.color, width=2.5, antialias=True)
        self.pen.setCapStyle(Qt.RoundCap)
        self.pen.setJoinStyle(Qt.RoundJoin)

        self.curve = self.plot.plot([], pen=self.pen, antialias=True)

        # 3. GLOW EFFECT (Subtle bloom)
        glow_color = QColor(self.color)
        glow_color.setAlpha(50) # Very transparent
        self.glow_pen = pg.mkPen(color=glow_color, width=6, antialias=True)
        self.glow_pen.setCapStyle(Qt.RoundCap)
        self.glow = self.plot.plot([], pen=self.glow_pen, antialias=True)

        # 4. PREMIUM GRADIENT FILL
        # Creates a fade from the line color to transparent at the bottom
        fill_color = QColor(self.color)
        fill_color.setAlpha(40)
        
        self.fill_bottom = pg.PlotCurveItem([], pen=None)
        self.fill = pg.FillBetweenItem(
            self.curve,
            self.fill_bottom,
            brush=pg.mkBrush(fill_color)
        )
        self.plot.addItem(self.fill)

        # Interaction settings
        self.plot.setFocusPolicy(Qt.NoFocus)
        self.plot.setAttribute(Qt.WA_NoMousePropagation)
        self.plot.installEventFilter(self)

        layout.addWidget(self.plot)

        # Animation state
        self.anim_timer = QTimer()
        self.anim_timer.setInterval(16) 
        self.anim_timer.timeout.connect(self.animate_step)
        self.anim_progress = 0
        self.anim_start = []
        self.anim_end = []

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """Blocks wheel events so mouse scrolling doesn't shrink the chart."""
        if obj is self.plot and event.type() == QEvent.Wheel:
            return True
        return super().eventFilter(obj, event)

    def set_points(self, points):
        """Instant redraw for batch updates (Daily Trends)."""
        try:
            self.data = [float(v) for v in points]
        except (ValueError, TypeError):
            return

        x = list(range(len(self.data)))
        self.curve.setData(x, self.data)
        self.glow.setData(x, self.data)
        self.fill_bottom.setData(x, [0] * len(self.data))
        # Auto-range once to fit data perfectly without user interaction
        self.plot_item.enableAutoRange()

    def add_point(self, value):
        """Smoothly animates a new point into the chart."""
        try:
            val = float(value)
        except (ValueError, TypeError):
            return

        self.data.append(val)
        if len(self.data) > self.max_points:
            self.data.pop(0)

        # Prepare animation
        curr_y = self.curve.getData()[1]
        self.anim_start = curr_y.tolist() if curr_y is not None else []
        self.anim_end = self.data.copy()
        self.anim_progress = 0
        self.anim_timer.start()

    def animate_step(self):
        if not self.anim_end: return
        
        self.anim_progress += 0.07 # Animation speed
        if self.anim_progress >= 1:
            self.anim_progress = 1
            self.anim_timer.stop()

        # Premium easing: OutCubic makes the 'bounce' feel natural
        easing = QEasingCurve(QEasingCurve.OutCubic)
        eased_val = easing.valueForProgress(self.anim_progress)

        interpolated = []
        for i in range(len(self.anim_end)):
            start_val = self.anim_start[i] if i < len(self.anim_start) else self.anim_end[i]
            end_val = self.anim_end[i]
            interpolated.append(start_val + (end_val - start_val) * eased_val)

        x = list(range(len(interpolated)))
        self.curve.setData(x, interpolated)
        self.glow.setData(x, interpolated)
        self.fill_bottom.setData(x, [0] * len(interpolated))