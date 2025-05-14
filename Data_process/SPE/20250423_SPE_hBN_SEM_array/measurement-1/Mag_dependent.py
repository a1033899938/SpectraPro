import os.path

import numpy as np
from numpy.core.numeric import infty
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import h5py
import matplotlib.pyplot as plt
from matplotlib import rcParams

from src.general import set_figure
from src.general.curve_functions import *
from src.general.edit_data import choose_range
from src.general.save_data import *

def the_figure(ax, key):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'{key[:-2]}', ylabel='Intensity(counts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 901, 50), ticks_ylabel=np.arange(0, 1.1, 0.1))  # Normalized
    ax.legend()
    set_figure.set_legend(ax, legend_labels=None)
    plt.tight_layout()

def the_figure_1(ax1, name):
    """P—I"""
    set_figure.set_label_and_title(ax1, title=f'Measurement  sequence\nof {name}',
                                   xlabel='Measurement  sequence', ylabel=r'Intensity(cts/s)')
    set_figure.set_spines(ax1)
    set_figure.set_tick(ax1, ticks_xlabel=np.arange(0, 21, 5))  # Normalized
    plt.tight_layout()

def the_figure_2(ax2, legends):
    set_figure.set_label_and_title(ax2, title=f'Intensity Variation over Time Series',
                                   xlabel='Measurement  sequence', ylabel='Intensity(cts/s)')
    set_figure.set_spines(ax2)
    set_figure.set_tick(ax2, ticks_xlabel=np.arange(0, 21, 5))
    set_figure.set_legend(ax2, legend_labels=legends)

datapath1 = r"D:\ExpData\SPE\20250423_SPE_hBN_SEM_array\measurement-1.h5"
save_fig = 1

