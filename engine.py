# engine.py
import time
import threading

from PyQt5.QtCore import pyqtSignal, QObject, QThread
from pynput import keyboard as pkb
from pynput.keyboard import Key, Controller


class BinderSignals(QObject):
    triggered = pyqtSignal(str, str)


class BinderEngine(QThread):
    def __init__(self, binds: list):
        super().__init__()
        self.binds = list(binds)
        self.signals = BinderSignals()
        self._ctrl = Controller()
        self._buf = []
        self._busy = False
        self._listener = None

    def update_binds(self, binds: list):
        self.binds = list(binds)

    def _do_replace(self, trigger, replacement, auto_send):
        self._busy = True
        time.sleep(0.04)
        for _ in range(len(trigger)):
            self._ctrl.tap(Key.backspace)
            time.sleep(0.008)
        self._ctrl.type(replacement)
        if auto_send:
            time.sleep(0.12)
            self._ctrl.tap(Key.enter)
        self.signals.triggered.emit(trigger, replacement)
        self._busy = False

    def _on_press(self, key):
        if self._busy:
            return
        if key in (Key.enter, Key.esc):
            self._buf.clear()
            return
        if key == Key.backspace:
            if self._buf:
                self._buf.pop()
            return
        if key == Key.space:
            self._buf.append(" ")
        elif hasattr(key, "char") and key.char:
            self._buf.append(key.char)

        current = "".join(self._buf)
        for b in self.binds:
            if current.endswith(b["trigger"]):
                del self._buf[-len(b["trigger"]):]
                threading.Thread(
                    target=self._do_replace,
                    args=(b["trigger"], b["replacement"], b.get("auto_send", False)),
                    daemon=True,
                ).start()
                break

    def run(self):
        with pkb.Listener(on_press=self._on_press) as listener:
            self._listener = listener
            listener.join()

    def stop(self):
        if self._listener:
            self._listener.stop()
