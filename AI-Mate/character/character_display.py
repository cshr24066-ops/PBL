from pathlib import Path

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel


class CharacterDisplay(QLabel):

    def __init__(self, image_path: str):
        super().__init__()

        self.image_path = image_path

        self.load_image()

    def load_image(self):

        image_file = Path(self.image_path)

        if not image_file.exists():
            self.setText(
                f"画像が見つかりません\n{self.image_path}"
            )
            self.adjustSize()
            return

        pixmap = QPixmap(str(image_file))

        if pixmap.isNull():
            self.setText("画像の読み込みに失敗しました")
            self.adjustSize()
            return

        self.setPixmap(pixmap)
        self.adjustSize()