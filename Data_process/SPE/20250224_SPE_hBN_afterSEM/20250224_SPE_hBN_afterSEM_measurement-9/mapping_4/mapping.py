import os.path
import h5py
from src.general.numerical.edit_data import *
from src.general.figure.draw_figure import *

def load_data(h5_file, dir_name, group_name, sp_name):
    with h5py.File(h5_file, "r") as f:
        # 读取mapping group
        data = f[dir_name][group_name]

        # 读取group下的keys（子group）和第一个子group下的所有keys（sp）
        row_keys = data.keys()
        row1_key = list(data.keys())[0]
        row1 = data[row1_key]
        column_keys_of_row1 = row1.keys()

        # 创建储存mapping数据的空数组
        mapping_range = [len(row_keys), len(column_keys_of_row1)]
        mapping = np.zeros([mapping_range[0], mapping_range[1]])

        # 读取第一个子group下的第一个sp的bgd和wav，并对积分时间作归一化
        bgd = np.array(data[f'x-0/{sp_name}-x0-y0'].attrs['background'])
        bgd_time = data[f'x-0/{sp_name}-x0-y0'].attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        wav = np.array(data[f'x-0/{sp_name}-x0-y0'].attrs['wavelengths'])

        # 创建画布
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)

        # 历遍所有sp
        for i in range(mapping_range[0]):
            parent_key = f"x-{i}"
            for j in range(mapping_range[1]):
                # print(f"i now: {i}, j now: {j}")
                child_key = f"{sp_name}-x{i}-y{j}"
                sp = data[f"{parent_key}/{child_key}"]
                sp_time = sp.attrs['integration_time'] / 1000
                sp = np.array(sp)
                sp = sp / sp_time
                sp = sp - bgd

                """数据处理区域"""
                x, y = choose_range(wav, sp, x1=450, x2=700)

                # # 初步筛选出需要处理尖峰噪声的sp
                if np.max(y) > 2000:
                    continue
                #     print(f"i now: {i}, j now: {j}")
                    # y = remove_spikes_with_local_median(x, y, filter_size=5)

                # 选取538nm位置的强度为mapping color幅度值
                mapping[i][j] = sp[find_val_idx(wav, 538)]

                # 画出每条sp
                ax.plot(x, y)
    the_figure(ax)
    return mapping, fig

def the_figure(ax):
    """拟合曲线"""
    set_label_and_title(ax, title=f'', ylabel='Intensity(cts)')
    set_spines(ax)
    set_tick(ax, ticks_xlabel=np.arange(450, 701, 50))  # Normalized
    plt.tight_layout()

if __name__ == '__main__':
    # 读取mapping数据
    h5_file = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-9\20250224_SPE_hBN_afterSEM_measurement-9.h5"
    group_name = 'hBN_afterSEM_mapping_4'
    mapping, fig_graph = load_data(h5_file=h5_file,
                        dir_name='OceanOpticsSpectrometer',
                        group_name=group_name,
                        sp_name='hBN_1-2_beforeSEM_mapping')

    # 创建文件夹
    folder_path = os.path.join(os.path.dirname(h5_file), f'{group_name}')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    # 保存mapping数据
    npz_file = os.path.join(folder_path, f'PL_mapping.npy')
    np.save(npz_file, mapping)

    # 读取mapping数据
    mapping = np.load(npz_file)

    # 作图
    fig_mapping = draw_mapping(mapping, title='PL Mapping')

    # 保存图片到npz的文件夹下
    fig_mapping.savefig(os.path.join(folder_path, f'mapping_2.png'))
    fig_graph.savefig(os.path.join(folder_path, f'graph.png'))
    plt.show()