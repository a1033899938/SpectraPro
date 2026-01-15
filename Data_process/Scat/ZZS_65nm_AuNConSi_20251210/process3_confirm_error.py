from src.general.proc.ProcTrack import *
from Data_process.Scat.ZZS_65nm_AuNConAu_20260108.figure_setting import *

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

filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_65nm_AuNConSi_20251216\ZZS_65nm_AuNConSi_20251216.h5"
process_types = ["before_achro", "after_achro"]
roots = ["OceanOpticsSpectrometer/20251216/sample1_3",
         "OceanOpticsSpectrometer/20251219/after_achro"]
bgdfilepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_65nm_AuNConSi_circle_20251210\ZZS_65nm_AuNConSi_20251210.h5"
spectrometer_noise_filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_65nm_AuNConSi_circle_20251210\OceanOpticsSpectrometer_Noise.npz"

p0_linear = [0.05, -10]
bounds_linear = [[0, -50],
                 [0.2, 0]]

wav_range = [450, 900]
fit_section = [[500, 656.3], [656.3, 730]]

section_colors = ["#0E8585", "#830783"]
type_colors = ["blue", "red"]
recon_colors_1 = plt.get_cmap("Blues")(np.linspace(1, 0.1, 10))
recon_colors_2 = plt.get_cmap("Reds")(np.linspace(1, 0.1, 10))
jump_steps = [2, 3, 4, 5, 6]
cal_error_func = "SAM"
if cal_error_func == "SAM":
    escape_error = 2e-3
elif cal_error_func == "s1-s2":
    escape_error = 1e-6
elif cal_error_func == "residual":
    escape_error = 1e-5


