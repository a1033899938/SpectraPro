import numpy as np
import re  # 添加正则表达式模块
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import ticker
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FixedLocator, FixedFormatter, NullFormatter
from mpl_toolkits.mplot3d import Axes3D


def set_label_and_title(ax, mode='2d', colorbar=None,
                        title='default title', xlabel='Wavelength(nm)', ylabel='Intensity(cts)', zlabel='Intensity(cts)', colorbar_label='colorbar_label',
                        title_fontsize=32, label_fontsize=30, colorbar_fontsize=30,
                        title_font_family='Times New Roman', label_font_family='Times New Roman', colorbar_font_family='Times New Roman',
                        title_fontweight='bold', label_fontweight='bold', colorbar_fontweight='bold',
                        title_pad=17, x_label_pad=15, y_label_pad=15, z_label_pad=15, colorbar_label_pad=25,
                        x_label_position=None, y_label_position=None, z_label_position=None, colorbar_position=None,
                        axis_order=(0, 1, 2),
                        xlabel_rotation=None, ylabel_rotation=None, zlabel_rotation=None, colorbar_rotation=90,
                        title_ha='center', title_va='center',
                        xlabel_ha='center', ylabel_ha='center', zlabel_ha='center', colorbar_ha='center',
                        xlabel_va='center', ylabel_va='center', zlabel_va='center', colorbar_va='center'):
    """
    设置标题和标签的参数
    :param ax: axis
    :param mode: 2d or 3d
    :param title:
    :param xlabel:
    :param ylabel:
    :param zlabel:
    :param title_fontsize: 字体大小
    :param label_fontsize:
    :param title_font_family: 字体类型
    :param label_font_family:
    :param title_fontweight: 字体粗细
    :param label_fontweight:
    :param title_pad: 字体与图框的距离
    :param label_pad:
    :param axis_order: 数值越小，轴的显示优先级越高。
                        优先级最高的轴占据“左侧”位置。
                        次优先级轴占据“右侧”位置。
                        最低优先级轴默认在“底部”。常见：(1, 2, 0)将z轴移到坐标
    :param xlabel_rotation: 标签角度（默认不一定是零）
    :param ylabel_rotation:
    :param zlabel_rotation:
    :param title_ha: 横向位置
    :param title_va: 纵向位置
    :param xlabel_ha:
    :param ylabel_ha:
    :param zlabel_ha:
    :param xlabel_va:
    :param ylabel_va:
    :param zlabel_va:
    :param colorbar_rotation: colorbar标签旋转角度
    :param colorbar_ha: colorbar标签水平对齐方式
    :param colorbar_va: colorbar标签垂直对齐方式
    :return:
    """
    try:
        label_font_dict = dict(fontsize=label_fontsize,
                               color='k',
                               family=label_font_family,
                               style='normal',
                               )
        title_font_dict = dict(fontsize=title_fontsize,
                               color='k',
                               family=title_font_family,
                               weight=title_fontweight,
                               style='normal',
                               )
        colorbar_font_dict = dict(fontsize=colorbar_fontsize,
                                  color='k',
                                  family=colorbar_font_family,
                                  weight=colorbar_fontweight,
                                  style='normal',
                                  )
        ax.set_xlabel(xlabel, fontdict=label_font_dict, weight=label_fontweight, labelpad=x_label_pad, picker=True, ha=xlabel_ha, va=xlabel_va)
        ax.set_ylabel(ylabel, fontdict=label_font_dict, weight=label_fontweight, labelpad=y_label_pad, picker=True, ha=ylabel_ha, va=ylabel_va)
        if mode == '3d':
            ax.set_zlabel(zlabel, fontdict=label_font_dict, weight=label_fontweight, labelpad=z_label_pad, picker=True, ha=zlabel_ha, va=zlabel_va)
            # ax.zaxis._axinfo['juggled'] = axis_order

        if xlabel_rotation is not None:
            ax.xaxis.set_rotate_label(False)
            xlabel = ax.xaxis.get_label()
            xlabel.set_rotation(xlabel_rotation)
        if ylabel_rotation is not None:
            ax.yaxis.set_rotate_label(False)
            ylabel = ax.yaxis.get_label()
            ylabel.set_rotation(ylabel_rotation)
        if zlabel_rotation is not None:
            ax.zaxis.set_rotate_label(False)
            zlabel = ax.zaxis.get_label()
            zlabel.set_rotation(zlabel_rotation)

        if x_label_position is not None:
            ax.xaxis.get_label().set_position(x_label_position)
        if y_label_position is not None:
            ax.yaxis.get_label().set_position(y_label_position)
        if z_label_position is not None:
            ax.zaxis.get_label().set_position(z_label_position)
        if colorbar_position is not None:
            ax.colorbar.set_position(colorbar_position)

        ax.set_title(title, fontdict=title_font_dict, weight=title_fontweight, pad=title_pad, picker=True, ha=title_ha, va=title_va)

        # 新增：完善colorbar设置
        if colorbar is not None:
            # 设置colorbar标签
            colorbar.set_label(
                colorbar_label,
                fontdict=colorbar_font_dict,
                weight=colorbar_fontweight,
                labelpad=colorbar_label_pad,
                rotation=colorbar_rotation,
                ha=colorbar_ha,
                va=colorbar_va
            )

            # 设置colorbar刻度字体
            for tick in colorbar.ax.get_yticklabels() if colorbar.orientation == 'vertical' else colorbar.ax.get_xticklabels():
                tick.set_family(label_font_family)
                tick.set_size(label_fontsize)

    except Exception as e:
        print(f"Error save_figure.set_label_and_title:\n  |--> {e}")


