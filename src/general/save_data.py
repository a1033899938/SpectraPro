import os
import numpy as np
import tkinter as tk
from tkinter import messagebox
import json

def save_lines_txt(data1, data2, *args, save_full_path, comfirm_all_overwrite=False):
    """
    将数据写入文件。

    参数:
        save_full_path (str): 文件保存路径。
        data1 (list): 第一列数据。
        data2 (list): 第二列数据。
        *args (list): 其他列数据（可变参数）
    """
    if comfirm_all_overwrite is True:
        ok = True
        print("确认所有写入执行覆盖操作！")
    else:
        if os.path.exists(save_full_path):
            print("File Exist!")
            # 创建主窗口
            root = tk.Tk()
            # root.withdraw()  # 隐藏主窗口

            # 弹出确认对话框
            ok = messagebox.askokcancel("确认", "文件已存在，是否覆盖")
            if ok:
                print("用户点击了 OK")
            root.destroy()
        else:
            ok = True

    # 根据用户选择执行操作
    if ok:
        print("确认写入txt")
        if len(data1) != len(data2):
            print("Notice!!!")
            print(f"length of data1: {len(data1)}")
            print(f"length of data2: {len(data2)}")
        else:
            # 动态生成占位符
            if args:
                number_of_placeholder = 2 + len(args)
            else:
                number_of_placeholder = 2
            placeholder = ' '.join(['{}'] * number_of_placeholder) + '\n'
            # 打开文件并逐行写入数据
            with open(save_full_path, "w") as f:
                for i in range(len(data1)):
                    row_data = [data1[i], data2[i]] + [arg[i] for arg in args]
                    f.write(placeholder.format(*row_data))
                    # f.write('{:} {:}\n'.format(data1[i], data2[i]))  # 每行末尾添加换行符
                f.close()
    else:
        print("用户点击了 Cancel")

def read_lines_txt(file_full_path):
    data_columns = []
    with open(file_full_path, "r") as f:
        for line in f.readlines():
            columns = line.strip().split()
            if columns:
                # 将每一列的数据转换为浮点数
                row_data = [float(col) for col in columns]
                # 如果是第一行，初始化 data_columns
                if not data_columns:
                    data_columns = [[] for _ in range(len(row_data))]
                # 将每一列的数据添加到对应的列表中
                for i, value in enumerate(row_data):
                    data_columns[i].append(value)
            # if columns:
            #     data1.append(float(columns[0]))
            #     data2.append(float(columns[1]))
    return tuple(data_columns)

def save_matrices_json(matrices, save_full_path, comfirm_all_overwrite=False):
    """
    保存不定数量的矩阵到JSON文件

    参数:
        matrices: 可以是以下形式之一:
                 - 列表形式 [matrix1, matrix2, ...]
                 - 字典形式 {"name1": matrix1, "name2": matrix2, ...}
        filename: 保存路径 (如 'data.json')
    """
    # 统一转换为字典格式
    if isinstance(matrices, (list, tuple)):
        matrix_dict = {f'matrix_{i}': mat.tolist() for i, mat in enumerate(matrices, 1)}
    elif isinstance(matrices, dict):
        matrix_dict = {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in matrices.items()}
    else:
        raise TypeError("输入必须是列表/元组或字典")

    # 保存到文件
    with open(save_full_path, 'w') as f:
        json.dump(matrix_dict, f, indent=4)  # indent参数使文件可读性更好


def load_matrices_from_json(file_full_path):
    """
    从JSON文件读取矩阵

    返回:
        字典形式 {矩阵名: numpy数组}
    """
    with open(file_full_path, 'r') as f:
        data = json.load(f)

    return {k: np.array(v) for k, v in data.items()}

if __name__ == "__main__":
    # save_path = r''
    # save_name = 'powers_ints.txt'
    # # def save_2line_txt(savepath, savename, x, y):
    # # 要保存的数据
    data1 = [1, 2, 3]
    data2 = [4, 5, 6]
    data3 = [4, 5, 6]
    # save_lines_txt(data1, data2, data3, save_full_path=r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6\powers_ints-2.txt")

    # file_path = r''
    # file_name = 'powers_ints.txt'
    # read_2line_txt(os.path.join(file_path, file_name))
