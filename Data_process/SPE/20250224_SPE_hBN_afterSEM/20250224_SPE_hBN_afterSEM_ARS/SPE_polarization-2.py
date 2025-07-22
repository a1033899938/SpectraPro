from src.ui import read_file
from src.ui.general_methods import GeneralMethods
from src.general.figure import set_figure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from scipy.optimize import curve_fit

def gaussian(x, A, mu, sigma):
    return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))


def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
    return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))


def lorentzian(x, A, x0, gamma):
    """
    洛伦兹函数
    :param x: 自变量
    :param A: 峰值面积
    :param x0: 峰值中心位置
    :param gamma: 半高全宽 (FWHM)
    :return: 洛伦兹函数值
    """
    return (A / np.pi) * (0.5 * gamma) / ((x - x0) ** 2 + (0.5 * gamma) ** 2)

def lorentzian_plus_gaussian(x, A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3):
    peak1 = lorentzian(x, A1, x1, gamma1)
    peak2 = gaussian(x, A2, x2, gamma2)
    peak3 = lorentzian(x, A3, x3, gamma3)
    return peak1 + peak2 + peak3

def triple_lorentzian(x, A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3):
    peak1 = lorentzian(x, A1, x1, gamma1)
    peak2 = lorentzian(x, A2, x2, gamma2)
    peak3 = lorentzian(x, A3, x3, gamma3)
    return peak1 + peak2 + peak3
'''
curve colors
'''
# 获取默认颜色循环
default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# 获取前 20 条曲线的颜色
num_colors = 20
colors = default_colors * (num_colors // len(default_colors) + 1)  # 复制颜色列表以确保足够多的颜色
colors = colors[:num_colors]  # 截取前 num_colors 条颜色

folder_path = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\SPE\20250318\SPEPolarization\m1"
extensions = ['.spe']

file_paths, files, file_names = GeneralMethods.list_files_in_directory(folder_path, extensions)
i = 0

rots = []
ints = []

i = 0
sps = []
for file_path, file_name in zip(file_paths, file_names):
    i += 1
    readFile = read_file(file_path, strip=[39, 52], show_data_flag=False)
    data = readFile.data
    x = data['wavelength']
    y = data['intensity']

    fig0 = plt.figure(figsize=(8, 6))
    ax0 = fig0.add_subplot(111)
    try:
        """三峰拟合"""
        p0 = [100, 537, 6,
                20, 550, 10,
                 20, 577, 6]

        bounds = ([0, 535, 0,
                   0, 540, 0,
                   0, 570, 0],
                  [100000, 540, 10,
                    100000, 565, 12,
                    100000, 580, 10])
        popt, pcov = curve_fit(lorentzian_plus_gaussian, x, y, p0=p0, bounds=bounds)
        A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3 = popt
        mag_now = (A1/np.pi)/(gamma1/2)
        print(file_name)
        print(f'拟合结果: A1 = {A1:.2f}, mu1 = {x1:.2f}, sigma1 = {gamma1:.2f}, '
              f'A2 = {A2:.2f}, mu2 = {x2:.2f}, sigma2 = {gamma2:.2f}',
              f'A3 = {A2:.2f}, mu3 = {x3:.2f}, sigma3 = {gamma3:.2f}')
        y_fit = lorentzian_plus_gaussian(x, *popt)
        y_fit1 = lorentzian(x, A1, x1, gamma1)
        y_fit2 = gaussian(x, A2, x2, gamma2)
        y_fit3 = lorentzian(x, A3, x3, gamma3)
        ax0.plot(x, y_fit, 'r-', label='Fitted Gaussian')
        ax0.plot(x, y_fit1, 'b--', label='Fitted Gaussian')
        ax0.plot(x, y_fit2, 'g--', label='Fitted Gaussian')
        ax0.plot(x, y_fit3, 'm--', label='Fitted Gaussian', linewidth=2)
    except Exception as e:
        print(e)
    sps.append(y)

    rots.append(int(file_name.split('_')[-1][1:4]))
    # ints.append(np.max(y))
    ints.append(mag_now)
    ax0.plot(x, y, label=file_name)

    title = f'Laser polarization-{i}'
    set_figure.set_label_and_title(ax0, title=title, ylabel='Intensity(counts)',
                                   label_fontsize=25, title_fontsize=25,
                                   label_font_family='Times New Roman', title_font_family='Times New Roman',
                                   label_fontweight='bold', title_fontweight='bold',
                                   label_pad=15, title_pad=15)
    set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
    set_figure.set_tick(ax0, xbins=16, ybins=0, fontsize=10, fontweight='bold',
                        linewidth=3, tick_pad=5, direction='in',
                        ticks_xlabel=np.arange(500, 641, 20))  # Normalized

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')
y = np.arange(i)
Z = np.array(sps)
X, Y = np.meshgrid(x, y)

for i in y:
    ax.plot(Y[i], X[i], Z[i], color=plt.cm.viridis(i / len(y)),
             linestyle='-', linewidth=1, alpha=1)
    ax.plot(Y[i], X[i], np.zeros_like(Z[i]), color='gray', alpha=1)

    polygon = [
        [Y[i, 0], X[i, 0], 0],  # 左下
        [Y[i, -1], X[i, -1], 0],  # 右下
    ]
    for j in range(len(x) - 1, -1, -1):  # 依次添加点，使得polygon成为一个完整的闭合多边形
        polygon.append([Y[i, j], X[i, j], Z[i, j]])
    ax.add_collection3d(Poly3DCollection([polygon], color=plt.cm.viridis(i / len(y)), alpha=0.5))
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=20, azim=45)  # elev 是仰角，azim 是方位角
print(rots)
print(ints)

