import cv2
import h5py
import os
import matplotlib.pyplot as plt
import numpy as np
from IPython.core.pylabtools import figsize
from scipy.optimize import curve_fit
from sympy.codegen.ast import continue_

from src.general.numerical.curve_functions import *
from src.general.numerical.edit_data import *
from figure_setting import *
from brokenaxes import brokenaxes
from scipy.signal import find_peaks
from PIL import Image
from datetime import datetime

# filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_AuNC_70nm_20251204.h5"

# 误差统计
plt.close('all')

figures = []
axes = []
for i in range(2):
    fig = plt.figure(figsize=(12*2, 8), dpi=100)
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    figures.append(fig)
    axes.append([ax1, ax2])

process_types = ["before_achro", "after_achro"]

"""处理"""
with h5py.File(filepath, "r") as f:
    mins = []
    maxs = []
    for iType, process_type in enumerate(process_types):
        root_folder = f["OceanOpticsSpectrometer/20251204"] # Tile_1/65nmAuNC_4/Image/
        root_folder = root_folder[process_type]

        tiled_image_keys = list(root_folder.keys())
        tiled_image_keys = sorted(tiled_image_keys, key=lambda x: int(x.split("_")[-1]))

        # 找到粒子总数
        last_tiled_image = root_folder[tiled_image_keys[-1]]
        particle_in_last_tiled_image_keys = list(last_tiled_image.keys())
        particle_in_last_tiled_image_keys.remove("tiled_image")
        particle_in_last_tiled_image_keys = sorted(particle_in_last_tiled_image_keys,
                                                   key=lambda x: int(x.split("_")[-1]))
        last_particle = last_tiled_image[particle_in_last_tiled_image_keys[-1]]
        total_particle = int(last_particle.attrs["total_particle_now"])

        maxz_range_stats = [None, None]
        for iTile, tiled_image_key in enumerate(tiled_image_keys):
            tiled_image = root_folder[tiled_image_key]

            particle_keys = list(tiled_image.keys())
            particle_keys.remove("tiled_image")

            particle_keys = sorted(particle_keys, key=lambda x: int(x.split("_")[-1]))

            for iParticle, particle_key in enumerate(particle_keys):
                particle = tiled_image[particle_key]
                total_particle_now = int(particle.attrs["total_particle_now"])

                is_valid = particle.attrs["JunProc: is_valid"]

                if not is_valid:
                    continue

                print(f"=====当前处理: {process_type}:{total_particle_now}/{total_particle}=====")

                maxz_range_min = particle.attrs["JunProc: maxz-range_min"]
                maxz_range_max = particle.attrs["JunProc: maxz-range_max"]
                maxz_range = [maxz_range_min, maxz_range_max]

                maxz_range_stats[iType] = maxz_range if maxz_range_stats[iType] is None else np.vstack([maxz_range_stats[iType], maxz_range])

        fig = figures[iType]
        for idx in range(2):
            ax = axes[iType][idx]
            counts, bins, patches = ax.hist(x=maxz_range_stats[iType][:, idx], bins=30, color='blue', edgecolor='black',
                                            density=False)
            bin_centers = (bins[0:-1] + bins[1::]) / 2

            A = np.max(counts)
            x0 = bin_centers[np.argmax(counts)]
            if idx == 0:
                sigma = 30
            else:
                sigma = 60

            p0 = [A, x0, sigma]
            popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)
            wav_hist = np.arange(bins[0], bins[-1], 0.001)
            fitted_curve = gaussian(wav_hist, *popt)
            ax.plot(wav_hist, fitted_curve, '-', color='gray')

            if idx == 0:
                min_now = popt[1] - 2*popt[2]  # x0 - FWFM/2
                mins.append(min_now)
            else:
                max_now = popt[1] + 2*popt[2]  # x0 + FWFM/2
                maxs.append(max_now)

            text_x = 0.95 * wav_hist.max()  # 水平位置：右偏95%
            text_y = 0.9 * A  # 垂直位置：上偏90%
            text_content = f"center: {popt[1]:.4f}"
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
            title = f"{process_type}_maxz_range_stats.png"

            my_maxz_range_stats(ax, title=f"{process_type}_range_min_stats" if idx == 0 else f"{process_type}_range_max_stats")

        save_path = os.path.join(os.path.dirname(filepath),
                                 fr"Image/Maxz_range/{title}.png")
        fig.savefig(save_path)

    print(f"最佳扫描范围(99.99367 % 几率扫描完整的光谱): {np.min(mins)}, {np.max(maxs)}")
    print(f"偏离中心位置距离: {50 - np.min(mins):.2f}, {np.max(maxs) - 50:.2f}")
# plt.show()
