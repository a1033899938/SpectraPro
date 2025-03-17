import os.path
from scipy.optimize import curve_fit
import h5py
from src.general import set_figure

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

def power_saturation(P, P_sat, I_inf):
    return (I_inf * P) / (P + P_sat)

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from src.general.save_2linedata import save_2line_txt, read_2line_txt

datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6\20250224_SPE_hBN_afterSEM_measurement-6.h5"
save_fig = 0

"""fig0"""
# with h5py.File(datapath1, "r") as f:
#     data = f['OceanOpticsSpectrometer']
#     bgd = np.array(data['hBN_afterSEM_5kV_5min_60KX_time_series_P10uW_0'].attrs['background'])
#     bgd_time = data['hBN_afterSEM_5kV_5min_60KX_time_series_P10uW_0'].attrs['background_int'] / 1000
#     wav = np.array(data['hBN_afterSEM_5kV_5min_60KX_time_series_P10uW_0'].attrs['wavelengths'])
#     bgd = bgd / bgd_time
#     bgd, _ = np.meshgrid(bgd, np.arange(0, data['hBN_afterSEM_5kV_5min_60KX_time_series_P10uW_0'].shape[0])) # 创建一个与sp相同大小的bgd阵列
#     min_differences = np.abs(wav - 400)
#     min_index = np.argmin(min_differences)
#     max_differences = np.abs(wav - 900)
#     max_index = np.argmin(max_differences)
#
#     powers = []
#     ints = []
#     for key in data.keys():
#         if 'hBN_afterSEM_5kV_5min_60KX_time_series' in key and key != 'hBN_afterSEM_5kV_5min_60KX_time_series_P600uW_0' and key != 'hBN_afterSEM_5kV_5min_60KX_time_series_P1100uW_0':
#             # fig0 = plt.figure(figsize=(8, 6))
#             # ax0 = fig0.add_subplot(111)
#             sp = data[key]
#             sp_time = sp.attrs['integration_time'] / 1000
#             sp = np.array(sp)
#             sp = sp / sp_time
#             sp = sp - bgd
#             # print(sp)
#
#             if key == 'hBN_afterSEM_5kV_5min_60KX_time_series_P400uW_0':
#                 key = 'hBN_afterSEM_5kV_5min_60KX_time_series_P300uW_0'
#             powers.append(int(key.split('_')[-2][1:-2]))
#             ints_now = []
#             cws_now = []
#             gammas_now = []
#
#             """逐条光谱拟合"""
#             for row in range(sp.shape[0]):
#                 fig0 = plt.figure(figsize=(8, 6))
#                 ax0 = fig0.add_subplot(111)
#                 sp_now = sp[row, :]
#                 x = wav[min_index:max_index]
#                 y = sp_now[min_index:max_index]
#                 ax0.plot(x, y)
#
#                 # try:
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
#                 min_differences_for_fit = np.abs(wav - 510)
#                 min_index_for_fit = np.argmin(min_differences_for_fit)
#                 max_differences_for_fit = np.abs(wav - 700)
#                 max_index_for_fit = np.argmin(max_differences_for_fit)
#
#                 x_for_fit = wav[min_index_for_fit:max_index_for_fit]
#                 y_for_fit = sp_now[min_index_for_fit:max_index_for_fit]
#                 popt, pcov = curve_fit(lorentzian_plus_gaussian, x_for_fit, y_for_fit, p0=p0, bounds=bounds)
#                 A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3 = popt
#                 mag_now = (A1/np.pi)/(gamma1/2)
#                 ints_now.append(mag_now)
#                 cws_now.append(x1)
#                 gammas_now.append(gamma1)
#                 print(key)
#                 print(f'拟合结果: A1 = {A1:.2f}, mu1 = {x1:.2f}, sigma1 = {gamma1:.2f}, '
#                       f'A2 = {A2:.2f}, mu2 = {x2:.2f}, sigma2 = {gamma2:.2f}',
#                       f'A3 = {A2:.2f}, mu3 = {x3:.2f}, sigma3 = {gamma3:.2f}')
#                 y_fit = lorentzian_plus_gaussian(x, *popt)
#                 y_fit1 = lorentzian(x_for_fit, A1, x1, gamma1)
#                 y_fit2 = gaussian(x_for_fit, A2, x2, gamma2)
#                 y_fit3 = lorentzian(x_for_fit, A3, x3, gamma3)
#                 ax0.plot(x, y_fit, 'r-', label='Fitted Gaussian')
#                 ax0.plot(x_for_fit, y_fit1, 'b--', label='Fitted Gaussian')
#                 ax0.plot(x_for_fit, y_fit2, 'g--', label='Fitted Gaussian')
#                 ax0.plot(x_for_fit, y_fit3, 'm--', label='Fitted Gaussian', linewidth=2)
#                 # except Exception as e:
#                 #     print(e)
#
#                 title = f'{key[:-2]}'
#                 set_figure.set_label_and_title(ax0, title=title, ylabel='Intensity(counts)',
#                                                label_fontsize=25, title_fontsize=25,
#                                                label_font_family='Times New Roman', title_font_family='Times New Roman',
#                                                label_fontweight='bold', title_fontweight='bold',
#                                                label_pad=15, title_pad=15)
#                 set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
#                 set_figure.set_tick(ax0, xbins=16, ybins=10, fontsize=10, fontweight='bold',
#                                     linewidth=3, tick_pad=5, direction='in',
#                                     ticks_xlabel=np.arange(400, 701, 50))  # Normalized
#                 # ax0.grid(True)
#                 plt.tight_layout()
#                 if save_fig == 1:
#                     from src.general.save_figure import save_subfig
#                     plt.savefig(os.path.join(os.path.dirname(datapath1), 'curve_fit-2', f'power_dependent_PL_curve_fit-{key}-No{row}.png'))
#
#                 plt.close(fig0)
#             ints_now = sorted(ints_now)
#             ints.append(np.mean(ints_now[1:-1]))  #去掉最小值和最大值再平均
#             # ints.append(np.mean(ints_now[:]))
#             # ints.append(ints_now[1:-1])

            # """对每个功率下的所有光谱，先求和再拟合"""
            # fig0 = plt.figure(figsize=(8, 6))
            # ax0 = fig0.add_subplot(111)
            # sp_now = np.sum(sp, 0)
            # x = wav[min_index:max_index]
            # y = sp_now[min_index:max_index]
            # ax0.plot(x, y)
            #
            # try:
            #     """三峰拟合"""
            #     p0 = [100, 537, 6,
            #             20, 550, 10,
            #              20, 577, 6]
            #
            #     bounds = ([0, 535, 0,
            #                0, 540, 0,
            #                0, 570, 0],
            #               [100000, 540, 10,
            #                 100000, 565, 12,
            #                 100000, 580, 10])
            #     min_differences_for_fit = np.abs(wav - 510)
            #     min_index_for_fit = np.argmin(min_differences_for_fit)
            #     max_differences_for_fit = np.abs(wav - 700)
            #     max_index_for_fit = np.argmin(max_differences_for_fit)
            #
            #     x_for_fit = wav[min_index_for_fit:max_index_for_fit]
            #     y_for_fit = sp_now[min_index_for_fit:max_index_for_fit]
            #     popt, pcov = curve_fit(lorentzian_plus_gaussian, x_for_fit, y_for_fit, p0=p0, bounds=bounds)
            #     # popt, pcov = curve_fit(triple_lorentzian, x_for_fit, y_for_fit, p0=p0, bounds=bounds)
            #     A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3 = popt
            #     mag_now = (A1/np.pi)/(gamma1/2)
            #     print(key)
            #     print(f'拟合结果: A1 = {A1:.2f}, mu1 = {x1:.2f}, sigma1 = {gamma1:.2f}, '
            #           f'A2 = {A2:.2f}, mu2 = {x2:.2f}, sigma2 = {gamma2:.2f}',
            #           f'A3 = {A2:.2f}, mu3 = {x3:.2f}, sigma3 = {gamma3:.2f}')
            #     y_fit = lorentzian_plus_gaussian(x, *popt)
            #     # y_fit = triple_lorentzian(x, *popt)
            #     y_fit1 = lorentzian(x_for_fit, A1, x1, gamma1)
            #     y_fit2 = gaussian(x_for_fit, A2, x2, gamma2)
            #     y_fit3 = lorentzian(x_for_fit, A3, x3, gamma3)
            #     ax0.plot(x, y_fit, 'r-', label='Fitted Gaussian')
            #     ax0.plot(x_for_fit, y_fit1, 'b--', label='Fitted Gaussian')
            #     ax0.plot(x_for_fit, y_fit2, 'g--', label='Fitted Gaussian')
            #     ax0.plot(x_for_fit, y_fit3, 'm--', label='Fitted Gaussian', linewidth=2)
            # except Exception as e:
            #     print(e)
            #
            # title = f'{key[:-2]}'
            # set_figure.set_label_and_title(ax0, title=title, ylabel='Intensity(counts)',
            #                                label_fontsize=25, title_fontsize=25,
            #                                label_font_family='Times New Roman', title_font_family='Times New Roman',
            #                                label_fontweight='bold', title_fontweight='bold',
            #                                label_pad=15, title_pad=15)
            # set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
            # set_figure.set_tick(ax0, xbins=16, ybins=10, fontsize=10, fontweight='bold',
            #                     linewidth=3, tick_pad=5, direction='in',
            #                     ticks_xlabel=np.arange(400, 701, 50))  # Normalized
            # # ax0.grid(True)
            # plt.tight_layout()
            # if save_fig == 1:
            #     from src.general.save_figure import save_subfig
            #     plt.savefig(os.path.join(os.path.dirname(datapath1), 'curve_fit', f'power_dependent_PL_curve_fit-{key}-No{row}.png'))
            #
            # # plt.close(fig0)
            # ints.append(mag_now)

