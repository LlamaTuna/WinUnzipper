from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QProgressBar, QTextBrowser, QLabel, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
import os
from unzip import Unzipper

class UnzipThread(QThread):
    # Define signals to send progress and log updates
    progress_signal = pyqtSignal(int)
    log_signal = pyqtSignal(str)

    def __init__(self, source_dir, dest_dir):
        super().__init__()
        # Initialize the unzipper with source and destination directories
        self.unzipper = Unzipper(source_dir, dest_dir)

    def run(self):
        # Run the unzipper's unzip method when thread is started
        self.unzipper.unzip(self.progress_signal, self.log_signal)

class GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'Unzipper GUI'
        self.initUI()

    def initUI(self):
        # Initialize the user interface
        self.setWindowTitle(self.title)

        # Create a vertical layout for the GUI components
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create and add button to select source directory
        self.btn_select_dir = QPushButton('Select directory to unzip', self)
        self.btn_select_dir.clicked.connect(self.select_directory)
        self.source_dir_label = QLabel(self)
        layout.addWidget(self.btn_select_dir)
        layout.addWidget(self.source_dir_label)

        # Create and add button to select destination directory
        self.btn_select_dest = QPushButton('Select destination directory', self)
        self.btn_select_dest.clicked.connect(self.select_destination)
        self.dest_dir_label = QLabel(self)
        layout.addWidget(self.btn_select_dest)
        layout.addWidget(self.dest_dir_label)

        # Create and add button to start the unzipping process
        self.btn_unzip = QPushButton('Unzip files', self)
        self.btn_unzip.clicked.connect(self.start_unzip)
        layout.addWidget(self.btn_unzip)

        # Create and add a progress bar
        self.progress = QProgressBar(self)
        layout.addWidget(self.progress)

        # Create and add a text browser for logging
        self.log = QTextBrowser(self)
        layout.addWidget(self.log)

    def select_directory(self):
        # Open a directory selection dialog and update the source directory label
        self.source_dir = QFileDialog.getExistingDirectory(self, 'Select directory')
        self.source_dir_label.setText(f'Selected directory: {self.source_dir}')

    def select_destination(self):
        # Open a directory selection dialog and update the destination directory label
        self.dest_dir = QFileDialog.getExistingDirectory(self, 'Select destination')
        self.dest_dir_label.setText(f'Selected destination: {self.dest_dir}')

    def start_unzip(self):
        # Check if destination directory exists and is not empty
        if os.path.exists(self.dest_dir) and os.listdir(self.dest_dir):
            # Prompt user about overwriting files in the destination directory
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setText("The destination directory is not empty. Do you want to overwrite existing files?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            retval = msg.exec()
            if retval == QMessageBox.StandardButton.Yes:
                # If user agrees, start the unzip thread
                self.start_unzip_thread()
            else:
                # If user disagrees, do nothing
                pass
        else:
            # If destination directory is empty, start the unzip thread
            self.start_unzip_thread()

    def start_unzip_thread(self):
        # Initialize the unzip thread and connect its signals
        self.unzipper_thread = UnzipThread(self.source_dir, self.dest_dir)
        self.unzipper_thread.progress_signal.connect(self.update_progress)
        self.unzipper_thread.log_signal.connect(self.update_log)
        self.unzipper_thread.start()

    def update_progress(self, value):
        # Update the progress bar with the provided value
        self.progress.setValue(value)

    def update_log(self, text):
        # Append provided text to the log
        self.log.append(text)
