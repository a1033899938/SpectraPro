import numpy as np

from src.general.figure import set_figure
from src.general.load_data import read_file


def the_figure(ax, cbar):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'', xlabel='Angle(degree)', ylabel='Energy(eV)', colorbar=cbar, colorbar_label='Intensity(cts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, colorbar=cbar, ticks_xlabel=np.arange(-30, 31, 10), ticks_ylabel=np.arange(1.55, 2.16, 0.15))  # Normalized
    set_figure.set_scientific_y_ticks(ax, cbar, sci_position=(2, 0))
    # ax.invert_yaxis()
    plt.tight_layout()

files = [r"C:\Users\a1033\Desktop\Junjie Xie\Spectra\Princeton Instrument\XieJunjie-PI\WS2ML-20230718-3#\20240320\2\WS2ML-20230718-3#-532nmLaser-50uW-hole-position1-kspace-noPinhole-50slit-2s-5frames-20240320-(1)-550to1000-x-x.spe",
         r"C:\Users\a1033\Desktop\Junjie Xie\Spectra\Princeton Instrument\XieJunjie-PI\WS2ML-20230718-3#\20240320\2\WS2ML-20230718-3#-532nmLaser-50uW-WS_2ML(sio2)-position1-kspace-noPinhole-50slit-2s-5frames-20240320-(1)-550to1000-x-x.spe",
         r"C:\Users\a1033\Desktop\Junjie Xie\Spectra\Princeton Instrument\XieJunjie-PI\WS2ML-20230718-3#\20240320\2\WS2ML-20230718-3#-532nmLaser-50uW-WS_2ML(hole)-position1-kspace-noPinhole-50slit-2s-5frames-20240320-(2)-550to1000-x-x.spe"
         ]
NA = 0.55

for file in files:
    readFile = read_file(file, strip=[45, 56], show_data_flag=False)
    data = readFile.data
    x = data['strip']
    y = data['wavelength']
    z = data['intensity_image']
    z = np.array(z)
    z = z / 50  # 20uW ex

    centerstrip = 51
    x = np.array(x)
    Angle = np.tan(np.arcsin(NA)) * ((x - centerstrip) / (centerstrip - 1))
    Angle = 180 / np.pi * np.arctan(Angle)
    print(np.max(Angle))
    x = Angle

    [y, z] = choose_range(y, z, min_val=550, max_val=800, axis=1)
    y = 1240 / y

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    im = ax.pcolor(x, y, np.transpose(z), cmap='viridis')

    cbar = fig.colorbar(im)
    ax.set_xlim([-30,30])
    the_figure(ax, cbar)

plt.show()