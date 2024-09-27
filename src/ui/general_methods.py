import time
import os
import numpy as np
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QLineEdit
from PyQt5.QtGui import QTransform
"""General methods
"""


class GeneralMethods:
    @staticmethod
    def select_spectrum_file_through_dialog():
        """Select spectrum file through a dialog, and return (1)file path"""
        print("Select spectrum file through a dialog.")
        try:
            # Open a file dialog to select a file and display the filename in the text edit.
            spectrum_file_path, _ = QFileDialog.getOpenFileName(parent=None, caption='Select spectrum file',
                                                                directory='',
                                                                filter='Spectrum file (*.txt *.spe *.h5 *.wxd)')
        except Exception as e:
            print(f"Error GeneralMethods.select_spectrum_file_through_dialog:\n  |--> {e}")
        return spectrum_file_path

    @staticmethod
    def select_spectra_file_folder_through_dialog():
        """Select spectra file folder through a dialog, and return (1)file folder path"""
        print("Select spectra file folder through a dialog.")
        try:
            spectra_file_folder_path = QFileDialog.getExistingDirectory(parent=None,
                                                                        caption='Select directory of files',
                                                                        directory='')
        except Exception as e:
            print(f"Error GeneralMethods.select_spectra_file_folder_through_dialog:\n  |--> {e}")
        return spectra_file_folder_path

    @staticmethod
    def input_dialog(parent, title='', property_name=''):
        try:
            text, okPressed = QInputDialog.getText(parent, f"{title}.", f"{property_name.title()}:", QLineEdit.Normal, "")
            return text, okPressed
        except Exception as e:
            print(f"Error GeneralMethods.input_dialog:\n  |--> {e}")

    @staticmethod
    def select_json_file_through_dialog():
        try:
            json_file_path, _ = QFileDialog.getOpenFileName(parent=None, caption='Select json file', directory='cache',
                                                            filter='Json file (*.json)')
            return json_file_path
        except Exception as e:
            print(f"Error GeneralMethods.select_json_file_through_dialog:\n  |--> {e}")

    @staticmethod
    def rotate_view(graphicsView, angle):
        try:
            # create a QTransform object
            transform = QTransform()

            # aplly rotation matrix
            transform.rotate(angle)

            # apply transtorm to graphics view
            graphicsView.setTransform(transform)
        except Exception as e:
            print(f"Error GeneralMethods.rotate_view:\n  |--> {e}")

    @staticmethod
    def get_formatted_time():
        timestamp = time.time()

        dt = datetime.fromtimestamp(timestamp)

        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')

        return formatted_time

    @staticmethod
    def list_files_in_directory(directory, extensions=None):
        file_paths = []
        file_names = []
        extensions = [ext.lower() for ext in extensions]
        files = "haven't done"
        if extensions is None:
            extensions = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_name, file_ext = os.path.splitext(file)
                file_ext = file_ext.lower()
                if not extensions or file_ext in extensions:
                    file_path = os.path.join(root, file)
                    file_paths.append(file_path)
                    file_names.append(file_name)
        return file_paths, files, file_names

    @staticmethod
    def save_figure_data_as_txt(ax, save_fullpath):
        lines = ax.get_lines()
        with open(save_fullpath, 'w') as file:
            for line in lines:
                xdata = line.get_xdata()
                ydata = line.get_ydata()

                # 写入数据到文件
                file.write('X data:\n')
                for xi in xdata:
                    file.write(f'{xi}\n')

                file.write('Y data:\n')
                for yi in ydata:
                    file.write(f'{yi}\n')

    @staticmethod
    def save_image_data_as_npz(ax, save_fullpath):
        dir_path = os.path.dirname(save_fullpath)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        data_to_save = {}
        data_to_save['image'] = ax.images[0].get_array().data  # 获取数据
        np.savez(save_fullpath, **data_to_save)

    @staticmethod
    def save_graph_data_as_npz(ax, save_fullpath):
        data_to_save = {}
        lines = ax.get_lines()
        for i, line in enumerate(lines):
            xdata = line.get_xdata()
            ydata = line.get_ydata()
            data_to_save[f'xdata_{i}'] = xdata
            data_to_save[f'ydata_{i}'] = ydata

        # 保存数据为 .npz 文件
        np.savez(save_fullpath, **data_to_save)

    @staticmethod
    def load_graph_data_from_npz(npz_file_path):
        # 读取 .npz 文件
        data = np.load(npz_file_path)

        # 还原数据
        lines_data = []
        for key in data.keys():
            if key.startswith('xdata_'):
                index = key.split('_')[-1]  # 提取索引
                xdata = data[key]
                ydata_key = f'ydata_{index}'
                if ydata_key in data:
                    ydata = data[ydata_key]
                    lines_data.append((xdata, ydata))

        return lines_data
