import os.path

import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import h5py
import matplotlib.pyplot as plt
from matplotlib import rcParams

from src.general import set_figure
from src.general.curve_functions import *
from src.general.edit_data import choose_range
from src.general.save_data import *

def the_figure(ax, legend_labels):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'405 / 450 nm Laser Excitation', ylabel='Intensity(counts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 901, 50))  # Normalized
    set_figure.set_legend(ax, legend_labels=legend_labels)
    plt.tight_layout()

datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-8\20250224_SPE_hBN_afterSEM_measurement-8.h5"
save_fig = 1

"""fig0"""
with h5py.File(datapath1, "r") as f:
    data = f['OceanOpticsSpectrometer']
    bgd = np.array(data['hBN_afterSEM_5kV_2min_60KX_405ex_500uW_0'].attrs['background'])
    bgd_time = data['hBN_afterSEM_5kV_2min_60KX_405ex_500uW_0'].attrs['background_int'] / 1000
    wav = np.array(data['hBN_afterSEM_5kV_2min_60KX_405ex_500uW_0'].attrs['wavelengths'])
    bgd = bgd / bgd_time

    keys = ['hBN_afterSEM_5kV_2min_60KX_405ex_500uW_0',
            'hBN_afterSEM_5kV_2min_60KX_405ex_500uW_1',]

    legend_labels = ['405 nm', '450 nm']
    ints = []
    cws = []
    gammas = []
    int_errors = []
    cw_errors = []
    gamma_errors = []
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    for i, key in enumerate(keys):
            sp = data[key]
            sp_time = sp.attrs['integration_time'] / 1000
            sp = np.array(sp)
            sp = sp / sp_time
            sp = sp - bgd


            x, y = choose_range(wav, sp, min_val=400, max_val=900)
            ax.plot(x, y)

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
            # 选择用于拟合的数据波段
            x_for_fit, y_for_fit = choose_range(wav, sp, min_val=510, max_val=900)
            popt, pcov = curve_fit(lorentzian_2_plus_gaussian_1, x_for_fit, y_for_fit, p0=p0, bounds=bounds)
            A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3 = popt
            mag_now = (A1/np.pi)/(gamma1/2)
            ints.append(mag_now)
            cws.append(x1)
            gammas.append(gamma1)
            print(f'拟合结果: '
                  f'A1 = {A1:.2f}, mu1 = {x1:.2f}, sigma1 = {gamma1:.2f}',
                  f'A2 = {A2:.2f}, mu2 = {x2:.2f}, sigma2 = {gamma2:.2f}',
                  f'A3 = {A2:.2f}, mu3 = {x3:.2f}, sigma3 = {gamma3:.2f}')
            y_fit = lorentzian_2_plus_gaussian_1(x, *popt)
            y_fit1 = lorentzian(x_for_fit, A1, x1, gamma1)
            y_fit2 = gaussian(x_for_fit, A2, x2, gamma2)
            y_fit3 = lorentzian(x_for_fit, A3, x3, gamma3)
            # ax.plot(x, y_fit, 'r-', label='Fitted lorentzian_2_plus_gaussian_1')
            # ax.plot(x_for_fit, y_fit1, 'b--', label='Fitted lorentzian')
            # ax.plot(x_for_fit, y_fit2, 'g--', label='Fitted Gaussian')
            # ax.plot(x_for_fit, y_fit3, 'm--', label='Fitted lorentzian')

            the_figure(ax, legend_labels)
            if save_fig == 1:
                plt.savefig(os.path.join(os.path.dirname(datapath1), f'Excitation_wavelength_dependent_PL.png'))
plt.show()