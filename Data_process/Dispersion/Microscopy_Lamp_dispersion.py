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

filepath = r"D:\ExpData\NP_scattering_Dispersion\Microscopy_Lamp_dispersion.h5"

group = "df_scan_z_0"
with h5py.File(filepath, "r") as f:
    data = f[f'OceanOpticsSpectrometer/{group}']
    sps = []
    num = []
    keys = list(data.keys())

    sorted_keys = sorted(keys, key=sort_by_number)
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

        if i == 1:
            sps = sp
        else:
            sps = np.vstack([sps, sp])
        num.append(i)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(1, 1, 1, projection='3d')
x = np.array(wav)
y = np.array(num)
Z = np.array(sps)
draw_cascade_3d(x, y, Z, ax=ax, alpha=0.2, draw_polygon=True)
ax.view_init(elev=20, azim=120)
ax.set_title(group)
plt.show()