for iType, (process_type, root) in enumerate(zip(process_types, roots)):
    PROC = ProcTrack(filepath, root)
    tile_keys, full_tile_keys = PROC.get_tile_keys()
    if iType == 0:
        with h5py.File(filepath, "r") as f:
            sp = f["OceanOpticsSpectrometer/ref_500ms_0"]
            ref_time = sp.attrs['integration_time'] / 1000
            ref = np.array(sp)
            ref = np.mean(ref, axis=0)
            ref = ref / ref_time
    else:
        with h5py.File(filepath, "r") as f:
            sp = f["OceanOpticsSpectrometer/ref_500ms_1"]
            ref_time = sp.attrs['integration_time'] / 1000
            ref = np.array(sp)
            ref = np.mean(ref, axis=0)
            ref = ref / ref_time

    with h5py.File(bgdfilepath, "r") as f:
        sp = f["OceanOpticsSpectrometer/20251210/sample1_circle_1/Tile_0/65nmAuNConSi_0/Spectra/scan_z/scan_z_p0"]
        ref_time = sp.attrs['integration_time'] / 1000
        bgd = np.array(sp.attrs['background'])
        bgd_time = sp.attrs['background_int'] / 1000
        bgd = bgd / bgd_time

    for iTile, full_tile_key in enumerate(full_tile_keys):
        particle_keys, full_particle_keys = PROC.get_particle_keys(full_tile_key)
        for iParticle, full_particle_key in enumerate(full_particle_keys):
            print(iType, iTile, iParticle)
            "跳过"

            fig = plt.figure(figsize=(12*2, 8*2), dpi=200)
            ax1 = fig.add_subplot(221)  # contour
            ax2 = fig.add_subplot(222)  # Recon. Scat
            ax3 = fig.add_subplot(223)  # Thumb image
            ax4 = fig.add_subplot(224)  # Recon. Process

            "Image"
            image_key, full_image_key = PROC.get_image_key(full_particle_key, 0)

            img, img_gray = PROC.proc_thumb_image(full_image_key, full_particle_key)  # full_particle_key

            is_valid = PROC.get_attrs(full_particle_key, f"JunProc: is_valid")
            if not is_valid:
                continue

            "Spectra"
            # 2d
            spectra_key, full_spectra_key = PROC.get_spectra_key(full_particle_key, "scan_z")
            wav, positions, scats, times = PROC.get_scanning(full_spectra_key, wav_range=wav_range, spectra_type="scat", if_despiking=True, bgd=bgd, ref=ref) # , bgd=bgd, ref=ref
            ax1.pcolor(wav, positions, scats, cmap="coolwarm")

            "wav-maxz曲线"
            maxz = PROC.proc_maxz(wav, positions, scats)

            "拟合wav-maxz曲线"
            popts = []
            ax = ax1
            for iSection, section in enumerate(fit_section):
                x1 = fit_section[iSection][0]
                x2 = fit_section[iSection][1]
                label = f"{int(x1)}- {int(x2)} nm"
                section_center = (x1 + x2) / 2

                x_for_fit, y_for_fit = choose_range(wav, maxz, x1=x1, x2=x2)
                popt, pcov = curve_fit(linear, x_for_fit, y_for_fit, p0=p0_linear, bounds=bounds_linear)
                popts.append(popt)
                fitted_curve = linear(x_for_fit, *popt)

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
                    idx0 = find_val_idx(positions, median_z)

            "reconstruct光谱"
            ax = ax2
            reconstruct_scat = np.max(scats, axis=0)
            ax.plot(wav, reconstruct_scat, "-", color="red", label="Recon. Scat")

            "重构过程"
            len_scats = len(positions)
            for jump_step in jump_steps:
                start_idx = idx0 % jump_step  # 找到包含idx1的起始点
                indices = np.arange(start_idx, len_scats, jump_step)
                len_jump_scats = len(indices)
                jump_scats = scats[indices, :]
                idx1 = np.where(indices == idx0)[0][0]

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
                    this_scats = jump_scats[idx1:idx2, :]

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
                            idx1 -= 1
                            if idx1 == 0:
                                if_reach_one_side = "left"
                        else:
                            idx2 += 1  # 范围右挪一格
                            if idx2 == len_jump_scats:
                                if_reach_one_side = "right"
                    else:
                        if if_reach_one_side == "left":
                            idx2 += 1  # 范围右挪一格
                            if idx2 == len_jump_scats+1:
                                break
                        elif if_reach_one_side == "right":
                            idx1 -= 1  # 范围左挪一格
                            if idx1 == -1:
                                break

                    i += 1

                ax.plot(wav, this_reconstruct_scat, label=f"{jump_step}")
            ax.legend()

                # ax = ax4
                #
                # iters = np.arange(0, len(errors), 1)
                # errors = np.array(errors)
                #
                # B = errors[-1]
                # I0 = errors[0] - B
                # idx = find_val_idx(errors, I0*0.37)
                # # tau = iters[idx]
                # tau=1
                # p0_exp = [I0, tau, B]
                # bounds_exp = [[0, 0, 0],
                #               [1, len_scats, escape_error*10]]
                #
                # popt, pcov = curve_fit(mono_exp, iters, errors, p0=p0_exp, bounds=bounds_exp, maxfev=5000, ftol=1e-9, xtol=1e-9)
                #
                # fitted_curve = mono_exp(iters, *popt)
                #
                # ax.plot(iters, errors, "o", linewidth=1, color=type_colors[iType], alpha=1,
                #           label=f"Data: Before Correction" if iType == 0 else f"Data: After Correction")
                # ax.plot(iters, fitted_curve, "-", linewidth=1, color=type_colors[iType], alpha=1,
                #           label=f"Fitted mono_exp: Before Correction" if iType == 0 else f"Fitted mono_exp: After Correction")
                # ax.axhspan(ymin=-escape_error, ymax=escape_error, color="lightgreen", alpha=0.1)
                # content = f"{My_Char.get('tau')}: {popt[1]:.2f}"
                # ax.text(x=0.5, y=0.5, s=content, fontsize=20, ha='center', va='top',
                #         color=type_colors[iType], weight='bold', transform=ax.transAxes)
                #
                # if not if_successfully_reconstruct:
                #     escape_idx1 = idx1
                #     escape_idx2 = idx2-1
                #     escape_i = i
                #
                # print(escape_idx1, escape_idx2)
                # escape_scats = scats[escape_idx1:escape_idx2, :]
                # escape_reconstruct_scat = np.max(escape_scats, axis=0)

            plt.show()
            input()

            "重构scat子图"
            color = "blue" if iType == 0 else "red"

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
    # loadpath = os.path.join(os.path.dirname(filepath), "Images", f"{process_type}_Statics_{cal_error_func}.npz")
    # with np.load(loadpath) as f:
    #     wav_maxz_popts_type = f["wav_maxz_popts_type"]
    #     iters_error_popts_type = f["iters_error_popts_type"]
    #     reconstruct_times_type = f["reconstruct_times_type"]

    """Tile结束"""
    "统计斜率"
    # wav_maxz_fit_slopes = np.array(wav_maxz_popts_type)[:, :, 0]  # 所有tile&particle, 所有section的slope
    #
    # step = 0.001
    # ax = ax11 if iType == 0 else ax21
    # this_slopes = wav_maxz_fit_slopes[:, :]
    # bins_start = np.min(this_slopes)
    # bins_end = np.max(this_slopes)
    # ratio = (bins_end - bins_start) * 0.05
    # x_hist = np.arange(bins_start - ratio, bins_end + ratio, 0.0001)
    # for iSection in range(2):
    #     slopes = np.array(wav_maxz_fit_slopes[:, iSection])
    #
    #     "拟合直线"
    #     x1 = fit_section[iSection][0]
    #     x2 = fit_section[iSection][1]
    #
    #     "Tile中所有斜率的统计"
    #     bin_min = np.min(slopes)  # 向下取整，保证包含最小值
    #     bin_max = np.max(slopes)  # 向上取整，保证包含最大值
    #     bins = np.arange(bin_min, bin_max + step, step)
    #
    #     label = f"{int(x1)}- {int(x2)} nm"
    #     counts, bins, patches = ax.hist(x=slopes, bins=bins, color=section_colors[iSection], alpha=0.5, edgecolor='black', density=False, label=label)
    #     fit_stats(ax, counts, bins, x_hist=x_hist, sigma=0.02,
    #               text_x=0.05, text_y=0.95 if iSection==0 else 0.9, color=section_colors[iSection], decimal=4)

    "统计重构速率(时间)"
    # iters_error_fit_tau = np.array(iters_error_popts_type)[:, 1]
    # ax = ax12 if iType == 0 else ax22
    # label = ("Before" if iType == 0 else "After") + " Correction"
    # counts, bins, patches = ax.hist(x=iters_error_fit_tau, bins=error_bins,
    #                                  color=type_colors[iType], alpha=0.5, edgecolor='black',
    #                                  density=False, label=label)
    # fit_stats(ax, counts, bins, sigma=3, text_x=0.95, text_y=0.95, color=type_colors[iType], ha="right")
    #
    # "统计时间"
    # ax = ax13 if iType == 0 else ax23
    # label = ("Before" if iType==0 else "After") + " Correction"
    # counts, bins, patches = ax.hist(x=np.array(reconstruct_times_type), bins=recon_bins,
    #                                  color=type_colors[iType], alpha=0.5, edgecolor='black',
    #                                  density=False, label=label)
    # fit_stats(ax, counts, bins, sigma=5, text_x=0.95, text_y=0.95, color=type_colors[iType], ha="right")
    # ax.legend(loc="best")
    #
    # savepath = os.path.join(os.path.dirname(filepath), "Images", f"{process_type}_Statics_{cal_error_func}")
    #
    # np.savez(savepath, wav_maxz_popts_type=wav_maxz_popts_type, iters_error_popts_type=iters_error_popts_type,
    #          reconstruct_times_type=reconstruct_times_type)

"""Type结束"""
# my_wav_maxz_fit_popt_stats(ax11, title="Fitted Slope Statistics", title_pad=30)
# my_wav_maxz_fit_popt_stats(ax21, title="", title_pad=0)
# my_reconstrution_error_fit_popt_stats(ax12, title="Recon. Convergence Time Stats")
# my_reconstrution_error_fit_popt_stats(ax22, title="", title_pad=0)
# my_wav_maxz_required_time_stats(ax13, title="Spectra Recon. Time Stats")
# my_wav_maxz_required_time_stats(ax23, title="", title_pad=0)
# save_path = os.path.join(os.path.dirname(filepath), "Images", f"Statics_{cal_error_func}.png")
# fig.savefig(save_path)
# plt.close(fig)
#
# print(f"统计粒子数: {particle_number}")


# plt.show()
# input()