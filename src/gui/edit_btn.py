from PySide6.QtWidgets import QWidget, QFormLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem
from PySide6.QtCore import Slot, QMetaObject, Qt
from PySide6.QtGui import QCloseEvent, QGuiApplication
from typing import List

from utils.data_type import ButtonInfo, EditCallback, ColorCallback, ColorInfo

from gui.key import KeyWindow
from gui.color import ColorWindow

class EditWindow(QWidget):
    def __init__(self, info: ButtonInfo, callback: EditCallback):
        self.info = info
        self.callback = callback

        super().__init__()

        self.setWindowTitle("编辑")

        self.init_UI()

    def init_UI(self):
        name_lab = QLabel("名称", self)
        self.name_box = QLineEdit(self.info.name, self)
        self.name_box.setObjectName("name_box")

        size_lab = QLabel("大小", self)
        self.size_box = QLineEdit(str(self.info.size["x"]), self)
        self.size_box.setObjectName("size_box")
        self.size_plus_btn = QPushButton("+", self)
        self.size_plus_btn.setObjectName("size_plus_btn")
        self.size_plus_btn.setFixedSize(30, 30)
        self.size_mins_btn = QPushButton("-", self)
        self.size_mins_btn.setObjectName("size_mins_btn")
        self.size_mins_btn.setFixedSize(30, 30)

        size_hbox = QHBoxLayout()
        size_hbox.addWidget(self.size_box)
        size_hbox.addWidget(self.size_plus_btn)
        size_hbox.addWidget(self.size_mins_btn)

        alpha_lab = QLabel("透明度", self)
        self.alpha_box = QLineEdit(str(self.info.alpha), self)
        self.alpha_box.setObjectName("alpha_box")
        self.alpha_plus_btn = QPushButton("+", self)
        self.alpha_plus_btn.setObjectName("alpha_plus_btn")
        self.alpha_plus_btn.setFixedSize(30, 30)
        self.alpha_mins_btn = QPushButton("-", self)
        self.alpha_mins_btn.setObjectName("alpha_mins_btn")
        self.alpha_mins_btn.setFixedSize(30, 30)

        alpha_hbox = QHBoxLayout()
        alpha_hbox.addWidget(self.alpha_box)
        alpha_hbox.addWidget(self.alpha_plus_btn)
        alpha_hbox.addWidget(self.alpha_mins_btn)

        color_lab = QLabel("颜色", self)
        self.color_btn = QPushButton("设置", self)
        self.color_btn.setObjectName("color_btn")
        self.color_btn.setFixedSize(80, 30)
        self.delete_btn = QPushButton("删除控件", self)
        self.delete_btn.setObjectName("delete_btn")
        self.delete_btn.setFixedSize(100, 30)

        color_hbox = QHBoxLayout()
        color_hbox.addWidget(self.color_btn)
        color_hbox.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        color_hbox.addWidget(self.delete_btn)

        key_lab = QLabel("按键")
        self.key_box = QLineEdit(", ".join(self.info.key), self)
        self.key_box.setReadOnly(True)
        self.key_btn = QPushButton("设置", self)
        self.key_btn.setObjectName("key_btn")

        key_hbox = QHBoxLayout()
        key_hbox.addWidget(self.key_box, 0)
        key_hbox.addWidget(self.key_btn, 0)

        form_box = QFormLayout()
        form_box.addRow(name_lab, self.name_box)
        form_box.addRow(size_lab, size_hbox)
        form_box.addRow(alpha_lab, alpha_hbox)
        form_box.addRow(key_lab, key_hbox)
        form_box.addRow(color_lab, color_hbox)

        self.ok_btn = QPushButton("确定", self)
        self.ok_btn.setObjectName("ok_btn")
        self.ok_btn.setFixedSize(100, 35)
        self.cancel_btn = QPushButton("取消", self)
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.setFixedSize(100, 35)

        bottom_hbox = QHBoxLayout()
        bottom_hbox.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        bottom_hbox.addWidget(self.ok_btn)
        bottom_hbox.addWidget(self.cancel_btn)

        vbox = QVBoxLayout()
        vbox.addLayout(form_box)
        vbox.addSpacing(10)
        vbox.addLayout(bottom_hbox)

        self.setLayout(vbox)

        self.setWindowFlag(Qt.Tool | Qt.WindowStaysOnTopHint)

        QMetaObject.connectSlotsByName(self)

    def showEvent(self, event):
        super().showEvent(event)

        screen = QGuiApplication.primaryScreen()
        
        self.screen_width = screen.size().width()
        self.screen_height = screen.size().height()

        self.frame_width = self.frameGeometry().width()
        self.farme_height = self.frameGeometry().height()

        self.task_bar_height = self.screen_height - screen.availableSize().height()
        
        self.set_position(self.info.pos["x"] + self.info.size["x"] + 16, self.info.pos["y"])

        self.temp_text_color, self.temp_background_color = self.info.text_color, self.info.background_color
    
    def closeEvent(self, event: QCloseEvent):
        self.callback.restore_callback()

        event.accept()

    @Slot()
    def on_name_box_textChanged(self):
        self.callback.rename_callback(self.name_box.text())

    @Slot()
    def on_size_box_textChanged(self):
        value = self.size_box.text()

        if value:
            self.callback.resize_callback(int(value))

    @Slot()
    def on_alpha_box_textChanged(self):
        value = self.alpha_box.text()

        if value:
            self.callback.realpha_callback(float(value))

    @Slot()
    def on_size_plus_btn_clicked(self):
        value = int(self.size_box.text())

        self.size_box.setText(str(value + 4))

        self.resize(value)

    @Slot()
    def on_size_mins_btn_clicked(self):
        value = int(self.size_box.text())

        self.size_box.setText(str(value - 4))

        self.resize(value)

    @Slot()
    def on_alpha_plus_btn_clicked(self):
        value = float(self.alpha_box.text())
        result = round(value + 0.1, 1)

        if result == 1.0:
            self.alpha_plus_btn.setDisabled(True)
        else:
            self.alpha_mins_btn.setDisabled(False)

        self.alpha_box.setText(str(result))

        self.callback.realpha_callback(value)
    
    @Slot()
    def on_alpha_mins_btn_clicked(self):
        value = float(self.alpha_box.text())
        result = round(value - 0.1, 1)

        if result == 0.0:
            self.alpha_mins_btn.setDisabled(True)
        else:
            self.alpha_plus_btn.setDisabled(False)

        self.alpha_box.setText(str(result))

        self.callback.realpha_callback(value)

    @Slot()
    def on_key_btn_clicked(self):
        def callback(items: List[str]):
            self.key_box.setText(", ".join(items))

        key_window = KeyWindow(self, self.info.key, callback)
        key_window.exec()
    
    @Slot()
    def on_color_btn_clicked(self):
        def text_color_callback(color: str):
            self.callback.text_color_callback(color)

        def background_color_callback(color: str):
            self.callback.background_callback(color)

        def update_callback(kwargs: dict):
            self.temp_text_color = kwargs["text_color"]
            self.temp_background_color = kwargs["background_color"]

        def _get_info():
            info = ColorInfo()
            info.text_color = self.info.text_color
            info.background_color = self.info.background_color

            return info

        def _get_callback():
            callback = ColorCallback()
            callback.text_color_callback = text_color_callback
            callback.background_color_callback = background_color_callback
            callback.update_callback = update_callback

            return callback

        color_window = ColorWindow(self, _get_info(), _get_callback())
        color_window.exec()

    @Slot()
    def on_delete_btn_clicked(self):
        self.close()

        self.callback.delete_callback()

    @Slot()
    def on_ok_btn_clicked(self):
        def _get_kwargs():
            return {
                "name": self.name_box.text(),
                "alpha": float(self.alpha_box.text()),
                "key": self.key_box.text().split(", "),
                "text_color": self.temp_text_color,
                "background_color": self.temp_background_color,
                "size": {
                    "x": int(self.size_box.text()),
                    "y": int(self.size_box.text())
                }
            }
        
        self.callback.update_callback(_get_kwargs())

        self.close()

    @Slot()
    def on_cancel_btn_clicked(self):
        self.callback.restore_callback()

        self.close()

    def resize(self, value: float):
        self.set_position(self.info.pos["x"] + value + 16, self.info.pos["y"])

        self.callback.resize_callback(value)

    def set_position(self, x: int, y: int):
        if y + self.farme_height > self.screen_height - self.task_bar_height:
            y = self.screen_height - self.farme_height - self.task_bar_height

        if x + self.frame_width > self.screen_width:
            x = self.info.pos["x"] - self.frame_width - 16
        
        self.move(x, y)
