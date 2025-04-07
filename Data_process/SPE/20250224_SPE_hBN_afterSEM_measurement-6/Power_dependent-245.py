import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from src.general import set_figure
from src.general.curve_functions import *
from src.general.save_data import *

def the_fig(ax):
    plt.yscale('log')
    set_figure.set_label_and_title(ax, title=f'Excitation power-denpendent intensity\nof peak 1',
                                   xlabel='Excitaion Power(uW)', ylabel='Intensity(counts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ybins=0, ticks_xlabel=np.arange(0, 12001, 2000))  # Normalized

datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6\20250224_SPE_hBN_afterSEM_measurement-6.h5"
save_fig = 1

txt_files = ['powers_ints-2.txt',
             'powers_ints-4.txt',
             'powers_ints-5.txt']

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
colors = ['#1f77b4', '#ff7f0e', '#d62728']
fmts = ['o', 's', '^']
for i, file in enumerate(txt_files):
    """读取数据"""
    powers, ints, errors = read_lines_txt(os.path.join(r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6", file))

    ax.errorbar(powers, ints, yerr=errors, fmt=fmts[i], color=colors[i], ecolor=colors[i], capsize=10)
    """功率依赖PL拟合"""
    popt, pcov = curve_fit(power_saturation, powers, ints)
    P_sat, I_inf = popt
    ints_fit = power_saturation(powers, *popt)
    ax.plot(powers, ints_fit, '-', color=colors[i], linewidth=2)

# powers_fun = np.arange(1, 12001, 1)
# ints_fun = np.log(powers_fun)
# ax.plot(powers_fun, ints_fun)

the_fig(ax)
plt.tight_layout()
if save_fig == 1:
    plt.savefig(os.path.join(os.path.dirname(datapath1), f'power_dependent_intensity_of_peak-1_m245_log.png'))
    # plt.savefig(os.path.join(os.path.dirname(datapath1), f'power_dependent_intensity_of_peak-1_m245.png'))
plt.show()