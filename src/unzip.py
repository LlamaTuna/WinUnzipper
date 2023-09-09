import os
import zipfile
from PyQt6.QtCore import pyqtSignal

class Unzipper:
    def __init__(self, source_dir, dest_dir):
        # Initialize with source and destination directories
        self.source_dir = source_dir
        self.dest_dir = dest_dir

    def unzip(self, progress_signal: pyqtSignal, log_signal: pyqtSignal):
        try:
            # Call the helper method to unzip the folder
            self._unzip_folder(self.source_dir, progress_signal, log_signal)
        except Exception as e:
            # Emit any encountered error to the log_signal
            log_signal.emit(f'Error: {e}')

    def _unzip_folder(self, folder, progress_signal, log_signal):
        try:
            # List all the items in the specified folder
            items = os.listdir(folder)
        except OSError as e:
            # Emit an error if reading the directory fails
            log_signal.emit(f'Error reading directory {folder}: {e}')
            return

        for i, item in enumerate(items):
            # Construct the full path of the item
            item_path = os.path.join(folder, item)
            
            # Check if the item is a zip file
            if zipfile.is_zipfile(item_path):
                # Create a new extraction directory under dest_dir that includes 
                # the relative path of the item to the source directory.
                relative_path = os.path.relpath(item_path, self.source_dir)
                extract_dir = os.path.join(self.dest_dir, os.path.splitext(relative_path)[0])
                os.makedirs(extract_dir, exist_ok=True)
                
                try:
                    # Open the zip file and extract it to the extraction directory
                    with zipfile.ZipFile(item_path, 'r') as zip_ref:
                        log_signal.emit(f'Unzipping: {item_path}')
                        zip_ref.extractall(extract_dir)
                        log_signal.emit(f'Unzipped: {item_path}')
                except zipfile.BadZipFile:
                    # Emit an error if the file isn't a valid zip file
                    log_signal.emit(f'Error: {item_path} is not a zip file')
                    continue
                except RuntimeError as e:
                    # Emit any other runtime error encountered during extraction
                    log_signal.emit(f'Error unzipping {item_path}: {e}')
                    continue

                # Recursively call _unzip_folder on the extraction directory 
                # to handle nested zips
                self._unzip_folder(extract_dir, progress_signal, log_signal)
            
            # If the item is a directory, call _unzip_folder on it
            elif os.path.isdir(item_path):
                self._unzip_folder(item_path, progress_signal, log_signal)

            # Calculate and emit the progress percentage
            progress = int((i + 1) / len(items) * 100)
            progress_signal.emit(progress)
