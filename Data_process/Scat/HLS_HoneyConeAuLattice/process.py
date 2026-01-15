import cv2
import h5py
import os
import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms.shortest_paths.dense import reconstruct_path
from scipy.optimize import curve_fit
from sympy.codegen.ast import continue_

from src.general.numerical.curve_functions import *
from src.general.numerical.edit_data import *
from figure_setting import *
from scipy.signal import find_peaks
from PIL import Image
import matplotlib.colors as colors
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

filepath = r"D:\ExpData\NP_scattering_Dispersion\HLS_HoneyConeAuLattice\HLS_HoneyConeAuLattice.h5"

p0_linear = [0.06, -20]
bounds_linear = [[0, -50],
            [0.15, 75]]

"""处理"""
with h5py.File(filepath, "a") as f:
    root_folder_keys = list(f.keys())
    root_folder_scanner_keys = []
    root_folder_particles_keys = []

    total_particle_now = -1
    for root_folder_key in root_folder_keys:
        if "Particle" in root_folder_key:
            if "Scanner" in root_folder_key:
                root_folder_scanner_keys.append(root_folder_key)
            else:
                if "bgd" not in root_folder_key:
                    root_folder_particles_keys.append(root_folder_key)

    root_folder_scanner_keys = sorted(root_folder_scanner_keys, key=lambda x: int(x.split("_")[-1]))
    root_folder_scanner_keys.append(000)

    for iScanner, root_folder_scanner_key in enumerate(root_folder_scanner_keys):
        if iScanner != len(root_folder_scanner_keys) - 1:
            root_folder_scanner = f[root_folder_scanner_key]
            particle_keys = list(root_folder_scanner.keys())
        else:
            root_folder_scanner = f[root_folder_scanner_key]
            particle_keys = root_folder_particles_keys

        # if iScanner != 5:
        #     continue

        temp_keys = []
        for particle_key in particle_keys:
            if "Particle" in particle_key:
                temp_keys.append(particle_key)
        particle_keys = temp_keys
        particle_keys = sorted(particle_keys, key=lambda x: int(x.split("_")[-1]))

        for iParticle, particle_key in enumerate(particle_keys):
            particle = root_folder_scanner[particle_key]

            print(root_folder_scanner_key, particle_key)
            # if iParticle != 3:
            #     continue

            data_keys = list(particle.keys())
            temp_keys = []
            image_key = None
            scan_key = None
            for data_key in data_keys:
                if "image" in data_key:
                    image_key = data_key
                elif "scan" in data_key:
                    scan_key = data_key

            try:
                scats = None
                if scan_key is not None:
                    fig = plt.figure(figsize=(12 * 2, 8 * 2))
                    ax1 = fig.add_subplot(221)
                    ax2 = fig.add_subplot(222)
                    ax3 = fig.add_subplot(223)
                    ax4 = fig.add_subplot(224)

                    scan  = particle[scan_key]

                    wav = np.array(scan.attrs['wavelengths'])
                    indices = np.array(range(len(wav)))
                    wav, indices = choose_range(wav, indices, x1=400, x2=900)

                    # 仅获取第一条光谱的bgd, ref, 节省时间
                    bgd = np.array(scan.attrs['background'])
                    bgd_time = scan.attrs['background_int'] / 1000
                    bgd = bgd / bgd_time
                    bgd = bgd[indices]

                    ref = np.array(scan.attrs['reference'])
                    ref_time = scan.attrs['reference_int'] / 1000
                    ref = ref / ref_time
                    ref = ref[indices]

                    sgs = np.array(scan)
                    sg_time = scan.attrs['integration_time'] / 1000
                    h, w = np.shape(sgs)
                    zs = np.array(range(h))

                    for iZ, z in enumerate(zs):
                        sg = sgs[iZ, :]
                        sg = sg / sg_time
                        sg = sg[indices]

                        numerator = sg - bgd  # 分子

                        denominator = ref - bgd  # 分母

                        denominator[denominator == 0] = 1  # 如果分母为0，设为1
                        numerator[denominator == 0] = 0  # 对应的分子，设为0

                        scat = numerator / denominator

                        scats = scat if scats is None else np.vstack([scats, scat])
            except Exception as e:
                print(str(e))

            # 重建scat
            scats_max = np.max(scats, axis=0)
            ax1.plot(wav, scats_max)
            my_reconstruct_scat(ax1, title="Reconstructed Spectrum")

            ax2.pcolor(wav, zs, scats, cmap="coolwarm")

            "wav-maxz曲线"
            try:
                maxz_indice = []
                for iWav, wav0 in enumerate(wav):
                    ints = scats[:, iWav]
                    maxz_idx = np.argmax(ints)
                    maxz_indice.append(maxz_idx)

                maxz = zs[maxz_indice]

                ax2.plot(wav, maxz)
                my_zstack_scats(ax2, title="Z-Axis Stacked Spectra")

            except Exception as e:
                print(str(e))

            "最大强度处的z-int曲线"
            try:
                max_int_idx = np.argmax(scats)  # 扁平索引
                max_int_idx = np.unravel_index(max_int_idx, scats.shape)  # 二维索引
                z0_idx = max_int_idx[0]
                wav0_idx = max_int_idx[1]
                scat_at_max_int = scats[z0_idx, :]

                z0 = zs[z0_idx]
                wav0 = wav[wav0_idx]

                ax2.axvline(x=wav0, color="green", linestyle="--", linewidth=2)

                # 取出最大值所在波长位置的ints
                maxint_ints = scats[:, wav0_idx]
                ax3.plot(zs, maxint_ints, "-", label="data")
                title = "z_ints-at-max_int"

                A = np.max(maxint_ints)
                x0 = zs[np.argmax(maxint_ints)]
                sigma = 5
                p0 = [A, x0, sigma]
                popt, pcov = curve_fit(gaussian, zs, maxint_ints, p0=p0)
                fitted_curve = gaussian(zs, *popt)

                z_ins_at_max_int_fit_popts_attrs = {"JunProc: z_ins_at_max_int_fit_popts_attrs": popt}
                particle.attrs.update(z_ins_at_max_int_fit_popts_attrs)

                ax3.plot(zs, fitted_curve, '--', color='gray', label="gaussian fit")
                my_maxint_ints(ax3, title=title)

                text_x = 0.05 * zs.max()  # 水平位置：右偏95%
                text_y = 0.95 * maxint_ints.max()  # 垂直位置：上偏90%
                text_content = (f"A: {popt[0]:.3f}\n"
                                f"z0: {popt[1]:.1f}\n"
                                f"sigma: {popt[2]:.1f}\n")
                ax3.text(
                    x=text_x,
                    y=text_y,
                    s=text_content,
                    fontsize=20,  # 字体大小（关键）
                    ha='left',  # 水平右对齐（避免文本超出图像）
                    va='top',  # 垂直上对齐
                    color='red',  # 文本颜色
                    weight='bold'  # 加粗（可选）
                )
            except Exception as e:
                print(str(e))

            if image_key is not None:
                image = particle[image_key]
                image = np.asarray(image)
                ax4.imshow(image)

            if scan_key is not None:
                total_particle_now += 1
                total_particle_now_attrs = {"JunProc: total_particle_now": total_particle_now}
                particle.attrs.update(total_particle_now_attrs)

                save_path = os.path.join(os.path.dirname(filepath), fr"Image/Reconstuct_scat & stacked_scats/p{total_particle_now}.png")
                my_reconstruct_scat(ax1, title="Reconstructed Spectrum")
                my_zstack_scats(ax2, title="Z-Axis Stacked Spectra")
                fig.savefig(save_path)
                plt.close(fig)

        # # " 处理完所有粒子, 保存在tiled image中"
        # # # 以tiled image为单位统计以上部分信息
        # #
        # # # wav-max拟合信息
        # # wav_maxz_fit_popts_stats_attrs = {"JunProc: wav-maxz fit-popts_stats": wav_maxz_fit_popts_stats}
        # # tiled_image.attrs.update(wav_maxz_fit_popts_stats_attrs)
        # #
        # # # 总耗时
        # # total_time_stats_attrs = {"JunProc: total time(s)_stats": total_second_stats}
        # # tiled_image.attrs.update(total_time_stats_attrs)
        # #
        # # # 复原粒子光谱至少所需的时间
        # # minimum_second_stats_attrs = {"JunProc: minimum required time(s)_stats": minimum_second_stats}
        # # tiled_image.attrs.update(minimum_second_stats_attrs)
# plt.show()