import json
from pathlib import Path


class SettingsManager:

    def __init__(self):

        self.settings_file = Path(
            "config/settings.json"
        )

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


        with open(
            self.settings_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    def save_settings(self, settings=None):

        if settings is None:
            settings = self.settings


        with open(
            self.settings_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                settings,
                f,
                indent=4,
                ensure_ascii=False
            )


    def get_character_position(self):

        character = self.settings["character"]

        return (
            character["x"],
            character["y"]
        )


    def save_character_position(self, x, y):

        self.settings["character"]["x"] = x
        self.settings["character"]["y"] = y

        self.save_settings()


    def get_voicevox_settings(self):

        return self.settings["voicevox"]