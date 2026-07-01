from PySide6.QtCore import QObject, Signal, Slot


class VoicevoxWorker(QObject):
    """
    VOICEVOX音声生成を別スレッドで実行するWorker
    """

    finished = Signal(str)
    error = Signal(str)


    def __init__(
        self,
        voicevox_client,
        text
    ):

        super().__init__()

        self.voicevox = voicevox_client
        self.text = text


    @Slot()
    def run(self):

        print("voicevox worker start")

        try:

            filename = self.voicevox.create_audio(
                self.text
            )

            print(
                "voicevox finished:",
                filename
            )

            self.finished.emit(
                filename
            )


        except Exception as e:

            print(e)

            self.error.emit(
                str(e)
            )