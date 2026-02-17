# widgets.py
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout

from config import ACCENT, BG3, TEXT_MID, TEXT_DIM, BORDER


class Toast(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("toast")
        self.setAlignment(Qt.AlignCenter)
        self.hide()
        self._ain = QPropertyAnimation(self, b"geometry")
        self._aout = QPropertyAnimation(self, b"geometry")
        self._tmr = QTimer(self)
        self._tmr.setSingleShot(True)
        self._tmr.timeout.connect(self._hide)

    def show_message(self, text: str, ms: int = 2200):
        self.setText(text)
        self.adjustSize()
        pw = self.parent().width()
        w = max(self.sizeHint().width() + 40, 240)
        h = 38
        x = (pw - w) // 2
        ye = self.parent().height() - 52
        ys = ye + 14
        self.setGeometry(x, ys, w, h)
        self.show()
        self.raise_()

        self._ain.stop()
        self._ain.setDuration(200)
        self._ain.setEasingCurve(QEasingCurve.OutCubic)
        self._ain.setStartValue(QRect(x, ys, w, h))
        self._ain.setEndValue(QRect(x, ye, w, h))
        self._ain.start()

        self._tmr.start(ms)

    def _hide(self):
        g = self.geometry()
        self._aout.stop()
        self._aout.setDuration(160)
        self._aout.setEasingCurve(QEasingCurve.InCubic)
        self._aout.setStartValue(g)
        self._aout.setEndValue(QRect(g.x(), g.y() + 12, g.width(), g.height()))
        self._aout.finished.connect(self.hide)
        self._aout.start()


class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("titlebar")
        self.setFixedHeight(46)
        self._drag = None

        lay = QHBoxLayout(self)
        lay.setContentsMargins(18, 0, 0, 0)
        lay.setSpacing(0)

        dot = QLabel("●")
        dot.setStyleSheet(f"color:{ACCENT};font-size:10px;margin-right:10px;background:transparent;")
        lay.addWidget(dot)

        col = QVBoxLayout()
        col.setSpacing(0)
        t = QLabel("RP BINDER")
        t.setObjectName("app_title")
        s = QLabel("GTA 5  ·  AUTO-REPLACE")
        s.setObjectName("app_subtitle")
        col.addWidget(t)
        col.addWidget(s)
        lay.addLayout(col)
        lay.addStretch()

        for name, symbol, slot in [
            ("tb_min", "─", parent.showMinimized),
            ("tb_close", "✕", parent.close),
        ]:
            b = QPushButton(symbol)
            b.setObjectName(name)
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(slot)
            lay.addWidget(b)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag = e.globalPos() - self.window().frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self._drag and e.buttons() == Qt.LeftButton:
            self.window().move(e.globalPos() - self._drag)

    def mouseReleaseEvent(self, e):
        self._drag = None
