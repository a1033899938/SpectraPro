"""
Author: Junjie-Xie
Updated: 2025/7/18
Functions:
    1. 将多个变量保存为.npz格式（支持自定义变量名或默认命名）
    2. 将多个一维数组按列写入txt文件（支持添加标题行、自定义分隔符、文件覆盖确认）
    3. 按列读取txt文件数据为浮点数列表（支持跳过行、自定义分隔符、从指定行读取列名）
    4. 保存不定数量的矩阵到JSON文件（支持列表或字典形式输入）
    5. 从JSON文件加载矩阵数据为字典形式
"""
import os
import numpy as np
import tkinter as tk
from tkinter import messagebox
import json
from typing import Union

def save_variables_npy(*args, save_path: str, variables_names: list=None):
    """
    将多个变量保存为npz
    :param args: 多个变量
    :param save_path: 文件保存路径
    :param variables_names: 变量名
    :return:
    """
    save_with_variables_names = False
    # 仅当提供了与变量个数相同的variables_names, 才会以variables_names中给定的字符作为变量名
    if variables_names is not None:
        if len(variables_names) == len(args):
            save_with_variables_names = True
        else:
            print(f"variables_names length {len(variables_names)} is not equal to args length {len(args)}")

    if save_with_variables_names is True:
        print(f"以variables_names: {variables_names}, 中的字符作为保存的变量名")
        np.savez(save_path,
                 **{name: arg for name, arg in zip(variables_names, args)})
    else:
        print(f"以data1, data2, ...作为变量名")
        default_names = ['data'+ str(i) for i in range(len(args))]
        np.savez(save_path,
                 **{name: arg for name, arg in zip(default_names, args)})

def save_lines_txt(data1: Union[np.ndarray, list], data2: Union[np.ndarray, list], *args: Union[np.ndarray, list], save_path: str, separator: str=' ', lines_names: list=None, confirm_all_overwrite: bool=False):
    """
    将多个一维数组，按列写入txt
    :param data1: 第一列数据
    :param data2: 第二列数据
    :param args: 其他列数据
    :param save_path: 文件保存路径
    :param separator: 行分隔符
    :param lines_names: 第一行的字符
    :param confirm_all_overwrite: 是否覆盖全部已有文件，将不再弹出询问框！
    """

    if confirm_all_overwrite is True:
        ok = True
        print("确认所有写入执行覆盖操作！")
    else:
        if os.path.exists(save_path):
            print("File Exist!")
            # 创建主窗口
            root = tk.Tk()

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

            # 如number_of_placeholder = 2时，placeholder = '{} {}\n'
            placeholder = separator.join(['{}'] * number_of_placeholder) + '\n'
            print(placeholder)
            # 打开文件并逐行写入数据
            with open(save_path, "w") as f:
                if lines_names is not None:
                    f.write(placeholder.format(*lines_names))
                for i in range(len(data1)):
                    row_data = [data1[i], data2[i]] + [arg[i] for arg in args]
                    f.write(placeholder.format(*row_data))
                f.close()
    else:
        print("用户点击了 Cancel")
    return ok


def read_lines_txt(file_path, separator=' ', skip_lines=0, row_lines_names=None):
    """
    按列读取TXT文件中的数据，存储为浮点数列表，并可选跳过前几行
    :param file_path: 文件路径
    :param separator: 行分隔符
    :param skip_lines: 跳过的行数
    :param row_lines_names: 行名所在行号（0-based），None表示使用默认键名
    :return: 字典，键为列名(或row_lines_names中对应的名称)，值为对应列的数据列表
    """

    data_columns = []
    with open(file_path, "r") as f:
        if row_lines_names is not None:
            # 通过字符化只显示可见字符, 再通过分割符分割行
            lines_names = f.readlines()[row_lines_names].strip().split(separator)

        # 重置文件指针并读取数据行
        f.seek(0)
        # 读取所有行，并跳过前skip_lines行
        lines = f.readlines()[skip_lines:]  # 切片操作直接跳过前n行

        for line in lines:
            columns = line.strip().split(separator)  # 按行分隔符分割列
            if columns:  # 跳过空行
                # 将每一列的数据转换为浮点数
                row_data = [float(col) for col in columns]
                # 如果是第一行有效数据，初始化data_columns（按列数创建列表）
                if not data_columns:
                    data_columns = [[] for _ in range(len(row_data))]
                # 检查当前行的列数是否与第一行一致（避免数据格式不一致）
                if len(row_data) != len(data_columns):
                    raise ValueError(f"数据格式不一致：第{len(data_columns[0]) + 1}行的列数与第一行不同")
                # 将每列数据添加到对应的列表
                for i, value in enumerate(row_data):
                    data_columns[i].append(value)

    # 构建返回的字典
    if lines_names is not None:
        # 使用读取的列名作为键
        if len(lines_names) != len(data_columns):
            raise ValueError(f"列名数量({len(lines_names)})与数据列数({len(data_columns)})不一致")
            print("使用默认键名 data1, data2, ...")
            return {f'data{i + 1}': data for i, data in enumerate(data_columns)}
        else:
            print(f"使用第{row_lines_names}行:{[line_name for line_name in lines_names]},作为键名")
            return {name: data for name, data in zip(lines_names, data_columns)}
    else:
        # 使用默认键名 data1, data2, ...
        print("使用默认键名 data1, data2, ...")
        return {f'data{i + 1}': data for i, data in enumerate(data_columns)}

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


def read_row_txt(file_path, delimiter=None):
    """
    读取文本文件，将所有行的元素合并为一个一维列表返回

    参数:
        file_path (str): 要读取的文件路径
        delimiter (str, optional): 分隔符，默认为None表示使用任意空白字符作为分隔符

    返回:
        list: 包含所有元素的一维列表，如果文件不存在则返回空列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            elements = []
            for line in file:
                # 去除首尾空白字符（包括换行符）
                stripped_line = line.strip()
                # 如果行不为空，则拆分并添加到元素列表
                if stripped_line:
                    if delimiter is None:
                        # 用任意空白字符拆分
                        line_elements = stripped_line.split()
                    else:
                        # 用指定分隔符拆分
                        line_elements = stripped_line.split(delimiter)
                    elements.extend(line_elements)  # 使用extend而非append合并到一维列表
        return elements
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在")
        return []
    except Exception as e:
        print(f"读取文件时发生错误: {str(e)}")
        return []

if __name__ == "__main__":
    pass
    # save_lines_txt, 使用示例
    # a = [1, 2, 4]
    # b = [4, 5, 6]
    # c = [7, 8, 9]
    # save_path = r"test.txt"
    # save_lines_txt(a, b, c, save_path=save_path, first_line=['a', 'b', 'c'], confirm_all_overwrite=False)

    # read_lines_txt, 使用示例
    # save_path = r"test.txt"
    # data = read_lines_txt(file_path=save_path, separator=' ', row_lines_names=0, skip_lines=1)

    # save_variables_npy, 使用示例
    # a = 10
    # b = [1, 2, 3]
    # variables_names = ["a", "b"]
    # vars = [a, b]
    # save_variables_npy(a, b, save_path=r"test.npz", variables_names=["a", "b"])
    # data = np.load(r"test.npz")
    # 打印data中的key和value对
    # for key, value in data.items():
    #     print(key, value)
    # # 打印data中的所有key
    # for key in data.files:
    #     print(key, data[key])