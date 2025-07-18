import os
import numpy as np
import pprint
import spe_loader as sl
import h5py
from selenium.webdriver.common.devtools.v85.network import emulate_network_conditions

from src.general import SpeFile
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
    from src.general.figure import set_figure
    from scipy.optimize import curve_fit
    import re
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D


    def gaussian(x, A, mu, sigma):
        return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))


    def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
        return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))


    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import numpy as np

    def the_figure0(ax):
        """拟合曲线"""
        set_figure.set_label_and_title(ax, title=f'Time-Resolved PL-50uW', xlabel='Time(s)', ylabel='Wavelength(nm)', zlabel='Intensity(cts)', zlabel_rotation=90, mode='3d', x_label_pad=25, xlabel_rotation=-30, z_label_pad=20, title_pad=0)
        set_figure.set_spines(ax)
        set_figure.set_tick(ax, ticks_xlabel=np.arange(0, 21, 5), ticks_ylabel=np.arange(400, 901, 100), mode='3d', ticks_xlabel_rotation=35)  # Normalized
        ax.zaxis.set_rotate_label(False)
        ax.set_box_aspect([1, 1, 1])
        ax.view_init(elev=20, azim=-45)  # elev 是仰角，azim 是方位角
        ax.grid(True)
        plt.tight_layout()

    datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-3\measurement-3.h5"

    """fig0"""
    with h5py.File(datapath1, "r") as f:
        data = f['OceanOpticsSpectrometer']
        keys_afterSEM = []
        keys_afterSEM.append('1min_50uW_time_series_2_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_10uW__1')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_20uW__0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_50uW__0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_100uW__1')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_200uW__0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_500uW__0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_1000uW__0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_2000uW__1')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_3000uW__0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_2000uW_back_2')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_1000uW_back_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_500uW_back_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_200uW_back_2_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_100uW_back_3')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_50uW_back_1')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_20uW_back_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_10uW_back_1')
        legend_labels_afterSEM = ['10', '20', '50', '100', '200', '500', '1000', '2000', '3000',
                                  '2000*', '1000*', '500*', '200*', '100*', '50*',
                                  '20*', '10*']
        power_afterSEM = [10, 20, 50, 100, 200, 500, 1000, 2000, 3000,
                          2000, 1000, 500, 200, 100, 50, 20, 10]

        fig0 = plt.figure(figsize=(20, 9))
        ax0 = fig0.add_subplot(121, projection='3d')
        sps = []
        for index, key in enumerate(keys_afterSEM):
            if key != '1min_50uW_time_series_2_0':
                continue
            fig0 = plt.figure(figsize=(8 * 1.5, 6 * 1.5))
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

            for i in np.arange(Z.shape[0]):
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

            the_figure0(ax0)

            # from src.general.save_figure import save_subfig
            # plt.savefig(f'D:\\ExpData\\SPE\\20250224_SPE_hBN_afterSEMprocess\\measurement-3\\1min_time_resolved_PL\\{titles_1min_time_resolution[idx]}.png')
            # if val == 1:
            #     break
        plt.show()