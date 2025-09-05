import matplotlib.pyplot as plt
import os

from src.ui import read_file
from src.general.figure import set_figure


def the_figure(ax, le):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=le, ylabel='Intensity(counts)')
    set_figure.set_spines(ax)
    # set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 901, 50))  # Normalized
    # set_figure.set_legend(ax, legend_labels=le)
    plt.tight_layout()

def the_figure1(ax):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'2D PL Spectrum', ylabel='Strip')
    set_figure.set_spines(ax)
    # set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 901, 50))  # Normalized
    plt.tight_layout()

save_fig = 1
folder_path = r"E:\Data\ChenGroup\SPE\20250410"
keys = ['hBN_afterSEM_5kV_1min 039.spe',
        'hBN_afterSEM_5kV_1min 041.spe',
        'hBN_afterSEM_5kV_1min 040.spe']
le = ['430 LP', '550 LP', '532 Raman LP + 550 SP']
extensions = ['.spe']
for i, key in enumerate(keys):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    data_path = os.path.join(folder_path, key)
    readFile = read_file(data_path, strip=[43, 48], show_data_flag=False)
    data = readFile.data0
    x = data['wavelength']
    y = data['intensity']
    ax.plot(x, y)
    the_figure(ax, le[i])
        # fig = plt.figure(figsize=(8, 6))
        # ax = fig.add_subplot(111)
        # ax.plot(x, y)
        #
        # x = data['wavelength']
        # y = data['strip']
        # z = data['intensity_image']
        # # x, z = choose_range(x, z, min_val=-20, max_val=20, axis=1)
        # fig1 = plt.figure(figsize=(8, 6))
        # ax1 = fig1.add_subplot(111)
        # ax1.pcolor(x, y, z)
        # the_figure1(ax1)
        #
        # readFile = read_file(data_path, strip=[58, 63], show_data_flag=False)
        # data = readFile.data
        # x = data['wavelength']
        # y = data['intensity']
        # ax.plot(x, y)
        # the_figure(ax, le)

    if save_fig == 1:
        fig.savefig(fr"E:\Data\ChenGroup\SPE\20250410\fig{i}.png")


plt.show()