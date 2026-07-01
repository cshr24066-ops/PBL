from datetime import datetime
from chat.message import Message


class ChatManager:

    MAX_HISTORY = 10

    def __init__(self):
        self.messages = []


    def create_user_message(self, text):

        message = Message(
            sender="User",
            text=text,
            timestamp=datetime.now()
        )

        self.messages.append(message)

        return message


    def add_message(self, message):

        self.messages.append(message)


    def get_history(self):

        print(
        "送信履歴数:",
        len(self.messages[-self.MAX_HISTORY:])
        )


        return self.messages[-self.MAX_HISTORY:]