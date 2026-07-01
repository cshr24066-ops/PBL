from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
)

from PySide6.QtCore import Signal

from chat.input_text_edit import InputTextEdit

class ChatWindow(QWidget):
    
    send_requested = Signal(str)

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        self.setWindowTitle("AI Mate Chat")

        self.resize(300, 250)
        
        layout = QVBoxLayout()

        self.history_area = QTextEdit()
        self.history_area.setReadOnly(True)

        self.input_box = InputTextEdit()
        self.input_box.setMaximumHeight(70)

        self.send_button = QPushButton("送信")

        self.send_button.clicked.connect(
            self.on_send_button_clicked
        )


        layout.addWidget(self.history_area)
        layout.addWidget(self.input_box)
        layout.addWidget(self.send_button)

        self.setLayout(layout)


        self.input_box.send_requested.connect(
            self.send_requested.emit
        )

    def refresh_history(self, history):

        self.history_area.clear()

        for message in history:

            self.append_message(message)
            
    def append_message(self, message):

        self.history_area.append(
            f"{message.sender}: {message.text}"
        )
    
    def on_send_button_clicked(self):

        self.input_box.submit()