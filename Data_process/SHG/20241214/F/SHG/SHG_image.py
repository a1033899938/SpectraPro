import os
import pprint
import matplotlib.pyplot as plt
import numpy as np
from src.general.read_file import read_file
from src.general import set_figure
from src.ui.general_methods import GeneralMethods
from src.general.save_figure import save_subfig
from src.general.sort_by_number import sort_files
import re
import pandas as pd
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import medfilt


def gaussian(x, A, mu, sigma, C):
    return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2)) + C


def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
    return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))


def find_nearest_idx(lst, target):
    # 计算每个元素与目标值的差值，返回最小值的索引
    return min(range(len(lst)), key=lambda i: abs(lst[i] - target))


"""
Note：
本代码用于
1、读取四次SHG测试的数据
    --分别是MoS2/Si, MoS2/AuFilm, AuSHIN-1/MoS2/AuFilm, AuSHIN-2/MoS2/AuFilm这三种结构四个点位的PL光谱
    --MoS2/Si是章立心测量的，.spe无法目前的脚本打开，所以先用matlab转成了.mat文件。其余三个是我测的，可以正常打开
2、读取SHG graph的（1）degree（2）intensity（3）linewidth数组
"""

"""分别读取四次数据"""
folder_paths = [r'F:\Data\SHG\20241208_SHG\800nm-2mw-step2-20s',
                r'F:\Data\SHG\20241214SHG\MoS2_Au_Step2d_2mW_20s',
                r'F:\Data\SHG\20241214SHG\AuSHIN_MoS2_Au_Step2d_2mW_20s',
                r'F:\Data\SHG\20241214SHG\AuSHIN-2_MoS2_Au_Step2d_2mW_20s']

# 图片标题
titles = [r'$\mathrm{MoS}_2/\mathrm{Si} \; \mathrm{SHG}$',
          r'$\mathrm{MoS}_2/\mathrm{AuFilm} \; \mathrm{SHG}$',
          r'$\mathrm{AuSHIN-1}/\mathrm{MoS}_2/\mathrm{AuFilm} \; \mathrm{SHG}$',
          r'$\mathrm{AuSHIN-2}/\mathrm{MoS}_2/\mathrm{AuFilm} \; \mathrm{SHG}$']

save_names = ['MoS2_Si_intensity.txt',
              'MoS2_AuFilm_intensity.txt',
              'AuSHIN-1_MoS2_AuFilm_intensity.txt',
              'AuSHIN-2_MoS2_AuFilm_intensity.txt']

#
vmins = [575, -10, -10, -10]
vmaxs = [620, 30, 30, 30]

for i in range(4):
# i = 1
    folder_path = folder_paths[i]
    if i == 0:
        extensions = ['.mat']
    else:
        extensions = ['.spe']

    # 读取目录下的：文件路径、文件名，并根据文件名中的序号排序。
    file_paths, files, file_names = GeneralMethods.list_files_in_directory(folder_path, extensions)
    file_names_sorted = sort_files(file_names)
    file_paths_sorted = sort_files(file_paths)

    # 读取光谱强度、波长
    nums = []  # 文件序号
    images = []  # 光谱强度
    sps = []
    if i == 0:
        idx = [21, 75]  # MoS2/Si
        k = 0  # 顺序
    elif i == 1:
        idx = [65, 28]  # MoS2/AuFilm
        k = 1  # 逆序
    elif i == 2:
        idx = [20, 28]  # AuSHIN-1/MoS2/AuFilm
        k = 0  # 顺序
    elif i == 3:
        idx = [65, 29]  # AuSHIN-2/MoS2/AuFilm
        k = 1  # 逆序
    for file_path, file_name in zip(file_paths_sorted, file_names_sorted):
        numbers = re.findall(r'\d+\.\d+|\d+', file_path)
        if int(numbers[-1]) in idx:
            nums.append(numbers[-1])
            if i == 0:
                strip = [187, 211]
            else:
                strip = [181, 205]
            RF = read_file(file_path, strip=strip, show_data_flag=False)
            image = RF.data['intensity_image']
            images.append(image)
            sp = RF.data['intensity']
            sps.append(sp)
            strip = RF.data['strip']
            wav = RF.data['wavelength']

    for num, image, sp in zip(nums, images, sps):
        """Image"""
        fig = plt.figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        # 使用 pcolor 绘制图像
        cax = ax.pcolor(wav, strip, image, cmap='coolwarm', vmin=vmins[i], vmax=vmaxs[i])  # 'shading'控制着色的方式

        # 添加颜色条
        cbar = plt.colorbar(cax, ax=ax)
        cbar.set_label('Intensity(counts)', fontsize=15, fontweight='bold', family='serif')
        cbar.ax.tick_params(labelsize=15, width=2)

        # # 图片设置
        if k == 0:
            title = titles[i] + r'_$\mathrm{minval}$'
        elif k == 1:
            title = titles[i] + r'_$\mathrm{maxval}$'
        set_figure.set_label_and_title(ax, title=title, xlabel='Wavelength (nm)', ylabel='Strip',
                                       label_fontsize=25, title_fontsize=25,
                                       label_font_family='Times New Roman', title_font_family='Times New Roman',
                                       label_fontweight='bold', title_fontweight='bold',
                                       label_pad=8, title_pad=15)
        set_figure.set_spines(ax, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
        set_figure.set_tick(ax, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                            linewidth=3, tick_pad=5, direction='in'
                            )

        if k == 0:
            save_filename = os.path.join(r'F:\Data\SHG\20241214SHG', save_names[i].replace('.txt', '_Image_min'))
        elif k == 1:
            save_filename = os.path.join(r'F:\Data\SHG\20241214SHG', save_names[i].replace('.txt', '_Image_max'))
        save_subfig(fig, save_filename)
        print('Save file: ' + save_filename)

        """Graph"""
        fig = plt.figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(wav, sp)
        try:
            popt, pcov = curve_fit(gaussian, wav, sp, p0=[200, 400, 5, 0], maxfev=5000)
            A_fit, mu_fit, sigma_fit, C = popt
            print(num)
            print(popt)
            y_fit = gaussian(wav, *popt)
            ax.plot(wav, y_fit)
        except Exception as e:
            print(f"拟合失败, 错误：{e}")
            pass

        # 图片设置
        set_figure.set_label_and_title(ax, title=title, xlabel='Wavelength(nm)', ylabel='Intensity(counts)',
                                       label_fontsize=25, title_fontsize=25,
                                       label_font_family='Times New Roman', title_font_family='Times New Roman',
                                       label_fontweight='bold', title_fontweight='bold',
                                       label_pad=8, title_pad=15)
        set_figure.set_spines(ax, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
        set_figure.set_tick(ax, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                            linewidth=3, tick_pad=5, direction='in'
                            )
        if k == 0:
            save_filename = os.path.join(r'F:\Data\SHG\20241214SHG', save_names[i].replace('.txt', '_Graph_min'))
        elif k == 1:
            save_filename = os.path.join(r'F:\Data\SHG\20241214SHG', save_names[i].replace('.txt', '_Graph_max'))
        save_subfig(fig, save_filename)
        print('Save file: ' + save_filename)
        k = 1 - k
plt.show()
