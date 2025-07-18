import os.path
import h5py
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from src.general import *
from src.general import *
from src.general.figure import set_figure

datapath1 = r"D:\ExpData\SPE\20250513_SPE_hBN_SEM_array\hBN-2\20250513_SPE_hBN-2_SEM_array-measurement-1.h5"

def the_figure(ax):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'', ylabel='Normalized Intensity(a.u.)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(450, 701, 50))  # Normalized
    set_figure.set_scientific_y_ticks(ax, sci_fontsize=20)
    plt.tight_layout()


def the_figure1(ax, cbar):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'', xlabel='X', ylabel='Y', colorbar=cbar, colorbar_label='Normalized Intensity(a.u.)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, colorbar=cbar)  # Normalized
    set_figure.set_scientific_y_ticks(ax, cbar, sci_position=(2, 0))
    plt.tight_layout()

# hBN_2_beforeSEM_mapping_0
# hBN_2_afterSEM_mapping_0
"""fig0"""
# with h5py.File(datapath1, "r") as f:
#     mapping_name = 'hBN_2_afterSEM_mapping_0'
#     data = f['OceanOpticsSpectrometer'][mapping_name]
#     row_keys = data.keys()
#     row1_key = list(data.keys())[0]
#     row1 = data[row1_key]
#     column_keys_of_row1 = row1.keys()
#
#
#     bgd = np.array(data[f'x-0/{mapping_name[:-2]}-x0-y0'].attrs['background'])
#     bgd_time = data[f'x-0/{mapping_name[:-2]}-x0-y0'].attrs['background_int'] / 1000
#     wav = np.array(data[f'x-0/{mapping_name[:-2]}-x0-y0'].attrs['wavelengths'])
#     bgd = bgd / bgd_time
#     mapping_range = [len(row_keys), len(column_keys_of_row1)]
#     mapping_5 = np.zeros([mapping_range[0], mapping_range[1]])
#
#     fig = plt.figure(figsize=(8, 6))
#     ax = fig.add_subplot(111)
#     for i in range(mapping_range[0]):
#         parent_key = f"x-{i}"
#         for j in range(mapping_range[1]):
#             print(f"i now: {i}, j now: {j}")
#             child_key = f"{mapping_name[:-2]}-x{i}-y{j}"
#             sp = data[f"{parent_key}/{child_key}"]
#             sp_time = sp.attrs['integration_time'] / 1000
#             sp = np.array(sp)
#             sp = sp / sp_time
#             sp = sp - bgd
#             x, y = choose_range(wav, sp, min_val=460, max_val=700)
#             y = remove_spikes_with_local_median(x, y, filter_size=5)
#
#             mapping_5[i][j] = np.mean(sp[find_val_idx(wav, 505):find_val_idx(wav, 700)])
#             if np.max(sp[find_val_idx(wav, 600):find_val_idx(wav, 650)]) > 50:
#                 mapping_5[i][j] = mapping_5[i][j - 1]
#                 continue
#
#             ax.plot(x, y)
# the_figure(ax)
#
# np.save(os.path.join(os.path.dirname(datapath1), fr'm1\afterSEM.npy'), mapping_5)

"""保存图片"""
save_fig = 0
mapping =np.load(os.path.join(os.path.dirname(datapath1), fr'm1\afterSEM.npy'))
mapping_range = [mapping.shape[0], mapping.shape[1]]

fig0 = plt.figure(figsize=(8, 6))
ax0 = fig0.add_subplot(111)
x = range(mapping_range[0])
y = range(mapping_range[1])
X, Y = np.meshgrid(x, y)
print(f"shape x: {np.shape(X)}")
print(f"shape y: {np.shape(Y)}")
Z = mapping
im=ax0.pcolor(X, Y, np.transpose(Z), cmap='viridis')

# 添加颜色条
cbar = fig0.colorbar(im)

the_figure1(ax0, cbar)

if save_fig == 1:
    fig.savefig(os.path.join(os.path.dirname(datapath1), f'm1\PL_afterSEM.png'))
    fig0.savefig(os.path.join(os.path.dirname(datapath1), f'm1\PL_mapping_afterSEM.png'))
plt.show()