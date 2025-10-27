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

filepath = r"C:\Users\a1033\Desktop\Edge Download\measurement-2.h5"


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
    for group in data.keys():
        if group == "all_spectra_above_excitation=450CW_50uW_0":
            continue
        else:
            groups.append(group)

print(groups)
# group = "hBN_w._exposure_1$_7-5_scan_z_0"
with h5py.File(filepath, "r") as f:
    for group in groups:
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
            bgd = np.array(sp.attrs['background'])
            bgd_time = sp.attrs['background_int'] / 1000
            bgd = bgd / bgd_time
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
        # ax.set_zlim(-15, 30)
        # ax.set_zlim(-1, 1)

        fig2 = plt.figure(figsize=(12, 8))
        ax2 = fig2.add_subplot(1, 1, 1)
        sp_max = np.max(sps, axis=0)
        ax2.plot(wav, sp_max, color='r')
plt.show()