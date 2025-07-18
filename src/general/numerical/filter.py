# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.fft import rfft, irfft, rfftfreq
# from src.general.edit_data import *
#
# def remove_spikes(signal, window_size=5, threshold=3, axis=0):
#     """
#     去除尖峰，但不修改正常数据。
#
#     参数:
#         signal (np.array): 输入信号。
#         window_size (int): 滑动窗口大小。
#         threshold (float): 尖峰检测的阈值（标准差的倍数）。
#
#     返回:
#         np.array: 去除尖峰后的信号。
#     """
#     if signal.ndim == 1:
#         filtered_signal = signal.copy()  # 复制信号，避免修改原始数据
#         n = len(signal)
#
#         for i in range(n):
#             # 确定滑动窗口的边界
#             left = max(0, i - window_size)
#             right = min(n, i + window_size + 1)
#
#             # 提取窗口内的数据（排除当前点）
#             window_data = np.concatenate([signal[left:i], signal[i + 1:right]])
#
#             # 计算窗口内的均值和标准差
#             window_mean = np.mean(window_data)
#             window_std = np.std(window_data)
#
#             # 如果当前点与均值的差异超过阈值倍的标准差，则认为是尖峰
#             if window_std > 0 and abs(signal[i] - window_mean) > threshold * window_std:
#                 # 用窗口内的中值或线性插值替换尖峰
#                 filtered_signal[i] = np.median(window_data)  # 或者用插值方法
#     elif signal.ndim == 2:
#         filtered_signal = np.zeros(np.shape(signal))
#         if axis == 0:
#             nline = signal.shape[0]
#             for i in range(nline):
#                 signal_now = signal[i, :]
#                 filtered_signal[i, :] = remove_spikes(signal_now)
#         elif axis == 1:
#             nline = signal.shape[1]
#             for i in range(nline):
#                 signal_now = signal[:, i]
#                 filtered_signal[:, i] = remove_spikes(signal_now)
#         else:
#             print("axis must be 0 or 1!")
#     else:
#         print("signal.ndim error!")
#     return filtered_signal
#
#
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.fft import rfft, irfft, rfftfreq
#
#
# def remove_spikes_with_local_median(wavelengths, intensities, detect_window=5, threshold=3.0, filter_size=3):
#     """
#     结合异常检测和局部中位数滤波去除光谱尖峰
#
#     参数:
#     wavelengths (array-like): 波长数组
#     intensities (array-like): 强度数组
#     detect_window (int): 异常检测的局部窗口大小
#     threshold (float): 异常检测阈值(以MAD为单位)
#     filter_size (int): 中位数滤波器大小(奇数)
#
#     返回:
#     array-like: 处理后的强度数组
#     """
#     # 转换为numpy数组
#     wavelengths = np.array(wavelengths)
#     intensities = np.array(intensities)
#     cleaned = intensities.copy()
#
#     # 边缘填充，避免边界问题
#     padded = np.pad(cleaned, detect_window, mode='edge')
#
#     # 检测异常峰并应用局部中位数滤波
#     for i in range(len(cleaned)):
#         # 计算局部邻域的统计特性
#         local_window = padded[i:i + 2 * detect_window + 1]
#         local_median = np.median(local_window)
#         local_mad = np.median(np.abs(local_window - local_median)) * 1.4826  # MAD到STD的转换因子
#
#         # 判断是否为异常峰
#         if abs(cleaned[i] - local_median) > threshold * local_mad:
#             # 确定滤波窗口
#             half_size = filter_size // 2
#             start = max(0, i - half_size)
#             end = min(len(cleaned), i + half_size + 1)
#
#             # 应用中位数滤波
#             cleaned[i] = np.median(cleaned[start:end])
#
#     return cleaned
#
#
# def advanced_peak_removal(wavelengths, intensities, detect_window=7, repair_window=3,
#                           threshold=3.5, max_iterations=3):
#     """
#     高级尖峰去除算法，结合多级异常检测和自适应局部修复
#
#     参数:
#     wavelengths (array-like): 波长数组
#     intensities (array-like): 强度数组
#     detect_window (int): 异常检测窗口大小
#     repair_window (int): 修复窗口大小
#     threshold (float): 异常检测阈值(以MAD为单位)
#     max_iterations (int): 迭代处理次数
#
#     返回:
#     array-like: 处理后的强度数组
#     """
#     # 转换为numpy数组
#     wavelengths = np.array(wavelengths)
#     intensities = np.array(intensities)
#     cleaned = intensities.copy()
#
#     # 迭代处理，逐步消除顽固尖峰
#     for _ in range(max_iterations):
#         # 创建边缘填充，避免边界问题
#         padded = np.pad(cleaned, detect_window, mode='edge')
#         anomalies = []
#
#         # 第一阶段：检测异常峰
#         for i in range(len(cleaned)):
#             # 获取局部邻域
#             local_window = padded[i:i + 2 * detect_window + 1]
#
#             # 计算局部统计特性（排除中心点）
#             center_idx = detect_window
#             neighborhood = np.delete(local_window, center_idx)
#             local_median = np.median(neighborhood)
#             local_mad = np.median(np.abs(neighborhood - local_median)) * 1.4826
#
#             # 判断是否为异常峰（同时检查是否为局部极大值）
#             is_peak = (cleaned[i] > local_median + threshold * local_mad)
#             is_local_max = (cleaned[i] > cleaned[max(0, i - 1)]) and (
#                         cleaned[i] > cleaned[min(len(cleaned) - 1, i + 1)])
#
#             if is_peak and is_local_max:
#                 anomalies.append(i)
#
#         # 如果没有检测到异常，提前退出
#         if not anomalies:
#             break
#
#         # 第二阶段：修复异常峰
#         for idx in anomalies:
#             # 确定修复窗口
#             start = max(0, idx - repair_window)
#             end = min(len(cleaned), idx + repair_window + 1)
#
#             # 提取局部区域
#             local_region = cleaned[start:end]
#             region_indices = np.arange(start, end)
#
#             # 排除异常点本身
#             valid_indices = np.delete(region_indices, idx - start)
#             valid_values = np.delete(local_region, idx - start)
#
#             # 如果有足够的有效点，使用加权插值修复
#             if len(valid_values) >= 2:
#                 # 使用距离加权的局部插值
#                 weights = 1.0 / (1.0 + np.abs(valid_indices - idx))
#                 weights = weights / np.sum(weights)
#                 cleaned[idx] = np.sum(valid_values * weights)
#             else:
#                 # 回退到简单中位数
#                 cleaned[idx] = np.median(local_region)
#
#     return cleaned
#
# def replace_outliers(sp, wav, wavelength_range, threshold, tolerance=0.1):
#     """
#     对指定波长范围内的数据，如果有值大于阈值，则用该值附近10个数据点（去除与该值相近的所有值）的平均值来替代与该值相近的所有值。
#
#     参数:
#         data (numpy.ndarray): 数据数组，假设为二维数组，第一列是波长，第二列是值。
#         wavelength_range (tuple): 波长范围，例如 (400, 700)。
#         threshold (float): 阈值，大于该值的点会被处理。
#         tolerance (float): 判断“相近”的容差范围。
#
#     返回:
#         numpy.ndarray: 处理后的数据。
#     """
#     # 筛选指定波长范围内的数据
#
#     min_differences = np.abs(wav - wavelength_range[0])
#     min_index = np.argmin(min_differences)
#     max_differences = np.abs(wav - wavelength_range[1])
#     max_index = np.argmin(max_differences)
#
#     filtered_data = sp[min_index:max_index]
#
#     # 找到大于阈值的值
#     outlier_indices = np.where(filtered_data > threshold)[0]
#
#     # 遍历所有大于阈值的点
#     for idx in outlier_indices:
#         outlier_value = filtered_data[idx]
#
#         # 找到与该值相近的所有点
#         close_indices = np.where(np.abs(filtered_data[:] - outlier_value) <= tolerance)[0]
#
#         # 提取附近10个数据点（排除相近的点）
#         start = max(0, idx - 10 - len(close_indices))
#         end = min(len(filtered_data), idx + 10 + len(close_indices))
#         nearby_values = filtered_data[start:end]
#
#         # 排除相近的点
#         nearby_values = nearby_values[np.abs(nearby_values - outlier_value) > tolerance]
#
#         # 如果附近有足够的数据点，计算平均值并替换
#         if len(nearby_values) >= 10:
#             avg_value = np.mean(nearby_values[:10])  # 取前10个数据点的平均值
#             filtered_data[close_indices] = avg_value  # 替换相近的所有值
#
#     # 将处理后的数据合并回原始数据
#     sp[min_index:max_index] = filtered_data
#     return sp
#
# # 示例使用
# if __name__ == "__main__":
#     # 生成示例光谱数据
#     np.random.seed(42)
#     wavelengths = np.linspace(400, 800, 500)
#     base_signal = 100 + 50 * np.sin(wavelengths / 50) + 0.1 * wavelengths
#
#     # 添加随机尖峰
#     intensities = base_signal.copy()
#     for i in np.random.choice(range(10, 490), 20, replace=False):
#         intensities[i] += 30 * np.random.random()  # 添加随机尖峰
#
#     # 添加一个宽峰
#     intensities += 60 * np.exp(-0.5 * ((wavelengths - 600) / 15) ** 2)
#
#     # 频域滤波处理光谱数据
#     cleaned = spectral_filtering(wavelengths, intensities, cutoff_freq=0.1)
#
#     # 可视化结果
#     plt.figure(figsize=(12, 6))
#     plt.plot(wavelengths, intensities, 'b-', alpha=0.7, label='原始光谱')
#     plt.plot(wavelengths, cleaned, 'r-', alpha=0.7, label='滤波后的光谱')
#     plt.xlabel('波长 (nm)')
#     plt.ylabel('强度')
#     plt.title('频域滤波去除尖峰')
#     plt.legend()
#     plt.grid(True)
#     plt.show()

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import median_filter


