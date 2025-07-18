import numpy as np
from scipy.optimize import curve_fit
import os
import h5py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from src.general.figure import set_figure
from src.general import *
from src.general import *
from src.general import *

def wavlength_to_energy(wavelength):
    return 1240 / wavelength

def the_figure(ax, fig):
    set_figure.set_label_and_title(ax, title=f'Quantum dot\n{key}', xlabel='Process time(min)', ylabel='Intensity(counts)', mode='3d')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticklabel_pad=10, ticks_xlabel=np.arange(0, Z.shape[0] + 1, 5), ticks_ylabel=np.arange(500, 801, 100), mode='3d')
    ax.set_xlabel(xlabel='Measurement  sequence', labelpad=20)
    ax.set_ylabel(ylabel='Wavelength(nm)', labelpad=20)
    ax.zaxis.set_rotate_label(False)
    ax.set_zlabel(zlabel='Intensity(counts)', rotation=90, labelpad=25)

    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=20, azim=45)  # elev 是仰角，azim 是方位角
    ax.grid(True)
    fig.tight_layout()

def the_figure1(ax1, ax2):
    set_figure.set_label_and_title(ax1, title=f'Quantum dot\n{key}')
    set_figure.set_spines(ax1)
    set_figure.set_tick(ax1, ticks_xlabel=np.arange(1, 3.6, 0.5))
    ax1.grid(True)
    ax2.set_xlim(ax1.get_xlim()[0], ax1.get_xlim()[1])
    set_figure.set_tick(ax2, ticks_xlabel=wavlength_to_energy(np.arange(450, 1151, 150)), change_ticks_xlabel=np.arange(450, 1151, 150))
    plt.tight_layout()


datapath1 = r"D:\ExpData\Fellows\HWL\20250321\2025-03-21.h5"
save_fig = 1

"""fig0"""
with h5py.File(datapath1, "r") as f:
    data = f['OceanOpticsSpectrometer']
    bgd = np.array(data['QDs_sample2_0'].attrs['background'])
    bgd_time = data['QDs_sample2_0'].attrs['background_int'] / 1000
    wav = np.array(data['QDs_sample2_0'].attrs['wavelengths'])
    bgd = bgd / bgd_time

    bgd, _ = np.meshgrid(bgd, np.arange(0, data['QDs_sample2_0'].shape[0])) # 创建一个与sp相同大小的bgd阵列
    legend_labels = []
    for key in data.keys():
        if 'QDs_sample2' in key:
            sp = data[key]
            sp_time = sp.attrs['integration_time'] / 1000
            sp = np.array(sp)
            sp = sp / sp_time
            sp = sp - bgd


            fig = plt.figure(figsize=(12, 9))
            ax = fig.add_subplot(111, projection='3d')
            x, Z = choose_range(wav, sp, min_val=500, max_val=800, axis=1)
            draw_cascade(ax, x, Z)
            the_figure(ax, fig)
            if save_fig == 1:
                fig.savefig(os.path.join(os.path.dirname(datapath1), 'cascade', f'{key}.png'))
            # plt.close(fig0)

            erg = 1240 / wav
            erg = erg[::-1]
            fig1 = plt.figure(figsize=(8, 6))
            for sp_now in sp:
                sp = sp[:, ::-1]
                ax1 = fig1.add_subplot(111)
                sp_now = sp[0]
                ax1.plot(erg, sp_now, 'black', linewidth=3)

                p0 = [100, 1.9, 0.1, 0.1]

                x_for_fit, y_for_fit = choose_range(erg, sp_now, min_val=1.2, max_val=3)
                popt, pcov = curve_fit(voigt, x_for_fit, y_for_fit, p0=p0)
                amplitude, center, sigma, gamma = popt

                print(f"amplitude = {amplitude}, center = {center}, sigma = {sigma}, gamma = {gamma}")
                y_fit = voigt(x_for_fit, *popt)
                ax1.plot(x_for_fit, y_fit, 'r-', label='Fitted voigt')

                ax2 = ax1.twiny()
                the_figure1(ax1, ax2)
plt.show()