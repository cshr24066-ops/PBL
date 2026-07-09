from pathlib import Path

from PySide6.QtCore import (
    Qt,
    QPoint,
    QSize,
    Signal
)

from PySide6.QtWidgets import (
    QLabel,
    QMenu
)

from character.character_state import CharacterState
from config.settings_manager import SettingsManager
from PySide6.QtGui import QMovie, QGuiApplication


class CharacterDisplay(QLabel):

    clicked = Signal()
    exit_requested = Signal()
    position_changed = Signal(int, int)
    state_changed = Signal(CharacterState)

    def __init__(
            self, 
            image_paths: dict
    ):
        
        super().__init__()

        self.settings_manager = SettingsManager()

        self.state = CharacterState.IDLE

        self.image_paths = image_paths

        self.character_size = QSize(108, 165)

        # ドラッグ用
        self.drag_position = QPoint()

        # ウィンドウ設定
        self._setup_window()

        # GIF読み込み
        self._load_gif()

        # ドラッグ中かどうかのフラグ
        self.dragging = False

        

    def _setup_window(self):
 
        # タイトルバー非表示
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            # 常に最前面
            | Qt.WindowType.WindowStaysOnTopHint
        )

        # 背景透過
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

    def _set_movie(self, gif_path):

        self.movie = QMovie(gif_path)

        self.movie.setScaledSize(
            self.character_size
        )

        if not self.movie.isValid():
            return

        self.setMovie(self.movie)

        self.movie.start()

        self.adjustSize()

    def _load_gif(self):

        image_file = Path(
            self.image_paths[
                CharacterState.IDLE
            ]
        )

        self._set_movie(str(image_file))
        x, y = self.settings_manager.get_character_position()

        pos = self._clamp_position(
            QPoint(x, y)
        )

        self.move(pos)

    def _clamp_position(self, pos: QPoint) -> QPoint:
        """
        キャラクターが完全に画面外へ出ないように座標を補正
        """

        screen = QGuiApplication.screenAt(pos)

        if screen is None:
            screen = QGuiApplication.primaryScreen()

        geometry = screen.availableGeometry()

        # この分だけ画面内に残す
        VISIBLE_WIDTH = 60
        VISIBLE_HEIGHT = 10

        x = max(
            geometry.left() - self.width() + VISIBLE_WIDTH,
            min(
                pos.x(),
                geometry.right() - VISIBLE_WIDTH
            )
        )

        y = max(
            geometry.top(),
            min(
                pos.y(),
                geometry.bottom() - VISIBLE_HEIGHT
            )
        )

        return QPoint(x, y)


        
    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):

        if event.buttons() & Qt.MouseButton.LeftButton:
            new_pos = (
                event.globalPosition().toPoint()
                - self.drag_position
            )

            new_pos = self._clamp_position(new_pos)

            self.move(new_pos)

        self.dragging = True

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.position_changed.emit(
                self.x(),
                self.y()
            )

            if not self.dragging:

                self.clicked.emit()

        self.dragging = False
                
    def contextMenuEvent(self, event):
        """
        右クリックメニュー
        """

        menu = QMenu(self)

        exit_action = menu.addAction("終了")

        selected_action = menu.exec(
            event.globalPos()
        )

        if selected_action == exit_action:
            self.exit_requested.emit()

    def change_state(self, state):

        print("change: ", state)

        self.state = state

        gif_path = self.image_paths.get(state)

        if gif_path is None:
            return

        self._set_movie(gif_path)
        self.state_changed.emit(state)

    