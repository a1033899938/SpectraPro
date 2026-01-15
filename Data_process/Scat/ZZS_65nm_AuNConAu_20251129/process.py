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

filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_AuNC_70nm_20251117\ZZS_AuNC_70nm_20251117.h5"

fig = plt.figure(figsize=(12*2, 8*2))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

p0_linear = [0.06, -20]
bounds_linear = [[0, -50],
            [0.15, 75]]

process_types = ["before_achro", "after_achro"]
"""处理"""
with h5py.File(filepath, "a") as f:
    for iType, process_type in enumerate(process_types):
        root_folder = f[f"OceanOpticsSpectrometer/20251129/{process_type}"] # Tile_1/65nmAuNC_4/Image/

        particle_keys = list(root_folder.keys())
        particle_keys = sorted(particle_keys, key=lambda x: int(x.split("-")[-1]))

        wav_maxz_fit_popts_stats = []
        total_second_stats = []
        minimum_second_stats = []
        for iParticle, particle_key in enumerate(particle_keys):
            particle = root_folder[particle_key]

            """处理图像-判断光谱组是否有效"""
            img = particle["Image//OM image"]

            img = np.asarray(img)
            size = 100
            h, w, _ = img.shape
            start_x, end_x = (w - size)//2, (w + size)//2
            start_y, end_y = (h - size)//2, (h + size)//2

            img = img[start_y:end_y, start_x :end_x, :]
            ax4.imshow(img)
            my_thumb_image(ax4, title="image")

            spectra = particle["Spectra"]

            steps = int(spectra.attrs["steps"])
            total_length = float(spectra.attrs["total length(um)"])

            spectra_keys = spectra.keys()

            spectra_keys = sorted(spectra_keys, key=lambda x: int(x.split("_")[-1][1::]))

            scats = None
            times = []
            "历遍该粒子所有光谱"
            for iSpectra, sp_key in enumerate(spectra_keys):
                sp = spectra[sp_key]

                time_now = sp.attrs['creation_timestamp']
                time_now = datetime.fromisoformat(time_now)
                times.append(time_now)

                wav = np.array(sp.attrs['wavelengths'])

                bgd = np.array(sp.attrs['background'])
                bgd_time = sp.attrs['background_int'] / 1000
                bgd = bgd / bgd_time

                ref = np.array(sp.attrs['reference'])
                ref_time = sp.attrs['reference_int'] / 1000
                ref = ref / ref_time

                sg_time = sp.attrs['integration_time'] / 1000
                sg = np.array(sp)
                sg = sg / sg_time

                numerator = sg - bgd  # 分子

                denominator = ref - bgd  # 分母

                denominator[denominator == 0] = 1  # 如果分母为0，设为1
                numerator[denominator == 0] = 0  # 对应的分子，设为0

                scat = numerator / denominator

                wav, scat = choose_range(wav, scat, x1=450, x2=1000)

                scats = scat if scats is None else np.vstack([scats, scat])

            """处理完组内所有光谱, 保存在particle中"""
            zs = np.linspace(0, total_length, steps)

            scats_max = np.max(scats, axis=0)
            ax2.pcolor(wav, zs, scats, cmap="coolwarm")

            # 重建scat
            ax1.plot(wav, scats_max)

            reconstruct_error = []

            # 计算不同步长时重构光谱的误差
            # 每n行取一行
            scats_max_safe = scats_max[scats_max != 0]
            jump_steps = [2, 3, 4, 5, 6, 7, 8, 9, 10]
            for jump_step in jump_steps:
                result = scats[::jump_step]
                this_scats_max = np.max(result, axis=0)

                this_scats_max_safe = this_scats_max[scats_max!=0]

                dim_diff = np.abs(this_scats_max_safe - scats_max_safe) / scats_max_safe
                scats_max_diff_mean = np.mean(dim_diff)
                reconstruct_error.append(scats_max_diff_mean)

            # 计算未重构谱的误差
            max_int_idx = np.argmax(scats)  # 扁平索引
            max_int_idx = np.unravel_index(max_int_idx, scats.shape)  # 二维索引
            z0_idx = max_int_idx[0]
            wav0_idx = max_int_idx[1]
            scat_at_max_int = scats[z0_idx, :]

            scat_at_max_int = scat_at_max_int[scats_max != 0]

            dim_diff = np.abs(scat_at_max_int - scats_max_safe) / scats_max_safe
            scat_at_max_int_diff_mean = np.mean(dim_diff)
            reconstruct_error.append(scat_at_max_int_diff_mean)

            # reconstruct_error比jump_steps多一位，首位未重构误差的jump_steps用-1补齐
            jump_steps.append(-1)
            reconstruct_error_attrs = {"JunProc: jump_steps-reconstruct_error": [jump_steps, reconstruct_error]}
            particle.attrs.update(reconstruct_error_attrs)

            "wav-maxz曲线"
            maxz_indice = []
            for iWav, wav0 in enumerate(wav):
                ints = scats[:, iWav]
                maxz_idx = np.argmax(ints)
                maxz_indice.append(maxz_idx)

            maxz = zs[maxz_indice]
            maxz_range = np.max(maxz) - np.min(maxz)

            wav_maxz_attrs = {"JunProc: wav-maxz": [wav, maxz]}
            maxz_range_attrs = {
                "JunProc: maxz-range": maxz_range,
                "JunProc: maxz-range_min": np.min(maxz),
                "JunProc: maxz-range_max": np.max(maxz)}
            particle.attrs.update(wav_maxz_attrs)
            particle.attrs.update(maxz_range_attrs)

            # 拟合所有分段wav-maxz
            maxz = np.array(maxz)
            # 分段1：480-70
            fit_section = [[480, 700], [700, 950]]

            for iSection, section in enumerate(fit_section):
                x1 = fit_section[iSection][0]
                x2 = fit_section[iSection][1]
                x_for_fit, y_for_fit = choose_range(wav, maxz, x1=x1, x2=x2)
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

                if z2_idx == z1_idx:
                    continue

                # 记录粒子采集总耗时
                t_first = times[0]
                t_last = times[-1]
                t_diff = t_last - t_first
                total_second = t_diff.total_seconds()
                ratio1 = (len(times) + 1) / (len(times))
                total_second *= ratio1

                total_time_attrs = {f"JunProc: total time(s) {iSection}": total_second}
                total_second_stats.append(total_second)
                particle.attrs.update(total_time_attrs)

                t1 = times[z1_idx]
                t2 = times[z2_idx]
                t_diff = t2 - t1
                minimum_second = t_diff.total_seconds()
                ratio2 = (z2_idx - z1_idx + 1) / (z2_idx - z1_idx)  # 实际需要的时间为两个光谱创建的时间差 + 一条光谱的耗时
                minimum_second *= ratio2

                minimum_second_attrs = {f"JunProc: minimum required time(s) {iSection}": minimum_second}
                minimum_second_stats.append(minimum_second)
                particle.attrs.update(minimum_second_attrs)

                ax2.plot(x_for_fit, fitted_curve, "--", color="black")

            "最大强度处的z-int曲线"
            z0 = zs[z0_idx]
            wav0 = wav[wav0_idx]

            ax2.axvline(x=wav0, color="green", linestyle="--", linewidth=2)

            # 取出最大值所在波长位置的ints
            maxint_ints = scats[:, wav0_idx]
            ax3.plot(zs, maxint_ints, "-", label="data")
            title = "z_ints-at-max_int"

            try:
                A = np.max(maxint_ints)
                x0 = zs[np.argmax(maxint_ints)]
                sigma = 20
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
            except:
                pass

            save_path = os.path.join(os.path.dirname(filepath), fr"Image/Reconstuct_scat & stacked_scats/{process_type}_p{iParticle}.png")
            my_reconstruct_scat(ax1, title="Reconstructed Spectrum")
            my_zstack_scats(ax2, title="Z-Axis Stacked Spectra")
            fig.savefig(save_path)
            ax1.clear()
            ax2.clear()
            ax3.clear()
# plt.show()