import matplotlib.pyplot as plt
import numpy as np
import os

from src.general import choose_range
from src.ui import read_file
from src.general.figure import set_figure


def the_figure(ax, le):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'Qdot_spin-coating', ylabel='Intensity(counts)')
    set_figure.set_spines(ax)
    # set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 901, 50))  # Normalized
    set_figure.set_legend(ax, legend_labels=le)
    plt.tight_layout()

def the_figure1(ax):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'2D PL Spectrum', ylabel='Strip')
    set_figure.set_spines(ax)
    # set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 901, 50))  # Normalized
    plt.tight_layout()

save_fig = 1
folder_path = r"E:\Data\ChenGroup\Qdot\20250331"
keys = ['Qdot_4000x_3000r_0CW.spe',
        'Qdot_4000x_3000r_650CW_532ex500uW.spe']
le = ['Qdot-upper', 'Qdot-middle']
extensions = ['.spe']
for i, key in enumerate(keys):
    data_path = os.path.join(folder_path, key)
    if i == 0:
        readFile = read_file(data_path, strip=[49, 58], show_data_flag=False)
        data = readFile.data
        x = data['wavelength']
        y = data['strip']
        z = data['intensity_image']
        x, z = choose_range(x, z, min_val=-20, max_val=20, axis=1)
        print(np.shape(z))
        fig0 = plt.figure(figsize=(8, 6))
        ax0 = fig0.add_subplot(111)
        ax0.pcolor(x, y, z)
    elif i == 1:
        readFile = read_file(data_path, strip=[85, 90], show_data_flag=False)
        data = readFile.data
        x = data['wavelength']
        y = data['intensity']
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.plot(x, y)

        x = data['wavelength']
        y = data['strip']
        z = data['intensity_image']
        # x, z = choose_range(x, z, min_val=-20, max_val=20, axis=1)
        fig1 = plt.figure(figsize=(8, 6))
        ax1 = fig1.add_subplot(111)
        ax1.pcolor(x, y, z)
        the_figure1(ax1)

        readFile = read_file(data_path, strip=[50, 55], show_data_flag=False)
        data = readFile.data
        x = data['wavelength']
        y = data['intensity']
        ax.plot(x, y)
        the_figure(ax, le)

if save_fig == 1:
    fig.savefig(fr"E:\Data\ChenGroup\Qdot\20250331\fig.png")
    fig0.savefig(fr"E:\Data\ChenGroup\Qdot\20250331\fig0.png")
    fig1.savefig(fr"E:\Data\ChenGroup\Qdot\20250331\fig1.png")

plt.show()