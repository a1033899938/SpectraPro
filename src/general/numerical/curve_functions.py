"""
Author: Junjie-Xie
Updated: 2025/07/18
Functions:
    1. 基础函数：线性函数、高斯函数、洛伦兹函数、Voigt函数
    2. 物理模型函数：功率饱和曲线、部分偏振光马吕斯定律、椭圆偏振光马吕斯定律
    3. 组合函数：双高斯函数、双洛伦兹函数、三洛伦兹函数、两洛伦兹加一高斯函数
"""

import numpy as np
from scipy.special import wofz  # Faddeeva 函数，用于计算 Voigt 函数

"""基础函数"""
def linear(x, k, b):
    """
    :param x: 自变量
    :param k: 斜率
    :param b: 截距
    :return:
    """
    y = k*x + b
    return y

def gaussian(x, A, mu, sigma):
    """
    :param x: 自变量
    :param A: 峰值幅度
    :param mu: 峰值中心位置
    :param sigma: 标准差 (FWHM≈2.3548*sigma)
    :return:
    """
    """高斯峰函数：A-振幅，x0-中心位置，sigma-标准差（半高宽 ≈ 2√(2ln2)*sigma ≈ 2.3548*sigma），全宽 ≈ 2*sigma"""
    # fwhm = 2 * np.sqrt(2 * np.log(2)) * sigma  # 半高全宽
    # fwtm = 2 * np.sqrt(2 * np.log(10)) * sigma  # 1/10高度全宽 (FWTM)
    # full_width = 2 * sigma  # 标准差全宽
    # theoretical_range = 6 * sigma  # 3σ范围（覆盖99.7%）

    return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))

def lorentzian(x, A, x0, gamma):
    """
    洛伦兹函数
    :param x: 自变量
    :param A: 峰值面积 (幅值=2A/(π*gamma))
    :param x0: 峰值中心位置
    :param gamma: 半高全宽 (FWHM)
    :return: 洛伦兹函数值
    """
    return (A / np.pi) * (0.5 * gamma) / ((x - x0) ** 2 + (0.5 * gamma) ** 2)

def voigt(x, A, mu, sigma, gamma):
    """
       Voigt线形函数（高斯-洛伦兹卷积）

       :param x: 自变量（如波长、频率）
       :param amplitude: 振幅（缩放因子）
       :param center: 峰中心位置
       :param gauss_std: 高斯成分的标准差
       :param lorentz_hwhm: 洛伦兹成分的半高半宽（HWHM）
       :return: Voigt函数值
       """

    z = (x - mu + 1j * gamma) / (sigma * np.sqrt(2))
    return A * np.real(wofz(z)) / (sigma * np.sqrt(2 * np.pi))

def power_law_fit(x, A, x0):
    return A / (x - x0)**2

def mono_exp(t, I0, tau, B):
    return I0 * np.exp(-t / tau) + B

"""物理模型函数"""
def power_saturation(P, P_sat, I_inf):
    """
    用于拟合PL强度随功率增大而饱和的数据
    :param P: 自变量（激发功率）
    :param P_sat: 饱和功率
    :param I_inf: 饱和时的PL强度
    :return: PL强度值
    """
    P = np.array(P, dtype=np.float64)
    return (I_inf * P) / (P + P_sat)

def partial_polarized_malus_law(theta, I0, DOP, phi):
    """
    根据马吕斯定律计算部分偏振光通过偏振片后的透射光强。
    :param theta: 自变量（旋转角度）（单位：度）
    :param I0: 入射光的总光强
    :param DOP: 偏振度（0 <= DOP <= 1）
    :param phi: 初相位
    :return: 透射光强
    """

    # 计算完全偏振光和非偏振光的光强
    I_p = I0 * DOP  # 完全偏振光的光强
    I_u = I0 * (1 - DOP)  # 非偏振光的光强

    # 计算完全偏振光部分的透射光强（马吕斯定律）
    I_p_transmitted = I_p * (np.cos(theta + phi) ** 2)

    # 计算非偏振光部分的透射光强（减半）
    I_u_transmitted = I_u / 2

    # 总透射光强
    I_transmitted = I_p_transmitted + I_u_transmitted

    return I_transmitted

def elliptical_polarization_malus_law(theta, I0, Ex, Ey, delta):
    """
    根据马吕斯定律计算椭圆偏振光通过偏振片后的透射光强
    :param theta: 自变量（旋转角度）（单位：度）
    :param I0: 入射光的总光强
    :param Ex: 电场在x方向的振幅
    :param Ey: 电场在y方向的振幅
    :param delta: x和y分量之间的相位差（单位：度）
    :return: 透射光强
    """

    # 计算透射光强
    I_transmitted = I0 * (
        (Ex * np.cos(theta)) ** 2 +
        (Ey * np.sin(theta)) ** 2 +
        2 * Ex * Ey * np.cos(theta) * np.sin(theta) * np.cos(delta)
    )

    # 计算线偏振度（Degree of Linear Polarization）
    dolp_numerator = np.sqrt((Ex ** 2 - Ey ** 2) ** 2 + 4 * (Ex * Ey * np.cos(delta)) ** 2)
    dolp_denominator = Ex ** 2 + Ey ** 2
    dolp = dolp_numerator / dolp_denominator if dolp_denominator != 0 else 0
    print(f"dolp = {dolp}")
    return I_transmitted


"""组合函数"""
def double_lorentzian(x, A1, x1, gamma1, A2, x2, gamma2):
    peak1 = lorentzian(x, A1, x1, gamma1)
    peak2 = lorentzian(x, A2, x2, gamma2)
    return peak1 + peak2

def triple_lorentzian(x, A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3):
    peak1 = lorentzian(x, A1, x1, gamma1)
    peak2 = lorentzian(x, A2, x2, gamma2)
    peak3 = lorentzian(x, A3, x3, gamma3)
    return peak1 + peak2 + peak3

def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
    peak1 = gaussian(x, A1, mu1, sigma1)
    peak2 = gaussian(x, A2, mu2, sigma2)
    return peak1 + peak2

def triple_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2, A3, mu3, sigma3):
    peak1 = gaussian(x, A1, mu1, sigma1)
    peak2 = gaussian(x, A2, mu2, sigma2)
    peak3 = gaussian(x, A3, mu3, sigma3)
    return peak1 + peak2 + peak3

def lorentzian_2_plus_gaussian_1(x, A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3):
    peak1 = lorentzian(x, A1, x1, gamma1)
    peak2 = gaussian(x, A2, x2, gamma2)
    peak3 = lorentzian(x, A3, x3, gamma3)
    return peak1 + peak2 + peak3

