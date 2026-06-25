import sys

from PySide6.QtWidgets import QApplication

from character.character_display import CharacterDisplay
from character.character_state import CharacterState

from PySide6.QtCore import QTimer

from chat.chat_window import ChatWindow

def main():

    from config.settings_manager import (
        SettingsManager
    )

    settings_manager = SettingsManager()

    settings = (
        settings_manager.load_settings()
    )

    settings["volume"] = 0.5

    settings_manager.save_settings(
        settings
    )

    print(settings)



    app = QApplication(sys.argv)

    gifs = {
        CharacterState.IDLE:
            "assets/idle.gif",

        CharacterState.THINKING:
            "assets/thinking.gif",

        CharacterState.TALKING:
            "assets/talking.gif",
    }

    character = CharacterDisplay(gifs)

    character.show()

    QTimer.singleShot(
        3000,
        lambda: character.change_state(
            CharacterState.THINKING
        )
    )

    QTimer.singleShot(
        6000,
        lambda: character.change_state(
            CharacterState.TALKING
        )
    )

    window = ChatWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()