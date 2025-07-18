"""
Author: Junjie-Xie
Updated: 2025/07/18
Functions: 列出文件夹下的所有文件（带后缀过滤）
"""
import os


def list_dir_files(folder, filters: list=None):
    """
    列出文件夹下的所有文件，过滤其中带有后缀的项
    :param folder: 文件架路径
    :param filters: 要过滤的后缀
    :return:
    """
    if filters is None:
        filters = []
    files = [
            f for f in os.listdir(folder)
            if not any(f.endswith(ext) for ext in filters)
    ]
    return files


if __name__ == '__main__':
    dir_path = r'D:\GitProject\SpectraPro\tests\pass'
    filters = ['.txt', '.png']
    files = list_dir_files(dir_path, filters)
    print(files)