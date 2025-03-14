import os
import pprint
import matplotlib.pyplot as plt
import numpy as np
from src.general.read_file import read_file
from src.general import set_figure
from src.ui.general_methods import GeneralMethods
from src.general.save_figure import save_subfig
from src.general.sort_by_number import sort_files
import re
import pandas as pd
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import medfilt


def gaussian(x, A, mu, sigma, C):
    return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2)) + C


def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
    return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))


def find_nearest_idx(lst, target):
    # 计算每个元素与目标值的差值，返回最小值的索引
    return min(range(len(lst)), key=lambda i: abs(lst[i] - target))


"""
Note：
本代码用于
1、读取四次SHG测试的数据
    --分别是MoS2/Si, MoS2/AuFilm, AuSHIN-1/MoS2/AuFilm, AuSHIN-2/MoS2/AuFilm这三种结构四个点位的PL光谱
    --MoS2/Si是章立心测量的，.spe无法目前的脚本打开，所以先用matlab转成了.mat文件。其余三个是我测的，可以正常打开
2、读取SHG graph的（1）degree（2）intensity（3）linewidth数组
"""

"""分别读取四次数据"""
folder_paths = [r'F:\Data\SHG\20241208_SHG\800nm-2mw-step2-20s',
                r'F:\Data\SHG\20241214SHG\MoS2_Au_Step2d_2mW_20s',
                r'F:\Data\SHG\20241214SHG\AuSHIN_MoS2_Au_Step2d_2mW_20s',
                r'F:\Data\SHG\20241214SHG\AuSHIN-2_MoS2_Au_Step2d_2mW_20s']

# 图片标题
titles = [r'$\mathrm{MoS}_2/\mathrm{Si} \; \mathrm{SHG \; Spectrum}$',
          r'$\mathrm{MoS}_2/\mathrm{AuFilm} \; \mathrm{SHG \; Spectrum}$',
          r'$\mathrm{AuSHIN-1}/\mathrm{MoS}_2/\mathrm{AuFilm} \; \mathrm{SHG \; Spectrum}$',
          r'$\mathrm{AuSHIN-2}/\mathrm{MoS}_2/\mathrm{AuFilm} \; \mathrm{SHG \; Spectrum}$']

# 数组txt文件名
intensity_txt_names = ['MoS2_Si_intensity.txt',
                       'MoS2_AuFilm_intensity.txt',
                       'AuSHIN-1_MoS2_AuFilm_intensity.txt',
                       'AuSHIN-2_MoS2_AuFilm_intensity.txt']

linewidth_txt_names = ['MoS2_Si_linewidth.txt',
                       'MoS2_AuFilm_linewidth.txt',
                       'AuSHIN-1_MoS2_AuFilm_linewidth.txt',
                       'AuSHIN-2_MoS2_AuFilm_linewidth.txt']

