import h5py
import matplotlib.pyplot as plt

from src.general.figure import set_figure
from src.my_style.my_mapping_para import *
from src.general.load_data.read_name import *
from src.general.load_data.save_read_data import *
"""路径"""
h5file = r"D:\ExpData\Fellows\WYQ\20250714_WYQ_SHIN\20250714_WYQ_SHIN.h5"
dir_name = 'OceanOpticsSpectrometer'

def the_figure(ax):
    set_figure.set_label_and_title(ax, title='', ylabel='Intensity(a.u.)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 1101, 100), show_xlabel_every_ticks=2)  # Normalized
    set_figure.set_legend(ax)
    plt.tight_layout()

# print_name_in_h5(h5file, dir_name, field_in=None, field_out=None, sort_field=None, print_names=True)
sp_names_0 = [
            "shin-1_0",
            "shin-2_0",
            "shin-3_0",
            "shin-4_0",
            "shin-5_0",
            "shin-6_0",
            "shin-7_0",
            "shin-8_0",
            "shin-9_0",
            "shin-10_0",
            "shin-11_0",
             ]

sp_names_1 = [
            "8SHcube_0",
            "8SHcube_1",
            "8SHcube_2",
            "8SHcube_3",
            "8SHcube_4",
            "8SHcube_5",
            "8SHcube_6",
             ]

sp_names_2 = [
            "4SHcube_0",
            "4SHcube_1",
            "4SHcube_2",
            "4SHcube_3",
            "4SHcube_4",
            "4SHcube_5",]

with h5py.File(h5file, "r") as f:
    # 读取sp目录
    data = f[dir_name]

    np_names = sp_names_0 + sp_names_1 + sp_names_2

    # 作不同反射板和光源的曲线
    max_val = []
    for np_name in np_names:
        wav = np.array(data[np_name].attrs['wavelengths'])

        bgd = np.array(data[np_name].attrs['background'])
        bgd_time = data[np_name].attrs['background_int'] / 1000
        bgd = bgd / bgd_time

        ref = np.array(data[np_name].attrs['reference'])
        ref_time = data[np_name].attrs['reference_int'] / 1000
        ref = ref / ref_time

        sp = data[np_name]
        sp_time = sp.attrs['integration_time'] / 1000
        sp = np.array(sp)
        sp = sp / sp_time

        # save_full_path = fr"{os.path.dirname(h5file)}\data\{np_name}.txt"
        # save_lines_txt(wav, bgd, ref, sp, first_line=["wav", "bgd", "ref", "sp"], save_full_path=save_full_path, comfirm_all_overwrite=True)

        if np_name == 'shin-1_0' or np_name == '8SHcube_0' or np_name == '4SHcube_0':
            fig = plt.figure(figsize=(12, 8), dpi=200)
            ax = fig.add_subplot(111)
        x = wav
        y = (sp - bgd) / (ref - bgd)
        x, y, ref = choose_range(x, y, ref, x1=400, x2=1000)
        ax.plot(x, y, label=np_name)
        max_val.append(np.max(y))
        if np_name == 'shin-11_0' or np_name == '8SHcube_6' or np_name == '4SHcube_5':
            ax.set_ylim([0, max(max_val)])
            ax.plot(x, ref/np.max(ref)*max(max_val), label="ref", color='red')
            max_val = []
        the_figure(ax)

plt.show()