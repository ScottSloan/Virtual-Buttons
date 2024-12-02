from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QPointF, QRectF, Qt, QLineF
from PySide6.QtGui import QPainter
from enum import Enum
import ctypes

from utils.key import PressKey, ReleaseKey
from utils.map import key_map
from utils.config import Config, ConfigUtils
from utils.data_type import JoyStickInfo

class Direction(Enum):
    Up = 1
    Left_Up = 2
    Left = 3
    Left_Down = 4
    Down = 5
    Right_Down = 6
    Right = 7
    Right_Up = 8

class Joystick(QWidget):
    def __init__(self, info: JoyStickInfo):
        self.info = info

        super().__init__()

        self.init_UI()

        self.movingOffset = QPointF(0, 0)
        self.grabCenter = False
        self.__maxDistance = self.info.inner_size["x"]
        self.last_direction = None
        self.last_key_list = []
        self.press = False
        self.prev_mouse_position = None

        self.init_utils()

    def init_UI(self):
        self.setGeometry(self.info.pos["x"], self.info.pos["y"], self.info.outer_size["x"], self.info.outer_size["y"])

        self.setWindowOpacity(self.info.alpha)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)

        self.set_no_active()

    def init_utils(self):
        self.in_editing = False

        self.config_utils = ConfigUtils()

    def paintEvent(self, event):
        painter = QPainter(self)
        bounds = QRectF(-self.__maxDistance, -self.__maxDistance, self.__maxDistance * 2, self.__maxDistance * 2).translated(self._center())
        painter.drawEllipse(bounds)
        painter.setBrush(Qt.black)
        painter.drawEllipse(self._centerEllipse())

    def _centerEllipse(self):
        if self.grabCenter:
            return QRectF(-20, -20, 40, 40).translated(self.movingOffset)

        return QRectF(-20, -20, 40, 40).translated(self._center())

    def _center(self):
        return QPointF(self.width()/2, self.height()/2)

    def _boundJoystick(self, point):
        limitLine = QLineF(self._center(), point)

        if (limitLine.length() > self.__maxDistance):
            limitLine.setLength(self.__maxDistance)

        return limitLine.p2()

    def joystickDirection(self):
        if not self.grabCenter:
            return 0

        normVector = QLineF(self._center(), self.movingOffset)
        #currentDistance = normVector.length()
        angle = normVector.angle()

        #distance = min(currentDistance / self.__maxDistance, 1.0)

        if 22.5 <= angle < 67.5:
            return Direction.Right_Up

        elif 67.5 <= angle < 112.5:
            return Direction.Up
        
        elif 112.5 <= angle < 157.5:
            return Direction.Left_Up

        elif 157.5 <= angle < 202.5:
            return Direction.Left
        
        elif 202.5 <= angle < 247.5:
            return Direction.Left_Down
        
        elif 247.5 <= angle < 292.5:
            return Direction.Down
        
        elif 292.5 <= angle < 337.5:
            return Direction.Right_Down
        else:
            return Direction.Right

    def mousePressEvent(self, event):
        self.press = True

        match Config.current_mode:
            case 0:
                self.grabCenter = self._centerEllipse().contains(event.pos())

            case 1:
                self.prev_mouse_position = event.pos()

            case 2:
                if not self.in_editing:
                    # _set_border()

                    if Config.last_edit_window:
                        Config.last_edit_window.close()
                        Config.last_edit_window = None

                    # Config.last_edit_window = EditWindow(self.info, _get_callback())
                    # Config.last_edit_window.show()
                        
                self.in_editing = not self.in_editing

    def mouseReleaseEvent(self, event):
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
                self.grabCenter = False
                self.movingOffset = QPointF(0, 0)
                self.update()

                for key in self.last_key_list:
                    ReleaseKey(key_map[key])

                self.last_direction  = None
                self.last_key_list = []
            
            case 1:
                self.prev_mouse_position = None

                self.config_utils.update_config_kwargs(self.info.id, **_get_kwargs())

                self.update_config_json()

    def mouseMoveEvent(self, event):
        match Config.current_mode:
            case 0:
                if self.grabCenter:
                    self.movingOffset = self._boundJoystick(event.pos())
                    self.update()
                
                self.get_direction()
            
            case 1:
                if self.press and self.prev_mouse_position:
                    delta = event.pos() - self.prev_mouse_position

                    self.move(self.pos() + delta)

    def get_direction(self):
        direction = self.joystickDirection()

        if direction == self.last_direction:
            pass
        else:
            for key in self.last_key_list:
                ReleaseKey(key_map[key])

            match direction:
                case Direction.Up:
                    self.last_key_list = ["UP"]

                case Direction.Down:
                    self.last_key_list = ["DOWN"]

                case Direction.Left:
                    self.last_key_list = ["LEFT"]

                case Direction.Right:
                    self.last_key_list = ["RIGHT"]

                case Direction.Left_Up:
                    self.last_key_list = ["LEFT", "UP"]

                case Direction.Left_Down:
                    self.last_key_list = ["LEFT", "DOWN"]
                
                case Direction.Right_Up:
                    self.last_key_list = ["RIGHT", "UP"]

                case Direction.Right_Down:
                    self.last_key_list = ["RIGHT", "DOWN"]

            for key in self.last_key_list:
                PressKey(key_map[key])

        self.last_direction = direction

    def set_no_active(self):
        WS_EX_NOACTIVATE = 0x08000000
        GWL_EXSTYLE = -20

        hwnd = self.winId()
        current_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, current_style | WS_EX_NOACTIVATE)

    def update_config_json(self):
        joystick_info = JoyStickInfo()
        joystick_info.load_from_dict(self.config_utils.get_control_config(self.info.id))

        self.info = joystick_info
