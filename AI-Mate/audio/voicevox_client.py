import requests


class VoicevoxClient:

    def __init__(self, settings):

        self.settings = settings

        self.base_url = (
            "http://localhost:50021"
        )


    def create_audio(
        self,
        text,
        speaker=None
    ):

        if speaker is None:
            speaker = self.settings["speaker"]


        # 音声合成用パラメータ作成
        query_response = requests.post(
            f"{self.base_url}/audio_query",
            params={
                "text": text,
                "speaker": speaker
            }
        )

        query_response.raise_for_status()


        # 音声合成
        synthesis_response = requests.post(
            f"{self.base_url}/synthesis",
            params={
                "speaker": speaker
            },
            json=query_response.json()
        )

        synthesis_response.raise_for_status()


        filename = "voice.wav"

        with open(
            filename,
            "wb"
        ) as f:

            f.write(
                synthesis_response.content
            )


        return filename