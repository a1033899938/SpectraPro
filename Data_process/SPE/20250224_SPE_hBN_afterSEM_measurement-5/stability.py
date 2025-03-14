import os.path
from scipy.optimize import curve_fit
import h5py
from src.general import set_figure

def gaussian(x, A, mu, sigma):
    return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))


def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
    return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))


def lorentzian(x, A, x0, gamma):
    """
    洛伦兹函数
    :param x: 自变量
    :param A: 峰值面积
    :param x0: 峰值中心位置
    :param gamma: 半高全宽 (FWHM)
    :return: 洛伦兹函数值
    """
    return (A / np.pi) * (0.5 * gamma) / ((x - x0) ** 2 + (0.5 * gamma) ** 2)

def lorentzian_plus_gaussian(x, A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3):
    peak1 = lorentzian(x, A1, x1, gamma1)
    peak2 = gaussian(x, A2, x2, gamma2)
    peak3 = lorentzian(x, A3, x3, gamma3)
    return peak1 + peak2 + peak3

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-5\20250224_SPE_hBN_afterSEM_measurement-5.h5"
save_fig = 1

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
            fig0 = plt.figure(figsize=(12, 9))
            ax0 = fig0.add_subplot(111, projection='3d')
            sp = data[key]
            print(np.shape(np.array(sp)))
            sp_time = sp.attrs['integration_time'] / 1000
            sp = np.array(sp)
            print(sp)
            sp = sp / sp_time
            sp = sp - bgd
            # print(sp)
            min_differences = np.abs(wav - 400)
            min_index = np.argmin(min_differences)
            max_differences = np.abs(wav - 900)
            max_index = np.argmin(max_differences)

            x = wav[min_index:max_index]
            y = np.arange(sp.shape[0])
            X, Y = np.meshgrid(x, y)
            Z = sp[:, min_index:max_index]

            for i in y:
                ax0.plot(Y[i], X[i], Z[i], color=plt.cm.viridis(i / len(y)),
                         linestyle='-', linewidth=1, alpha=1)
                ax0.plot(Y[i], X[i], np.zeros_like(Z[i]), color='gray', alpha=1)

                polygon = [
                    [Y[i, 0], X[i, 0], 0],  # 左下
                    [Y[i, -1], X[i, -1], 0],  # 右下
                ]
                for j in range(len(x) - 1, -1, -1):  # 依次添加点，使得polygon成为一个完整的闭合多边形
                    polygon.append([Y[i, j], X[i, j], Z[i, j]])
                ax0.add_collection3d(Poly3DCollection([polygon], color=plt.cm.viridis(i / len(y)), alpha=0.5))

            # 导出数据之后，修正key
            if key == 'hBN_afterSEM_5kV_2min_100KX_2mW_m3_stability_0':
                key = 'hBN_afterSEM_5kV_5min_100KX_2mW_m3_stability_0'
            elif key == 'hBN_afterSEM_10kV_5min_100KX_2mW_m3_stability_0':
                key = 'hBN_afterSEM_5kV_2min_100KX_2mW_m3_stability_0'
            elif key == 'hBN_afterSEM_15kV_2min_100KX_2mW_m3_stability_0':
                key = 'hBN_afterSEM_5kV_5min_100KX_2mW_m3_stability_0'
            elif key == 'hBN_afterSEM_15kV_1min_100KX_2mW_m3_stability_0':
                key = 'hBN_afterSEM_5kV_2min_100KX_2mW_m3_stability_0'

            title = f'hBN-after-SEM-process Time-Resolved PL\n{key}'
            set_figure.set_label_and_title(ax0, title=title, xlabel='Process time(min)', ylabel='Intensity(counts)',
                                           label_fontsize=25, title_fontsize=25,
                                           label_font_family='Times New Roman', title_font_family='Times New Roman',
                                           label_fontweight='bold', title_fontweight='bold',
                                           label_pad=15, title_pad=15, mode='3d')
            set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
            set_figure.set_tick(ax0, xbins=6, ybins=10, fontsize=10, fontweight='bold',
                                linewidth=3, tick_pad=5, direction='in',
                                ticks_xlabel=np.arange(0, sp.shape[0]+1, 50),
                                ticks_ylabel=np.arange(400, 901, 100), mode='3d')  # Normalized
            ax0.set_xlabel(xlabel='Measurement  sequence', labelpad=15)
            ax0.set_ylabel(ylabel='Wavelength(nm)', labelpad=15)
            ax0.zaxis.set_rotate_label(False)
            ax0.set_zlabel(zlabel='Intensity(counts)', rotation=90, labelpad=15)

            ax0.set_box_aspect([1, 1, 1])
            ax0.view_init(elev=20, azim=45)  # elev 是仰角，azim 是方位角
            plt.tight_layout()
            ax0.grid(True)
            # plt.show()
            # print(len('_2mW_m3_stability_0'))
            if save_fig == 1:
                from src.general.save_figure import save_subfig
                plt.savefig(os.path.join(os.path.dirname(datapath1), 'stability', f'{key[:-19]}.png'))
            # plt.close()