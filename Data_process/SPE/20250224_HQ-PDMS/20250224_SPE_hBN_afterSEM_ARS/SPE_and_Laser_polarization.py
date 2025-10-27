import os

import numpy as np

from src.general.figure.set_figure import *
from src.my_style.my_mapping_para import *


def the_figure(ax, title):
    set_label_and_title(ax, title=title, xlabel='Rotation(degree)',
                                   ylabel='Wavelength(nm)', zlabel='Normalized Intensity(a.u.)', zlabel_rotation=90,
                                   mode='3d', z_label_pad=25, title_pad=0)
    set_spines(ax)
    set_tick(ax, ticks_xlabel=np.arange(0, 721 ,180), ticks_ylabel=np.arange(500, 601, 25), ticks_zlabel=np.arange(0, 1.1, 0.2), mode='3d',
                ticks_zlabel_pad=10, show_ylabel_every_ticks=2, show_xlabel_every_ticks=2)  # Normalized
    ax.zaxis.set_rotate_label(False)
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=20, azim=45)  # elev 是仰角，azim 是方位角
    ax.grid(True)
    plt.tight_layout()

def the_figure1(ax, title):
    set_label_and_title(ax, title=title, xlabel='Rotation(degree)',
                                   ylabel='Wavelength(nm)', zlabel='Normalized Intensity(a.u.)', zlabel_rotation=90,
                                   mode='3d', z_label_pad=25, title_pad=0)
    set_spines(ax)
    set_tick(ax, ticks_xlabel=np.arange(0, 721 ,180), ticks_ylabel=np.arange(440, 461, 5), ticks_zlabel=np.arange(0, 1.1, 0.2) , mode='3d',
                ticks_zlabel_pad=10, show_ylabel_every_ticks=2, show_xlabel_every_ticks=2)  # Normalized
    ax.zaxis.set_rotate_label(False)
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=20, azim=45)  # elev 是仰角，azim 是方位角
    ax.grid(True)
    plt.tight_layout()


def the_figure2(ax):
    set_label_and_title(ax, title='', xlabel='', ylabel='')
    set_spines(ax, mode='polar')
    set_tick(ax, ticks_xlabel=np.radians(np.arange(0, 360, 45)), ticks_ylabel=np.arange(0, 1.2, 0.2), ticks_xlabel_pad=20)
    ax.axes.get_yticklabels()[0].set_visible(False)  # 隐藏y轴（极轴）第一个标签
    ax.axes.get_yticklabels()[-1].set_visible(False)  # 隐藏y轴（极轴）最后一个标签
    set_legend(ax, legend_labels = ['Excitaion', 'Emission'], location=(1, 1, 3, 0))
    ax.grid(True)

folder = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\ARS\20250318"
files = ["rots_ints_emission.npz",
         "rots_ints_excitation.npz",
         "wav_sps_emission.npz",
         "wav_sps_excitation.npz"]

# data1 = np.load(os.path.join(folder, files[2]))
# data2 = np.load(os.path.join(folder, files[3]))

# wav_em = data1["wav"]
# sps_em = data1["sps"]
# wav_ex = data2["wav"]
# sps_ex = data2["sps"]

# fig = plt.figure(figsize=(12, 8), dpi=200)
# ax = fig.add_subplot(111, projection='3d')
# x = wav_em
# y = np.arange(sps_em.shape[0])
# y = np.array(y)
# X, Y = np.meshgrid(x,y*4)
# Z = sps_em
# cascade_3d(X, Y, Z, ax, draw_polygon=True, normalize=True)
# the_figure(ax, title='Emission')

# fig = plt.figure(figsize=(12, 8), dpi=200)
# ax = fig.add_subplot(111, projection='3d')
# x = wav_ex
# y = np.arange(sps_ex.shape[0])
# y = np.array(y)
# X, Y = np.meshgrid(x,y*4)
# Z = sps_ex
# cascade_3d(X, Y, Z, ax, draw_polygon=True, normalize=True)
# the_figure1(ax, title='Excitation')

data3 = np.load(os.path.join(folder, files[0]))
data4 = np.load(os.path.join(folder, files[1]))
rots_em = data3['rots']
ints_em = data3['ints']
ints_em = ints_em / np.max(ints_em)
rots_em, ints_em = choose_range(rots_em, ints_em, x1=0, x2=2 * np.pi)

rots_ex = data4['rots']
ints_ex = data4['ints']
ints_ex = ints_ex / np.max(ints_ex)
rots_ex, ints_ex = choose_range(rots_ex, ints_ex, x1=0, x2=2 * np.pi)
rots_ex = rots_ex + np.deg2rad(-2)

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, polar=True)
ax.scatter(rots_ex, ints_ex, linewidth=3, color='#1f77b4')
ax.scatter(rots_em, ints_em, linewidth=3, color='#d62728')

popt, pcov = curve_fit(elliptical_polarization_malus_law, rots_ex, ints_ex)
I0, Ex, Ey, delta = popt
print(f"I0={I0}, Ex={Ex}, Ey={Ey}, delta={delta}")
y_fit = elliptical_polarization_malus_law(rots_ex, *popt)
ax.plot(rots_ex, y_fit, linewidth=2, color='#1f77b4')

# 计算线偏振度（Degree of Linear Polarization）
dolp_numerator = np.sqrt((Ex**2 - Ey**2)**2 + 4 * (Ex*Ey*np.cos(delta))**2)
dolp_denominator = Ex**2 + Ey**2
dolp = dolp_numerator / dolp_denominator if dolp_denominator != 0 else 0
print(f"dolp={dolp}")

popt, pcov = curve_fit(elliptical_polarization_malus_law, rots_em, ints_em)
I0, Ex, Ey, delta = popt
print(f"I0={I0}, Ex={Ex}, Ey={Ey}, delta={delta}")
y_fit = elliptical_polarization_malus_law(rots_em, *popt)
ax.plot(rots_em, y_fit, linewidth=2, color='#d62728')
# 计算线偏振度（Degree of Linear Polarization）
dolp_numerator = np.sqrt((Ex**2 - Ey**2)**2 + 4 * (Ex*Ey*np.cos(delta))**2)
dolp_denominator = Ex**2 + Ey**2
dolp = dolp_numerator / dolp_denominator if dolp_denominator != 0 else 0
print(f"dolp={dolp}")

the_figure2(ax)
plt.tight_layout()

# 设置坐标轴的线条样式
ax.spines['polar'].set_linewidth(3)  # 极坐标的脊线宽度
for spine in ax.spines.values():
    spine.set_linewidth(3)
plt.show()