import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, irfft, rfftfreq

def remove_spikes(signal, window_size=5, threshold=3, axis=0):
    """
    去除尖峰，但不修改正常数据。

    参数:
        signal (np.array): 输入信号。
        window_size (int): 滑动窗口大小。
        threshold (float): 尖峰检测的阈值（标准差的倍数）。

    返回:
        np.array: 去除尖峰后的信号。
    """
    if signal.ndim == 1:
        filtered_signal = signal.copy()  # 复制信号，避免修改原始数据
        n = len(signal)

        for i in range(n):
            # 确定滑动窗口的边界
            left = max(0, i - window_size)
            right = min(n, i + window_size + 1)

            # 提取窗口内的数据（排除当前点）
            window_data = np.concatenate([signal[left:i], signal[i + 1:right]])

            # 计算窗口内的均值和标准差
            window_mean = np.mean(window_data)
            window_std = np.std(window_data)

            # 如果当前点与均值的差异超过阈值倍的标准差，则认为是尖峰
            if window_std > 0 and abs(signal[i] - window_mean) > threshold * window_std:
                # 用窗口内的中值或线性插值替换尖峰
                filtered_signal[i] = np.median(window_data)  # 或者用插值方法
    elif signal.ndim == 2:
        filtered_signal = np.zeros(np.shape(signal))
        if axis == 0:
            nline = signal.shape[0]
            for i in range(nline):
                signal_now = signal[i, :]
                filtered_signal[i, :] = remove_spikes(signal_now)
        elif axis == 1:
            nline = signal.shape[1]
            for i in range(nline):
                signal_now = signal[:, i]
                filtered_signal[:, i] = remove_spikes(signal_now)
        else:
            print("axis must be 0 or 1!")
    else:
        print("signal.ndim error!")
    return filtered_signal


import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, irfft, rfftfreq


def remove_spikes_with_local_median(wavelengths, intensities, detect_window=5, threshold=3.0, filter_size=3):
    """
    结合异常检测和局部中位数滤波去除光谱尖峰

    参数:
    wavelengths (array-like): 波长数组
    intensities (array-like): 强度数组
    detect_window (int): 异常检测的局部窗口大小
    threshold (float): 异常检测阈值(以MAD为单位)
    filter_size (int): 中位数滤波器大小(奇数)

    返回:
    array-like: 处理后的强度数组
    """
    # 转换为numpy数组
    wavelengths = np.array(wavelengths)
    intensities = np.array(intensities)
    cleaned = intensities.copy()

    # 边缘填充，避免边界问题
    padded = np.pad(cleaned, detect_window, mode='edge')

    # 检测异常峰并应用局部中位数滤波
    for i in range(len(cleaned)):
        # 计算局部邻域的统计特性
        local_window = padded[i:i + 2 * detect_window + 1]
        local_median = np.median(local_window)
        local_mad = np.median(np.abs(local_window - local_median)) * 1.4826  # MAD到STD的转换因子

        # 判断是否为异常峰
        if abs(cleaned[i] - local_median) > threshold * local_mad:
            # 确定滤波窗口
            half_size = filter_size // 2
            start = max(0, i - half_size)
            end = min(len(cleaned), i + half_size + 1)

            # 应用中位数滤波
            cleaned[i] = np.median(cleaned[start:end])

    return cleaned


def advanced_peak_removal(wavelengths, intensities, detect_window=7, repair_window=3,
                          threshold=3.5, max_iterations=3):
    """
    高级尖峰去除算法，结合多级异常检测和自适应局部修复

    参数:
    wavelengths (array-like): 波长数组
    intensities (array-like): 强度数组
    detect_window (int): 异常检测窗口大小
    repair_window (int): 修复窗口大小
    threshold (float): 异常检测阈值(以MAD为单位)
    max_iterations (int): 迭代处理次数

    返回:
    array-like: 处理后的强度数组
    """
    # 转换为numpy数组
    wavelengths = np.array(wavelengths)
    intensities = np.array(intensities)
    cleaned = intensities.copy()

    # 迭代处理，逐步消除顽固尖峰
    for _ in range(max_iterations):
        # 创建边缘填充，避免边界问题
        padded = np.pad(cleaned, detect_window, mode='edge')
        anomalies = []

        # 第一阶段：检测异常峰
        for i in range(len(cleaned)):
            # 获取局部邻域
            local_window = padded[i:i + 2 * detect_window + 1]

            # 计算局部统计特性（排除中心点）
            center_idx = detect_window
            neighborhood = np.delete(local_window, center_idx)
            local_median = np.median(neighborhood)
            local_mad = np.median(np.abs(neighborhood - local_median)) * 1.4826

            # 判断是否为异常峰（同时检查是否为局部极大值）
            is_peak = (cleaned[i] > local_median + threshold * local_mad)
            is_local_max = (cleaned[i] > cleaned[max(0, i - 1)]) and (
                        cleaned[i] > cleaned[min(len(cleaned) - 1, i + 1)])

            if is_peak and is_local_max:
                anomalies.append(i)

        # 如果没有检测到异常，提前退出
        if not anomalies:
            break

        # 第二阶段：修复异常峰
        for idx in anomalies:
            # 确定修复窗口
            start = max(0, idx - repair_window)
            end = min(len(cleaned), idx + repair_window + 1)

            # 提取局部区域
            local_region = cleaned[start:end]
            region_indices = np.arange(start, end)

            # 排除异常点本身
            valid_indices = np.delete(region_indices, idx - start)
            valid_values = np.delete(local_region, idx - start)

            # 如果有足够的有效点，使用加权插值修复
            if len(valid_values) >= 2:
                # 使用距离加权的局部插值
                weights = 1.0 / (1.0 + np.abs(valid_indices - idx))
                weights = weights / np.sum(weights)
                cleaned[idx] = np.sum(valid_values * weights)
            else:
                # 回退到简单中位数
                cleaned[idx] = np.median(local_region)

    return cleaned

# 示例使用
if __name__ == "__main__":
    # 生成示例光谱数据
    np.random.seed(42)
    wavelengths = np.linspace(400, 800, 500)
    base_signal = 100 + 50 * np.sin(wavelengths / 50) + 0.1 * wavelengths

    # 添加随机尖峰
    intensities = base_signal.copy()
    for i in np.random.choice(range(10, 490), 20, replace=False):
        intensities[i] += 30 * np.random.random()  # 添加随机尖峰

    # 添加一个宽峰
    intensities += 60 * np.exp(-0.5 * ((wavelengths - 600) / 15) ** 2)

    # 频域滤波处理光谱数据
    cleaned = spectral_filtering(wavelengths, intensities, cutoff_freq=0.1)

    # 可视化结果
    plt.figure(figsize=(12, 6))
    plt.plot(wavelengths, intensities, 'b-', alpha=0.7, label='原始光谱')
    plt.plot(wavelengths, cleaned, 'r-', alpha=0.7, label='滤波后的光谱')
    plt.xlabel('波长 (nm)')
    plt.ylabel('强度')
    plt.title('频域滤波去除尖峰')
    plt.legend()
    plt.grid(True)
    plt.show()