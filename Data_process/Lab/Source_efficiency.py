import os.path
import h5py
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from sympy.physics.units import years

from src.general.figure import set_figure
from src.general import *
from src.general import *
from src.general import *

def the_figure1(ax):
    ax.legend()
    set_figure.set_legend(ax, legend_labels=None)
    set_figure.set_spines(ax)
    set_figure.set_label_and_title(ax, title='Souce Efficiency\n100X 0.9NA')
    ax.set_ylabel('Normalized Intensity(a.u.)')  # nor
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 1101, 200))

def the_figure2(ax):
    ax.legend()
    set_figure.set_legend(ax, legend_labels=None)
    set_figure.set_spines(ax)
    set_figure.set_label_and_title(ax, title='Souce Efficiency\n100X 0.8NA')
    ax.set_ylabel('Normalized Intensity(a.u.)')  # nor
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 1101, 200))

datapath1 = r"D:\ExpData\SouceEffect.h5"
save_fig = 1

"""fig0"""
fig1 = plt.figure(figsize=(8, 6))
ax1 = fig1.add_subplot(111)
fig2 = plt.figure(figsize=(8, 6))
ax2 = fig2.add_subplot(111)
with h5py.File(datapath1, "r") as f:
    data = f['OceanOpticsSpectrometer']
    bgd = np.array(data['100X_0.9NA_0'].attrs['background'])
    bgd_time = data['100X_0.9NA_0'].attrs['background_int'] / 1000
    wav = np.array(data['100X_0.9NA_0'].attrs['wavelengths'])
    bgd = bgd / bgd_time
    for key in data.keys():
        sp = data[key]
        sp_time = sp.attrs['integration_time'] / 1000
        sp = np.array(sp)
        sp = sp / sp_time
        sp = sp - bgd
        sp = sp / np.max(sp)  # nor
        power_now = key.split('_')[-1]
        if '0.9NA' in key:
            ax1.plot(wav, sp , label=power_now)
        if '0.8NA' in key:
            ax2.plot(wav, sp, label=power_now)


the_figure1(ax1)
fig1.tight_layout()

if save_fig == 1:
    # fig1.savefig(os.path.join(os.path.dirname(datapath1), f'source_efficiency_0.9NA.png'))
    fig1.savefig(os.path.join(os.path.dirname(datapath1), f'source_efficiency_0.9NA_normalized.png'))  #nor

the_figure2(ax2)
fig2.tight_layout()

if save_fig == 1:
    # fig2.savefig(os.path.join(os.path.dirname(datapath1), f'source_efficiency_0.8NA.png'))
    fig2.savefig(os.path.join(os.path.dirname(datapath1), f'source_efficiency_0.8NA_normalized.png'))  #nor
plt.show()