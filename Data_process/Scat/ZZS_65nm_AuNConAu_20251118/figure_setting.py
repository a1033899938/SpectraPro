"""
Author: Junjie-Xie
Updated: 2025/11/19
Functions: 
"""
import numpy as np

from src.general.figure.set_figure import *

def single_axis_scan_map2d(ax, title="Mapping"):
    set_label_and_title(ax, title=title, xlabel='Wavlength(nm)', ylabel='Position_z(um)', mode='2d', title_pad=20)
    set_tick(ax, ticks_ylabel=np.arange(0, 50, 10), ticks_xlabel=np.arange(550, 1000, 200), show_xlabel_every_ticks=4, show_ylabel_every_ticks=2)  # Normalized
    set_legend(ax)
    set_spines(ax)
    plt.tight_layout()

def single_axis_scan_graph(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Wavelength(nm)', ylabel='Intensity(a.u.)')
    set_tick(ax, ticks_xlabel=np.arange(400, 1101, 200), show_xlabel_every_ticks=4) # Normalized
    set_legend(ax, font_size=12, location='best')
    set_spines(ax)
    plt.tight_layout()

def single_axis_scan_result_var_wav(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Wavelength(nm)', ylabel='Position(um)', title_fontsize=30, title_fontweight="bold")
    set_tick(ax, ticks_xlabel=np.arange(400, 1101, 200), show_xlabel_every_ticks=4)  # Normalized
    set_legend(ax, font_size=20, location='best')
    set_spines(ax)
    plt.tight_layout()

def single_axis_scan_result_var_pos(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Position(um)', ylabel='Intensity(a.u.)', title_fontsize=30, title_fontweight="bold")
    set_tick(ax, ticks_ylabel=np.arange(0, 1.1, 0.2), show_xlabel_every_ticks=5, show_ylabel_every_ticks=2)  # Normalized
    set_legend(ax, font_size=20, location='best')
    set_spines(ax)
    plt.tight_layout()

def fitting_FWFM_hist(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='FWFM(um)', ylabel='Frequency')
    set_tick(ax, show_xlabel_every_ticks=5)  # Normalized
    set_legend(ax, font_size=12, location='best')
    set_spines(ax)
    plt.tight_layout()

def fitting_slope_hist(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Slope(um/nm)', ylabel='Frequency')
    set_tick(ax, ticks_xlabel=[0.03, 0.04, 0.05, 0.06, 0.07])  # Normalized
    set_legend(ax, font_size=12, location='best')
    set_spines(ax)
    plt.tight_layout()