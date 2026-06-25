import json
from pathlib import Path


class SettingsManager:

    DEFAULT_SETTINGS = {
        "gemini_api_key": "",
        "volume": 0.8,
        "character_x": 100,
        "character_y": 100
    }

    def __init__(self):

        self.settings_file = Path(
            "config/settings.json"
        )

    def load_settings(self):

        if not self.settings_file.exists():

            self.save_settings(
                self.DEFAULT_SETTINGS
            )

            return self.DEFAULT_SETTINGS

        try:

            with open(
                self.settings_file,
                "r",
                encoding="utf-8"
            ) as file:

                settings = json.load(file)

            return settings

        except (
            json.JSONDecodeError,
            OSError
        ):

            return self.DEFAULT_SETTINGS

    def save_settings(self, settings: dict):

        with open(
            self.settings_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                settings,
                file,
                indent=4,
                ensure_ascii=False
            )