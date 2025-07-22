from src.general.figure.set_figure import *

def the_mapping(ax, cbar):
    set_label_and_title(ax, title='Mapping', xlabel='X', ylabel='Y', colorbar=cbar, colorbar_label='Intensity(cts)')
    set_tick(ax, colorbar=cbar) # Normalized
    set_legend(ax)
    set_spines(ax)
    plt.tight_layout()

def the_cascade(ax):
    set_label_and_title(ax, title='Mapping', xlabel='Wavlength(nm)', ylabel='Time(s)', zlabel='Intensity(cts)', mode='3d')
    set_tick(ax, mode='3d')  # Normalized
    set_legend(ax)
    set_spines(ax)
    plt.tight_layout()