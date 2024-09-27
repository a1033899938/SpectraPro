import os
import shutil
import sys
import time


def move_txt_files(source_folder, destination_folder):
    txt_files = [f for f in os.listdir(source_folder) if f.endswith('.txt')]
    n_files = len(txt_files)
    for i, filename in enumerate(txt_files):
        source_file = os.path.join(source_folder, filename)
        destination_file = os.path.join(destination_folder, filename)
        shutil.move(source_file, destination_file)
        print_progress_bar(i + 1, n_files)  # 更新进度条
    print()


def print_progress_bar(iteration, total, length=40):
    percent = (iteration / total) * 100
    bar_length = int(length * iteration // total)
    bar = '█' * bar_length + '-' * (length - bar_length)
    sys.stdout.write(f'\r|{bar}| {percent:.2f}%')
    sys.stdout.flush()


if __name__ == '__main__':
    source_folder = r'D:\GitProject\SpectraPro\tests\data_processing\20240925'
    destination_folder = r'D:\GitProject\SpectraPro\tests\trash'

    move_txt_files(source_folder, destination_folder)
