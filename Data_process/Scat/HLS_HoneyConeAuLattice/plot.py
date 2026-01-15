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

# filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_AuNC_70nm_20251204.h5"

figures = [[],[]]
axes = [[],[]]
for i in range(12):
    fig = plt.figure(figsize=(12, 8), dpi=100)
    ax = fig.add_subplot(111)
    if i < 6:
        figures[0].append(fig)
        axes[0].append(ax)
    else:
        figures[1].append(fig)
        axes[1].append(ax)

figures2 = [[],[]]
axes2 = [[],[]]
for i in range(18):
    fig = plt.figure(figsize=(12, 8), dpi=100)
    ax = fig.add_subplot(111)
    if i < 9:
        figures2[0].append(fig)
        axes2[0].append(ax)
    else:
        figures2[1].append(fig)
        axes2[1].append(ax)
# print(np.shape(axes))

process_types = ["before_achro", "after_achro"]

p0_linear = [0.06, -20]
bounds_linear = [[0.03, -30],
            [0.09, 10]]

"""处理"""
with h5py.File(filepath, "r") as f:
    for iType, process_type in enumerate(process_types):
        root_folder = f["OceanOpticsSpectrometer/20251204"] # Tile_1/65nmAuNC_4/Image/
        root_folder = root_folder[process_type]

        # if iType != 1:
        #     continue

        tiled_image_keys = list(root_folder.keys())
        tiled_image_keys = sorted(tiled_image_keys, key=lambda x: int(x.split("_")[-1]))

        slope_stats = [[], []]
        minimum_time_stats = [[], []]
        dist_from_center = []
        reconstruct_error_stats = [None, None]
        for iTile, tiled_image_key in enumerate(tiled_image_keys):
            tiled_image = root_folder[tiled_image_key]

            # if iTile != 0:
            #     continue

            particle_keys = list(tiled_image.keys())
            particle_keys.remove("tiled_image")

            particle_keys = sorted(particle_keys, key=lambda x: int(x.split("_")[-1]))

            for iParticle, particle_key in enumerate(particle_keys):
                particle = tiled_image[particle_key]

                # if iParticle != 0:
                #     continue

                is_valid = particle.attrs["JunProc: is_valid"]

                if not is_valid:
                    continue

                """粒子居中的组，标记并处理"""
                # 标记
                spectra = particle["Spectra/scan_z"]

                steps = spectra.attrs["steps"]
                total_length = spectra.attrs["total length(um)"]

                zs = np.linspace(0, total_length, steps)

                # wav-maxz
                wav_maxz = particle.attrs["JunProc: wav-maxz"]

                wav, maxz = wav_maxz

                ax = axes[iType][0]

                ax.plot(wav, maxz)

                # wav-maxz-fit
                wav_maxz_fit_popts = particle.attrs["JunProc: wav-maxz fit-popts"]
                fitted_curve = linear(wav, *wav_maxz_fit_popts)
                ax.plot(wav, fitted_curve, "--")

                # maxz_range
                maxz_range_min = particle.attrs["JunProc: maxz-range_min"]
                maxz_range_max = particle.attrs["JunProc: maxz-range_max"]
                dist_from_center.append(np.abs(maxz_range_min - 50))
                dist_from_center.append(np.abs(maxz_range_max - 50))

                # reconstruct_error
                jump_steps, reconstruct_error =  particle.attrs["JunProc: jump_steps-reconstruct_error"]
                reconstruct_error_stats[iType] = reconstruct_error if reconstruct_error_stats[iType] is None else np.vstack([reconstruct_error_stats[iType], reconstruct_error])
                " 处理完所有粒子, 保存在tiled image中"

                # wav-max拟合信息
                for iSection in range(2):
                    wav_maxz_fit_popts_tiled_image = particle.attrs[f"JunProc: wav-maxz fit-popts {iSection}"]

                    slopes = wav_maxz_fit_popts_tiled_image[0]

                    # slope_stats[iSection] = slopes if slope_stats[iSection] is None else np.concatenate([slope_stats[iSection], slopes])
                    slope_stats[iSection].append(slopes)

                    # 复原粒子光谱至少所需的时间
                    minimum_time_tiled_image = particle.attrs[f"JunProc: minimum required time(s) {iSection}"]
                    # minimum_time_stats[iSection] = minimum_time_tiled_image if minimum_time_stats[iSection] is None else np.concatenate([minimum_time_stats[iSection], minimum_time_tiled_image])
                    minimum_time_stats[iSection].append(minimum_time_tiled_image)

        ax = axes[iType][1]
        counts, bins, patches = ax.hist(x=slope_stats[0], bins=30, color='blue', edgecolor='black', density=False)
        bin_centers = (bins[0:-1] + bins[1::]) / 2
        A = np.max(counts)
        x0 = bin_centers[np.argmax(counts)]
        sigma = 0.03
        p0 = [A, x0, sigma]
        popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)
        wav_hist = np.arange(bins[0], bins[-1], 0.001)
        fitted_curve = gaussian(wav_hist, *popt)
        ax.plot(wav_hist, fitted_curve, '-', color='gray')
        my_graph3(ax, title=f"{process_type} 400-700nm Slope")
        # ax.text(popt[1])
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

        ax = axes[iType][2]
        counts, bins, patches = ax.hist(x=slope_stats[1], bins=30, color='blue', edgecolor='black', density=False)
        bin_centers = (bins[0:-1] + bins[1::]) / 2
        A = np.max(counts)
        x0 = bin_centers[np.argmax(counts)]
        sigma = 0.03
        p0 = [A, x0, sigma]
        popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)
        wav_hist = np.arange(bins[0], bins[-1], 0.001)
        fitted_curve = gaussian(wav_hist, *popt)
        ax.plot(wav_hist, fitted_curve, '-', color='gray')
        my_graph3(ax, title=f"{process_type} 700-950nm Slope")
        # ax.text(popt[1])
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

        ax = axes[iType][3]
        counts, bins, patches = ax.hist(x=minimum_time_stats[0], bins=30, color='blue', edgecolor='black', density=False)
        bin_centers = (bins[0:-1] + bins[1::]) / 2
        A = np.max(counts)
        x0 = bin_centers[np.argmax(counts)]
        sigma = 3
        p0 = [A, x0, sigma]
        popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)
        wav_hist = np.arange(bins[0], bins[-1], 0.001)
        fitted_curve = gaussian(wav_hist, *popt)
        ax.plot(wav_hist, fitted_curve, '-', color='gray')
        my_graph4(ax, title=f"{process_type} 400-700nm require time(s)")
        # ax.text(popt[1])
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

        ax = axes[iType][4]
        counts, bins, patches = ax.hist(x=minimum_time_stats[1], bins=30, color='blue', edgecolor='black', density=False)
        bin_centers = (bins[0:-1] + bins[1::]) / 2
        A = np.max(counts)
        x0 = bin_centers[np.argmax(counts)]
        sigma = 3
        p0 = [A, x0, sigma]
        popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)
        wav_hist = np.arange(bins[0], bins[-1], 0.001)
        fitted_curve = gaussian(wav_hist, *popt)
        ax.plot(wav_hist, fitted_curve, '-', color='gray')
        my_graph4(ax, title=f"{process_type} 700-950nm require time(s)")
        # ax.text(popt[1])
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

        ax = axes[iType][5]
        counts, bins, patches = ax.hist(x=dist_from_center, bins=30, color='blue', edgecolor='black',
                                        density=False)
        bin_centers = (bins[0:-1] + bins[1::]) / 2
        A = np.max(counts)
        x0 = bin_centers[np.argmax(counts)]
        sigma = 3
        p0 = [A, x0, sigma]
        popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)
        wav_hist = np.arange(bins[0], bins[-1], 0.001)
        fitted_curve = gaussian(wav_hist, *popt)
        ax.plot(wav_hist, fitted_curve, '-', color='gray')
        my_graph4(ax, title=f"{process_type} dist_from_center")
        # ax.text(popt[1])
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

        for iJumpStep, jump_step in enumerate(jump_steps):
            ax = axes2[iType][iJumpStep]
            counts, bins, patches = ax.hist(x=reconstruct_error_stats[iType][:, iJumpStep], bins=30, color='blue', edgecolor='black',
                                            density=False)
            bin_centers = (bins[0:-1] + bins[1::]) / 2
            A = np.max(counts)
            x0 = bin_centers[np.argmax(counts)]
            sigma = 0.001
            p0 = [A, x0, sigma]
            popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)
            wav_hist = np.arange(bins[0], bins[-1], 0.001)
            fitted_curve = gaussian(wav_hist, *popt)
            ax.plot(wav_hist, fitted_curve, '-', color='gray')
            my_graph4(ax, title=f"{process_type} reconstruct_error: jump_step={jump_step}")
            # ax.text(popt[1])
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
plt.show()
