# ============================================================
# themes.py — Central Theme Engine for the Wellbeing App
# ============================================================

THEMES = {
    "light": {
        "bg": "#E9ECF1",
        "panel": "#FFFFFF",
        "card": "#F5F7FA",
        "text": "#333333",
        "accent": "#4A90E2",
        "accent_hover": "#6FB3F2",
        "border": "#D0D4D9",
        "shadow": "#C7CBD1"
    },

    "dark": {
        "bg": "#1E1E1E",
        "panel": "#252525",
        "card": "#2A2A2A",
        "text": "#FFFFFF",
        "accent": "#4A90E2",
        "accent_hover": "#6FB3F2",
        "border": "#3A3A3A",
        "shadow": "#000000"
    },

    "gray": {
        "bg": "#D9D9D9",
        "panel": "#C7C7C7",
        "card": "#BEBEBE",
        "text": "#222222",
        "accent": "#4A90E2",
        "accent_hover": "#6FB3F2",
        "border": "#AFAFAF",
        "shadow": "#B5B5B5"
    },

    "blue": {
        "bg": "#E8F0FF",
        "panel": "#FFFFFF",
        "card": "#DDE7FF",
        "text": "#1A1A1A",
        "accent": "#3A6FF7",
        "accent_hover": "#6A8FFF",
        "border": "#C5D4FF",
        "shadow": "#B8C8F7"
    },

    "teal": {
        "bg": "#E6FFFA",
        "panel": "#FFFFFF",
        "card": "#CCF5EE",
        "text": "#1A1A1A",
        "accent": "#1ABC9C",
        "accent_hover": "#48D1B5",
        "border": "#B3EDE2",
        "shadow": "#A0E0D4"
    },

    "purple": {
        "bg": "#F3E8FF",
        "panel": "#FFFFFF",
        "card": "#E6D6FF",
        "text": "#1A1A1A",
        "accent": "#9B59B6",
        "accent_hover": "#B57CCF",
        "border": "#D8C2F0",
        "shadow": "#C9B0E5"
    }
}


def get_theme(name: str):
    """Return theme dictionary, fallback to light."""
    return THEMES.get(name.lower(), THEMES["light"])
