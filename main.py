import sys
from PyQt6.QtWidgets import QApplication
from ParsingWindow import ParsingWindow

if __name__ == '__main__':
    app = QApplication([])
    pw = ParsingWindow()
    pw.show()

    sys.exit(app.exec())
