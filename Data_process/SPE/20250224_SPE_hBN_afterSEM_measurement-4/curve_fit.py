import h5py
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.optimize import curve_fit

from src.general.edit_data import *
from src.general.curve_functions import *
from src.general import set_figure
from src.general.save_data import *



def the_figure(ax, fig, key):
    set_figure.set_label_and_title(ax, title=f'{key[:-2]}')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 901, 50))  # Normalized
    fig.tight_layout()

def the_fig1(ax, fig):
    set_figure.set_label_and_title(ax, title=f'Linewidth of peak-1', xlabel='EHT(kV)', ylabel='Exposure Time(min)', zlabel='FWHM(nm)', mode='3d', zlabel_rotation=90, axis_order=(1, 2, 0))
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(0, 6), change_ticks_xlabel=['5', '10', '15', '5*', '10*', '15*'], ticks_xlabel_rotation=0, mode='3d')
    ax.view_init(elev=20, azim=-45)
    ax.set_zlim([0, 12])
    fig.tight_layout()

datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-4\measurement-4.h5"
save_fig = 0

"""fig0"""
with h5py.File(datapath1, "r") as f:
    data = f['OceanOpticsSpectrometer']

    mag_fits = np.zeros([6, 4])
    wav_fits = np.zeros([6, 4])
    gamma_fits = np.zeros([6, 4])
    mag_max = np.zeros([6, 4])
    for key in data.keys():
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)

        sp = data[key]
        bgd = np.array(sp.attrs['background'])
        wav = np.array(sp.attrs['wavelengths'])
        sp_time = sp.attrs['integration_time'] / 1000
        bgd_time = sp.attrs['background_int'] / 1000
        sp = sp / sp_time
        bgd = bgd / bgd_time
        sp = np.array(sp) - bgd

        x, y = choose_range(wav, sp, min_val=400, max_val=900)

        ax.plot(x, y)

        if '15kV' in key:
            row = 2
        elif '10kV' in key:
            row = 1
        elif '5kV' in key:
            row = 0
        else:
            print('error: kV')

        if '0.5min' in key:
            col = 0
        elif '1min' in key:
            col = 1
        elif '2min' in key:
            col = 2
        elif '5min' in key:
            col = 3
        else:
            print('error: min')

        if '60KX' in key:
            pass
        elif '100KX' in key:
            row += 3
        else:
            print('error: KX')

        """三峰拟合"""
        p0 = [100, 537, 6,
                20, 550, 30,
                 20, 577, 6]

        bounds = ([0, 535, 0,
                   0, 540, 0,
                   0, 570, 0],
                  [100000, 540, 10,
                    100000, 565, 100,
                    100000, 580, 30])

        x_for_fit, y_for_fit = choose_range(wav, sp, min_val=520, max_val=900)
        popt, pcov = curve_fit(lorentzian_2_plus_gaussian_1, x_for_fit, y_for_fit, p0=p0, bounds=bounds)
        A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3 = popt
        mag_now = (A1/np.pi)/(gamma1/2)
        wav_now = x1
        gamma_now = gamma1

        mag_fits[row][col] = mag_now
        mag_max[row][col] = np.max(y_for_fit)
        wav_fits[row][col] = wav_now
        gamma_fits[row][col] = gamma_now

        print(f'拟合结果: A1 = {A1:.2f}, mu1 = {x1:.2f}, sigma1 = {gamma1:.2f}, '
              f'A2 = {A2:.2f}, mu2 = {x2:.2f}, sigma2 = {gamma2:.2f}',
              f'A3 = {A2:.2f}, mu3 = {x3:.2f}, sigma3 = {gamma3:.2f}')
        y_fit = lorentzian_2_plus_gaussian_1(x, *popt)
        y_fit1 = lorentzian(x, A1, x1, gamma1)
        y_fit2 = gaussian(x, A2, x2, gamma2)
        y_fit3 = lorentzian(x, A3, x3, gamma3)
        ax.plot(x, y_fit, 'r-', label='Fitted lorentzian_2_plus_gaussian_1')
        ax.plot(x, y_fit1, 'b--', label='Fitted lorentzian')
        ax.plot(x, y_fit2, 'g--', label='Fitted Gaussian')
        ax.plot(x, y_fit3, 'm--', label='Fitted lorentzian', linewidth=2)

        the_figure(ax, fig, key)

        if save_fig == 1:
            fig.savefig(fr'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-4\curve_fit\20250224_SPE_hBN_afterSEM_measurement4_curve_fit-{key}.png')

"""读取数据"""
# powers, ints, errors = read_lines_txt(r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6\powers_ints-2.txt")
"""保存PL线形拟合数据"""
save_lines_txt(mag_fits, wav_fits, gamma_fits, save_full_path=os.path.join(os.path.dirname(datapath1), 'mag_cw_gamma.txt'))
# save_lines_txt无法保存矩阵

