from audio.voicevox_client import VoicevoxClient


voicevox = VoicevoxClient()

file = voicevox.create_audio(
    "こんにちは。AI Mateです。"
)

print(file)