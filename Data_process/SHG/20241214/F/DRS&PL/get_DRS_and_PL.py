import os
import pprint
import pprint
import matplotlib.pyplot as plt
import numpy as np
from src.general.read_file import read_file
from src.general import set_figure
from src.ui.general_methods import GeneralMethods
from src.general.save_figure import save_subfig
from matplotlib.lines import Line2D
from scipy.optimize import curve_fit
from src.general.sort_by_number import sort_files
import copy
import re
import pandas as pd
import scipy.io as sio


def gaussian(x, A, mu, sigma, C):
    return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2)) + C


def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
    return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))


def find_nearest_idx(lst, target):
    # 计算每个元素与目标值的差值，返回最小值的索引
    return min(range(len(lst)), key=lambda i: abs(lst[i] - target))


folder_path = r'F:\Data\SHG\20241214SHG\PL&DRS'
extensions = ['.spe']


file_paths, files, file_names = GeneralMethods.list_files_in_directory(folder_path, extensions)

for file_path, file_name in zip(file_paths, file_names):
    if 'White' in file_name:  # RCD
        RF = read_file(file_path, strip=[40, 67], show_data_flag=False)  # RCD
        if 'bgd' in file_name:
            sp_ref = RF.data['intensity']
        else:
            sp_R = RF.data['intensity']
            wav_RCD = RF.data['wavelength']
    elif 'uW' in file_name:
        RF = read_file(file_path, strip=[49, 58], show_data_flag=False)  # PL
        sp_PL = RF.data['intensity']
        wav_PL = RF.data['wavelength']


# idx_low = find_nearest_idx(wav_RCD, 560)
# idx_high = find_nearest_idx(wav_RCD, 720)

"""RCD"""
fig = plt.figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)
sp_RCD = (sp_R - sp_ref)/sp_ref  # RCD
sp_RCD = sp_RCD/np.max(sp_RCD)  # RCD
ene_RCD = 1240/wav_RCD
ax.plot(ene_RCD, sp_RCD)

# 设置fig
title = r'$\mathrm{MoS_2} \; \mathrm{RCD}$'
xlabel = 'Energy(eV)'
ylabel = 'Reflectance Contrast Derivative(a.u.)'  # RCD
set_figure.set_label_and_title(ax, title=title, xlabel=xlabel, ylabel=ylabel,
                               label_fontsize=25, title_fontsize=25,
                               label_font_family='Times New Roman', title_font_family='Times New Roman',
                               label_fontweight='bold', title_fontweight='bold',
                               label_pad=8, title_pad=15)
set_figure.set_spines(ax, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
set_figure.set_tick(ax, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                    linewidth=3, tick_pad=5, direction='in'
                    )

# 保存图片
save_filename = os.path.join(folder_path, 'MoS2_RCD')  # RCD
save_subfig(fig, save_filename)
np.savetxt('MoS2_RCD.txt', np.column_stack((ene_RCD, sp_RCD)), header="X, Y", delimiter='\t')
print('Save file: ' + save_filename)

"""PL"""
fig = plt.figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)
ene_PL = 1240/wav_PL
ax.plot(ene_PL, sp_PL)

# 设置fig
title = r'$\mathrm{MoS_2} \; \mathrm{PL}$'
ylabel = 'Integrated PL Intensity(counts)'  # PL
set_figure.set_label_and_title(ax, title=title, xlabel=xlabel, ylabel=ylabel,
                               label_fontsize=25, title_fontsize=25,
                               label_font_family='Times New Roman', title_font_family='Times New Roman',
                               label_fontweight='bold', title_fontweight='bold',
                               label_pad=8, title_pad=15)
