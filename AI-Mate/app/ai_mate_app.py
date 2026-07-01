from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from character.character_display import CharacterDisplay
from character.character_state import CharacterState
from chat.chat_window import ChatWindow
from config.settings_manager import SettingsManager
from chat.chat_manager import ChatManager


class AIMateApp:

    def __init__(self):

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
           self.send_message
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

        QTimer.singleShot(
            3000,
            lambda: self.character.change_state(
                CharacterState.THINKING
            )
        )

        QTimer.singleShot(
            6000,
            lambda: self.character.change_state(
                CharacterState.TALKING
            )
        )
    
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
    
    def send_message(self, text):

        user_message = self.chat_manager.send(text)

        self.chat.append_message(user_message)

        ai_message = self.chat_manager.get_response()

        self.chat.append_message(ai_message)
            
    def exit_application(self):

        self.chat.close()
        self.character.close()