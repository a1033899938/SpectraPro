"""各类拟合函数"""
import numpy as np


# 定义高斯函数。用于拟合
def gaussian(x, height, center, width, shift):
    return height * np.exp(-(x - center) ** 2 / (2 * width ** 2)) + shift