for i, folder_path in enumerate(folder_paths):
    if i == 0:
        extensions = ['.mat']
    else:
        extensions = ['.spe']

    # 读取目录下的：文件路径、文件名，并根据文件名中的序号排序。
    file_paths, files, file_names = GeneralMethods.list_files_in_directory(folder_path, extensions)
    file_names_sorted = sort_files(file_names)
    file_paths_sorted = sort_files(file_paths)

    # 读取光谱强度、波长
    nums = []  # 文件序号
    sps = []  # 光谱强度
    for file_path, file_name in zip(file_paths_sorted, file_names_sorted):
        numbers = re.findall(r'\d+\.\d+|\d+', file_path)
        nums.append(numbers[-1])
        # 根据gui显示的二维图像，观察并取strip范围
        # 取25条strip
        if i == 0:
            strip = [187, 211]
        else:
            strip = [181, 205]
        RF = read_file(file_path, strip=strip, show_data_flag=False)
        sp = RF.data['intensity']
        wav = RF.data['wavelength']

        # 对光谱进行噪声去除
        # 设置一个阈值，用于判断数据的差异是否过大
        threshold = 100  # 当相邻点的差值大于此值时，认为是噪声
        # 计算相邻点的差值
        sp = sp.astype(float)
        """转换为更高精度的类型非常重要，否则逸出了，根本得不到正确的diff结果"""
        diff = sp[1:-1] - sp[0:-2]  # 计算相邻点的绝对差值
        # 判断哪些点的差值大于阈值，并去除它们
        sp_filtered = sp.astype(float)
        for k in range(1, len(diff) - 1):
            if diff[k - 1] > threshold or diff[k] > threshold:
                sp_filtered[k] = np.nan  # 将噪声点替换为NaN
        # 使用插值填充 NaN 值
        nan_indices = np.isnan(sp_filtered)
        sp_filtered[nan_indices] = interp1d(np.where(~nan_indices)[0], sp_filtered[~nan_indices], kind='linear',
                                            fill_value='extrapolate')(np.where(nan_indices)[0])
        sps.append(sp_filtered)

    """拟合曲线，并获取强度和线宽数组"""
    peak_intensity = []
    peak_linewidth = []
    failed_fits = 0
    for num, sp in zip(nums, sps):
        fig = plt.figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(wav, sp)
        try:
            popt, pcov = curve_fit(gaussian, wav, sp, p0=[200, 400, 5, 0], maxfev=5000)
            A_fit, mu_fit, sigma_fit, C = popt
            print(num)
            print(popt)
            y_fit = gaussian(wav, *popt)
            ax.plot(wav, y_fit)
            if A_fit <= 0 or sigma_fit > 100:
                peak_intensity.append(0)
                peak_linewidth.append(0)
            else:
                if sigma_fit < 0:
                    peak_linewidth.append(-sigma_fit)
                else:
                    peak_linewidth.append(sigma_fit)
                peak_intensity.append(A_fit)
        except Exception as e:
            print(f"拟合失败，文件：{file_name}, 错误：{e}")
            failed_fits += 1
            peak_intensity.append(np.nan)  # 存储一个 NaN 值，保持列表长度一致
            peak_linewidth.append(np.nan)
            pass

        # 图片设置
        title = titles[i]
        set_figure.set_label_and_title(ax, title=title, xlabel='Wavelength(nm)', ylabel='Intensity(counts)',
                                       label_fontsize=25, title_fontsize=25,
                                       label_font_family='Times New Roman', title_font_family='Times New Roman',
                                       label_fontweight='bold', title_fontweight='bold',
                                       label_pad=8, title_pad=15)
        set_figure.set_spines(ax, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
        set_figure.set_tick(ax, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                            linewidth=3, tick_pad=5, direction='in'
                            )

        save_filename = os.path.join(folder_path, num + '.png')
        save_subfig(fig, save_filename)
        print('Save file: ' + save_filename)
        plt.close(fig)

    """强度、线宽数据去噪声"""
    # 强度
    mean_intensity = np.mean(peak_intensity)  # 计算 diff 的均值
    mean_linewidth = np.mean(peak_linewidth)  # 计算 diff 的均值
    threshold_intensity = 5 * mean_intensity  # 计算均值的五倍
    threshold_linewidth = 5 * mean_linewidth  # 计算均值的五倍
    peak_intensity = np.array(peak_intensity).astype(float)
    peak_linewidth = np.array(peak_linewidth).astype(float)
    nums = np.array(nums).astype(float)
    peak_intensity[peak_intensity > threshold_intensity] = np.nan
    peak_linewidth[peak_linewidth > threshold_linewidth] = np.nan
    nan_indices_intensity = np.isnan(peak_intensity)  # 取出nan值索引
    nan_indices_linewidth = np.isnan(peak_linewidth)  # 取出nan值索引
    nan_indices = np.union1d(nan_indices_intensity, nan_indices_linewidth)
    peak_intensity = np.delete(peak_intensity, np.where(nan_indices)[0])
    peak_linewidth = np.delete(peak_linewidth, np.where(nan_indices)[0])
    nums = np.delete(nums, np.where(nan_indices)[0])

    """作角度-强度极图"""
    nums = angles_deg = pd.to_numeric(nums)
    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111, polar=True)
    # 角度转幅度
    nums = np.radians(nums)
    nums = nums * 4
    print(nums)
    print(peak_intensity)
    ax.plot(nums, peak_intensity)
    # 保存强度数组
    np.savetxt(intensity_txt_names[i], np.column_stack((nums, peak_intensity)), header="X, Y", delimiter='\t')
    # 保存图片
    save_filename = os.path.join(folder_path, intensity_txt_names[i].replace('.txt', '.png'))
    save_subfig(fig, save_filename)

    """作角度-线宽极图"""
    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(nums, peak_linewidth)
    # 保存线宽数组
    np.savetxt(linewidth_txt_names[i], np.column_stack((nums, peak_linewidth)), header="X, Y",
               delimiter='\t')
    # 保存图片
    save_filename = os.path.join(folder_path, linewidth_txt_names[i].replace('.txt', '.png'))
    save_subfig(fig, save_filename)

    print(f"共有 {failed_fits} 次拟合失败。")
plt.show()
