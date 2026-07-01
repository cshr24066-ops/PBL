from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTextEdit
from system.windows.ime import (
    is_ime_composing
)


class InputTextEdit(QTextEdit):

    send_requested = Signal(str)

    def keyPressEvent(self, event):

        hwnd = int(self.winId())

        if is_ime_composing(hwnd):
            super().keyPressEvent(event)
            return

        if (
            event.key()
            in (
                Qt.Key.Key_Return,
                Qt.Key.Key_Enter
            )
        ):

            if (
                event.modifiers()
                & Qt.KeyboardModifier.ShiftModifier
            ):

                super().keyPressEvent(event)
                return

            text = self.toPlainText().strip()

            if text:

                self.send_requested.emit(text)

                self.clear()

            return

        super().keyPressEvent(event)
    
    def submit(self):

        text = self.toPlainText().strip()

        if not text:
            return

        self.send_requested.emit(text)

        self.clear()