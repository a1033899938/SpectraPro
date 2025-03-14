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


    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import numpy as np

    datapath1 = r'D:\XmuNetDisk\20250224_SPE_hBN_afterSEM (1)\20250224_SPE_hBN_afterSEM_test2.h5'

    """fig0"""
    with h5py.File(datapath1, "r") as f:
        data = f['OceanOpticsSpectrometer']
        keys_afterSEM = []
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_10uW__1')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_20uW__0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_50uW__0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_100uW__1')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_200uW__0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_500uW__0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_1000uW__0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_2000uW__1')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_3000uW__0')
        legend_labels_afterSEM = ['10uW', '20uW', '50uW', '100uW', '200uW', '500uW', '1000uW', '2000uW', '3000uW']

        fig0 = plt.figure(figsize=(8, 6))
        ax0 = fig0.add_subplot(111)
        for key in keys_afterSEM:
            sp = data[key]
            bgd = np.array(sp.attrs['background'])
            wav = np.array(sp.attrs['wavelengths'])
            sp_time = sp.attrs['integration_time'] / 1000
            bgd_time = sp.attrs['background_int'] / 1000
            sp = sp / sp_time
            bgd = bgd / bgd_time
            sp = np.array(sp) - bgd

            min_differences = np.abs(wav - 400)
            min_index = np.argmin(min_differences)
            max_differences = np.abs(wav - 900)
            max_index = np.argmin(max_differences)

            x = wav[min_index:max_index]
            y = sp[min_index:max_index]

            ax0.plot(x, y)

    title = f'hBN-after-SEM-process_5kV_5min\n Excitation power-dependent PL spectra (↑)'
    set_figure.set_label_and_title(ax0, title=title, ylabel='Intensity(counts)',
                                   label_fontsize=25, title_fontsize=25,
                                   label_font_family='Times New Roman', title_font_family='Times New Roman',
                                   label_fontweight='bold', title_fontweight='bold',
                                   label_pad=15, title_pad=15)
    set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
    set_figure.set_tick(ax0, xbins=16, ybins=10, fontsize=10, fontweight='bold',
                        linewidth=3, tick_pad=5, direction='in',
                        ticks_xlabel=np.arange(400, 901, 50))  # Normalized
    set_figure.set_legend(ax0, legend_labels=legend_labels_afterSEM, font_size=15, location='upper right')
    ax0.grid(True)
    plt.tight_layout()
    # from src.general.save_figure import save_subfig
    # plt.savefig(r'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-2\\cascade&2d\\20250224_SPE_hBN_afterSEM_measurement2_Graph_increase_power.png')

    """fig1"""
    with h5py.File(datapath1, "r") as f:
        data = f['OceanOpticsSpectrometer']
        keys_afterSEM = []
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_3000uW__0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_2000uW_back_2')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_1000uW_back_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_500uW_back_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_200uW_back_2_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_100uW_back_3')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_50uW_back_1')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_20uW_back_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_5min_expose10s_10uW_back_1')
        keys_afterSEM.reverse()
        legend_labels_afterSEM = ['3000uW', '2000uW', '1000uW', '500uW', '200uW', '100uW', '50uW',
                                  '20uW', '10uW']
        legend_labels_afterSEM.reverse()

        fig0 = plt.figure(figsize=(8, 6))
        ax0 = fig0.add_subplot(111)
        for key in keys_afterSEM:
            sp = data[key]
            bgd = np.array(sp.attrs['background'])
            wav = np.array(sp.attrs['wavelengths'])
            sp_time = sp.attrs['integration_time'] / 1000
            bgd_time = sp.attrs['background_int'] / 1000
            sp = sp / sp_time
            bgd = bgd / bgd_time
            sp = np.array(sp) - bgd

            min_differences = np.abs(wav - 1240 / 2.5)
            min_index = np.argmin(min_differences)
            max_differences = np.abs(wav - 1240 / 1.5)
            max_index = np.argmin(max_differences)

            x = wav[min_index:max_index]
            y = sp[min_index:max_index]

            x = 1240 / x
            ax0.plot(x, y)
    title = (f'Excitation power-dependent PL spectra')
    set_figure.set_label_and_title(ax0, title=title, xlabel='Energy(eV)', ylabel='Intensity(counts)',
                                   label_fontsize=25, title_fontsize=25,
                                   label_font_family='Times New Roman', title_font_family='Times New Roman',
                                   label_fontweight='bold', title_fontweight='bold',
                                   label_pad=15, title_pad=15)
    set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
    set_figure.set_tick(ax0, xbins=16, ybins=10, fontsize=15, fontweight='bold',
                        linewidth=3, tick_pad=5, direction='in',
                        ticks_xlabel=np.arange(1.5, 2.51, 0.1))  # Normalized
    set_figure.set_legend(ax0, legend_labels=legend_labels_afterSEM, font_size=15, location='upper right')
    # ax0.grid(True)
    plt.tight_layout()
    from src.general.save_figure import save_subfig
    plt.savefig(r'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-2\\cascade&2d\\20250224_SPE_hBN_afterSEM_measurement-2_Graph_decrease_power_energy.png')
    plt.show()