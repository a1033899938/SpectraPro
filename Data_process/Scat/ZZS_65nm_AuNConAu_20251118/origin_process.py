import h5py
from scipy.optimize import curve_fit

from src.general.numerical.curve_functions import *
from src.general.numerical.edit_data import *
from figure_setting import *

filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_AuNC_70nm_20251117.h5"

"""处理"""
with h5py.File(filepath, "a") as f:
    parent_folder = f["OceanOpticsSpectrometer/20251117"]
    keys_1 = parent_folder.keys()
    sorted_keys_1 = sort_by_end_number(keys_1)

    step_length = None

    "拟合参数：z-int曲线"
    p00 = [0.08, 25, 12]
    bounds0 = [[0, 5, 5],
              [0.1, 45, 35]]

    "拟合参数：wav-maxz曲线"
    p01 = [0.06, -20]
    bounds1 = [[0.03, -30],
               [0.09, 10]]
    for i, key_1 in enumerate(sorted_keys_1):
        child_folder = parent_folder[f"{key_1}/Spectra"]
        step_length = child_folder.attrs["step length(um)"]

        keys_2 = child_folder.keys()
        sorted_keys_2 = sort_by_end_number(keys_2)

        scats = None
        max_positions = []
        for j, key_2 in enumerate(sorted_keys_2):
            print(f"正在处理: {key_1}/{key_2}")
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

            scats = scat if scats is None else np.vstack([scats, scat])

        # roi范围内的最大值
        idx1 = find_val_idx(wav, 600)
        idx2 = find_val_idx(wav, 1100)

        scats_of_roi = scats[:, idx1:idx2]
        max_idx = np.argmax(scats_of_roi)  # 扁平索引
        max_idx = np.unravel_index(max_idx, scats_of_roi.shape)  # 二维索引
        maxz_idx = max_idx[0]
        maxwav_idx = max_idx[1]

        # 取出最大值所在的光谱
        max_sp = scats[maxz_idx, :]
        max_z_int = scats[:, maxwav_idx]

        "拟合参数：z-int曲线"
        popts0 = None
        for iWav, wav0 in enumerate(wav):
            ints = scats[:, iWav]
            max_position_idx = np.argmax(ints)
            zs = np.arange(0, step_length*len(ints), step_length)
            max_positions.append(zs[max_position_idx])
            try:
                popt, pcov = curve_fit(gaussian, zs, ints, p0=p00, bounds=bounds0)
                fitted_curve = gaussian(zs, *popt)
                residuals = ints - fitted_curve
                rms_error = np.sqrt(np.mean(residuals ** 2))  # 均方根误差
                if not rms_error > np.max(ints) * 0.1:  # 例如超过最大强度的10%
                    popts0 = popt if popts0 is None else np.vstack([popts0, popt])
            except Exception as e:
                pass

        "拟合参数：wav-maxz曲线"
        popts1 = None
        try:
            x_for_fit, y_for_fit = choose_range(wav, np.array(max_positions), x1=550, x2=950)
            popt, pcov = curve_fit(linear, x_for_fit, y_for_fit, p0=p01, bounds=bounds1)
            popts1 = popt if popts1 is None else np.vstack([popts1, popt])
            fitted_curve = linear(np.arange(400, 1101, 1), *popt)
        except Exception as e:
            print(str(e))

        child_folder.attrs["Result_z-int"] = [zs, max_z_int]
        child_folder.attrs["Result_z-int_popts"] = popts0
        child_folder.attrs["Result_wav-maxz"] = [wav, max_positions]
        child_folder.attrs["Result_wav-maxz_popts"] = popts1