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

folder_path = r'C:\Users\a1033\Desktop\Contemporary\motor2'
# folder_path = r'C:\Users\a1033\Desktop\Contemporary\20241208_SHG\20241208_SHG\800nm-3mw-step2-20s'
extensions = ['.spe']

file_paths, files, file_names = GeneralMethods.list_files_in_directory(folder_path, extensions)

i = 0
file_names_sorted = sort_files(file_names)
file_paths_sorted = sort_files(file_paths)
# pprint.pprint(file_names_sorted)

num_file = []
sps = []
for file_path, file_name in zip(file_paths_sorted, file_names_sorted):
    numbers = re.findall(r'\d+\.\d+|\d+', file_path)
    num_file.append(numbers[-1])
    RF = read_file(file_path, strip=[197, 223], show_data_flag=False)
    # RF = read_file(file_path, strip=[194, 206], show_data_flag=False)
    sp = RF.data['intensity']
    sps.append(sp)
    wav = RF.data['wavelength']


# print(num_file)


def gaussian(x, A, mu, sigma, C):
    return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2)) + C


def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
    return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))


from scipy.optimize import curve_fit


def find_nearest_idx(lst, target):
    # 计算每个元素与目标值的差值，返回最小值的索引
    return min(range(len(lst)), key=lambda i: abs(lst[i] - target))


idx_low = find_nearest_idx(wav, 312)
idx_high = find_nearest_idx(wav, 487)
peak_intensity = []
failed_fits = 0
for num, sp in zip(num_file, sps):
    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(wav[idx_low:idx_high], sp[idx_low:idx_high])
    try:
        popt, pcov = curve_fit(gaussian, wav[idx_low:idx_high], sp[idx_low:idx_high], p0=[500, 400, 4, 0], maxfev=5000)
        A_fit, mu_fit, sigma_fit, C = popt
        print(popt)
        y_fit = gaussian(wav, *popt)
        ax.plot(wav[idx_low:idx_high], y_fit[idx_low:idx_high])
        if A_fit <= 0:
            peak_intensity.append(0)
        else:
            peak_intensity.append(A_fit)
    except Exception as e:
        print(f"拟合失败，文件：{file_name}, 错误：{e}")
        failed_fits += 1
        peak_intensity.append(np.nan)  # 存储一个 NaN 值，保持列表长度一致
        pass

    save_filename = os.path.join(folder_path, num + '.png')
    print(save_filename)
    # set_figure.set_scientific_y_ticks(ax, sci_fontsize=15, sci_fontweight='bold')
    save_subfig(fig, save_filename)
    plt.close(fig)
title = 'MoS2 SHG'
set_figure.set_label_and_title(ax, title=title, ylabel='Intensity(Contrast, Normalized)',
                               label_fontsize=25, title_fontsize=25,
                               label_font_family='Times New Roman', title_font_family='Times New Roman',
                               label_fontweight='bold', title_fontweight='bold',
                               label_pad=8, title_pad=15)
set_figure.set_spines(ax, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
set_figure.set_tick(ax, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                    linewidth=3, tick_pad=5, direction='in'
                    )

num_file = angles_deg = pd.to_numeric(num_file)
fig = plt.figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111, polar=True)
num_file = np.radians(num_file)
num_file = num_file * 6
ax.plot(num_file, peak_intensity)
print(peak_intensity)

# ticks_xlabel=np.linspace(500, 1000, 11)
# set_figure.set_legend(ax, legend_labels=legend_labels, font_size=20)
print(f"共有 {failed_fits} 次拟合失败。")
plt.show()
