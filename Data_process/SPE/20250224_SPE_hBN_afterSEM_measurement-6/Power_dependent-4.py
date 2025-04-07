import os.path
import h5py
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from sympy.physics.units import years

from src.general import set_figure
from src.general.curve_functions import *
from src.general.save_data import *
from src.general.edit_data import *

def the_figure(ax, key):
    set_figure.set_label_and_title(ax, title=f'{key[:-2]}', ylabel='Intensity(counts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 701, 50))  # Normalized

def the_figure1(ax1):
    # plt.yscale('log')
    set_figure.set_label_and_title(ax1, title=f'Excitation power-denpendent intensity\nof peak 1',
                                   xlabel='Excitaion Power(uW)', ylabel='Intensity(counts)')
    set_figure.set_spines(ax1)
    set_figure.set_tick(ax1, ybins=0, ticks_xlabel=np.arange(0, 12001, 2000))

datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6\measurement-6.h5"
save_fig = 0

"""fig0"""
# with h5py.File(datapath1, "r") as f:
#     data = f['OceanOpticsSpectrometer']
#     bgd = np.array(data['hBN_afterSEM_5kV_5min_60KX_time_series_m2_P10uW_0'].attrs['background'])
#     bgd_time = data['hBN_afterSEM_5kV_5min_60KX_time_series_m2_P10uW_0'].attrs['background_int'] / 1000
#     wav = np.array(data['hBN_afterSEM_5kV_5min_60KX_time_series_m2_P10uW_0'].attrs['wavelengths'])
#     bgd = bgd / bgd_time
#     bgd, _ = np.meshgrid(bgd, np.arange(0, data['hBN_afterSEM_5kV_5min_60KX_time_series_m2_P10uW_0'].shape[0])) # 创建一个与sp相同大小的bgd阵列
#
#     keys = ['hBN_afterSEM_5kV_5min_60KX_time_series_m4_P10uW_0',
#             'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P20uW_0',
#             'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P30uW_0',
#             'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P50uW_0',
#             'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P100uW_0',
#             'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P200uW_0',
#             'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P300uW_0',
#             'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P500uW_0',
#             'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P1000uW_0',
#             'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P2000uW_0',
#             'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P3000uW_1',
#             'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P5000uW_1',
#             'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P10000uW_0',
#             'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P15000uW_0']
#
#     powers = []
#     ints = []
#     errors = []
#     for key in keys:
#         sp = data[key]
#         sp_time = sp.attrs['integration_time'] / 1000
#         sp = np.array(sp)
#         sp = sp / sp_time
#         sp = sp - bgd
#         # print(sp)
#
#         if key == 'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P15000uW_0':
#             key = 'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P12000uW_0'
#         powers.append(int(key.split('_')[-2][1:-2]))
#         ints_now = []
#         cws_now = []
#         gammas_now = []
#
#         """逐条光谱拟合"""
#         for row in range(sp.shape[0]):
#             fig = plt.figure(figsize=(12, 8))
#             ax = fig.add_subplot(111)
#             sp_now = sp[row, :]
#             x, y = choose_range(wav, sp_now, min_val=400, max_val=900)
#             ax.plot(x, y)
#
#             """三峰拟合"""
#             p0 = [100, 537, 6,
#                     20, 550, 10,
#                      20, 577, 6]
#
#             bounds = ([0, 535, 0,
#                        0, 540, 0,
#                        0, 570, 0],
#                       [100000, 540, 10,
#                         100000, 565, 12,
#                         100000, 580, 10])
#             x_for_fit, y_for_fit = choose_range(wav, sp_now, min_val=510, max_val=700)
#
#             popt, pcov = curve_fit(lorentzian_2_plus_gaussian_1, x_for_fit, y_for_fit, p0=p0, bounds=bounds)
#             A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3 = popt
#             mag_now = (A1/np.pi)/(gamma1/2)
#             ints_now.append(mag_now)
#             cws_now.append(x1)
#             gammas_now.append(gamma1)
#             print(key)
#             print(f'拟合结果: A1 = {A1:.2f}, mu1 = {x1:.2f}, sigma1 = {gamma1:.2f}, '
#                   f'A2 = {A2:.2f}, mu2 = {x2:.2f}, sigma2 = {gamma2:.2f}',
#                   f'A3 = {A2:.2f}, mu3 = {x3:.2f}, sigma3 = {gamma3:.2f}')
#             y_fit = lorentzian_2_plus_gaussian_1(x, *popt)
#             y_fit1 = lorentzian(x_for_fit, A1, x1, gamma1)
#             y_fit2 = gaussian(x_for_fit, A2, x2, gamma2)
#             y_fit3 = lorentzian(x_for_fit, A3, x3, gamma3)
#             ax.plot(x, y_fit, 'r-', label='Fitted lorentzian_2_plus_gaussian_1')
#             ax.plot(x_for_fit, y_fit1, 'b--', label='Fitted lorentzian')
#             ax.plot(x_for_fit, y_fit2, 'g--', label='Fitted Gaussian')
#             ax.plot(x_for_fit, y_fit3, 'm--', label='Fitted lorentzian')
#
#             the_figure(ax, key)
#             plt.tight_layout()
#             if save_fig == 1:
#                 plt.savefig(os.path.join(os.path.dirname(datapath1), 'curve_fit-4', f'power_dependent_PL_curve_fit-{key}-No{row}.png'))
#
#             plt.close(fig)
#         ints_now = sorted(ints_now)
#         ints.append(np.mean(ints_now[1:-1]))  #去掉最小值和最大值再平均
#         errors_now = np.max(ints_now[1:-1]) - np.min(ints_now[1:-1])
#         errors.append(errors_now)
#
# powers, ints, errors = sort_lists(powers, ints, errors)

"""读取数据"""
powers, ints, errors = read_lines_txt(r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6\powers_ints-4.txt")
"""保存PL线形拟合数据"""
# save_lines_txt(powers, ints, errors, save_full_path=os.path.join(os.path.dirname(datapath1), 'powers_ints-4.txt'))

fig1 = plt.figure(figsize=(8, 6))
ax1 = fig1.add_subplot(111)

# ax1.scatter(powers, ints, c='none', marker='^', edgecolors='#d62728', s=40, linewidths=1.5)
ax1.errorbar(powers, ints, yerr=errors, fmt='^', color='#d62728', ecolor='#d62728', capsize=10)
"""功率依赖PL拟合"""
popt, pcov = curve_fit(power_saturation, powers, ints)
P_sat, I_inf = popt
ints_fit = power_saturation(powers, *popt)
ax1.plot(powers, ints_fit, '-', color='#d62728', linewidth=2)

the_figure1(ax1)
plt.tight_layout()
if save_fig == 1:
    # plt.savefig(os.path.join(os.path.dirname(datapath1), 'curve_fit-4', f'power_dependent_intensity_of_peak-1_log.png'))
    plt.savefig(os.path.join(os.path.dirname(datapath1), 'curve_fit-4', f'power_dependent_intensity_of_peak-1.png'))
plt.show()