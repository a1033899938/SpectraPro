import os.path
from scipy.optimize import curve_fit
import h5py
import matplotlib.pyplot as plt

from src.general import set_figure
from src.general.curve_functions import *
from src.general.edit_data import choose_range

def the_figure(ax, key):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'{key[:-2]}', ylabel='Intensity(counts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 901, 50))  # Normalized
    ax.legend()
    set_figure.set_legend(ax, legend_labels=None)
    plt.tight_layout()

def the_figure_1(ax1):
    """P—I"""
    set_figure.set_label_and_title(ax1, title=f'Excitation power-denpendent intensity\nof peak 1',
                                   xlabel='Excitaion Power(uW)', ylabel='Intensity(counts)')
    set_figure.set_spines(ax1)
    set_figure.set_tick(ax1, ticks_xlabel=np.arange(0, 3001, 500))  # Normalized
    plt.tight_layout()

def the_figure_2(ax2):
    """P-CW"""
    set_figure.set_label_and_title(ax2, title=f'Excitation power-denpendent center wavelength\nof peak 1',
                                   xlabel='Excitaion Power(uW)', ylabel='Center Wavelength(nm)')
    set_figure.set_spines(ax2)
    set_figure.set_tick(ax2, ticks_xlabel=np.arange(0, 3001, 500),
                        ticks_ylabel=np.arange(535, 541, 1))

def the_figure_3(ax3):
    """P-FWHM"""
    set_figure.set_label_and_title(ax3, title=f'Excitation power-denpendent FWHM\nof peak 1',
                                   xlabel='Excitaion Power(uW)', ylabel='FWHM(nm)')
    set_figure.set_spines(ax3)
    set_figure.set_tick(ax3, ticks_xlabel=np.arange(0, 3001, 500), ticks_ylabel=np.arange(0, 11, 1))

datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6\measurement-6.h5"
save_fig = 0

"""fig0"""
with h5py.File(datapath1, "r") as f:
    data = f['OceanOpticsSpectrometer']
    bgd = np.array(data['hBN_afterSEM_5kV_5min_60KX_P10uW_0'].attrs['background'])
    bgd_time = data['hBN_afterSEM_5kV_5min_60KX_P10uW_0'].attrs['background_int'] / 1000
    wav = np.array(data['hBN_afterSEM_5kV_5min_60KX_P10uW_0'].attrs['wavelengths'])
    bgd = bgd / bgd_time

    keys = ['hBN_afterSEM_5kV_5min_60KX_P10uW_0',
            'hBN_afterSEM_5kV_5min_60KX_P20uW_0',
            'hBN_afterSEM_5kV_5min_60KX_P50uW_0',
            'hBN_afterSEM_5kV_5min_60KX_P100uW_0',
            'hBN_afterSEM_5kV_5min_60KX_P200uW_0',
            'hBN_afterSEM_5kV_5min_60KX_P500uW_0',
            'hBN_afterSEM_5kV_5min_60KX_P1000uW_0',
            'hBN_afterSEM_5kV_5min_60KX_P2000uW_0',
            'hBN_afterSEM_5kV_5min_60KX_P3000uW_0']

    legend_labels = []
    ints = []
    cws = []
    gammas = []
    for key in keys:
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111)
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
            ax.plot(x, y_fit, 'r-', label='Fitted lorentzian_2_plus_gaussian_1')
            ax.plot(x_for_fit, y_fit1, 'b--', label='Fitted lorentzian')
            ax.plot(x_for_fit, y_fit2, 'g--', label='Fitted Gaussian')
            ax.plot(x_for_fit, y_fit3, 'm--', label='Fitted lorentzian')

            the_figure(ax, key)
            if save_fig == 1:
                plt.savefig(os.path.join(os.path.dirname(datapath1), 'curve_fit', f'power_dependent_PL_curve_fit-{key}.png'))

"""fig1-intensity"""
fig1 = plt.figure(figsize=(8, 6))
ax1 = fig1.add_subplot(111)
x = [10, 20, 50, 100, 200, 500, 1000, 2000, 3000]
x = np.array(x)
y = np.array(ints)
ax1.plot(x, y, 'o-', markersize=10)

the_figure_1(ax1)
if save_fig == 1:
    plt.savefig(os.path.join(os.path.dirname(datapath1), 'curve_fit', f'power_dependent_intensity_of_peak-1.png'))

"""fig2-CW"""
fig2 = plt.figure(figsize=(8, 6))
ax2 = fig2.add_subplot(111)
x = [10, 20, 50, 100, 200, 500, 1000, 2000, 3000]
x = np.array(x)
y = np.array(cws)
ax2.plot(x, y, 'o-', markersize=10)

the_figure_2(ax2)
plt.tight_layout()
if save_fig == 1:
    plt.savefig(os.path.join(os.path.dirname(datapath1), 'curve_fit', f'power_dependent_center_wavelength_of_peak-1.png'))

"""fig3-FWHM"""
fig3 = plt.figure(figsize=(8, 6))
ax3 = fig3.add_subplot(111)
x = [10, 20, 50, 100, 200, 500, 1000, 2000, 3000]
x = np.array(x)
y = np.array(gammas)
ax3.plot(x, y, 'o-', markersize=10)

the_figure_3(ax3)
plt.tight_layout()
if save_fig == 1:
    plt.savefig(os.path.join(os.path.dirname(datapath1), 'curve_fit', f'power_dependent_FWHM_of_peak-1.png'))

plt.show()