from google import genai
from google.genai import types
from dotenv import load_dotenv
import os


class GeminiClient:
    """Gemini APIとの通信を担当するクラス"""

    SYSTEM_INSTRUCTION = """
あなたは『おいしんぼ』という作品の登場キャラクターである，海原雄山です。

以下の方針で応答してください。
・指定したキャラクターの口調で応答する
・必要以上に長い回答は避ける
"""

    def __init__(self):

        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY が設定されていません。"
            )

        self.client = genai.Client(
            api_key=api_key
        )


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
            config=types.GenerateContentConfig(
                system_instruction=self.SYSTEM_INSTRUCTION
            )
        )

        return response.text