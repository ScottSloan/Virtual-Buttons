from PySide6.QtWidgets import QDialog, QLabel, QColorDialog, QPushButton, QFormLayout, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import QMetaObject, Slot
from PySide6.QtGui import QPalette

from utils.data_type import ButtonInfo, ColorCallback

class ColorWindow(QDialog):
    def __init__(self, parent, info: ButtonInfo, callback: ColorCallback):
        self.info, self.callback = info, callback

        super().__init__(parent)

        self.setWindowTitle("设置颜色")

        self.init_UI()

    def init_UI(self):
        text_color_lab = QLabel("文本颜色")
        self.text_color_set_btn = QPushButton("")
        self.text_color_set_btn.setObjectName("text_color_set_btn")
        self.text_color_set_btn.setFixedSize(80, 30)
        self.text_color_set_btn.setPalette(self.get_palette(self.info.text_color))
        self.text_color_lab = QLabel(self.info.text_color)

        text_color_hbox = QHBoxLayout()
        text_color_hbox.addWidget(self.text_color_set_btn)
        text_color_hbox.addWidget(self.text_color_lab)

        background_color_lab = QLabel("背景颜色")
        self.background_color_set_btn = QPushButton("")
        self.background_color_set_btn.setObjectName("background_color_set_btn")
        self.background_color_set_btn.setFixedSize(80, 30)
        self.background_color_set_btn.setPalette(self.get_palette(self.info.background_color))
        self.background_color_lab = QLabel(self.info.background_color)

        background_color_hbox = QHBoxLayout()
        background_color_hbox.addWidget(self.background_color_set_btn)
        background_color_hbox.addWidget(self.background_color_lab)

        form_vbox = QFormLayout()
        form_vbox.addRow(text_color_lab, text_color_hbox)
        form_vbox.addRow(background_color_lab, background_color_hbox)

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
        vbox.addLayout(form_vbox)
        vbox.addSpacing(10)
        vbox.addLayout(bottom_hbox)

        self.setLayout(vbox)

        QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_text_color_set_btn_clicked(self):
        color = self.get_color(self.info.text_color)

        self.text_color_set_btn.setPalette(self.get_palette(color))
        self.text_color_lab.setText(color)
        self.info.text_color = color

        self.callback.text_color_callback(color)

    @Slot()
    def on_background_color_set_btn_clicked(self):
        color = self.get_color(self.info.background_color)

        self.background_color_set_btn.setPalette(self.get_palette(color))
        self.background_color_lab.setText(color)
        self.info.background_color = color

        self.callback.background_color_callback(color)

    @Slot()
    def on_ok_btn_clicked(self):
        def _get_kwargs():
            return {
                "text_color": self.info.text_color,
                "background_color": self.info.background_color
            }

        self.callback.update_callback(_get_kwargs())

        self.close()

    @Slot()
    def on_cancel_btn_clicked(self):
        self.close()

    def get_color(self, initial: str):
        dlg = QColorDialog(initial, self)
        dlg.exec()

        return dlg.currentColor().name().upper()
    
    def get_palette(self, color: str):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Button, color)

        return palette