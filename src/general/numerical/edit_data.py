"""
Author: Junjie-Xie
Updated: 2025/07/15
Functions:
    1. 查找值在数组中的索引（寻找与目标值最接近的位置）
    2. 计算指定x位置附近的y值中位数（支持自定义窗口大小）
    3. 提取数组指定范围内的子集（支持多维数组和任意轴）
    4. 多列表排序（根据第一个列表对所有列表进行同步排序）
    5. 文件名智能排序（按数字部分排序，支持整数和浮点数）
"""

import numpy as np
from typing import Union
import copy
import re

def find_val_idx(x, x0):
    """
    寻找数组 x 中，与值 x0 最近的位置索引
    :param x: 数组 x
    :param x0: 要寻找的值
    :return: 与 x0 值最近的值对应的位置索引
    """

    idx = np.argmin(np.abs(x - x0))
    return idx


def calculate_median_y_near_x0(
        x: np.ndarray,  # 波长数组（自变量）
        y: np.ndarray,  # 强度数组（因变量）
        x0: Union[float, int],  # 目标波长位置
        window_size: int = 5  # 窗口大小（默认5个点）
) -> float:
    """
    寻找值 x0 在数组 x 中的位置，找到数组 y 在 对应位置附近（某窗口大小范围内）的中位值
    :param x: 数组
    * 要求数组 x 的值是单调有序的
    :param y: 数组
    :param x0: 目标值
    :param window_size: 窗口尺寸
    :return: 数组 y 在窗口内的中位值
    """
    if not isinstance(x, np.ndarray):
        raise TypeError('x must be a numpy array')
    if not isinstance(y, np.ndarray):
        raise TypeError('y must be a numpy array')
    if not isinstance(x0, float) and not isinstance(x0, int):
        raise TypeError('x0 must be a float')

    # 查找值 x0 位置的索引
    index = np.argmin(np.abs(x - x0))
    # 在窗口内，查找数组 y 的中位值
    vals = y[index - window_size//2:index + window_size//2 + 1]
    return np.median(vals)


def choose_range(x: np.ndarray, y: np.ndarray, *args: np.ndarray, x1: Union[float, int], x2: Union[float, int], axis: int=0)\
        -> np.ndarray:
    """
    寻找数组 x 中的 x1 和 x2 的位置，作为子集端点，输出 x 数组在两个端点之间的子集，也输出 y 数组和其他数组对应位置的子集
    :param x: 用于确定端点的数组（也同时会取其子数组）。如波长
    * 要求数组 x 的值是单调有序的
    :param y: 需要取子集的数组。如强度
    :param arg: 其需要取子集的他数组
    :param x1: 子集左端点值
    :param x2: 子集右端点值
    :param axis: 数组 y 和数组 arg 取子集的维度（取第 axis 维的子集）
    :return: x、y和其他数组，各自的子集
    """

    # 输入类型检查
    if not isinstance(x, np.ndarray):
        raise TypeError("x must be a numpy ndarray")
    if not isinstance(y, np.ndarray):
        raise TypeError("y must be a numpy ndarray")
    for arg in args:
        if not isinstance(arg, np.ndarray):
            raise TypeError("All additional arguments must be numpy ndarrays")
    if not isinstance(x1, float) and not isinstance(x1, int):
        raise TypeError('x1 must be a float')
    if not isinstance(x2, float) and not isinstance(x2, int):
        raise TypeError('x2 must be a float')
    if not isinstance(axis, int):
        raise TypeError("axis must be an int")

    # 确定x1和x2的位置
    if x[-1] > x[0]:  # 递增
        start_idx = np.searchsorted(x, x1, 'left')  # 指定当数组中存在重复值时，返回最左侧的插入位置
        end_idx = np.searchsorted(x, x2, 'right')
    else:  # 递减
        start_idx = np.searchsorted(x, x1, 'right')
        end_idx = np.searchsorted(x, x2, 'left')

    # 数组 x 的子集
    x_sliced = x[start_idx:end_idx]

    # 定义子函数，用于取数组 y 和其他数组的子集，并应对它们是1-3维的情况
    def slice_array(arr):
        if arr.ndim == 1:
            return arr[start_idx:end_idx]
        elif arr.ndim == 2:
            if axis == 0:
                return arr[start_idx:end_idx, :]
            elif axis == 1:
                return arr[:, start_idx:end_idx]
        elif arr.ndim == 3:
            if axis == 0:
                return arr[start_idx:end_idx, :, :]
            elif axis == 1:
                return arr[:, start_idx:end_idx, :]
            elif axis == 2:
                return arr[:, :, start_idx:end_idx]
        raise ValueError(f"不支持的矩阵维度： {arr.ndim} for axis {axis}")

    y_sliced = slice_array(y)
    args_sliced = [slice_array(arg) for arg in args]
    return  (x_sliced, y_sliced) + tuple(args_sliced)

def sort_lists(list1, list2, *args):
    """
    先对x排序，再用同样顺序其他参数排序
    :param list1: list 1（对它排序）
    :param list2: 其他需要排序的list
    :param args: 其他需要排序的list
    :return: 排序后的list
    """
    # 将三个列表组合在一起，并根据 list1 排序
    zipped_lists = zip(list1, list2, *args)
    sorted_zipped_lists = sorted(zipped_lists, key=lambda x: x[0])

    # 解压缩得到排序后的 list
    list1, list2, *args = zip(*sorted_zipped_lists)

    # 将结果转换回列表（因为 zip 返回的是元组）
    list1 = list(list1)
    list2 = list(list2)
    for arg in args:
        arg = list(arg)
    return list1, list2, *args

def sort_files(file_names):
    """对文件名列表进行排序"""
    def sort_key(filename):
        """定义排序键函数"""
        # 提取文件名中的所有数字（包括整数和浮点数）
        # \d+\.\d+ 匹配浮点数（例如 0.75），\d+ 匹配整数（例如 12、100）
        numbers = re.findall(r'\d+\.\d+|\d+', filename)
        # 将数字从字符串转换为浮点数或整数
        numbers = [float(num) if '.' in num else int(num) for num in numbers]
        return numbers
    # 通过深复制确保副本完全独立，避免修改原始列表
    file_names_sorted = copy.deepcopy(file_names)
    # 使用sort方法，传入排序键
    file_names_sorted.sort(key=sort_key)
    return file_names_sorted

if __name__ == '__main__':
    # 测试sort_lists
    x = [2, 3, 1, 4]
    y = [1, 2, 3, 4]
    x_s, y_s  = sort_lists(x, y)
    print(x_s, y_s)
    print(x, y)