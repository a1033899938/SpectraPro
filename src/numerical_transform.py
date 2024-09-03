import numpy as np


def Scale_up(Min, Max, Mid, min, max):
    scale = (Mid-Min)/(Max-Min)  # scale = (Mid-Min)/(Max-Min) = (mid-min)/(max-min)
    mid = scale*(max-min)+min
    return mid

