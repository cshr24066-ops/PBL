from datetime import datetime

from chat.message import Message


class ChatManager:

    def __init__(self):

        self.messages = []

    def send(self, text: str):

        text = text.strip()

        if not text:
            return False

        message = Message(
            sender="ユーザー",
            text=text,
            timestamp=datetime.now()
        )

        self.messages.append(message)

        return True

    def get_history(self):

        return self.messages