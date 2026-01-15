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

# 误差-跳步 曲线
fig2, (ax2_left, ax2_right) = plt.subplots(1, 2, figsize=(12,8), dpi=100, sharey=True, gridspec_kw={'width_ratios': [3, 1]})
fig2.subplots_adjust(wspace=0.05)

figures3 = []
axes3 = []
for i in range(2):
    fig = plt.figure(figsize=(12, 8), dpi=100)
    ax = fig.add_subplot(111)
    figures3.append(fig)
    axes3.append(ax)

process_types = ["before_achro", "after_achro"]

"""处理"""
with h5py.File(filepath, "r") as f:
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

        reconstruct_error_stats = [None, None]
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

                # reconstruct_error
                jump_steps, reconstruct_error =  particle.attrs["JunProc: jump_steps-reconstruct_error"]
                reconstruct_error_stats[iType] = reconstruct_error if reconstruct_error_stats[iType] is None else np.vstack([reconstruct_error_stats[iType], reconstruct_error])
                " 处理完所有粒子, 保存在tiled image中"

                spectra = particle["Spectra/scan_z"]
                spectra_keys = spectra.keys()
                spectra_keys = sorted(spectra_keys, key=lambda x: int(x.split("_")[-1][1::]))
                scats = None
                # if iTile == 0 and iParticle == 0:
                # for iSpectra, sp_key in enumerate(spectra_keys):
                #
                #     print(f"=====当前处理: {process_type}:{iSpectra}/{total_particle_now}/{total_particle}=====")
                #     sp = spectra[sp_key]
                #
                #     wav = np.array(sp.attrs['wavelengths'])
                #
                #     bgd = np.array(sp.attrs['background'])
                #     bgd_time = sp.attrs['background_int'] / 1000
                #     bgd = bgd / bgd_time
                #
                #     ref = np.array(sp.attrs['reference'])
                #     ref_time = sp.attrs['reference_int'] / 1000
                #     ref = ref / ref_time
                #
                #     sg_time = sp.attrs['integration_time'] / 1000
                #     sg = np.array(sp)
                #     sg = sg / sg_time
                #
                #     numerator = sg - bgd  # 分子
                #
                #     denominator = ref - bgd  # 分母
                #     denominator[denominator == 0] = 1  # 如果分母为0，设为1
                #
                #     scat = numerator / denominator
                #
                #     wav, scat = choose_range(wav, scat, x1=450, x2=1000)
                #
                #     scats = scat if scats is None else np.vstack([scats, scat])
                #
                # max_int_idx = np.argmax(scats)  # 扁平索引
                # max_int_idx = np.unravel_index(max_int_idx, scats.shape)  # 二维索引
                # z0_idx = max_int_idx[0]
                # scat_at_max_int = scats[z0_idx, :]
                # ax.plot(wav, scat_at_max_int, '--', label="unreconstructed", color="black")
                #
                # scats_max = np.max(scats, axis=0)
                # fig = figures3[iType]
                # ax = axes3[iType]
                # ax.plot(wav, scats_max, label="origin(0.5 um per step)")
                # for iJumpStep, jump_step in enumerate(jump_steps):
                #     result = scats[::int(jump_step)]
                #     this_scats_max = np.max(result, axis=0)
                #     ax.plot(wav, this_scats_max, label=f"jump step: {jump_step}", linewidth=1)
                #
                # title = f"{process_type}-jump_step_reconstruct_scat"
                # my_reconstruct_scat_jump_step(ax, title=f"{process_type}-jump_step_reconstruct_scat")
                # save_path = os.path.join(os.path.dirname(filepath), fr"Image/Reconstruct_Error/{title}_p{total_particle_now}.png")
                # fig.savefig(save_path)
                # ax.clear()

        reconstruct_errors = []
        reconstruct_errors_errorbar = []
        for iJumpStep, jump_step in enumerate(jump_steps):
            fig = plt.figure(figsize=(12, 8), dpi=100)
            ax = fig.add_subplot(111)

            counts, bins, patches = ax.hist(x=reconstruct_error_stats[iType][:, iJumpStep], bins=30, color='blue', edgecolor='black',
                                            density=False)
            bin_centers = (bins[0:-1] + bins[1::]) / 2

            A = np.max(counts)
            x0 = bin_centers[np.argmax(counts)]
            if iJumpStep == -1:
                sigma = 0.25
            else:
                sigma = 0.01
            p0 = [A, x0, sigma]
            popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)
            wav_hist = np.arange(bins[0], bins[-1], 0.001)
            fitted_curve = gaussian(wav_hist, *popt)
            ax.plot(wav_hist, fitted_curve, '-', color='gray')

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
            reconstruct_errors.append(popt[1])
            FWFM = popt[2]*4
            FWHM = popt[2]*2*np.sqrt(2*np.log(2))
            reconstruct_errors_errorbar.append(FWHM)

            if iJumpStep == -1:  # error均为与step_length=0.5um的误差
                title = f"{process_type}-unreconstruct_error_stats"
            else:
                title = f"{process_type}-reconstruct_error_stats-jump_step_{int(jump_step)}"

            my_reconstruct_error_stats(ax, title=title)
            save_path = os.path.join(os.path.dirname(filepath), fr"Image/Reconstruct_Error/{title}.png")
            fig.savefig(save_path)
            plt.close(fig)

        step_length = np.array(jump_steps) * 0.5  # unit: um
        step_length[-1] = 50
        ax2_left.errorbar(step_length[:-1], reconstruct_errors[:-1], fmt='o-', color='blue' if iType == 0 else 'red', label=process_type, yerr=reconstruct_errors_errorbar[:-1],
                     capsize=5,  # 误差棒两端横线长度（可选，提升美观）
                     elinewidth=0,  # 误差棒线条宽度（可选）
                     markeredgewidth=2  # 误差棒端点宽度（可选）
                     )

        ax2_right.errorbar(step_length[-1], reconstruct_errors[-1], fmt='o-', color='blue' if iType == 0 else 'red',
                          label=process_type, yerr=reconstruct_errors_errorbar[-1],
                          capsize=5,  # 误差棒两端横线长度（可选，提升美观）
                          elinewidth=0,  # 误差棒线条宽度（可选）
                          markeredgewidth=2  # 误差棒端点宽度（可选）
                          )

        # 调整x轴范围
        ax2_left.set_xlim([0, 5.5])
        ax2_right.set_xlim([49.5, 50.5])

        # 隐藏不需要的轴线
        ax2_left.spines.right.set_visible(False)  # 隐藏ax1的底部轴线
        ax2_right.spines.left.set_visible(False)  # 隐藏ax2的顶部轴线

        # 调整刻度位置
        ax2_left.yaxis.tick_left()
        ax2_right.yaxis.tick_right()
        ax2_right.tick_params(labelright=False)

        d = 0.5  # 斜线的倾斜度
        kwargs = dict(
            marker=[(-1, -d), (1, d)],  # 定义斜线标记：左端点(-1,-d)，右端点(1,d)
            markersize=12,  # 标记大小
            linestyle="none",  # 无连接线
            color='k',  # 颜色：黑色
            mec='k', mew=1,  # 边缘颜色和宽度
            clip_on=False  # 禁用裁剪（允许超出坐标轴范围）
        )

        # 使用坐标轴坐标（而非数据坐标）
        ax2_left.plot([1, 1], [0, 1], transform=ax2_left.transAxes, **kwargs)
        ax2_right.plot([0, 0], [0, 1], transform=ax2_right.transAxes, **kwargs)

        title = f"{process_type}-Reconstruct_error-Step_size"
        my_reconstruct_error_jump_step_left(fig2, ax2_left, ax2_right, title=title)
        if iType == 1:
            save_path = os.path.join(os.path.dirname(filepath),
                                     fr"Image/Reconstruct_Error/{title}.png")
            fig2.savefig(save_path)
# plt.show()
