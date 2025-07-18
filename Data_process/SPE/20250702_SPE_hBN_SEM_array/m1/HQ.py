import h5py
from src.general.figure.draw_figure import *
from src.my_style.my_mapping_para import *
from src.general.numerical.edit_data import *


def load_data(h5_file, dir_name, bgd_name):
    with h5py.File(h5_file, "r") as f:
        # 读取mapping group
        data = f[dir_name]

        # 读取第一个sp的bgd和wav，并对积分时间作归一化
        bgd = np.array(data[bgd_name].attrs['background'])
        bgd_time = data[bgd_name].attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        wav = np.array(data[bgd_name].attrs['wavelengths'])

        sp_names = []
        powers = []
        for key in data.keys():
            if 'P1-450ex-' in key and not any(sub_key in key for sub_key in ['P1-450ex-10uW_1', 'P1-450ex-10uW_2', 'Onway']):
                sp_names.append(key)
                powers.append(int(key[len('P1-450ex-'):-len("uW_0")]))

        # for key in data.keys():
        #     if 'Onway_P1-450ex-' in key and key[-2:] == '_0':
        #         sp_names.append(key)
        #         powers.append(int(key[len('Onway_P1-450ex-'):-len("uW_0")]))

        powers, sp_names = sort_lists(powers, sp_names)

        print(sp_names)

        ints1 = []
        ints2 = []
        ints3 = []
        ints4 = []



        # 创建画布
        fig2 = plt.figure(figsize=(8, 6))
        ax2 = fig2.add_subplot(111)
        for i, (power, sp_name) in enumerate(zip(powers, sp_names)):
            print(sp_name)
            # 创建画布
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111)
            if i != 0:
                y_last = y
            sp_2d = data[sp_name]
            sp_time = sp_2d.attrs['integration_time'] / 1000
            sp_2d = np.array(sp_2d)
            for row in range(sp_2d.shape[0]):
                if row != 20:
                    continue
                sp = sp_2d[row, :]
                sp = sp / sp_time
                sp = sp - bgd
                sp = sp / power

                """处理数据区域"""
                x, y = choose_range(wav, sp, x1=510, x2=900, axis=0)

                # 画出每条sp
                ax.plot(x, y, label=sp_name)
                if i != 0:
                    diff = -(y - y_last)
                    ax2.plot(x, diff / np.max(diff), '--', label=i)
                # fitting_paras = penta_peaks_fitting(x, y, ax=ax)
                fitting_paras = quatra_peaks_fitting(x, y, ax=ax)
                # ints1.append(fitting_paras["mag1"])
                # ints2.append(fitting_paras["mag2"])
                # ints3.append(fitting_paras["mag3"])
                # ints4.append(fitting_paras["mag4"])
            the_figure(ax)
            the_figure(ax2)

        # fig = plt.figure(figsize=(8, 6))
        # ax = fig.add_subplot(111)
        # ax.plot(range(len(ints1)), ints1, label='peak1')
        # ax.plot(range(len(ints2)), ints2, label='peak2')
        # ax.plot(range(len(ints3)), ints3, label='peak3')
        # ax.plot(range(len(ints4)), ints4, label='peak4')
        # the_figure1(ax)
    return fig

def the_figure(ax):
    """拟合曲线"""
    set_label_and_title(ax, title=f'', ylabel='Intensity(cts)')
    set_spines(ax)
    set_tick(ax, ticks_xlabel=np.arange(510, 901, 100))  # Normalized
    set_legend(ax)
    plt.tight_layout()

def the_figure1(ax):
    """拟合曲线"""
    set_label_and_title(ax, title=f'', ylabel='Intensity(cts)')
    set_spines(ax)
    set_tick(ax)  # Normalized
    set_legend(ax)
    plt.tight_layout()

if __name__ == '__main__':
    # 读取mapping数据
    h5_file = r"D:\ExpData\SPE\20250702_SPE_hBN_SEM_array\measurement-1.h5"
    bgd_name = "P1-450ex-10uW_0"
    fig_graph = load_data(h5_file=h5_file,
                          dir_name='OceanOpticsSpectrometer',
                          bgd_name=bgd_name)

    # 创建文件夹
    # folder_path = os.path.join(os.path.dirname(h5_file), f'{group_name}')
    # if not os.path.exists(folder_path):
    #     os.makedirs(folder_path, exist_ok=True)

    # 保存mapping数据
    # npz_file = os.path.join(folder_path, f'PL_mapping.npy')
    # np.save(npz_file, mapping)

    # 读取mapping数据
    # mapping = np.load(npz_file)

    # 作图
    # fig_mapping = draw_mapping(mapping, title='PL Mapping')

    # # 保存图片到npz的文件夹下
    # fig_mapping.savefig(os.path.join(folder_path, f'mapping_2.png'))
    # fig_graph.savefig(os.path.join(folder_path, f'graph.png'))
    plt.show()