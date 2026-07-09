from datetime import datetime

from PySide6.QtCore import Qt, QThread
from PySide6.QtWidgets import QApplication

from ai.gemini_client import GeminiClient
from ai.gemini_worker import GeminiWorker

from audio.audio_player import AudioPlayer
from audio.voicevox_client import VoicevoxClient
from audio.voicevox_engine import VoiceVoxEngine
from audio.voicevox_worker import VoicevoxWorker

from character.character_display import CharacterDisplay
from character.character_state import CharacterState

from chat.chat_manager import ChatManager
from chat.chat_window import ChatWindow
from chat.message import Message

from config.logger import get_logger
from config.settings_manager import SettingsManager

import shutil
from pathlib import Path

logger = get_logger(__name__)


class AIMateApp:

    def __init__(self):

        self.gemini_thread = QThread()
        self.voice_thread = QThread()

        self.gemini = GeminiClient()

        self.worker = GeminiWorker(
            self.gemini
        )

        self.worker.moveToThread(
            self.gemini_thread
        )

        self.gemini_thread.started.connect(
            self.worker.run
        )

        self.worker.finished.connect(
            self.on_ai_response,
            Qt.ConnectionType.QueuedConnection
        )

        self.worker.error.connect(
            self.on_ai_error,
            Qt.ConnectionType.QueuedConnection
        )

        self.worker.finished.connect(
            self.gemini_thread.quit
        )
        self.worker.error.connect(
            self.gemini_thread.quit
        )

        self.settings_manager = SettingsManager()

        self.voicevox_engine = VoiceVoxEngine()

        try:
            self.voicevox_engine.start()
        except Exception:
            logger.exception(
                "VOICEVOX Engine起動失敗"
            )
            raise

        self.voicevox = VoicevoxClient(
            self.settings_manager.get_voicevox_settings()
        )

        self.audio_player = AudioPlayer()

        self.voice_worker = VoicevoxWorker(
            self.voicevox
        )

        self.voice_worker.moveToThread(
            self.voice_thread
        )

        self.voice_thread.started.connect(
            self.voice_worker.run
        )

        self.voice_worker.finished.connect(
            self.audio_player.play_file,
            Qt.ConnectionType.QueuedConnection
        )

        self.voice_worker.error.connect(
            self.on_voice_error,
            Qt.ConnectionType.QueuedConnection
        )

        self.voice_worker.finished.connect(
            self.voice_thread.quit
        )

        self.audio_player.finished.connect(
            self.on_voice_finished
        )

        self.chat = ChatWindow()

        self.gifs = {
            CharacterState.IDLE: "assets/idle.gif",
            CharacterState.THINKING: "assets/thinking.gif",
            CharacterState.TALKING: "assets/talking.gif",
        }

        self.character = CharacterDisplay(
            self.gifs
        )

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

        logger.info(
            f"Character state changed: {state}"
        )

    def on_message_sent(self, text):

        if self.is_processing:
            print("処理中のため送信停止")
            return

        self.is_processing = True

        user_message = self.chat_manager.create_user_message(text)
        self.chat.add_message(user_message)

        self.character.change_state(
            CharacterState.THINKING
        )

        self.worker.set_history(
            self.chat_manager.get_history()
        )

        self.gemini_thread.start()


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

    def start_voice(self, text):

        if self.voice_thread.isRunning():
            print("VOICEVOX実行中")
            return

        self.voice_worker.set_text(text)

        self.voice_thread.start()

    def on_voice_finished(self):

        print("voice finished")

        self.is_processing = False

        self.character.change_state(
            CharacterState.IDLE
        )

    def on_ai_error(self, error_message):

        self.is_processing = False

        error = Message(
            sender="AI",
            text=error_message,
            timestamp=datetime.now()
        )

        self.chat.add_message(error)

        self.character.change_state(
            CharacterState.IDLE
        )

    def on_voice_error(self, error_message):

        print(
            "VOICEVOX ERROR:",
            error_message
        )

        self.is_processing = False

        self.character.change_state(
            CharacterState.IDLE
        )

    def exit_application(self):

        if self.gemini_thread.isRunning():
            self.gemini_thread.quit()
            self.gemini_thread.wait()

        if self.voice_thread.isRunning():
            self.voice_thread.quit()
            self.voice_thread.wait()

        self.voicevox_engine.stop()

        self.chat.close()
        self.character.close()

        temp_dir = Path("temp")

        if temp_dir.exists():
            shutil.rmtree(temp_dir)

        QApplication.quit()

    def stop(self):

        if self.gemini_thread.isRunning():
            self.gemini_thread.quit()
            self.gemini_thread.wait()

        if self.voice_thread.isRunning():
            self.voice_thread.quit()
            self.voice_thread.wait()

        self.voicevox_engine.stop()

        # 一時音声ファイル削除
        temp_dir = Path("temp")

        if temp_dir.exists():
            shutil.rmtree(temp_dir)