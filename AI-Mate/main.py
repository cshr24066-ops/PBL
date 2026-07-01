import sys

from PySide6.QtWidgets import QApplication

from app.ai_mate_app import AIMateApp


def main():

    app = QApplication(sys.argv)

    ai_mate = AIMateApp()

    ai_mate.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()