import os
import matplotlib.pyplot as plt
import numpy as np
from src.general.read_file import read_file
from src.general import set_figure
from src.ui.general_methods import GeneralMethods
from src.general.save_figure import save_subfig

'''
curve colors
'''
# 获取默认颜色循环
default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# 获取前 20 条曲线的颜色
num_colors = 20
colors = default_colors * (num_colors // len(default_colors) + 1)  # 复制颜色列表以确保足够多的颜色
colors = colors[:num_colors]  # 截取前 num_colors 条颜色

folder_path = r'C:\Users\a1033\Desktop\Contemporary\240806-240808\20240914process\13#\1-1'
extensions = ['.txt', '.spe']

fig = plt.figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)

file_paths, files, file_names = GeneralMethods.list_files_in_directory(folder_path, extensions)
i = 0

figure_xmins = []
figure_xmaxs = []
figure_ymins = []
figure_ymaxs = []

texts = ['Substrate 1', 'NP 1', 'NP 2', 'NP 3']
# texts = ['NP 3-1', 'NP 3-2', 'NP 4', 'NP 5-1', 'NP 5-2']
# texts = ['substrate', 'NP 1', 'NP 2', 'NP 3-1', 'NP 3-2', 'NP 4', 'NP 5-1', 'NP 5-2']
legend_text = texts
# texts = ['0.5%', '1%', '5%', '10%', '50%', '100%']
# legend_text = [f'Laser Power {text}' for text in texts]
# powers = [0.5, 1, 5, 10, 50, 100]

for file_path, file_name in zip(file_paths, file_names):
    readFile = read_file(file_path, show_data_flag=False)
    data = readFile.data
    x = data['wavelength']
    y = data['intensity']

    # y = y / powers[i]
    y /= 10  # 10s
    figure_xmins.append(x.min())
    figure_ymins.append(y.min())
    figure_xmaxs.append(x.max())
    '''ignore y.max of bgd'''
    if i == 0:
        figure_ymaxs.append(y.min())
    else:
        figure_ymaxs.append(y.max())

    '''
    text
    '''
    text_y = np.max(y)
    index_text_y = np.argmax(y)
    text_x = x[index_text_y]
    if i == 0:
        text_x = 595.7
        text_y = 53
        text_y /= 10
    elif i == 1:
        text_x = 581.7
        text_y = 1310
        text_y /= 10
    elif i == 3:
        text_x += 0
        # text_y -= 50
        # text_y /= 10
    set_figure.set_text(ax, x_text=text_x - 10, y_text=text_y + 0.5, text=texts[i],
                        fontfamily='Times New Roman', fontweight='bold', fontsize=17, color=colors[i])

    # Ensure x and y are 1D arrays and z is a 2D array
    x = np.array(x)
    y = np.array(y)

    linewidth = 2
    ax.plot(x, y, linewidth=linewidth)
    i += 1

figure_xmin = np.array(figure_xmins).min()
figure_xmax = np.array(figure_xmaxs).min()
figure_ymin = np.array(figure_ymins).min()
figure_ymax = np.array(figure_ymaxs).max()

"""temp region"""
'''
legend
'''
legend = set_figure.set_legend(ax, legend_labels=legend_text, fontfamily='Times New Roman', font_size=12,
                               location='upper right')
set_figure.set_legend_linewidth(legend, linewidth=3)
'''
title
'''
title = 'hBN/AuNP/SiO$\mathrm{_2}$ PL'
'''
figure
'''
set_figure.set_label_and_title(ax, title=title, ylabel='Intensity(cts/s)',
                               label_fontsize=25, title_fontsize=25,
                               label_font_family='Times New Roman', title_font_family='Times New Roman',
                               label_fontweight='bold', title_fontweight='bold',
                               label_pad=8, title_pad=15)
set_figure.set_spines(ax, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
set_figure.set_tick(ax, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                    linewidth=3, tick_pad=5, direction='in', ticks_xlabel=np.linspace(500, 750, 6))
set_figure.set_scientific_y_ticks(ax, sci_fontsize=15, sci_fontweight='bold')
ax.set_xlim([figure_xmin, figure_xmax])
ax.set_ylim([figure_ymin, figure_ymax * 1.1])

save_filename = os.path.join(folder_path, os.path.splitext(os.path.basename(__file__))[0])
save_filename += '.png'
save_subfig(fig, ax, save_filename)

from src.ui.general_methods import GeneralMethods
save_data_of_figure_path = os.path.join(folder_path, os.path.splitext(os.path.basename(__file__))[0])
save_data_of_figure_path += '.npz'
GeneralMethods.save_graph_data_as_npz(ax, save_data_of_figure_path)

plt.show()
