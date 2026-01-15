"""
Author: Junjie-Xie
Updated: 2025/11/19
Functions: 
"""
import numpy as np

from src.general.figure.set_figure import *

"process"
def my_reconstruct_scat(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Wavelength(nm)', ylabel='Intensity(a.u.)')
    set_tick(ax, ticks_xlabel=np.arange(500, 901, 100), show_xlabel_every_ticks=2, yaxis_use_log_scale=False) # Normalized
    set_spines(ax)
    plt.tight_layout()

def my_zstack_scats(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Wavelength(nm)', ylabel='z(um)')
    set_tick(ax, ticks_xlabel=np.arange(500, 901, 100), ticks_ylabel=np.arange(0, 50, 10), show_xlabel_every_ticks=2, show_ylabel_every_ticks=2,
             yaxis_use_log_scale=False)  # Normalized
    set_spines(ax)
    plt.tight_layout()

def my_maxint_ints(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='z(um)', ylabel='Intensity(a.u.)')
    set_tick(ax, ticks_xlabel=np.arange(0, 50, 10), show_xlabel_every_ticks=2,
             yaxis_use_log_scale=False)  # Normalized
    set_legend(ax, font_size=20, location='upper right')
    set_spines(ax)
    plt.tight_layout()

def my_thumb_image(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='x(px)', ylabel='y(px)')
    set_tick(ax, ticks_xlabel=np.arange(0, 100, 20), ticks_ylabel=np.arange(0, 100, 20),
             yaxis_use_log_scale=False)  # Normalized
    set_spines(ax)
    plt.tight_layout()

"""plot reconstruct error"""
def my_reconstruct_scat_jump_step(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Wavelength(nm)', ylabel='Intensity(a.u.)')
    set_tick(ax)
    set_legend(ax, font_size=20, location='best')
    set_spines(ax)
    plt.tight_layout()

def my_reconstruct_error_stats(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Reconstruct Error', ylabel='Frequency')
    set_tick(ax)
    set_legend(ax, font_size=20, location='best')
    set_spines(ax)
    plt.tight_layout()

def my_reconstruct_error_jump_step_left(fig, ax1, ax2, title=''):
    set_label_and_title(ax1, title="", xlabel='', ylabel='Reconstruct Error')

    fig.suptitle(title, fontsize=32, fontweight='bold', y=0.98, family='Times New Roman')
    fig.text(0.5, 0.02, 'Step size(um)', ha='center', fontsize=30, fontweight='bold', family='Times New Roman')

    set_tick(ax1, ticks_xlabel=np.arange(0.5, 5.5, 0.5))
    set_tick(ax2, ticks_xlabel=np.arange(49.5, 51, 0.5))
    set_legend(ax1, font_size=20, location='upper left')
    set_spines(ax1)
    set_spines(ax2)
    plt.tight_layout()

"Maxz_range"
def my_maxz_range_stats(ax1, title=""):
    set_label_and_title(ax1, title=title, xlabel='z(um)', ylabel='Frequency')
    set_tick(ax1)
    set_legend(ax1, font_size=20, location='best')
    set_spines(ax1)

"wav_maxz_fit_stats"
def my_wav_maxz_fit_slope_stats(ax, title=""):
    set_label_and_title(ax, title=title, xlabel='Slope(um/nm)', ylabel='Frequency')
    set_tick(ax)
    set_spines(ax)
    plt.tight_layout()

def my_wav_maxz_minimum_required_time_stats(ax, title=""):
    set_label_and_title(ax, title=title, xlabel='Minimum Required Time(s)', ylabel='Frequency')
    set_tick(ax)
    set_spines(ax)
    plt.tight_layout()