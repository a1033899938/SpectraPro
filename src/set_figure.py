import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator  # set max number of ticks


def set_text(ax, xlabel='Wavelength(nm)', ylabel='Intensity(counts)', title='default title',
             xlabel_size=12, ylabel_size=12, title_size=15):
    try:
        ax.set_xlabel(xlabel, fontsize=xlabel_size, picker=True)
        ax.set_ylabel(ylabel, fontsize=ylabel_size, picker=True)
        ax.set_title(title, fontsize=title_size, picker=True)
    except Exception as e:
        print(f"Error save_figure.set_text:\n  |--> {e}")


def set_tick(ax, xbins=6, ybins=6):
    try:
        ax.xaxis.set_major_locator(MaxNLocator(nbins=xbins))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=ybins))
    except Exception as e:
        print(f"Error save_figure.set_tick:\n  |--> {e}")


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range(5))
    set_text(ax)
    set_tick(ax, xbins=3, ybins=2)
    plt.show()
