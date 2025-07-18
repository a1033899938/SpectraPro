import os.path
from scipy.optimize import curve_fit
import h5py
from src.general.figure import set_figure


def gaussian(x, A, mu, sigma):
    return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))


def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
    return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))


import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

datapath1 = r"D:\ExpData\Fellows\WYQ\20250313_WYQ_Cube\20250313_WYQ_Cube.h5"
save_fig = 1

"""fig0"""
with h5py.File(datapath1, "r") as f:
    data = f['OceanOpticsSpectrometer']

    fig0 = plt.figure(figsize=(8, 6))
    ax0 = fig0.add_subplot(111)
    legend_labels_afterSEM = []
    ref = np.array(data['reference_new_0'])
    ref_time = data['reference_new_0'].attrs['integration_time'] / 1000
    ref = ref / ref_time
    bgd = np.array(data['bgd_light_0'])
    bgd_time = data['bgd_light_0'].attrs['integration_time'] / 1000
    bgd = bgd / bgd_time

    A_fits = []
    mu_fits = []
    sigma_fits = []
    print(data.keys())
    for key in data.keys():
        # if key != '100nmAgNC-6#_NC-5_0':
        #     continue
        if '100nmAgNC' in key and int(key.split('-')[-1].split('_')[0]) >= 5 and int(key.split('-')[-1].split('_')[0]) != 11 and int(key.split('-')[-1].split('_')[0]) != 12:
            sp = data[key]
            wav = np.array(sp.attrs['wavelengths'])
            sp_time = sp.attrs['integration_time'] / 1000
            sp = sp / sp_time
            sp = (np.array(sp) - bgd) / (ref - bgd)
            # sp = sp / np.max(sp)  # 强度归一化

            min_differences = np.abs(wav - 500)
            min_index = np.argmin(min_differences)
            max_differences = np.abs(wav - 900)
            max_index = np.argmin(max_differences)

            x = wav[min_index:max_index]
            y = sp[min_index:max_index]

            # y = y / np.max(y)

            legend_labels_afterSEM.append(key)
            ax0.plot(x, y)

# set_figure.set_label_and_title(ax0, title = '100nmAgNC Scattering')
# set_figure.set_spines(ax0)
# set_figure.set_tick(ax0, xbins=16, ybins=10, fontsize=10, fontweight='bold',
#                     linewidth=3, tick_pad=5, direction='in',
#                     ticks_xlabel=np.arange(300, 1101, 50))  # Normalized
# set_figure.set_legend(ax0, legend_labels=legend_labels_afterSEM, font_size=8, location='upper right')
# ax0.grid(True)
# plt.tight_layout()
# if save_fig == 1:
#     from src.general.save_figure import save_subfig
#     plt.savefig(os.path.join(os.path.dirname(datapath1), 'your_save_figure.png'))


"""fig1"""  # 曲线拟合与直方图
with h5py.File(datapath1, "r") as f:
    data = f['OceanOpticsSpectrometer']

    legend_labels_afterSEM = []
    ref = np.array(data['reference_new_0'])
    ref_time = data['reference_new_0'].attrs['integration_time'] / 1000
    ref = ref / ref_time
    bgd = np.array(data['bgd_light_0'])
    bgd_time = data['bgd_light_0'].attrs['integration_time'] / 1000
    bgd = bgd / bgd_time

    A_fits = []
    mu_fits = []
    sigma_fits = []
    for key in data.keys():
        # if key != '100nmAgNC-6#_NC-16_0':
        #     break
        if '100nmAgNC' in key and int(key.split('-')[-1].split('_')[0]) >= 5 and int(key.split('-')[-1].split('_')[0]) != 11 and int(key.split('-')[-1].split('_')[0]) != 12:
            fig0 = plt.figure(figsize=(8, 6))
            ax0 = fig0.add_subplot(111)
            sp = data[key]
            wav = np.array(sp.attrs['wavelengths'])
            sp_time = sp.attrs['integration_time'] / 1000
            sp = sp / sp_time
            sp = (np.array(sp) - bgd) / (ref - bgd)

            min_differences = np.abs(wav - 300)
            min_index = np.argmin(min_differences)
            max_differences = np.abs(wav - 1100)
            max_index = np.argmin(max_differences)

            x = wav[min_index:max_index]
            y = sp[min_index:max_index]

            legend_labels_afterSEM.append(key)
            ax0.plot(x, y)

            # try:
            #     """单峰拟合"""
            #     p0 = [1, 700, 50]  # 初始猜想值
            #
            #     bounds = ([0, 650, 20],
            #               [2, 750, 100])  # 边界限定
            #     min_differences_for_fit = np.abs(wav - 600)
            #     min_index_for_fit = np.argmin(min_differences_for_fit)
            #     max_differences_for_fit = np.abs(wav - 750)
            #     max_index_for_fit = np.argmin(max_differences_for_fit)
            #
            #     x_for_fit = wav[min_index_for_fit:max_index_for_fit]
            #     y_for_fit = sp[min_index_for_fit:max_index_for_fit]
            #     popt, pcov = curve_fit(gaussian, x_for_fit, y_for_fit, p0=p0, bounds=bounds)
            #
            #     A, mu, sigma = popt
            #     A_fits.append(A)
            #     mu_fits.append(mu)
            #     sigma_fits.append(sigma)
            #
            #     print(f'拟合结果: A1 = {A:.2f}, mu1 = {mu:.2f}, sigma1 = {sigma:.2f}')
            #     y_fit = gaussian(x_for_fit, *popt)
            #     ax0.plot(x_for_fit, y_fit, 'r-', label='Fitted Gaussian')
            # except Exception as e:
            #     print(e)

            # if save_fig == 1:
            #     from src.general.save_figure import save_subfig
            #     plt.savefig(os.path.join(os.path.dirname(datapath1), f'curve_fit_{key}.png'))
# fig0 = plt.figure(figsize=(8, 6))
# ax0 = fig0.add_subplot(111)
# ax0.hist(mu_fits)  # 中心波长
# ax0.hist(sigma_fits)  # 半高宽


def the_figure(ax):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'', ylabel='Scattering Intensity(a.u.)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(500, 901, 50))  # Normalized
    plt.tight_layout()

the_figure(ax0)
# set_figure.set_label_and_title(ax0, ylabel='Frequency', title = '100nmAgNC Center Wavelength histogram')  # 中心波长
# # set_figure.set_label_and_title(ax0, xlabel='FWHM(nm)', ylabel='Frequency', title = '100nmAgNC FWHM histogram')  # 半高宽
# set_figure.set_spines(ax0)
# set_figure.set_tick(ax0, xbins=16, ybins=10, fontsize=10, fontweight='bold',
#                     linewidth=3, tick_pad=5, direction='in',
#                     ticks_xlabel=np.arange(300, 1101, 50))  # 中心波长
# # set_figure.set_tick(ax0, xbins=16, ybins=10, fontsize=10, fontweight='bold',
# #                     linewidth=3, tick_pad=5, direction='in') # 半高宽
# ax0.grid(True)
# plt.tight_layout()
# if save_fig == 1:
#     from src.general.save_figure import save_subfig
#     plt.savefig(os.path.join(os.path.dirname(datapath1), 'CW_histogram.png'))  # 中心波长
#     # plt.savefig(os.path.join(os.path.dirname(datapath1), 'Sigama_histogram.png'))  # 半高宽
plt.show()