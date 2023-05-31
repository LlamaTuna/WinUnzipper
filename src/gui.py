from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QProgressBar, QTextBrowser, QLabel, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
import os
import zipfile
import sys
from unzip import Unzipper

class UnzipThread(QThread):
    progress_signal = pyqtSignal(int)
    log_signal = pyqtSignal(str)

    def __init__(self, source_dir, dest_dir):
        super().__init__()
        self.unzipper = Unzipper(source_dir, dest_dir)

    def run(self):
        self.unzipper.unzip(self.progress_signal, self.log_signal)

class GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'Unzipper GUI'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.btn_select_dir = QPushButton('Select directory to unzip', self)
        self.btn_select_dir.clicked.connect(self.select_directory)
        self.source_dir_label = QLabel(self)
        layout.addWidget(self.btn_select_dir)
        layout.addWidget(self.source_dir_label)

        self.btn_select_dest = QPushButton('Select destination directory', self)
        self.btn_select_dest.clicked.connect(self.select_destination)
        self.dest_dir_label = QLabel(self)
        layout.addWidget(self.btn_select_dest)
        layout.addWidget(self.dest_dir_label)

        self.btn_unzip = QPushButton('Unzip files', self)
        self.btn_unzip.clicked.connect(self.start_unzip)
        layout.addWidget(self.btn_unzip)

        self.progress = QProgressBar(self)
        layout.addWidget(self.progress)

        self.log = QTextBrowser(self)
        layout.addWidget(self.log)

    def select_directory(self):
        self.source_dir = QFileDialog.getExistingDirectory(self, 'Select directory')
        self.source_dir_label.setText(f'Selected directory: {self.source_dir}')

    def select_destination(self):
        self.dest_dir = QFileDialog.getExistingDirectory(self, 'Select destination')
        self.dest_dir_label.setText(f'Selected destination: {self.dest_dir}')

    def start_unzip(self):
        if os.path.exists(self.dest_dir) and os.listdir(self.dest_dir):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setText("The destination directory is not empty. Do you want to overwrite existing files?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            retval = msg.exec()  # change here
            if retval == QMessageBox.StandardButton.Yes:
                self.unzipper_thread = UnzipThread(self.source_dir, self.dest_dir)
                self.unzipper_thread.progress_signal.connect(self.update_progress)
                self.unzipper_thread.log_signal.connect(self.update_log)
                self.unzipper_thread.start()
            else:
                # Handle case where user does not want to overwrite
                pass
        else:
            self.unzipper_thread = UnzipThread(self.source_dir, self.dest_dir)
            self.unzipper_thread.progress_signal.connect(self.update_progress)
            self.unzipper_thread.log_signal.connect(self.update_log)
            self.unzipper_thread.start()


    def update_progress(self, value):
        # update the progress bar value
        self.progress.setValue(value)

    def update_log(self, text):
        # append text to the log
        self.log.append(text)
