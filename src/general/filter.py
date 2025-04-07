import numpy as np

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