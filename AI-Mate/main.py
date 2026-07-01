import sys

from PySide6.QtWidgets import QApplication

from app.ai_mate_app import AIMateApp
from config.logger import setup_logger

def main():
    setup_logger()
    app = QApplication(sys.argv)
    ai_mate = AIMateApp()

    ai_mate.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()