import os
import pprint
import pprint
import matplotlib.pyplot as plt
import numpy as np
from src.general.read_file import read_file
from src.general import set_figure
from src.ui.general_methods import GeneralMethods
from src.general.save_figure import save_subfig
from src.general.sort_by_number import sort_files
import copy
import re
import pandas as pd
import csv
import scipy.io as sio

'''
curve colors
'''
# 获取默认颜色循环
default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# 获取前 20 条曲线的颜色
num_colors = 20
colors = default_colors * (num_colors // len(default_colors) + 1)  # 复制颜色列表以确保足够多的颜色
colors = colors[:num_colors]  # 截取前 num_colors 条颜色

file_path = r'C:\Users\a1033\Desktop\Contemporary\20241211LBSPectra\20241214.csv'

data = []
with open(file_path, 'r') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        data.append(row)


print(data)
