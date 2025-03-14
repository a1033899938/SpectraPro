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


folder_path = r'F:\Data\SHG\20241214SHG'
extensions = ['.spe']

file_name = 'source_800fs.spe'
file_path = os.path.join(folder_path, file_name)

RF = read_file(file_path, strip=[193, 217], show_data_flag=False)
graph = RF.data['intensity']
image = RF.data['intensity_image']
strip = RF.data['strip']
wav = RF.data['wavelength']


"""Image"""
fig = plt.figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)
# 使用 pcolor 绘制图像
cax = ax.pcolor(wav, strip, image, cmap='coolwarm')  #, vmin=vmins[i], vmax=vmaxs[i]

# 添加颜色条
cbar = plt.colorbar(cax, ax=ax)
cbar.set_label('Intensity(counts)', fontsize=15, fontweight='bold', family='serif')
cbar.ax.tick_params(labelsize=15, width=2)


title = r'$\mathrm{Source-800fs} \; \mathrm{Pulse}$'
set_figure.set_label_and_title(ax, title=title, xlabel='Wavelength (nm)', ylabel='Strip',
                               label_fontsize=25, title_fontsize=25,
                               label_font_family='Times New Roman', title_font_family='Times New Roman',
                               label_fontweight='bold', title_fontweight='bold',
                               label_pad=8, title_pad=15)
set_figure.set_spines(ax, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
set_figure.set_tick(ax, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                    linewidth=3, tick_pad=5, direction='in'
                    )

save_filename = os.path.join(r'F:\Data\SHG\20241214SHG', 'Source_Image')
save_subfig(fig, save_filename)
print('Save file: ' + save_filename)

"""Graph"""
fig = plt.figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)
ax.plot(wav, graph/np.max(graph))

# 图片设置
set_figure.set_label_and_title(ax, title=title, xlabel='Wavelength(nm)', ylabel='Intensity Normalized',
                               label_fontsize=25, title_fontsize=25,
                               label_font_family='Times New Roman', title_font_family='Times New Roman',
                               label_fontweight='bold', title_fontweight='bold',
                               label_pad=8, title_pad=15)
set_figure.set_spines(ax, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
set_figure.set_tick(ax, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                    linewidth=3, tick_pad=5, direction='in'
                    )
save_filename = os.path.join(r'F:\Data\SHG\20241214SHG', 'Source_Graph')
save_subfig(fig, save_filename)
print('Save file: ' + save_filename)
plt.show()
