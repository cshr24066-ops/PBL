import json
from pathlib import Path
from datetime import datetime

from chat.message import Message


class ChatManager:


    def __init__(self):

        self.messages = []

        self.history_file = Path(
            "data/chat_history.json"
        )
        self.history_file.parent.mkdir(
            exist_ok=True
        )

        self.load_history()


    def create_user_message(self, text):

        message = Message(
            sender="User",
            text=text,
            timestamp=datetime.now()
        )

        self.messages.append(message)

        self.save_history()

        return message


    def add_message(self,message):

        self.messages.append(message)

        if len(self.messages) > 50:
            self.messages.pop(0)

        self.save_history()


    def get_history(self):

        return self.messages


    def save_history(self):

        data = []

        for message in self.messages:

            data.append(
                {
                    "sender": message.sender,
                    "text": message.text,
                    "timestamp":
                        message.timestamp.isoformat()
                }
            )


        with open(
            self.history_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )


    def load_history(self):

        if not self.history_file.exists():
            return

        try:

            with open(
                self.history_file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)


            for item in data:

                self.messages.append(
                    Message(
                        sender=item["sender"],
                        text=item["text"],
                        timestamp=datetime.fromisoformat(
                            item["timestamp"]
                        )
                    )
                )

        except Exception as e:

            print(
                "履歴読み込み失敗:",
                e
            )