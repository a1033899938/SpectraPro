"""
Author: Junjie-Xie
Updated: 2025/10/13
Functions: 
"""
import numpy as np
import matplotlib.pyplot as plt
import h5py
from src.general.figure.draw_figure import *
from src.general.numerical.edit_data import *
from src.my_style.my_figure import *
from src.my_style.my_color import *
from src.general.numerical.filter import *

filepath = r"D:\ExpData\SPE\20250224_HQ-PDMS\measurment-1_basic-PL.h5"

"""筛选光谱"""
with h5py.File(filepath, "r") as f:
    data = f[f'OceanOpticsSpectrometer']
    keys = []

    selected_keys = ['hBN_5keV_0.5min_0', "hBN_5keV_1min_0", "hBN_5keV_2min_0", "hBN_5keV_5min_0",
                     "hBN_10keV_0.5min_0", "hBN_10keV_1min_1", "hBN_10keV_2min_1", "hBN_10keV_5min_2",
                     "hBN_15keV_0.5min_0", "hBN_15keV_1min_0", "hBN_15keV_2min_0", "hBN_15keV_5min_0",
                     "hBN_5keV_0.5min_100KX_0", "hBN_5keV_1min_100KX_0", "hBN_5keV_2min_100KX_0", "hBN_5keV_5min_100KX_0",
                     "hBN_10keV_0.5min_100KX_0", "hBN_10keV_1min_100KX_1", "hBN_10keV_2min_100KX_0", "hBN_10keV_5min_100KX_0",
                     "hBN_15keV_0.5min_100KX_0", "hBN_15keV_1min_100KX_0", "hBN_15keV_2min_100KX_0", "hBN_15keV_5min_100KX_1",
                     "hBN_w.oSEM_0", "hBN_w.oSEM_1", "hBN_w.oSEM_2",
                     "sub_SiO2_0", "sub_SiO2_1", "sub_SiO2_2"
                     ]

    for key in data.keys():
        if key in selected_keys:
            keys.append(key)
        else:
            continue

