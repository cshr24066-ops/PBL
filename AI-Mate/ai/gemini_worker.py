from PySide6.QtCore import QObject, Signal, Slot

from chat.message import Message
from datetime import datetime


class GeminiWorker(QObject):
    """
    Gemini APIとの通信を別スレッドで行うWorker
    """

    finished = Signal(Message)
    error = Signal(str)

    def __init__(self, gemini_client, text):
        super().__init__()

        self.gemini = gemini_client
        self.text = text

    @Slot()
    def run(self):

        try:
            reply = self.gemini.generate(self.text)

            message = Message(
                sender="AI",
                text=reply,
                timestamp=datetime.now()
            )

            self.finished.emit(message)

        except Exception as e:
            self.error.emit(str(e))