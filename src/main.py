from PyQt6.QtWidgets import QApplication
from gui import GUI
import sys

def main():
    # Create a new instance of the QApplication
    app = QApplication(sys.argv)

    # Create a new instance of the GUI and display it
    gui = GUI()
    gui.show()

    # Run the application's main loop and exit with its return value
    sys.exit(app.exec())

# Check if the script is being run as the main module
if __name__ == "__main__":
    main()
