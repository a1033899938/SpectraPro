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

def my_graph1(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Wavelength(nm)', ylabel='Intensity(cts)')
    set_tick(ax, ticks_xlabel=np.arange(400, 1101, 200), show_xlabel_every_ticks=4, yaxis_use_log_scale=False) # Normalized
    set_legend(ax, font_size=12, location='best')
    set_spines(ax)
    plt.tight_layout()

def my_graph2(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Wavelength(nm)', ylabel='Intensity(a.u.)')
    set_tick(ax, ticks_xlabel=np.arange(400, 1101, 200), show_xlabel_every_ticks=4) # Normalized
    set_legend(ax, font_size=12, location='best')
    set_spines(ax)
    plt.tight_layout()

def my_graph3(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Wavelength(nm)', ylabel='Theoretical Range')
    set_tick(ax, ticks_xlabel=np.arange(400, 1101, 200), show_xlabel_every_ticks=4) # Normalized
    set_legend(ax, font_size=12, location='best')
    set_spines(ax)
    plt.tight_layout()

def my_graph4(ax, ticks_xlabel, title=''):
    set_label_and_title(ax, title=f"{title}_histogram", xlabel='Wavelength(nm)', ylabel='Frequency')
    set_tick(ax, ticks_xlabel=ticks_xlabel) # Normalized
    set_legend(ax, font_size=12, location='best')
    set_spines(ax)
    plt.tight_layout()