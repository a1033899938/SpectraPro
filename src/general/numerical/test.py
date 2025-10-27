import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from matplotlib.font_manager import FontProperties

def remove_narrow_peaks(wavelengths, signal, max_fwhm=1.0):
    """
    去除信号中所有半高宽(FWHM)小于等于指定值的峰

    参数:
    wavelengths: 波长数组 (nm)
    signal: 信号强度数组
    max_fwhm: 最大半高宽阈值，所有小于等于该值的峰将被去除，默认为1.0nm

    返回:
    filtered_signal: 滤波后的信号
    """
    # 确保输入是numpy数组
    wavelengths = np.asarray(wavelengths)
    signal = np.asarray(signal)

    # 检查输入长度是否一致
    if len(wavelengths) != len(signal):
        raise ValueError("波长和信号强度数组长度必须一致")

    # 确保波长数组按升序排列
    if not np.all(np.diff(wavelengths) >= 0):
        sorted_indices = np.argsort(wavelengths)
        wavelengths = wavelengths[sorted_indices]
        signal = signal[sorted_indices]
        print("警告：输入波长未按顺序排列，已自动排序")

    # 计算波长间隔
    dw = np.mean(np.diff(wavelengths))  # 平均波长间隔 (nm)
    n = len(signal)

    # 执行傅里叶变换
    yf = np.fft.fft(signal)
    xf = np.fft.fftfreq(n, dw)  # 空间频率 (1/nm)

    # 计算与最大半高宽对应的频率阈值
    # FWHM与标准差关系：FWHM = 2*sqrt(2*ln2)*σ
    sigma_wavelength = max_fwhm / (2 * np.sqrt(2 * np.log(2)))
    # 转换为频率域的阈值（窄峰对应高频成分）
    freq_threshold = 1 / (2 * np.pi * sigma_wavelength)

    # 创建滤波器：保留低于阈值的频率（宽峰），去除高于阈值的频率（窄峰）
    # 使用高斯过渡而不是硬阈值，减少振铃效应
    filter_mask = np.exp(-0.5 * (np.abs(xf) / freq_threshold) ** 4)  # 四次方使过渡更陡峭

    # 应用滤波器
    yf_filtered = yf * filter_mask

    # 执行逆傅里叶变换得到滤波后的信号
    filtered_signal = np.fft.ifft(yf_filtered).real

    return wavelengths, filtered_signal


def identify_peaks(wavelengths, signal, min_height=0.1):
    """识别信号中的峰并计算其半高宽"""
    # 找到所有峰
    peaks, _ = find_peaks(signal, height=min_height)

    peak_info = []
    for peak_idx in peaks:
        peak_wl = wavelengths[peak_idx]
        peak_height = signal[peak_idx]

        # 计算半高宽(FWHM)
        half_height = peak_height / 2

        # 向左找半高处
        left_idx = peak_idx
        while left_idx > 0 and signal[left_idx] > half_height:
            left_idx -= 1

        # 向右找半高处
        right_idx = peak_idx
        while right_idx < len(signal) - 1 and signal[right_idx] > half_height:
            right_idx += 1

        # 计算半高宽
        fwhm = wavelengths[right_idx] - wavelengths[left_idx]
        peak_info.append({
            'wavelength': peak_wl,
            'height': peak_height,
            'fwhm': fwhm,
            'is_narrow': fwhm <= 1.0
        })

    return peak_info


def generate_test_signal():
    """生成包含不同半高宽峰的测试信号"""
    # 波长范围 400-700nm
    wavelengths = np.linspace(400, 700, 2000)

    # 背景信号
    background = 0.05 * np.random.randn(len(wavelengths)) + 1.0

    # 高斯峰生成函数
    def gaussian_peak(wl, center, height, fwhm):
        sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
        return height * np.exp(-0.5 * ((wl - center) / sigma) ** 2)

    # 生成不同半高宽的峰
    # 窄峰（FWHM < 1nm）- 这些应该被去除
    peak1 = gaussian_peak(wavelengths, 450, 2.0, 0.5)  # FWHM 0.5nm
    peak2 = gaussian_peak(wavelengths, 510, 1.5, 0.8)  # FWHM 0.8nm

    # 宽峰（FWHM > 1nm）- 这些应该被保留
    peak3 = gaussian_peak(wavelengths, 550, 3.0, 2.0)  # FWHM 2.0nm
    peak4 = gaussian_peak(wavelengths, 600, 2.5, 1.5)  # FWHM 1.5nm
    peak5 = gaussian_peak(wavelengths, 650, 1.8, 3.0)  # FWHM 3.0nm

    # 合成信号
    signal = background + peak1 + peak2 + peak3 + peak4 + peak5

    return wavelengths, signal


# 示例用法
if __name__ == "__main__":
    # 配置中文显示
    plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
    # 解决负号显示问题
    plt.rcParams['axes.unicode_minus'] = False

    # 生成测试数据
    wavelengths, signal = generate_test_signal()

    # 识别原始信号中的峰
    original_peaks = identify_peaks(wavelengths, signal)
    print("原始信号中的峰:")
    for peak in original_peaks:
        status = "窄峰(将被去除)" if peak['is_narrow'] else "宽峰(将被保留)"
        print(f"波长: {peak['wavelength']:.1f}nm, 半高宽: {peak['fwhm']:.2f}nm, {status}")

    # 应用滤波去除所有半高宽小于1nm的峰
    filtered_wl, filtered_signal = remove_narrow_peaks(wavelengths, signal, max_fwhm=1.0)

    # 识别滤波后信号中的峰
    filtered_peaks = identify_peaks(filtered_wl, filtered_signal)
    print("\n滤波后信号中的峰:")
    for peak in filtered_peaks:
        print(f"波长: {peak['wavelength']:.1f}nm, 半高宽: {peak['fwhm']:.2f}nm")

    # 绘制结果
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(wavelengths, signal, label='原始信号')
    # 标记窄峰
    for peak in original_peaks:
        if peak['is_narrow']:
            plt.axvline(x=peak['wavelength'], color='r', linestyle='--', alpha=0.5)
    plt.title('原始信号（红色虚线标记窄峰）')
    plt.xlabel('波长 (nm)')
    plt.ylabel('信号强度')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(filtered_wl, filtered_signal, label='滤波后信号', color='g')
    plt.title('去除半高宽小于1nm的峰后的信号')
    plt.xlabel('波长 (nm)')
    plt.ylabel('信号强度')
    plt.legend()

    plt.tight_layout()
    plt.show()

    # 绘制频谱图
    plt.figure(figsize=(12, 6))
    n = len(signal)
    dw = np.mean(np.diff(wavelengths))
    yf = np.fft.fft(signal)
    yf_filtered = np.fft.fft(filtered_signal)
    xf = np.fft.fftfreq(n, dw)[:n // 2]

    plt.plot(xf, 2.0 / n * np.abs(yf[:n // 2]), label='原始信号频谱')
    plt.plot(xf, 2.0 / n * np.abs(yf_filtered[:n // 2]), label='滤波后信号频谱')
    plt.axvline(x=1 / (2 * np.pi * (1.0 / (2 * np.sqrt(2 * np.log(2))))),
                color='r', linestyle='--', label='1nm半高宽对应的频率阈值')
    plt.title('信号频谱对比')
    plt.xlabel('空间频率 (1/nm)')
    plt.ylabel('振幅')
    plt.xlim(0, 0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()
