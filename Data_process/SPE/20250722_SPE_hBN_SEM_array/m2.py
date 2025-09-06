"""
Author: Junjie-Xie
Updated: 2025/9/5
Functions: 
"""
import numpy as np
import matplotlib.pyplot as plt
import h5py

from src.general.numerical.edit_data import find_val_idx
from src.my_style.my_color import *
from src.my_style.my_figure import *

h5_file = r"E:\Data\20250722_SPE_hBN_SEM_array\measurement-2.h5"


with h5py.File(h5_file, "r") as f:
    data = f["OceanOpticsSpectrometer"]["HWP_degree_0"]
    fig = plt.figure(figsize=(9 * 1.1, 6 * 1.1), dpi=400)
    ax = fig.add_subplot(111, polar=True)
    fig2 = plt.figure(figsize=(9 * 1.1, 6 * 1.1), dpi=400)
    ax2 = fig2.add_subplot(111)
    peak_ints = []
    for i in range(180):
        spname = f"HWP_degree_{i}"
        sp = data[spname]

        bgd = np.array(sp.attrs['background'])
        wav = np.array(sp.attrs['wavelengths'])
        sp_time = sp.attrs['integration_time'] / 1000
        bgd_time = sp.attrs['background_int'] / 1000

        sp = sp / sp_time
        bgd = bgd / bgd_time
        sp = sp - bgd
        ax2.plot(wav, sp)
        peak_ints.append(sp[find_val_idx(wav, 538)])

nums = np.radians(range(180))
nums = nums * 4
ax.plot(nums, peak_ints)

"""设置fig"""
# 设置坐标轴的线条样式
ax.spines['polar'].set_linewidth(3)  # 极坐标的脊线宽度
for spine in ax.spines.values():
    spine.set_linewidth(3)  # 设置所有脊线宽度（可以按需指定特定方向的脊线）

# 设置刻度
# 设置45°间隔的刻度，排除360°（2π）
xticks = np.linspace(0, 2 * np.pi, 9)  # 从 0 到 2π，间隔为 45°（8个点）
xticks = xticks[:-1]  # 去除最后一个刻度 360°（2π）

# 设置角度刻度
ax.set_xticks(xticks)
ax.tick_params(axis='both', which='major', labelsize=15, length=10, width=3, direction='in', pad=10)

# 设置字体粗细和刻度标签
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(15)
    label.set_fontweight('bold')
    label.set_family('Times New Roman')

the_graph(ax2)
plt.show()