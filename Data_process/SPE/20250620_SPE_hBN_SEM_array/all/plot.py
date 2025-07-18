import numpy as np
import h5py
import matplotlib.pyplot as plt

from src.general.figure import set_figure
from src.general import choose_range

def the_figure(ax):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'', ylabel='Intensity(counts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 901, 100))  # Normalized
    ax.legend()
    set_figure.set_legend(ax, legend_labels=None)
    plt.tight_layout()

datapath1 = r"D:\ExpData\SPE\20250620_SPE_hBN_SEM_array\m2_20250618_2sample+20250620_3sample.h5"
save_fig = 0

"""fig0"""
with h5py.File(datapath1, "r") as f:
    data = f['OceanOpticsSpectrometer']
    bgd = np.array(data['hBN-HQ-PDMS-1_0'].attrs['background'])
    bgd_time = data['hBN-HQ-PDMS-1_0'].attrs['background_int'] / 1000
    wav = np.array(data['hBN-HQ-PDMS-1_0'].attrs['wavelengths'])
    bgd = bgd / bgd_time

    fig1 = plt.figure(figsize=(8, 6))
    # fig2 = plt.figure(figsize=(8, 6))
    # fig3 = plt.figure(figsize=(8, 6))
    ax1 = fig1.add_subplot(111)
    # ax2 = fig2.add_subplot(111)
    # ax3 = fig3.add_subplot(111)

    hq_pdms = np.zeros(665)
    hq_tap = np.zeros(665)
    onway_pdms = np.zeros(665)
    for key in data.keys():
            sp = data[key]
            sp_time = sp.attrs['integration_time'] / 1000
            sp = np.array(sp)
            sp = sp / sp_time
            sp = sp - bgd
            sp = sp / np.max(sp)

            x, y = choose_range(wav, sp, min_val=400, max_val=900)
            if 'hBN-HQ-PDMS' in key:
                hq_pdms = hq_pdms + y
            elif 'hBN-Onway-PDMS' in key:
                onway_pdms = onway_pdms + y
            elif 'hBN-HQ-ScotchTap' in key:
                hq_tap = hq_tap + y
ax1.plot(x, hq_pdms/np.max(hq_pdms), label='hBN-HQ-PDMS')
ax1.plot(x, hq_tap/np.max(hq_tap), label='hBN-HQ-ScotchTap')
ax1.plot(x, onway_pdms/np.max(onway_pdms), label='hBN-Onway-PDMS')
the_figure(ax1)
# ax2.plot(x, y)
# the_figure(ax2)
# ax3.plot(x, y)
# the_figure(ax3)
plt.show()
            # if save_fig == 1:
            #     plt.savefig(os.path.join(os.path.dirname(datapath1), 'curve_fit', f'power_dependent_PL_curve_fit-{key}.png'))