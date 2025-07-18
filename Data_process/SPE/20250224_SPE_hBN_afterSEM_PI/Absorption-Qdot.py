import matplotlib.pyplot as plt
import os

from src.general.load_data import read_file
from src.general.figure import set_figure


def the_figure(ax, le):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'Qdot-PL', ylabel='Intensity(counts)')
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
folder_path = r"E:\Data\ChenGroup\Qdot\20250410"
keys = ['qdot_532ex_20uW 021.spe',
        'qdot_white 029.spe',
        'sio2_white 034.spe']

extensions = ['.spe']
for i, key in enumerate(keys):
    data_path = os.path.join(folder_path, key)
    if i == 0:
        readFile = read_file(data_path, strip=[42, 49], show_data_flag=False)
        data = readFile.data
        x = data['wavelength']
        y = data['intensity']
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.plot(x, y)
        the_figure(ax, key)

    if key == 'qdot_white 029.spe':
        readFile = read_file(data_path, strip=[35, 53], show_data_flag=False)
        data = readFile.data
        wav = data['wavelength']
        sp = data['intensity']
    elif key == 'sio2_white 034.spe':
        readFile = read_file(data_path, strip=[35, 53], show_data_flag=False)
        data = readFile.data
        sub = data['intensity']

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
abs = (sp - sub) / sub
ax.plot(wav, abs)

#         x = data['wavelength']
#         y = data['strip']
#         z = data['intensity_image']
#         # x, z = choose_range(x, z, min_val=-20, max_val=20, axis=1)
#         fig1 = plt.figure(figsize=(8, 6))
#         ax1 = fig1.add_subplot(111)
#         ax1.pcolor(x, y, z)
#         the_figure1(ax1)
#
#         readFile = read_file(data_path, strip=[35, 63], show_data_flag=False)
#         data = readFile.data
#         x = data['wavelength']
#         y = data['intensity']
#         ax.plot(x, y)
#         the_figure(ax, le)
#
# if save_fig == 1:
#     fig.savefig(fr"E:\Data\ChenGroup\FS\20250331\fig.png")
#     fig0.savefig(fr"E:\Data\ChenGroup\FS\20250331\fig0.png")
#     fig1.savefig(fr"E:\Data\ChenGroup\FS\20250331\fig1.png")

plt.show()