import ctypes
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QMouseEvent, QPalette

from utils.data_type import ButtonInfo, EditCallback
from utils.config import Config, ConfigUtils
from utils.key import PressKey, ReleaseKey
from utils.map import key_map

from gui.edit_btn import EditWindow

class Button(QWidget):
    def __init__(self, info: ButtonInfo = None):
        self.info = info

        super().__init__()

        self.setWindowTitle(self.info.name)

        self.init_UI()

        self.init_utils()

        self.set_no_active()

        self.press = False

    def init_UI(self):
        self.setGeometry(self.info.pos["x"], self.info.pos["y"], self.info.size["x"], self.info.size["y"])

        self.name_lab = QLabel(self.info.name, self)
        self.name_lab.setObjectName("name_lab")
        self.name_lab.setAlignment(Qt.AlignCenter)
        self.name_lab.setPalette(self.get_palette(QPalette.ColorRole.WindowText, self.info.text_color))

        vbox = QVBoxLayout()
        vbox.addWidget(self.name_lab, 0)
        vbox.setContentsMargins(1, 1, 1, 1)

        self.setLayout(vbox)

        self.setWindowOpacity(self.info.alpha)
        self.setPalette(self.get_palette(QPalette.ColorRole.Window, self.info.background_color))

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)

    def eventFilter(self, obj, event: QEvent):
        if event.type() == QEvent.Type.TouchBegin:
            Config.touch_screen = True
            self.onTouchBegin(event.touchPoints()[0].pos().toPoint())
            return True
        
        if event.type() == QEvent.Type.TouchUpdate:
            self.onTouchUpdate(event.touchPoints()[0].pos().toPoint())
            return True

        elif event.type() == QEvent.Type.TouchEnd:
            self.onTouchEnd(event)
            return True

        return super(Button, self).eventFilter(obj, event)
    
    def mousePressEvent(self, event: QMouseEvent):
        Config.touch_screen = False

        if event.button() == Qt.LeftButton:
            self.onTouchBegin(event.pos())

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.onTouchEnd(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        self.onTouchUpdate(event.pos())

    def onTouchEnd(self, event):
        def _get_kwargs():
            kwargs = {
                "pos": {
                    "x": self.x(),
                    "y": self.y(),
                }
            }

            return kwargs
        
        self.press = False

        match Config.current_mode:
            case 0:
                for _key in self.info.key:
                    ReleaseKey(key_map[_key])

            case 1:
                self.prev_mouse_position = None

                self.config_utils.update_config_kwargs(self.info.id, **_get_kwargs())

                self.update_config_json()
    
    def onTouchBegin(self, pos):
        def update_callback(kwargs = None):
            self.config_utils.update_config_kwargs(self.info.id, **kwargs)

            self.update_config_json()

            _reset()
        
        def rename_callback(name: str):
            self.name_lab.setText(name)

        def resize_callback(value: int):
            self.resize(value, value)

        def realpha_callback(alpha: float):
            self.setWindowOpacity(alpha)

        def restore_callback():
            self.name_lab.setText(self.info.name)
            self.resize(self.info.size["x"], self.info.size["y"])
            self.setWindowOpacity(self.info.alpha)
            self.name_lab.setPalette(self.get_palette(QPalette.ColorRole.WindowText, self.info.text_color))
            self.setPalette(self.get_palette(QPalette.ColorRole.Window, self.info.background_color))

            _reset()

        def delete_callback():
            self.config_utils.delete_control_config(self.info.id)

            self.close()

        def text_color_callback(color: str):
            self.name_lab.setPalette(self.get_palette(QPalette.ColorRole.WindowText, color))

        def background_color_callback(color: str):
            self.setPalette(self.get_palette(QPalette.ColorRole.Window, color))

        def _get_callback():
            callback = EditCallback()
            callback.update_callback = update_callback
            callback.rename_callback = rename_callback
            callback.resize_callback = resize_callback
            callback.realpha_callback = realpha_callback
            callback.restore_callback = restore_callback
            callback.delete_callback = delete_callback
            callback.text_color_callback = text_color_callback
            callback.background_callback = background_color_callback

            return callback

        def _set_border():
            self.setStyleSheet("""border: 1px solid red;""")

        def _reset():
            self.setStyleSheet("")

            self.in_editing = False
            Config.last_edit_window = None

        self.press = True

        match Config.current_mode:
            case 0:
                for _key in self.info.key:
                    PressKey(key_map[_key])

            case 1:
                self.prev_mouse_position = pos

            case 2:
                if not self.in_editing:
                    _set_border()

                    if Config.last_edit_window:
                        Config.last_edit_window.close()
                        Config.last_edit_window = None

                    Config.last_edit_window = EditWindow(self.info, _get_callback())
                    Config.last_edit_window.show()
                        
                self.in_editing = not self.in_editing
    
    def onTouchUpdate(self, pos):
        match Config.current_mode:
            case 1:
                if self.press and self.prev_mouse_position:
                    delta = pos - self.prev_mouse_position

                    self.move(self.pos() + delta)
    
    def init_utils(self):
        self.in_editing = False

        self.config_utils = ConfigUtils()

    def update_config_json(self):
        button_info = ButtonInfo()
        button_info.load_from_dict(self.config_utils.get_control_config(self.info.id))

        self.info = button_info
    
    def set_no_active(self):
        WS_EX_NOACTIVATE = 0x08000000
        GWL_EXSTYLE = -20

        hwnd = self.winId()
        current_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, current_style | WS_EX_NOACTIVATE)

    def get_palette(self, role: QPalette.ColorRole, color: str):
        palette = QPalette()
        palette.setColor(role, color)

        return palette