"""设置刻度的参数"""
def set_tick(ax, mode='2d', colorbar=None,
             xbins=10, ybins=10, zbins = 10, show_xlabel_every_ticks=None, show_ylabel_every_ticks=None, show_zlabel_every_ticks=None,
             hide_tick=None, hide_tick_label=None,
             fontsize=20, fontweight='bold',
             linewidth=3, linelength=7, direction='in',
             ticks_xlabel_pad=5, ticks_ylabel_pad=5, ticks_zlabel_pad=5,
             ticks_xlabel=None, ticks_ylabel=None, ticks_zlabel=None,
             change_ticks_xlabel=None, change_ticks_ylabel=None, change_ticks_zlabel=None,
             ticks_xlabel_rotation=None, ticks_ylabel_rotation=None, ticks_zlabel_rotation=None,
             colorbar_ticks=None, colorbar_ticklabels=None, colorbar_ticklabels_rotation=None,
             colorbar_fontsize=25, colorbar_fontweight=None, colorbar_linewidth=None, colorbar_linelength=None,
             xaxis_use_log_scale=False, yaxis_use_log_scale=False, zaxis_use_log_scale=False):
    """
    :param ax: 目标坐标轴
    :param mode: 2d or 3d
    :param colorbar: colorbar对象(如果有)
    :param xbins: x轴的最大刻度数
    :param ybins: ...
    :param zbins: ...
    :param show_label_every_ticks: 每几个刻度显示一个标签（如[2, 3, _]表示x轴每2个刻度一个标签，y轴每2个刻度一个标签，）
    :param hide_tick: 需隐藏的刻度（如['x', 'z']）
    :param hide_tick_label: 需隐藏的刻度标签
    :param fontsize: 刻度字体大小
    :param fontweight: 刻度字体粗细
    :param linewidth: 刻度线宽
    :param linelength: 刻度长度
    :param direction: 刻度方向
    :param ticklabel_pad: 刻度文本距离（距刻度）
    :param ticks_xlabel: 刻度文本(与xbins冲突，这个优先级高)
    :param ticks_ylabel:
    :param ticks_zlabel:
    :param change_ticks_xlabel: 修改实际要显示的刻度标签
    :param change_ticks_ylabel:
    :param change_ticks_zlabel:
    :param ticks_xlabel_rotation: 刻度标签的角度（默认不一定是0）
    :param ticks_ylabel_rotation:
    :param ticks_zlabel_rotation:
    :param colorbar_ticks: colorbar刻度位置
    :param colorbar_ticklabels: colorbar刻度标签
    :param colorbar_ticklabels_rotation: colorbar刻度标签旋转角度
    :param colorbar_fontsize: colorbar刻度字体大小
    :param colorbar_fontweight: colorbar刻度字体粗细
    :param colorbar_linewidth: colorbar刻度线宽
    :param colorbar_linelength: colorbar刻度线长度
    :return:
    """

    try:
        if xbins != 0:
            ax.xaxis.set_major_locator(MaxNLocator(nbins=xbins))
        if ybins != 0:
            ax.yaxis.set_major_locator(MaxNLocator(nbins=ybins))

        # 主刻度设置
        ax.tick_params(
            axis='both',
            which='major',  # 指定主刻度
            labelsize=fontsize,
            width=linewidth,
            length=linelength,  # 主刻度长度，用传入的 linelength
            direction=direction
        )
        # 次刻度设置
        ax.tick_params(
            axis='both',
            which='minor',  # 指定次刻度
            direction='in',
            width=linewidth,  # 可根据需求调整次刻度线宽
            length=linelength*0.66  # 次刻度长度，设置一个比主刻度短的值，比如这里写死为 4，也可改为参数传入
        )

        # ax.tick_params(axis='both', labelsize=fontsize, width=linewidth, length=linelength, direction=direction)
        # ax.tick_params(axis='both', which='minor', direction='in', width=1.5, length=4)
        # # ax.tick_params(axis='both', which='minor')

        ax.xaxis.set_tick_params(pad=ticks_xlabel_pad)
        ax.yaxis.set_tick_params(pad=ticks_ylabel_pad)

        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontweight(fontweight)

        # 设置刻度范围
        if ticks_xlabel is not None:
            ax.xaxis.set_ticks(ticks_xlabel)
        if ticks_ylabel is not None:
            ax.yaxis.set_ticks(ticks_ylabel)

        # 修改刻度文本
        if change_ticks_xlabel is not None:
            ax.set_xticklabels(change_ticks_xlabel)
        if change_ticks_ylabel is not None:
            ax.set_yticklabels(change_ticks_ylabel)

        # if show_xlabel_every_ticks:
        #     # 打印默认的 Locator 和 Formatter 类型
        #     ticks = ax.get_xticks()
        #     tickslabels = ax.get_xticklabels()
        #     ax.xaxis.set_major_locator(FixedLocator(ticks))  # 固定刻度位置
        #     new_labels = [label.get_text() if i % show_xlabel_every_ticks == 0 else "" for i, label in enumerate(tickslabels)]
        #     ax.set_xticklabels(new_labels)
        #
        # if show_ylabel_every_ticks:
        #     # 打印默认的 Locator 和 Formatter 类型
        #     ticks = ax.get_yticks()
        #     tickslabels = ax.get_yticklabels()
        #     ax.yaxis.set_major_locator(FixedLocator(ticks))  # 固定刻度位置
        #     new_labels = [label.get_text() if i % show_ylabel_every_ticks == 0 else "" for i, label in enumerate(tickslabels)]
        #     ax.set_yticklabels(new_labels)

        # 替换原有的 show_xlabel_every_ticks 和 show_ylabel_every_ticks 逻辑
        if show_xlabel_every_ticks:
            ticks = ax.get_xticks()
            tickslabels = ax.get_xticklabels()

            ax.xaxis.set_major_locator(FixedLocator(ticks))
            ax.xaxis.set_major_formatter(FixedFormatter(ax.get_xticklabels()))
            ax.set_xticklabels(tickslabels)

            lim = ax.get_xlim()
            valid_positions = [tick for tick in ticks if lim[0] <= tick <= lim[1]]

            # 计算主刻度间隔（假设均匀分布，取第一个间隔作为基准）
            delta = valid_positions[1] - valid_positions[0]

            # 次刻度间隔 = 主刻度间隔 / (n + 1)
            minor_interval = delta / show_xlabel_every_ticks

            ax.xaxis.set_minor_locator(MultipleLocator(base=minor_interval))
            ax.xaxis.set_minor_formatter(NullFormatter())

        if show_ylabel_every_ticks:
            ticks = ax.get_yticks()
            tickslabels = ax.get_yticklabels()

            ax.yaxis.set_major_locator(FixedLocator(ticks))
            ax.yaxis.set_major_formatter(FixedFormatter(ax.get_yticklabels()))
            ax.set_yticklabels(tickslabels)

            lim = ax.get_ylim()
            valid_positions = [tick for tick in ticks if lim[0] <= tick <= lim[1]]

            # 计算主刻度间隔（假设均匀分布，取第一个间隔作为基准）
            delta = valid_positions[1] - valid_positions[0]

            # 次刻度间隔 = 主刻度间隔 / (n + 1)
            minor_interval = delta / show_ylabel_every_ticks

            ax.yaxis.set_minor_locator(MultipleLocator(base=minor_interval))
            ax.yaxis.set_minor_formatter(NullFormatter())

        if ticks_xlabel_rotation is not None:
            ax.xaxis.set_tick_params(rotation=ticks_xlabel_rotation)
        if ticks_ylabel_rotation is not None:
            ax.yaxis.set_tick_params(rotation=ticks_ylabel_rotation)

        if hide_tick:
            # 隐藏刻度
            if 'x' in hide_tick:
                ax.set_xticks([])  # 完全隐藏

            if 'y' in hide_tick:
                ax.set_yticks([])

        if hide_tick_label:
            # 仅隐藏文本但保留刻度线
            if 'x' in hide_tick_label:
                ax.set_xticklabels([])
            if 'y' in hide_tick_label:
                ax.set_yticklabels([])

        if mode == '3d':
            ax.zaxis.set_major_locator(MaxNLocator(nbins=zbins))
            ax.zaxis.set_tick_params(pad=ticks_zlabel_pad)
            for label in ax.get_zticklabels():
                label.set_fontweight(fontweight)

            if ticks_zlabel is not None:
                ax.zaxis.set_ticks(ticks_zlabel)

            if change_ticks_zlabel is not None:
                ax.set_zticklabels(change_ticks_ylabel)

            if show_zlabel_every_ticks:
                # 打印默认的 Locator 和 Formatter 类型
                ticks = ax.get_zticks()
                tickslabels = ax.get_zticklabels()
                ax.zaxis.set_major_locator(FixedLocator(ticks))  # 固定刻度位置
                new_labels = [label.get_text() if i % show_zlabel_every_ticks == 0 else "" for i, label in enumerate(tickslabels)]
                ax.set_zticklabels(new_labels)

            if ticks_zlabel_rotation is not None:
                ax.zaxis.set_ticks(rotation=ticks_zlabel_rotation)

            if hide_tick:
                if 'z' in hide_tick:
                    ax.set_zticks([])

            if hide_tick_label:
                if 'z' in hide_tick_label:
                    ax.set_zticklabels([])

        # 新增：colorbar设置
        if colorbar is not None:
            # 设置colorbar刻度位置
            if colorbar_ticks is not None:
                colorbar.set_ticks(colorbar_ticks)

            # 设置colorbar刻度标签
            if colorbar_ticklabels is not None:
                colorbar.set_ticklabels(colorbar_ticklabels)

            # 设置colorbar刻度标签旋转角度
            if colorbar_ticklabels_rotation is not None:
                # for tick in colorbar.ax.get_yticklabels() if colorbar.orientation == 'vertical' else colorbar.ax.get_xticklabels():
                for tick in colorbar.ax.get_yticklabels():
                    tick.set_rotation(colorbar_ticklabels_rotation)

            # 设置colorbar刻度字体
            cbar_fontsize = colorbar_fontsize if colorbar_fontsize is not None else fontsize
            cbar_fontweight = colorbar_fontweight if colorbar_fontweight is not None else fontweight
            # for tick in colorbar.ax.get_yticklabels() if colorbar.orientation == 'vertical' else colorbar.ax.get_xticklabels():
            for tick in colorbar.ax.get_yticklabels():
                tick.set_size(cbar_fontsize)
                tick.set_weight(cbar_fontweight)

            # 设置colorbar刻度线
            cbar_linewidth = colorbar_linewidth if colorbar_linewidth is not None else linewidth
            cbar_linelength = colorbar_linelength if colorbar_linelength is not None else linelength
            colorbar.ax.tick_params(width=cbar_linewidth, length=cbar_linelength)

        if xaxis_use_log_scale:
            ax.set_xscale('log')
        if yaxis_use_log_scale:
            ax.set_yscale('log')
        if zaxis_use_log_scale:
            ax.set_zscale('log')
    except Exception as e:
        print(f"Error save_figure.set_tick:\n  |--> {e}")

