"""
Author: Junjie-Xie
Updated: 2025/7/21
Functions: 
"""
import numpy as np
import matplotlib.pyplot as plt
import h5py
from src.general.figure.draw_figure import *
from src.general.numerical.edit_data import *
from src.my_style.my_figure import *
from src.general.numerical.filter import *

filepath = r"D:\ExpData\SPE\20250722_SPE_hBN_SEM_array\measurement-3.h5"


def sort_by_middle_number(key, prefix, suffix):
    prefix_len = len(prefix)
    suffix_len = len(suffix)

    # 检查字符串长度是否足够同时去除前缀和后缀
    if len(key) < prefix_len + suffix_len:
        return float('inf')  # 长度不足的放最后

    # 去除前缀和后缀，获取中间部分
    middle_part = key[prefix_len: len(key) - suffix_len]

    # 尝试将中间部分转换为整数
    try:
        return int(middle_part)
    except ValueError:
        return float('inf')  # 无法转换为整数的放最后

with h5py.File(filepath, "r") as f:
    data = f[f'OceanOpticsSpectrometer']
    groups = []

    filter_groups = ["test_0", "laser power=50uW_0", "LampOn_bgd_0",
                     '450exPL_woExposed-scan_z_0',
                     "450exPL_p1-scan_z_0",  # 修正这里的分隔符
                     "450exPL_p1-scan_z_1",
                     "450exPL_p1-scan_z_2",
                     "450exPL_p1-scan_z_3",
                     "450exPL_p9-scan_z_0",
                     "450exPL_p9-scan_z_1"]

    for group in data.keys():

        if group in filter_groups:
            continue
        else:
            groups.append(group)

with h5py.File(filepath, "r") as f:
    for j, group in enumerate(groups):
        data = f[f'OceanOpticsSpectrometer/{group}']
        sps = []
        num = []
        keys = list(data.keys())

        sorted_keys = sorted(keys, key=lambda k: sort_by_middle_number(k, group[:-1], ""), reverse=False)
        print(sorted_keys)
        for i, key in enumerate(sorted_keys):
            if i == 0:
                continue

            sp = data[key]

            # 读取第一个子group下的第一个sp的bgd和wav，并对积分时间作归一化
            if sp.attrs.get("background") is not None:
                bgd = np.array(sp.attrs['background'])
                bgd_time = sp.attrs['background_int'] / 1000
                bgd = bgd / bgd_time
                last_bgd = bgd
            else:
                bgd = last_bgd
            wav = np.array(sp.attrs['wavelengths'])

            sp_time = sp.attrs['integration_time'] / 1000
            raw = np.array(sp)
            raw = raw / sp_time

            wav, bgd, raw = choose_range(wav, bgd, raw, x1=400, x2=1100)
            sp = raw - bgd
            # sp = sp / sp.max()

            if i == 1:
                sps = sp
            else:
                sps = np.vstack([sps, sp])
            num.append(i)

        # fig1 = plt.figure(figsize=(12, 8))
        # ax1 = fig1.add_subplot(1, 1, 1, projection='3d')
        # x = np.array(wav)
        # y = np.array(num)
        # Z = np.array(sps)
        # draw_cascade_3d(x, y, Z, ax=ax1, alpha=0.2, draw_polygon=True)
        # ax1.view_init(elev=0, azim=90)
        # ax1.set_title(group)

        if j == 0:
            fig21 = plt.figure(figsize=(12, 8))
            ax21 = fig21.add_subplot(1, 1, 1)

            fig22 = plt.figure(figsize=(12, 8))
            ax22 = fig22.add_subplot(1, 1, 1)

            fig23 = plt.figure(figsize=(12, 8))
            ax23 = fig23.add_subplot(1, 1, 1)

            fig24 = plt.figure(figsize=(12, 8))
            ax24 = fig24.add_subplot(1, 1, 1)
        else:
            sp_max = np.max(sps, axis=0)
            # idx = find_val_idx(x=wav, x0=538)
            # sp_max = sp_max / sp_max[idx]
            if "hBNwo" in group:
                ax22.plot(wav, sp_max, label=group)
            elif "Subw." in group:
                ax23.plot(wav, sp_max, label=group)
            elif "Subwo" in group:
                ax24.plot(wav, sp_max, label=group)
            else:
                ax21.plot(wav, sp_max, label=group)
        # sp_max_norm = sp_max / np.max(sp_max)
        # print(np.shape(wav), np.shape(sp_max_norm))
        # wav, sp_max_norm_filtered = remove_narrow_peaks(wav, sp_max_norm, max_fwhm=5.0)

# ax21.legend(loc=[1,0])
# ax22.legend(loc=[1,0])
# ax23.legend(loc=[1,0])
# ax24.legend(loc=[1,0])

ax21.legend()
ax22.legend()
ax23.legend()
ax24.legend()

# ax22.set_ylim(-10, 200)
# ax23.set_ylim(-10, 200)
# ax24.set_ylim(-10, 200)

# ax21.set_ylim(-1, 1.2)
# ax22.set_ylim(-1, 1.2)
# ax23.set_ylim(-1, 1.2)
# ax24.set_ylim(-1, 1.2)

plt.show()