from datetime import datetime

from PySide6.QtCore import QObject, Signal, Slot

from chat.message import Message
from config.logger import get_logger

logger = get_logger(__name__)


class GeminiWorker(QObject):

    finished = Signal(Message)
    error = Signal(str)

    def __init__(self, gemini_client):
        super().__init__()

        self.gemini = gemini_client
        self.history = []

    def set_history(self, history):
        self.history = history

    @Slot()
    def run(self):

        logger.info("Gemini worker start")

        try:

            reply = self.gemini.generate(
                self.history
            )

            message = Message(
                sender="AI",
                text=reply,
                timestamp=datetime.now()
            )

            self.finished.emit(
                message
            )

        except Exception as e:

            logger.exception(
                "Gemini API error"
            )

            self.error.emit(
                self.convert_error_message(e)
            )

    def convert_error_message(self, error):

        error_text = str(error)

        if "429" in error_text:
            return (
                "現在、AIサービスの利用上限に達しています。\n"
                "しばらく時間をおいてから再試行してください。"
            )

        elif "401" in error_text:
            return (
                "APIキーが正しく設定されていません。"
            )

        elif "400" in error_text:
            return (
                "送信内容に問題があります。"
            )

        return (
            "AIとの通信中にエラーが発生しました。"
        )