def set_scientific_y_ticks(ax, cbar=None,
                           sci_powerlimits=(0, 0),
                           sci_sig_digits=1,
                           sci_fontsize=25,
                           sci_fontweight='bold',
                           sci_position=(0, 0)):
    # 创建原始的科学计数格式化器
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits(sci_powerlimits)
    # formatter.format = f"%.{sci_sig_digits}f"

    if cbar is None:
        ax.yaxis.set_major_formatter(formatter)
        ax.yaxis.get_offset_text().set_fontsize(sci_fontsize)
        ax.yaxis.get_offset_text().set_fontweight(sci_fontweight)
        ax.yaxis.get_offset_text().set_position(sci_position)
    else:
        cbar.ax.yaxis.set_major_formatter(formatter)
        cbar.ax.yaxis.get_offset_text().set_size(sci_fontsize)
        cbar.ax.yaxis.get_offset_text().set_weight(sci_fontweight)
        cbar.ax.yaxis.get_offset_text().set_position(sci_position)


"""设置figure框的线条宽度"""
def set_spines(ax, bottom_linewidth=3, left_linewidth=3, right_linewidth=3, top_linewidth=3, polar_linewidth=3, mode='2d'):
    if mode == '2d':
        ax.spines['bottom'].set_linewidth(bottom_linewidth)
        ax.spines['left'].set_linewidth(left_linewidth)
        ax.spines['right'].set_linewidth(right_linewidth)
        ax.spines['top'].set_linewidth(top_linewidth)

        # color
        # ax.spines['bottom'].set_color('red')
    elif mode == 'polar':
        ax.spines['polar'].set_linewidth(polar_linewidth)  # 极坐标的脊线宽度
        for spine in ax.spines.values():
            spine.set_linewidth(polar_linewidth)  # 设置所有脊线宽度（可以按需指定特定方向的脊线）


