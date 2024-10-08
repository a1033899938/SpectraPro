import numpy as np


# define gaussian function for fitting
def gaussian(x, height, center, width, shift):
    return height * np.exp(-(x - center) ** 2 / (2 * width ** 2)) + shift


