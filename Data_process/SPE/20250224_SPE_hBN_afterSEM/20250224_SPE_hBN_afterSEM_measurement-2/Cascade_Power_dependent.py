import h5py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

from src.general.figure.set_figure import *
from src.general.numerical.edit_data import *
from src.my_style.my_mapping_para import *
datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-2\measurement-2.h5"

"""fig0"""
with h5py.File(datapath1, "r") as f:
    data = f['OceanOpticsSpectrometer']
    keys_afterSEM = ['hBN_afterSEM_5kV_5min_expose10s_10uW__1',
                     'hBN_afterSEM_5kV_5min_expose10s_20uW__0',
                     'hBN_afterSEM_5kV_5min_expose10s_50uW__0',
                     'hBN_afterSEM_5kV_5min_expose10s_100uW__1',
                     'hBN_afterSEM_5kV_5min_expose10s_200uW__0',
                     'hBN_afterSEM_5kV_5min_expose10s_500uW__0',
                     'hBN_afterSEM_5kV_5min_expose10s_1000uW__0',
                     'hBN_afterSEM_5kV_5min_expose10s_2000uW__1',
                     'hBN_afterSEM_5kV_5min_expose10s_3000uW__0']
                     # 'hBN_afterSEM_5kV_5min_expose10s_2000uW_back_2',
                     # 'hBN_afterSEM_5kV_5min_expose10s_1000uW_back_0',
                     # 'hBN_afterSEM_5kV_5min_expose10s_500uW_back_0',
                     # 'hBN_afterSEM_5kV_5min_expose10s_200uW_back_2_0',
                     # 'hBN_afterSEM_5kV_5min_expose10s_100uW_back_3',
                     # 'hBN_afterSEM_5kV_5min_expose10s_50uW_back_1',
                     # 'hBN_afterSEM_5kV_5min_expose10s_20uW_back_0',
                     # 'hBN_afterSEM_5kV_5min_expose10s_10uW_back_1']
    les = ['10', '20', '50', '100', '200', '500', '1000', '2000', '3000']
    les = [le+'uw' for le in les]

    sps = []
    for i, key in enumerate(keys_afterSEM):
        sp = data[key]
        bgd = np.array(sp.attrs['background'])
        wav = np.array(sp.attrs['wavelengths'])
        sp_time = sp.attrs['integration_time'] / 1000
        bgd_time = sp.attrs['background_int'] / 1000
        sp = sp / sp_time
        bgd = bgd / bgd_time
        sp = np.array(sp) - bgd
        wav, sp = choose_range(wav, sp, x1=400, x2=900)
        sps.append(sp)

sps = np.array(sps)
fig, axes = cascade_2d(x=wav, ys=sps, les=les)
nsubplots = len(les)

for i, ax in enumerate(axes):
    set_tick(ax, linewidth=1, ybins=4, fontsize=10, show_ylabel_every_ticks=2)
    if i == nsubplots // 2:
        set_label_and_title(axes[i], title='', xlabel='', ylabel='Intensity(cts)', ylabel_ha='center', ylabel_va='center', ylabel_rotation=(-0.15, 0.9))

title = f'hBN w/ EBI'
set_label_and_title(axes[0], title=title, xlabel='', ylabel='', title_pad=30)
set_label_and_title(axes[-1], title='', ylabel='', x_label_pad=20)
set_tick(axes[-1], ticks_xlabel=np.arange(400, 901, 100), linewidth=1, ybins=4, fontsize=10, show_ylabel_every_ticks=2)
plt.subplots_adjust(left=0.15)
plt.tight_layout()

"""fig1"""
with h5py.File(datapath1, "r") as f:
    data = f['OceanOpticsSpectrometer']
    keys_withoutSEM = ['hBN_withoutSEM_5kV_5min_expose10s_10uW_0',
                       'hBN_withoutSEM_5kV_5min_expose10s_20uW_0',
                       'hBN_withoutSEM_5kV_5min_expose10s_50uW_0',
                       'hBN_withoutSEM_5kV_5min_expose10s_100uW_0',
                       'hBN_withoutSEM_5kV_5min_expose10s_200uW_2',
                       'hBN_withoutSEM_5kV_5min_expose10s_500uW_1',
                       'hBN_withoutSEM_5kV_5min_expose10s_100uW_2',
                       'hBN_withoutSEM_5kV_5min_expose10s_2000uW_0',
                       'hBN_withoutSEM_5kV_5min_expose10s_3000uW_0']
    les = ['10', '20', '50', '100', '200', '500', '1000', '2000', '3000']
    les = [le+'uw' for le in les]

    sps = []
    for i, key in enumerate(keys_withoutSEM):
        sp = data[key]
        bgd = np.array(sp.attrs['background'])
        wav = np.array(sp.attrs['wavelengths'])
        sp_time = sp.attrs['integration_time'] / 1000
        bgd_time = sp.attrs['background_int'] / 1000
        sp = sp / sp_time
        bgd = bgd / bgd_time
        sp = np.array(sp) - bgd
        wav, sp = choose_range(wav, sp, x1=400, x2=900)
        sps.append(sp)

sps = np.array(sps)
fig, axes = cascade_2d(x=wav, ys=sps, les=les)
nsubplots = len(les)

for i, ax in enumerate(axes):
    set_tick(ax, linewidth=1, ybins=4, fontsize=10, show_ylabel_every_ticks=2)
    if i == nsubplots // 2:
        set_label_and_title(axes[i], title='', xlabel='', ylabel='Intensity(cts)', ylabel_ha='center', ylabel_va='center', ylabel_rotation=(-0.15, 0.9))

title = f'hBN w/o EBI'
set_label_and_title(axes[0], title=title, xlabel='', ylabel='', title_pad=30)
set_label_and_title(axes[-1], title='', ylabel='', x_label_pad=20)
set_tick(axes[-1], ticks_xlabel=np.arange(400, 901, 100), linewidth=1, ybins=4, fontsize=10, show_ylabel_every_ticks=2)
plt.subplots_adjust(left=0.15)
plt.tight_layout()

plt.show()