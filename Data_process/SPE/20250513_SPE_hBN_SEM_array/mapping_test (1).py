import os.path
from scipy.optimize import curve_fit
import h5py
from src.general import set_figure
from PIL import Image  # 用于保存图像
from src.general.save_figure import save_subfig

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

datapath1 = r"D:\User\Junjie-Xie\Data\SPE\20250224_SPE_hBN_afterSEM\20250224_SPE_hBN_afterSEM_measurement-9.h5"
save_fig = 1

"""fig0"""
with h5py.File(datapath1, "r") as f:
    data = f['OceanOpticsSpectrometer']['hBN_afterSEM_mapping_3']
    bgd = np.array(data['x-0/hBN_afterSEM_mapping-x0-y0'].attrs['background'])
    bgd_time = data['x-0/hBN_afterSEM_mapping-x0-y0'].attrs['background_int'] / 1000
    wav = np.array(data['x-0/hBN_afterSEM_mapping-x0-y0'].attrs['wavelengths'])
    bgd = bgd / bgd_time
    mapping = np.zeros([55, 65])
    print(np.shape(mapping))
    for i in range(mapping[0]):
        parent_key = f"x-{i}"
        for j in range(mapping[1]):
            child_key = f"hBN_afterSEM_mapping-x{i}-y{j}"
            sp = data[f"{parent_key}/{child_key}"]
            sp_time = sp.attrs['integration_time'] / 1000
            sp = np.array(sp)
            sp = sp / sp_time
            sp = sp - bgd
            mapping[i][j] = np.max(sp)

    fig0 = plt.figure(figsize=(8, 6))
    ax0 = fig0.add_subplot(111)
    x = range(mapping[0])
    y = range(mapping[1])
    X, Y = np.meshgrid(x, y)
    Z = mapping
    ax0.pcolor(X, Y, np.transpose(Z))
    #
    # data = f['LumeneraCamera']
    # for i, key in enumerate(data.keys()):
    #     img = data[key]
    #     img = np.asarray(img)
    #     if data[key].ndim == 2:
    #         img = Image.fromarray(img.astype(np.uint8))  # 转换为 PIL 图像
    #     elif data[key].ndim == 3:
    #         img = Image.fromarray(img.astype(np.uint8))  # 转换为 PIL 图像
    #     else:
    #         print(f"图像 {i} 的维度不支持：{img.shape}")
    #
    #     save_name = os.path.dirname(datapath1)
    #     save_name = os.path.join(save_name, f'{key}.png')
    #     img.save(save_name)
    #     # 可选：使用 matplotlib 显示图像
    #     fig1 = plt.figure(figsize=(8, 6))
    #     ax1 = fig1.add_subplot(111)
    #     ax1.imshow(img, cmap='gray' if data[key].ndim == 2 else None)

if save_fig == 1:
    # 隐藏 x 轴和 y 轴的刻度
    ax0.set_xticks([])
    ax0.set_yticks([])
    # ax1.set_xticks([])
    # ax1.set_yticks([])

    # 隐藏 x 轴和 y 轴的刻度标签
    ax0.set_xticklabels([])
    ax0.set_yticklabels([])
    # ax1.set_xticklabels([])
    # ax1.set_yticklabels([])

    # 隐藏 x 轴和 y 轴的标签
    ax0.set_xlabel('')
    ax0.set_ylabel('')
    # ax1.set_xlabel('')
    # ax1.set_ylabel('')

    fig0.savefig(os.path.join(os.path.dirname(datapath1), f'PL_mapping_hBN_afterSEM.png'))
    # fig1.savefig(os.path.join(os.path.dirname(datapath1), f'OM_image_WS2_ML.png'))
plt.show()