powers, ints = read_2line_txt(r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6\powers_ints.txt")

fig0 = plt.figure(figsize=(8, 6))
ax0 = fig0.add_subplot(111)

# 将两个列表组合在一起，并根据 list1 排序
zipped_lists = zip(powers, ints)
sorted_zipped_lists = sorted(zipped_lists, key=lambda x: x[0])
# 解压缩得到排序后的 list1 和 list2
powers, ints = zip(*sorted_zipped_lists)
# 将结果转换回列表（因为 zip 返回的是元组）
powers = np.array(list(powers))
ints = np.array(list(ints))

"""保存PL线形拟合数据"""
# save_2line_txt(powers, ints, os.path.dirname(datapath1), 'powers_ints.txt')

ax0.scatter(powers, ints, c='none', marker='^', edgecolors='#d62728', s=40, linewidths=1.5)
"""功率依赖PL拟合"""
popt, pcov = curve_fit(power_saturation, powers, ints)
P_sat, I_inf = popt
ints_fit = power_saturation(powers, *popt)
ax0.plot(powers, ints_fit, '-', color='#d62728', linewidth=2)


plt.yscale('log')
title = f'Excitation power-denpendent intensity\nof peak 1'
set_figure.set_label_and_title(ax0, title=title, xlabel='Excitaion Power(uW)', ylabel='Intensity(counts)',
                               label_fontsize=25, title_fontsize=25,
                               label_font_family='Times New Roman', title_font_family='Times New Roman',
                               label_fontweight='bold', title_fontweight='bold',
                               label_pad=15, title_pad=15)
set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
set_figure.set_tick(ax0, xbins=16, ybins=0, fontsize=10, fontweight='bold',
                    linewidth=3, tick_pad=5, direction='in',
                    ticks_xlabel=np.arange(0, 3001, 500))  # Normalized
# plt.yticks(np.concatenate([np.arange(0, 101, 20), np.arange(200, 1001, 200)]), ['', '', '', '', '', 100, '', '', '', '', 1000])

# ax0.grid(True)
plt.tight_layout()
print(powers)
print(ints)
if save_fig == 1:
    from src.general.save_figure import save_subfig
    plt.savefig(os.path.join(os.path.dirname(datapath1), 'curve_fit-2', f'power_dependent_intensity_of_peak-1.png'))
plt.show()