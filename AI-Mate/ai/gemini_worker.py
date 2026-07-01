from PySide6.QtCore import QObject, Signal, Slot

from chat.message import Message
from datetime import datetime


class GeminiWorker(QObject):
    """
    Gemini APIとの通信を別スレッドで行うWorker
    """

    finished = Signal(Message)
    error = Signal(str)

    def __init__(self, gemini_client, history):
        super().__init__()

        self.gemini = gemini_client
        self.history = history

    @Slot()
    @Slot()
    def run(self):

        print("worker start")

        try:
            reply = self.gemini.generate(self.history)

            print("gemini finished")

            message = Message(
                sender="AI",
                text=reply,
                timestamp=datetime.now()
            )

            print("emit finished")

            self.finished.emit(message)

        except Exception as e:
            print(e)
            self.error.emit(str(e))