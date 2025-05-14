import h5py
import os
from scipy.optimize import curve_fit
from src.general import set_figure
from src.general.draw_figure import *
from src.general.edit_data import *
from src.general.filter import *
from src.general.curve_functions import *
from src.general.save_data import *

def the_figure(ax, key):
    set_figure.set_label_and_title(ax, title=f'hBN-after-SEM-process PL-Continuous Collection\n{key[13:-15]}', xlabel='Measurement  sequence', ylabel='Wavelength(nm)', mode='3d', zlabel_rotation=90, axis_order=(1, 2, 0))
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(0, 301, 50), ticks_ylabel=np.arange(400, 901, 100), mode='3d')  # Normalized
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=20, azim=-45)  # elev 是仰角，azim 是方位角
    plt.tight_layout()
    ax.grid(True)

def the_figure1(ax, key):
    set_figure.set_label_and_title(ax, title=f'Stability of Peak-1\n{key[13:-15]}', xlabel="Time(s)", ylabel='Intensity(counts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(0, 301, 100))
    ax1.set_ylim(0, np.max(ints_now) * 1.1)
    plt.tight_layout()

datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-5\20250224_SPE_hBN_afterSEM_measurement-5.h5"
save_fig = 0

"""fig0"""
with h5py.File(datapath1, "r") as f:
    data = f['OceanOpticsSpectrometer']
    bgd = np.array(data['hBN_afterSEM_5kV_5min_2mW_m3_stability_0'].attrs['background'])
    bgd_time = data['hBN_afterSEM_5kV_5min_2mW_m3_stability_0'].attrs['background_int'] / 1000
    wav = np.array(data['hBN_afterSEM_5kV_5min_2mW_m3_stability_0'].attrs['wavelengths'])
    bgd = bgd / bgd_time

    bgd, _ = np.meshgrid(bgd, np.arange(0, data['hBN_afterSEM_5kV_5min_2mW_m3_stability_0'].shape[0])) # 创建一个与sp相同大小的bgd阵列
    legend_labels = []
    for key in data.keys():
        if 'stability' in key:
            # fig = plt.figure(figsize=(12, 9))
            # ax = fig.add_subplot(111, projection='3d')
            # sp = data[key]
            # sp_time = sp.attrs['integration_time'] / 1000
            # sp = np.array(sp)
            # sp = sp / sp_time
            # sp = sp - bgd
            #
            # """三维时序图"""
            # Z = []
            # for line in sp:
            #     Z.append(remove_spikes(line, window_size=5, threshold=3))
            # Z = np.array(Z)
            # x, Z = choose_range(wav, Z, min_val=400, max_val=900, axis=1)
            # draw_cascade(ax, x, Z, highlight_maximum=True, plot_maximum=True)
            # """三维时序图"""
            #
            # # 导出数据之后，修正key
            # if key == 'hBN_afterSEM_5kV_2min_100KX_2mW_m3_stability_0':
            #     key = 'hBN_afterSEM_5kV_5min_100KX_2mW_m3_stability_0'
            # elif key == 'hBN_afterSEM_10kV_5min_100KX_2mW_m3_stability_0':
            #     key = 'hBN_afterSEM_10kV_2min_100KX_2mW_m3_stability_0'
            # elif key == 'hBN_afterSEM_15kV_2min_100KX_2mW_m3_stability_0':
            #     key = 'hBN_afterSEM_15kV_5min_100KX_2mW_m3_stability_0'
            # elif key == 'hBN_afterSEM_15kV_1min_100KX_2mW_m3_stability_0':
            #     key = 'hBN_afterSEM_15kV_2min_100KX_2mW_m3_stability_0'
            # the_figure(ax, key)
            #
            # if save_fig == 1:
            #     fig.savefig(os.path.join(os.path.dirname(datapath1), 'stability', f'{key[13:-15]}.png'))
            # plt.close(fig)
            #
            #
            # ints_now = []
            # cws_now = []
            # gammas_now = []
            # times_now = []
            # for i, line in enumerate(Z):
            #     x = x
            #     y = line
            #     times_now.append(i*1)
            #
            #     """三峰拟合"""
            #     p0 = [100, 537, 6,
            #             20, 550, 10,
            #              20, 577, 6]
            #
            #     bounds = ([0, 535, 0,
            #                0, 540, 0,
            #                0, 570, 0],
            #               [100000, 540, 10,
            #                 100000, 565, 12,
            #                 100000, 580, 10])
            #     min_differences_for_fit = np.abs(x - 510)
            #     min_index_for_fit = np.argmin(min_differences_for_fit)
            #     max_differences_for_fit = np.abs(x - 700)
            #     max_index_for_fit = np.argmin(max_differences_for_fit)
            #
            #     x_for_fit, y_for_fit = choose_range(x, y, min_val=510, max_val=700)
            #     popt, pcov = curve_fit(lorentzian_2_plus_gaussian_1, x_for_fit, y_for_fit, p0=p0, bounds=bounds)
            #     A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3 = popt
            #     mag_now = (A1/np.pi)/(gamma1/2)
            #     ints_now.append(mag_now)
            #     cws_now.append(x1)
            #     gammas_now.append(gamma1)

            """读取数据"""
            times_now, ints_now = read_lines_txt(fr"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-5\stability\txt\times_ints_{key[13:-15]}.txt")
            """保存PL线形拟合数据"""
            # save_lines_txt(times_now, ints_now, save_full_path=os.path.join(r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-5\stability\txt", f'times_ints_{key[13:-15]}.txt'))

            fig1 = plt.figure(figsize=(8, 6))
            ax1 = fig1.add_subplot(111)
            ax1.plot(times_now, ints_now, color='#1f77b4', linewidth=2)
            the_figure1(ax1, key)
            if save_fig == 1:
                fig1.savefig(os.path.join(os.path.dirname(datapath1), 'stability', f'stability_{key[13:-15]}.png'))

            plt.close(fig1)
plt.show()