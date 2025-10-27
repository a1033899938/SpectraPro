import h5py
import os
import matplotlib.pyplot as plt

from src.general.figure import set_figure
from src.general.numerical.edit_data import choose_range
from src.my_style.my_mapping_para import *

def load_data(h5_file, dir_name, sp_names, le):
    with h5py.File(h5_file, "r") as f:
        # 读取sp目录
        data = f[dir_name]

        # 读取目录下的第一个sp的bgd和wav，并对积分时间作归一化
        bgd = np.array(data[sp_names[0]].attrs['background'])
        bgd_time = data[sp_names[0]].attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        wav = np.array(data[sp_names[0]].attrs['wavelengths'])

        # 创建画布
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)

        # 历遍所有sp
        for i, key in enumerate(sp_names):
            sp = data[key]
            sp_time = sp.attrs['integration_time'] / 1000
            sp = np.array(sp)
            sp = sp / sp_time
            sp = sp - bgd

            """数据处理区域"""
            x, y = choose_range(wav, sp, x1=400, x2=900)
            ax.plot(x, y)
            # 曲线拟合
            x_for_fit, y_for_fit = choose_range(wav, sp, x1=510, x2=900)
            fitting_paras = triple_peaks_fitting(x_for_fit, y_for_fit, ax=ax)

        the_figure(ax, le)
    return fig

def the_figure(ax, le):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=f'405 / 450 nm Laser Excitation', ylabel='Intensity(cts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 901, 100))  # Normalized
    set_figure.set_legend(ax, legend_labels=le)
    set_figure.set_scientific_y_ticks(ax)
    plt.tight_layout()

if __name__ == '__main__':
    h5_file = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-8\20250224_SPE_hBN_afterSEM_measurement-8.h5"
    dir_name = 'OceanOpticsSpectrometer'
    ex_405_name = 'hBN_afterSEM_5kV_2min_60KX_405ex_500uW_0'
    ex_450_name = 'hBN_afterSEM_5kV_2min_60KX_405ex_500uW_1'  # hBN_afterSEM_5kV_2min_60KX_405ex_500uW_1实为hBN_afterSEM_5kV_2min_60KX_450ex_500uW_1
    sp_names = ['hBN_afterSEM_5kV_2min_60KX_405ex_500uW_0',
                'hBN_afterSEM_5kV_2min_60KX_405ex_500uW_1']
    le = ['405 ex',
          '450 ex']

    fig = load_data(h5_file, dir_name, sp_names, le)

    # 保存图片到npz的文件夹下
    fig.savefig(os.path.join(os.path.dirname(h5_file), f'405ex vs 450ex.png'))
    plt.show()