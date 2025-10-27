"""
Author: Junjie-Xie
Updated: 2025/9/19
Functions: 
"""
import numpy as np
import matplotlib.pyplot as plt
from src.general.sys.list_dir_files import *
from src.general.numerical.edit_data import *
from src.general.load_data.save_read_data import *
from src.my_style.my_figure import *

filefolder = r"D:\ExpData\SPE\20250917RenishawRaman\XJJ\20250917\20250403#"
filters = ['.spc', '.wdf']
files = list_dir_files(filefolder, filters)
# for file in files:
#     # if "532" not in file and "(" not in file:
#     if "532" in file:
#         print(file)
# print("------------")
new_files = []
nums = []
for file in files:
    if "hBN_with_EBI" in file and "(" not in file:
        if 'hBN_with_EBI_P_6.txt' in file:
            continue
        else:
            new_files.append(file)
    else:
        pass

new_files = sort_files(new_files)
nums = range(1, len(new_files)+1, 1)
names = ["1000KX", "500KX", "200KX", "100KX", "50KX"]
new_names = [name for name in names for _ in range(3)]

for num, file in zip(nums, new_files):
    data = read_lines_txt(os.path.join(filefolder, file), separator='\t', skip_lines=1, row_lines_names=None)
    x = np.array(data['data1'])
    y = np.array(data['data2'])
    if any(True if i == num else False for i in range(1, 16, 3)):
        fig = plt.figure(figsize=(8*3, 6*1.3), dpi=200)
        ax1 = fig.add_subplot(131)
        ax2 = fig.add_subplot(132)
        ax3 = fig.add_subplot(133)
        fig.suptitle("hBN w/ EBI-" + new_names[num], fontsize=30, fontweight='bold', y=1)
        the_graph1(ax1)
        the_graph1(ax2)
        the_graph2(ax3)


    mask1 = (x < 1000)
    mask2 = (1000 < x) & (x < 2000)
    mask3 = (2000 < x)
    x1, y1 = x[mask1], y[mask1]
    x2, y2 = x[mask2], y[mask2]
    x3, y3 = x[mask3], y[mask3]

    ax1.plot(x1, y1)
    ax2.plot(x2, y2)
    ax3.plot(x3, y3)

plt.show()