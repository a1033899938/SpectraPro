import h5py
from scipy.optimize import curve_fit
import os
from src.general.numerical.curve_functions import *
from src.general.numerical.edit_data import *
from src.general.figure.draw_figure import *
from figure_setting import *

filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_AuNC_70nm_20251117.h5"
"拟合参数：z-int曲线"
p00 = [0.08, 25, 12]
bounds0 = [[0, 5, 5],
          [1.1, 45, 35]]

"拟合参数：wav-maxz曲线"
p01 = [0.06, -20]
bounds1 = [[0.03, -30],
            [0.09, 10]]

"""作图"""
measures = ["20251117", "20251119"]
names = ["Origin", "Achromatic"]
figures = []
"拟合参数"
# fig1 = plt.figure(figsize=(12*2, 8), dpi=200)
# ax1 = fig1.add_subplot(121)
# ax2 = fig1.add_subplot(122)

fig2 = plt.figure(figsize=(12*2, 8), dpi=200)
ax3 = fig2.add_subplot(121)
ax4 = fig2.add_subplot(122)

fig3 = plt.figure(figsize=(12*2, 8), dpi=200)
ax5 = fig3.add_subplot(121)
ax6 = fig3.add_subplot(122)
popts0_group_origin = None
popts1_group_origin = None
popts0_group_ac = None
popts1_group_ac = None
with h5py.File(filepath, "r") as f:
    for iMeasure, measure in enumerate(measures):
        parent_folder = f[f"OceanOpticsSpectrometer/{measure}"]
        keys_1 = parent_folder.keys()
        sorted_keys_1 = sort_by_end_number(keys_1)

        for i, key_1 in enumerate(sorted_keys_1):
            # if (iMeasure == 0 and i == 10) or (iMeasure == 1 and i == 0):
            #     pass
            # else:
            #     continue
            child_folder = parent_folder[f"{key_1}/Spectra"]
            step_length = child_folder.attrs["step length(um)"]
            steps = child_folder.attrs["steps"]

            keys_2 = child_folder.keys()
            sorted_keys_2 = sort_by_end_number(keys_2)

            scats = None
            max_positions = []

            "光谱Map"
            # fig0 = plt.figure(figsize=(12, 8), dpi=200)
            # ax0 = fig0.add_subplot(111)
            # figures.append(fig0)



            max_z_int = child_folder.attrs["Result_z-int"]
            popts0 = child_folder.attrs["Result_z-int_popts"]
            max_positions = child_folder.attrs["Result_wav-maxz"]
            popts1 = child_folder.attrs["Result_wav-maxz_popts"]

            if iMeasure == 0:
                popts0_group_origin = popts0 if popts0_group_origin is None else np.vstack([popts0_group_origin, popts0])
                popts1_group_origin = popts1 if popts1_group_origin is None else np.vstack([popts1_group_origin, popts1])
            else:
                popts0_group_ac = popts0 if popts0_group_ac is None else np.vstack(
                    [popts0_group_ac, popts0])
                popts1_group_ac = popts1 if popts1_group_ac is None else np.vstack(
                    [popts1_group_ac, popts1])

            # x = max_z_int[0]
            # y = max_z_int[1]
            # y = (y - y.min()) / (y.max() - y.min())
            # popt, pcov = curve_fit(gaussian, x, y, p0=p00, bounds=bounds0)
            # y_fit = gaussian(x, *popt)

            # if iMeasure == 0:
            #     color = "blue"
            #     fit_color = "lightblue"
            # else:
            #     color = "red"
            #     fit_color = "lightcoral"

            # label = names[iMeasure]
            # ax1.plot(x, y, "o", color=color, markerfacecolor='none')
            # ax1.plot(x, y_fit, fit_color, label=label)
            #
            # x = max_positions[0]
            # y = max_positions[1]
            # popt = popts1
            # y_fit = linear(x, *popt)
            # ax2.plot(x, y, "o", color=color, markerfacecolor='none')
            # ax2.plot(x, y_fit, fit_color, label=label)
            #
            # single_axis_scan_result_var_pos(ax1, title="$z-I_{\lambda0}$")
            # single_axis_scan_result_var_wav(ax2, title="$\lambda$-$z_{max}$")


            # for j, key_2 in enumerate(sorted_keys_2):
            #     sp = child_folder[key_2]
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
            #     sp_time = sp.attrs['integration_time'] / 1000
            #     sp = np.array(sp)
            #     sp = sp / sp_time
            #
            #     numerator = sp - bgd  # 分子
            #     numerator[numerator == 0] = 1
            #
            #     denominator = ref - bgd  # 分母
            #     denominator[denominator == 0] = 1  # 如果分母为0，设为1
            #
            #     scat = numerator / denominator
            #
            #     "取出ROI范围内的光谱"
            #     wav, scat = choose_range(wav, scat, x1=450, x2=1000)
            #
            #     scats = scat if scats is None else np.vstack([scats, scat])

            # "光谱组Map图"
            # y_min = np.min(scats)
            # y_max = np.max(scats)
            #
            # diff = y_max - y_min
            # if diff == 0:
            #     diff = 1.0
            #
            # scats = (scats - y_min) / diff
            #
            # x = wav
            # y = np.arange(0, step_length*steps, step_length)
            # Z = scats
            # ax0.pcolor(x, y, Z, cmap="coolwarm")
            # single_axis_scan_map2d(ax0, title=f"{names[iMeasure]}-Scattering Map")
            #
            # current_dir = os.path.dirname(os.path.abspath(__file__))
            # target_dir = os.path.join(current_dir, "Image")
            #
            # if not os.path.exists(target_dir):
            #     os.makedirs(target_dir)

            # savepath = os.path.join(target_dir, f"{names[iMeasure]}_{key_1}_Scattering_Map.png")
            # plt.savefig(savepath, dpi=200, bbox_inches="tight")
            # plt.close()

    # print(np.shape(popts0_group_origin))
    # print(np.shape(popts1_group_origin))
    #
    # print(np.shape(popts0_group_ac))
    # print(np.shape(popts1_group_ac))

    FWFM_1 = np.array(popts0_group_origin[:, 2]) * 2.828
    Slope_1 = np.array(popts1_group_origin[:, 0])

    FWFM_2 = np.array(popts0_group_ac[:, 2]) * 2.828
    Slope_2 = np.array(popts1_group_ac[:, 0])

    counts, bins, patches = ax3.hist(x=FWFM_1, bins=30, color='blue', edgecolor='black', density=False)
    fitting_FWFM_hist(ax3, title="Origin")

    counts, bins, patches = ax4.hist(x=FWFM_2, bins=30, color='blue', edgecolor='black', density=False)
    fitting_FWFM_hist(ax4, title="Achromatic")

    counts, bins, patches = ax5.hist(x=Slope_1, bins=30, color='blue', edgecolor='black', density=False)
    fitting_slope_hist(ax5, title="Origin")

    counts, bins, patches = ax6.hist(x=Slope_2, bins=30, color='blue', edgecolor='black', density=False)
    fitting_slope_hist(ax6, title="Achromatic")

    print(f"Origin-slope: {np.median(Slope_1):.2f}")
    print(f"Ac-slope: {np.median(Slope_2):.2f}")
    print(f"Origin-slope: {np.median(FWFM_1):.2f}")
    print(f"Ac-slope: {np.median(FWFM_2):.2f}")

plt.show()