import sys

from PySide6.QtWidgets import QApplication

from character.character_display import CharacterDisplay


def main():

    app = QApplication(sys.argv)

    character = CharacterDisplay(
        "assets/character.png"
    )

    character.setWindowTitle("AI Mate")

    character.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()