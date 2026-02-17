# style.py
from config import (
    ACCENT, ACCENT_H, ACCENT_D,
    BG, BG2, BG3, BORDER,
    TEXT, TEXT_DIM, TEXT_MID,
)

STYLE = f"""
QWidget, QWidget * {{
    background-color: {BG};
    color: {TEXT};
    font-family: "Segoe UI", "DejaVu Sans", sans-serif;
}}

/* ── Тайтлбар ── */
QWidget#titlebar {{
    background-color: {BG};
    border-bottom: 1px solid {BORDER};
}}
QLabel#app_title {{
    color: {ACCENT}; font-size: 13px; font-weight: 700;
    letter-spacing: 4px; background: transparent;
}}
QLabel#app_subtitle {{
    color: {TEXT_DIM}; font-size: 9px;
    letter-spacing: 2px; background: transparent;
}}

/* ── Кнопки тайтлбара ── */
QPushButton#tb_min {{
    background-color: transparent; border: none; color: {TEXT_DIM};
    font-size: 16px; min-width: 40px; max-width: 40px;
    min-height: 46px; max-height: 46px; border-radius: 0px; padding: 0;
}}
QPushButton#tb_min:hover {{ background-color: #2a2a2a; color: {TEXT}; }}
QPushButton#tb_close {{
    background-color: transparent; border: none; color: {TEXT_DIM};
    font-size: 14px; min-width: 40px; max-width: 40px;
    min-height: 46px; max-height: 46px; border-radius: 0px; padding: 0;
}}
QPushButton#tb_close:hover {{ background-color: {ACCENT}; color: #ffffff; }}
QPushButton#tb_close:pressed {{ background-color: {ACCENT_D}; }}

/* ── Вкладки ── */
QTabWidget::pane {{ border: none; background-color: {BG}; }}
QTabWidget::tab-bar {{ alignment: left; }}
QTabBar {{ background-color: {BG}; }}
QTabBar::tab {{
    background-color: {BG}; color: {TEXT_DIM};
    font-size: 10px; font-weight: 700; letter-spacing: 2px;
    padding: 10px 22px; border: none;
    border-bottom: 2px solid transparent; min-width: 100px;
}}
QTabBar::tab:selected {{ color: {TEXT}; border-bottom: 2px solid {ACCENT}; }}
QTabBar::tab:hover:!selected {{ color: {TEXT_MID}; background-color: {BG}; }}

/* ── Метки ── */
QLabel#fieldlabel {{
    color: {TEXT_DIM}; font-size: 9px; font-weight: 700;
    letter-spacing: 2px; background: transparent;
}}
QLabel#section_title {{
    color: {TEXT_MID}; font-size: 9px; font-weight: 700;
    letter-spacing: 3px; background: transparent;
}}
QLabel#counter {{
    color: {TEXT_DIM}; font-size: 9px;
    letter-spacing: 1px; background: transparent;
}}

/* ── Разделитель ── */
QFrame#divider {{ background-color: {BORDER}; max-height: 1px; border: none; }}

/* ── Поля ввода ── */
QLineEdit {{
    background-color: {BG2}; border: 1px solid {BORDER};
    border-radius: 5px; color: {TEXT}; font-size: 13px; padding: 9px 12px;
    selection-background-color: {ACCENT}40; selection-color: #ffffff;
}}
QLineEdit:focus {{ border: 1px solid {ACCENT}; }}
QLineEdit#search_box {{
    background-color: {BG2}; border: 1px solid {BORDER};
    border-radius: 5px; color: {TEXT}; font-size: 12px; padding: 7px 12px;
}}
QLineEdit#search_box:focus {{ border: 1px solid {ACCENT}; }}

/* ── Чекбоксы ── */
QCheckBox {{
    color: {TEXT_MID}; font-size: 11px; spacing: 6px; background: transparent;
}}
QCheckBox:hover {{ color: {TEXT}; }}
QCheckBox::indicator {{
    width: 16px; height: 16px; border-radius: 3px;
    border: 1px solid {BORDER}; background-color: {BG2};
}}
QCheckBox::indicator:hover {{ border-color: {ACCENT}; }}
QCheckBox::indicator:checked {{ background-color: {ACCENT}; border-color: {ACCENT}; image: none; }}

/* ── Панель формы ── */
QWidget#form_panel {{
    background-color: {BG2}; border: 1px solid {BORDER}; border-radius: 7px;
}}

/* ── Таблица — без выделения ── */
QTableWidget {{
    background-color: {BG2}; border: 1px solid {BORDER};
    border-radius: 7px; gridline-color: transparent;
    color: {TEXT}; font-size: 13px; outline: none;
}}
QTableWidget::item {{
    padding: 0px 10px; border-bottom: 1px solid {BORDER};
    background-color: {BG2};
}}
QTableWidget::item:selected {{ background-color: {BG2}; color: {TEXT}; }}
QTableWidget::item:hover    {{ background-color: {BG2}; color: {TEXT}; }}
QHeaderView {{ background-color: {BG2}; border: none; }}
QHeaderView::section {{
    background-color: {BG2}; color: {TEXT_DIM};
    font-size: 9px; font-weight: 700; letter-spacing: 2px;
    padding: 9px 10px; border: none; border-bottom: 1px solid {BORDER};
}}
QScrollBar:vertical {{
    background: {BG}; width: 5px; border-radius: 2px; margin: 0;
}}
QScrollBar::handle:vertical {{
    background: #333; border-radius: 2px; min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{ background: {ACCENT}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{ height: 0px; }}

/* ── Кнопка + ДОБАВИТЬ ── */
QPushButton#btn_add {{
    background-color: {ACCENT}; color: #fff; border: none;
    border-radius: 5px; font-size: 12px; font-weight: 700;
    letter-spacing: 1px; padding: 10px 24px;
}}
QPushButton#btn_add:hover {{ background-color: {ACCENT_H}; }}
QPushButton#btn_add:pressed {{ background-color: {ACCENT_D}; }}

/* ── Кнопка ОТМЕНА ── */
QPushButton#btn_cancel {{
    background-color: transparent; border: 1px solid {BORDER};
    border-radius: 5px; color: {TEXT_MID}; font-size: 12px; padding: 10px 20px;
}}
QPushButton#btn_cancel:hover {{ border-color: {TEXT_MID}; color: {TEXT}; }}

/* ── Кнопка открыть панель ── */
QPushButton#btn_open_panel {{
    background-color: {BG2}; border: 1px solid {BORDER};
    border-radius: 5px; color: {TEXT}; font-size: 12px;
    font-weight: 600; padding: 9px 18px; text-align: left;
}}
QPushButton#btn_open_panel:hover {{
    border-color: {ACCENT}; color: {ACCENT}; background-color: {ACCENT}12;
}}

/* ── Кнопка НАЗАД ── */
QPushButton#btn_back {{
    background-color: transparent; border: 1px solid {BORDER};
    border-radius: 5px; color: {TEXT_MID}; font-size: 11px; padding: 7px 16px;
}}
QPushButton#btn_back:hover {{ border-color: {TEXT_MID}; color: {TEXT}; }}

/* ── Иконки-кнопки: карандаш ── */
QPushButton#btn_icon_edit {{
    background-color: transparent; border: 1px solid {BORDER};
    border-radius: 5px; color: {TEXT_MID}; font-size: 14px;
    min-width: 34px; max-width: 34px; min-height: 34px; max-height: 34px; padding: 0;
}}
QPushButton#btn_icon_edit:hover {{
    background-color: {ACCENT}22; border-color: {ACCENT}; color: {ACCENT};
}}

/* ── Иконки-кнопки: корзина ── */
QPushButton#btn_icon_del {{
    background-color: transparent; border: 1px solid #3a1a1a;
    border-radius: 5px; color: #883333; font-size: 14px;
    min-width: 34px; max-width: 34px; min-height: 34px; max-height: 34px; padding: 0;
}}
QPushButton#btn_icon_del:hover {{
    background-color: #ff000022; border-color: #ff4444; color: #ff4444;
}}

/* ── Кнопка сохранить строку ── */
QPushButton#btn_icon_save {{
    background-color: {ACCENT}; border: none;
    border-radius: 5px; color: #fff; font-size: 11px; font-weight: 700;
    min-width: 52px; max-width: 52px; min-height: 34px; max-height: 34px;
    padding: 0; letter-spacing: 0px;
}}
QPushButton#btn_icon_save:hover {{ background-color: {ACCENT_H}; }}
QPushButton#btn_icon_save:pressed {{ background-color: {ACCENT_D}; }}

/* ── Кнопка отмена строки ── */
QPushButton#btn_icon_cancel {{
    background-color: transparent; border: 1px solid {BORDER};
    border-radius: 5px; color: {TEXT_DIM}; font-size: 18px;
    min-width: 34px; max-width: 34px; min-height: 34px; max-height: 34px; padding: 0;
}}
QPushButton#btn_icon_cancel:hover {{ border-color: {TEXT_MID}; color: {TEXT}; }}

/* ── Кнопки настройки/экспорта ── */
QPushButton#btn_settings {{
    background-color: {BG2}; border: 1px solid {BORDER};
    border-radius: 5px; color: {TEXT}; font-size: 12px;
    font-weight: 600; padding: 10px 18px;
}}
QPushButton#btn_settings:hover {{
    border-color: {ACCENT}; color: {ACCENT}; background-color: {ACCENT}10;
}}
QPushButton#btn_settings:pressed {{ background-color: {ACCENT}20; }}

/* ── Бейдж ── */
QLabel#badge_send {{
    color: {ACCENT}; font-size: 10px; font-weight: 700;
    background: transparent; padding: 0;
}}

/* ── Тост ── */
QLabel#toast {{
    background-color: {BG3}; border: 1px solid {ACCENT}50;
    border-radius: 5px; color: {TEXT_MID};
    font-size: 11px; letter-spacing: 1px; padding: 8px 16px;
}}

/* ── Статусбар ── */
QStatusBar {{
    background-color: {BG}; color: {TEXT_DIM};
    font-size: 9px; border-top: 1px solid {BORDER};
}}
QStatusBar QLabel {{ background: transparent; color: {TEXT_DIM}; }}

/* ── Диалог ── */
QMessageBox {{ background-color: {BG2}; }}

/* ── Поле ввода внутри таблицы ── */
QLineEdit#cell_edit {{
    background-color: {BG}; border: 1px solid {ACCENT};
    border-radius: 3px; color: {TEXT}; font-size: 12px;
    padding: 3px 7px; min-height: 28px;
}}
"""
