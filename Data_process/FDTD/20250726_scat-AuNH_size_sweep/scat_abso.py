"""
Author: Junjie-Xie
Updated: 2025/7/25
Functions: 
"""
import numpy as np
from matplotlib import pyplot as plt
from src.general.load_data.save_read_data import *
from src.my_style.my_figure import *
from src.my_style.my_color import *
from src.general.figure.draw_figure import *

filepath1 = r"D:\FDTDSimFile\NP_scattering\size_of_AuNH-lambda_scat_abso\lambda_scats_absos.txt"
data1 = read_lines_txt(filepath1, separator=',', skip_lines=1, row_lines_names=0)
filepath2 = r"D:\FDTDSimFile\NP_scattering\size_of_AuNH-lambda_scat_abso\rs.txt"
lens = read_row_txt(filepath2, delimiter=' ')

fig = plt.figure(figsize=(12*2, 8), dpi=200)
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

scats = None
absos = None
les = [f"{int(float(len))} nm" for len in lens]
for i, (key, value) in enumerate(data1.items()):
    if 'lambda' in key:
        wav = np.array(value)
    else:
        num = int(key.split('_')[-1])
        len = int(float(lens[num - 1]))
        le = f"{len} nm"

    if 'scat' in key:
        scat = np.array(value)
        scat = scat / np.max(scat)
        ax1.plot(wav, scat, label=le, color=MyColor.get_color("professional", num-1))
        if scats is None:
            scats = scat
        else:
            scats = np.vstack((scats, scat))
    elif 'abso' in key:
        abso = -np.array(value)
        ax2.plot(wav, abso, label=le, color=MyColor.get_color("professional", num-1))
        if absos is None:
            absos = abso
        else:
            absos = np.vstack((absos, abso))

the_graph(ax1, title="Scattering")
the_graph(ax2, title="Absorption")

# cascade_2d
fig, axes1 = draw_cascade_2d(x=wav, ys=scats, les=les)
fig, axes2 = draw_cascade_2d(x=wav, ys=absos, les=les)
the_cascade_2d(axes1, "Scattering")
the_cascade_2d(axes2, "Absorption")
plt.show()