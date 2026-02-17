# config.py
import os

# ─────────────────────────────────────────────────────────────────────────────
#  Константы / дефолты
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "binder_settings.json")

DEFAULT_BINDS = [
    {"trigger": ".ку",     "replacement": "Приветствую",                              "auto_send": False, "is_command": False},
    {"trigger": ".пока",   "replacement": "До свидания, удачи на дорогах!",           "auto_send": False, "is_command": False},
    {"trigger": ".помощь", "replacement": "Нужна помощь? Обращайтесь!",               "auto_send": False, "is_command": False},
    {"trigger": ".инфо",   "replacement": "Меня зовут Officer Johnson, значок #1337", "auto_send": False, "is_command": False},
]

ACCENT   = "#ff0068"
ACCENT_H = "#ff3385"
ACCENT_D = "#cc0054"
BG       = "#141414"
BG2      = "#1c1c1c"
BG3      = "#222222"
BORDER   = "#2a2a2a"
TEXT     = "#ffffff"
TEXT_DIM = "#666666"
TEXT_MID = "#aaaaaa"

FIXED_WIDTH    = 820
DEFAULT_HEIGHT = 700
SCREEN_MARGIN  = 60  # отступ от нижней части экрана


def normalize_bind(b: dict) -> dict:
    """Приводит бинд к корректному виду (на случай импорта/слияния)."""
    return {
        "trigger": str(b.get("trigger", "")).strip(),
        "replacement": str(b.get("replacement", "")).strip(),
        "auto_send": bool(b.get("auto_send", False)),
        "is_command": bool(b.get("is_command", False)),
    }
