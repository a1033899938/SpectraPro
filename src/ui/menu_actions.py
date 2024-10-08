from PyQt5.QtWidgets import QAction
from src.ui.general_methods import GeneralMethods


class MenuActions:
    """Handles menu actions and their corresponding slots."""

    def __init__(self, main_window, treeManager):
        print("MenuActions is instantiating...")
        try:
            self.parent = main_window
            self.treeManager = treeManager
            self.model = self.treeManager.model
        except Exception as e:
            print(f"Error MenuActions.init:\n  |--> {e}")

    def select_spectrum_file_action(self):
        """Create a custom action for file selection."""
        try:
            action = QAction('Select Spectrum File', self.parent)
            action.triggered.connect(self.select_spectrum_file_slot)
            return action
        except Exception as e:
            print(f"Error MenuActions.select_spectrum_file_action:\n  |--> {e}")

    def select_spectrum_file_slot(self):
        """A slot to handle: 'select_spectrum_file_action."""
        """Select spectrum file and show it's path in textedit."""
        try:
            print("#################################")
            print("You click 'select spectrum file'.")
            print("Selecting spectrum file and show it's path in textedit...")
            self.parent.spectrum_file_path = GeneralMethods.select_spectrum_file_through_dialog()
            if self.parent.spectrum_file_path:
                print(f"  |--> Select spectrum file: {self.parent.spectrum_file_path}")
                self.parent.spectrumFileTextEdit.setText(self.parent.spectrum_file_path)
        except Exception as e:
            print(f"Error MenuActions.select_spectrum_file_slot:\n  |--> {e}")

    def select_spectra_file_folder_action(self):
        """Create a custom action for file folder selection."""
        try:
            action = QAction('Select Spectra File Folder', self.parent)
            action.triggered.connect(self.select_spectra_file_folder_slot)
            return action
        except Exception as e:
            print(f"Error MenuActions.select_spectra_file_folder_action:\n  |--> {e}")

    def select_spectra_file_folder_slot(self):
        """A slot to handle: 'select_spectra_file_folder_action."""
        """Select spectra file folder and show it's path in textedit."""
        try:
            print("#################################")
            print("You click 'select spectra file folder'.")
            print("Selecting spectra file folder and show it's path in textedit.")
            self.parent.spectra_file_folder_path = GeneralMethods.select_spectra_file_folder_through_dialog()
            if self.parent.spectra_file_folder_path:
                print(f"  |--> Select spectra file folder: {self.parent.spectra_file_folder_path}")
                self.parent.spectraFolderTextEdit.setText(self.parent.spectra_file_folder_path)
                self.treeManager.loadDirectory(self.parent.spectra_file_folder_path)
        except Exception as e:
            print(f"Error MenuActions.select_spectra_file_folder_slot:\n  |--> {e}")

    def save_cache_action(self):
        try:
            action = QAction('Save cache', self.parent)
            action.triggered.connect(self.treeManager.input_name_head_and_save_cache)
            return action
        except Exception as e:
            print(f"Error MenuActions.save_cache_action:\n  |--> {e}")

    def load_cache_action(self):
        try:
            action = QAction('Load cache', self.parent)
            action.triggered.connect(self.treeManager.select_json_file_and_load_cache)
            return action
        except Exception as e:
            print(f"Error MenuActions.load_cache_action:\n  |--> {e}")