set_figure.set_spines(ax, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
set_figure.set_tick(ax, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                    linewidth=3, tick_pad=5, direction='in'
                    )

# 保存图片
save_filename = os.path.join(folder_path, 'MoS2_PL')  # PL
save_subfig(fig, save_filename)
np.savetxt('MoS2_PL.txt', np.column_stack((ene_PL, sp_PL)), header="X, Y", delimiter='\t')
print('Save file: ' + save_filename)

"""RCD_and_PL"""
fig = plt.figure(figsize=(8, 6), dpi=100)
ax1 = fig.add_subplot(111)
ax1_color = 'gray'
ax1.plot(ene_RCD, sp_RCD, color=ax1_color, label='RCD')

# 设置ax1
xlabel = 'Energy(eV)'
ylabel = 'Reflectance Contrast Derivative(a.u.)'  # PL
ax1.set_xlabel(xlabel=xlabel, fontsize=25, family='Times New Roman', weight='bold', labelpad=8)
ax1.set_ylabel(ylabel=ylabel, color=ax1_color, fontsize=25, family='Times New Roman', weight='bold', labelpad=8)
# 设置左侧坐标轴的边框线宽
ax1.spines['bottom'].set_linewidth(3)
ax1.spines['left'].set_linewidth(3)
ax1.spines['top'].set_linewidth(3)
ax1.spines['right'].set_linewidth(3)
# 设置x轴和y轴的刻度数量和线宽
# ax1.xaxis.set_ticks(np.linspace(0, 10, 6))  # x轴刻度
# ax1.yaxis.set_ticks(np.linspace(-1, 1, 10))  # y1轴刻度
ax1.tick_params(axis='x', length=6, width=3, labelsize=15, pad=5, direction='in')
ax1.tick_params(axis='y', length=6, width=3, labelsize=15, pad=5, direction='in', color=ax1_color, labelcolor=ax1_color)
for label in ax1.get_xticklabels() + ax1.get_yticklabels():
    label.set_fontweight('bold')

# 创建右侧的 y 轴
ax2 = ax1.twinx()
ax2_color = '#1f77b4'
ax2.plot(ene_PL, sp_PL, color=ax2_color, label='PL')

# 设置ax2
ylabel = 'Integrated PL Intensity(counts)'
ax2.set_ylabel(ylabel=ylabel, color=ax2_color, fontsize=25, family='Times New Roman', weight='bold', labelpad=8)
# 设置右侧坐标轴的边框线宽
ax2.spines['right'].set_linewidth(3)
ax2.spines['left'].set_linewidth(3)
ax2.spines['top'].set_linewidth(3)
ax2.spines['bottom'].set_linewidth(3)
# 设置x轴和y轴的刻度数量和线宽
# ax2.xaxis.set_ticks(np.linspace(0, 10, 6))  # x轴刻度
# ax2.yaxis.set_ticks(np.linspace(-100, 100, 10))  # y2轴刻度
ax2.tick_params(axis='x', length=6, width=3, labelsize=15, pad=5, direction='in')
ax2.tick_params(axis='y', length=6, width=3, labelsize=15, pad=5, direction='in', color=ax2_color, labelcolor=ax2_color)
for label in ax2.get_xticklabels() + ax2.get_yticklabels():
    label.set_fontweight('bold')

# 设置标题, legend
title = r'$\mathrm{MoS_2} \; \mathrm{Spectra}$'
ax1.set_title(title, fontsize=25, family='Times New Roman', weight='bold', pad=15)
# custom_line1 = Line2D([0], [0], color=ax1_color, lw=3)  # 设置绿色线条，粗细为3
# custom_line2 = Line2D([0], [0], color=ax2_color, lw=3)  # 设置蓝色线条，粗细为2
# ax1.legend(handles=[custom_line1], labels=['RCD'], fontsize=15, loc='upper left')
# ax2.legend(handles=[custom_line2], labels=['PL'], fontsize=15, loc='upper right')

# 保存图片
save_filename = os.path.join(folder_path, 'MoS2_RCD_and_PL')  # PL
save_subfig(fig, save_filename)
np.savetxt('MoS2_RCD_and_PL.txt', np.column_stack((ene_PL, sp_PL)), header="X, Y", delimiter='\t')
print('Save file: ' + save_filename)
plt.show()
