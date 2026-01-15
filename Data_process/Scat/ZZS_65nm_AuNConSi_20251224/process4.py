import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from tifffile import transpose_axes

from src.general.proc.ProcTrack import *
from figure_setting import *
from src.my_style.my_color import MyColor

def fit_stats(ax, counts, bins, x_hist=None, sigma=20, text_x=0, text_y=0.9, color="black", decimal=2, ha="left"):
    try:
        bin_centers = (bins[0:-1] + bins[1::]) / 2
        A = np.max(counts)
        x0 = bin_centers[np.argmax(counts)]
        p0 = [A, x0, sigma]
        popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)
        if x_hist is None:
            x_hist = np.arange(bins[0], bins[-1], 0.001)
        fitted_curve = gaussian(x_hist, *popt)
        ax.plot(x_hist, fitted_curve, '-', color=color)

        text_content = f"Center:{popt[1]:.{decimal}f}  sigma:{popt[2]:.{decimal}f}"
        ax.text(
            x=text_x,
            y=text_y,
            s=text_content,
            fontsize=16,  # 字体大小（关键）
            ha=ha,  # 水平右对齐（避免文本超出图像）
            va='top',  # 垂直上对齐
            color=color,  # 文本颜色
            weight='bold',  # 加粗（可选）
            transform = ax.transAxes
        )
    except:
        pass

colors = [
    "#000000",  # 纯黑
    "#FF0000",  # 正红
    "#00FF00",  # 正绿
    "#0000FF",  # 正蓝
    "#FFFF00",  # 明黄
    "#00FFFF",  # 青色
    "#800080",  # 紫色
    "#FFA500",  # 橙色
    "#808080",  # 深灰
    "#FF69B4",  # 粉色
    "#A52A2A",  # 棕色
    "#228B22"  # 森林绿
]

filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_65nm_AuNConSi_20251225\ZZS_65nm_AuNConSi_20251224.h5"
process_types = ["before_achro", "after_achro"]
roots = ["", "OceanOpticsSpectrometer/20251224/after_achro"]

p0_linear = [0.05, -10]
bounds_linear = [[0, -50],
                 [0.2, 0]]

wav_range = [450, 900]
fit_section = [[500, 656.3], [656.3, 730]]

section_colors = ["#0E8585", "#830783"]
type_colors = ["blue", "red"]
escape_color = "lightgreen"
recon_colors_1 = plt.get_cmap("Blues")(np.linspace(1, 0.1, 10))
recon_colors_2 = plt.get_cmap("Reds")(np.linspace(1, 0.1, 10))
cal_error_func = "s1-s2"
if cal_error_func == "SAM":
    escape_error = 2e-3
    error_bins = np.arange(0, 10, 0.1)
elif cal_error_func == "s1-s2":
    escape_error = 1e-6
    error_bins = np.arange(0, 6, 0.05)
elif cal_error_func == "residual":
    escape_error = 1e-5
    # error_bins = np.arange(0, 6 + 0.3, 0.3)
recon_bins = np.arange(0, 23, 0.5)

if_plot1 = True
if_plot2 = True
if_import_data = True

"""处理图片"""
fig = plt.figure(figsize=(12 * 3, 8 * 2), dpi=200)
ax11 = fig.add_subplot(231)  # Fitted Slope
ax12 = fig.add_subplot(232)  # Recon. tau
ax13 = fig.add_subplot(233)  # Recon. Time
axes1 = [ax11, ax12, ax13]

ax21 = fig.add_subplot(234, sharex=ax11)
ax22 = fig.add_subplot(235, sharex=ax12)
ax23 = fig.add_subplot(236, sharex=ax13)
axes2 = [ax21, ax22, ax23]

bgd_color1 = (0, 0, 1, 0.1)
bgd_color2 = (1, 0, 0, 0.1)
bgd_colors = [bgd_color1, bgd_color2]

axess = [axes1, axes2]
particle_number = [0, 0]
for iAxes, axes in enumerate(axess):
    color = bgd_colors[iAxes]
    for ax in axes:
        ax.set_facecolor(color)  # 光谱组蓝背景

