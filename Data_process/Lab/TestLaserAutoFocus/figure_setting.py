"""
Author: Junjie-Xie
Updated: 2025/11/19
Functions: 
"""
import numpy as np

from src.general.figure.set_figure import *

"Maxz_range"
def my_auto_focus(ax, title="", ylabel=""):
    set_label_and_title(ax, title=title, xlabel='z(um)', ylabel=ylabel)
    set_tick(ax, ticks_xlabel=np.arange(-50, 51, 10), show_xlabel_every_ticks=2)
    set_spines(ax)