"""fig0"""
with h5py.File(datapath1, "r") as f:
    data = f['OceanOpticsSpectrometer']
    bgd = np.array(data['sub_1'].attrs['background'])
    bgd_time = data['sub_1'].attrs['background_int'] / 1000
    wav = np.array(data['sub_1'].attrs['wavelengths'])
    bgd = bgd / bgd_time

    keys_sub = ['sub_1',
                'sub_2',
                'sub_3',
                'sub_4',
                'sub_5']

    keys_5s = ['time_series_5s-1_0',
               'time_series_5s-2_0',
              'time_series_5s-3_0',
              'time_series_5s-4_0',
              'time_series_5s-5_0',
              'time_series_5s-6_0',
              'time_series_5s-7_0',
              'time_series_5s-8_0',
              'time_series_5s-9_0',
              'time_series_5s-10_0']

    keys_10s = ['time_series_10s-0',
                'time_series_10s-1',
                'time_series_10s-3_0',
                'time_series_10s-4_0',
                'time_series_10s-5_0',
                'time_series_10s-6_0',
                'time_series_10s-7_0',
                'time_series_10s-8_0',
                'time_series_10s-9_0',
                'time_series_10s-10_0',]

    keys_30s = ['time_series_30s-1_0',
                'time_series_30s-2_0',
                'time_series_30s-3_0',
                'time_series_30s-4_0',
                'time_series_30s-5_0',
                'time_series_30s-6_0',
                'time_series_30s-7_0',
                'time_series_30s-8_0',
                'time_series_30s-9_0',
                'time_series_30s-10_0']

    keys_60s = ['time_series_60s-1_0',
                'time_series_60s-2_0',
                'time_series_60s-3_0',
                'time_series_60s-4_0',
                'time_series_60s-5_0',
                'time_series_60s-6_0',
                'time_series_60s-7_0',
                'time_series_60s-8_0',
                'time_series_60s-9_0',
                'time_series_60s-10_0']

    keys_120s = ['time_series_120s-1_0',
                 'time_series_120s-2_0',
                 'time_series_120s-3_0',
                 'time_series_120s-4_0',
                 'time_series_120s-5_0',
                 'time_series_120s-6_0',
                 'time_series_120s-7_0',
                 'time_series_120s-8_0',
                 'time_series_120s-9_0',
                 'time_series_120s-10_0']

    keys_this_hBN = ['thishBN_woSEM-1_0',
                     'thishBN_woSEM-2_0',
                     'thishBN_woSEM-3_0',
                     'thishBN_woSEM-4_0',
                     'thishBN_woSEM-5_0']

    keys_beside_hBN = ['besidehBN_woSEM-1_0',
                       'besidehBN_woSEM-2_0',
                       'besidehBN_woSEM-3_0',
                       'besidehBN_woSEM-4_0',
                       'besidehBN_woSEM-5_0']

    keys_all = [keys_sub, keys_this_hBN, keys_beside_hBN,
                keys_5s, keys_10s, keys_30s, keys_60s, keys_120s]
    series_names = ['SiO2', 'hBN_nonIrradiated','hBN_nonIrradiated-2',
                    'hBN_Irradiated-5s', 'hBN_Irradiated-10s', 'hBN_Irradiated-30s', 'hBN_Irradiated-60s', 'hBN_Irradiated-120s']

    ints_all = []
    errs_max = []
    errs_min = []
    for n, key_all in enumerate(keys_all):
        spot_number = len(key_all)
        ints = np.zeros([spot_number, 20])
        print(np.shape(ints))
        fig1 = plt.figure(figsize=(8, 6))
        ax1 = fig1.add_subplot(111)
        for i, key in enumerate(key_all):
            sps = data[key]
            bgd = np.array(sps.attrs['background'])
            wav = np.array(sps.attrs['wavelengths'])
            sp_time = sps.attrs['integration_time'] / 1000
            bgd_time = sps.attrs['background_int'] / 1000
            bgd, _ = np.meshgrid(bgd, np.arange(0, sps.shape[0]))
            sps = sps / sp_time
            bgd = bgd / bgd_time
            sps = sps - bgd

            x = wav
            y = np.arange(sps.shape[0])
            sps = np.array(sps)
            x, Z = choose_range(wav, sps, min_val=400, max_val=1100, axis=1)
            print(np.shape(x))
            print(np.shape(Z))

            # fig = plt.figure(figsize=(8, 6))
            # ax = fig.add_subplot(111)
            for j in y:
                y = Z[j, :]


                # ax.plot(x, y)

                """三峰拟合"""
                p0 = [10, 550, 100]

                bounds = ([0, 400, 0],
                          [1000,1100,200])
                x_for_fit, y_for_fit = choose_range(x, y, min_val=400, max_val=900)
                popt, pcov = curve_fit(gaussian, x_for_fit, y_for_fit, p0=p0, bounds=bounds)
                A, mu, gamma= popt
                ints[i][j] = A
                print(f'拟合结果: '
                      f'A = {A:.2f}',
                      f'mu = {mu:.2f}',
                      f'gamma = {gamma:.2f}')
                y_fit = gaussian(x_for_fit, *popt)
                # ax.plot(x_for_fit, y_fit, 'r-', label='Fitted gaussian')
                # the_figure(ax, key)
                # if save_fig == 1:
                #     plt.savefig(os.path.join(os.path.dirname(datapath1), 'curve_fit', f'power_dependent_PL_curve_fit-{key}.png'))

        # i：曝光s数
        # j：第几个点
        mean_int = np.mean(ints, axis=0)
        err_max = np.max(ints, axis=0)
        err_min = np.min(ints, axis=0)
        ints_all.append(mean_int)
        errs_max.append(err_max)
        errs_min.append(err_min)

        for i in range(spot_number):
            ax1.plot(ints[i])
            the_figure_1(ax1, series_names[n])
        if save_fig == 1:
            fig1.savefig(os.path.join(os.path.dirname(datapath1), 'curve_fit', f'time_series_{series_names[n]}.png'))

print(np.shape(ints_all))
print(np.shape(errs_max))
print(np.shape(errs_min))
fig2 = plt.figure(figsize=(8, 6))
ax2 = fig2.add_subplot(111)

import matplotlib.colors as mcolors
color_sequence = ['#FF4136', '#0074D9', '#2ECC40', '#FFDC00', '#B10DC9', '#FF851B', '#00FFFF', '#7F7F7F']
num_lines = len(color_sequence)

for i in range(np.shape(ints_all)[0]):
    x = np.arange(0, 20)
    y = ints_all[i]
    err_max = errs_max[i]
    err_min = errs_min[i]
    color = color_sequence[i % len(color_sequence)]  # 循环使用颜色序列
    h, s, v = mcolors.rgb_to_hsv(mcolors.to_rgb(color))  # 将颜色转换为 HSV 空间
    s = 0.3  # 调整饱和度为 30%
    new_color = mcolors.hsv_to_rgb((h, s, v))  # 将调整后的 HSV 颜色转换回 RGB
    ax2.errorbar(x, y, yerr=[err_min, err_max], fmt='-^', color=color, ecolor=new_color, capsize=10)
    the_figure_2(ax2, series_names)

if save_fig == 1:
    fig2.savefig(os.path.join(os.path.dirname(datapath1), 'curve_fit', f'time_series.png'))
plt.show()