import os
import numpy as np
import pprint
import spe_loader as sl
import h5py
from selenium.webdriver.common.devtools.v85.network import emulate_network_conditions

from src.general.winspec import SpeFile
import src.spe2py.spe2py as spe
import scipy.io as sio


class read_file:
    def __init__(self, filepath, strip='all', show_data_flag=True):
        self.filepath = filepath
        self.strip = strip
        self.show_data_flag = show_data_flag
        self.filetype = None
        self.data = None
        self.determine_filetype()
        self.data = self.read_data()

    def determine_filetype(self):
        """determine_filetype"""
        self.filetype = os.path.splitext(self.filepath)[1]
        return self.filetype

    def read_data(self):
        if self.filetype == '.spe':
            return self.read_spe()
        elif self.filetype == '.mat':
            return self.read_mat()
        elif self.filetype == '.txt':
            return self.read_txt()
        elif self.filetype == '.h5':
            return self.read_h5()
        else:
            raise ValueError("Unsupported file type")

    def read_spe(self):
        try:
            print('path now:')
            print(self.filepath)
            sp = sl.load_from_files([self.filepath])
            data = {}
            if sp.xdim[0] > sp.ydim[0]:
                data['xdim'] = sp.xdim[0]
                data['ydim'] = sp.ydim[0]
                data['intensity_image'] = np.squeeze(np.array(sp.data))
                data['wavelength'] = sp.wavelength
                data['strip'] = range(data['ydim'])
            else:
                data['xdim'] = sp.ydim[0]
                data['ydim'] = sp.xdim[0]
                data['intensity_image'] = np.transpose(np.squeeze(np.array(sp.data)))
                data['wavelength'] = sp.wavelength
                data['strip'] = range(data['ydim'])

            if self.strip == 'all':
                data['intensity'] = np.sum(data['intensity_image'], axis=0)
            else:
                self.strip = np.array(self.strip)
                data['intensity'] = np.sum(data['intensity_image'][self.strip.min():self.strip.max(), :], axis=0)

            if self.show_data_flag:
                print("==========data==========")
                pprint.pprint(data)
                print("========data end========")
            return data
        except Exception as e:
            print(f"Error read_file.read_spe:\n  |--> {e}")

    def read_mat(self):
        try:
            print('path now:')
            print(self.filepath)
            mat_data = sio.loadmat(self.filepath, squeeze_me=True, struct_as_record=False)
            sp = matstruct_to_dict(mat_data['spnow'])
            print(sp['xdim'])
            print(dir(sp))
            data = {}
            if sp['xdim'] > sp['ydim']:
                data['xdim'] = sp['xdim']
                data['ydim'] = sp['ydim']
                data['intensity_image'] = np.squeeze(np.array(sp['int']))
                data['wavelength'] = sp['wavelength']
                data['strip'] = range(data['ydim'])
            else:
                data['xdim'] = sp['ydim']
                data['ydim'] = sp['xdim']
                data['intensity_image'] = np.transpose(np.squeeze(np.array(sp['int'])))
                data['wavelength'] = sp['wavelength']
                data['strip'] = range(data['ydim'])

            if self.strip == 'all':
                data['intensity'] = np.sum(data['intensity_image'], axis=0)
            else:
                self.strip = np.array(self.strip)
                data['intensity'] = np.sum(data['intensity_image'][self.strip.min():self.strip.max(), :], axis=0)

            if self.show_data_flag:
                print("==========data==========")
                pprint.pprint(data)
                print("========data end========")
            return data
        except Exception as e:
            print(f"Error read_file.read_spe:\n  |--> {e}")

    def read_txt(self):
        try:
            with open(self.filepath, "r") as f:  # 打开文件
                sp = np.loadtxt(f, usecols=(0, 1), skiprows=0)

            data = {}
            data['wavelength'] = sp[:, 0]
            data['intensity'] = sp[:, 1]

            if self.show_data_flag:
                print("==========data==========")
                pprint.pprint(data)
                print("========data end========")
            return data
        except Exception as e:
            print(f"Error read_file.read_txt:\n  |--> {e}")

    def read_h5(self):
        try:
            pass
        except Exception as e:
            print(f"Error read_file.read_h5:\n  |--> {e}")


