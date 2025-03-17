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

def linear(x, k, b):
    y = k*x + b
    return y

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

"""fig0"""
x = [10, 20, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000, 3500, 4000 ,4500]
y = [42.2, 84.2, 214, 437, 828, 1265, 1730, 2230, 2570, 3290, 3850, 4140, 4380, 6610, 8880, 11420, 13650, 16050, 18200,  20200]
x = np.array(x)
y = np.array(y)
print(len(x))
print(len(y))

try:
    """三峰拟合"""
    p0 = [40, 0]
    popt, pcov = curve_fit(linear, x, y, p0=p0)
    k, b = popt
    print(f'拟合结果: k = {k:.5f}, b = {b:.5f}')
    y_fit = linear(x, *popt)
except Exception as e:
    print(e)

fig0 = plt.figure(figsize=(8, 6))
ax0 = fig0.add_subplot(111)
ax0.plot(x, y, 'o', color='blue')
ax0.plot(x, y_fit, color='red')
ax0.grid(True)
plt.tight_layout()

x_new = np.array([10, 20, 50])
x_new = np.concatenate((x_new, np.arange(100, 4501, 100)))
y_new = linear(x_new, *popt)
y_new = [int(y) for y in y_new]
import pprint
for x, y in zip(x_new, y_new):
    print(f'x = {x}, y = {y}')

plt.show()