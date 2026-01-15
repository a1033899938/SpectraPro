"""
Author: Junjie-Xie
Updated: 2025/7/16
Functions: 
"""
import h5py
import matplotlib.pyplot as plt
import numpy as np

from src.general.figure import set_figure
from src.general.load_data.load_data_from_h5 import *
from src.my_style.my_mapping_para import *
from src.my_style.my_figure import *
from src.my_style.my_color import *

# """路径"""
h5file = r"D:\ExpData\LabInstrumentTest\NewVsOld Ocean-20251127\NewVsOldSpectrometer.h5"
from figure_setting import *

with h5py.File(h5file, "r") as f:
    root = f["OceanOpticsSpectrometer"]

    Figures = []
    Axes = []
    for i in range(4):
        fig = plt.figure(i, figsize=(12, 8), dpi=200)
        ax = fig.add_subplot(111)
        Figures.append(fig)
        Axes.append(ax)

    old_background = f["OceanOpticsSpectrometer//old_bgd_1"]
    new_background = f["OceanOpticsSpectrometer//new_bgd_1"]

    backgrounds = [old_background, new_background]
    FWFM_old = []
    FWFM_new = []
    for iBackground, background in enumerate(backgrounds):
        wav = np.array(background.attrs['wavelengths'])

        sp_time = background.attrs['integration_time'] / 1000
        sps = np.array(background)

        for iWav, wav0 in enumerate(wav):
            col = sps[:, iWav]

            # ax.plot(col)
            # counts, bins, patches = ax.hist(x=col, color='blue', edgecolor='black', density=False)
            counts, bins = np.histogram(col)

            "由于边界数总比直方条数多1，所以要取边界中间作为统计位置"
            bin_centers = (bins[0:-1] + bins[1::])/2

            A = np.max(counts)
            x0 = bin_centers[np.argmax(counts)]
            sigma = 3
            p0 = [A, x0, sigma]

            try:
                popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)

                wav_hist = np.arange(bins[0], bins[-1], 0.1)
                fitted_curve = gaussian(wav_hist, *popt)

                theoretical_range = popt[2] * 6
            except Exception:
                theoretical_range = np.nan

            if iBackground == 0:
                FWFM_old.append(theoretical_range)
            else:
                FWFM_new.append(theoretical_range)

        if iBackground == 0:
            savepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_65nm_AuNConSi_circle_20251210\OceanOpticsSpectrometer_Noise.npz"
            np.savez(savepath, noise_FWFM=FWFM_old, wav=wav)

        sps = sps.ravel()
        sps_min = int(np.min(sps))
        sps_max = int(np.max(sps))
        sps_diff = sps_max - sps_min
        if iBackground == 0:
            ax = Axes[0]
            ax.plot(wav, FWFM_old, '-', color='blue')
            my_graph3(ax, "Old Ocean Noise(Single Wavelength)")

            ax = Axes[2]

            counts, bins, patches = ax.hist(x=sps, bins=sps_diff+1, color='blue', edgecolor='black', density=False)
        else:
            ax = Axes[1]
            ax.plot(wav, FWFM_new, '-', color='red')
            my_graph3(ax, "New Ocean Noise(Single Wavelength)")

            ax = Axes[3]
            counts, bins, patches = ax.hist(x=sps, bins=sps_diff+1, color='red', edgecolor='black', density=False)

        bin_centers = (bins[0:-1] + bins[1::]) / 2

        A = np.max(counts)
        x0 = bin_centers[np.argmax(counts)]
        sigma = 3
        p0 = [A, x0, sigma]

        popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)

        wav_hist = np.arange(bins[0], bins[-1], 0.1)
        fitted_curve = gaussian(wav_hist, *popt)

        ax.plot(wav_hist, fitted_curve, '-', color='gray')

        theoretical_range = popt[2] * 6


        if iBackground == 0:
            ax = Axes[2]
            ticks_xlabel = np.arange(sps_min, sps_max + 1, 5)
            my_graph4(ax, ticks_xlabel, "Old Ocean Noise(Global)")
        else:
            ax = Axes[3]
            ticks_xlabel = np.arange(sps_min, sps_max + 1, 2)
            my_graph4(ax, ticks_xlabel, "New Ocean Noise(Global)")

        print(theoretical_range)
plt.show()