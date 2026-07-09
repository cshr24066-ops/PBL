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
        
        self.player.positionChanged.connect(
            lambda p: print("position =", p)
        )

        self.player.durationChanged.connect(
            lambda d: print("duration =", d)
        )

        self.player.errorOccurred.connect(
            lambda: print(
                self.player.error(),
                self.player.errorString()
            )
        )


    def play(self, filename):

        print("duration before =", self.player.duration())

        self.player.setSource(
            QUrl.fromLocalFile(filename)
        )

        print("duration after setSource =", self.player.duration())

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