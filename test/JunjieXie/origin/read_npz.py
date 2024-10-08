import numpy as np
import matplotlib.pyplot as plt


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


def plot_lines_from_data(lines_data):
    fig, ax = plt.subplots()
    for xdata, ydata in lines_data:
        ax.plot(xdata, ydata)
    plt.show()


if __name__ == '__main__':
    # folder_path = r'C:\Users\a1033\Desktop\Contemporary\240806-240808\20240914process\npz'
    # npz_file_path = r'C:\Users\a1033\Desktop\Contemporary\240806-240808\20240914process\npz\8#.npz'
    # extensions = '.npz'
    # file_paths, files, file_names = GeneralMethods.list_files_in_directory(folder_path, extensions)
    #
    # # for file_path, file_name in zip(file_paths, file_names):
    # #     data = np.load(file_path)
    # #     for key in data:
    # #         print(f'{key}: {data[key]}')
    npz_file_path = r'D:\GitProject\SpectraPro\tests\data_processing\ParticleScannerScan_0\Tiles\tile_0.npz'
    # lines_data = load_graph_data_from_npz(npz_file_path)
    # plot_lines_from_data(lines_data)

    loaded = np.load(npz_file_path)
    image_data = loaded['image']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(image_data)
    plt.show()