def matstruct_to_dict(matstruct):
    """
    递归函数，用于将 mat_struct 对象转换为字典。
    """
    if isinstance(matstruct, sio.matlab.mio5_params.mat_struct):
        d = {}
        for field_name in matstruct._fieldnames:
            item = getattr(matstruct, field_name)
            if isinstance(item, sio.matlab.mio5_params.mat_struct):
                d[field_name] = matstruct_to_dict(item)
            else:
                d[field_name] = item
        return d
    else:
        return matstruct


if __name__ == '__main__':
    import h5py
    from shutil import copyfile
    import pySPM
    import matplotlib.pyplot as plt
    import pprint
    from src.general import set_figure
    from scipy.optimize import curve_fit
    import re
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D


    def gaussian(x, A, mu, sigma):
        return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))


    def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
        return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))


    def replace_outliers_with_bounds(data):
        """
        用上下边界值替代异常值
        :param data: 输入数据（列表或一维数组）
        :return: 替换异常值后的数据
        """
        data = np.array(data)
        Q1 = np.percentile(data, 25)
        Q3 = np.percentile(data, 75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # 用边界值替代异常值
        data[data < lower_bound] = lower_bound
        data[data > upper_bound] = upper_bound
        return data.tolist()

    """中值去噪"""
    def replace_outliers_with_median(data, threshold=3):
        """
        用中位数替代异常值
        :param data: 输入数据（列表或一维数组）
        :param threshold: Z-Score 阈值，默认 3
        :return: 替换异常值后的数据
        """
        data = np.array(data)
        median = np.median(data)
        std = np.std(data)
        z_scores = (data - np.mean(data)) / std
        data[np.abs(z_scores) > threshold] = median  # 用中位数替代异常值
        return data.tolist()


    def replace_outliers_manually(sp, wav_min, wav_max, threshold, half_window=4):
        min_differences = np.abs(wav - wav_min)
        min_index = np.argmin(min_differences)
        max_differences = np.abs(wav - wav_max)
        max_index = np.argmin(max_differences)

        # 波段内的数据
        data = sp[min_index:max_index]
        mean = np.mean(sorted(data)[:-5])  # 去除最大的五个值

        # 比阈值大的所有值的索引
        idxs = abs(data - mean) > threshold
        noise_value = data[idxs[0]]

        # # 这些阈值附近的窗口
        # for idx in idxs:
        data_window = data[idxs[0]-half_window:idxs[0]+half_window]
        data_window[abs(data_window - noise_value) < noise_value * 0.9] = 0
        mean_window = np.mean(data_window)
        data[idxs] = mean_window

        sp[min_index:max_index] = data
        return sp


    def replace_outliers(data, wavelength_range, threshold, tolerance=0.1):
        """
        对指定波长范围内的数据，如果有值大于阈值，则用该值附近10个数据点（去除与该值相近的所有值）的平均值来替代与该值相近的所有值。

        参数:
            data (numpy.ndarray): 数据数组，假设为二维数组，第一列是波长，第二列是值。
            wavelength_range (tuple): 波长范围，例如 (400, 700)。
            threshold (float): 阈值，大于该值的点会被处理。
            tolerance (float): 判断“相近”的容差范围。

        返回:
            numpy.ndarray: 处理后的数据。
        """
        # 筛选指定波长范围内的数据
        min_differences = np.abs(wav - wavelength_range[0])
        min_index = np.argmin(min_differences)
        max_differences = np.abs(wav - wavelength_range[1])
        max_index = np.argmin(max_differences)

        filtered_data = data[min_index:max_index]

        # 找到大于阈值的值
        outlier_indices = np.where(filtered_data > threshold)[0]

        # 遍历所有大于阈值的点
        for idx in outlier_indices:
            outlier_value = filtered_data[idx]

            # 找到与该值相近的所有点
            close_indices = np.where(np.abs(filtered_data[:] - outlier_value) <= tolerance)[0]

            # 提取附近10个数据点（排除相近的点）
            start = max(0, idx - 10 - len(close_indices))
            end = min(len(filtered_data), idx + 10 + len(close_indices))
            nearby_values = filtered_data[start:end]

            # 排除相近的点
            nearby_values = nearby_values[np.abs(nearby_values - outlier_value) > tolerance]

            # 如果附近有足够的数据点，计算平均值并替换
            if len(nearby_values) >= 10:
                avg_value = np.mean(nearby_values[:10])  # 取前10个数据点的平均值
                filtered_data[close_indices] = avg_value  # 替换相近的所有值

        # 将处理后的数据合并回原始数据
        data[min_index:max_index] = filtered_data
        return data

    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import numpy as np

    datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-3\20250224_SPE_hBN_afterSEM_measurement-3.h5"

    """fig0"""
    with h5py.File(datapath1, "r") as f:
        data = f['OceanOpticsSpectrometer']
        print(np.shape(data['1min_10uW_time_series_2_0']))
        keys_1min_time_resolution = []
        keys_1min_time_resolution.append('1min_10uW_time_series_2_0')
        keys_1min_time_resolution.append('1min_20uW_time_series_2_0')
        keys_1min_time_resolution.append('1min_50uW_time_series_2_0')
        keys_1min_time_resolution.append('1min_100uW_time_series_0')
        keys_1min_time_resolution.append('1min_500uW_time_series_0')
        keys_1min_time_resolution.append('1min_1000uW_time_series_0')
        keys_1min_time_resolution.append('1min_2000uW_time_series_0')
        keys_1min_time_resolution.append('1min_3000uW_time_series_0')
        keys_1min_time_resolution.append('1min_2000uW_back_time_series_0')
        keys_1min_time_resolution.append('1min_1000uW_back_time_series_0')
        keys_1min_time_resolution.append('1min_500uW_back_time_series_0')
        keys_1min_time_resolution.append('1min_200uW_back_time_series_0')
        keys_1min_time_resolution.append('1min_100uW_back_time_series_0')
        keys_1min_time_resolution.append('1min_50uW_back_time_series_0')
        keys_1min_time_resolution.append('1min_20uW_back_time_series_0')
        keys_1min_time_resolution.append('1min_10uW_back_time_series_0')


        titles_1min_time_resolution = ['10uW', '20uW', '50uW', '100uW', '500uW', '1000uW', '2000uW', '3000uW',
                                  '2000uW_back', '1000uW_back', '500uW_back', '200uW_back', '100uW_back', '50uW_back',
                                  '20uW_back', '10uW_back']
        # plt.close('all')
        for idx, key in enumerate(keys_1min_time_resolution):
            fig0 = plt.figure(figsize=(12, 9))
            ax0 = fig0.add_subplot(111, projection='3d')
            sps = data[key]
            bgd = np.array(sps.attrs['background'])
            wav = np.array(sps.attrs['wavelengths'])
            sp_time = sps.attrs['integration_time'] / 1000
            bgd_time = sps.attrs['background_int'] / 1000
            bgd, _ = np.meshgrid(bgd, np.arange(0, sps.shape[0]))
            sps = sps / sp_time
            bgd = bgd / bgd_time
            sps = sps - bgd

            x = wav
            print(np.shape(x))
            Z = np.array(sps)
            y = np.arange(Z.shape[0])

            # """IQR法去噪点"""
            # for row in range(Z.shape[0]):
            #     min_differences = np.abs(wav - 480)
            #     min_index = np.argmin(min_differences)
            #     max_differences = np.abs(wav - 750)
            #     max_index = np.argmin(max_differences)
            #     Z[row, 0:min_index] = replace_outliers_with_bounds(Z[row, 0:min_index])
            #     Z[row, max_index:-1] = replace_outliers_with_bounds(Z[row, max_index:-1])

            """手动去噪"""
            val = 0
            if key == '1min_10uW_time_series_2_0':
                for row in range(Z.shape[0]):
                    Z[row, :] = replace_outliers(Z[row, :], (399, 500), 10)
                    Z[row, :] = replace_outliers(Z[row, :], (510, 570), 80)
                    Z[row, :] = replace_outliers(Z[row, :], (800, 900), 7)
            elif key == '1min_10uW_back_time_series_0':
                for row in range(Z.shape[0]):
                    Z[row, :] = replace_outliers(Z[row, :], (650, 750), 8)
                    Z[row, :] = replace_outliers(Z[row, :], (900, 1100), 8)
            elif key == '1min_20uW_time_series_2_0':
                for row in range(Z.shape[0]):
                    Z[row, :] = replace_outliers(Z[row, :], (399, 500), 15)
                    Z[row, :] = replace_outliers(Z[row, :], (700, 800), 30)
                    Z[row, :] = replace_outliers(Z[row, :], (900, 1100), 10)
            elif key == '1min_50uW_time_series_2_0':
                for row in range(Z.shape[0]):
                    Z[row, :] = replace_outliers(Z[row, :], (399, 500), 15)
            elif key == '1min_50uW_back_time_series_0':
                for row in range(Z.shape[0]):
                    Z[row, :] = replace_outliers(Z[row, :], (399, 500), 5)
                    Z[row, :] = replace_outliers(Z[row, :], (750, 850), 5)
            elif key == '1min_100uW_back_time_series_0':
                for row in range(Z.shape[0]):
                    Z[row, :] = replace_outliers(Z[row, :], (1000, 1100), 5)
            elif key == '1min_500uW_time_series_0':
                for row in range(Z.shape[0]):
                    Z[row, :] = replace_outliers(Z[row, :], (400, 500), 10)
            elif key == '1min_500uW_back_time_series_0':
                for row in range(Z.shape[0]):
                    Z[row, :] = replace_outliers(Z[row, :], (700, 800), 10)
            elif key == '1min_1000uW_back_time_series_0':
                for row in range(Z.shape[0]):
                    Z[row, :] = replace_outliers(Z[row, :], (900, 1000), 10)
            elif key == '1min_2000uW_time_series_0':
                for row in range(Z.shape[0]):
                    Z[row, :] = replace_outliers(Z[row, :], (700, 800), 10)
            elif key == '1min_2000uW_back_time_series_0':
                for row in range(Z.shape[0]):
                    Z[row, :] = replace_outliers(Z[row, :], (800, 900), 10)
                    # val = 1

            min_differences = np.abs(wav - 400)
            min_index = np.argmin(min_differences)
            max_differences = np.abs(wav - 900)
            max_index = np.argmin(max_differences)
            x = x[min_index:max_index]
            Z = Z[:, min_index:max_index]
            print(np.shape(Z))
            print(np.shape(x))
            print(np.shape(y))
            X, Y = np.meshgrid(x, y)

            for i in y:
                ax0.plot(Y[i], X[i], Z[i], color=plt.cm.viridis(i / len(y)),
                         linestyle='-', linewidth=1, alpha=1)
                ax0.plot(Y[i], X[i], np.zeros_like(Z[i]), color='gray', alpha=1)

                polygon = [
                    [Y[i, 0], X[i, 0], 0],  # 左下
                    [Y[i, -1], X[i, -1], 0],  # 右下
                ]
                for j in range(len(x) - 1, -1, -1):  # 依次添加点，使得polygon成为一个完整的闭合多边形
                    polygon.append([Y[i, j], X[i, j], Z[i, j]])
                ax0.add_collection3d(Poly3DCollection([polygon], color=plt.cm.viridis(i / len(y)), alpha=0.5))

            title = f'hBN-after-SEM-process_1min Time-Resolved PL\n{titles_1min_time_resolution[idx]}'
            set_figure.set_label_and_title(ax0, title=title, xlabel='Process time(min)', ylabel='Intensity(counts)',
                                           label_fontsize=25, title_fontsize=25,
                                           label_font_family='Times New Roman', title_font_family='Times New Roman',
                                           label_fontweight='bold', title_fontweight='bold',
                                           label_pad=15, title_pad=15, mode='3d')
            set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
            set_figure.set_tick(ax0, xbins=6, ybins=10, fontsize=10, fontweight='bold',
                                linewidth=3, tick_pad=5, direction='in',
                                ticks_xlabel=np.arange(0, 20, 2),
                                ticks_ylabel=np.arange(400, 901, 100), mode='3d')  # Normalized
            ax0.set_xlabel(xlabel='Measurement  sequence', labelpad=15)
            ax0.set_ylabel(ylabel='Wavelength(nm)', labelpad=15)
            ax0.zaxis.set_rotate_label(False)
            ax0.set_zlabel(zlabel='Intensity(counts)', rotation=90, labelpad=15)

            ax0.set_box_aspect([1, 1, 1])
            ax0.view_init(elev=20, azim=45)  # elev 是仰角，azim 是方位角
            # plt.tight_layout()
            ax0.grid(True)

            # from src.general.save_figure import save_subfig
            # plt.savefig(f'D:\\ExpData\\SPE\\20250224_SPE_hBN_afterSEMprocess\\measurement-3\\1min_time_resolved_PL\\{titles_1min_time_resolution[idx]}.png')
            # if val == 1:
            #     break
    plt.show()