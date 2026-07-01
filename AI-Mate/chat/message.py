from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:

    sender: str
    text: str
    timestamp: datetime