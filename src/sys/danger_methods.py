import os
import shutil
from  src.general.progress_bar import *


def move_txt_files(source_folder, destination_folder):
    filenames = [f for f in os.listdir(source_folder) if f.endswith('.txt')]
    n_files = len(filenames)
    for i, filename in enumerate(filenames):
        source_filepath = os.path.join(source_folder, filename)
        destination_filepath = os.path.join(destination_folder, filename)
        shutil.move(source_filepath, destination_filepath)
        print_progress_bar(i + 1, n_files)  # 更新进度条
    print()


if __name__ == '__main__':
    source_folder = r'D:\GitProject\SpectraPro\tests\data_processing\20240925'
    destination_folder = r'D:\GitProject\SpectraPro\tests\trash'

    move_txt_files(source_folder, destination_folder)
