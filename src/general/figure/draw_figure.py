from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from src.general.figure.set_figure import *
from scipy.optimize import curve_fit
from src.general.numerical.curve_functions import *

def draw_mapping(mapping, title='', xlabel='X', ylabel='Y', colorbar_label='Intensity(cts)'):
    """
    作二维扫描图像
    :param mapping: 二维数组
    :return:
    """
    mapping_range = [mapping.shape[0], mapping.shape[1]]

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    x = range(mapping_range[0])
    y = range(mapping_range[1])
    X, Y = np.meshgrid(x, y)
    Z = mapping
    im = ax.pcolor(X, Y, np.transpose(Z), cmap='viridis')

    # 添加颜色条
    cbar = fig.colorbar(im)

    """设置figure参数"""
    set_label_and_title(ax, title=title, xlabel=xlabel, ylabel=ylabel, colorbar=cbar, colorbar_label=colorbar_label)
    set_spines(ax)
    set_tick(ax, colorbar=cbar)  # Normalized
    set_scientific_y_ticks(ax, cbar, sci_position=(3, 0))
    plt.tight_layout()

    return fig

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

def draw_cascade(ax, x, Z, bot_z=0, highlight_maximum=False, plot_maximum=False):
    """

    :param ax: matplotlib axes
    :param x: 一维数列 x（如波长）
    :param Z: 二维矩阵 Z (波长需对应Z的第二维，即len(x) = Z.shape[1])
    """
    if Z.shape[1] != len(x):
        print("error: Z.shape[0] != len(x), try transpose Z ?")
        draw_flag = 0
    else:
        y = np.arange(Z.shape[0])
        X, Y = np.meshgrid(x, y)
        draw_flag = 1

    if draw_flag == 1:
        for i in y:
            ax.plot(Y[i, :], X[i, :], Z[i, :], color=plt.cm.viridis(i / len(y)),
                     linestyle='-', linewidth=1, alpha=1)
            ax.plot(Y[i, :], X[i, :], np.zeros_like(Z[i])+bot_z, color='gray', alpha=1)

            polygon = [
                [Y[i, 0], X[i, 0], 0+bot_z],  # 左下
                [Y[i, -1], X[i, -1], 0+bot_z],  # 右下
            ]
            for j in range(len(x) - 1, -1, -1):  # 依次添加点，使得polygon成为一个完整的闭合多边形
                polygon.append([Y[i, j], X[i, j], Z[i, j]])
            ax.add_collection3d(Poly3DCollection([polygon], color=plt.cm.viridis(i / len(y)), alpha=0.5))

        if bot_z != 0:
            ax.set_zlim(bot_z, )

        # 将峰值位置连成曲线
        if highlight_maximum is True:
            # 找到每行最大值的索引
            max_indices = np.argmax(Z, axis=1)
            # 获取对应的x,y,z坐标
            max_x = x[max_indices]
            max_y = y
            max_z = Z[range(len(y)), max_indices]

            # 绘制最大值连线
            ax.plot(max_y, max_x, max_z,
                    'r-', linewidth=2, alpha=0.5,
                    label='Column Maxima')

            # 在每个最大值点添加标记
            ax.scatter(max_y, max_x, max_z,
                       c='red', s=5, alpha=0.2,
                       marker='o', edgecolors='white')

        # 将峰值的Sequence曲线画在波长最大值位置的平面上
        if plot_maximum is True:
            # 找到每行最大值的索引
            max_indices = np.argmax(Z, axis=1)
            # 找到每行的最大值
            max_z = Z[range(len(y)), max_indices]
            max_x = np.ones(np.shape(y)) * x[-1]  # 波长最大值位置

            # 绘制最大值连线
            ax.plot(y, max_x, max_z,
                    'g-', linewidth=2, alpha=0.5,
                    label='Column Maxima')

            # 在每个最大值点添加标记
            ax.scatter(y, max_x, max_z,
                       c='green', s=5, alpha=0.2,
                       marker='o', edgecolors='white')

        if highlight_maximum is True or plot_maximum is True:
            return max_z
    else:
        print("didn't draw cascade!")

if __name__ == '__main__':
    filepath = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-9\m4\PL_mapping.npy"
    data = np.load(filepath)
    draw_mapping(data, title='PL Mapping')
    plt.show()