from ai.gemini_client import GeminiClient


client = GeminiClient()

reply = client.generate("こんにちは！自己紹介してください。")

print(reply)