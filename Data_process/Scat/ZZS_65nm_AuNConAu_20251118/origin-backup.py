import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from src.general.numerical.curve_functions import *
from src.general.numerical.edit_data import *
from figure_setting import *

filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_AuNC_70nm_20251117.h5"

with h5py.File(filepath, "r") as f:
    parent_folder = f["OceanOpticsSpectrometer/20251117"]
    keys_1 = parent_folder.keys()
    sorted_keys_1 = sort_by_end_number(keys_1)
    # fig0 = plt.figure(figsize=(12*3, 8), dpi=100)
    # ax01 = fig0.add_subplot(131)
    # ax02 = fig0.add_subplot(132)
    # ax03 = fig0.add_subplot(133)
    # figures1 = []
    popts0 = None
    popts1 = None
    step_length = None
    p00 = [0.08, 25, 12]
    bounds0 = [[0, 5, 5],
              [0.1, 45, 35]]
    p01 = [0.06, -20]
    bounds1 = [[0.03, -30],
               [0.09, 10]]
    for i, key_1 in enumerate(sorted_keys_1):
        child_folder = parent_folder[f"{key_1}/Spectra"]
        step_length = child_folder.attrs["step length(um)"]

        keys_2 = child_folder.keys()
        sorted_keys_2 = sort_by_end_number(keys_2)

        # fig1= plt.figure(figsize=(12*2,8), dpi=100)
        # figures1.append(fig1)
        # ax11 = fig1.add_subplot(121)
        # ax12 = fig1.add_subplot(122)
        scats = None
        max_positions = []
        for j, key_2 in enumerate(sorted_keys_2):
            sp = child_folder[key_2]

            wav = np.array(sp.attrs['wavelengths'])

            bgd = np.array(sp.attrs['background'])
            bgd_time = sp.attrs['background_int'] / 1000
            bgd = bgd / bgd_time

            ref = np.array(sp.attrs['reference'])
            ref_time = sp.attrs['reference_int'] / 1000
            ref = ref / ref_time

            sp_time = sp.attrs['integration_time'] / 1000
            sp = np.array(sp)
            sp = sp / sp_time

            numerator = sp - bgd  # 分子
            numerator[numerator == 0] = 1

            denominator = ref - bgd  # 分母
            denominator[denominator == 0] = 1  # 如果分母为0，设为1

            scat = numerator / denominator

            # ax11.plot(wav, scat)

            scats = scat if scats is None else np.vstack([scats, scat])

        # single_axis_scan_graph(ax11, title=key_1)

        # idx1 = find_val_idx(wav, 600)
        # idx2 = find_val_idx(wav, 1100)
        #
        # scats_of_roi = scats[:, idx1:idx2]
        # y_min = np.min(scats_of_roi)
        # y_max = np.max(scats_of_roi)
        #
        # diff = y_max - y_min
        # y_max = y_max + diff / 10
        # y_min = y_min - diff / 10

        # ax11.set_ylim([y_min, y_max])

        for k, wav0 in wav:
            # wav_idx = find_val_idx(wav, wav0)
            ints = scats[:, k]
            max_position_idx = np.argmax(ints)
            pos = np.arange(0, step_length*len(ints), step_length)
            max_positions.append(pos[max_position_idx])
            # ax01.plot(pos, ints) # 呈高斯分布，与光子态密度分布一致
            try:
                popt, pcov = curve_fit(gaussian, pos, ints, p0=p00, bounds=bounds0)
                fitted_curve = gaussian(pos, *popt)
                residuals = ints - fitted_curve
                rms_error = np.sqrt(np.mean(residuals ** 2))  # 均方根误差
                if not rms_error > np.max(ints) * 0.1:  # 例如超过最大强度的10%
                    popts0 = popt if popts0 is None else np.vstack([popts0, popt])
                    # ax01.plot(pos, fitted_curve, "--", color="black")
            except Exception as e:
                pass

        child_folder.attrs["Result_wav-maxz"] = max_positions
        child_folder.attrs["Result_wav-maxz"] = max_positions
        # ax12.plot(np.arange(400, 1101, 1), max_positions) # 呈线性，与色散-波长关系一致
        try:
            x_for_fit, y_for_fit = choose_range(np.arange(400, 1101, 1), np.array(max_positions), x1=560, x2=960)
            popt, pcov = curve_fit(linear, x_for_fit, y_for_fit, p0=p01, bounds=bounds1)
            popts1 = popt if popts1 is None else np.vstack([popts1, popt])
            fitted_curve = linear(np.arange(400, 1101, 1), *popt)
            # ax12.plot(np.arange(400, 1101, 1), fitted_curve, "--", color="black")
        except Exception as e:
            print(str(e))
        single_axis_scan_result_var_wav(ax12)

    single_axis_scan_result_var_pos(ax01)
    FWFM = np.array(popts0[:, 2])*2.828
    counts, bins, patches =  ax02.hist(x=FWFM, bins=30, color='blue', edgecolor='black', density=False)
    fitting_FWFM_hist(ax02)
    print(f"Origin-FWFM: min={np.min(FWFM):.2f}, max={np.max(FWFM):.2f}, median={np.median(FWFM):.2f}, mean={np.mean(FWFM):.2f} um")

    slope = popts1[:, 0]
    counts, bins, patches =  ax03.hist(x=slope, bins=30, color='blue', edgecolor='black', density=False)
    fitting_slope_hist(ax03)
    ax03.set_yticks(np.unique(counts))
    print(f"Origin-slope: min={np.min(slope):.2f}, max={np.max(slope):.2f}, median={np.median(slope):.2f}, mean={np.mean(slope):.2f} um/nm")

    fig0.suptitle("Origin", fontweight="bold", fontsize=35, y=0.98)
    fig0.tight_layout(rect=[0, 0, 1, 0.97])

    for fig in figures1:
        fig.suptitle("Origin", fontweight="bold", fontsize=35, y=0.98)
        fig.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()




