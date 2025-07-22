import os.path
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from src.general.figure import set_figure
from src.general.numerical.curve_functions import *
from src.general.load_data.load_data_from_txt import *

def the_figure(ax):
    set_figure.set_label_and_title(ax, title='Excitation Polarization', xlabel='', ylabel='')
    set_figure.set_spines(ax, mode='polar')
    set_figure.set_tick(ax, ticks_xlabel=np.radians(np.arange(0, 360, 45)), ticks_ylabel=np.arange(0, 251, 50), ticks_xlabel_pad=20)
    ax.axes.get_yticklabels()[0].set_visible(False)  # 隐藏y轴（极轴）第一个标签
    ax.grid(True)


datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-5\20250224_SPE_hBN_afterSEM_measurement-5.h5"
save_fig = 1

"""fig0"""
# with h5py.File(datapath1, "r") as f:
#     data = f['OceanOpticsSpectrometer']
#     bgd = np.array(data['calibration_Laser_HP_m2_0d_0'].attrs['background'])
#     bgd_time = data['calibration_Laser_HP_m2_0d_0'].attrs['background_int'] / 1000
#     wav = np.array(data['calibration_Laser_HP_m2_0d_0'].attrs['wavelengths'])
#     bgd = bgd / bgd_time
#
#     rots = []
#     ints = []
#     legend_labels = []
#     for key in data.keys():
#         if 'calibration_Laser_HP_m2' in key:
#             if key == 'calibration_Laser_HP_m2_44d_0':
#                 continue
#             elif key == 'calibration_Laser_HP_m2_64d_0':
#                 continue
#             elif key =='calibration_Laser_HP_m2_104d_0':
#                 continue
#             sp = data[key]
#             sp_time = sp.attrs['integration_time'] / 1000
#             sp = np.array(sp)
#             sp = sp / sp_time
#             sp = sp - bgd
#
#             x, y = choose_range(wav, sp, min_val=440, max_val=470)
#             if key == 'calibration_Laser_HP_m2_272d_1' or key == 'calibration_Laser_HP_m2_276d_1' or key == 'calibration_Laser_HP_m2_280d_1':
#                 rots.append(int(key.split('_')[-2][0:-1])+20)
#             else:
#                 rots.append(int(key.split('_')[-2][0:-1]))
#             ints.append(np.max(y))  # sp最大值
#
# rots, ints = sort_lists(rots, ints)
# rots = np.radians(rots)*2

"""读取数据"""
data = read_2d_array_from_txt(os.path.join(os.path.dirname(datapath1), f'rots_ints-Excitation.txt'), delimiter=' ')
rots = data[:, 0]
ints = data[:, 1]
"""保存PL线形拟合数据"""
# save_lines_txt(rots, ints, save_full_path=os.path.join(os.path.dirname(datapath1), f'rots_ints-Excitation.txt'))

fig0 = plt.figure(figsize=(12, 8), dpi=200)
ax0 = fig0.add_subplot(111, polar=True)
ax0.scatter(rots, ints, linewidth=3)

popt, pcov = curve_fit(elliptical_polarization_malus_law, rots, ints)
I0, Ex, Ey, delta = popt
print(f"I0={I0}, Ex={Ex}, Ey={Ey}, delta={delta}")
y_fit = elliptical_polarization_malus_law(rots, *popt)
ax0.plot(rots, y_fit, linewidth=2, color='#d62728')

the_figure(ax0)
plt.tight_layout()
if save_fig == 1:
    plt.savefig(os.path.join(os.path.dirname(datapath1), 'Excitation-polarization.png'))
plt.show()