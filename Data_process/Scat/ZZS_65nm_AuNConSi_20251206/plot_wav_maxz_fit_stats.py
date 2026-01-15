import cv2
import h5py
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sympy.codegen.ast import continue_

from src.general.numerical.curve_functions import *
from src.general.numerical.edit_data import *
from figure_setting import *
from scipy.signal import find_peaks
from PIL import Image
from datetime import datetime

def sigma_moment(y, x):
    y = np.nan_to_num(y, nan=0.0, posinf=0.0, neginf=0.0)
    x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)

    total = np.sum(y)
    if total == 0:
        return 0
    mu  = np.sum(x * y) / total
    sigma = np.sqrt(np.sum((x - mu ) ** 2 * y) / total)

    # width_997 = 6*sigma
    width_1e2 = 4*sigma
    return mu, width_1e2

filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_AuNC_65nm_20251206\ZZS_AuNC_65nm_20251206.h5"

p0_linear = [0.06, -20]
bounds_linear = [[0, -30],
            [0.1, 10]]

"""处理"""
with h5py.File(filepath, "r") as f:
    process_type = "after_achro"
    iType = 1
    root_folder = f["OceanOpticsSpectrometer/20251207/sample2"] # Tile_1/65nmAuNC_4/Image/
    # root_folder = root_folder[process_type]

    # if iType != 1:
    #     continue

    tiled_image_keys = list(root_folder.keys())
    tiled_image_keys = sorted(tiled_image_keys, key=lambda x: int(x.split("_")[-1]))

    slope_stats = [[], []]
    minimum_time_stats = [[], []]
    total_valid_particle = 0
    for iTile, tiled_image_key in enumerate(tiled_image_keys):
        tiled_image = root_folder[tiled_image_key]

        # if iTile != 0:
        #     continue

        particle_keys = list(tiled_image.keys())
        particle_keys.remove("tiled_image")

        particle_keys = sorted(particle_keys, key=lambda x: int(x.split("_")[-1]))

        fit_range_0 = None
        fit_range_1 = None
        for iParticle, particle_key in enumerate(particle_keys):
            particle = tiled_image[particle_key]

            # if iParticle != 0:
            #     continue

            is_valid = particle.attrs["JunProc: is_valid"]

            if not is_valid:
                continue

            total_valid_particle += 1

            """粒子居中的组，标记并处理"""
            # 标记
            spectra = particle["Spectra/scan_z"]

            # wav-max拟合信息

            fit_range = [None, None]
            for iSection in range(2):
                if any([key not in particle.attrs.keys() for key in
                        [f"JunProc: wav-maxz fit-popts {iSection}", f"JunProc: minimum required time(s) {iSection}"]]):
                    continue

                fit_range[iSection] = particle.attrs[f"JunProc: wav-maxz fit-range {iSection}"]

                wav_maxz_fit_popts_tiled_image = particle.attrs[f"JunProc: wav-maxz fit-popts {iSection}"]

                slopes = wav_maxz_fit_popts_tiled_image[0]

                slope_stats[iSection].append(slopes)

                # 复原粒子光谱至少所需的时间
                minimum_time_tiled_image = particle.attrs[f"JunProc: minimum required time(s) {iSection}"]
                minimum_time_stats[iSection].append(minimum_time_tiled_image)

    fig = plt.figure(figsize=(12*2, 8*2), dpi=100)
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)
    axes = [ax1, ax2, ax3, ax4]

    for iSection in range(2):
        ax = axes[iSection]
        counts, bins, patches = ax.hist(x=slope_stats[iSection], bins=30, color='blue', edgecolor='black', density=False)
        bin_centers = (bins[0:-1] + bins[1::]) / 2
        A = np.max(counts)
        x0 = bin_centers[np.argmax(counts)]
        sigma = 0.03
        p0 = [A, x0, sigma]
        popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)
        wav_hist = np.arange(bins[0], bins[-1], 0.001)
        fitted_curve = gaussian(wav_hist, *popt)
        ax.plot(wav_hist, fitted_curve, '-', color='gray')
        text_x = 0.95 * wav_hist.max()  # 水平位置：右偏95%
        text_y = 0.9 * fitted_curve.max()  # 垂直位置：上偏90%
        text_content = f"{popt[1]:.2f}"
        ax.text(
            x=text_x,
            y=text_y,
            s=text_content,
            fontsize=20,  # 字体大小（关键）
            ha='right',  # 水平右对齐（避免文本超出图像）
            va='top',  # 垂直上对齐
            color='red',  # 文本颜色
            weight='bold'  # 加粗（可选）
        )
        my_wav_maxz_fit_slope_stats(ax, title=f"Fitted slope: {fit_range[iSection][0]:.1f} - {fit_range[iSection][1]:.1f} nm")

        ax = axes[iSection+2]
        counts, bins, patches = ax.hist(x=minimum_time_stats[iSection], bins=30, color='blue', edgecolor='black', density=False)
        bin_centers = (bins[0:-1] + bins[1::]) / 2
        A = np.max(counts)
        x0 = bin_centers[np.argmax(counts)]
        sigma = 20
        p0 = [A, x0, sigma]
        popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)
        wav_hist = np.arange(bins[0], bins[-1], 0.001)
        fitted_curve = gaussian(wav_hist, *popt)
        ax.plot(wav_hist, fitted_curve, '-', color='gray')
        # my_graph3(ax, title=f"{process_type} 400-700nm Slope")
        text_x = 0.95 * wav_hist.max()  # 水平位置：右偏95%
        text_y = 0.9 * fitted_curve.max()  # 垂直位置：上偏90%
        text_content = f"{popt[1]:.2f}"
        ax.text(
            x=text_x,
            y=text_y,
            s=text_content,
            fontsize=20,  # 字体大小（关键）
            ha='right',  # 水平右对齐（避免文本超出图像）
            va='top',  # 垂直上对齐
            color='red',  # 文本颜色
            weight='bold'  # 加粗（可选）
        )
        my_wav_maxz_minimum_required_time_stats(ax, title=f"Minimum Required Time: {fit_range[iSection][0]:.1f} - {fit_range[iSection][1]:.1f} nm")

    save_path = os.path.join(os.path.dirname(filepath),
                             fr"Image/Reconstuct_scat & stacked_scats/{process_type}_Minimun_Required_time.png")
    fig.savefig(save_path)
print(f"total_valid_particle: {total_valid_particle}")
plt.show()
