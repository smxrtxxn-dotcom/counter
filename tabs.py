# tabs.py
import json
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox,
    QFileDialog,
)

from config import TEXT_DIM


class _PlaceholderTab(QWidget):
    def __init__(self, text: str):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignCenter)
        lbl = QLabel(text)
        lbl.setStyleSheet(f"color:{TEXT_DIM};font-size:13px;background:transparent;")
        lbl.setAlignment(Qt.AlignCenter)
        lay.addWidget(lbl)


class SettingsTab(_PlaceholderTab):
    def __init__(self):
        super().__init__("Настройки — в разработке")


class BindsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window
        self._editing_idx = -1
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 18, 20, 14)
        lay.setSpacing(0)

        # ── Форма добавления
        form = QWidget()
        form.setObjectName("form_panel")
        fl = QVBoxLayout(form)
        fl.setContentsMargins(14, 12, 14, 12)
        fl.setSpacing(10)

        self.form_lbl = QLabel("ДОБАВИТЬ БИНД")
        self.form_lbl.setObjectName("section_title")
        fl.addWidget(self.form_lbl)

        fr = QHBoxLayout()
        fr.setSpacing(10)

        col_t = QVBoxLayout()
        col_t.setSpacing(4)
        lt = QLabel("ТРИГГЕР")
        lt.setObjectName("fieldlabel")
        self.inp_trigger = QLineEdit()
        self.inp_trigger.setPlaceholderText(".ку")
        self.inp_trigger.setFixedHeight(40)
        col_t.addWidget(lt)
        col_t.addWidget(self.inp_trigger)

        col_r = QVBoxLayout()
        col_r.setSpacing(4)
        lr = QLabel("ЗАМЕНА")
        lr.setObjectName("fieldlabel")
        self.inp_replace = QLineEdit()
        self.inp_replace.setPlaceholderText("Приветствую")
        self.inp_replace.setFixedHeight(40)
        col_r.addWidget(lr)
        col_r.addWidget(self.inp_replace)

        fr.addLayout(col_t, 1)
        fr.addLayout(col_r, 2)
        fl.addLayout(fr)

        cbrow = QHBoxLayout()
        cbrow.setSpacing(20)
        self.chk_send = QCheckBox("Автоотправка")
        self.chk_cmd = QCheckBox("Команда")
        cbrow.addWidget(self.chk_send)
        cbrow.addWidget(self.chk_cmd)
        cbrow.addStretch()
        fl.addLayout(cbrow)

        br = QHBoxLayout()
        br.setSpacing(8)
        self.btn_cancel = QPushButton("ОТМЕНА")
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_cancel.setFixedHeight(40)
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.clicked.connect(self._cancel)
        self.btn_cancel.hide()

        self.btn_add = QPushButton("+ ДОБАВИТЬ")
        self.btn_add.setObjectName("btn_add")
        self.btn_add.setFixedHeight(40)
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_add.clicked.connect(self._save)

        br.addStretch()
        br.addWidget(self.btn_cancel)
        br.addWidget(self.btn_add)
        fl.addLayout(br)

        lay.addWidget(form)
        lay.addSpacing(20)

        # ── Управление списками
        sec1 = QLabel("УПРАВЛЕНИЕ СПИСКАМИ")
        sec1.setObjectName("section_title")
        lay.addWidget(sec1)
        lay.addSpacing(8)

        prow = QHBoxLayout()
        prow.setSpacing(12)

        self.btn_open_binds = QPushButton("  📋  БИНДЫ  →")
        self.btn_open_binds.setObjectName("btn_open_panel")
        self.btn_open_binds.setFixedHeight(46)
        self.btn_open_binds.setCursor(Qt.PointingHandCursor)
        self.btn_open_binds.clicked.connect(lambda: self.mw.open_panel(False))

        self.btn_open_cmds = QPushButton("  ⌨  КОМАНДЫ  →")
        self.btn_open_cmds.setObjectName("btn_open_panel")
        self.btn_open_cmds.setFixedHeight(46)
        self.btn_open_cmds.setCursor(Qt.PointingHandCursor)
        self.btn_open_cmds.clicked.connect(lambda: self.mw.open_panel(True))

        prow.addWidget(self.btn_open_binds, 1)
        prow.addWidget(self.btn_open_cmds, 1)
        lay.addLayout(prow)
        lay.addSpacing(20)

        # ── Экспорт / Импорт / Слияние
        sec2 = QLabel("ЭКСПОРТ И ИМПОРТ")
        sec2.setObjectName("section_title")
        lay.addWidget(sec2)
        lay.addSpacing(8)

        exp_row = QHBoxLayout()
        exp_row.setSpacing(10)
        for label, slot in [
            ("↗  ЭКСПОРТ", self._export),
            ("↙  ИМПОРТ", self._import),
            ("⇄  СЛИЯНИЕ", self._merge),
        ]:
            b = QPushButton(label)
            b.setObjectName("btn_settings")
            b.setFixedHeight(40)
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(slot)
            exp_row.addWidget(b, 1)
        lay.addLayout(exp_row)
        lay.addSpacing(12)

        # Счётчики
        ctr = QHBoxLayout()
        self.lbl_cnt_binds = QLabel("")
        self.lbl_cnt_binds.setObjectName("counter")
        self.lbl_cnt_cmds = QLabel("")
        self.lbl_cnt_cmds.setObjectName("counter")
        ctr.addWidget(self.lbl_cnt_binds)
        ctr.addStretch()
        ctr.addWidget(self.lbl_cnt_cmds)
        lay.addLayout(ctr)

        lay.addStretch()

        self.inp_trigger.returnPressed.connect(self._save)
        self.inp_replace.returnPressed.connect(self._save)

    def fill(self):
        nb = len([b for b in self.mw.binds if not b.get("is_command", False)])
        nc = len([b for b in self.mw.binds if b.get("is_command", False)])
        wb = "бинд" if nb == 1 else "бинда" if 2 <= nb <= 4 else "биндов"
        wc = "команда" if nc == 1 else "команды" if 2 <= nc <= 4 else "команд"
        self.btn_open_binds.setText(f"  📋  БИНДЫ  —  {nb} {wb}  →")
        self.btn_open_cmds.setText(f"  ⌨  КОМАНДЫ  —  {nc} {wc}  →")
        self.lbl_cnt_binds.setText(f"Всего биндов: {nb}")
        self.lbl_cnt_cmds.setText(f"Всего команд: {nc}")

    def _save(self):
        trigger = self.inp_trigger.text().strip()
        replacement = self.inp_replace.text().strip()
        if not trigger:
            self.mw._shake(self.inp_trigger)
            return
        if not replacement:
            self.mw._shake(self.inp_replace)
            return

        auto_send = self.chk_send.isChecked()
        is_command = self.chk_cmd.isChecked()

        if self._editing_idx >= 0:
            self.mw.binds[self._editing_idx] = {
                "trigger": trigger,
                "replacement": replacement,
                "auto_send": auto_send,
                "is_command": is_command,
            }
            self._editing_idx = -1
            self.btn_add.setText("+ ДОБАВИТЬ")
            self.form_lbl.setText("ДОБАВИТЬ БИНД")
            self.btn_cancel.hide()
            msg = f"Бинд «{trigger}» обновлён"
        else:
            if trigger in [b["trigger"] for b in self.mw.binds]:
                self.mw.toast.show_message(f"⚠  Триггер «{trigger}» уже существует")
                self.mw._shake(self.inp_trigger)
                return
            self.mw.binds.append(
                {
                    "trigger": trigger,
                    "replacement": replacement,
                    "auto_send": auto_send,
                    "is_command": is_command,
                }
            )
            msg = f"Бинд «{trigger}» добавлён"

        self.mw._save_settings()
        self.fill()
        self.mw._update_engine()
        self.inp_trigger.clear()
        self.inp_replace.clear()
        self.chk_send.setChecked(False)
        self.chk_cmd.setChecked(False)
        self.mw.toast.show_message(f"✓  {msg}")

    def _cancel(self):
        self._editing_idx = -1
        self.inp_trigger.clear()
        self.inp_replace.clear()
        self.chk_send.setChecked(False)
        self.chk_cmd.setChecked(False)
        self.btn_add.setText("+ ДОБАВИТЬ")
        self.form_lbl.setText("ДОБАВИТЬ БИНД")
        self.btn_cancel.hide()

    def _export(self):
        path, _ = QFileDialog.getSaveFileName(self, "Экспорт биндов", "binds_export.json", "JSON (*.json)")
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.mw.binds, f, ensure_ascii=False, indent=2)
            self.mw.toast.show_message(f"✓  Экспортировано: {os.path.basename(path)}")
        except Exception as e:
            self.mw.toast.show_message(f"⚠  Ошибка: {e}")

    def _import(self):
        path, _ = QFileDialog.getOpenFileName(self, "Импорт биндов", "", "JSON (*.json)")
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Ожидается список биндов")
            self.mw.binds = data
            self.mw._save_settings()
            self.fill()
            self.mw._update_engine()
            self.mw.toast.show_message(f"✓  Импортировано: {len(data)} биндов")
        except Exception as e:
            self.mw.toast.show_message(f"⚠  Ошибка: {e}")

    def _merge(self):
        path, _ = QFileDialog.getOpenFileName(self, "Слияние биндов", "", "JSON (*.json)")
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Ожидается список биндов")
            existing = {b["trigger"] for b in self.mw.binds}
            added = 0
            for b in data:
                t = b.get("trigger")
                if not t or t in existing:
                    continue
                self.mw.binds.append(b)
                existing.add(t)
                added += 1

            self.mw._save_settings()
            self.fill()
            self.mw._update_engine()
            self.mw.toast.show_message(f"✓  Добавлено {added} новых биндов")
        except Exception as e:
            self.mw.toast.show_message(f"⚠  Ошибка: {e}")
