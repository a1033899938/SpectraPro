"""
Author: Junjie-Xie
Updated: 2025/7/18
Functions:
    1. 基于局部中位数、Savitzky-Golay滤波和小波变换检测信号中的尖峰
    2. 通过线性插值或局部中位数替换去除检测到的尖峰
    3. 高级尖峰去除算法，结合多级异常检测和自适应局部修复
    4. 针对指定波长范围的数据，替换超过阈值的异常值
    5. 生成包含尖峰的测试信号用于算法验证
"""
import numpy as np
from scipy.ndimage import median_filter
from scipy.signal import savgol_filter
import pywt

# def remove_spikes(signal, spike_indices, window_size=5, method='linear'):
#     """
#     去除检测到的尖峰
#
#     参数:
#     signal: 输入信号
#     spike_indices: 尖峰位置索引
#     method: 替换方法，'linear'（线性插值）或'median'（中位数）
#
#     返回:
#     cleaned_signal: 去除尖峰后的信号
#     """
#     cleaned_signal = np.copy(signal)
#
#     half_window = window_size // 2
#     for idx in spike_indices:
#         # 确定插值范围
#         left = max(0, idx - half_window)
#         right = min(len(signal) - 1, idx + half_window)
#
#         if method == 'linear':
#             # 线性插值
#             if left < right:
#                 for i in range(left, right):
#                     cleaned_signal[idx] = np.interp(i, [left, right], [signal[left], signal[right]])
#         elif method == 'median':
#             # 使用局部中位数替换
#             neighborhood = np.concatenate([signal[max(0, idx - half_window):idx],
#                                            signal[idx + 1:min(len(signal), idx + half_window)]])
#             cleaned_signal[idx] = np.median(neighborhood)
#
#     return cleaned_signal

def remove_spikes(signal, spike_indices, window_size=5, method='linear'):
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
    spike_set = set(spike_indices)  # 转换为集合以便快速查找

    half_window = window_size // 2

    for idx in spike_indices:
        # 确定插值范围
        left = max(0, idx - half_window)
        right = min(len(signal) - 1, idx + half_window)

        # 找到左右边界附近的非尖峰点
        clean_left = left
        # 如果窗口左端点不是尖峰集合之外的, 则左端点右移, 直至等于右端点
        while clean_left < right and clean_left in spike_set:
            clean_left += 1

        clean_right = right
        # 如果窗口右端点不是尖峰集合之外的, 则右端点左移, 直至等于左端点
        while clean_right > clean_left and clean_right in spike_set:
            clean_right -= 1

        # 如果找不到足够的非尖峰点，使用更保守的方法
        if clean_left >= clean_right:
            print("保守滤波")
            if method == 'linear' and idx > 0 and idx < len(signal) - 1:
                # 使用相邻两点线性插值
                cleaned_signal[idx] = (cleaned_signal[idx - 1] + cleaned_signal[idx + 1]) / 2
            else:
                # 使用全局中位数作为替代
                cleaned_signal[idx] = np.median(np.delete(signal, spike_indices))
            continue

        if method == 'linear':
            # 改进的线性插值
            cleaned_signal[idx] = np.interp(idx, [clean_left, clean_right],
                                            [signal[clean_left], signal[clean_right]])
        elif method == 'median':
            # 改进的中位数替换 - 排除尖峰点
            neighborhood = []
            for i in range(max(0, idx - half_window), idx):
                if i not in spike_set:
                    neighborhood.append(signal[i])
            for i in range(idx + 1, min(len(signal), idx + half_window + 1)):
                if i not in spike_set:
                    neighborhood.append(signal[i])

            if neighborhood:
                cleaned_signal[idx] = np.median(neighborhood)
            else:
                # 如果邻域中没有非尖峰点，使用全局中位数
                cleaned_signal[idx] = np.median(np.delete(signal, spike_indices))

    return cleaned_signal

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

def detect_spikes_savgol(signal, window_length=7, polyorder=3, threshold=3.0):
    """
    基于Savitzky-Golay滤波检测尖峰

    参数:
    signal: 输入信号
    window_length: 滤波窗口大小（奇数）
    polyorder: 多项式阶数
    threshold: 判定尖峰的阈值 (残差超过标准差 threshold 倍)

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
    import numpy as np
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(12, 8), dpi=300)
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    x, signal, spike_indices = generate_test_signal()
    ax1.plot(x, signal)
    spike_indices = detect_spikes_savgol(signal, threshold=1.5)
    ax1.vlines(spike_indices, np.min(signal), np.max(signal), 'r', '--', linewidth=0.5, alpha=0.2)

    signal_wospikes = remove_spikes(signal, spike_indices, window_size=10, method='median')
    ax2.plot(x, signal_wospikes)
    plt.show()