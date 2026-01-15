from src.general.proc.ProcTrack import *
from Data_process.Scat.ZZS_65nm_AuNConAu_20260108.figure_setting import *

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

filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_65nm_AuNConSi_circle_20251210\ZZS_65nm_AuNConSi_20251210.h5"
process_types = ["before_achro", "after_achro"]
roots = ["OceanOpticsSpectrometer/20251210/sample1_before_achro_circle",
         "OceanOpticsSpectrometer/20251210/sample1_circle_1"]
spectrometer_noise_filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_65nm_AuNConSi_circle_20251210\OceanOpticsSpectrometer_Noise.npz"

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
    error_bins = np.arange(0, 10, 0.5)
elif cal_error_func == "s1-s2":
    escape_error = 1e-6
    error_bins = np.arange(0, 6, 0.3)
elif cal_error_func == "residual":
    escape_error = 1e-5
    # error_bins = np.arange(0, 6 + 0.3, 0.3)
recon_bins = np.arange(0, 23, 1)

noise_data = np.load(spectrometer_noise_filepath)
wav_noise = noise_data["wav"]
spectrometer_noise = noise_data["noise_FWFM"]

if_plot = True

for iParticle in range(10):
    if iParticle == 1 or iParticle == 5:
        continue

    """处理图片"""
    fig = plt.figure(figsize=(12 * 4, 8 * 2), dpi=200)
    ax11 = fig.add_subplot(241)
    ax12 = fig.add_subplot(242)
    ax13 = fig.add_subplot(243)
    ax14 = fig.add_subplot(244)
    # ax14_inset = ax14.inset_axes([0.7, 0.7, 0.18, 0.18])
    axes1 = [ax11, ax12]

    ax21 = fig.add_subplot(245, sharex=ax11)
    ax22 = fig.add_subplot(246, sharex=ax12)
    ax23 = fig.add_subplot(247)
    ax24 = fig.add_subplot(248)
    axes2 = [ax21, ax22]

    bgd_color1 = (0, 0, 1, 0.1)
    bgd_color2 = (1, 0, 0, 0.1)
    bgd_colors = [bgd_color1, bgd_color2]

    axess = [axes1, axes2]
    for iAxes, axes in enumerate(axess):
        color = bgd_colors[iAxes]
        for ax in axes:
            ax.set_facecolor(color)  # 光谱组蓝背景


    """ax13子图"""
    ax_insets = [[None for i in range(5)] for j in range(2)]
    for i in range(10):
        row = i // 5
        col = i % 5

        if row == 0:
            pos = [col*0.2, 0.8]
        else:
            pos = [col*0.2, 0.6]
        ax_inset = ax13.inset_axes([pos[0]+0.01, pos[1]+0.01, 0.18, 0.18])
        ax_insets[row][col] = ax_inset

    max_values_ax13 = []
    for iType, (process_type, root) in enumerate(zip(process_types, roots)):
        PROC = ProcTrack(filepath, root)

        reconstruct_scats = []
        scats_tile = []
        maxzs_tile = []
        wav_maxz_popts_tile = []  # tile, section, [k, b]

        iters_errors_tile = []
        iters_error_popts_tile = []  # I0, tau, B
        iColor = 0
        reconstruct_times = []

        reconstruct_scat_base = None
        for iTile in range(10):
            full_particle_key = f"{root}//Tile_{iTile}//65nmAuNConSi_{iParticle}"

            # print(iType, iTile, iParticle)
            "跳过"
            if iTile >= 10:
                continue

            """删除unvalid的图片"""
            # is_valid = PROC.get_attrs(full_particle_key, f"JunProc: is_valid")
            # from pathlib import Path
            # if not is_valid:
            #     save_path = Path(os.path.join(os.path.dirname(filepath), fr"Image/Reconstuct_scat & stacked_scats/{process_type}_p{iParticle}_t{iTile}.png"))
            #     if save_path.exists() and save_path.is_file():
            #         print(iType, iTile, iParticle)
            #         save_path.unlink()

            "Image"
            image_key, full_image_key = PROC.get_image_key(full_particle_key, 0)

            # SAVE
            img, img_gray = PROC.proc_thumb_image(full_image_key, full_particle_key)  # full_particle_key
            is_valid = PROC.get_attrs(full_particle_key, f"JunProc: is_valid")
            if not is_valid:
                continue
            # ax14.imshow(img)  ####################
            # ax14_inset.imshow(img_gray)  ####################

            "Spectra"
            # 2d
            spectra_key, full_spectra_key = PROC.get_spectra_key(full_particle_key, "scan_z")
            wav, positions, scats, times = PROC.get_scanning(full_spectra_key, wav_range=wav_range, spectra_type="scat", if_despiking=True)
            scats_tile.append(scats)

            "计算加入噪声背景后的曲线误差，衡量误差阈值"
            # _, _, scats_with_noise, times = PROC.get_added_noise_scanning(full_spectra_key, spectrometer_noise/2, wav_range=wav_range, spectra_type="scat")
            # reconstruct_scat_with_noise = np.max(scats_with_noise, axis=0)  # 加上背景
            #
            # fig = plt.figure(figsize=(12, 8), dpi=200)
            # ax = fig.add_subplot(111)
            #
            #
            # error = cal_error(reconstruct_scat, reconstruct_scat_with_noise)
            # ax.plot(wav, reconstruct_scat, "-", color="gray", label="Reconstructed Scat")
            # ax.plot(wav, reconstruct_scat_with_noise, "-", color="black", label="Reconstructed Scat(add noise)")
            # ax.text(x=0.05, y=0.1, s=f"Reconstructed Error: {error}", color="red", fontsize=20, fontweight="bold", transform=ax.transAxes)
            #
            # my_reconstruct_scat_with_noise(ax)
            # print(error)
            # plt.show()
            # input()

            "wav-maxz曲线"
            maxz = PROC.proc_maxz(wav, positions, scats)
            maxzs_tile.append(maxz)

            "拟合wav-maxz曲线"
            popts = []
            for iSection, section in enumerate(fit_section):
                x1 = fit_section[iSection][0]
                x2 = fit_section[iSection][1]
                x_for_fit, y_for_fit = choose_range(wav, maxz, x1=x1, x2=x2)
                popt, pcov = curve_fit(linear, x_for_fit, y_for_fit, p0=p0_linear, bounds=bounds_linear)
                popts.append(popt)

                # 取出第一段曲线的拟合直线
                if iSection == 0:
                    fitted_curve = linear(x_for_fit, *popts[0])
                    median_wav_idx = len(x_for_fit)//2
                    median_z = fitted_curve[median_wav_idx]
                    idx1 = find_val_idx(positions, median_z)

            wav_maxz_popts_tile.append(popts)

            "reconstruct光谱"
            reconstruct_scat = np.max(scats, axis=0)

            "重构过程"
            idx_range = len(positions)

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
                        if idx2 == 41:
                            if_reach_one_side = "right"
                else:
                    if if_reach_one_side == "left":
                        idx2 += 1  # 范围右挪一格
                        if idx2 == 42:
                            break
                    elif if_reach_one_side == "right":
                        idx1 -= 1  # 范围左挪一格
                        if idx1 == -1:
                            break

                i += 1
            iters = np.arange(0, len(errors), 1)
            errors = np.array(errors)
            iters_errors_tile.append(errors)

            B = errors[-1]
            I0 = errors[0] - B
            idx = find_val_idx(errors, I0*0.37)
            tau = iters[idx]
            p0_exp = [I0, tau, B]
            bounds_exp = [[0, 0, 0],
                          [1, 41, escape_error*10]]

            popt, pcov = curve_fit(mono_exp, iters, errors, p0=p0_exp, bounds=bounds_exp)
            fitted_curve = mono_exp(iters, *popt)

            iters_error_popts_tile.append(popt)

            if not if_successfully_reconstruct:
                escape_idx1 = idx1
                escape_idx2 = idx2-1
                escape_i = i

            escape_scats = scats[escape_idx1:escape_idx2, :]
            escape_reconstruct_scat = np.max(escape_scats, axis=0)

            "重构scat子图"
            color = "blue" if iType == 0 else "red"
            row = iTile // 5
            col = iTile % 5

            ax = ax_insets[row][col]
            ax.plot(wav, reconstruct_scat, color=color, linewidth=1, alpha=0.2)
            ax.plot(wav, escape_reconstruct_scat, color=color, linewidth=0.3, alpha=1, label=escape_i)
            ax.set_xticks([])  # 隐藏x轴刻度
            ax.set_yticks([])  # 隐藏y轴刻度
            ax.legend()
            reconstruct_time = PROC.proc_reconstruct_time(full_spectra_key, escape_idx1, escape_idx2)
            reconstruct_times.append(reconstruct_time)

            ax = ax = ax13

            if iType == 0:
                the_colors = recon_colors_1
            else:
                the_colors = recon_colors_2

            if reconstruct_scat_base is None:
                reconstruct_scat_base = escape_reconstruct_scat
                ax.plot(wav, reconstruct_scat_base, color=the_colors[iColor], linewidth=1, alpha=1, label="Before Correction" if iType == 0 else "After Correction")
                iColor += 1

            error = cal_error(reconstruct_scat_base, escape_reconstruct_scat, func=cal_error_func)

            if error > (5*escape_error):
                ax.plot(wav, escape_reconstruct_scat, color=the_colors[iColor], linewidth=1, alpha=1)
                iColor += 1

            max_values_ax13.append(np.max(escape_reconstruct_scat) / 0.45)

        """Tile结束"""
        "统计斜率"
        wav_maxz_fit_slopes = np.array(wav_maxz_popts_tile)[:, :, 0]  # 所有tile, 所有section的slope
        wav_maxz_section1_fit_slopes = wav_maxz_fit_slopes[:, 0]  # section1的slope
        median_slope_idx = argmedian(wav_maxz_section1_fit_slopes)

        scats = scats_tile[median_slope_idx]
        maxz = maxzs_tile[median_slope_idx]
        popts = wav_maxz_popts_tile[median_slope_idx]

        ax1 = ax11 if iType == 0 else ax21

        ax1.pcolor(wav, positions, scats, cmap="coolwarm")  if if_plot else None
        ax1.plot(wav, maxz, "-", color="lightblue", label="Data - Focused Position") if if_plot else None

        step = 0.001
        for iSection in range(2):
            popt = popts[iSection]

            "拟合直线"
            x1 = fit_section[iSection][0]
            x2 = fit_section[iSection][1]
            label = f"{int(x1)}- {int(x2)} nm"
            x_for_fit, y_for_fit = choose_range(wav, maxz, x1=x1, x2=x2)
            fitted_curve = linear(x_for_fit, *popt)
            ax1.plot(x_for_fit, fitted_curve, "--", color=section_colors[iSection], linewidth=2, label=f"Fitted Line: {label}") if if_plot else None

            section_center = (x1 + x2) / 2
            content = f"Slope(um/nm): \n{popt[0]:.3f}"
            ax1.text(x=section_center, y=8.5, s=content, fontsize=15, ha='center', va='top', color=section_colors[iSection], weight='bold')  if if_plot else None

            "Tile中所有斜率的统计"
            ax2 = ax12 if iType == 0 else ax22

            bin_min = np.min(np.array(wav_maxz_fit_slopes[:, iSection]))  # 向下取整，保证包含最小值
            bin_max = np.max(np.array(wav_maxz_fit_slopes[:, iSection]))  # 向上取整，保证包含最大值
            bins = np.arange(bin_min, bin_max + step, step)

            label = f"{int(x1)}- {int(x2)} nm"
            counts, bins, patches = ax2.hist(x=wav_maxz_fit_slopes[:, iSection], bins=bins, color=section_colors[iSection], alpha=0.5, edgecolor='black', density=False, label=label)

        "重构误差"
        iters_error_popts_tile = np.array(iters_error_popts_tile)
        iters_error_fit_tau = iters_error_popts_tile[:, 1]
        median_tau_idx = argmedian(iters_error_fit_tau)

        iters_error = iters_errors_tile[median_tau_idx]
        popt = iters_error_popts_tile[median_tau_idx, :]
        fitted_curve = mono_exp(iters, *popt)

        ax23.plot(iters, iters_error, "o", linewidth=1, color=type_colors[iType], alpha=1,
                  label=f"Data: Before Correction" if iType == 0 else f"Data: After Correction")
        ax23.plot(iters, fitted_curve, "-", linewidth=1, color=type_colors[iType], alpha=1,
                  label=f"Fitted mono_exp: Before Correction" if iType == 0 else f"Fitted mono_exp: After Correction")

        ax23.axhspan(ymin=-escape_error, ymax=escape_error, color=escape_color, alpha=0.1)

        "统计重构速率(时间)"
        ax = ax14
        label = ("Before" if iType == 0 else "After") + " Correction"
        counts, bins, patches = ax.hist(x=iters_error_fit_tau, bins=error_bins,
                                         color=type_colors[iType], alpha=0.5, edgecolor='black',
                                         density=False, label=label)


        "统计时间"
        ax = ax24
        label = ("Before" if iType==0 else "After") + " Correction"
        counts, bins, patches = ax.hist(x=np.array(reconstruct_times), bins=recon_bins,
                                         color=type_colors[iType], alpha=0.5, edgecolor='black',
                                         density=False, label=label)

        ax.legend(loc="best")

    """Type结束"""
    "save fig"
    my_zstack_scats(ax11, title="Z-Axis Stacked Spectra", title_pad=30)
    my_zstack_scats(ax21, title="", title_pad=0)

    my_wav_maxz_fit_popt_stats(ax12, title="Fitted Slope Statistics", title_pad=30)
    my_wav_maxz_fit_popt_stats(ax22, title="", title_pad=0)

    my_reconstruct_scat(ax13, title="Recon. Scattering", title_pad=30)
    ax13.set_ylim([0, np.max(max_values_ax13)])
    my_reconstrution_process_error(ax23, title="Recon. Iteration Process")

    # my_thumb_image(ax14, title="Thumb Image")
    my_reconstrution_error_fit_popt_stats(ax14, title="Recon. Convergence Time Stats")
    my_wav_maxz_required_time_stats(ax24, title="Spectra Recon. Time Stats")
    save_path = os.path.join(os.path.dirname(filepath),
                              fr"Images2//p{iParticle}.png")
    fig.savefig(save_path)
    plt.close(fig)
    print(f"Particle: {iParticle}")
    # plt.show()
    # input()