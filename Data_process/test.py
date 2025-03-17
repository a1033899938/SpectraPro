import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from src.general import set_figure
import matplotlib.ticker as ticker

fig0 = plt.figure(figsize=(8, 6))
ax0 = fig0.add_subplot(111)
x = np.arange(0, 3000, 3)
y = np.arange(0, 1000, 1)
ax0.plot(x, y, 'o-', markersize=1)
plt.yscale('log')
title = f'Excitation power-denpendent intensity\nof peak 1'
set_figure.set_label_and_title(ax0, title=title, xlabel='Excitaion Power(uW)', ylabel='Intensity(counts)',
                               label_fontsize=25, title_fontsize=25,
                               label_font_family='Times New Roman', title_font_family='Times New Roman',
                               label_fontweight='bold', title_fontweight='bold',
                               label_pad=15, title_pad=15)
set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)

# 设置主刻度为 10^1, 10^2, 10^3 等
# ax0.yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=15))

# 设置次刻度（在 10^1 和 10^2 之间添加 200, 400, 600, 800）
# ax0.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=[2.0, 4.0, 6.0, 8.0]))

# 设置主刻度标签为 10^1, 10^2, 10^3 等
# ax0.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'$10^{{{int(np.log10(y))}}}$' if y > 0 else ''))

# # 设置次刻度标签为 200, 400, 600, 800
# ax0.yaxis.set_minor_formatter(ticker.FixedFormatter(['', '', '', '']))

set_figure.set_tick(ax0, xbins=16, ybins=0, fontsize=10, fontweight='bold',
                    linewidth=3, tick_pad=5, direction='in',
                    ticks_xlabel=np.arange(0, 3001, 500))  # Normalized
# print(np.concatenate([np.arange(0, 101, 20), np.arange(200, 1101, 200)]))
# plt.yticks(np.concatenate([np.arange(0, 101, 20), np.arange(200, 1001, 200)]), ['', '', '', '', '', 100, '', '', '', '', 1000])


plt.show()
