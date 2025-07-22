"""
Author: Junjie-Xie
Updated: 2025/07/18
Functions:
    1. 从TXT文件读取二维数组（支持自定义分隔符、跳过行和数据类型）
"""
import numpy as np

def read_2d_array_from_txt(filename, delimiter=','):
    """
    从 TXT 文件中读取二维数组

    参数:
    filename (str): 文件名

    返回:
    numpy.ndarray: 二维数组
    """
    try:
        # 使用 numpy 读取 CSV 文件
        array = np.loadtxt(filename, delimiter=delimiter)
        return array

    except FileNotFoundError:
        print(f"错误: 文件 '{filename}' 不存在")
        return None
    except Exception as e:
        print(f"错误: 读取文件时发生异常: {e}")
        return None


# 使用示例
if __name__ == "__main__":
    filename = r"D:\FDTDSimFile\cascade\txt\80nm_0.19.txt"
    array = read_2d_array_from_txt(filename)

    if array is not None:
        print(f"读取的数组形状: {array.shape}")
        print("数组内容:")
        print(array)