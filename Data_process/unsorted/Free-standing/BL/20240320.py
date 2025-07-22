import numpy as np

from src.general.figure import set_figure
from src.ui import read_file


def the_figure(ax, cbar):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'', xlabel='Angle(degree)', ylabel='Energy(eV)', colorbar=cbar, colorbar_label='Intensity(cts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, colorbar=cbar, ticks_xlabel=np.arange(-30, 31, 10), ticks_ylabel=np.arange(1.55, 2.16, 0.15))  # Normalized
    set_figure.set_scientific_y_ticks(ax, cbar, sci_position=(2, 0))
    # ax.invert_yaxis()
    plt.tight_layout()

files = [r"C:\Users\a1033\Desktop\Junjie Xie\Spectra\Princeton Instrument\XieJunjie-PI\WS2BL-20230907-1#\20230913\PL\WS_2-20230907-1#532nmLaser-48.8uW-hole-position1-kspace-noPinhole-100Slit-30s-5frames-(1)-20230913-x-x-x.spe",
         r"C:\Users\a1033\Desktop\Junjie Xie\Spectra\Princeton Instrument\XieJunjie-PI\WS2BL-20230907-1#\20230913\PL\WS_2-20230907-1#532nmLaser-48.8uW-WS_2(SiO_2)-position1-kspace-noPinhole-100Slit-30s-5frames-(1)-20230913-x-x-x.spe.spe",
         r"C:\Users\a1033\Desktop\Junjie Xie\Spectra\Princeton Instrument\XieJunjie-PI\WS2BL-20230907-1#\20230913\PL\WS_2-20230907-1#532nmLaser-48.8uW-WS_2(suspended)-position1-kspace-noPinhole-100Slit-30s-5frames-(1)-20230913-x-x-x.spe"
         ]
NA = 0.55

for i, file in enumerate(files):
    readFile = read_file(file, strip=[45, 56], show_data_flag=False)
    data = readFile.data
    x = data['strip']
    y = data['wavelength']
    z = data['intensity_image']
    z = np.array(z)
    z = z / 100  # 100uW ex
    # if i == 0:
    #     sub = z
    # elif i == 1:
    #     sp = z
    #     mask = (sub == 0)
    #     sp = (sp - sub)/sub
    #     sp[mask] = 0
    #     z = sp

    centerstrip = 47
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