def set_legend(ax, legend_labels = None, order=None,
               font_size=18, fontfamily='Arial', fontweight='bold',
               location='upper right', ncol=1,
               columnspacing=1.0, handletextpad=0.8):
    """

    :param ax:
    :param legend_labels:
    :param font_size:
    :param fontfamily:
    :param fontweight:
    :param location: 输入字符或者一个长度为4的list，num 1和num 2为legend中某点的位置，num 1为水平位置(范围为 0~1)，num 2为垂直位置(范围为 0~1)。该点的位置位于legend的num 3位置，num 3的范围如下：
                    'best'	0
                    'upper right'	1
                    'upper left'	2
                    'lower left'	3
                    'lower right'	4
                    'right'	        5
                    'center left'	6
                    'center right'	7
                    'lower center'	8
                    'upper center'	9
                    'center'	    10
                    num4表示轴和legend之间的填充，默认值为None（有一定填充），设置为0即取消填充
    :return:
    """
    legend_font_dict = dict(size=font_size,
                            family=fontfamily,
                            weight=fontweight,
                            style='normal',
                            )
    if legend_labels is None:
        handles, labels = ax.get_legend_handles_labels()
        legend_labels = labels

        if order is not None:
            if len(order) != len(handles):
                raise ValueError("排序索引数量与图例项数量不匹配")
            handles = [handles[i] for i in order]
            legend_labels = [labels[i] for i in order]

        if isinstance(location, str):
            legend = ax.legend(handles, legend_labels, loc=location, prop=legend_font_dict, frameon=False, ncol=ncol, columnspacing=columnspacing, handletextpad=handletextpad)
        elif isinstance(location, tuple):
            legend = ax.legend(handles, legend_labels, loc='upper right', prop=legend_font_dict, bbox_to_anchor=location, frameon=False, ncol=ncol, columnspacing=columnspacing, handletextpad=handletextpad)
        else:
            raise TypeError('location must be str or turple')
    else:
        if isinstance(location, str):
            legend = ax.legend(legend_labels, loc=location, prop=legend_font_dict, frameon=False, ncol=ncol, columnspacing=columnspacing, handletextpad=handletextpad)
        elif isinstance(location, tuple):
            legend = ax.legend(legend_labels, loc='upper right', prop=legend_font_dict, bbox_to_anchor=location, frameon=False, ncol=ncol, columnspacing=columnspacing, handletextpad=handletextpad)
        else:
            raise TypeError('location must be str or turple')
    return legend