def detect_spikes_median(signal, filter_size=5, threshold=3.0):
    """
    基于局部中位数检测尖峰

    参数:
    signal: 输入信号
    filter_size: 局部邻域大小（奇数）
    threshold: 判定尖峰的阈值（标准差倍数）

    返回:
    spike_indices: 尖峰位置索引
    """
    # 计算局部中位数
    median_signal = median_filter(signal, size=filter_size)

    # 计算残差（原始信号与中位数的差异）
    residuals = np.abs(signal - median_signal)

    # 计算残差的标准差
    std_residuals = np.std(residuals)

    # 检测超过阈值的点
    spike_indices = np.where(residuals > threshold * std_residuals)[0]

    return spike_indices


def remove_spikes(signal, spike_indices, method='linear'):
    """
    去除检测到的尖峰

    参数:
    signal: 输入信号
    spike_indices: 尖峰位置索引
    method: 替换方法，'linear'（线性插值）或'median'（中位数）

    返回:
    cleaned_signal: 去除尖峰后的信号
    """
    cleaned_signal = np.copy(signal)

    for idx in spike_indices:
        # 确定插值范围
        left = max(0, idx - 2)
        right = min(len(signal) - 1, idx + 2)

        if method == 'linear':
            # 线性插值
            if left < right:
                cleaned_signal[idx] = np.interp(idx, [left, right], [signal[left], signal[right]])
        else:
            # 使用局部中位数替换
            neighborhood = np.concatenate([signal[max(0, idx - 3):idx],
                                           signal[idx + 1:min(len(signal), idx + 4)]])
            cleaned_signal[idx] = np.median(neighborhood)

    return cleaned_signal


