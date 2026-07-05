from PySide6.QtMultimedia import (
    QMediaPlayer,
    QAudioOutput
)

from PySide6.QtCore import (
    QUrl,
    QObject,
    Signal,
    Slot
)


class AudioPlayer(QObject):

    finished = Signal()


    def __init__(self):

        super().__init__()

        self.player = QMediaPlayer()

        self.audio_output = QAudioOutput()

        self.player.setAudioOutput(
            self.audio_output
        )


        self.player.mediaStatusChanged.connect(
            self.on_media_status_changed
        )


    def play(self, filename):

        self.player.setSource(
            QUrl.fromLocalFile(filename)
        )

        self.player.play()


    def on_media_status_changed(
        self,
        status
    ):

        if status == QMediaPlayer.MediaStatus.EndOfMedia:

            print(
                "audio finished"
            )

            self.finished.emit()
    
    @Slot(str)
    def play_file(self, filename):
        self.play(filename)