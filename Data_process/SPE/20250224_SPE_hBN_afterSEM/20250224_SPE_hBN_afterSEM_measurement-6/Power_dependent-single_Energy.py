import h5py
import os
import matplotlib.pyplot as plt
import numpy as np

from src.general.figure import set_figure
from src.general.figure.set_figure import set_legend
from src.general.numerical.edit_data import choose_range
from src.my_style.my_mapping_para import *

def load_data(h5_file, dir_name, sp_names, le=None, save_folder=None):
    with h5py.File(h5_file, "r") as f:
        # 读取sp目录
        data = f[dir_name]

        # 读取目录下的第一个sp的bgd和wav，并对积分时间作归一化
        bgd = np.array(data[sp_names[0]].attrs['background'])
        bgd_time = data[sp_names[0]].attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        wav = np.array(data[sp_names[0]].attrs['wavelengths'])

        ints = []
        cws = []
        gammas = []
        # 历遍所有sp
        for i, key in enumerate(sp_names):
            fig = plt.figure(figsize=(8, 6), dpi=200)
            ax = fig.add_subplot(111)

            sp = data[key]
            sp_time = sp.attrs['integration_time'] / 1000
            sp = np.array(sp)
            sp = sp / sp_time
            sp = sp - bgd

            """数据处理区域"""
            sp_max = np.max(sp)
            sp = sp/sp_max
            energy = 1240 / wav
            x, y = choose_range(energy, sp, x1=1.7, x2=2.5)
            ax.plot(x, y, label='Exp. data')
            # 曲线拟合
            x_for_fit, y_for_fit = choose_range(energy, sp, x1=1.7, x2=2.5)
            # fitting_paras = quatra_peaks_fitting_voigt_energy(x_for_fit, y_for_fit, ax=ax, maxfev=10000)  # com
            fitting_paras = quatra_peaks_fitting2(x_for_fit, y_for_fit, ax=ax, if_x_unit_energy=True)
            # # 储存拟合参数
            # ints.append(fitting_paras["peak1"]["magnitude"])
            # cws.append(fitting_paras["peak1"]["center"])
            # gammas.append(fitting_paras["peak1"]["fwhm"])

            the_figure(ax, title=f"Lorentzian-Gaussian Multi-Peak Fit")  # com
            if save_folder:
                fig.savefig(os.path.join(save_folder, f'{le[i]}uW.png'))
    return ints, cws, gammas

def the_figure(ax, title):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=title, xlabel='Energy(eV)', ylabel='Normalized Intensity(cts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(1.7, 2.6, 0.2), ticks_ylabel=np.arange(0, 1.1, 0.2), show_ylabel_every_ticks=2, show_xlabel_every_ticks=2)  # Normalized
    set_legend(ax, font_size=13, location='best')
    plt.tight_layout()

def the_figure1(ax1):
    """P—I"""
    set_figure.set_label_and_title(ax1, title=f'Excitation power-denpendent intensity\nof peak 1',
                                   xlabel='Excitaion Power(uW)', ylabel='Intensity(cts)')
    set_figure.set_spines(ax1)
    set_figure.set_tick(ax1, ticks_xlabel=np.arange(0, 3001, 500))  # Normalized
    plt.tight_layout()

def the_figure2(ax2):
    """P-CW"""
    set_figure.set_label_and_title(ax2, title=f'Excitation power-denpendent center wavelength\nof peak 1',
                                   xlabel='Excitaion Power(uW)', ylabel='Center Wavelength(nm)')
    set_figure.set_spines(ax2)
    set_figure.set_tick(ax2, ticks_xlabel=np.arange(0, 3001, 500),
                        ticks_ylabel=np.arange(535, 541, 1))
    plt.tight_layout()

def the_figure3(ax3):
    """P-FWHM"""
    set_figure.set_label_and_title(ax3, title=f'Excitation power-denpendent FWHM\nof peak 1',
                                   xlabel='Excitaion Power(uW)', ylabel='FWHM(nm)')
    set_figure.set_spines(ax3)
    set_figure.set_tick(ax3, ticks_xlabel=np.arange(0, 3001, 500), ticks_ylabel=np.arange(0, 11, 1))
    plt.tight_layout()

if __name__ == '__main__':
    """路径"""
    h5_file = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6\measurement-6.h5"
    save_folder = os.path.join(os.path.dirname(h5_file), 'single_spectrum-0', 'curve_fit')
    npz_file = os.path.join(os.path.dirname(save_folder), f'PL_mapping.npz')
    fig1_file = os.path.join(os.path.dirname(save_folder), f'power_dependent_intensity_of_peak-1.png')
    fig2_file = os.path.join(os.path.dirname(save_folder), f'power_dependent_center_wavelength_of_peak-1.png')
    fig3_file = os.path.join(os.path.dirname(save_folder), f'power_dependent_FWHM_of_peak-1.png')

    # 创建文件夹
    if not os.path.exists(save_folder):
        os.makedirs(save_folder, exist_ok=True)

    """加载并保存拟合数据"""
    dir_name = 'OceanOpticsSpectrometer'
    sp_names = ['hBN_afterSEM_5kV_5min_60KX_P10uW_0',
                'hBN_afterSEM_5kV_5min_60KX_P20uW_0',
                'hBN_afterSEM_5kV_5min_60KX_P50uW_0',
                'hBN_afterSEM_5kV_5min_60KX_P100uW_0',
                'hBN_afterSEM_5kV_5min_60KX_P200uW_0',
                'hBN_afterSEM_5kV_5min_60KX_P500uW_0',
                'hBN_afterSEM_5kV_5min_60KX_P1000uW_0',
                'hBN_afterSEM_5kV_5min_60KX_P2000uW_0',
                'hBN_afterSEM_5kV_5min_60KX_P3000uW_0']
    powers = [10, 20, 50, 100, 200, 500, 1000, 2000, 3000]
    ints, cws, gammas = load_data(h5_file, dir_name, sp_names, le=powers, save_folder=save_folder)
    # 保存拟合数据
    np.savez(npz_file, powers=powers, ints=ints, cws=cws, gammas=gammas)

    # """作图并保存"""
    # # 读取拟合数据
    # data = np.load(npz_file)
    #
    # # 作图
    # powers = data['powers']
    # ints = data['ints']
    # cws = data['cws']
    # gammas = data['gammas']
    #
    # """fig1-intensity"""
    # fig1 = plt.figure(figsize=(8*1.1, 6*1.2))
    # fig2 = plt.figure(figsize=(8*1.1, 6*1.2))
    # fig3 = plt.figure(figsize=(8*1.1, 6*1.2))
    # ax1 = fig1.add_subplot(111)
    # ax2 = fig2.add_subplot(111)
    # ax3 = fig3.add_subplot(111)
    #
    # x = np.array(powers)
    #
    # y = np.array(ints)
    # ax1.plot(x, y, 'o-', markersize=10, markerfacecolor='none', markeredgecolor='blue', markeredgewidth=1.5)
    #
    # y = np.array(cws)
    # ax2.plot(x, y, 'o-', markersize=10, markerfacecolor='none', markeredgecolor='blue', markeredgewidth=1.5)
    #
    # y = np.array(gammas)
    # ax3.plot(x, y, 'o-', markersize=10, markerfacecolor='none', markeredgecolor='blue', markeredgewidth=1.5)

    # 保存图片
    # the_figure1(ax1)
    # fig1.savefig(fig1_file)
    # the_figure2(ax2)
    # fig2.savefig(fig2_file)
    # the_figure3(ax3)
    # fig3.savefig(fig3_file)

    plt.show()