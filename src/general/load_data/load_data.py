import os.path
import h5py
import numpy as np
import matplotlib.pyplot as plt
from src.my_style.my_mapping_para import *

def load_mapping(h5_file, dir_name, group_name, sp_name, save_sub_folder, calculate_mapping_para=None, bgd_name=None):
    mapping_paras = {}

    if bgd_name is None:
        print(f"Read 'bgd' from first file.")
    with h5py.File(h5_file, "r") as f:
        # 读取mapping group
        data = f[dir_name][group_name]

        # 读取group下的keys（子group）和第一个子group下的所有keys（sp）
        row_keys = data.keys()
        row1_key = list(data.keys())[0]
        row1 = data[row1_key]
        column_keys_of_row1 = row1.keys()

        # 创建储存mapping数据的空数组
        mapping_shape = [len(row_keys), len(column_keys_of_row1)]
        empty_mapping = np.zeros([mapping_shape[0], mapping_shape[1]])

        if bgd_name is None:
            bgd_name = f'{dir_name}/{group_name}/x-0/{sp_name}-x0-y0'  # 读取第一个子group下的第一个sp的bgd

        # 读取第一个子group下的第一个sp的bgd和wav，并对积分时间作归一化
        bgd = np.array(f[bgd_name].attrs['background'])
        bgd_time = f[bgd_name].attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        wav = np.array(f[bgd_name].attrs['wavelengths'])

        # 历遍所有sp
        for i in range(mapping_shape[0]):
            parent_key = f"x-{i}"
            for j in range(mapping_shape[1]):
                print(f"i now: {i}, j now: {j}")
                child_key = f"{sp_name}-x{i}-y{j}"
                sp = data[f"{parent_key}/{child_key}"]
                sp_time = sp.attrs['integration_time'] / 1000
                sp = np.array(sp)
                sp = sp / sp_time
                sp = sp - bgd

                fitting_paras = calculate_mapping_para(wav, sp)
                if i == 0 and j == 0:
                    for key, value in fitting_paras.items():
                        mapping_paras[key] = np.zeros_like(empty_mapping)  # 以返回的参数字典的key作为这种变量对应mapping的参数名，并且创建空数组

                # 保存数据
                for key, value in fitting_paras.items():
                    mapping_paras[key][i][j] = value
    create_folder(save_sub_folder)
    np.save(os.path.join(save_sub_folder, "mapping_paras.npz"), mapping_paras)
    return mapping_paras

if __name__ == '__main__':
    """读取mapping数据"""
    h5_file = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-9\20250224_SPE_hBN_afterSEM_measurement-9.h5"
    mapping_paras = load_mapping(
                        h5_file=h5_file,
                        dir_name='OceanOpticsSpectrometer',
                        group_name='hBN_afterSEM_mapping_6',
                        sp_name='hBN_1-2_beforeSEM_mapping',
                        save_sub_folder=os.path.join(os.path.dirname(h5_file), 'hBN_afterSEM_mapping_6'),
                        calculate_mapping_para=triple_peaks_fitting,
                        bgd_name=None)

    for key, value in mapping_paras.items():
        print('\n')
        print(key)
        print(np.shape(value))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(value)
    plt.show()

