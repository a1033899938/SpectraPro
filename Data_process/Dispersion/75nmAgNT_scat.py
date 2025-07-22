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

filepath = r"D:\ExpData\NP_scattering_Dispersion\75nmAgNT_measurement-1.h5"

with h5py.File(filepath, "r") as f:
    data = f['OceanOpticsSpectrometer']
    group_name = ["75nmAgNT_scat_0",
                  "75nmAgNT-2_scat_0",
                  "75nmAgNT-3_scat_0"]

    group = data[group_name[0]]
    group_keys = group.keys()
    scats = []
    for i, key in enumerate(group_keys):
        sp = group[key]

        # 读取第一个子group下的第一个sp的bgd和wav，并对积分时间作归一化
        bgd = np.array(sp.attrs['background'])
        bgd_time = sp.attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        ref = np.array(sp.attrs['reference'])
        ref_time = sp.attrs['reference_int'] / 1000
        ref = ref / ref_time
        wav = np.array(sp.attrs['wavelengths'])

        sp_time = sp.attrs['integration_time'] / 1000
        raw = np.array(sp)
        raw = raw / sp_time

        wav, bgd, ref, raw = choose_range(wav, bgd, ref, raw, x1=400, x2=900)
        scat = (raw - bgd) / (ref - bgd)

        # 去除尖峰
        spike_indices = detect_spikes_savgol(scat, threshold=1.5)
        scat = remove_spikes(scat, spike_indices, window_size=10, method='median')

        scats.append(scat)

scats = np.array(scats)
# 对最后一条看不见散射峰的曲线进行多项式拟合
coefficients = np.polyfit(wav, scats[-1, :], 5)  # 返回系数 [a, b, c, d]
fitted_polynomial = np.poly1d(coefficients)
base_line = fitted_polynomial(wav)

def my_curve(x, A, x0, sigma, a, b, c, d, e, f):
    # 高斯部分
    gaussian_part = gaussian(x, A, x0, sigma)

    # 五阶多项式部分
    poly_part = a + b * x ** 1 + c * x ** 2 + d * x ** 3 + e * x ** 4 + f * x ** 5

    return gaussian_part + poly_part

p0 = [0.0008, 600, 100] + coefficients.tolist()
As = []
xs = []
ps = []
for i in range(scats.shape[0]):
    try:
        print(f"iteration: {i} in {scats.shape[0]}")
        x = wav
        y = scats[i, :]
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        ax.plot(x, y, 'b-')

        popt, pcov = curve_fit(my_curve, x, y, p0=p0)
        A, x0, gamma, a, b, c, d, e, f = popt
        ax.plot(x, my_curve(x, *popt), 'r--')
        As.append(A)
        xs.append(x0)
        ps.append(i)
    except:
        pass

fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.plot(ps, As)
ax2.plot(ps, xs)


# 时间序列图
# fig = plt.figure(figsize=(12, 8), dpi=100)
# ax = fig.add_subplot(111, projection='3d')
# draw_cascade_3d(x=wav, y=range(np.shape(scats)[0]), Z=scats, ax=ax)
# # ax.set_zlim([-0.0001, 0.00344])
# # ax.set_zlim([-0.0001, 0.00101])
# ax.set_zlim([-0.0001, 0.00095])
# ax.view_init(elev=20, azim=0)
# # the_cascade(ax)
plt.show()