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

    def generate(self, message: str) -> str:
        """
        Geminiへメッセージを送信し、応答を取得する

        Parameters
        ----------
        message : str
            ユーザーからの入力

        Returns
        -------
        str
            Geminiの応答
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message,
        )

        return response.text