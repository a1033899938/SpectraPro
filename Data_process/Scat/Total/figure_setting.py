"""
Author: Junjie-Xie
Updated: 2025/11/19
Functions: 
"""
import numpy as np
from src.my_style.my_char import *
from src.general.figure.set_figure import *


def my_graph(ax, title, xtick, xlabel, ylabel):
    set_label_and_title(ax, title=title, xlabel=xlabel, ylabel=ylabel)
    set_tick(ax, ticks_xlabel=xtick, show_xlabel_every_ticks=2,
             yaxis_use_log_scale=False)  # Normalized
    set_spines(ax)
    set_legend(ax, ncol=2, font_size=16, location='upper right')
    plt.tight_layout()

"process"
def my_reconstruct_scat(ax, title_pad=17, title='', bbox_to_anchor=(1, 0.6)):
    set_label_and_title(ax, title=title, xlabel='Wavelength(nm)', ylabel='Intensity(a.u.)', title_pad=title_pad)
    set_tick(ax, ticks_xlabel=np.arange(500, 901, 100), show_xlabel_every_ticks=2, yaxis_use_log_scale=False) # Normalized
    set_spines(ax)
    set_legend(ax, font_size=20, location='upper right', bbox_to_anchor=bbox_to_anchor)
    plt.tight_layout()

def my_zstack_scats(ax, title_pad=17, title='', ytick=np.arange(-10, 11, 5)):
    set_label_and_title(ax, title=title, xlabel='Wavelength(nm)', ylabel='z(um)', title_pad=title_pad)
    set_tick(ax, ticks_xlabel=np.arange(500, 901, 100), ticks_ylabel=ytick, show_xlabel_every_ticks=2, show_ylabel_every_ticks=2,
             yaxis_use_log_scale=False)  # Normalized
    set_spines(ax)
    set_legend(ax, font_size=20, location='lower right')
    plt.tight_layout()

def my_maxint_ints(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='z(um)', ylabel='Intensity(a.u.)')
    set_tick(ax, ticks_xlabel=np.arange(-10, 11, 5), show_xlabel_every_ticks=2,
             yaxis_use_log_scale=False)  # Normalized
    set_legend(ax, font_size=20, location='upper left')
    set_spines(ax)
    plt.tight_layout()

def my_thumb_image(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='x(px)', ylabel='y(px)')
    set_tick(ax, ticks_xlabel=np.arange(0, 100, 20), ticks_ylabel=np.arange(0, 100, 20),
             yaxis_use_log_scale=False)  # Normalized
    set_spines(ax)
    plt.tight_layout()

def my_stage_position(ax, title='', unit='um'):
    set_label_and_title(ax, title=title, xlabel=f'x({unit})', ylabel=f'y({unit})')
    set_tick(ax)  # Normalized
    set_legend(ax, font_size=20, location='best')
    set_spines(ax)
    plt.tight_layout()

"reconstruct"
def my_reconstruct_scat_with_noise(ax, title=''):
    set_label_and_title(ax, title=title, xlabel='Wavelength(nm)', ylabel='Intensity(a.u.)')
    set_tick(ax, ticks_xlabel=np.arange(500, 730, 100), show_xlabel_every_ticks=2, yaxis_use_log_scale=False) # Normalized
    set_spines(ax)
    set_legend(ax, font_size=20, location='upper right')
    plt.tight_layout()

def my_reconstrution_process_error(ax, title=''):
    set_label_and_title(ax, title=title, xlabel="Iteration Count", ylabel="Recon. Error")
    set_tick(ax, ticks_xlabel=np.arange(0, 21, 5), show_xlabel_every_ticks=2)  # Normalized
    set_spines(ax)
    set_legend(ax, font_size=20, location='upper right')
    set_scientific_y_ticks(ax)
    plt.tight_layout()

"wav_maxz"
def my_wav_maxz_fit_popt_stats(ax, title_pad=17, title='', xlabel=f'Fitted Slope(um/nm)'):
    set_label_and_title(ax, title=title, xlabel=xlabel, ylabel=f'Frequency', title_pad=title_pad)
    set_tick(ax, y_tick_integer=True)  # Normalized
    set_spines(ax)
    set_legend(ax, font_size=20, location='upper left')
    plt.tight_layout()

def my_reconstrution_error_fit_popt_stats(ax, title='', title_pad=17, xlabel=f"Recon. Convergence Time Constant {My_Char.get('tau')} (s)"):
    set_label_and_title(ax, title=title, xlabel=xlabel, ylabel=f'Frequency', title_pad=title_pad)
    set_tick(ax, y_tick_integer=True)  # Normalized
    set_spines(ax)
    set_legend(ax, font_size=20, location='upper left')
    plt.tight_layout()

def my_wav_maxz_required_time_stats(ax, title='', title_pad=17, xlabel=f'Recon. Required Time(s)'):
    set_label_and_title(ax, title=title, xlabel=xlabel, ylabel=f'Frequency', title_pad=title_pad)
    set_tick(ax, y_tick_integer=True)  # Normalized
    set_spines(ax)
    set_legend(ax, font_size=20, location="upper left")
    plt.tight_layout()