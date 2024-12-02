from typing import Callable

class ButtonInfo:
    def __init__(self):
        self.id: int = 0
        self.name: str = ""
        self.key: list = []
        self.alpha: float = 0
        self.text_color: str = ""
        self.background_color: str = ""
        self.size: dict = {}
        self.pos: dict = {}

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "key": self.key,
            "alpha": self.alpha,
            "text_color": self.text_color,
            "background_color": self.background_color,
            "size": self.size,
            "pos": self.pos
        }

    def load_from_dict(self, data: dict):
        self.id = data["id"]
        self.name = data["name"]
        self.key = data["key"]
        self.alpha = data["alpha"]
        self.text_color = data["text_color"]
        self.background_color = data["background_color"]
        self.size = data["size"]
        self.pos = data["pos"]

class JoyStickInfo:
    def __init__(self):
        self.id: int = 0
        self.alpha: float = 0
        self.outer_size: dict = {}
        self.inner_size: dict = {}
        self.pos: dict = {}

    def to_dict(self):
        return {
            "id": self.id,
            "alpha": self.alpha,
            "outer_size": self.outer_size,
            "inner_size": self.inner_size,
            "pos": self.pos
        }
    
    def load_from_dict(self, data: dict):
        self.id = data["id"]
        self.alpha = data["alpha"]
        self.outer_size = data["outer_size"]
        self.inner_size = data["inner_size"]
        self.pos = data["pos"]

class ColorInfo:
    def __init__(self):
        self.text_color: str = ""
        self.background_color: str = ""

class EditCallback:
    def __init__(self):
        self.update_callback: Callable = None
        self.rename_callback: Callable = None
        self.resize_callback: Callable = None
        self.realpha_callback: Callable = None
        self.restore_callback: Callable = None
        self.delete_callback: Callable = None

        self.text_color_callback: Callable = None
        self.background_callback: Callable = None

class ColorCallback:
    def __init__(self):
        self.text_color_callback: Callable = None
        self.background_color_callback: Callable = None
        self.update_callback: Callable = None
