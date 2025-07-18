import numpy as np

from src.general.figure import set_figure
from src.general.load_data import read_file


def the_figure(ax, le):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'', ylabel='Intensity(cts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(1.55, 2.16, 0.15))  # Normalized
    set_figure.set_legend(ax, legend_labels=le, location='best', font_size=20)
    set_figure.set_scientific_y_ticks(ax)
    plt.tight_layout()

files = [r"C:\Users\a1033\Desktop\Junjie Xie\Spectra\Princeton Instrument\XieJunjie-PI\WS2ML-20230718-3#\20240320\1\WS2ML-20230718-3#-532nmLaser-0.1uW-WS_2ML(sio2)-position1-rspace-noPinhole-2000slit-3s-1frames-20240320-(1)-550to1000-x-x.spe",
         r"C:\Users\a1033\Desktop\Junjie Xie\Spectra\Princeton Instrument\XieJunjie-PI\WS2ML-20230718-3#\20240320\1\WS2ML-20230718-3#-532nmLaser-0.1uW-WS_2ML(hole)-position1-rspace-noPinhole-1785slit-3s-1frames-20240320-(1)-550to1000-x-x.spe"
         ]
NA = 0.75

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
le = ['Supported', 'Suspended']
for file in files:
    readFile = read_file(file, strip=[45, 55], show_data_flag=False)
    data = readFile.data
    x = data['wavelength']
    y = data['intensity']
    y = np.array(y)
    y = y/50  #50uW ex

    [x, y] = choose_range(x, y, min_val=550, max_val=800)

    x = np.array(x)
    x = 1240 / x
    im = ax.plot(x, y, linewidth=2)

    # popt, pcov = curve_fit(lorentzian, x, y)
    # A1, x1, gamma1 = popt
    # ax.plot(x, lorentzian(x, *popt), color='r')
    # print(f"A1={A1}, x1={x1}, gamma1={gamma1}")
the_figure(ax, le)

plt.show()