# app.py
import sys
import json
import os

from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QColor, QPalette, QPixmap, QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTabWidget, QStackedWidget, QStatusBar,
)

from config import (
    SETTINGS_FILE, DEFAULT_BINDS,
    FIXED_WIDTH, DEFAULT_HEIGHT, SCREEN_MARGIN,
    BG, BG2, BG3, BORDER, TEXT, ACCENT,
)
from style import STYLE
from engine import BinderEngine
from widgets import TitleBar, Toast
from tabs import BindsTab, _PlaceholderTab, SettingsTab
from panels import BindListPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._settings = self._load_settings()
        self.binds: list = self._settings.get("binds", list(DEFAULT_BINDS))
        self._main_height = DEFAULT_HEIGHT

        self._setup_window()
        self._build_ui()

        self.binds_tab.fill()
        self._start_engine()

    def _setup_window(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setWindowTitle("GTA5 RP Binder")
        self.setFixedWidth(FIXED_WIDTH)
        self.setFixedHeight(DEFAULT_HEIGHT)
        self.setStyleSheet(STYLE)

        pix = QPixmap(32, 32)
        pix.fill(QColor(ACCENT))
        self.setWindowIcon(QIcon(pix))

        pos = self._settings.get("window_pos")
        if pos:
            self.move(pos[0], pos[1])

    def _build_ui(self):
        root_w = QWidget()
        self.setCentralWidget(root_w)
        root = QVBoxLayout(root_w)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(TitleBar(self))

        self.pages = QStackedWidget()

        # Страница 0 — основной интерфейс
        main_page = QWidget()
        mp = QVBoxLayout(main_page)
        mp.setContentsMargins(0, 0, 0, 0)
        mp.setSpacing(0)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.binds_tab = BindsTab(self)
        self.tabs.addTab(self.binds_tab, "БИНДЫ")
        self.tabs.addTab(_PlaceholderTab("Счётчик — в разработке"), "СЧЁТЧИК")
        self.tabs.addTab(_PlaceholderTab("Статистика — в разработке"), "СТАТИСТИКА")
        self.tabs.addTab(SettingsTab(), "НАСТРОЙКИ")

        mp.addWidget(self.tabs, 1)
        self.pages.addWidget(main_page)

        # Страница 1 — панель биндов
        self.panel_binds = BindListPanel(self, is_commands=False)
        self.pages.addWidget(self.panel_binds)

        # Страница 2 — панель команд
        self.panel_cmds = BindListPanel(self, is_commands=True)
        self.pages.addWidget(self.panel_cmds)

        root.addWidget(self.pages, 1)

        sb = QStatusBar()
        sb.setSizeGripEnabled(False)
        self.setStatusBar(sb)

        self.toast = Toast(root_w)

    # ── Открыть панель ────────────────────────────────────────────────────────
    def open_panel(self, is_commands: bool):
        panel = self.panel_cmds if is_commands else self.panel_binds
        panel.refresh()

        screen = QApplication.primaryScreen().availableGeometry()
        max_h = screen.height() - SCREEN_MARGIN
        target_h = min(1000, max_h)

        cur_x = self.x()
        cur_y = self.y()
        if cur_y + target_h > screen.bottom() - SCREEN_MARGIN:
            cur_y = max(screen.top(), screen.bottom() - target_h - SCREEN_MARGIN)
            self.move(cur_x, cur_y)

        self.setFixedHeight(target_h)
        self.pages.setCurrentIndex(2 if is_commands else 1)

    # ── Настройки ─────────────────────────────────────────────────────────────
    def _load_settings(self) -> dict:
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"binds": list(DEFAULT_BINDS)}

    def _save_settings(self):
        self._settings["binds"] = self.binds
        self._settings["window_pos"] = [self.pos().x(), self.pos().y()]
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self._settings, f, ensure_ascii=False, indent=2)

    # ── Утилиты ───────────────────────────────────────────────────────────────
    def _shake(self, widget):
        orig = widget.geometry()
        a = QPropertyAnimation(widget, b"geometry")
        a.setDuration(280)
        a.setEasingCurve(QEasingCurve.Linear)
        dx = 5
        for t, m in [(0, 0), (.15, -1), (.3, 1), (.45, -1), (.6, 1), (.75, -1), (1, 0)]:
            a.setKeyValueAt(t, QRect(orig.x() + dx * m, orig.y(), orig.width(), orig.height()))
        a.start()
        self._shake_anim = a

    # ── Движок ────────────────────────────────────────────────────────────────
    def _start_engine(self):
        self.engine = BinderEngine(self.binds)
        self.engine.start()

    def _update_engine(self):
        self.engine.update_binds(self.binds)

    def closeEvent(self, event):
        self._save_settings()
        self.engine.stop()
        self.engine.wait(1000)
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(BG))
    palette.setColor(QPalette.WindowText, QColor(TEXT))
    palette.setColor(QPalette.Base, QColor(BG2))
    palette.setColor(QPalette.AlternateBase, QColor(BG3))
    palette.setColor(QPalette.Text, QColor(TEXT))
    palette.setColor(QPalette.Button, QColor(BG2))
    palette.setColor(QPalette.ButtonText, QColor(TEXT))
    palette.setColor(QPalette.Highlight, QColor(ACCENT + "40"))
    palette.setColor(QPalette.HighlightedText, QColor(ACCENT))
    app.setPalette(palette)

    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
