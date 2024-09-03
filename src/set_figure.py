import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator  # set max number of ticks


def set_text(ax, xlabel='Wavelength(nm)', ylabel='Intensity(counts)', title='default title',
             xlabel_size=12, ylabel_size=12, title_size=15):
    ax.set_xlabel(xlabel, fontsize=xlabel_size)
    ax.set_ylabel(ylabel, fontsize=ylabel_size)
    ax.set_title(title, fontsize=title_size)


def set_tick(ax, xbins=6, ybins=6):
    ax.xaxis.set_major_locator(MaxNLocator(nbins=xbins))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=ybins))


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range(5))
    set_text(ax)
    set_tick(ax, xbins=3, ybins=2)
    plt.show()
