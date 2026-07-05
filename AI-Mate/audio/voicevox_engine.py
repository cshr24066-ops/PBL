from pathlib import Path
import subprocess
import sys
import time

import requests

from config.logger import get_logger

logger = get_logger(__name__)


class VoiceVoxEngine:

    def __init__(self):

        self.process = None
        self.started_by_app = False

        # -----------------------------
        # 実行場所を取得
        # -----------------------------
        if getattr(sys, "frozen", False):
            # PyInstaller(one-folder)
            self.base_path = Path(sys.executable).parent
        else:
            # 開発環境
            self.base_path = Path(__file__).resolve().parent.parent

        # engine/run.exe
        self.engine_path = (
            self.base_path /
            "engine" /
            "run.exe"
        )

    def is_running(self):
        try:
            res = requests.get(
                "http://127.0.0.1:50021/version",
                timeout=1
            )
            return res.status_code == 200
        except requests.RequestException:
            return False
        
    def start(self):
        """
        VOICEVOX Engineを起動
        """

        if self.is_running():

            logger.info(
                "VOICEVOX Engineは既に起動しています。"
            )

            self.started_by_app = False
            return

        if not self.engine_path.exists():

            raise FileNotFoundError(
                f"VOICEVOX Engineが見つかりません。\n"
                f"{self.engine_path}"
            )

        logger.info(
            "VOICEVOX Engineを起動します。"
        )
        self.process = subprocess.Popen(
            [str(self.engine_path)],
            cwd=str(self.engine_path.parent)
        )
        time.sleep(2)  # ★追加（超重要：起動猶予）
        self.started_by_app = True

        self.wait_until_ready()

        logger.info(
            "VOICEVOX Engineの起動が完了しました。"
        )

    def wait_until_ready(self, timeout=30):

        start = time.time()

        while time.time() - start < timeout:

            if self.process is not None:

                code = self.process.poll()

                if code is not None:
                    raise RuntimeError(
                        f"VOICEVOX Engineが終了しました (exit code={code})"
                    )

            if self.is_running():
                return

            time.sleep(1)

        raise TimeoutError("VOICEVOX起動タイムアウト")
    def stop(self):
        """
        AI Mateが起動したEngineのみ終了
        """

        if not self.started_by_app:
            return

        if self.process is None:
            return

        try:

            self.process.terminate()
            self.process.wait(timeout=5)

            logger.info(
                "VOICEVOX Engineを終了しました。"
            )

        except subprocess.TimeoutExpired:

            self.process.kill()

            logger.warning(
                "VOICEVOX Engineを強制終了しました。"
            )