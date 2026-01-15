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

filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_AuNC_65nm_20251206\ZZS_AuNC_65nm_20251206.h5"

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
    process_type = "after_achro"

    root_folder = f[f"OceanOpticsSpectrometer/20251207/sample2"] # Tile_1/65nmAuNC_4/Image/

    tiled_image_keys = list(root_folder.keys())
    tiled_image_keys = sorted(tiled_image_keys, key=lambda x: int(x.split("_")[-1]))
    bgd = None
    ref = None

    # 找到粒子总数
    last_tiled_image = root_folder[tiled_image_keys[-1]]
    particle_in_last_tiled_image_keys = list(last_tiled_image.keys())
    particle_in_last_tiled_image_keys.remove("tiled_image")
    particle_in_last_tiled_image_keys = sorted(particle_in_last_tiled_image_keys, key=lambda x: int(x.split("_")[-1]))
    last_particle = last_tiled_image[particle_in_last_tiled_image_keys[-1]]
    total_particle = int(last_particle.attrs["total_particle_now"])

    for iTile, tiled_image_key in enumerate(tiled_image_keys):
        tiled_image = root_folder[tiled_image_key]

        # if iTile != 3:
        #     continue

        particle_keys = list(tiled_image.keys())
        particle_keys.remove("tiled_image")
        particle_keys = sorted(particle_keys, key=lambda x: int(x.split("_")[-1]))

        wav_maxz_fit_popts_stats = []
        total_second_stats = []
        minimum_second_stats = []
        for iParticle, particle_key in enumerate(particle_keys):
            particle = tiled_image[particle_key]
            total_particle_now = int(particle.attrs["total_particle_now"])

            # if iParticle != 3:
            #     continue


            """删除过去的处理结果"""
            keys_to_delete = []
            for proc_atts in particle.attrs:
                if "JunProc" in proc_atts:
                    keys_to_delete.append(proc_atts)
            if len(keys_to_delete) > 0:
                for key in keys_to_delete:
                    del particle.attrs[key]


            """处理图像-判断光谱组是否有效"""
            img = particle["Image//OM thumb image"]

            img = np.asarray(img)
            # ax4.imshow(img)
            my_thumb_image(ax4, title="Thumb Image")
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

            # ax4_inset.imshow(img)

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

            # if len(peaks_h) >= 2 or len(peaks_h) == 0:
            #     flag1 = True
            # else:
            #     if np.abs(peaks_h[0] - len(proj_h)/2) > 30:
            #         flag1 = True
            #
            # if len(peaks_v) >= 2 or len(peaks_v) == 0:
            #     flag2 = True
            # else:
            #     if np.abs(peaks_v[0] - len(proj_v) / 2) > 30:
            #         flag2 = True

            if np.abs(max_h_idx - len(proj_h)/2) > 30:
                flag1 = True
            if np.abs(max_v_idx - len(proj_v)/2) > 30:
                flag2 = True

            # if particle.name == "/OceanOpticsSpectrometer/20251207/sample2/Tile_1/65nmAuNConSi_0":
            #     fig = plt.figure(figsize=(12, 8))
            #     ax = fig.add_subplot(111)
            #     ax.imshow(img)
            #     ax.plot(range(100), proj_h, "red")
            #     ax.plot(proj_v, range(100), "blue")
            #     plt.show()
            #     print(flag1, flag2)
            #     input("按回车键继续...")

            if flag1 or flag2:
                particle.attrs.update({"JunProc: is_valid": False})
                continue

            """粒子居中的组，标记并处理"""
            # 标记
            particle.attrs.update({"JunProc: is_valid": True})

            spectra = particle["Spectra/scan_z"]

            steps = spectra.attrs["steps"]
            total_length = spectra.attrs["total length(um)"]

            spectra_keys = spectra.keys()

            # 由于track中断重新采谱，导致一个scan_z里有两组谱，因此删除第二组
            # if tiled_image_key == "Tile_0" and particle_key == "65nmAuNC_0":
            #     del particle["Spectra/scan_xy"]
            #     for key in spectra_keys:
            #         if "p" not in key.split("_")[-1]:
            #             del spectra[key]
            #
            # if tiled_image_key == "Tile_0" and particle_key == "65nmAuNC_1":
            #     for key in spectra_keys:
            #         if "p" not in key.split("_")[-1]:
            #             del spectra[key]

            spectra_keys = sorted(spectra_keys, key=lambda x: int(x.split("_")[-1][1::]))

            scats = None
            times = []
            "历遍该粒子所有光谱"
            for iSpectra, sp_key in enumerate(spectra_keys):
                print(f"=====当前处理: {process_type}:{iSpectra}/{total_particle_now}/{total_particle}=====")
                sp = spectra[sp_key]

                # if iSpectra != 50:
                #     continue

                time_now = sp.attrs['creation_timestamp']
                time_now = datetime.fromisoformat(time_now)
                times.append(time_now)

                wav = np.array(sp.attrs['wavelengths'])

                # 仅获取第一条光谱的bgd, ref, 节省时间
                if bgd is None:
                    bgd = np.array(sp.attrs['background'])
                    bgd_time = sp.attrs['background_int'] / 1000
                    bgd = bgd / bgd_time

                if ref is None:
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

                wav, scat = choose_range(wav, scat, x1=450, x2=900)

                scats = scat if scats is None else np.vstack([scats, scat])

            """处理完组内所有光谱, 保存在particle中"""
            zs = np.linspace(0, total_length, steps)

            scats_max = np.max(scats, axis=0)
            # ax2.pcolor(wav, zs, scats, cmap="coolwarm")

            # 重建scat
            # ax1.plot(wav, scats_max)

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
                # ax2.plot(x_for_show, y_for_show, color="blue" if iSection == 0 else "red")

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

                # 记录粒子采集总耗时
                t_first = times[0]
                t_last = times[-1]
                t_diff = t_last - t_first
                total_second = t_diff.total_seconds()
                ratio1 = (len(times) + 1) / (len(times))
                total_second *= ratio1

                total_time_attrs = {f"JunProc: total time(s)": total_second}
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

                # ax2.plot(x_for_fit, fitted_curve, "--", color="black")

            "最大强度处的z-int曲线"
            wavs_target = [486.1, 587.6, 656.3] + [wav_max]
            wavs_indice_target = [find_val_idx(wav, wav_target) for wav_target in wavs_target] + [wav0_idx]
            colors = ["blue", "green", "red", "orange"]

            sorted_tuples  = sorted(zip(wavs_target, wavs_indice_target, colors), key=lambda x: x[0])
            wavs_target, wavs_indice_target, colors = zip(*sorted_tuples)

            for iWavTarget, (color, wav_target, wav_index_target) in enumerate(zip(colors, wavs_target, wavs_indice_target)):
                # ax2.axvline(x=wav_target, color=color, linestyle="--", linewidth=2)
                # 对应波长位置的ints
                ints_target = scats[:, wav_index_target]
                # ax3.plot(zs, ints_target, "-", color=color, label=f"data - {wav_target:.1f} nm")
                title = "z-int at Target Wavelength"
                # my_maxint_ints(ax3, title=title)

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

                    # ax3.plot(zs, fitted_curve, '--', color=color, label=f"gaussian fit - {wav_target:.1f} nm")
                    my_maxint_ints(ax3, title=title)

                    mag, z0, sigma = popt
                except:
                    pass

                # text_x = 0.05
                # text_y = 0.95 - 0.05 * iWavTarget
                # text_content1 = f"A: {mag:.2e}" if mag is not None else "A: --"
                # text_content2 = f"z0: {z0:.1f}" if z0 is not None else "z0: --"
                # text_content3 = f"sigma: {sigma:.1f}" if sigma is not None else "sigma: --"
                # text_content = text_content1 + " " +  text_content2 + " " +  text_content3
                # ax3.text(
                #     x=text_x,
                #     y=text_y,
                #     s=text_content,
                #     fontsize=15,  # 字体大小（关键）
                #     ha='left',  # 水平右对齐（避免文本超出图像）
                #     va='top',  # 垂直上对齐
                #     color=color,  # 文本颜色
                #     weight='bold',  # 加粗（可选）
                #     transform=ax3.transAxes
                # )

            # save_path = os.path.join(os.path.dirname(filepath), fr"Image/Reconstuct_scat & stacked_scats/{process_type}_p{total_particle_now}.png")
            # my_reconstruct_scat(ax1, title="Reconstructed Spectrum")
            # my_zstack_scats(ax2, title="Z-Axis Stacked Spectra")
            # fig.savefig(save_path)
            # ax1.clear()
            # ax2.clear()
            # ax3.clear()
# plt.show()