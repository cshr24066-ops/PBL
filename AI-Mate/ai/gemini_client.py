from google import genai
from dotenv import load_dotenv
import os


class GeminiClient:
    """Gemini APIとの通信を担当するクラス"""

    def __init__(self):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY が設定されていません。")

        self.client = genai.Client(api_key=api_key)

    def generate(self, history) -> str:

        contents = []

        for message in history:

            role = (
                "user"
                if message.sender == "User"
                else "model"
            )

            contents.append(
                {
                    "role": role,
                    "parts": [
                        {
                            "text": message.text
                        }
                    ]
                }
            )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
        )

        return response.text