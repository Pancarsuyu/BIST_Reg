from PyQt5.QtWidgets import QApplication
import sys
from ui import MyWindow

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    window()
