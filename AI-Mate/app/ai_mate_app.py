from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread
from character.character_display import CharacterDisplay
from character.character_state import CharacterState
from chat.chat_window import ChatWindow
from config.settings_manager import SettingsManager
from chat.chat_manager import ChatManager
from ai.gemini_client import GeminiClient
from ai.gemini_worker import GeminiWorker
from PySide6.QtCore import Qt
from chat.message import Message
from datetime import datetime
from audio.voicevox_worker import VoicevoxWorker
from audio.voicevox_client import VoicevoxClient
from audio.audio_player import AudioPlayer

class AIMateApp:

    def __init__(self):
        self.gemini = GeminiClient()
        self.settings_manager = SettingsManager()

        self.voicevox = VoicevoxClient(
            self.settings_manager.get_voicevox_settings()
        )
        self.audio_player = AudioPlayer()

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
        self.chat_manager = ChatManager()

        self._connect_signals()

        self.is_processing = False


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
        self.audio_player.finished.connect(
            self.on_voice_finished
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
        if self.is_processing:

            print(
                "処理中のため送信停止"
            )

            return
        self.is_processing = True

        # ユーザーメッセージを表示
        user_message = self.chat_manager.create_user_message(text)
        self.chat.add_message(user_message)

            # 考え中状態
        self.character.change_state(
            CharacterState.THINKING
        )

        # WorkerとThreadを生成
        self.thread = QThread()
        self.worker = GeminiWorker(
            self.gemini,
            self.chat_manager.get_history()
        )

        # Workerを別スレッドへ移動
        self.worker.moveToThread(self.thread)

        # スレッド開始時にWorkerを実行
        self.thread.started.connect(self.worker.run)

        # Worker終了時
        self.worker.finished.connect(
            self.on_ai_response,
            Qt.ConnectionType.QueuedConnection
        )
        # エラー時
        self.worker.error.connect(
            self.on_ai_error,
            Qt.ConnectionType.QueuedConnection
        )

        # 後始末
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
    
    def on_ai_response(self, message):

        print("on_ai_response start")

        self.chat_manager.add_message(message)
        self.chat.add_message(message)

        self.character.change_state(
            CharacterState.TALKING
        )

        self.start_voice(
            message.text
        )

        if self.thread.isRunning():
            self.thread.quit()

    def on_ai_error(self, error_message):

        print("on_ai_error called")

        self.is_processing = False

        error = Message(
            sender="AI",
            text="現在、AIサービスの利用制限中です。\nしばらく待ってから再試行してください。",
            timestamp=datetime.now()
        )

        self.chat.add_message(error)

        self.character.change_state(
            CharacterState.IDLE
        )

        if self.thread.isRunning():
            self.thread.quit()

    def on_voice_error(self, error_message):

        print(
            "VOICEVOX ERROR:",
            error_message
        )

        self.is_processing = False

        self.character.change_state(
            CharacterState.IDLE
        )
    def start_voice(self, text):
        self.is_processing = True
        self.voice_thread = QThread()

        self.voice_worker = VoicevoxWorker(
            self.voicevox,
            text
        )

        self.voice_worker.moveToThread(
            self.voice_thread
        )


        self.voice_thread.started.connect(
            self.voice_worker.run
        )


        self.voice_worker.finished.connect(
            self.play_voice
        )


        self.voice_worker.error.connect(
            self.on_voice_error
        )


        self.voice_worker.finished.connect(
            self.voice_thread.quit
        )

        self.voice_worker.finished.connect(
            self.voice_worker.deleteLater
        )

        self.voice_thread.finished.connect(
            self.voice_thread.deleteLater
        )


        self.voice_thread.start()

    def play_voice(self, filename):

        self.audio_player.play(
            filename
        )

    def on_voice_finished(self):

        print(
            "voice finished"
        )

        self.is_processing = False

        self.character.change_state(
            CharacterState.IDLE
        )
    def exit_application(self):

        try:
            if hasattr(self, "thread") and self.thread.isRunning():
                self.thread.quit()
                self.thread.wait()

        except RuntimeError:
            pass

        if hasattr(self, "voice_thread"):

            if self.voice_thread.isRunning():
                self.voice_thread.quit()
                self.voice_thread.wait()
                
        self.chat.close()
        self.character.close()

        QApplication.quit()