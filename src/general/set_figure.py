import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator  # set max number of ticks
# from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
import matplotlib as mpl
from matplotlib import ticker


def set_label_and_title(ax, 
                        xlabel='Wavelength(nm)', ylabel='Intensity(counts)', title='default title',
                        label_fontsize=12, title_fontsize=15,
                        label_font_family='Arial', title_font_family='Arial',
                        label_fontweight='bold', title_fontweight='bold',
                        label_pad=20, title_pad=20):
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
        ax.set_xlabel(xlabel, fontdict=label_font_dict, weight=label_fontweight, labelpad=label_pad, picker=True)
        ax.set_ylabel(ylabel, fontdict=label_font_dict, weight=label_fontweight, labelpad=label_pad, picker=True)
        ax.set_title(title, fontdict=title_font_dict, weight=title_fontweight, pad=title_pad, picker=True)
    except Exception as e:
        print(f"Error save_figure.set_label_and_title:\n  |--> {e}")


def set_tick(ax,
             xbins=6, ybins=6, fontsize=15, fontweight='bold',
             linewidth=2, direction='in', tick_pad=2,
             ticks_xlabel=None, ticks_ylabel=None):
    try:
        ax.xaxis.set_major_locator(MaxNLocator(nbins=xbins))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=ybins))
        ax.tick_params(axis='both', labelsize=fontsize, width=linewidth, direction=direction)
        ax.xaxis.set_tick_params(pad=tick_pad)
        ax.yaxis.set_tick_params(pad=tick_pad)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontweight(fontweight)
        if ticks_xlabel is not None:
            ax.xaxis.set_ticks(ticks_xlabel)
        if ticks_ylabel is not None:
            ax.yaxis.set_ticks(ticks_ylabel)
    except Exception as e:
        print(f"Error save_figure.set_tick:\n  |--> {e}")


def set_scientific_y_ticks(ax,
                           sci_fontsize=12,
                           sci_fontweight='light'):
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3, 3))
    ax.yaxis.set_major_formatter(formatter)
    # ax.ticklabel_format(style='sci', scilimits=(-15, 0), axis='y', useMathText=True)
    ax.yaxis.get_offset_text().set_fontsize(sci_fontsize)
    ax.yaxis.get_offset_text().set_fontweight(sci_fontweight)


def set_spines(ax, bottom_linewidth=2, left_linewidth=2, right_linewidth=0, top_linewidth=0):
    ax.spines['bottom'].set_linewidth(bottom_linewidth)
    ax.spines['left'].set_linewidth(left_linewidth)
    ax.spines['right'].set_linewidth(right_linewidth)
    ax.spines['top'].set_linewidth(top_linewidth)


def set_legend(ax, legend_labels,
               font_size=12, fontfamily='Arial', fontweight='bold',
               location='upper right'):
    legend_font_dict = dict(size=font_size,
                            family=fontfamily,
                            weight=fontweight,
                            style='normal',
                            )
    legend = ax.legend(legend_labels,
                       loc=location, prop=legend_font_dict, frameon=False)
    return legend


def set_legend_linewidth(legend, linewidth=1):
    for line in legend.get_lines():
        line.set_linewidth(linewidth)


def set_text(ax, x_text, y_text, text, fontfamily='Arial', fontsize=12, fontweight='light', color='k'):
    ax.text(x_text, y_text, text, fontfamily=fontfamily, fontsize=fontsize, fontweight=fontweight, color=color)


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range(5))
    set_label_and_title(ax)
    set_tick(ax, xbins=3, ybins=2)
    plt.show()