from scipy.signal import savgol_filter


def detect_spikes_savgol(signal, window_length=7, polyorder=3, threshold=3.0):
    """
    基于Savitzky-Golay滤波检测尖峰

    参数:
    signal: 输入信号
    window_length: 滤波窗口大小（奇数）
    polyorder: 多项式阶数
    threshold: 判定尖峰的阈值

    返回:
    spike_indices: 尖峰位置索引
    """
    # 使用Savitzky-Golay滤波平滑信号
    smoothed_signal = savgol_filter(signal, window_length, polyorder)

    # 计算残差
    residuals = np.abs(signal - smoothed_signal)

    # 计算残差的标准差
    std_residuals = np.std(residuals)

    # 检测超过阈值的点
    spike_indices = np.where(residuals > threshold * std_residuals)[0]

    return spike_indices


import pywt


def detect_spikes_wavelet(signal, wavelet='db4', level=1, threshold=3.0):
    """
    基于小波变换检测尖峰

    参数:
    signal: 输入信号
    wavelet: 小波函数名称
    level: 分解级别
    threshold: 判定尖峰的阈值

    返回:
    spike_indices: 尖峰位置索引
    """
    # 执行小波分解
    coeffs = pywt.wavedec(signal, wavelet, level=level)

    # 获取细节系数（包含高频成分）
    details = coeffs[-1]

    # 计算细节系数的标准差
    std_details = np.std(details)

    # 检测超过阈值的点
    spike_indices_wavelet = np.where(np.abs(details) > threshold * std_details)[0]

    # 将小波域的索引映射回原始信号
    scaling_factor = len(signal) / len(details)
    spike_indices = (spike_indices_wavelet * scaling_factor).astype(int)

    return spike_indices

