from src.general.proc.ProcTrack import *
from Data_process.Scat.ZZS_65nm_AuNConAu_20260108.figure_setting import *

filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_65nm_AuNConSi_circle_20251210\ZZS_65nm_AuNConSi_20251210.h5"
process_types = ["before_achro", "after_achro"]
roots = ["OceanOpticsSpectrometer/20251210/sample1_before_achro_circle",
         "OceanOpticsSpectrometer/20251210/sample1_circle_1"]

p0_linear = [0.1, -10]
bounds_linear = [[0, -50],
                 [0.2, 0]]

fig2 = plt.figure(figsize=(12*2, 8), dpi=100)
ax5 = fig2.add_subplot(121)
ax6 = fig2.add_subplot(122)
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

for iType, (process_type, root) in enumerate(zip(process_types, roots)):
    PROC = ProcTrack(filepath, root)

    tile_keys, full_tile_keys = PROC.get_tile_keys(mask=["Tile_10"])

    for iTile, full_tile_key in enumerate(full_tile_keys):
        particle_keys, full_particle_keys = PROC.get_particle_keys(full_tile_key)

        for iParticle, full_particle_key in enumerate(full_particle_keys):
            print(iType, iTile, iParticle)
            "跳过"
            if iTile >= 10:
                continue

            """删除unvalid的图片"""
            is_valid = PROC.get_attrs(full_particle_key, f"JunProc: is_valid")
            from pathlib import Path
            if not is_valid:
                save_path = Path(os.path.join(os.path.dirname(filepath), fr"Image/Reconstuct_scat & stacked_scats/{process_type}_p{iParticle}_t{iTile}.png"))
                if save_path.exists() and save_path.is_file():
                    print(iType, iTile, iParticle)
                    save_path.unlink()

            # """处理图片"""
            # fig = plt.figure(figsize=(12 * 2, 8 * 2), dpi=100)
            # ax1 = fig.add_subplot(221)
            # ax2 = fig.add_subplot(222)
            # ax3 = fig.add_subplot(223)
            # ax4 = fig.add_subplot(224)
            # ax4_inset = ax4.inset_axes([0.7, 0.7, 0.25, 0.25])
            #
            # "Image"
            # image_key, full_image_key = PROC.get_image_key(full_particle_key, 0)
            #
            # # SAVE
            # img, img_gray = PROC.proc_thumb_image(full_image_key, None)  # full_particle_key
            # ax4.imshow(img)  ####################
            # ax4_inset.imshow(img_gray)  ####################
            #
            # "Spectra"
            # # 2d
            # spectra_key, full_spectra_key = PROC.get_spectra_key(full_particle_key, "scan_z")
            # wav, positions, scats, times = PROC.get_scanning(full_spectra_key, [450, 900], "scat")
            #
            # ax2.pcolor(wav, positions, scats, cmap="coolwarm")  ####################
            #
            # "reconstruct"
            # step_length = PROC.get_attrs(full_spectra_key, "step length(um)")
            # jump_steps = np.array(list(range(2, 12, 1))+[21])
            # steps_length = jump_steps * step_length
            #
            # # SAVE
            # reconstruct_error, jump_step_reconstruct_scats = PROC.proc_reconstruct_error(scats, jump_steps=jump_steps, save_path_key=full_particle_key, wav=wav)  # full_particle_key
            # reconstruct_scat = np.max(scats, axis=0)
            #
            # ax1.plot(wav, reconstruct_scat, "-", color="red", label="Reconstructed Scat Step(um): 0.5")  ####################
            # for iJumpStep, jump_step_reconstruct_scat in enumerate(jump_step_reconstruct_scats):
            #     ax1.plot(wav, jump_step_reconstruct_scat, "-", label=f"Reconstructed Scat Step(um): {steps_length[iJumpStep]}")  ####################
            #
            # """maxz"""
            # "maxz"
            # maxz = PROC.proc_maxz(wav, positions, scats)
            # ax2.plot(wav, maxz, "-", color="lightblue", label="Max Z")  ####################
            #
            # fit_section = [[500, 656.3], [656.3, 730]]
            # popts = []
            # reconstruct_required_ranges = []
            # for iSection, section in enumerate(fit_section):
            #     x1 = fit_section[iSection][0]
            #     x2 = fit_section[iSection][1]
            #     x_for_fit, y_for_fit = choose_range(wav, maxz, x1=x1, x2=x2)
            #     popt, pcov = curve_fit(linear, x_for_fit, y_for_fit, p0=p0_linear, bounds=bounds_linear)
            #     fitted_curve = linear(x_for_fit, *popt)
            #     ax2.plot(x_for_fit, fitted_curve, "--", color="black")  ####################
            #     ax2.plot(x_for_fit, y_for_fit, "-", color="blue" if iSection == 0 else "red")  ####################
            #
            #     popts.append(list(popt))
            #     reconstruct_required_ranges.append([fitted_curve[0], fitted_curve[-1]])
            #
            # # SAVE
            # PROC.set_attrs(full_particle_key, "wav-maxz fit function", "linear")
            # PROC.set_attrs(full_particle_key, "wav-maxz fit popts", popts)
            # PROC.set_attrs(full_particle_key, "wav-maxz fit section", fit_section)
            #
            # "required time"
            # total_seconds = []
            # norm_total_seconds = []
            # for iSection, (section, reconstruct_required_range) in enumerate(zip(fit_section, reconstruct_required_ranges)):
            #     position1_idx = find_val_idx(positions, reconstruct_required_range[0])
            #     position2_idx = find_val_idx(positions, reconstruct_required_range[1])
            #
            #     time1 = times[position1_idx]
            #     time2 = times[position2_idx]
            #
            #     time_diff = time2 - time1
            #     total_second = time_diff.total_seconds()
            #     ratio1 = (len(times) + 1) / (len(times))
            #     total_second *= ratio1
            #     norm_total_second = total_second / (section[-1] - section[0])
            #
            #     total_seconds.append(total_second)
            #     norm_total_seconds.append(norm_total_second)
            #
            # PROC.set_attrs(full_particle_key, "wav-maxz total_second(s)", total_seconds)
            # PROC.set_attrs(full_particle_key, "wav-maxz norm. total_second(s/nm)", norm_total_seconds)
            #
            # "ints_at_wav0"
            # wavs = [500, 587.6, 656.3, 730]
            # colors = ["blue", "green", "orange", "red"]
            #
            # popts = []
            # fit_valid_wavs = []
            # for wav0, color in zip(wavs, colors):
            #     ints_at_wav0 = PROC.proc_int_at_wav0(wav0, wav, scats)
            #     ax2.axvline(x=wav0, color=color, linestyle="--", linewidth=2)  ####################
            #     ax3.plot(positions, ints_at_wav0, "-", color=color, label=f"data - {wav0:.1f} nm")  ####################
            #
            #     "fit"
            #
            #     try:
            #         A0 = np.max(ints_at_wav0)
            #         x0 = positions[np.argmax(ints_at_wav0)]
            #         sigma0 = 20
            #         p0 = [A0, x0, sigma0]
            #         popt, pcov = curve_fit(gaussian, positions, ints_at_wav0, p0=p0)
            #
            #         fitted_curve = gaussian(positions, *popt)
            #
            #         text_content = [f"A: {popt[0]:.2e}", f"z0: {popt[1]:.1f}", f"sigma: {popt[2]:.1f}"]
            #         text_content = " ".join(text_content)
            #         text_content = f" - {text_content}"
            #
            #         ax3.plot(positions, fitted_curve, '--', color=color, label=f"gaussian fit - {wav0:.1f} nm{text_content}")  ####################
            #
            #         popts.append(list(popt))
            #         fit_valid_wavs.append(wav0)
            #     except:
            #         popt = [None, None, None]
            #
            # #SAVE
            # if popts is not None:
            #     PROC.set_attrs(full_particle_key, "ints_at_wav0 wavs", wavs)
            #     PROC.set_attrs(full_particle_key, "ints_at_wav0 fit valid wavs", fit_valid_wavs)
            #     PROC.set_attrs(full_particle_key, "ints_at_wav0 fit popts", popts)
            #
            # "save fig"
            # fig.suptitle(f"{process_type.title()}_p{iParticle}_t{iTile}", color="#333333", fontsize=40, fontweight="bold", family="Times New Roman")
            # my_reconstruct_scat(ax1, title="Reconstructed Spectrum")
            # my_zstack_scats(ax2, title="Z-Axis Stacked Spectra")
            # my_maxint_ints(ax3, title="z-int at Target Wavelength")
            # my_thumb_image(ax4, title="Thumb Image")
            # save_path = os.path.join(os.path.dirname(filepath),
            #                          fr"Image/Reconstuct_scat & stacked_scats/{process_type}_p{iParticle}_t{iTile}.png")
            # fig.savefig(save_path)
            # # plt.show()
            # # input()
            # plt.close(fig)