for iType, (process_type, root) in enumerate(zip(process_types, roots)):
    if iType == 0:
        continue
    PROC = ProcTrack(filepath, root)
    tile_keys, full_tile_keys = PROC.get_tile_keys()
    if not if_import_data:
        if iType == 1:
            with h5py.File(filepath, "r") as f:
                sp = f["OceanOpticsSpectrometer/ref_200ms_while_bgd_200ms_0"]
                bgd = np.array(sp.attrs["background"])
                bgd_time = sp.attrs["background_int"] / 1000
                bgd = bgd / bgd_time

                ref_time = sp.attrs['integration_time'] / 1000
                ref = np.array(sp)
                ref = np.mean(ref, axis=0)
                ref = ref / ref_time
            ref_minus_bgd = ref - bgd

        wav_maxz_popts_type = []
        iters_error_popts_type = []
        reconstruct_times_type = []
        for iTile, full_tile_key in enumerate(full_tile_keys):
            # if iTile >= 1:
            #     continue
            particle_keys, full_particle_keys = PROC.get_particle_keys(full_tile_key)
            for iParticle, full_particle_key in enumerate(full_particle_keys):
                print(iType, iTile, iParticle)
                "跳过"

                if if_plot2:
                    fig2 = plt.figure(figsize=(12 * 2, 8 * 2), dpi=200)
                    ax2_11 = fig2.add_subplot(221)  # contour
                    ax2_12 = fig2.add_subplot(222)  # Recon. Scat
                    ax2_21 = fig2.add_subplot(223)  # Thumb image
                    ax2_21_inset = ax2_21.inset_axes([0.7, 0.7, 0.18, 0.18])
                    ax2_22 = fig2.add_subplot(224)  # Recon. Process

                "Image"
                image_key, full_image_key = PROC.get_image_key(full_particle_key, 0)

                # SAVE
                if if_plot2:
                    img, img_gray = PROC.proc_thumb_image(full_image_key, full_particle_key)  # full_particle_key

                is_valid = PROC.get_attrs(full_particle_key, f"JunProc: is_valid")
                if not is_valid:
                    continue
                particle_number[iType] += 1

                if if_plot2:
                    ax2_21.imshow(img) if if_plot1 else None
                    ax2_21_inset.imshow(img_gray)  if if_plot1 else None

                "Spectra"
                # 2d
                spectra_key, full_spectra_key = PROC.get_spectra_key(full_particle_key, "scan_z")
                wav, positions, scats, times = PROC.get_scanning(full_spectra_key, wav_range=wav_range, spectra_type="scat", if_despiking=True, ref_minus_bgd=ref_minus_bgd) # , bgd=bgd, ref=ref
                ax2_11.pcolor(wav, positions, scats, cmap="coolwarm") if if_plot2 else None
                "wav-maxz曲线"
                maxz = PROC.proc_maxz(wav, positions, scats)

                "拟合wav-maxz曲线"
                popts = []
                ax = ax2_11
                for iSection, section in enumerate(fit_section):
                    x1 = fit_section[iSection][0]
                    x2 = fit_section[iSection][1]
                    label = f"{int(x1)}- {int(x2)} nm"
                    section_center = (x1 + x2) / 2

                    x_for_fit, y_for_fit = choose_range(wav, maxz, x1=x1, x2=x2)
                    popt, pcov = curve_fit(linear, x_for_fit, y_for_fit, p0=p0_linear, bounds=bounds_linear)
                    popts.append(popt)
                    fitted_curve = linear(x_for_fit, *popt)

                    if if_plot2:
                        ax.plot(wav, maxz, "-", color="lightblue", label="Data - Focused Position")
                        ax.plot(x_for_fit, fitted_curve, "--", color=section_colors[iSection], linewidth=2,
                                 label=f"Fitted Line: {label}")
                        content = f"Slope(um/nm): \n{popt[0]:.3f}"
                        ax.text(x=section_center, y=8.5, s=content, fontsize=15, ha='center', va='top',
                                 color=section_colors[iSection], weight='bold')

                    # 取出第一段曲线的拟合直线
                    if iSection == 0:
                        median_wav_idx = len(x_for_fit)//2
                        median_z = fitted_curve[median_wav_idx]
                        idx1 = find_val_idx(positions, median_z)
                wav_maxz_popts_type.append(popts)

                "reconstruct光谱"
                reconstruct_scat = np.max(scats, axis=0)

                "重构过程"
                z_idx_range = len(positions)

                # 令起点为section1拟合直线的中点
                fitted_curve = linear(x_for_fit, *popts[0])

                idx2 = idx1 + 1
                i = 0

                wav_idx1 = find_val_idx(wav, fit_section[0][0])
                wav_idx2 = find_val_idx(wav, fit_section[0][1])

                errors = []
                if_successfully_reconstruct = False
                if_reach_one_side = None

                while True:
                    this_scats = scats[idx1:idx2, :]

                    this_reconstruct_scat = np.max(this_scats, axis=0)

                    error = cal_error(reconstruct_scat[wav_idx1:wav_idx2], this_reconstruct_scat[wav_idx1:wav_idx2], func=cal_error_func)
                    errors.append(error)

                    # 如果第一次低于阈值，则记录此时的idx
                    if error < escape_error and not if_successfully_reconstruct:
                        if_successfully_reconstruct = True
                        escape_idx1 = idx1
                        escape_idx2 = idx2-1
                        escape_i = i

                    if if_reach_one_side is None:
                        if i % 2 == 0:
                            idx1 -= 1  # 范围左挪一格
                            if idx1 == 0:
                                if_reach_one_side = "left"
                        else:
                            idx2 += 1  # 范围右挪一格
                            if idx2 == z_idx_range:
                                if_reach_one_side = "right"
                    else:
                        if if_reach_one_side == "left":
                            idx2 += 1  # 范围右挪一格
                            if idx2 == z_idx_range+1:
                                break
                        elif if_reach_one_side == "right":
                            idx1 -= 1  # 范围左挪一格
                            if idx1 == -1:
                                break

                    i += 1
                iters = np.arange(0, len(errors), 1)
                errors = np.array(errors)

                B = errors[-1]
                I0 = errors[0] - B
                idx = find_val_idx(errors, I0*0.37)
                # tau = iters[idx]
                tau=1
                p0_exp = [I0, tau, B]
                bounds_exp = [[0, 0, 0],
                              [1, z_idx_range, escape_error*10]]

                popt, pcov = curve_fit(mono_exp, iters, errors, p0=p0_exp, bounds=bounds_exp, maxfev=5000, ftol=1e-9, xtol=1e-9)
                # print(pcov)
                # input()
                fitted_curve = mono_exp(iters, *popt)
                if if_plot2:
                    ax2_22.plot(iters, errors, "o", linewidth=1, color=type_colors[iType], alpha=1,
                              label=f"Data: Before Correction" if iType == 0 else f"Data: After Correction")
                    ax2_22.plot(iters, fitted_curve, "-", linewidth=1, color=type_colors[iType], alpha=1,
                              label=f"Fitted mono_exp: Before Correction" if iType == 0 else f"Fitted mono_exp: After Correction")
                    ax2_22.axhspan(ymin=-escape_error, ymax=escape_error, color=escape_color, alpha=0.1)
                    iters_error_popts_type.append(popt)
                    content = f"{My_Char.get('tau')}: {popt[1]:.2f}"
                    ax2_22.text(x=0.5, y=0.5, s=content, fontsize=20, ha='center', va='top',
                            color=type_colors[iType], weight='bold', transform=ax2_22.transAxes) if if_plot1 else None

                if not if_successfully_reconstruct:
                    escape_idx1 = idx1
                    escape_idx2 = idx2-1
                    escape_i = i

                escape_scats = scats[escape_idx1:escape_idx2, :]
                escape_reconstruct_scat = np.max(escape_scats, axis=0)

                "重构scat子图"
                color = "blue" if iType == 0 else "red"

                ax = ax2_12
                if if_plot2:
                    ax.plot(wav, reconstruct_scat, color="black", linewidth=1, alpha=0.5, label="Recon. by Global")
                    ax.plot(wav, escape_reconstruct_scat, color=color, linewidth=1, alpha=0.5, label=f"Recon. by Local: {escape_i}")
                    ax.set_xticks([])  # 隐藏x轴刻度
                    ax.set_yticks([])  # 隐藏y轴刻度
                    ax.legend()
                reconstruct_time = PROC.proc_reconstruct_time(full_spectra_key, escape_idx1, escape_idx2)
                reconstruct_times_type.append(reconstruct_time)

                """Tile结束"""
                "save fig"
                if if_plot2:
                    my_zstack_scats(ax2_11, ytick=np.arange(positions[0], positions[-1]+5, 5), title="Z-Axis Stacked Spectra", title_pad=30)
                    my_reconstruct_scat(ax2_12, title="Recon. Scattering", title_pad=30, bbox_to_anchor=None)
                    my_thumb_image(ax2_21, title="Thumb Image")
                    my_reconstrution_process_error(ax2_22, title="Recon. Iteration Process")

                    save_path = os.path.join(os.path.dirname(filepath),
                                             fr"Images//{cal_error_func}//{process_type}_Tile{iTile}_p{iParticle}.png")
                    fig2.savefig(save_path)
                    plt.close(fig2)

    """导入结果"""
    if if_import_data:
        loadpath = os.path.join(os.path.dirname(filepath), "Images", f"{process_type}_Statics_{cal_error_func}.npz")
        with np.load(loadpath) as f:
            wav_maxz_popts_type = f["wav_maxz_popts_type"]
            iters_error_popts_type = f["iters_error_popts_type"]
            reconstruct_times_type = f["reconstruct_times_type"]

    """Tile结束"""
    "统计斜率"
    wav_maxz_fit_slopes = np.array(wav_maxz_popts_type)[:, :, 0]  # 所有tile&particle, 所有section的slope

    step = 0.001
    ax = ax11 if iType == 0 else ax21
    this_slopes = wav_maxz_fit_slopes[:, :]
    bins_start = np.min(this_slopes)
    bins_end = np.max(this_slopes)
    ratio = (bins_end - bins_start) * 0.05
    x_hist = np.arange(bins_start - ratio, bins_end + ratio, 0.0001)
    for iSection in range(2):
        slopes = np.array(wav_maxz_fit_slopes[:, iSection])

        "拟合直线"
        x1 = fit_section[iSection][0]
        x2 = fit_section[iSection][1]

        "Tile中所有斜率的统计"
        bin_min = np.min(slopes)  # 向下取整，保证包含最小值
        bin_max = np.max(slopes)  # 向上取整，保证包含最大值
        bins = np.arange(bin_min, bin_max + step, step)

        label = f"{int(x1)}- {int(x2)} nm"
        counts, bins, patches = ax.hist(x=slopes, bins=bins, color=section_colors[iSection], alpha=0.5, edgecolor='black', density=False, label=label)
        fit_stats(ax, counts, bins, x_hist=x_hist, sigma=0.02,
                  text_x=0.05, text_y=0.95 if iSection==0 else 0.9, color=section_colors[iSection], decimal=4)

    "统计重构速率(时间)"
    iters_error_fit_tau = np.array(iters_error_popts_type)[:, 1]
    ax = ax12 if iType == 0 else ax22
    label = ("Before" if iType == 0 else "After") + " Correction"
    counts, bins, patches = ax.hist(x=iters_error_fit_tau, bins=error_bins,
                                     color=type_colors[iType], alpha=0.5, edgecolor='black',
                                     density=False, label=label)
    fit_stats(ax, counts, bins, sigma=3, text_x=0.95, text_y=0.95, color=type_colors[iType], ha="right")

    "统计时间"
    ax = ax13 if iType == 0 else ax23
    label = ("Before" if iType==0 else "After") + " Correction"
    counts, bins, patches = ax.hist(x=np.array(reconstruct_times_type), bins=recon_bins,
                                     color=type_colors[iType], alpha=0.5, edgecolor='black',
                                     density=False, label=label)
    fit_stats(ax, counts, bins, sigma=5, text_x=0.95, text_y=0.95, color=type_colors[iType], ha="right")
    ax.legend(loc="best")

    if not if_import_data:
        savepath = os.path.join(os.path.dirname(filepath), "Images", f"{process_type}_Statics_{cal_error_func}")

        np.savez(savepath, wav_maxz_popts_type=wav_maxz_popts_type, iters_error_popts_type=iters_error_popts_type,
                 reconstruct_times_type=reconstruct_times_type)

"""Type结束"""
my_wav_maxz_fit_popt_stats(ax11, title="Fitted Slope Statistics", title_pad=30)
my_wav_maxz_fit_popt_stats(ax21, title="", title_pad=0)
my_reconstrution_error_fit_popt_stats(ax12, title="Recon. Convergence Time Stats")
my_reconstrution_error_fit_popt_stats(ax22, title="", title_pad=0)
my_wav_maxz_required_time_stats(ax13, title="Spectra Recon. Time Stats")
my_wav_maxz_required_time_stats(ax23, title="", title_pad=0)
save_path = os.path.join(os.path.dirname(filepath), "Images", f"Statics_{cal_error_func}.png")
fig.savefig(save_path)
plt.close(fig)

print(f"统计粒子数: {particle_number}")


# plt.show()
# input()