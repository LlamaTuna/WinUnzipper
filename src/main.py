from PyQt6.QtWidgets import QApplication
from gui import GUI
import sys


def main():
    app = QApplication(sys.argv)

    gui = GUI()
    gui.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
