from pathlib import Path
from datetime import datetime

import requests
import shutil

class VoicevoxClient:

    def __init__(self, settings):

        self.settings = settings

        self.base_url = "http://localhost:50021"

        self.temp_dir = Path("temp")

        # 前回の一時フォルダを削除
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

        # 新しく作成
        self.temp_dir.mkdir()

        print("カレントディレクトリ:", Path.cwd())
        print("tempの絶対パス:", self.temp_dir.resolve())

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

        # 現在時刻を利用したファイル名
        filename = self.temp_dir / (
            datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".wav"
        )

        with open(
            filename,
            "wb"
        ) as f:

            f.write(
                synthesis_response.content
            )

        return str(filename)