def set_legend_linewidth(legend, linewidth=1):
    for line in legend.get_lines():
        line.set_linewidth(linewidth)


def set_text(ax, x_text, y_text, text, fontfamily='Arial', fontsize=12, fontweight='light', color='k'):
    ax.text(x_text, y_text, text, fontfamily=fontfamily, fontsize=fontsize, fontweight=fontweight, color=color)


if __name__ == '__main__':
    # 创建测试数据
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = 1e-6 * np.sin(x)

    # 创建图表
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y)

    # 应用科学计数格式化，使用指定的小数位数
    set_scientific_y_ticks(ax, sci_sig_digits=expected_digits)

    # 验证格式化器是否正确设置
    y_formatter = ax.yaxis.get_major_formatter()
    assert isinstance(y_formatter, ticker.ScalarFormatter), "未正确设置为标量格式化器"
    assert y_formatter._scientific, "未启用科学计数法"

    # 验证小数位数
    plt.draw()  # 强制更新图表以生成刻度标签
    tick_labels = [label.get_text() for label in ax.get_yticklabels()]

    # 检查标签是否符合预期格式
    has_exponent = False
    for label in tick_labels:
        # 处理LaTeX格式的标签（如$\mathdefault{-1.23}$）
        clean_label = label.replace('$\mathdefault{', '').replace('}$', '')

        if 'e' in clean_label:
            has_exponent = True
        if '.' in clean_label:
            decimal_part = clean_label.split('.')[1].split('e')[0]
            assert len(decimal_part) == expected_digits, f"小数位数不正确: {label}，期望{expected_digits}位"

    assert has_exponent, "未检测到科学计数法表示"

    # 验证偏移文本属性
    offset_text = ax.yaxis.get_offset_text()
    assert offset_text.get_fontsize() == 25, "字体大小设置不正确"
    assert offset_text.get_fontweight() == 'bold', "字体粗细设置不正确"

    print("所有测试通过!")
    plt.show()  # 显示图表以便直观检查
