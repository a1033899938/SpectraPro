import numpy as np


def find_val_idx(x, val):
    """
    查找数组中最接近给定值的元素索引

    参数:
    x (array-like): 输入数组
    val (float): 要查找的值

    返回:
    int: 最接近给定值的元素索引
    """
    idx = np.argmin(np.abs(x - val))
    return idx

def choose_range(x, y, *args, min_val, max_val, axis=0):
    """
    选择x范围为min到max，同时对y等参数也取相同索引范围的数据
    :param x: 如波长
    :param y: 如强度
    :param arg: 其他参数
    :param min: x的起点值
    :param max: x的终点值
    :return: 选择完范围的x, y ...参数值
    """
    if min_val > max_val:
        min_val, max_val = max_val, min_val

    min_index = np.argmin(np.abs(x - min_val))  # 区间左闭
    max_index = np.argmin(np.abs(x - max_val)) + 1  # 区间右闭

    x_sliced = x[min_index:max_index]
    def slice_array(arr):
        if arr.ndim == 1:
            return arr[min_index:max_index]
        elif arr.ndim == 2:
            if axis == 0:
                return arr[min_index:max_index, :]
            elif axis == 1:
                return arr[:, min_index:max_index]
        elif arr.ndim == 3:
            if axis == 0:
                return arr[min_index:max_index, :, :]
            elif axis == 1:
                return arr[:, min_index:max_index, :]
            elif axis == 2:
                return arr[:, :, min_index:max_index]
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

if __name__ == '__main__':
    x = np.array([1, 2, 3, 4])
    y = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    print(type(y))
    x, y = choose_range(x, y, min_val=2, max_val=3, axis=1)
    print(x)
    print(y)