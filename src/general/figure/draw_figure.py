import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.optimize import curve_fit

from src.general.figure.set_figure import *
from src.general.numerical.curve_functions import *
from src.general.numerical.edit_data import *

def draw_mapping(mapping, fig=None, ax=None, colormap='viridis', x: np.ndarray=None, y: np.ndarray=None):
    """
    作二维扫描图像
    :param mapping: 二维数组
    :return:
    """
    mapping_range = [mapping.shape[0], mapping.shape[1]]

    if x is None or y is None:
        print("默认形式为xy数组")
        x = range(mapping_range[0])
        y = range(mapping_range[1])
    else:
        print("以给定的x, y作为xy轴")
        if len(x) != mapping_range[0] or len(y) != mapping_range[1]:
            raise ValueError(f"数组不匹配. x, y, mapping的尺寸分别为: {len(x)}, {len(y)}, {mapping_range}")

    if fig is None or ax is None:
        print("fig或ax为None, 新建fig和ax以作图")
        fig = plt.figure(figsize=(12*1.2, 8), dpi=100)
        ax = fig.add_subplot(111)

    X, Y = np.meshgrid(x, y)
    Z = mapping
    im = ax.pcolor(X, Y, np.transpose(Z), cmap=colormap)

    # 添加颜色条
    cbar = fig.colorbar(im)

    return fig, ax, cbar

def draw_cascade_3d(x, y, Z, ax: plt.axis, normalize=False, connect_peaks: bool=False, find_peak_args: dict=None, draw_polygon: bool=True, alpha: float=0.5):
    """
    作三维瀑布图
    :param x: 单副图的自变量
    :param y: 不同图之间的关系参数阵列，长度为图的数量（如时间，range(len(Z.shape[]))）
    :param Z: 函数值矩阵，为单副图因变量的组合
    :param ax:
    :param alpha:
    :param draw_polygon:
    :param find_peak_args:
    :param connect_peaks:
    :param normalize:
    :return:
    """

    X, Y = np.meshgrid(x, y)

    # 存储每条曲线的最大值点
    peak_x = []
    peak_y = []
    peak_z = []

    # 设置find_peaks的默认参数
    if find_peak_args is None:
        find_peak_args = {'height': 0, 'prominence': 0.1}
        # height: 设置峰值的最小高度阈值。只有高度大于或等于该值的峰值才会被检测到。
        # prominence: 设置峰值的最小 “突出度”（prominence）。突出度表示峰值与其两侧最近的 “山谷”（局部最小值）之间的高度差。

    if normalize is True:
        Z = Z / np.max(Z)

    lines_num = len(y)
    for i in range(lines_num):
        ax.plot(Y[i], X[i], Z[i], color=plt.cm.viridis(i / lines_num),
                 linestyle='-', linewidth=1, alpha=1)

        # 绘制基线
        ax.plot(Y[i], X[i], np.zeros_like(Z[i]), color='gray', alpha=1)

        if draw_polygon:
            polygon = [
                [Y[i, 0], X[i, 0], 0],  # 左下
                [Y[i, -1], X[i, -1], 0],  # 右下
            ]
            for j in range(len(x) - 1, -1, -1):  # 依次添加点，使得polygon成为一个完整的闭合多边形
                polygon.append([Y[i, j], X[i, j], Z[i, j]])
            ax.add_collection3d(Poly3DCollection([polygon], color=plt.cm.viridis(i / lines_num), alpha=alpha))

        # 如果需要，连接各曲线的最大值点
        if connect_peaks:
            # 找出最大值点
            peaks, _ = find_peaks(Z[i] / np.max(Z[i]), **find_peak_args)
            peak_x.append(X[i][peaks[0]])
            peak_y.append(Y[i][peaks[0]])
            peak_z.append(Z[i][peaks[0]])
            ax.plot(peak_y, peak_x, peak_z, 'ro-', linewidth=1, markersize=3, markeredgecolor='r', markerfacecolor='none', label='连接各曲线最大值')

