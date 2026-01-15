import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from tifffile import transpose_axes

from src.general.proc.ProcTrack import *
from figure_setting import *
from src.my_style.my_color import MyColor

def fit_stats(ax, counts, bins, x_hist=None, sigma=20, text_x=0, text_y=0.9, color="black", decimal=2, ha="left"):
    try:
        bin_centers = (bins[0:-1] + bins[1::]) / 2
        A = np.max(counts)
        x0 = bin_centers[np.argmax(counts)]
        p0 = [A, x0, sigma]
        popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=p0)
        if x_hist is None:
            x_hist = np.arange(bins[0], bins[-1], 0.001)
        fitted_curve = gaussian(x_hist, *popt)
        ax.plot(x_hist, fitted_curve, '-', color=color)

        text_content = f"Center:{popt[1]:.{decimal}f}  sigma:{popt[2]:.{decimal}f}"
        ax.text(
            x=text_x,
            y=text_y,
            s=text_content,
            fontsize=16,  # 字体大小（关键）
            ha=ha,  # 水平右对齐（避免文本超出图像）
            va='top',  # 垂直上对齐
            color=color,  # 文本颜色
            weight='bold',  # 加粗（可选）
            transform = ax.transAxes
        )
    except:
        pass

colors = [
    "#000000",  # 纯黑
    "#FF0000",  # 正红
    "#00FF00",  # 正绿
    "#0000FF",  # 正蓝
    "#FFFF00",  # 明黄
    "#00FFFF",  # 青色
    "#800080",  # 紫色
    "#FFA500",  # 橙色
    "#808080",  # 深灰
    "#FF69B4",  # 粉色
    "#A52A2A",  # 棕色
    "#228B22"  # 森林绿
]

filepaths = [
             r"D:\ExpData\NP_scattering_Dispersion\ZZS_65nm_AuNConSi_20251216\Images\before_achro_Statics_s1-s2.npz",  #  old achro-before
             r"D:\ExpData\NP_scattering_Dispersion\ZZS_65nm_AuNConSi_20251216\Images\after_achro_Statics_s1-s2.npz",  #  old achro-after
             r"D:\ExpData\NP_scattering_Dispersion\ZZS_65nm_AuNConSi_20251225\Images\after_achro_Statics_s1-s2.npz",  # new achro-after
             r"D:\ExpData\NP_scattering_Dispersion\ZZS_AuNC_TDBC_20251225\Images\1TDBC-1\after_achro_Statics_s1-s2.npz",  # new achro-after-1TDBC-1
             r"D:\ExpData\NP_scattering_Dispersion\ZZS_AuNC_TDBC_20251225\Images\1TDBC-2\after_achro_Statics_s1-s2.npz",  # new achro-after-1TDBC-2
             r"D:\ExpData\NP_scattering_Dispersion\ZZS_AuNC_TDBC_20251225\Images\2TDBC\after_achro_Statics_s1-s2.npz",  # new achro-after-2TDBC
             ]
type_colors = ["blue", "red", "red", "red", "red", "red"]

save_path = r"D:\ExpData\NP_scattering_Dispersion\Total"

p0_linear = [0.05, -10]
bounds_linear = [[0, -50],
                 [0.2, 0]]

wav_range = [450, 900]
fit_section = [[500, 656.3], [656.3, 730]]

section_colors = ["#0E8585", "#830783"]
cal_error_func = "s1-s2"
if cal_error_func == "SAM":
    escape_error = 2e-3
    error_bins = np.arange(0, 10, 0.1)
elif cal_error_func == "s1-s2":
    escape_error = 1e-6
    error_bins = np.arange(0, 6, 0.05)
elif cal_error_func == "residual":
    escape_error = 1e-5
    # error_bins = np.arange(0, 6 + 0.3, 0.3)
recon_bins = np.arange(0, 23, 0.5)

if_import_data = True

"""处理图片"""
fig = plt.figure(figsize=(12 * 3, 8 * 6), dpi=200)
axes = [[[],[],[]] for i in range(6)]

for i in range(6):
    if i == 0:
        axes[i][0] = fig.add_subplot(6, 3, 1+3*i)  # Fitted Slope
        axes[i][1] = fig.add_subplot(6, 3, 2+3*i)  # Recon. tau
        axes[i][2] = fig.add_subplot(6, 3, 3+3*i)  # Recon. Time
    else:
        axes[i][0] = fig.add_subplot(6, 3, 1 + 3 * i, sharex=axes[0][0])  # Fitted Slope
        axes[i][1] = fig.add_subplot(6, 3, 2 + 3 * i, sharex=axes[0][1])  # Recon. tau
        axes[i][2] = fig.add_subplot(6, 3, 3 + 3 * i, sharex=axes[0][2])  # Recon. Time

