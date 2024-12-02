from PySide6.QtWidgets import QListWidget, QHBoxLayout, QDialog, QStyledItemDelegate, QLabel, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QMessageBox, QScroller
from PySide6.QtCore import Slot, QMetaObject, Qt

class ItemDelegate(QStyledItemDelegate):
    def __int__(self, parent):
        super().__init__(parent)

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(35)

        return size

class KeyWindow(QDialog):
    def __init__(self, parent, key, callback):
        self.key, self.callback = key, callback

        super().__init__(parent)

        self.setWindowTitle("设置按键")

        self.init_UI()

    def init_UI(self):
        key_to_add = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "LCtrl", "RCtrl", "LAlt", "RAlt", "LShift", "RShift", "Esc", "Tab", "Backspace", "Enter", "Space", "CapsLock", "Home", "End", "Pause", "Insert", "Delete", "PageUp", "PageDown", "UP", "DOWN", "LEFT", "RIGHT", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]

        key_lab = QLabel("已添加")

        self.key_list = QListWidget(self)
        self.key_list.setItemDelegate(ItemDelegate(self))
        self.key_list.addItems(self.key)

        scroller = QScroller.scroller(self.key_list)
        scroller.grabGesture(self.key_list.viewport(), QScroller.ScrollerGestureType.LeftMouseButtonGesture)
        self.key_list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)

        self.delete_btn = QPushButton("删除按键")
        self.delete_btn.setObjectName("delete_btn")

        key_vbox = QVBoxLayout()
        key_vbox.addWidget(key_lab)
        key_vbox.addWidget(self.key_list)
        key_vbox.addWidget(self.delete_btn)

        key_to_add_lab = QLabel("按键列表")

        self.key_to_add_list = QListWidget(self)
        self.key_to_add_list.setItemDelegate(ItemDelegate(self))
        self.key_to_add_list.addItems(key_to_add)

        scroller = QScroller.scroller(self.key_to_add_list)
        scroller.grabGesture(self.key_to_add_list.viewport(), QScroller.ScrollerGestureType.LeftMouseButtonGesture)
        self.key_to_add_list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)

        self.add_key_btn = QPushButton("添加按键")
        self.add_key_btn.setObjectName("add_key_btn")

        key_to_add_vbox = QVBoxLayout()
        key_to_add_vbox.addWidget(key_to_add_lab)
        key_to_add_vbox.addWidget(self.key_to_add_list)
        key_to_add_vbox.addWidget(self.add_key_btn)

        hbox = QHBoxLayout()
        hbox.addLayout(key_vbox)
        hbox.addLayout(key_to_add_vbox)

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
        vbox.addLayout(hbox)
        vbox.addLayout(bottom_hbox)

        self.setLayout(vbox)

        QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_add_key_btn_clicked(self):
        item = self.key_to_add_list.currentItem()

        if item:
            if self.key_list.findItems(item.text(), Qt.MatchFlag.MatchExactly):
                QMessageBox.warning(self, "警告", "按键已经添加")
                return

            self.key_list.addItem(item.text())

    @Slot()
    def on_delete_btn_clicked(self):
        item = self.key_list.currentItem()

        if item:
            self.key_list.takeItem(self.key_list.row(item))

    @Slot()
    def on_ok_btn_clicked(self):
        items = [self.key_list.item(i).text() for i in range(self.key_list.count())]

        self.close()

        self.callback(items)

    @Slot()
    def on_cancel_btn_clicked(self):
        self.close()
