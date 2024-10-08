import os
import numpy as np


def save_figure_data_as_txt(ax, save_fullpath):
    lines = ax.get_lines()
    with open(save_fullpath, 'w') as file:
        for line in lines:
            xdata = line.get_xdata()
            ydata = line.get_ydata()

            # 写入数据到文件
            file.write('X data:\n')
            for xi in xdata:
                file.write(f'{xi}\n')

            file.write('Y data:\n')
            for yi in ydata:
                file.write(f'{yi}\n')


def save_image_data_as_npz(ax, save_fullpath):
    dir_path = os.path.dirname(save_fullpath)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    data_to_save = {}
    data_to_save['image'] = ax.images[0].get_array().data  # 获取数据
    np.savez(save_fullpath, **data_to_save)


def save_graph_data_as_npz(ax, save_fullpath):
    data_to_save = {}
    lines = ax.get_lines()
    for i, line in enumerate(lines):
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        data_to_save[f'xdata_{i}'] = xdata
        data_to_save[f'ydata_{i}'] = ydata

    # 保存数据为 .npz 文件
    np.savez(save_fullpath, **data_to_save)


def load_graph_data_from_npz(npz_file_path):
    # 读取 .npz 文件
    data = np.load(npz_file_path)

    # 还原数据
    lines_data = []
    for key in data.keys():
        if key.startswith('xdata_'):
            index = key.split('_')[-1]  # 提取索引
            xdata = data[key]
            ydata_key = f'ydata_{index}'
            if ydata_key in data:
                ydata = data[ydata_key]
                lines_data.append((xdata, ydata))

    return lines_data
