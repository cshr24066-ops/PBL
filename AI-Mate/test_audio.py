from audio.audio_player import AudioPlayer
from PySide6.QtWidgets import QApplication
import sys


app = QApplication(sys.argv)


player = AudioPlayer()


player.finished.connect(
    lambda:
        print("再生終了")
)


player.play(
    "voice.wav"
)


sys.exit(
    app.exec()
)