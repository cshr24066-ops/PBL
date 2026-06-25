from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from chat.chat_manager import ChatManager


class ChatWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.chat_manager = ChatManager()

        self.setup_ui()

    def setup_ui(self):

        self.setWindowTitle("AI Mate Chat")

        self.resize(300, 250)
        
        layout = QVBoxLayout()

        self.history_area = QTextEdit()
        self.history_area.setReadOnly(True)

        self.input_box = QLineEdit()

        self.send_button = QPushButton("送信")

        self.send_button.clicked.connect(
            self.send_message
        )

        layout.addWidget(self.history_area)
        layout.addWidget(self.input_box)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def send_message(self):

        text = self.input_box.text()

        success = self.chat_manager.send(text)

        if not success:

            QMessageBox.warning(
                self,
                "入力エラー",
                "メッセージを入力してください"
            )

            return

        self.refresh_history()

        self.input_box.clear()

    def refresh_history(self):

        self.history_area.clear()

        for message in self.chat_manager.get_history():

            self.history_area.append(
                f"{message.sender}: {message.text}"
            )