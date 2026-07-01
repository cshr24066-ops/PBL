from datetime import datetime
from chat.message import Message


class ChatManager:

    def __init__(self, max_history=10):

        self.messages = []

        self.max_history = max_history

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

        return self.messages[-self.max_history:]
    
        print(
            "Gemini送信履歴:",
            len(history)
        )

        return history