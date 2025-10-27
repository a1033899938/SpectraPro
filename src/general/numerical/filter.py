import numpy as np
from scipy.ndimage import median_filter
from scipy.signal import savgol_filter, find_peaks
import pywt

class SpikeRemover:
    def __init__(self):
        pass

    def remove_spikes_unified(self, wavelengths, signal, target_idx=None, max_fwhm=1.0, repair_method='median'):
        """
        统一尖峰去除方法：支持指定索引去尖峰，或自动检测窄峰去尖峰

        参数:
        wavelengths (np.ndarray): 波长数组（nm），需与信号长度一致
        signal (np.ndarray): 输入光谱信号
        target_idx (list/int, 可选): 需去除尖峰的指定索引，输入None则自动检测窄峰
        max_fwhm (float, 可选): 自动检测时的窄峰阈值（半高宽≤此值判定为尖峰），默认1.0nm
        repair_method (str, 可选): 尖峰修复方式，'median'（中值滤波）或'linear'（线性插值），默认'median'

        返回:
        np.ndarray: 去尖峰后的信号
        list: 被处理的尖峰中心索引（用于验证）
        """
        # 输入预处理：转为numpy数组并确保长度一致
        wavelengths = np.asarray(wavelengths)
        signal = np.asarray(signal)
        if len(wavelengths) != len(signal):
            raise ValueError("波长数组与信号数组长度必须一致")

        # 确保波长升序（避免后续峰检测错位）
        if not np.all(np.diff(wavelengths) >= 0):
            sorted_idx = np.argsort(wavelengths)
            wavelengths = wavelengths[sorted_idx]
            signal = signal[sorted_idx]
            # 若指定了索引，同步调整索引
            if target_idx is not None:
                target_idx = [sorted_idx.tolist().index(i) for i in target_idx if i in sorted_idx.tolist()]
            print("警告：波长未升序，已自动排序并同步调整索引（若有）")

        # 步骤1：确定需处理的尖峰中心索引
        if target_idx is not None:
            # 模式1：指定尖峰索引（支持单索引或多索引列表）
            spike_centers = [target_idx] if isinstance(target_idx, int) else target_idx
            # 过滤超出信号长度的无效索引
            spike_centers = [idx for idx in spike_centers if 0 <= idx < len(signal)]
            if not spike_centers:
                raise ValueError("指定的尖峰索引全部超出信号长度，无有效尖峰可处理")
        else:
            # 模式2：自动检测窄峰（半高宽≤max_fwhm）
            spike_centers = self._detect_narrow_peaks(wavelengths, signal, max_fwhm)
            if not spike_centers:
                print("未检测到半高宽≤{}nm的窄峰，信号无需处理".format(max_fwhm))
                return signal.copy(), []

        # 步骤2：对每个尖峰，用3倍半高宽范围做修复
        cleaned_signal = signal.copy()
        for center in spike_centers:
            # 计算当前尖峰的半高宽（FWHM）
            fwhm = self._calculate_fwhm(wavelengths, signal, center)
            # 修复窗口：尖峰中心±1.5*FWHM（总宽度3*FWHM）
            half_window_wl = 1.5 * fwhm
            # 找到窗口对应的索引范围（避免超出信号边界）
            left_wl = wavelengths[center] - half_window_wl
            right_wl = wavelengths[center] + half_window_wl
            left_idx = max(0, np.searchsorted(wavelengths, left_wl) - 1)
            right_idx = min(len(signal)-1, np.searchsorted(wavelengths, right_wl) + 1)

            # 确保窗口有效（至少包含3个点，避免滤波不稳定）
            if right_idx - left_idx < 2:
                left_idx = max(0, center - 2)
                right_idx = min(len(signal)-1, center + 2)
                print("警告：尖峰{}的3倍FWHM窗口过窄，自动调整为中心±2索引窗口".format(center))

            # 步骤3：用指定方法修复窗口内的尖峰
            if repair_method == 'median':
                # 中值滤波：用窗口内非尖峰区域的中值替换（排除中心尖峰点）
                window_data = np.concatenate([
                    cleaned_signal[left_idx:center],  # 窗口左半部分（不含中心）
                    cleaned_signal[center+1:right_idx+1]  # 窗口右半部分（不含中心）
                ])
                if len(window_data) < 1:
                    # 极端情况：窗口内只有中心尖峰，用全局中值替换
                    repair_val = np.median(cleaned_signal[np.arange(len(cleaned_signal)) != center])
                else:
                    repair_val = np.median(window_data)
                # 替换窗口内所有点（确保尖峰区域完全平滑）
                cleaned_signal[left_idx:right_idx+1] = repair_val

            elif repair_method == 'linear':
                # 线性插值：用窗口左右边界的非尖峰点做线性拟合
                # 找窗口左边界外的第一个非尖峰参考点
                left_ref_idx = left_idx - 1
                while left_ref_idx >= 0 and left_ref_idx in spike_centers:
                    left_ref_idx -= 1
                left_ref_idx = max(0, left_ref_idx)  # 若左边界外无点，用窗口左端点

                # 找窗口右边界外的第一个非尖峰参考点
                right_ref_idx = right_idx + 1
                while right_ref_idx < len(signal) and right_ref_idx in spike_centers:
                    right_ref_idx += 1
                right_ref_idx = min(len(signal)-1, right_ref_idx)  # 若右边界外无点，用窗口右端点

                # 线性插值填充窗口
                x_interp = np.arange(left_idx, right_idx+1)
                y_interp = np.interp(
                    x_interp,
                    [left_ref_idx, right_ref_idx],
                    [cleaned_signal[left_ref_idx], cleaned_signal[right_ref_idx]]
                )
                cleaned_signal[left_idx:right_idx+1] = y_interp

            else:
                raise ValueError("修复方式仅支持'median'（中值滤波）或'linear'（线性插值）")

        return cleaned_signal, spike_centers

    def _detect_narrow_peaks(self, wavelengths, signal, max_fwhm):
        """辅助函数：检测半高宽≤max_fwhm的窄峰，返回峰中心索引"""
        # 基础峰检测（最小峰高设为信号均值+1倍标准差，避免检测噪声）
        min_height = np.mean(signal) + np.std(signal)
        peaks, _ = find_peaks(signal, height=min_height)
        if not peaks.size:
            return []

        # 筛选出半高宽≤max_fwhm的窄峰
        narrow_peak_centers = []
        for peak_idx in peaks:
            fwhm = self._calculate_fwhm(wavelengths, signal, peak_idx)
            if fwhm <= max_fwhm:
                narrow_peak_centers.append(peak_idx)
        return narrow_peak_centers

    def _calculate_fwhm(self, wavelengths, signal, peak_center):
        """辅助函数：计算指定峰中心的半高宽（FWHM）"""
        peak_height = signal[peak_center]
        half_height = peak_height / 2

        # 向左找半高处的波长（从峰中心向左遍历）
        left_idx = peak_center
        while left_idx > 0 and signal[left_idx] > half_height:
            left_idx -= 1
        # 若左边界到顶仍未到半高，用左边界
        left_wl = wavelengths[left_idx] if signal[left_idx] <= half_height else wavelengths[0]

        # 向右找半高处的波长（从峰中心向右遍历）
        right_idx = peak_center
        while right_idx < len(signal)-1 and signal[right_idx] > half_height:
            right_idx += 1
        # 若右边界到顶仍未到半高，用右边界
        right_wl = wavelengths[right_idx] if signal[right_idx] <= half_height else wavelengths[-1]

        return right_wl - left_wl

    # def _calculate_fwhm(self, wavelengths, signal, peak_center):
    #     """
    #     辅助函数：精准计算指定峰中心的半高宽（FWHM）
    #     优化点：适配单点尖峰/边界峰/非单调峰，增加线性插值提升精度，补充异常处理
    #     """
    #     # 输入校验：确保峰中心在信号有效范围内
    #     if not (0 <= peak_center < len(signal)):
    #         raise ValueError(f"峰中心索引 {peak_center} 超出信号长度范围（0~{len(signal) - 1}）")
    #
    #     # 1. 获取峰高与半高阈值（处理峰高为0的极端情况）
    #     peak_height = signal[peak_center]
    #     if peak_height < 1e-10:  # 避免除以接近0的值（信号基线噪声）
    #         return 0.0  # 峰高接近0，视为无有效峰，FWHM为0
    #     half_height = peak_height / 2
    #
    #     # 2. 向左查找半高处：支持线性插值，适配非单调下降的峰左侧
    #     left_idx = peak_center
    #     # 第一步：找到左侧第一个 ≤ 半高的点（或左边界）
    #     while left_idx > 0 and signal[left_idx] > half_height:
    #         left_idx -= 1
    #     # 第二步：分情况计算精确半高波长（线性插值提升精度）
    #     if left_idx == 0:
    #         # 左边界：若边界点仍 > 半高，用左边界波长；否则直接用边界点
    #         left_wl = wavelengths[0] if signal[0] > half_height else wavelengths[left_idx]
    #     else:
    #         # 非边界：若当前点 ≤ 半高，用当前点与前一点的线性插值（补全峰左侧过渡）
    #         if signal[left_idx] <= half_height:
    #             # 插值公式：x = x1 + (y_target - y1)*(x2 - x1)/(y2 - y1)
    #             x1, y1 = wavelengths[left_idx], signal[left_idx]
    #             x2, y2 = wavelengths[left_idx + 1], signal[left_idx + 1]
    #             # 避免y1==y2（水平段）导致除0，直接取两点中点
    #             if abs(y2 - y1) < 1e-10:
    #                 left_wl = (x1 + x2) / 2
    #             else:
    #                 left_wl = x1 + (half_height - y1) * (x2 - x1) / (y2 - y1)
    #         else:
    #             # 左边界点仍 > 半高，用左边界波长
    #             left_wl = wavelengths[0]
    #
    #     # 3. 向右查找半高处：逻辑与左侧对称，适配非单调上升的峰右侧
    #     right_idx = peak_center
    #     # 第一步：找到右侧第一个 ≤ 半高的点（或右边界）
    #     while right_idx < len(signal) - 1 and signal[right_idx] > half_height:
    #         right_idx += 1
    #     # 第二步：分情况计算精确半高波长（线性插值）
    #     if right_idx == len(signal) - 1:
    #         # 右边界：若边界点仍 > 半高，用右边界波长；否则直接用边界点
    #         right_wl = wavelengths[-1] if signal[-1] > half_height else wavelengths[right_idx]
    #     else:
    #         # 非边界：若当前点 ≤ 半高，用当前点与后一点的线性插值
    #         if signal[right_idx] <= half_height:
    #             x1, y1 = wavelengths[right_idx], signal[right_idx]
    #             x2, y2 = wavelengths[right_idx - 1], signal[right_idx - 1]
    #             if abs(y2 - y1) < 1e-10:
    #                 right_wl = (x1 + x2) / 2
    #             else:
    #                 right_wl = x1 + (half_height - y1) * (x2 - x1) / (y2 - y1)
    #         else:
    #             # 右边界点仍 > 半高，用右边界波长
    #             right_wl = wavelengths[-1]
    #
    #     # 4. 确保FWHM非负（避免极端情况下插值导致的顺序反转）
    #     fwhm = max(0.0, right_wl - left_wl)
    #     return fwhm
