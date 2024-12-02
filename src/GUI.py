import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from gui.main import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setFont(QFont("微软雅黑"))

    main_window = MainWindow(None)
    main_window.show()

    sys.exit(app.exec())
