from PySide6.QtCore import QObject, Signal, Slot

from config.logger import get_logger

logger = get_logger(__name__)


class VoicevoxWorker(QObject):

    finished = Signal(str)
    error = Signal(str)

    def __init__(self, voicevox_client):
        super().__init__()

        self.voicevox = voicevox_client
        self.text = ""

    def set_text(self, text):
        self.text = text

    @Slot()
    def run(self):

        logger.info("Voicevox worker start")

        try:

            filename = self.voicevox.create_audio(
                self.text
            )

            logger.info(
                f"VOICEVOX finished: {filename}"
            )

            self.finished.emit(
                filename
            )

        except Exception as e:

            logger.exception(
                "VOICEVOX error"
            )

            self.error.emit(
                str(e)
            )