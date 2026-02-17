# panels.py
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit,
    QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QAbstractItemView,
    QCheckBox,
)

from config import ACCENT, BG2, BG3, BORDER, TEXT, TEXT_DIM


class BindListPanel(QWidget):
    def __init__(self, main_window, is_commands: bool = False):
        super().__init__()
        self.mw = main_window
        self.is_commands = is_commands
        self._edit_row = -1
        self._edit_bind_idx = -1
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(12)

        # Шапка
        top = QHBoxLayout()
        btn_back = QPushButton("← НАЗАД")
        btn_back.setObjectName("btn_back")
        btn_back.setCursor(Qt.PointingHandCursor)
        btn_back.clicked.connect(self._go_back)

        lbl = QLabel("КОМАНДЫ" if self.is_commands else "БИНДЫ")
        lbl.setObjectName("section_title")

        self.lbl_count = QLabel("")
        self.lbl_count.setObjectName("counter")

        top.addWidget(btn_back)
        top.addSpacing(12)
        top.addWidget(lbl)
        top.addStretch()
        top.addWidget(self.lbl_count)
        lay.addLayout(top)

        # Поиск
        self.search = QLineEdit()
        self.search.setObjectName("search_box")
        self.search.setPlaceholderText("🔍  Поиск по триггеру или фразе...")
        self.search.setFixedHeight(38)
        self.search.textChanged.connect(self._apply_filter)
        lay.addWidget(self.search)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ТРИГГЕР", "ФРАЗА", "↵", "", ""])
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.Fixed)
        hh.setSectionResizeMode(1, QHeaderView.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.Fixed)
        hh.setSectionResizeMode(3, QHeaderView.Fixed)
        hh.setSectionResizeMode(4, QHeaderView.Fixed)

        self.table.setColumnWidth(0, 110)
        self.table.setColumnWidth(2, 30)
        self.table.setColumnWidth(3, 0)
        self.table.setColumnWidth(4, 88)

        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.verticalHeader().setDefaultSectionSize(50)
        lay.addWidget(self.table, 1)

    # ── Навигация ─────────────────────────────────────────────────────────────
    def _go_back(self):
        self._cancel_inline()
        self.mw.pages.setCurrentIndex(0)
        self.mw.setFixedHeight(self.mw._main_height)

    # ── Обновление ────────────────────────────────────────────────────────────
    def refresh(self):
        self._cancel_inline()
        self.search.clear()
        self._apply_filter("")

    def _apply_filter(self, text: str):
        q = text.strip().lower()
        items = [b for b in self.mw.binds if b.get("is_command", False) == self.is_commands]
        if q:
            items = [b for b in items if q in b["trigger"].lower() or q in b["replacement"].lower()]
        self._fill(items)

        total = len([b for b in self.mw.binds if b.get("is_command", False) == self.is_commands])
        label = "команд" if self.is_commands else "биндов"
        self.lbl_count.setText(f"{len(items)} / {total} {label}" if q else f"{total} {label}")

    def _fill(self, items: list):
        self._edit_row = -1
        self._edit_bind_idx = -1
        self.table.setRowCount(0)
        self.table.setColumnWidth(3, 0)

        for b in items:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self._set_row_view(row, b)

    def _set_row_view(self, row: int, b: dict):
        it = QTableWidgetItem(b["trigger"])
        it.setFont(QFont("Consolas", 12))
        it.setForeground(QColor(ACCENT))
        it.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.table.setItem(row, 0, it)

        short = b["replacement"] if len(b["replacement"]) <= 38 else b["replacement"][:35] + "…"
        ir = QTableWidgetItem(short)
        ir.setForeground(QColor(TEXT))
        ir.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        ir.setToolTip(b["replacement"])
        self.table.setItem(row, 1, ir)

        fw = QWidget()
        fw.setStyleSheet("background:transparent;")
        fl = QHBoxLayout(fw)
        fl.setContentsMargins(0, 0, 0, 0)
        fl.setAlignment(Qt.AlignCenter)
        if b.get("auto_send"):
            lb = QLabel("↵")
            lb.setObjectName("badge_send")
            lb.setToolTip("Автоотправка")
            fl.addWidget(lb)
        self.table.setCellWidget(row, 2, fw)

        self.table.setItem(row, 3, QTableWidgetItem(""))
        self._set_action_btns(row, b)

    def _set_action_btns(self, row: int, b: dict):
        cell = QWidget()
        cell.setStyleSheet("background:transparent;")
        cl = QHBoxLayout(cell)
        cl.setContentsMargins(6, 8, 8, 8)
        cl.setSpacing(6)

        be = QPushButton("✎")
        be.setObjectName("btn_icon_edit")
        be.setCursor(Qt.PointingHandCursor)
        be.setToolTip("Редактировать")
        be.clicked.connect(lambda _, bind=b, r=row: self._start_inline(r, bind))

        bd = QPushButton("🗑")
        bd.setObjectName("btn_icon_del")
        bd.setCursor(Qt.PointingHandCursor)
        bd.setToolTip("Удалить")
        bd.clicked.connect(lambda _, bind=b: self._delete(bind))

        cl.addStretch()
        cl.addWidget(be)
        cl.addWidget(bd)
        self.table.setCellWidget(row, 4, cell)

    # ── Инлайн-редактирование ─────────────────────────────────────────────────
    def _start_inline(self, row: int, b: dict):
        if self._edit_row >= 0:
            self._cancel_inline()

        self._edit_row = row
        self._edit_bind_idx = self.mw.binds.index(b)

        self.table.setColumnWidth(3, 240)
        self.table.setRowHeight(row, 58)

        w0 = QWidget()
        w0.setStyleSheet("background:transparent;")
        l0 = QHBoxLayout(w0)
        l0.setContentsMargins(4, 8, 4, 8)
        inp_t = QLineEdit(b["trigger"])
        inp_t.setObjectName("cell_edit")
        inp_t.setFixedHeight(34)
        l0.addWidget(inp_t)
        self.table.setCellWidget(row, 0, w0)
        self._inp_trigger = inp_t

        w3 = QWidget()
        w3.setStyleSheet("background:transparent;")
        l3 = QVBoxLayout(w3)
        l3.setContentsMargins(4, 6, 4, 6)
        l3.setSpacing(4)
        inp_r = QLineEdit(b["replacement"])
        inp_r.setObjectName("cell_edit")
        inp_r.setFixedHeight(34)
        chk = QCheckBox("Автоотправка")
        chk.setChecked(b.get("auto_send", False))
        chk.setStyleSheet(f"font-size:10px;color:{TEXT_DIM};background:transparent;spacing:4px;")
        l3.addWidget(inp_r)
        l3.addWidget(chk)
        self.table.setCellWidget(row, 3, w3)
        self._inp_replace = inp_r
        self._chk_send = chk

        cell = QWidget()
        cell.setStyleSheet("background:transparent;")
        cl = QHBoxLayout(cell)
        cl.setContentsMargins(6, 8, 8, 8)
        cl.setSpacing(6)

        bs = QPushButton("OK")
        bs.setObjectName("btn_icon_save")
        bs.setCursor(Qt.PointingHandCursor)
        bs.clicked.connect(self._commit_inline)

        bc = QPushButton("✕")
        bc.setObjectName("btn_icon_cancel")
        bc.setCursor(Qt.PointingHandCursor)
        bc.clicked.connect(self._cancel_inline)

        cl.addStretch()
        cl.addWidget(bs)
        cl.addWidget(bc)
        self.table.setCellWidget(row, 4, cell)

        inp_t.returnPressed.connect(self._commit_inline)
        inp_r.returnPressed.connect(self._commit_inline)

    def _commit_inline(self):
        if self._edit_row < 0:
            return

        new_trigger = self._inp_trigger.text().strip()
        new_replace = self._inp_replace.text().strip()
        if not new_trigger or not new_replace:
            return

        b = self.mw.binds[self._edit_bind_idx]
        old_trigger = b["trigger"]

        for i, ex in enumerate(self.mw.binds):
            if i != self._edit_bind_idx and ex["trigger"] == new_trigger:
                self.mw.toast.show_message(f"⚠  Триггер «{new_trigger}» уже существует")
                return

        self.mw.binds[self._edit_bind_idx] = {
            "trigger": new_trigger,
            "replacement": new_replace,
            "auto_send": self._chk_send.isChecked(),
            "is_command": b.get("is_command", False),
        }
        self.mw._save_settings()
        self.mw._update_engine()
        self.mw.binds_tab.fill()
        self.mw.toast.show_message(f"✓  Бинд «{old_trigger}» обновлён")

        self._edit_row = -1
        self._edit_bind_idx = -1
        self.table.setColumnWidth(3, 0)
        self._apply_filter(self.search.text())

    def _cancel_inline(self):
        if self._edit_row < 0:
            return
        self._edit_row = -1
        self._edit_bind_idx = -1
        self.table.setColumnWidth(3, 0)
        self._apply_filter(self.search.text())

    # ── Удаление ──────────────────────────────────────────────────────────────
    def _delete(self, b: dict):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Удаление")
        dlg.setText(f"Удалить бинд <b style='color:{ACCENT}'>{b['trigger']}</b>?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setDefaultButton(QMessageBox.No)
        dlg.setStyleSheet(f"""
            QMessageBox {{ background-color:{BG2}; }}
            QLabel {{ color:{TEXT}; font-size:13px; background:transparent; }}
            QPushButton {{
                background-color:{BG3}; border:1px solid {BORDER};
                border-radius:4px; color:{TEXT}; padding:6px 22px; min-width:70px;
            }}
            QPushButton:hover {{ border-color:{ACCENT}; color:{ACCENT}; }}
        """)
        if dlg.exec_() != QMessageBox.Yes:
            return

        self.mw.binds.remove(b)
        self.mw._save_settings()
        self.mw._update_engine()
        self.mw.binds_tab.fill()
        self._cancel_inline()
        self._apply_filter(self.search.text())
        self.mw.toast.show_message(f"✕  Бинд «{b['trigger']}» удалён")
