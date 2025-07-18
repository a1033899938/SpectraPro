import os
import tkinter as tk
from tkinter import messagebox

def create_folder(path):
    """
    检查文件夹是否存在，不存在则创建，存在则跳过
    :param path: 要创建的文件夹路径
    :return: bool - 是否成功创建（True表示创建或已存在，False表示创建失败）
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            print(f"创建文件夹: {path}")
        else:
            print(f"文件夹已存在，跳过创建: {path}")
        return True
    except Exception as e:
        print(f"创建文件夹失败: {e}")
        return False

if __name__ == '__main__':
    folder_now = r"D:\ExpData"
    folders_to_create = create_folder(r"D:\ExpData\1\2")