# 将两个列表组合在一起，并根据 list1 排序
zipped_lists = zip(rots, ints)
sorted_zipped_lists = sorted(zipped_lists, key=lambda x: x[0])
# 解压缩得到排序后的 list1 和 list2
rots, ints = zip(*sorted_zipped_lists)
# 将结果转换回列表（因为 zip 返回的是元组）
rots = list(rots)
ints = list(ints)
rots = np.array(rots)
ints = np.array(ints)/3000*1.1
rots = np.radians(rots)*4

print(rots)
print(ints)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, polar=True)
ax.scatter(rots, ints, c='none', marker='^', edgecolors='#d62728', s=40, linewidths=1.5)

set_figure.set_label_and_title(ax, title ='Laser-Polarization', xlabel='', ylabel='', label_pad=25)
# set_figure.set_spines(ax0)
# set_figure.set_tick(ax0, xbins=16, ybins=10, fontsize=10, fontweight='bold',
#                     linewidth=3, tick_pad=5, direction='in',
#                     ticks_xlabel=np.arange(300, 1101, 50))  # Normalized
# set_figure.set_legend(ax0, legend_labels=legend_labels, font_size=8, location='upper right')

# 设置坐标轴的线条样式
ax.spines['polar'].set_linewidth(3)  # 极坐标的脊线宽度
for spine in ax.spines.values():
    spine.set_linewidth(3)  # 设置所有脊线宽度（可以按需指定特定方向的脊线）

"""Laser"""
folder_path = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\SPE\20250318\LaserPolarization\m8"
extensions = ['.spe']

file_paths, files, file_names = GeneralMethods.list_files_in_directory(folder_path, extensions)
i = 0

rots = []
ints = []

i = 0
sps = []
for file_path, file_name in zip(file_paths, file_names):
    i += 1
    readFile = read_file(file_path, strip=[45, 56], show_data_flag=False)
    data = readFile.data
    x = data['wavelength']
    y = data['intensity']

    min_differences = np.abs(x - 440)
    min_index = np.argmin(min_differences)
    max_differences = np.abs(x - 460)
    max_index = np.argmin(max_differences)

    x = x[min_index:max_index]
    y = y[min_index:max_index]
    sps.append(y)

    rots.append(int(file_name.split('_')[-1][1:4]))
    ints.append(np.max(y))
#     ax.plot(x, y, label=file_name)
#
#     title = f'Laser polarization-{i}'
#     set_figure.set_label_and_title(ax, title=title, xlabel='Rotation(Degree)', ylabel='Intensity(counts)',
#                                    label_fontsize=25, title_fontsize=25,
#                                    label_font_family='Times New Roman', title_font_family='Times New Roman',
#                                    label_fontweight='bold', title_fontweight='bold',
#                                    label_pad=15, title_pad=15)
#     set_figure.set_spines(ax, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
#     set_figure.set_tick(ax, xbins=16, ybins=0, fontsize=10, fontweight='bold',
#                         linewidth=3, tick_pad=5, direction='in',
#                         ticks_xlabel=np.arange(440, 461, 5))  # Normalized
#
# fig = plt.figure(figsize=(12, 9))
# ax = fig.add_subplot(111, projection='3d')
# y = np.arange(i)
# Z = np.array(sps)
# X, Y = np.meshgrid(x, y)
#
# for i in y:
#     ax.plot(Y[i], X[i], Z[i], color=plt.cm.viridis(i / len(y)),
#              linestyle='-', linewidth=1, alpha=1)
#     ax.plot(Y[i], X[i], np.zeros_like(Z[i]), color='gray', alpha=1)
#
#     polygon = [
#         [Y[i, 0], X[i, 0], 0],  # 左下
#         [Y[i, -1], X[i, -1], 0],  # 右下
#     ]
#     for j in range(len(x) - 1, -1, -1):  # 依次添加点，使得polygon成为一个完整的闭合多边形
#         polygon.append([Y[i, j], X[i, j], Z[i, j]])
#     ax.add_collection3d(Poly3DCollection([polygon], color=plt.cm.viridis(i / len(y)), alpha=0.5))
#     ax.set_box_aspect([1, 1, 1])
#     ax.view_init(elev=20, azim=45)  # elev 是仰角，azim 是方位角
# print(rots)
# print(ints)

# 将两个列表组合在一起，并根据 list1 排序
zipped_lists = zip(rots, ints)
sorted_zipped_lists = sorted(zipped_lists, key=lambda x: x[0])
# 解压缩得到排序后的 list1 和 list2
rots, ints = zip(*sorted_zipped_lists)
# 将结果转换回列表（因为 zip 返回的是元组）
rots = list(rots)
ints = list(ints)
rots = np.array(rots)
ints = np.array(ints)/200000
rots = np.radians(rots)*4

print(rots)
print(ints)

ax.scatter(rots, ints, linewidth=3, color='#1f77b4', marker='*')

plt.show()