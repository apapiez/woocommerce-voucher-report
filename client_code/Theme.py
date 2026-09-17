from anvil.js.window import document, localStorage

STORAGE_KEY = "wca-theme"

LIGHT_CHART_COLORS = {"font": "#1d2430", "grid": "#eef2f6"}
DARK_CHART_COLORS = {"font": "#c7d2db", "grid": "#2c3a45"}


def get_theme():
    return localStorage.getItem(STORAGE_KEY) or "light"


def apply_theme(theme):
    root = document.documentElement
    if root is not None:
        root.setAttribute("data-theme", theme)


def set_theme(theme):
    localStorage.setItem(STORAGE_KEY, theme)
    apply_theme(theme)


def toggle_theme():
    new_theme = "light" if get_theme() == "dark" else "dark"
    set_theme(new_theme)
    return new_theme


def chart_colors():
    return DARK_CHART_COLORS if get_theme() == "dark" else LIGHT_CHART_COLORS