# ---------------------- 使用示例 ----------------------

class SignalFilter:
    """
    多组信号滤波工具类：支持对多组x,y数据进行滤波，不绑定具体数据，灵活处理不同输入
    所有滤波窗口均基于x轴物理宽度（如波长、时间等），适配均匀/非均匀x数据
    """

    def __init__(self):
        """初始化滤波工具（不绑定具体数据）"""
        pass

    def _validate_input(self, x, y):
        """验证输入x,y的合法性"""
        x = np.asarray(x, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)

        if len(x) != len(y):
            raise ValueError("x和y必须长度一致")
        if not np.all(np.diff(x) >= 0):
            raise ValueError("x必须按升序排列（非降序）")
        if len(x) < 2:
            raise ValueError("输入数据点至少需要2个")
        return x, y

    def _get_window_indices(self, x, i, x_window_width):
        """辅助函数：根据x窗口宽度获取当前点的窗口索引范围"""
        half_window = x_window_width / 2
        current_x = x[i]
        window_left = current_x - half_window
        window_right = current_x + half_window

        # 查找窗口内的x索引（左闭右开）
        left_idx = np.searchsorted(x, window_left, side="left")
        right_idx = np.searchsorted(x, window_right, side="right")

        # 限制索引在有效范围内
        return max(0, left_idx), min(len(x), right_idx)

    def mean_filter(self, x, y, x_window_width):
        """
        均值滤波：基于x物理宽度的窗口均值

        参数:
        x (array-like): x轴数据（升序，物理量）
        y (array-like): 待滤波的y轴数据
        x_window_width (float): x轴上的窗口物理宽度

        返回:
        np.ndarray: 滤波后的y数据
        """
        x, y = self._validate_input(x, y)
        filtered_y = np.zeros_like(y)
        for i in range(len(x)):
            left_idx, right_idx = self._get_window_indices(x, i, x_window_width)
            window_y = y[left_idx:right_idx]
            filtered_y[i] = np.mean(window_y) if len(window_y) > 0 else y[i]
        return filtered_y

    def median_filter(self, x, y, x_window_width):
        """
        中值滤波：基于x物理宽度的窗口中值（抗脉冲噪声能力强）
        """
        x, y = self._validate_input(x, y)
        filtered_y = np.zeros_like(y)
        for i in range(len(x)):
            left_idx, right_idx = self._get_window_indices(x, i, x_window_width)
            window_y = y[left_idx:right_idx]
            # 窗口内至少2个点才做中值滤波，否则用原数据
            filtered_y[i] = np.median(window_y) if len(window_y) >= 2 else y[i]
        return filtered_y

    def gaussian_filter(self, x, y, x_window_width, sigma_ratio=0.3):
        """
        高斯滤波：基于x物理宽度的高斯加权平均（平滑效果好）
        """
        x, y = self._validate_input(x, y)
        # 计算高斯核标准差（基于x窗口宽度动态适配）
        half_window = x_window_width / 2
        sigma = sigma_ratio * half_window

        # 计算x的平均间隔，用于转换为高斯滤波的"sigma索引"
        avg_x_spacing = np.mean(np.diff(x))
        sigma_idx = sigma / avg_x_spacing  # 转换为索引空间的sigma

        # 应用高斯滤波（mode='nearest'处理边界）
        return gaussian_filter1d(y, sigma=sigma_idx, mode='nearest')

    def savgol_filter(self, x, y, x_window_width, polyorder=2):
        """
        Savitzky-Golay滤波：多项式平滑滤波（保留峰值特征好）
        """
        x, y = self._validate_input(x, y)
        # 根据x窗口宽度计算所需的窗口索引数（向上取整为奇数）
        avg_x_spacing = np.mean(np.diff(x))
        window_length = int(x_window_width / avg_x_spacing)
        window_length = max(3, window_length if window_length % 2 == 1 else window_length + 1)
        window_length = min(window_length, len(x))  # 不超过数据总长度

        # 应用Savitzky-Golay滤波
        return savgol_filter(y, window_length=window_length, polyorder=polyorder, mode='nearest')

    def apply_filter(self, x, y, filter_type, x_window_width, **kwargs):
        """
        统一接口：选择滤波类型并应用

        参数:
        x (array-like): x轴数据（升序，物理量）
        y (array-like): 待滤波的y轴数据
        filter_type (str): 滤波类型，可选 'mean'/'median'/'gaussian'/'savgol'
        x_window_width (float): x轴窗口物理宽度
       ** kwargs: 各滤波方法的额外参数（如gaussian的sigma_ratio，savgol的polyorder）

        返回:
        np.ndarray: 滤波后的y数据
        """
        filter_methods = {
            'mean': self.mean_filter,
            'median': self.median_filter,
            'gaussian': self.gaussian_filter,
            'savgol': self.savgol_filter
        }

        if filter_type not in filter_methods:
            raise ValueError(f"不支持的滤波类型：{filter_type}，可选类型：{list(filter_methods.keys())}")

        return filter_methods[filter_type](x, y, x_window_width, **kwargs)


