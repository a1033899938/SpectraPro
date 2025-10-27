import numpy as np

from src.general.figure.set_figure import *

def the_graph1(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Wavenumber(cm^-1)', ylabel='Intensity(cts)')
    set_tick(ax, ticks_xlabel=np.arange(200, 4001, 200), show_xlabel_every_ticks=2, yaxis_use_log_scale=False) # Normalized
    set_legend(ax, font_size=12, location='best')
    set_scientific_y_ticks(ax)
    set_spines(ax)
    plt.tight_layout()

def the_graph2(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Wavenumber(cm^-1)', ylabel='Intensity(cts)')
    set_tick(ax, ticks_xlabel=np.arange(200, 4001, 500), show_xlabel_every_ticks=2, yaxis_use_log_scale=False) # Normalized
    set_legend(ax, font_size=12, location='best')
    set_scientific_y_ticks(ax)
    set_spines(ax)
    plt.tight_layout()

def the_graph3(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Wavenumber(cm^-1)', ylabel='Intensity(cts)')
    set_tick(ax, ticks_xlabel=np.arange(1250, 1450, 50), show_xlabel_every_ticks=2, yaxis_use_log_scale=False) # Normalized
    set_legend(ax, font_size=12, location='best')
    set_scientific_y_ticks(ax)
    set_spines(ax)
    plt.tight_layout()

def the_graph4(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Wavelength(nm)', ylabel='Intensity(cts)')
    set_tick(ax, ticks_xlabel=np.arange(500, 960, 100), show_xlabel_every_ticks=2, yaxis_use_log_scale=False) # Normalized
    set_legend(ax, font_size=12, location='best')
    set_scientific_y_ticks(ax)
    set_spines(ax)
    plt.tight_layout()

def the_mapping(ax, cbar):
    set_label_and_title(ax, title='Mapping', xlabel='X', ylabel='Y', colorbar=cbar, colorbar_label='Intensity(cts)')
    set_tick(ax, colorbar=cbar) # Normalized
    set_legend(ax)
    set_spines(ax)
    plt.tight_layout()

def the_cascade_3d(ax):
    set_label_and_title(ax, title='Mapping', xlabel='Wavlength(nm)', ylabel='Time(s)', zlabel='Intensity(cts)', mode='3d')
    set_tick(ax, mode='3d')  # Normalized
    set_legend(ax)
    set_spines(ax)
    plt.tight_layout()

def the_cascade_2d(axes, title):
    for i, ax in enumerate(axes):
        set_legend(ax, font_size=5)
        set_tick(ax, linewidth=1, ybins=4, fontsize=10, show_ylabel_every_ticks=2)
        n_subplots = len(axes)

        # 计算垂直中间位置（0-1范围，相对于整个子图区域）
        if n_subplots % 2 == 1:  # 奇数个子图，就在中间子图的中部位置作label
            label_ax = n_subplots // 2 + 1
            middle_pos = 0.5
        else:  # 偶数个子图，就在中间两幅子图中处于下方的子图的上边作label(注意，子图序号为label_ax-1)
            label_ax = n_subplots // 2
            middle_pos = 0
    set_label_and_title(axes[label_ax-1], title='', xlabel='', ylabel='Intensity(cts)', ylabel_ha='center',
                        ylabel_va='center', y_label_position=(-0.15, middle_pos))  # , ylabel_rotation=(-0.15, 0.9)

    set_label_and_title(axes[0], title=title, xlabel='', ylabel='', title_pad=35, title_fontsize=30)
    set_label_and_title(axes[-1], title='', ylabel='', x_label_pad=20)
    set_tick(axes[-1], ticks_xlabel=np.arange(400, 1101, 100), linewidth=1, ybins=4, fontsize=10,
             show_ylabel_every_ticks=2, show_xlabel_every_ticks=2)
    plt.subplots_adjust(left=0.15)
    plt.tight_layout()