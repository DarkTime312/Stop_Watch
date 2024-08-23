# main.py
from PySide6.QtWidgets import QApplication
import sys
from controller import StopWatchController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StopWatchController()
    window.view.show()
    sys.exit(app.exec())
