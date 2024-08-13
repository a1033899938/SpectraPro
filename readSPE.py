import spe2py as spe
import spe_loader as sl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms
import math  # e
import os
from scipy.optimize import curve_fit  # 用于拟合


"""定义高斯函数。用于拟合"""
def gaussian(x, height, center, width, shift):
    return height * np.exp(-(x - center) ** 2 / (2 * width ** 2)) + shift


def gaussian2(x, height_1, center_1, width_1, shift, height_2, center_2, width_2):
    return height_1 * np.exp(-(x - center_1) ** 2 / (2 * width_1 ** 2)) + height_2 * np.exp(-(x - center_2) ** 2 / (2 * width_2 ** 2)) + shift


# spe_tools = spe.load()
filepath = r'F:\Spectra\Princeton Instrument\XieJunjie\20240806'
files = []
filenames = []
for key in os.listdir(filepath):
    if 'uW-3' in key:
        filename_now = os.path.join(filepath, key)
        files.append(filename_now)
        filenames.append(key)

iFig = 0

le = []
plt.figure(iFig, figsize=(8, 6))
iFig += 1
for key, filename in zip(files, filenames):
    sp = sl.load_from_files([key])
    xdim = sp.xdim[0]
    ydim = sp.ydim[0]
    intensity = np.array(sp.data)
    intensity = np.squeeze(intensity)
    wavelength = sp.wavelength
    # wavelength = 1240/wavelength
    strip = np.arange(ydim)+1
    # print(dir(sp))
    # plt.pcolor(wavelength, strip, intensity)
    # # plt.imshow(intensity, aspect='auto')
    # plt.tight_layout()
    """取强度减小到最大值1/e处的strip"""
    sum_all_wav = np.sum(intensity, axis=1)
    sum_all_wav -= min(sum_all_wav)  # 使其都变为正数
    sum_all_wav /= max(sum_all_wav)  # 归一化
    idx_max = np.argmax(sum_all_wav) + 1
    idx_sum_all_wav_low = np.argmin(abs(sum_all_wav[1:idx_max]-1/math.e))
    idx_sum_all_wav_high = np.argmin(abs(sum_all_wav[idx_max:-1]-1/math.e)) + idx_max
    sum_all_wav = min(wavelength) + sum_all_wav*(max(wavelength) - min(wavelength))/3
    strip_min = idx_sum_all_wav_low
    strip_max = idx_sum_all_wav_high
    # plt.plot(wavelength, np.ones(len(wavelength))*strip_min, '--', color='red')
    # plt.plot(wavelength, np.ones(len(wavelength))*strip_max, '--', color='red')
    # plt.plot(sum_all_wav, strip)
    """作graph"""
    graph = np.sum(intensity[strip_min-1:strip_max-1, :], axis=0)
    graph_normalized = graph - min(graph)
    graph_normalized /= max(graph_normalized)
    graph_normalized = graph_normalized*max(strip)
    # plt.plot(wavelength, graph_normalized, '-', color='green')
    if 1:
        linestyle = '-'
    # elif 'uW-2' in key:
    #     linestyle = '--'
    # else:
    #     linestyle = ':'
    plt.plot(wavelength, graph, linestyle)
    # try:
    #     x = wavelength
    #     y = graph
    #     idx_fitMin = np.argmin(abs(x - 700))
    #     idx_fitMax = np.argmin(abs(x - 840))  # 取定拟合区间
    #     popt, pcov = curve_fit(gaussian2, x[idx_fitMin:idx_fitMax], y[idx_fitMin:idx_fitMax], p0=[10000, 740, 20, 0, 2000, 780, 20],
    #                            method='trf')  # 获取拟合参数列表popt: height, center, width, shift
    #     plt.plot(x[idx_fitMin:idx_fitMax], gaussian2(x[idx_fitMin:idx_fitMax], *popt), color='blue')
    #     plt.text(0.8, 0.85, "{:.1f}".format(popt[1]), fontsize=15, ha='center', color='red')
    #
    #
    #     "save figure"
    #     # extent = full_extent(ax[i, j]).transformed(Fig.dpi_scale_trans.inverted())
    #     # savepath = r'C:\Users\a1033\Desktop\临时备份\20240620\Particles'
    #     # savename = savepath + fr'\{key}-SERS.png'
    #     # plt.savefig(savename, bbox_inches=extent)
    #     # print(f"add file: {key}-SERS.png")
    # except Exception as e:
    #     print(f'fitting error this file: {filename} >>>>> ', end='')
    #     print(e)
    #     pass
    le.append(filename.rstrip('.spe'))
    # plt.title(f'{filename}')
plt.title("hBNonNPs 3")
plt.xlabel("wavelength(nm)")
plt.ylabel("intensity(counts)")
plt.legend(le)
plt.show()