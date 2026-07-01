from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtCore import QThread
from character.character_display import CharacterDisplay
from character.character_state import CharacterState
from chat.chat_window import ChatWindow
from config.settings_manager import SettingsManager
from chat.chat_manager import ChatManager
from ai.gemini_client import GeminiClient
from ai.gemini_worker import GeminiWorker

class AIMateApp:

    def __init__(self):
        self.gemini = GeminiClient()

        self.chat = ChatWindow()

        self.gifs = {
            CharacterState.IDLE:
                "assets/idle.gif",

            CharacterState.THINKING:
                "assets/thinking.gif",

            CharacterState.TALKING:
                "assets/talking.gif",
        }

        self.character = CharacterDisplay(self.gifs)
        self.settings_manager = SettingsManager()
        self._connect_signals()
        self.chat_manager = ChatManager()

    def _connect_signals(self):

        self.character.clicked.connect(
            self.toggle_chat
        )

        self.character.destroyed.connect(
            self.chat.close
        )
        self.character.exit_requested.connect(
           self.exit_application
        )
        self.character.position_changed.connect(
            self.save_character_position
        )
        self.character.state_changed.connect(
            self.on_state_changed
        )
        self.chat.send_requested.connect(
            self.on_message_sent
        )

    def toggle_chat(self):

        if self.chat.isVisible():
            self.chat.hide()

        else:

            self.chat.move(
                self.character.x() + self.character.width(),
                self.character.y()
            )

            self.chat.show()

    def start(self):

        self.character.show()

       
    
    def save_character_position(
        self,
        x,
        y
    ):

        self.settings_manager.save_character_position(
            x,
            y
        )
    
    def on_state_changed(
    self,
    state
    ):

        print(state)
    


    def on_message_sent(self, text):

        # ユーザーメッセージを表示
        user_message = self.chat_manager.create_user_message(text)
        self.chat.add_message(user_message)

            # 考え中状態
        self.character.change_state(
            CharacterState.THINKING
        )

        # WorkerとThreadを生成
        self.thread = QThread()
        self.worker = GeminiWorker(self.gemini, text)

        # Workerを別スレッドへ移動
        self.worker.moveToThread(self.thread)

        # スレッド開始時にWorkerを実行
        self.thread.started.connect(self.worker.run)

        # Worker終了時
        self.worker.finished.connect(self.on_ai_response)

        # エラー時
        self.worker.error.connect(self.on_ai_error)

        # 後始末
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
    
    def on_ai_response(self, message):

        self.chat_manager.add_message(message)

        self.chat.add_message(message)

        # 会話状態
        self.character.change_state(
            CharacterState.TALKING
        )

        QTimer.singleShot(
            5000,
            lambda: self.character.change_state(
                CharacterState.IDLE
            )
    )
    
    def on_ai_error(self, error_message):

        print(error_message)

    def exit_application(self):

        self.chat.close()
        self.character.close()