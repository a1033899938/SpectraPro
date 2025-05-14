from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from src.general import set_figure
from src.general.curve_functions import *
from src.general.save_figure import save_subfig

save_fig = 0

"""fig0"""
# x：物镜下激光功率
# y：爬高架前激光功率
x = [10, 20, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000, 3500, 4000 ,4500]
y = [42.2, 84.2, 214, 437, 828, 1265, 1730, 2230, 2570, 3290, 3850, 4140, 4380, 6610, 8880, 11420, 13650, 16050, 18200,  20200]
x = np.array(x)
y = np.array(y)

"""拟合"""
try:
    p0 = [40, 0]
    popt, pcov = curve_fit(linear, x, y, p0=p0)
    k, b = popt
    print(f'拟合结果: k = {k:.5f}, b = {b:.5f}')
    y_fit = linear(x, *popt)
except Exception as e:
    print(e)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
ax.plot(x, y, 'o', color='blue')
ax.plot(x, y_fit, color='red')

title = 'Laser Power Ratio'
set_figure.set_label_and_title(ax, title=title, xlabel='Laser Power on Sample(uW)', ylabel='Laser Power before Elevator(uW)',
                               label_fontsize=25, title_fontsize=25,
                               label_font_family='Times New Roman', title_font_family='Times New Roman',
                               label_fontweight='bold', title_fontweight='bold',
                               label_pad=8, title_pad=15)
set_figure.set_tick(ax, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                    linewidth=3, tick_pad=5, direction='in',
                    ticks_xlabel=np.arange(0, 4501, 1500))
plt.tight_layout()
plt.show()

if save_fig == 1:
    plt.savefig(fig, r'D:\ExpData\Lab\LaserPowerRatio\LaserPowerRatio.png')

"""计算目标功率"""
x_new = np.array([10, 20, 50])
x_new = np.concatenate((x_new, np.arange(100, 4501, 100)))
y_new = linear(x_new, *popt)
y_new = [int(y) for y in y_new]
for x, y in zip(x_new, y_new):
    print(f'x = {x}, y = {y}')

