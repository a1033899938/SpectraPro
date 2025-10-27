from src.ui.read_file import *
from src.ui.general_methods import GeneralMethods
from src.general.figure import set_figure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from scipy.optimize import curve_fit



def elliptical_polarization_malus_law(theta, I0, Ex, Ey, delta):
    """
    根据马吕斯定律计算椭圆偏振光通过偏振片后的透射光强。

    参数:
        I0 (float): 入射光的总光强。
        Ex (float): 电场在x方向的振幅。
        Ey (float): 电场在y方向的振幅。
        delta (float): x和y分量之间的相位差（单位：度）。
        theta (float): 偏振片的透光轴与x轴的夹角（单位：度）。

    返回:
        float: 透射光强。
    """
    # # 将角度转换为弧度
    # delta_rad = math.radians(delta)
    # theta_rad = math.radians(theta)

    # 计算透射光强
    I_transmitted = I0 * (
        (Ex * np.cos(theta)) ** 2 +
        (Ey * np.sin(theta)) ** 2 +
        2 * Ex * Ey * np.cos(theta) * np.sin(theta) * np.cos(delta)
    )

    return I_transmitted

'''
curve colors
'''
# 获取默认颜色循环
default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# 获取前 20 条曲线的颜色
num_colors = 20
colors = default_colors * (num_colors // len(default_colors) + 1)  # 复制颜色列表以确保足够多的颜色
colors = colors[:num_colors]  # 截取前 num_colors 条颜色

folder_path = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\ARS\20250318\LaserPolarization\m8"
extensions = ['.spe']

fig0 = plt.figure(figsize=(8, 6))
ax0 = fig0.add_subplot(111)

file_paths, files, file_names = GeneralMethods.list_files_in_directory(folder_path, extensions)
i = 0
save_fig = 1

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

    wav = x
    sps.append(y)

    rots.append(int(file_name.split('_')[-1][1:4]))
    ints.append(np.max(y))
    ax0.plot(x, y, label=file_name)

    # title = f'Laser polarization-{i}'
    # set_figure.set_label_and_title(ax0, title=title, xlabel='Rotation(Degree)', ylabel='Intensity(counts)',
    #                                label_fontsize=25, title_fontsize=25,
    #                                label_font_family='Times New Roman', title_font_family='Times New Roman',
    #                                label_fontweight='bold', title_fontweight='bold',
    #                                label_pad=15, title_pad=15)
    # set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
    # set_figure.set_tick(ax0, xbins=16, ybins=0, fontsize=10, fontweight='bold',
    #                     linewidth=3, tick_pad=5, direction='in',
    #                     ticks_xlabel=np.arange(440, 461, 5))  # Normalized

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')
print(x)
y = np.arange(np.shape(rots)[0])
Z = np.array(sps)
X, Y = np.meshgrid(x, np.array(rots)*4)

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

# title = f'Excitation-Polarization'
# set_figure.set_label_and_title(ax, title=title, xlabel='Process time(min)', ylabel='Intensity(counts)',
#                                label_fontsize=25, title_fontsize=25,
#                                label_font_family='Times New Roman', title_font_family='Times New Roman',
#                                label_fontweight='bold', title_fontweight='bold',
#                                label_pad=15, title_pad=15, mode='3d')
# set_figure.set_spines(ax, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
# set_figure.set_tick(ax, xbins=6, ybins=10, fontsize=10, fontweight='bold',
#                     linewidth=3, tick_pad=5, direction='in',
#                     ticks_xlabel=np.arange(0, 721, 120),
#                     ticks_ylabel=np.arange(np.min(x), np.max(x)+1, 5), mode='3d')  # Normalized
# ax.set_xlabel(xlabel='Angle(degree)', labelpad=15)
# ax.set_ylabel(ylabel='Wavelength(nm)', labelpad=15)
# ax.zaxis.set_rotate_label(False)
# ax.set_zlabel(zlabel='Intensity(counts)', rotation=90, labelpad=15)

# ax0.set_box_aspect([1, 1, 1])
ax.view_init(elev=20, azim=45)  # elev 是仰角，azim 是方位角
plt.tight_layout()
# ax.grid(True)
if save_fig == 1:
    plt.savefig(fr"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\ARS\20250318\LaserPolarization\Laser_Polarization_3d.png")

# 将两个列表组合在一起，并根据 list1 排序
zipped_lists = zip(rots, ints)
sorted_zipped_lists = sorted(zipped_lists, key=lambda x: x[0])
# 解压缩得到排序后的 list1 和 list2
rots, ints = zip(*sorted_zipped_lists)
# 将结果转换回列表（因为 zip 返回的是元组）
rots = list(rots)
ints = list(ints)
rots = np.array(rots)
ints = np.array(ints)
rots = np.radians(rots)*4
import os

np.savez(os.path.join(os.path.dirname(folder_path), 'wav_sps_excitation.npz'),
             wav=wav,
             sps=sps)

np.savez(os.path.join(os.path.dirname(folder_path), 'rots_ints_excitation.npz'),
             rots=rots,
             ints=ints)

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, polar=True)
ax.scatter(rots, ints, linewidth=3)

set_figure.set_label_and_title(ax, title ='Excitation-Polarization', xlabel='', ylabel='', label_pad=25)
# set_figure.set_spines(ax0)
# set_figure.set_tick(ax0, xbins=16, ybins=10, fontsize=10, fontweight='bold',
#                     linewidth=3, tick_pad=5, direction='in',
#                     ticks_xlabel=np.arange(300, 1101, 50))  # Normalized
# set_figure.set_legend(ax0, legend_labels=legend_labels, font_size=8, location='upper right')

popt, pcov = curve_fit(elliptical_polarization_malus_law, rots, ints)
I0, Ex, Ey, delta = popt
print(f"I0={I0}, Ex={Ex}, Ey={Ey}, delta={delta}")
y_fit = elliptical_polarization_malus_law(rots, *popt)
ax.plot(rots, y_fit, linewidth=2, color='#d62728')
ax.plot(rots, y_fit, linewidth=2, color='#d62728')

# 设置坐标轴的线条样式
ax.spines['polar'].set_linewidth(3)  # 极坐标的脊线宽度
for spine in ax.spines.values():
    spine.set_linewidth(3)  # 设置所有脊线宽度（可以按需指定特定方向的脊线）

if save_fig == 1:
    plt.savefig(fr"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\ARS\20250318\LaserPolarization\Laser_Polarization_2d.png")

plt.show()