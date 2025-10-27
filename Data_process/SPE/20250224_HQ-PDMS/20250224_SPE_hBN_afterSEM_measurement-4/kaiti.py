import os.path
import h5py
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from src.general import *
from src.general import *
from src.general.figure import set_figure


def the_figure(ax):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'', ylabel='Frequency')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_ylabel=np.arange(0, 7, 1))  # Normalized
    set_figure.set_scientific_y_ticks(ax, sci_fontsize=20)
    plt.tight_layout()

filepath = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-4\wavlength_fit.npy"

wavelength_fit = np.load(filepath)
wavelength_fit = np.array(wavelength_fit).flatten().tolist()

fig0 = plt.figure(figsize=(8, 6))
ax0 = fig0.add_subplot(111)

ax0.hist(
    wavelength_fit,               # 数据
    bins=10,              # 区间数量
    density=False,        # 是否显示频率（False为频数）
    color='purple',      # 颜色
    edgecolor='navy',     # 边框颜色
    alpha=0.7,            # 透明度
    zorder=2              # 图层顺序，避免边框被覆盖
)
the_figure(ax0)

plt.show()
