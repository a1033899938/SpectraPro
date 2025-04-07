import h5py

from src.general import set_figure
from src.general.draw_figure import *
from src.general.edit_data import *
from src.general.filter import *

def the_figure(ax, fig):
    set_figure.set_label_and_title(ax, title=f'Stability of Measurement System', xlabel='Measurement Sequence', ylabel='Wavelength(nm)', mode='3d', zlabel_rotation=90, label_pad=25, axis_order=(1, 2, 0))
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticklabel_pad=10, ticks_xlabel=np.arange(0, 601, 100), ticks_ylabel=np.arange(500, 901, 100), mode='3d')
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=20, azim=-45)  # elev 是仰角，azim 是方位角
    ax.grid(True)
    fig.tight_layout()

def the_figure0(ax):
    set_figure.set_label_and_title(ax, title=f'Stability of Measurement System', xlabel='Measurement Sequence', ylabel='Intensity(a.u.)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(0, 601, 100), ticks_ylabel=np.arange(0, 1.1, 0.1))

datapath1 = r"D:\XmuNetDisk\2025-03-27.h5"
save_fig = 0

"""fig0"""
with h5py.File(datapath1, "r") as f:
    data = f['OceanOpticsSpectrometer']
    bgd = np.array(data['stability_75nmTetrahedron_0'].attrs['background'])
    bgd_time = data['stability_75nmTetrahedron_0'].attrs['background_int'] / 1000
    wav = np.array(data['stability_75nmTetrahedron_0'].attrs['wavelengths'])
    bgd = bgd / bgd_time
    ref = np.array(data['stability_75nmTetrahedron_0'].attrs['reference'])
    ref_time = data['stability_75nmTetrahedron_0'].attrs['reference_int'] / 1000
    ref = ref / ref_time

    bgd, _ = np.meshgrid(bgd, np.arange(0, data['stability_75nmTetrahedron_0'].shape[0])) # 创建一个与sp相同大小的bgd阵列
    ref, _ = np.meshgrid(ref, np.arange(0, data['stability_75nmTetrahedron_0'].shape[0])) # 创建一个与sp相同大小的ref阵列

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    sp = data['stability_75nmTetrahedron_0']
    sp_time = sp.attrs['integration_time'] / 1000
    sp = np.array(sp)
    sp = sp / sp_time
    sp = (sp - bgd) / (ref - bgd)
    sp = remove_spikes(sp, axis=1)

    wav, sp = choose_range(wav, sp, min_val=500, max_val=900, axis=1)
    max_z = draw_cascade(ax, wav, sp, highlight_maximum=True, plot_maximum=False)
    the_figure(ax, fig)

fig0 = plt.figure(figsize=(8, 6))
ax0 = fig0.add_subplot(111)
ax0.plot(max_z / np.max(max_z))
the_figure0(ax0)

plt.show()