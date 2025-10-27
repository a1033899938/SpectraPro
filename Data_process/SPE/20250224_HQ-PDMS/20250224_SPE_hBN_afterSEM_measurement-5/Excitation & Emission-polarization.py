import os.path
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from src.general.figure import set_figure
from src.general.numerical.curve_functions import *
from src.general.load_data.load_data_from_txt import *


def the_figure(ax):
    set_figure.set_label_and_title(ax, title='Excitation Polarization', xlabel='', ylabel='')
    set_figure.set_spines(ax, mode='polar')
    set_figure.set_tick(ax, ticks_xlabel=np.radians(np.arange(0, 360, 45)), ticks_ylabel=np.arange(0, 1.2, 0.2), ticks_xlabel_pad=20)
    ax.axes.get_yticklabels()[0].set_visible(False)  # 隐藏y轴（极轴）第一个标签
    ax.axes.get_yticklabels()[-1].set_visible(False)  # 隐藏y轴（极轴）最后一个标签
    set_figure.set_legend(ax, legend_labels = ['Excitaion', 'Emission'], location=(1, 1, 3, 0))
    ax.grid(True)


datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-5\20250224_SPE_hBN_afterSEM_measurement-5.h5"
save_fig = 1

"""读取数据"""
data1 = read_2d_array_from_txt(os.path.join(os.path.dirname(datapath1), f'rots_ints-Excitation.txt'), delimiter=' ')
rots_ex = data1[:, 0]
ints_ex = data1[:, 1]

data2 = read_2d_array_from_txt(os.path.join(os.path.dirname(datapath1), f'rots_ints-Emission.txt'), delimiter=' ')
rots_em = data2[:, 0]
ints_em = data2[:, 1]

# 归一化数据
ints_ex = ints_ex / np.max(ints_ex)
ints_em = ints_em / np.max(ints_em)

fig0 = plt.figure(figsize=(12, 8), dpi=200)
ax0 = fig0.add_subplot(111, polar=True)
ax0.scatter(rots_ex, ints_ex, linewidth=3, color='#1f77b4')
ax0.scatter(rots_em, ints_em, linewidth=3, color='#d62728')

popt, pcov = curve_fit(elliptical_polarization_malus_law, rots_ex, ints_ex)
I0, Ex, Ey, delta = popt
print(f"I0={I0}, Ex={Ex}, Ey={Ey}, delta={delta}")
y_fit = elliptical_polarization_malus_law(rots_ex, *popt)
ax0.plot(rots_ex, y_fit, linewidth=2, color='#1f77b4')

popt, pcov = curve_fit(elliptical_polarization_malus_law, rots_em, ints_em)
I0, Ex, Ey, delta = popt
print(f"I0={I0}, Ex={Ex}, Ey={Ey}, delta={delta}")
y_fit = elliptical_polarization_malus_law(rots_em, *popt)
ax0.plot(rots_em, y_fit, linewidth=2, color='#d62728')

the_figure(ax0)
plt.tight_layout()
if save_fig == 1:
    plt.savefig(os.path.join(os.path.dirname(datapath1), 'Excitation_and_Emission-polarization.png'))
plt.show()