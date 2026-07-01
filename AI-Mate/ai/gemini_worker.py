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

            error_message = self.convert_error_message(e)

            self.error.emit(error_message)
    
    def convert_error_message(self, error):

        error_text = str(error)

        if "429" in error_text:
            return (
                "現在、AIの利用制限中です。\n"
                "しばらく待ってから再試行してください。"
            )

        elif "401" in error_text:
            return (
                "APIキーが正しく設定されていません。\n"
                "設定を確認してください。"
            )

        elif "400" in error_text:
            return (
                "送信内容に問題があります。\n"
                "入力内容を確認してください。"
            )

        else:
            return (
                "AIとの通信中にエラーが発生しました。\n"
                "もう一度試してください。"
            )