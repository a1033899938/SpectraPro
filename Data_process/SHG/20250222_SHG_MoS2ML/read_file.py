import os
import numpy as np
import pprint
import spe_loader as sl
import h5py
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
                data['intensity_image'] = np.squeeze(np.array(sp.data0))
                data['wavelength'] = sp.wavelength
                data['strip'] = range(data['ydim'])
            else:
                data['xdim'] = sp.ydim[0]
                data['ydim'] = sp.xdim[0]
                data['intensity_image'] = np.transpose(np.squeeze(np.array(sp.data0)))
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


    def gaussian(x, A, mu, sigma):
        return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))


    def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
        return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))

    # # 启用 LaTeX 渲染
    # plt.rcParams['text.usetex'] = True
    # plt.rcParams['font.family'] = 'sans-serif'  # 设置字体为无衬线字体
    # plt.rcParams['font.sans-serif'] = ['Helvetica']  # 设置具体字体名称
    datapath = r'D:\XmuNetDisk\20250222_SHG_MoS2ML\2025-02-22_SHG_MoS2ML.h5'
    legend_labels = []
    fig = plt.figure(figsize=(16, 12))
    ax1 = fig.add_subplot(111)
    with h5py.File(datapath, "r") as f:
        data = f['OceanOpticsSpectrometer']
        for key in data.keys():
            print(key)
            sp = data[key]

            bgd_int_time = sp.attrs['background_int'] / 1000  # 单位由ms换为s
            ref_int_time = sp.attrs['reference_int'] / 1000
            sp_int_time = sp.attrs['integration_time'] / 1000

            wav = np.array(sp.attrs['wavelengths'])
            bgd = np.array(sp.attrs['background']) / bgd_int_time
            ref = np.array(sp.attrs['reference']) / ref_int_time
            sp = data[key] / sp_int_time

            sp = (np.array(sp) - bgd) / (np.array(ref) - bgd)
            ax1.plot(wav, sp)
            legend_labels.append(key)

            # popt, pcov = curve_fit(double_gaussian, wav, sp, p0=[1, 600, 50, 1, 800, 50])
            # A1_fit, mu1_fit, sigma1_fit, A2_fit, mu2_fit, sigma2_fit = popt
            # print(f'拟合结果: A1 = {A1_fit:.2f}, mu1 = {mu1_fit:.2f}, sigma1 = {sigma1_fit:.2f}')
            # print(f'拟合结果: A2 = {A2_fit:.2f}, mu2 = {mu2_fit:.2f}, sigma2 = {sigma2_fit:.2f}')
            # y_fit = double_gaussian(wav, *popt)
            # ax1.plot(wav, y_fit, 'r-', label='Fitted Gaussian')

    title = f'AuNP/MoS2/AuFilm Dark Field Scattering'
    set_figure.set_label_and_title(ax1, title=title, ylabel='Normalized Intensity(a.u.)',
                                   label_fontsize=25, title_fontsize=25,
                                   label_font_family='Times New Roman', title_font_family='Times New Roman',
                                   label_fontweight='bold', title_fontweight='bold',
                                   label_pad=8, title_pad=15)
    set_figure.set_spines(ax1, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
    set_figure.set_tick(ax1, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                        linewidth=3, tick_pad=5, direction='in',
                        ticks_xlabel=np.linspace(400, 1100, 8))  # Normalized
    set_figure.set_legend(ax1, legend_labels=legend_labels, font_size=15, location='upper right')

    from src.general import save_subfig
    plt.savefig(r'D:\\XmuNetDisk\\20250222_SHG_NP_DF.png')
    fig.tight_layout()
    plt.show()