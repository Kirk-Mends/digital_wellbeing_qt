from dataclasses import dataclass
from PySide6.QtGui import QColor


# ============================================================
# Premium Theme Model
# ============================================================

@dataclass
class AppTheme:
    name: str

    # Core surfaces
    backgroundColor: QColor
    cardColor: QColor
    panelColor: QColor
    dividerColor: QColor
    shadowColor: QColor

    # Accent + text
    accentColor: QColor
    textPrimary: QColor
    textSecondary: QColor
    subtleText: QColor

    # Blur + radii
    blurOpacity: float
    cardRadius: int
    panelRadius: int


# Global accent used across all themes
TEAL_ACCENT = QColor("#0FB5A9")


# ============================================================
# Light Theme
# ============================================================

def make_light_theme() -> AppTheme:
    return AppTheme(
        name="light",
        backgroundColor=QColor("#F4F5F7"),
        cardColor=QColor(255, 255, 255),
        panelColor=QColor(255, 255, 255),
        dividerColor=QColor(0, 0, 0),
        shadowColor=QColor(0, 0, 0),

        accentColor=TEAL_ACCENT,

        textPrimary=QColor("#111111"),
        textSecondary=QColor("#444444"),
        subtleText=QColor("#777777"),

        blurOpacity=0.82,
        cardRadius=18,
        panelRadius=22,
    )


# ============================================================
# Dark Theme
# ============================================================

def make_dark_theme() -> AppTheme:
    return AppTheme(
        name="dark",
        backgroundColor=QColor("#05070A"),
        cardColor=QColor(18, 20, 26),
        panelColor=QColor(16, 18, 24),
        dividerColor=QColor(255, 255, 255),
        shadowColor=QColor(0, 0, 0),

        accentColor=TEAL_ACCENT,

        textPrimary=QColor("#F5F7FA"),
        textSecondary=QColor("#C3C7D0"),
        subtleText=QColor("#8A8F9C"),

        blurOpacity=0.78,
        cardRadius=18,
        panelRadius=22,
    )


# ============================================================
# Blue Theme (Premium Midnight Blue)
# ============================================================

def make_blue_theme() -> AppTheme:
    return AppTheme(
        name="blue",
        backgroundColor=QColor("#0B1220"),
        cardColor=QColor(15, 23, 42),
        panelColor=QColor(15, 23, 42),
        dividerColor=QColor(148, 163, 184),
        shadowColor=QColor(15, 23, 42),

        accentColor=TEAL_ACCENT,

        textPrimary=QColor("#E5E7EB"),
        textSecondary=QColor("#9CA3AF"),
        subtleText=QColor("#6B7280"),

        blurOpacity=0.80,
        cardRadius=18,
        panelRadius=22,
    )


# ============================================================
# Custom Theme (User-defined background)
# ============================================================

def make_custom_theme(base_bg: QColor | None = None) -> AppTheme:
    bg = base_bg or QColor("#05070A")
    return AppTheme(
        name="custom",
        backgroundColor=bg,
        cardColor=QColor(18, 20, 26),
        panelColor=QColor(16, 18, 24),
        dividerColor=QColor(255, 255, 255),
        shadowColor=QColor(0, 0, 0),

        accentColor=TEAL_ACCENT,

        textPrimary=QColor("#F5F7FA"),
        textSecondary=QColor("#C3C7D0"),
        subtleText=QColor("#8A8F9C"),

        blurOpacity=0.80,
        cardRadius=18,
        panelRadius=22,
    )


# ============================================================
# Premium Metrics (Spacing, Radii, Layout Rhythm)
# ============================================================

class AppMetrics:
    CARD_RADIUS = 18
    CARD_PADDING = 10
    CARD_HEIGHT = 300

    GAP_SMALL = 8
    GAP_MEDIUM = 14
    GAP_LARGE = 22


# ============================================================
# Legacy Compatibility Layer (Old SmartMode + AIMode)
# ============================================================

class AppColors:
    # Semantic accents (old system)
    BEHAVIOR = "#0A84FF"       # blue
    FATIGUE = "#FF9F0A"        # orange
    BREAK = "#30D158"          # green
    SUPPRESSION = "#FF453A"    # red
    INSIGHT = "#BF5AF2"        # purple

    # Text (old system)
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "rgba(255, 255, 255, 0.7)"
    TEXT_MUTED = "rgba(255, 255, 255, 0.5)"

    # Surfaces (old system)
    SURFACE_DARK = "#1C1C1E"
    SURFACE_LIGHT = "#FFFFFF"
