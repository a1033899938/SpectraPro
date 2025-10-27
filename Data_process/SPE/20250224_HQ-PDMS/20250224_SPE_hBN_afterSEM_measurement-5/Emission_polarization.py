import os.path
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import h5py

from src.general.figure import set_figure
from src.general import *
from src.general import *
from src.general import *

def the_figure(ax, key):
    set_figure.set_label_and_title(ax, title=f'{key[:-2]}', ylabel='Intensity(counts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 1101, 50))

def the_figure2(ax):
    set_figure.set_label_and_title(ax, title='Emission Polarization', xlabel='', ylabel='', label_pad=25)
    set_figure.set_spines(ax, mode='polar')
    set_figure.set_tick(ax, ticks_xlabel=np.radians(np.arange(0, 360, 45)), ticks_ylabel=np.arange(0, 2001, 500))
    ax.axes.get_yticklabels()[0].set_visible(False)  # 隐藏y轴（极轴）第一个标签
    ax.grid(True)

datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-5\20250224_SPE_hBN_afterSEM_measurement-5.h5"
save_fig = 1

"""fig0"""
# with h5py.File(datapath1, "r") as f:
#     data = f['OceanOpticsSpectrometer']
#     bgd = np.array(data['hBN_afterSEM_5kV_5min_2mW_m2_0d_1'].attrs['background'])
#     bgd_time = data['hBN_afterSEM_5kV_5min_2mW_m2_0d_1'].attrs['background_int'] / 1000
#     wav = np.array(data['hBN_afterSEM_5kV_5min_2mW_m2_0d_1'].attrs['wavelengths'])
#     bgd = bgd / bgd_time
#
#     rots = []
#     ints = []
#     legend_labels = []
#     for key in data.keys():
#         if 'hBN_afterSEM_5kV_5min_2mW_m2' in key and 'hBN_afterSEM_5kV_5min_2mW_m2_0d_0' not in key:
#             fig = plt.figure(figsize=(8, 6))
#             ax = fig.add_subplot(111)
#             sp = data[key]
#             sp_time = sp.attrs['integration_time'] / 1000
#             sp = np.array(sp)
#             sp = sp / sp_time
#             sp = sp - bgd
#
#             x, y = choose_range(wav, sp, min_val=300, max_val=1100)
#
#             rots.append(int(key.split('_')[-2][0:-1]))
#             legend_labels.append(key)
#             ax.plot(x, y)
#
#             try:
#                 """三峰拟合"""
#                 p0 = [100, 537, 6,
#                         20, 550, 10,
#                          20, 577, 6]
#
#                 bounds = ([0, 535, 0,
#                            0, 540, 0,
#                            0, 570, 0],
#                           [100000, 540, 10,
#                             100000, 565, 12,
#                             100000, 580, 10])
#                 x_for_fit, y_for_fit = choose_range(wav, sp, min_val=510, max_val=900)
#                 popt, pcov = curve_fit(lorentzian_2_plus_gaussian_1, x_for_fit, y_for_fit, p0=p0, bounds=bounds)
#                 A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3 = popt
#                 mag_now = (A1/np.pi)/(gamma1/2)
#                 ints.append(mag_now)
#                 print(f'拟合结果: A1 = {A1:.2f}, mu1 = {x1:.2f}, sigma1 = {gamma1:.2f}, '
#                       f'A2 = {A2:.2f}, mu2 = {x2:.2f}, sigma2 = {gamma2:.2f}',
#                       f'A3 = {A2:.2f}, mu3 = {x3:.2f}, sigma3 = {gamma3:.2f}')
#                 y_fit = lorentzian_2_plus_gaussian_1(x, *popt)
#                 y_fit1 = lorentzian(x_for_fit, A1, x1, gamma1)
#                 y_fit2 = gaussian(x_for_fit, A2, x2, gamma2)
#                 y_fit3 = lorentzian(x_for_fit, A3, x3, gamma3)
#                 ax.plot(x, y_fit, 'r-', label='Fitted lorentzian_2_plus_gaussian_1')
#                 ax.plot(x_for_fit, y_fit1, 'b--', label='Fitted lorentzian')
#                 ax.plot(x_for_fit, y_fit2, 'g--', label='Fitted Gaussian')
#                 ax.plot(x_for_fit, y_fit3, 'm--', label='Fitted lorentzian')
#             except Exception as e:
#                 print(e)
#
#             the_figure(ax, key)
#             plt.tight_layout()
#             if save_fig == 1:
#                 plt.savefig(os.path.join(os.path.dirname(datapath1), 'curve_fit', f'HP_rotation_curve_fit-{key}.png'))
#
# rots, ints = sort_lists(rots, ints)
# rots = np.radians(rots)*2

"""读取数据"""
rots, ints = read_lines_txt(os.path.join(os.path.dirname(datapath1), f'rots_ints-Emission.txt'))
"""保存PL线形拟合数据"""
# save_lines_txt(rots, ints, save_full_path=os.path.join(os.path.dirname(datapath1), f'rots_ints-Emission.txt'))

fig1 = plt.figure(figsize=(8, 6))
ax1 = fig1.add_subplot(111, polar=True)
ax1.scatter(rots, ints, linewidth=3)

popt, pcov = curve_fit(elliptical_polarization_malus_law, rots, ints)
I0, Ex, Ey, delta = popt
print(f"I0={I0}, Ex={Ex}, Ey={Ey}, delta={delta}")
y_fit = elliptical_polarization_malus_law(rots, *popt)
ax1.plot(rots, y_fit, linewidth=2, color='#d62728')

the_figure2(ax1)
plt.tight_layout()
if save_fig == 1:
    plt.savefig(os.path.join(os.path.dirname(datapath1), 'Emission_polarization.png'))
plt.show()