def draw_cascade_2d(x: np.ndarray, ys: np.ndarray, *args, les=None, space=0.1, axis=0, figsize=None):
    if axis == 0:
        pass
    elif axis == 1:
        ys = np.transpose(ys)
    else:
        print("error axis")

    n_subplots = np.shape(ys)[0]

    if figsize is None:
        figsize = (6, 2*n_subplots)

    fig, axes = plt.subplots(
        n_subplots, ncols=1,  # 垂直排列
        sharex=True,  # 共享 X 轴
        figsize=figsize,  # 画布尺寸（可调整）
        gridspec_kw={"hspace": space}  # 减小子图间距
    )

    # 待完成：可通过传入fig来作图
    # # 1. 创建画布
    # fig = plt.figure(figsize=figsize)
    #
    # # 2. 逐个添加子图并存储到列表中（确保可迭代）
    # axes = []
    # for i in range(n_subplots):
    #     # 子图编号从1开始，格式为"总行数, 总列数, 当前索引"
    #     ax = fig.add_subplot(n_subplots, 1, i + 1)  # 垂直排列（n行1列）
    #     axes.append(ax)
    #
    # # 3. 共享X轴设置
    # for ax in axes[:-1]:  # 除了最后一个子图，隐藏其他子图的x轴刻度
    #     plt.setp(ax.get_xticklabels(), visible=False)
    #
    # # 4. 调整子图间距（替代gridspec_kw）
    # fig.subplots_adjust(hspace=space)
    #
    # # 5. 现在可以像之前一样迭代axes了
    # for i, ax in enumerate(axes):
    #     ax.plot([1, 2, 3], [i + 1, i + 2, i + 3])  # 示例绘图
    #     ax.set_title(f"子图 {i + 1}")

    # 3. 逐个子图绘制数据
    for i, ax in enumerate(axes):
        print(i)
        y = ys[i, :]
        ax.plot(x, y, color="black", linewidth=1.2)  # 绘制谱线
        if args is not None:
            for arg in args:
                zs = arg
                z = zs[i, :]
                ax.plot(x, z, color="red", linewidth=1.2)


        if les is not None:
            # label
            ax.text(
                0.03, 0.85, f"{les[i]}",  # 位置：左上方
                transform=ax.transAxes,  # 基于子图的相对坐标
                fontsize=10,
                fontweight="bold"
            )

        # 隐藏顶部/右侧边框，简化样式
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        # ax.set_yticks([])  # 隐藏 Y 轴刻度（若需保留可自定义）

    # 4. 统一设置 X 轴（仅最下方子图显示 X 轴）
    # axes[-1].set_xlabel("Photon Energy (eV)", fontsize=12)  # X 轴标题
    # axes[-1].set_xlim(1.3, 2.1)  # 统一 X 轴范围

    # 5. 手动标注特征峰
    # 示例：在第一个子图标注 IX 峰
    # axes[0].scatter(1.4, generate_spectrum(np.array([1.4]), 293),
    #                 color="red", label="IX", zorder=5)
    # axes[0].text(1.42, 10, "IX", fontsize=9, color="red")

    # 6. 显示图像
    plt.tight_layout()
    return fig, axes

def draw_cascade_group_2d(xs_group: list, ys_group: list, les_group=None, les_sg=None, colors_group=None, space=0.1, axis=0, figsize=None): # (6, 10)

    if len(xs_group) != len(ys_group):
        raise (ValueError("xs_group and ys_group must have same length"))
        return

    n_subplots = len(ys_group)

    if figsize is None:
        figsize = (6, 2*n_subplots)

    fig, axes = plt.subplots(
        n_subplots, ncols=1,  # 垂直排列
        sharex=True,  # 共享 X 轴
        figsize=figsize,  # 画布尺寸（可调整）
        gridspec_kw={"hspace": space}  # 减小子图间距
    )

    # 3. 逐个子图绘制数据
    for i, ax in enumerate(axes):
        xs = xs_group[i]
        ys = ys_group[i]
        les = les_group[i]
        colors = colors_group[i]
        if np.shape(xs) != np.shape(ys):
            raise (ValueError("xs and ys must have same shape"))

        if xs.ndim == 1:
            x = xs
            y = ys
            gh = ax.plot(x, y, color="black", linewidth=1.2, label=les)  # 绘制谱线
            if colors is not None:
                gh[0].set_color(colors[0])
        else:
            for j in range(np.shape(xs)[0]):
                x = xs[j, :]
                y = ys[j, :]
                gh = ax.plot(x, y, color="black", linewidth=1.2, label=les[j])  # 绘制谱线
                if colors is not None:
                    gh[0].set_color(colors[j])

        if les_sg is not None:
            # label
            ax.text(
                0.03, 0.85, f"{les_sg[i]}",  # 位置：左上方
                transform=ax.transAxes,  # 基于子图的相对坐标
                fontsize=10,
                fontweight="bold"
            )

        # 隐藏顶部/右侧边框，简化样式
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    return fig, axes

def peak_component_evolution(wav, sps, peak_wavs, ax, axis=0):
    try:
        if axis == 0:
            pass
        elif axis == 1:
            sps = np.transpose(sps)
        else:
            print("axis error")

        lines = np.shape(sps)[0]  # 光谱条数

        peaks = np.zeros([len(peak_wavs), lines])  # 峰数
        for i in range(lines):
            sp = sps[i, :]
            for j, peak_wav in enumerate(peak_wavs):
                peak = find_val_idx(x=wav, y=sp, x1=peak_wav)
                peaks[j, i] = peak

        for j, peak_wav in enumerate(peak_wavs):
            ax.plot(range(lines), peaks[j, :], label=peak_wav)
    except Exception as e:
        print(e)
    return peaks

def draw_power_dependent(powers, ints, ax=None):
    bounds = ([0, 0],
              [np.Inf, np.Inf])
    popt, pcov = curve_fit(power_saturation, powers, ints, bounds=bounds)
    P_sat, I_inf = popt
    print('P_sat:', P_sat)
    print('I_inf:', I_inf)
    ints_fit = power_saturation(powers, *popt)
    if ax is not None:
        ax.plot(powers, ints_fit, '-', color='#d62728', linewidth=2)

if __name__ == '__main__':
    # 测试draw_mapping
    # from src.my_style.my_figure import *
    # mapping = np.random.random([100, 100])
    # x = np.linspace(200, 1000, 100)
    # y = np.linspace(5, 10, 100)
    # fig, ax, cbar = draw_mapping(mapping, x=x, y=y, colormap='coolwarm')
    # the_mapping(ax, cbar=cbar)
    # plt.show()


    # filepath = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-9\m4\PL_mapping.npy"
    # data = np.load(filepath)
    # draw_mapping(data, title='PL Mapping')
    # plt.show()
    pass