def generate_test_signal(n_points=1000, n_spikes=20, noise_level=0.1):
    """生成包含尖峰的测试信号"""
    # 生成平滑信号（例如，高斯峰加线性背景）
    x = np.linspace(0, 1000, n_points)
    signal = 100 + 50 * np.exp(-(x - 500) ** 2 / (2 * 100 ** 2))  # 高斯峰

    # 添加随机噪声
    signal += np.random.normal(0, noise_level, n_points)

    # 添加随机尖峰
    spike_indices = np.random.choice(n_points, n_spikes, replace=False)
    spike_amplitudes = np.random.uniform(5, 20, n_spikes) * np.random.choice([-1, 1], n_spikes)
    signal[spike_indices] += spike_amplitudes

    return x, signal, spike_indices

if __name__ == '__main__':
    # # 生成测试数据
    # x, signal, true_spike_indices = generate_test_signal()
    #
    # # 检测尖峰
    # spike_indices_median = detect_spikes_median(signal, filter_size=7, threshold=3.0)
    # spike_indices_savgol = detect_spikes_savgol(signal, window_length=7, polyorder=3, threshold=3.0)
    #
    # # 去除尖峰
    # cleaned_signal_median = remove_spikes(signal, spike_indices_median, method='linear')
    # cleaned_signal_savgol = remove_spikes(signal, spike_indices_savgol, method='linear')
    #
    # # 可视化结果
    # plt.figure(figsize=(12, 8))
    #
    # plt.subplot(211)
    # plt.plot(x, signal, 'b-', label='origin')
    # plt.plot(x[true_spike_indices], signal[true_spike_indices], 'ro', markersize=5, label='true_spike_indices')
    # plt.plot(x[spike_indices_median], signal[spike_indices_median], 'g^', markersize=5, label='spike_indices_median')
    # plt.legend()
    # plt.title('尖峰检测结果')
    # plt.grid(True)
    #
    # plt.subplot(212)
    # plt.plot(x, signal, 'b-', alpha=0.3, label='origin')
    # plt.plot(x, cleaned_signal_median, 'r-', label='cleaned_signal_median')
    # plt.plot(x, cleaned_signal_savgol, 'g-', label='cleaned_signal_savgol')
    # plt.legend()
    # plt.title('尖峰去除结果')
    # plt.grid(True)
    #
    # plt.tight_layout()
    # plt.show()
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    import time

    filepath = r"D:\ExpData\np.png"
    img = cv2.imread(filepath)
    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    start_time = time.time()
    img_gray = cv2.cvtColor(img_RGB, cv2.COLOR_RGB2GRAY)
    laplacian = cv2.Laplacian(img_gray, cv2.CV_64F)
    sharpness = laplacian.var()
    print(sharpness)
    end_time = time.time()
    duration = end_time - start_time
    print(duration)

    img_processed = np.uint8(np.absolute(laplacian))
    fig = plt.figure(figsize=(8, 6), dpi=200)
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.imshow(img_gray, cmap='gray')
    ax2.imshow(img_processed, cmap='gray')
    fig.canvas.draw_idle()
    plt.show()