from pathlib import Path
import json
import sys


class SettingsManager:

    def __init__(self):

        if getattr(sys, "frozen", False):
            base_dir = Path(sys.executable).parent
        else:
            base_dir = Path(__file__).resolve().parent.parent

        self.base_dir = base_dir

        self.config_dir = self.base_dir / "config"
        self.settings_file = self.config_dir / "settings.json"

        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.settings = self.load_settings()

    def load_settings(self):

        if not self.settings_file.exists():

            default = {
                "character": {
                    "x": 100,
                    "y": 100
                },
                "voicevox": {
                    "speaker": 3
                }
            }

            self.save_settings(default)
            return default

        with open(self.settings_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_settings(self, settings=None):

        if settings is None:
            settings = self.settings

        self.settings_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(
                settings,
                f,
                indent=4,
                ensure_ascii=False
            )

    # ----------------------------
    # Character
    # ----------------------------

    def get_character_position(self):

        return (
            self.settings["character"]["x"],
            self.settings["character"]["y"]
        )

    def save_character_position(self, x, y):

        self.settings["character"]["x"] = x
        self.settings["character"]["y"] = y

        self.save_settings()

    # ----------------------------
    # VoiceVox
    # ----------------------------

    def get_voicevox_settings(self):

        return self.settings["voicevox"]