for iType, filepath in enumerate(filepaths):

    """导入结果"""
    if if_import_data:
        loadpath = os.path.join(filepath)
        with np.load(loadpath) as f:
            wav_maxz_popts_type = f["wav_maxz_popts_type"]
            iters_error_popts_type = f["iters_error_popts_type"]
            reconstruct_times_type = f["reconstruct_times_type"]

    """Tile结束"""
    "统计斜率"
    wav_maxz_fit_slopes = np.array(wav_maxz_popts_type)[:, :, 0]  # 所有tile&particle, 所有section的slope

    step = 0.001
    ax = axes[iType][0]
    this_slopes = wav_maxz_fit_slopes[:, :]
    bins_start = np.min(this_slopes)
    bins_end = np.max(this_slopes)
    ratio = (bins_end - bins_start) * 0.05
    x_hist = np.arange(bins_start - ratio, bins_end + ratio, 0.0001)
    for iSection in range(2):
        slopes = np.array(wav_maxz_fit_slopes[:, iSection])

        "拟合直线"
        x1 = fit_section[iSection][0]
        x2 = fit_section[iSection][1]

        "Tile中所有斜率的统计"
        bin_min = np.min(slopes)  # 向下取整，保证包含最小值
        bin_max = np.max(slopes)  # 向上取整，保证包含最大值
        bins = np.arange(bin_min, bin_max + step, step)

        label = f"{int(x1)}- {int(x2)} nm"
        counts, bins, patches = ax.hist(x=slopes, bins=bins, color=section_colors[iSection], alpha=0.5, edgecolor='black', density=False, label=label)
        fit_stats(ax, counts, bins, x_hist=x_hist, sigma=0.02,
                  text_x=0.05, text_y=0.95 if iSection==0 else 0.9, color=section_colors[iSection], decimal=4)

    "统计重构速率(时间)"
    iters_error_fit_tau = np.array(iters_error_popts_type)[:, 1]
    ax = axes[iType][1]
    label = ("Before" if iType == 0 else "After") + " Correction"
    counts, bins, patches = ax.hist(x=iters_error_fit_tau, bins=error_bins,
                                     color=type_colors[iType], alpha=0.5, edgecolor='black',
                                     density=False, label=label)
    fit_stats(ax, counts, bins, sigma=3, text_x=0.95, text_y=0.95, color=type_colors[iType], ha="right")

    "统计时间"
    ax = axes[iType][2]
    label = ("Before" if iType==0 else "After") + " Correction"
    counts, bins, patches = ax.hist(x=np.array(reconstruct_times_type), bins=recon_bins,
                                     color=type_colors[iType], alpha=0.5, edgecolor='black',
                                     density=False, label=label)
    fit_stats(ax, counts, bins, sigma=5, text_x=0.95, text_y=0.95, color=type_colors[iType], ha="right")
    ax.legend(loc="best")

"""Type结束"""
for i in range(6):
    if i == 0:
        my_wav_maxz_fit_popt_stats(axes[i][0], title="Fitted Slope Statistics", title_pad=30, xlabel='')
        my_reconstrution_error_fit_popt_stats(axes[i][1], title="Recon. Convergence Time Stats", xlabel='')
        my_wav_maxz_required_time_stats(axes[i][2], title="Spectra Recon. Time Stats", xlabel='')
    else:
        if i == 5:
            my_wav_maxz_fit_popt_stats(axes[i][0], title="", title_pad=0)
            my_reconstrution_error_fit_popt_stats(axes[i][1], title="", title_pad=0)
            my_wav_maxz_required_time_stats(axes[i][2], title="", title_pad=0)
        else:
            my_wav_maxz_fit_popt_stats(axes[i][0], title="", title_pad=30, xlabel='')
            my_reconstrution_error_fit_popt_stats(axes[i][1], title="", xlabel='')
            my_wav_maxz_required_time_stats(axes[i][2], title="", xlabel='')

save_path = os.path.join(save_path, f"Statics_{cal_error_func}.png")
fig.savefig(save_path)
plt.close(fig)

# plt.show()
# input()