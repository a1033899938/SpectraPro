import h5py
from src.general.figure import set_figure
import matplotlib.pyplot as plt
from src.general import *
from src.general import *

def the_figure(ax, fig, legend_labels_afterSEM):
    set_figure.set_label_and_title(ax, title='hBN-after-SEM-process\nPL spectra')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 901, 50))  # Normalized
    set_figure.set_legend(ax, legend_labels=legend_labels_afterSEM, font_size=8, location='upper right')
    ax.grid(True)
    fig.tight_layout()

datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-4\measurement-4.h5"
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

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
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

        x, y = choose_range(wav, sp, min_val=400, max_val=900)
        legend_labels_afterSEM.append(key)
        ax.plot(x, y)

the_figure(ax, fig, legend_labels_afterSEM)

if save_fig == 1:
    plt.savefig(r'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-2\\cascade&2d\\20250224_SPE_hBN_afterSEM_measurement2_Graph_increase_power.png')
plt.show()