import h5py
from shutil import copyfile
import pySPM
import matplotlib.pyplot as plt
import pprint
from src.general import set_figure
from scipy.optimize import curve_fit
import re
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def gaussian(x, A, mu, sigma):
    return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))


def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
    return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))


import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-4\20250224_SPE_hBN_afterSEM_measurement-4.h5"
save_fig = 0

"""fig0"""
with h5py.File(datapath1, "r") as f:
    data = f['OceanOpticsSpectrometer']
    # keys_afterSEM = []
    # keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_10uW__1')
    # keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_20uW__0')
    # keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_50uW__0')
    # keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_100uW__1')
    # keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_200uW__0')
    # keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_500uW__0')
    # keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_1000uW__0')
    # keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_2000uW__1')
    # keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_3000uW__0')
    # legend_labels_afterSEM = ['10uW', '20uW', '50uW', '100uW', '200uW', '500uW', '1000uW', '2000uW', '3000uW']

    fig0 = plt.figure(figsize=(8, 6))
    ax0 = fig0.add_subplot(111)
    legend_labels_afterSEM = []
    for key in data.keys():
        sp = data[key]
        bgd = np.array(sp.attrs['background'])
        wav = np.array(sp.attrs['wavelengths'])
        sp_time = sp.attrs['integration_time'] / 1000
        bgd_time = sp.attrs['background_int'] / 1000
        sp = sp / sp_time
        bgd = bgd / bgd_time
        sp = np.array(sp) - bgd

        min_differences = np.abs(wav - 400)
        min_index = np.argmin(min_differences)
        max_differences = np.abs(wav - 900)
        max_index = np.argmin(max_differences)

        x = wav[min_index:max_index]
        y = sp[min_index:max_index]

        legend_labels_afterSEM.append(key)
        ax0.plot(x, y)

set_figure.set_label_and_title(ax0, title = 'hBN-after-SEM-process\nPL spectra')
set_figure.set_spines(ax0)
set_figure.set_tick(ax0, xbins=16, ybins=10, fontsize=10, fontweight='bold',
                    linewidth=3, tick_pad=5, direction='in',
                    ticks_xlabel=np.arange(400, 901, 50))  # Normalized
set_figure.set_legend(ax0, legend_labels=legend_labels_afterSEM, font_size=8, location='upper right')
ax0.grid(True)
plt.tight_layout()
if save_fig == 1:
    from src.general.save_figure import save_subfig
    plt.savefig(r'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-2\\cascade&2d\\20250224_SPE_hBN_afterSEM_measurement2_Graph_increase_power.png')
plt.show()