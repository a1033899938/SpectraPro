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

filepath = r"D:\ExpData\NP_scattering_Dispersion\ZY\2025-11-29.h5"

fig = plt.figure(figsize=(12*2, 8*2))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
ax4_inset = ax4.inset_axes([0.7, 0.7, 0.25, 0.25])

p0_linear = [0.06, -20]
bounds_linear = [[0, -50],
            [0.15, 75]]

"""处理"""
with h5py.File(filepath, "a") as f:
    process_type = "before_achro"

    root_folder = f # Tile_1/65nmAuNC_4/Image/
    scanner_keys = list(root_folder.keys())

    temp_keys = []
    for key in scanner_keys:
        if "Scanner" in key:
            temp_keys.append(key)
    scanner_keys = temp_keys

    total_particle_now = 0
    wav_maxz_fit_popts_stats = []
    for iScanner, scanner_key in enumerate(scanner_keys):
        scanner = root_folder[scanner_key]
        particle_keys = list(scanner.keys())
        particle_keys.remove("Tiles")
        particle_keys = sorted(particle_keys, key=lambda x: int(x.split("_")[-1]))
        bgd = None
        ref = None

        for iParticle, particle_key in enumerate(particle_keys):
            particle = scanner[particle_key]

            """处理图像-判断光谱组是否有效"""
            img = particle["CWL.thumb_image_0"]

            img = np.asarray(img)
            ax4.imshow(img)
            my_thumb_image(ax4, title="Thumb Image")
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

            ax4_inset.imshow(img)

            proj_h = np.sum(img, axis=0)
            proj_v = np.sum(img, axis=0)

            peaks_h, _ = find_peaks(
                proj_h,
                height=0.1 * np.max(proj_h),  # 仅检测高于最大幅值10%的峰值（过滤小噪声）
                distance=5,  # 峰值之间最小距离（避免相邻假峰）
                prominence=20  # 峰值突出度（越大，仅检测越“尖”的峰）
            )

            peaks_v, _ = find_peaks(
                proj_v,
                height=0.1 * np.max(proj_h),  # 仅检测高于最大幅值10%的峰值（过滤小噪声）
                distance=5,  # 峰值之间最小距离（避免相邻假峰）
                prominence=20  # 峰值突出度（越大，仅检测越“尖”的峰）
            )

            "粒子未居中的组，仅标记，然后直接跳过"
            flag1 = False
            flag2 = False

            max_h_idx = np.argmax(proj_h)
            max_v_idx = np.argmax(proj_h)

            if np.abs(max_h_idx - len(proj_h)/2) > 30:
                flag1 = True
            if np.abs(max_v_idx - len(proj_v)/2) > 30:
                flag2 = True

            if flag1 or flag2:
                particle.attrs.update({"JunProc: is_valid": False})
                continue

            """粒子居中的组，标记并处理"""
            # 标记
            particle.attrs.update({"JunProc: is_valid": True})
            total_particle_now += 1

            steps = 18
            total_length = 19

            scan = particle["z_scan_0"]
            scats = None

            wav = np.array(scan.attrs['wavelengths'])
            indices = np.array(range(len(wav)))
            wav, indices = choose_range(wav, indices, x1=450, x2=900)

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
            zs = np.arange(0, total_length, steps)

            for iZ, z in enumerate(zs):
                sg = sgs[iZ, :]
                sg = sg / sg_time
                sg = sg[indices]

                numerator = sg - bgd  # 分子

                denominator = ref - bgd  # 分母

                denominator[denominator == 0] = 1  # 如果分母为0，设为1
                numerator[denominator == 0] = 0  # 对应的分子，设 = numerator / denominator

                scats = scat if scats is None else np.vstack([scats, scat])

            scats_max = np.max(scats, axis=0)
            print(np.shape(scats))
            input()
            ax2.pcolor(wav, zs, scats, cmap="coolwarm")
            ax1.plot(wav, scats_max)

            # 计算未重构谱的误差
            x1 = 500
            x2 = 700
            x1_idx = find_val_idx(wav, x1)
            x2_idx = find_val_idx(wav, x2)

            scats_roi = scats[:, x1_idx:x2_idx]

            max_int_idx = np.argmax(scats_roi)  # 扁平索引
            max_int_idx = np.unravel_index(max_int_idx, scats_roi.shape)  # 二维索引
            z0_idx = max_int_idx[0]
            wav0_idx = max_int_idx[1]
            wav0_idx = wav0_idx + x1_idx
            scat_at_max_int = scats[z0_idx, :]

            scat_at_max_int = scat_at_max_int[scats_max != 0]

            wav_max = wav[wav0_idx]

            "wav-maxz曲线"
            maxz_indice = []
            for iWav, wav0 in enumerate(wav):
                ints = scats[:, iWav]
                maxz_idx = np.argmax(ints)
                maxz_indice.append(maxz_idx)

            maxz = zs[maxz_indice]

            wav_maxz_attrs = {"JunProc: wav-maxz": [wav, maxz]}
            particle.attrs.update(wav_maxz_attrs)

            # 拟合所有分段wav-maxz
            maxz = np.array(maxz)
            # 分段1：480-70
            fit_section = [[486.1, 656.3], [656.3, 800]]
            show_section = [[450, 656.3], [656.3, 900]]

            for iSection, section in enumerate(fit_section):
                x1 = fit_section[iSection][0]
                x2 = fit_section[iSection][1]
                x3 = show_section[iSection][0]
                x4 = show_section[iSection][1]
                x_for_fit, y_for_fit = choose_range(wav, maxz, x1=x1, x2=x2)
                x_for_show, y_for_show = choose_range(wav, maxz, x1=x3, x2=x4)
                ax2.plot(x_for_show, y_for_show, color="blue" if iSection == 0 else "red")

                popt, pcov = curve_fit(linear, x_for_fit, y_for_fit, p0=p0_linear, bounds=bounds_linear)

                fitted_curve = linear(x_for_fit, *popt)

                wav_maxz_fit_popts_attrs = {
                    f"JunProc: wav-maxz fit-range {iSection}": [x1, x2],
                    f"JunProc: wav-maxz fit-func {iSection}": "linear",
                    f"JunProc: wav-maxz fit-popts {iSection}": popt,
                    }
                wav_maxz_fit_popts_stats.append(popt)
                particle.attrs.update(wav_maxz_fit_popts_attrs)

                # 根据所有分段wav-maxz，计算首末maxz位置
                z1_idx = find_val_idx(zs, fitted_curve[0])
                z2_idx = find_val_idx(zs, fitted_curve[-1])

                maxz_min = zs[z1_idx]
                maxz_max = zs[z2_idx]
                maxz_range = maxz_max - maxz_min
                maxz_range_attrs = {
                    f"JunProc: maxz-range {iSection}": maxz_range,
                    f"JunProc: maxz-range_min {iSection}": maxz_min,
                    f"JunProc: maxz-range_max {iSection}": maxz_max}
                particle.attrs.update(maxz_range_attrs)

                if z2_idx == z1_idx:
                    continue

                "最大强度处的z-int曲线"
                wavs_target = [486.1, 587.6, 656.3] + [wav_max]
                wavs_indice_target = [find_val_idx(wav, wav_target) for wav_target in wavs_target] + [wav0_idx]
                colors = ["blue", "green", "red", "orange"]

                sorted_tuples  = sorted(zip(wavs_target, wavs_indice_target, colors), key=lambda x: x[0])
                wavs_target, wavs_indice_target, colors = zip(*sorted_tuples)

                for iWavTarget, (color, wav_target, wav_index_target) in enumerate(zip(colors, wavs_target, wavs_indice_target)):
                    ax2.axvline(x=wav_target, color=color, linestyle="--", linewidth=2)
                    # 对应波长位置的ints
                    ints_target = scats[:, wav_index_target]
                    ax3.plot(zs, ints_target, "-", color=color, label=f"data - {wav_target:.1f} nm")
                    title = "z-int at Target Wavelength"
                    my_maxint_ints(ax3, title=title)

                    mag = None
                    z0 = None
                    sigma = None
                    try:
                        A0 = np.max(ints_target)
                        x0 = zs[np.argmax(ints_target)]
                        sigma0 = 20
                        p0 = [A0, x0, sigma0]
                        popt, pcov = curve_fit(gaussian, zs, ints_target, p0=p0)

                        fitted_curve = gaussian(zs, *popt)

                        z_ins_at_max_int_fit_popts_attrs = {"JunProc: z_ins_at_max_int_fit_popts_attrs": popt}
                        particle.attrs.update(z_ins_at_max_int_fit_popts_attrs)

                        ax3.plot(zs, fitted_curve, '--', color=color, label=f"gaussian fit - {wav_target:.1f} nm")
                        my_maxint_ints(ax3, title=title)

                        mag, z0, sigma = popt
                    except:
                        pass

                    text_x = 0.05
                    text_y = 0.95 - 0.05 * iWavTarget
                    text_content1 = f"A: {mag:.2e}" if mag is not None else "A: --"
                    text_content2 = f"z0: {z0:.1f}" if z0 is not None else "z0: --"
                    text_content3 = f"sigma: {sigma:.1f}" if sigma is not None else "sigma: --"
                    text_content = text_content1 + " " +  text_content2 + " " +  text_content3
                    ax3.text(
                        x=text_x,
                        y=text_y,
                        s=text_content,
                        fontsize=15,  # 字体大小（关键）
                        ha='left',  # 水平右对齐（避免文本超出图像）
                        va='top',  # 垂直上对齐
                        color=color,  # 文本颜色
                        weight='bold',  # 加粗（可选）
                        transform=ax3.transAxes
                    )

            save_path = os.path.join(os.path.dirname(filepath), fr"Image/Reconstuct_scat & stacked_scats/{process_type}_p{total_particle_now}.png")
            my_reconstruct_scat(ax1, title="Reconstructed Spectrum")
            my_zstack_scats(ax2, title="Z-Axis Stacked Spectra")
            fig.savefig(save_path)
            ax1.clear()
            ax2.clear()
            ax3.clear()
# plt.show()