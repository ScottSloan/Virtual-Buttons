import random
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import QMetaObject, Slot, Qt
from PySide6.QtGui import QGuiApplication

from utils.config import Config, ConfigUtils
from utils.data_type import ButtonInfo, JoyStickInfo

from gui.button import Button
from gui.joystick import Joystick

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Virtual Buttons")

        self.init_UI()

        self.init_utils()

    def init_UI(self):
        self.load_config_btn = QPushButton("读取配置", self)
        self.load_config_btn.setObjectName("load_config_btn")
        self.load_config_btn.setFixedSize(100, 30)
        self.add_button_btn = QPushButton("添加按钮", self)
        self.add_button_btn.setObjectName("add_button_btn")
        self.add_button_btn.setFixedSize(100, 30)
        self.add_joystick_btn = QPushButton("添加摇杆", self)
        self.add_joystick_btn.setObjectName("add_joystick_btn")
        self.add_joystick_btn.setFixedSize(100, 30)

        hbox = QHBoxLayout()
        hbox.addWidget(self.load_config_btn, 0)
        hbox.addWidget(self.add_button_btn, 0)
        hbox.addWidget(self.add_joystick_btn, 0)

        self.normal_btn = QPushButton("正常", self)
        self.normal_btn.setObjectName("normal_btn")
        self.normal_btn.setCheckable(True)
        self.normal_btn.setChecked(True)
        self.move_btn = QPushButton("移动", self)
        self.move_btn.setObjectName("move_btn")
        self.move_btn.setCheckable(True)
        self.edit_btn = QPushButton("编辑", self)
        self.edit_btn.setObjectName("edit_btn")
        self.edit_btn.setCheckable(True)

        action_hbox = QHBoxLayout()
        action_hbox.addWidget(self.normal_btn, 0)
        action_hbox.addWidget(self.move_btn, 0)
        action_hbox.addWidget(self.edit_btn, 0)

        ver_lab = QLabel(f"Version: {Config.version}")

        vbox = QVBoxLayout()
        vbox.addLayout(hbox, 0)
        vbox.addLayout(action_hbox, 0)
        vbox.addWidget(ver_lab, 0)

        self.setLayout(vbox)

        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint)

        QMetaObject.connectSlotsByName(self)
    
    def init_utils(self):
        self.temp = []

        self.config_utils = ConfigUtils()

    def showEvent(self, event):
        super().showEvent(event)

        screen = QGuiApplication.primaryScreen()
        
        self.screen_width = screen.size().width()
        self.screen_height = screen.size().height()

    @Slot()
    def on_load_config_btn_clicked(self):
        def _clear():
            for button in self.temp:
                button.close()

            self.temp = []
        
        _clear()

        for entry in self.config_utils._read_config_json().values():
            if "key" in entry:
                button_info = ButtonInfo()
                button_info.load_from_dict(entry)

                self.create_button(button_info)

            else:
                joystick_info = JoyStickInfo()
                joystick_info.load_from_dict(entry)

                self.create_joystick(joystick_info)

    @Slot()
    def on_add_button_btn_clicked(self):
        def _get_pos():
            return {
                "x": int((self.screen_width - 72) / 2),
                "y": int((self.screen_height - 72) / 2)
            }
        
        def _get_size():
            return {
                "x": 72,
                "y": 72
            }

        button_info = ButtonInfo()
        button_info.id = random.randint(10000000, 99999999)
        button_info.name = "Button"
        button_info.alpha = 0.7
        button_info.text_color = "#FFFFFF"
        button_info.background_color = "#1E1E1E"
        button_info.size = _get_size()
        button_info.pos = _get_pos()

        self.create_button(button_info)

        self.config_utils.add_entry(button_info)
    
    @Slot()
    def on_add_joystick_btn_clicked(self):
        def _get_pos():
            return {
                "x": int((self.screen_width - 72) / 2),
                "y": int((self.screen_height - 72) / 2)
            }
        
        def _get_outer_size():
            return {
                "x": 160,
                "y": 160
            }
        
        def _get_inner_size():
            return {
                "x": 65,
                "y": 65
            }

        joystick_info = JoyStickInfo()
        joystick_info.id = random.randint(10000000, 99999999)
        joystick_info.alpha = 0.7
        joystick_info.outer_size = _get_outer_size()
        joystick_info.inner_size = _get_inner_size()
        joystick_info.pos = _get_pos()

        self.create_joystick(joystick_info)

        self.config_utils.add_entry(joystick_info)

    @Slot()
    def on_normal_btn_clicked(self):
        if self.normal_btn.isChecked():
            Config.current_mode = 0

            self.move_btn.setChecked(False)
            self.edit_btn.setChecked(False)

            self.close_edit_window()
        else:
            self.normal_btn.setChecked(True)

    @Slot()
    def on_move_btn_clicked(self):
        if self.move_btn.isChecked():
            Config.current_mode = 1

            self.normal_btn.setChecked(False)
            self.edit_btn.setChecked(False)

            self.close_edit_window()
        else:
            self.move_btn.setChecked(True)

    @Slot()
    def on_edit_btn_clicked(self):
        if self.edit_btn.isChecked():
            Config.current_mode = 2

            self.normal_btn.setChecked(False)
            self.move_btn.setChecked(False)
        else:
            self.edit_btn.setChecked(True)

    def create_button(self, info: ButtonInfo):
        btn = Button(info)
        btn.setAttribute(Qt.WA_AcceptTouchEvents, True)
        btn.installEventFilter(btn)
        btn.show()

        self.temp.append(btn)

    def create_joystick(self, info: JoyStickInfo):
        joy = Joystick(info)
        joy.show()

        self.temp.append(joy)

    def close_edit_window(self):
        if Config.last_edit_window:
            Config.last_edit_window.close()
