import numpy as np
from scipy.optimize import curve_fit

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

files = [r"C:\Users\a1033\Desktop\Junjie Xie\Spectra\Princeton Instrument\XieJunjie-PI\WS2BL-20230907-1#\20240320\532ex\WS2BL-20230907-1#-532nmLaser-100uW-WS2BL(sio2)-position1-rspace-noPinhole-1785sit-30s-1frames-20240320-(1)-550to1000nm-x-x.spe",
         r"C:\Users\a1033\Desktop\Junjie Xie\Spectra\Princeton Instrument\XieJunjie-PI\WS2BL-20230907-1#\20240320\532ex\WS2BL-20230907-1#-532nmLaser-100uW-WS2BL(hole)-position1-rspace-noPinhole-1785sit-30s-1frames-20240320-(1)-550to1000nm-x-x.spe"
         ]
NA = 0.7

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
le = ['Supported', 'Suspended']
for file in files:
    readFile = read_file(file, strip=[45, 55], show_data_flag=False)
    data = readFile.data
    x = data['wavelength']
    y = data['intensity']
    y = np.array(y)
    y = y / 100 #100uW ex
    [x, y] = choose_range(x, y, min_val=550, max_val=800)

    x = np.array(x)
    x = 1240 / x
    im = ax.plot(x, y, linewidth=2)

    popt, pcov = curve_fit(double_lorentzian, x, y)
    A1, x1, gamma1, A2, x2, gamma2 = popt
    ax.plot(x, double_lorentzian(x, *popt), color='r')
    if A1 > A2:
        print(A1/A2)
    else:
        print(A2/A1)
    print(f"A1={A1}, x1={x1}, gamma1={gamma1}")
    print(f"A2={A2}, x2={x2}, gamma2={gamma2}")
the_figure(ax, le)

plt.show()