if __name__ == '__main__':
    # 1. 生成测试数据（含波长、带尖峰的信号）
    def generate_test_spectrum(n_points=1000, n_narrow_spikes=5, noise_level=0.5):
        wavelengths = np.linspace(400, 800, n_points)  # 400-800nm波长
        # 基础信号：2个宽峰（模拟正常光谱峰）+ 噪声
        signal = 10 * np.exp(-(wavelengths-500)**2/(2*20**2)) + 8 * np.exp(-(wavelengths-650)**2/(2*30**2))
        signal += np.random.normal(0, noise_level, n_points)
        # 添加窄峰（半高宽≈0.5-0.8nm，模拟尖峰）
        spike_centers = np.random.choice(n_points, n_narrow_spikes, replace=False)
        for center in spike_centers:
            # 窄峰：宽度≈0.5nm（对应~2个索引点），高度随机
            spike_width_idx = 2
            signal[max(0, center-spike_width_idx):min(n_points, center+spike_width_idx+1)] += np.random.uniform(5, 10)
        return wavelengths, signal, spike_centers

    # 生成测试数据
    test_wl, test_signal, true_spikes = generate_test_spectrum()

    # 2. 初始化去尖峰工具并使用
    remover = SpikeRemover()

    # 模式A：自动检测窄峰（去除FWHM≤1.0nm的尖峰）
    cleaned_auto, detected_spikes = remover.remove_spikes_unified(
        wavelengths=test_wl,
        signal=test_signal,
        target_idx=None,  # 自动检测模式
        max_fwhm=1.0,
        repair_method='median'
    )
    print("自动检测并处理的尖峰中心索引：", detected_spikes)
    print("真实尖峰中心索引（供对比）：", true_spikes.tolist())

    # 模式B：指定尖峰索引（例如处理索引100和200处的尖峰）
    # cleaned_specified, handled_spikes = remover.remove_spikes_unified(
    #     wavelengths=test_wl,
    #     signal=test_signal,
    #     target_idx=[100, 200],  # 指定索引模式
    #     repair_method='linear'
    # )
    # print("指定处理的尖峰中心索引：", handled_spikes)