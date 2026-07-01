from datetime import datetime
from chat.message import Message


class ChatManager:

    def __init__(self):

        self.messages = []

    def send(self, text):

        message = Message(

            sender="User",

            text=text,

            timestamp=datetime.now()

        )

        self.messages.append(message)

        return message
    
    def get_response(self):

        message = Message(

            sender="AI",

            text="現在AI機能は未実装です。",

            timestamp=datetime.now()

        )

        self.messages.append(message)

        return message
    
    def get_history(self):

        return self.messages