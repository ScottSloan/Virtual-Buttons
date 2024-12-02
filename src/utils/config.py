import os
import json
from PySide6.QtWidgets import QWidget

from utils.data_type import ButtonInfo

class Config:
    version = "1.02"

    touch_screen = False

    current_mode = 0

    last_edit_window: QWidget = None

class ConfigUtils:
    def __init__(self):
        self.config_path = os.path.join(os.getcwd(), "data.json")

        self.config = self._read_config_json()

        if not os.path.exists(self.config_path):
            self._write_config_json(self.config)

    def add_entry(self, entry: ButtonInfo):
        self.config = self._read_config_json()

        self.config[str(entry.id)] = entry.to_dict()

        self._write_config_json(self.config)

    def update_config_kwargs(self, id: int, **kwargs):
        self.config = self._read_config_json()

        for key, value in kwargs.items():
            self.config[str(id)][key] = value

        self._write_config_json(self.config)

    def get_control_config(self, id: int):
        self.config = self._read_config_json()

        return self.config[str(id)]

    def delete_control_config(self, id: int):
        self.config = self._read_config_json()

        self.config.pop(str(id))

        self._write_config_json(self.config)

    def _read_config_json(self):
        try:
            with open(self.config_path, "r", encoding = "utf-8") as f:
                return json.loads(f.read())
            
        except Exception:
            return {}
    
    def _write_config_json(self, contents: dict):
        with open(self.config_path, "w", encoding = "utf-8") as f:
            f.write(json.dumps(contents, ensure_ascii = False, indent = 4))