with h5py.File(filepath, "r") as f:
    data = f[f'OceanOpticsSpectrometer']

    xs_woSEM = np.array([]).reshape(0, 0)  # 临时初始化为(0,0)，后续会动态调整
    ys_woSEM = np.array([]).reshape(0, 0)

    xs_sub = np.array([]).reshape(0, 0)
    ys_sub = np.array([]).reshape(0, 0)

    xs_SEM_5kV_100KX = np.array([]).reshape(0, 0)
    ys_SEM_5kV_100KX = np.array([]).reshape(0, 0)

    xs_SEM_5kV_50KX = np.array([]).reshape(0, 0)
    ys_SEM_5kV_50KX = np.array([]).reshape(0, 0)

    xs_SEM_10kV_100KX = np.array([]).reshape(0, 0)
    ys_SEM_10kV_100KX = np.array([]).reshape(0, 0)

    xs_SEM_10kV_50KX = np.array([]).reshape(0, 0)
    ys_SEM_10kV_50KX = np.array([]).reshape(0, 0)

    xs_SEM_15kV_100KX = np.array([]).reshape(0, 0)
    ys_SEM_15kV_100KX = np.array([]).reshape(0, 0)

    xs_SEM_15kV_50KX = np.array([]).reshape(0, 0)
    ys_SEM_15kV_50KX = np.array([]).reshape(0, 0)

    for i, key in enumerate(keys):
        raw = data[key]

        bgd = np.array(raw.attrs['background'])
        bgd_time = raw.attrs['background_int'] / 1000
        bgd = bgd / bgd_time

        wav = np.array(raw.attrs['wavelengths'])

        raw_time = raw.attrs['integration_time'] / 1000
        raw = np.array(raw)
        raw = raw / raw_time

        wav, bgd, raw = choose_range(wav, bgd, raw, x1=400, x2=1100)
        sp = raw - bgd
        # sp = sp / sp.max()

        # 然后修改vstack的逻辑（第一次赋值时动态调整维度）
        if "w.o" in key:
            # 将wav和sp转为二维行向量(1, n)
            wav_2d = wav.reshape(1, -1)
            sp_2d = sp.reshape(1, -1)

            if xs_woSEM.size == 0:
                # 第一次赋值：直接用当前数组初始化（确定维度）
                xs_woSEM = wav_2d
                ys_woSEM = sp_2d
            else:
                # 后续堆叠：确保维度匹配
                xs_woSEM = np.vstack((xs_woSEM, wav_2d))
                ys_woSEM = np.vstack((ys_woSEM, sp_2d))

        elif "sub" in key:
            wav_2d = wav.reshape(1, -1)
            sp_2d = sp.reshape(1, -1)

            if xs_sub.size == 0:
                xs_sub = wav_2d
                ys_sub = sp_2d
            else:
                xs_sub = np.vstack((xs_sub, wav_2d))
                ys_sub = np.vstack((ys_sub, sp_2d))

        elif key[4:8] == "5keV":
            wav_2d = wav.reshape(1, -1)
            sp_2d = sp.reshape(1, -1)

            if "100KX" in key:
                if xs_SEM_5kV_100KX.size == 0:
                    xs_SEM_5kV_100KX = wav_2d
                    ys_SEM_5kV_100KX = sp_2d
                else:
                    xs_SEM_5kV_100KX = np.vstack((xs_SEM_5kV_100KX, wav_2d))
                    ys_SEM_5kV_100KX = np.vstack((ys_SEM_5kV_100KX, sp_2d))
            else:
                if xs_SEM_5kV_50KX.size == 0:
                    xs_SEM_5kV_50KX = wav_2d
                    ys_SEM_5kV_50KX = sp_2d
                else:
                    xs_SEM_5kV_50KX = np.vstack((xs_SEM_5kV_50KX, wav_2d))
                    ys_SEM_5kV_50KX = np.vstack((ys_SEM_5kV_50KX, sp_2d))
        elif key[4:9] == "10keV":
            # 将wav和sp转为二维行向量(1, n)
            wav_2d = wav.reshape(1, -1)
            sp_2d = sp.reshape(1, -1)

            if "100KX" in key:
                if xs_SEM_10kV_100KX.size == 0:
                    # 第一次赋值：直接初始化
                    xs_SEM_10kV_100KX = wav_2d
                    ys_SEM_10kV_100KX = sp_2d
                else:
                    # 后续堆叠：vstack合并
                    xs_SEM_10kV_100KX = np.vstack((xs_SEM_10kV_100KX, wav_2d))
                    ys_SEM_10kV_100KX = np.vstack((ys_SEM_10kV_100KX, sp_2d))
            else:
                if xs_SEM_10kV_50KX.size == 0:
                    xs_SEM_10kV_50KX = wav_2d
                    ys_SEM_10kV_50KX = sp_2d
                else:
                    xs_SEM_10kV_50KX = np.vstack((xs_SEM_10kV_50KX, wav_2d))
                    ys_SEM_10kV_50KX = np.vstack((ys_SEM_10kV_50KX, sp_2d))

        elif key[4:9] == "15keV":
            # 将wav和sp转为二维行向量(1, n)
            wav_2d = wav.reshape(1, -1)
            sp_2d = sp.reshape(1, -1)

            if "100KX" in key:
                if xs_SEM_15kV_100KX.size == 0:
                    # 第一次赋值：直接初始化
                    xs_SEM_15kV_100KX = wav_2d
                    ys_SEM_15kV_100KX = sp_2d
                else:
                    # 后续堆叠：vstack合并
                    xs_SEM_15kV_100KX = np.vstack((xs_SEM_15kV_100KX, wav_2d))
                    ys_SEM_15kV_100KX = np.vstack((ys_SEM_15kV_100KX, sp_2d))
            else:
                if xs_SEM_15kV_50KX.size == 0:
                    xs_SEM_15kV_50KX = wav_2d
                    ys_SEM_15kV_50KX = sp_2d
                else:
                    xs_SEM_15kV_50KX = np.vstack((xs_SEM_15kV_50KX, wav_2d))
                    ys_SEM_15kV_50KX = np.vstack((ys_SEM_15kV_50KX, sp_2d))
        # sp_max_norm = sp_max / np.max(sp_max)
        # print(np.shape(wav), np.shape(sp_max_norm))
        # wav, sp_max_norm_filtered = remove_narrow_peaks(wav, sp_max_norm, max_fwhm=5.0)

xs_group = [xs_SEM_5kV_50KX, xs_SEM_10kV_50KX, xs_SEM_15kV_50KX, xs_SEM_5kV_100KX, xs_SEM_10kV_100KX, xs_SEM_15kV_100KX, xs_woSEM, xs_sub]
ys_group = [ys_SEM_5kV_50KX, ys_SEM_10kV_50KX, ys_SEM_15kV_50KX, ys_SEM_5kV_100KX, ys_SEM_10kV_100KX, ys_SEM_15kV_100KX, ys_woSEM, ys_sub]
time = ["0.5 min", "1 min", "2 min", "5 min"]
num = ["p0", "p1", "p2"]
color = MyColor.vibrant
les_group = [time, time, time, time, time, time, num, num]
les_sg = ["w. SEM 5kV 50KX", "w. SEM 10kV 50KX", "w. SEM 15kV 50KX", "w. SEM 5kV 100KX", "w. SEM 10kV 100KX", "w. SEM 15kV 100KX", "wo SEM", "sub"]
colors_group = [color, color, color, color, color, color, color, color]
fig, axes = draw_cascade_group_2d(xs_group, ys_group, les_group=les_group, les_sg=les_sg, colors_group=colors_group, dpi=500)
for ax in axes:
    ax.legend()
plt.show()