# """peak1"""
# """fig1"""
# fig0 = plt.figure(figsize=(8, 6))
# ax0 = fig0.add_subplot(111, projection='3d')
# x = np.array([0.5, 1, 2, 5])
# y = np.arange(0, 6, 1)
# X, Y = np.meshgrid(x, y)
# Z = gamma_fits
#
# for i in y:
#     ax0.plot(Y[i], X[i], Z[i], 'o-', markeredgecolor='black', markerfacecolor=plt.cm.viridis(i / len(y)), markersize=8, linewidth=1, alpha=1)
#     ax0.plot(Y[i], X[i], np.zeros_like(Z[i]), color='gray', alpha=1)
#
#     polygon = [
#         [Y[i, 0], X[i, 0], 0],  # 左下
#         [Y[i, -1], X[i, -1], 0],  # 右下
#     ]
#     for j in range(len(x) - 1, -1, -1):  # 依次添加点，使得polygon成为一个完整的闭合多边形
#         polygon.append([Y[i, j], X[i, j], Z[i, j]])
#     ax0.add_collection3d(Poly3DCollection([polygon], color=plt.cm.viridis(i / len(y)), alpha=0.5))
#
# the_fig1(ax, fig)
#
# plt.savefig(
#     fr'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-4\curve_fit\20250224_SPE_hBN_afterSEM_measurement4_curve_fit-paras_phase_linewidth_peak-1.png')
#
# """fig2"""
# fig0 = plt.figure(figsize=(8, 6))
# ax0 = fig0.add_subplot(111, projection='3d')
# x = np.array([0.5, 1, 2, 5])
# y = np.arange(0, 6, 1)
# X, Y = np.meshgrid(x, y)
# Z = mag_fits
#
# for i in y:
#     ax0.plot(Y[i], X[i], Z[i], 'o-', markeredgecolor='black', markerfacecolor=plt.cm.viridis(i / len(y)), markersize=8, linewidth=1, alpha=1)
#     ax0.plot(Y[i], X[i], np.zeros_like(Z[i]), color='gray', alpha=1)
#
#     polygon = [
#         [Y[i, 0], X[i, 0], 0],  # 左下
#         [Y[i, -1], X[i, -1], 0],  # 右下
#     ]
#     for j in range(len(x) - 1, -1, -1):  # 依次添加点，使得polygon成为一个完整的闭合多边形
#         polygon.append([Y[i, j], X[i, j], Z[i, j]])
#     ax0.add_collection3d(Poly3DCollection([polygon], color=plt.cm.viridis(i / len(y)), alpha=0.5))
#
# title = f'Magnitude of peak-1'
# set_figure.set_label_and_title(ax0, title=title, xlabel='Process time(min)', ylabel='Intensity(counts)',
#                                label_fontsize=20, title_fontsize=25,
#                                label_font_family='Times New Roman', title_font_family='Times New Roman',
#                                label_fontweight='bold', title_fontweight='bold',
#                                label_pad=15, title_pad=5, mode='3d')
# set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
# set_figure.set_tick(ax0, xbins=6, ybins=5, fontsize=15, fontweight='bold',
#                     linewidth=3, tick_pad=5, direction='in', mode='3d')  # Normalized
# plt.xticks(np.arange(0, 6), ['5', '10', '15', '5*', '10*', '15*'], rotation=0)
# ax0.set_ylabel(ylabel='Exposure Time(min)', labelpad=15)
# ax0.set_xlabel(xlabel='EHT(kV)', labelpad=15)
# ax0.zaxis.set_rotate_label(False)  # 关闭默认旋转设置
# ax0.set_zlabel(zlabel='Intensity(counts)', rotation=90, labelpad=15)
# # ax0.grid(True)
# ax0.view_init(elev=20, azim=45)
# # ax0.view_init(elev=0, azim=0)
# plt.tight_layout()
#
# from src.general.save_figure import save_subfig
# plt.savefig(
#     fr'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-4\curve_fit\20250224_SPE_hBN_afterSEM_measurement4_curve_fit-paras_phase_magnitude_peak-1.png')
#
# """fig3"""
# fig0 = plt.figure(figsize=(8, 6))
# ax0 = fig0.add_subplot(111, projection='3d')
# x = np.array([0.5, 1, 2, 5])
# y = np.arange(0, 6, 1)
# X, Y = np.meshgrid(x, y)
# Z = wav_fits
#
# for i in y:
#     ax0.plot(Y[i], X[i], Z[i], 'o-', markeredgecolor='black', markerfacecolor=plt.cm.viridis(i / len(y)), markersize=8, linewidth=1, alpha=1)
#     ax0.plot(Y[i], X[i], np.zeros_like(Z[i])+535, color='gray', alpha=1)
#
#     polygon = [
#         [Y[i, 0], X[i, 0], 535],  # 左下
#         [Y[i, -1], X[i, -1], 535],  # 右下
#     ]
#     for j in range(len(x) - 1, -1, -1):  # 依次添加点，使得polygon成为一个完整的闭合多边形
#         polygon.append([Y[i, j], X[i, j], Z[i, j]])
#     ax0.add_collection3d(Poly3DCollection([polygon], color=plt.cm.viridis(i / len(y)), alpha=0.5))
#
# title = f'Center-wavelength of peak-1'
# set_figure.set_label_and_title(ax0, title=title, xlabel='Process time(min)', ylabel='Intensity(counts)',
#                                label_fontsize=20, title_fontsize=25,
#                                label_font_family='Times New Roman', title_font_family='Times New Roman',
#                                label_fontweight='bold', title_fontweight='bold',
#                                label_pad=15, title_pad=5, mode='3d')
# set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
# set_figure.set_tick(ax0, xbins=6, ybins=5, fontsize=15, fontweight='bold',
#                     linewidth=3, tick_pad=5, direction='in', mode='3d')  # Normalized
# plt.xticks(np.arange(0, 6), ['5', '10', '15', '5*', '10*', '15*'], rotation=0)
# ax0.set_ylabel(ylabel='Exposure Time(min)', labelpad=15)
# ax0.set_xlabel(xlabel='EHT(kV)', labelpad=15)
# ax0.zaxis.set_rotate_label(False)  # 关闭默认旋转设置
# ax0.set_zlabel(zlabel='Wavelength(nm)', rotation=90, labelpad=15)
# # ax0.grid(True)
# ax0.view_init(elev=20, azim=45)
# # ax0.view_init(elev=0, azim=0)
# ax0.set_zlim([535, 540])
# plt.tight_layout()
#
# from src.general.save_figure import save_subfig
# plt.savefig(
#     fr'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-4\curve_fit\20250224_SPE_hBN_afterSEM_measurement4_curve_fit-paras_phase_centerwavelength_peak-1.png')
#
# """fig4"""
# fig0 = plt.figure(figsize=(8, 6))
# ax0 = fig0.add_subplot(111, projection='3d')
# x = np.array([0.5, 1, 2, 5])
# y = np.arange(0, 6, 1)
# X, Y = np.meshgrid(x, y)
# Z = mag_max
#
# for i in y:
#     ax0.plot(Y[i], X[i], Z[i], 'o-', markeredgecolor='black', markerfacecolor=plt.cm.viridis(i / len(y)), markersize=8, linewidth=1, alpha=1)
#     ax0.plot(Y[i], X[i], np.zeros_like(Z[i]), color='gray', alpha=1)
#
#     polygon = [
#         [Y[i, 0], X[i, 0], 0],  # 左下
#         [Y[i, -1], X[i, -1], 0],  # 右下
#     ]
#     for j in range(len(x) - 1, -1, -1):  # 依次添加点，使得polygon成为一个完整的闭合多边形
#         polygon.append([Y[i, j], X[i, j], Z[i, j]])
#     ax0.add_collection3d(Poly3DCollection([polygon], color=plt.cm.viridis(i / len(y)), alpha=0.5))
#
# title = f'Maximum of curve'
# set_figure.set_label_and_title(ax0, title=title, xlabel='Process time(min)', ylabel='Intensity(counts)',
#                                label_fontsize=20, title_fontsize=25,
#                                label_font_family='Times New Roman', title_font_family='Times New Roman',
#                                label_fontweight='bold', title_fontweight='bold',
#                                label_pad=15, title_pad=5, mode='3d')
# set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
# set_figure.set_tick(ax0, xbins=6, ybins=5, fontsize=15, fontweight='bold',
#                     linewidth=3, tick_pad=5, direction='in', mode='3d')  # Normalized
# plt.xticks(np.arange(0, 6), ['5', '10', '15', '5*', '10*', '15*'], rotation=0)
# ax0.set_ylabel(ylabel='Exposure Time(min)', labelpad=15)
# ax0.set_xlabel(xlabel='EHT(kV)', labelpad=15)
# ax0.zaxis.set_rotate_label(False)  # 关闭默认旋转设置
# ax0.set_zlabel(zlabel='Peak Intensity(counts)', rotation=90, labelpad=15)
# # ax0.grid(True)
# ax0.view_init(elev=20, azim=45)
# # ax0.view_init(elev=0, azim=0)
# plt.tight_layout()
#
# if save_fig == 1:
#     plt.savefig(
#         fr'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-4\curve_fit\20250224_SPE_hBN_afterSEM_measurement4_curve_fit-paras_phase_Maximum_of_peaks.png')
plt.show()