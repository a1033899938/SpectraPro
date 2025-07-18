import numpy as np


def read_txt_by_column(file_path, delimiter='\t', skip_header=True, convert_numeric=True):
    """
    逐行读取txt文件并按列处理数据

    参数:
    file_path (str): 文件路径
    delimiter (str): 列分隔符，默认为制表符'\t'
    skip_header (bool): 是否跳过首行，默认为True
    convert_numeric (bool): 是否尝试将数据转换为数值类型，默认为True

    返回:
    list: 每列数据的列表，例如 [[col1_data], [col2_data], ...]
    """
    columns = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 跳过标题行
            if skip_header:
                next(file)

            # 逐行处理
            for line in file:
                line = line.strip()  # 去除首尾空白字符
                if not line:  # 跳过空行
                    continue

                # 按分隔符分割行
                values = line.split(delimiter)

                # 初始化列列表
                if not columns:
                    columns = [[] for _ in range(len(values))]

                # 将每个值添加到对应的列，并尝试转换为数值类型
                for i, value in enumerate(values):
                    if convert_numeric:
                        try:
                            # 尝试转换为整数
                            num = np.float64(value)
                        except Exception as e:
                            print(e)
                        columns[i].append(num)
                    else:
                        columns[i].append(value)

    except FileNotFoundError:
        print(f"错误：找不到文件 '{file_path}'")
    except PermissionError:
        print(f"错误：没有权限读取文件 '{file_path}'")
    except Exception as e:
        print(f"错误：读取文件时发生意外错误：{e}")

    return columns

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from src.general.figure import set_figure


    def the_figure(ax):
        """拟合曲线"""
        set_figure.set_label_and_title(ax, title=f'P_sample / P_afterFilter', xlabel='P_sample', ylabel='P_afterFilter')
        set_figure.set_spines(ax)
        set_figure.set_tick(ax)  # Normalized
        plt.tight_layout()


    def add_annotation(ax, x, y, text, position=None, fontsize=12, color='black', ha='center', va='center'):
        """
        在图表上添加文字标注

        参数:
        ax: matplotlib的axes对象
        x, y: 标注位置的坐标
        text: 要显示的文字内容
        position: 文字相对于标注点的位置偏移，默认为None(直接放置在标注点上)
        fontsize: 字体大小
        color: 文字颜色
        ha: 水平对齐方式 ('left', 'center', 'right')
        va: 垂直对齐方式 ('top', 'center', 'bottom')
        """
        if position:
            ax.annotate(text,
                        xy=(x, y),
                        xytext=position,
                        textcoords='offset points',
                        fontsize=fontsize,
                        color=color,
                        ha=ha,
                        va=va)
        else:
            ax.text(x, y, text, fontsize=fontsize, color=color, ha=ha, va=va)

    filepath = r"D:\ExpData\fromlab\LabInstrumentTest\PowerRatio\LaserPowerRatio-v3_20250626.txt"
    delimiter = ' '  # 请根据实际情况修改分隔符

    columns = read_txt_by_column(filepath, delimiter=' ')

    if columns:
        # 打印每列的前几个值
        for i, col in enumerate(columns):
            print(f"列 {i + 1}: {col[:]}... ({len(col)} 个值)")

    P_Sample = np.array(columns[0])
    P_afterFilter = np.array(columns[1])

    fig0 = plt.figure(figsize=(8, 6))
    ax0 = fig0.add_subplot(111)

    im = ax0.plot(P_Sample, P_afterFilter, 'o', c)

    # 对前6个点进行拟合（最后一个点脱离线形）
    x = P_Sample[:6]
    y = P_afterFilter[:6]
    popt, pcov = curve_fit(linear, x, y)
    y_fit = linear(P_Sample, *popt)

    ax0.plot(P_Sample, y_fit, '-', color='red')

    the_figure(ax0)

    # 添加拟合参数文字说明
    add_annotation(ax0,
                   # x=np.max(x) * 0.5,  # x位置在x范围的中间
                   # y=np.max(y) * 0.9,  # y位置在y范围的顶部
                   x = np.max(P_Sample) * 0.3,
                   y = np.max(y_fit) * 0.95,
                   text=f'k = {popt[0]:.2f}, b = {popt[1]:.2f}',
                   fontsize=25,
                   color='blue')

    # # 在特定点添加标注示例
    # add_annotation(ax0,
    #                x=x[0],  # 第一个数据点
    #                y=y[0],
    #                text='起始点',
    #                position=(20, 10),  # 文字偏移量
    #                fontsize=10,
    #                color='blue')
    # ax0.semilogx()
    plt.show()
