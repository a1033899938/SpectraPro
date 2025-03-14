import os
import pprint
import pprint
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks


# 修改默认颜色的顺序
plt.rcParams['axes.prop_cycle'] = plt.cycler('color', ['#d62728', '#2ca02c', '#ff7f0e', '#1f77b4'])
"""蓝色 (#1f77b4)
橙色 (#ff7f0e)
绿色 (#2ca02c)
红色 (#d62728)
紫色 (#9467bd)
棕色 (#8c564b)
粉色 (#e377c2)
绿色 (#7f7f7f)
蓝绿色 (#bcbd22)
灰色 (#17becf)"""

folder_path = r'F:\Data\SHG'
extensions = ['.txt']

file_names = ['MoS2_Si_intensity.txt',
              'MoS2_AuFilm_intensity.txt',
              'AuSHIN-1_MoS2_AuFilm_intensity.txt',
              'AuSHIN-2_MoS2_AuFilm_intensity.txt']
file_paths = [os.path.join(folder_path, file_name) for file_name in file_names]
legend_labels = [r'$\mathrm{MoS}_2/\mathrm{Si}$',
                 r'$\mathrm{MoS}_2/\mathrm{AuFilm}$',
                 r'$\mathrm{AuSHIN-1}/\mathrm{MoS}_2/\mathrm{AuFilm}$',
                 r'$\mathrm{AuSHIN-2}/\mathrm{MoS}_2/\mathrm{AuFilm}$']

nums = []
sps = []
for file_path, file_name in zip(file_paths, file_names):
    data = np.loadtxt(file_path, delimiter='\t', skiprows=1)
    # 分割数据
    x = data[:, 0]
    y = data[:, 1]
    nums.append(x)
    sps.append(y)

# 作图
fig = plt.figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111, polar=True)
i = 0
for num, sp in zip(nums, sps):
    ax.plot(num, sp)
    """寻找极值"""
    print("当前图形：")
    print(legend_labels[i])
    i += 1

    # 找到局部最大值的索引
    peaks, _ = find_peaks(sp, distance=10)
    max_index = np.argmax(sp)
    print("最大值的索引:", max_index)
    print("最大值的角度:", max_index*4)
    print("局部最大值的索引:", peaks)
    print("局部最大值的角度:", peaks*4)

    # 找到局部最小值的索引
    troughs, _ = find_peaks(-sp, distance=10)  # 取反后找局部最大值，即找局部最小值
    min_index = np.argmin(sp)
    print("最小值的索引:", min_index)
    print("最小值的角度:", min_index * 4)
    print("局部最小值的索引:", troughs)
    print("局部最小值的角度:", troughs * 4)

title = r'$\mathrm{MoS}_2 \; \mathrm{SHG \; Intensity}$'
ax.set_title(title, fontsize=25, fontname='Times New Roman', fontweight='bold', pad=15)
ax.set_xlabel('', fontsize=25, fontname='Times New Roman', fontweight='bold', labelpad=8)
ax.set_ylabel('', fontsize=25, fontname='Times New Roman', fontweight='bold', labelpad=8)

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

# 设置图例
legend_labels = legend_labels
ax.legend(legend_labels, fontsize=15, loc='upper left', bbox_to_anchor=(1, 1))
save_filename = os.path.join(r'F:\Data\SHG', 'SHG_intensity.png')

# save_subfig(fig, save_filename)
plt.show()
