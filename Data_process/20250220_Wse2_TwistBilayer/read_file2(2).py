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
    from scipy.signal import find_peaks
    from scipy.optimize import curve_fit


    def gaussian(x, A, mu, sigma):
        return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))


    def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
        return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))

    datapath1 = r'D:\XmuNetDisk\2025-02-20.h5'
    datapath2 = r'D:\XmuNetDisk\2025-02-20（2）.h5'

    fig = plt.figure(figsize=(16, 12))
    ax1 = fig.add_subplot(223)
    legend_labels = []
    A1_ax1 = []
    A2_ax1 = []
    with h5py.File(datapath2, "r") as f:
        # for key in f.keys():
        #     # print(f[key], key, f[key].name, f[key].value) # 因为这里有group对象它是没有value属性的,故会异常。另外字符串读出来是字节流，需要解码成字符串。
        data = f['OceanOpticsSpectrometer']
        for key in data.keys():
            print(key)
            if 'AuNP' in key and 'ML' in key:
                sp = data[key]
                bgd = np.array(sp.attrs['background'])
                wav = np.array(sp.attrs['wavelengths'])
                sp = np.array(sp) - bgd
                ax1.plot(wav, sp/np.max(sp))
                # ax1.plot(wav, sp)
                legend_labels.append(key)

                popt, pcov = curve_fit(double_gaussian, wav, sp / np.max(sp), p0=[1,800, 20, 1, 850, 20])
                A1_fit, mu1_fit, sigma1_fit, A2_fit, mu2_fit, sigma2_fit = popt
                # print(f'拟合结果: A1 = {A1_fit:.2f}, mu1 = {mu1_fit:.2f}, sigma1 = {sigma1_fit:.2f}')
                # print(f'拟合结果: A2 = {A2_fit:.2f}, mu2 = {mu2_fit:.2f}, sigma2 = {sigma2_fit:.2f}')
                y_fit = double_gaussian(wav, *popt)
                A1_ax1.append(mu1_fit)
                A2_ax1.append(mu2_fit)
                ax1.plot(wav, y_fit, 'r-', label='Fitted Gaussian')
    title = 'AuNS/WSe2 ML/AuFilm'
    set_figure.set_label_and_title(ax1, title=title, ylabel='Intensity(counts)',
                                   label_fontsize=25, title_fontsize=25,
                                   label_font_family='Times New Roman', title_font_family='Times New Roman',
                                   label_fontweight='bold', title_fontweight='bold',
                                   label_pad=8, title_pad=15)
    set_figure.set_spines(ax1, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
    set_figure.set_tick(ax1, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                        linewidth=3, tick_pad=5, direction='in',
                        ticks_xlabel=np.linspace(700, 1100, 5))  # Normalized
    set_figure.set_legend(ax1, legend_labels=legend_labels, font_size=10, location='upper right')
    # from src.general.save_figure import save_subfig
    # plt.savefig(os.path.join(datapath2, 'OceanVsMorpho.png'))
    # ax1.set_ylim(0, 1)

    ax2 = fig.add_subplot(224)
    legend_labels = []
    A1_ax2 = []
    A2_ax2 = []
    with h5py.File(datapath2, "r") as f:
        # for key in f.keys():
        #     # print(f[key], key, f[key].name, f[key].value) # 因为这里有group对象它是没有value属性的,故会异常。另外字符串读出来是字节流，需要解码成字符串。
        data = f['OceanOpticsSpectrometer']
        for key in data.keys():
            if 'AuNP' in key and 'BL' in key:
                sp = data[key]
                bgd = np.array(sp.attrs['background'])
                wav = np.array(sp.attrs['wavelengths'])
                sp = np.array(sp) - bgd
                ax2.plot(wav, sp/np.max(sp))
                # ax2.plot(wav, sp)
                legend_labels.append(key)

                popt, pcov = curve_fit(double_gaussian, wav, sp / np.max(sp), p0=[1, 800, 20, 1, 850, 20])
                A1_fit, mu1_fit, sigma1_fit, A2_fit, mu2_fit, sigma2_fit = popt
                # print(f'拟合结果: A1 = {A1_fit:.2f}, mu1 = {mu1_fit:.2f}, sigma1 = {sigma1_fit:.2f}')
                # print(f'拟合结果: A2 = {A2_fit:.2f}, mu2 = {mu2_fit:.2f}, sigma2 = {sigma2_fit:.2f}')
                y_fit = double_gaussian(wav, *popt)
                A1_ax2.append(mu1_fit)
                A2_ax2.append(mu2_fit)
                ax2.plot(wav, y_fit, 'r-', label='Fitted Gaussian')
    title = 'AuNS/WSe2 TBL/AuFilm'
    set_figure.set_label_and_title(ax2, title=title, ylabel='Intensity(counts)',
                                   label_fontsize=25, title_fontsize=25,
                                   label_font_family='Times New Roman', title_font_family='Times New Roman',
                                   label_fontweight='bold', title_fontweight='bold',
                                   label_pad=8, title_pad=15)
    set_figure.set_spines(ax2, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
    set_figure.set_tick(ax2, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                        linewidth=3, tick_pad=5, direction='in',
                        ticks_xlabel=np.linspace(700, 1100, 5))  # Normalized
    set_figure.set_legend(ax2, legend_labels=legend_labels, font_size=10, location='upper right')
    # from src.general.save_figure import save_subfig
    # plt.savefig(os.path.join(datapath2, 'OceanVsMorpho.png'))

    ax3 = fig.add_subplot(221)
    legend_labels = []
    A1_ax3 = []
    A2_ax3 = []
    with h5py.File(datapath2, "r") as f:
        # for key in f.keys():
        #     # print(f[key], key, f[key].name, f[key].value) # 因为这里有group对象它是没有value属性的,故会异常。另外字符串读出来是字节流，需要解码成字符串。
        data = f['OceanOpticsSpectrometer']
        for key in data.keys():
            if 'AuNP' not in key and 'ML' in key:
                sp = data[key]
                bgd = np.array(sp.attrs['background'])
                wav = np.array(sp.attrs['wavelengths'])
                sp = np.array(sp) - bgd
                ax3.plot(wav, sp / np.max(sp))
                # ax3.plot(wav, sp)
                legend_labels.append(key)

                popt, pcov = curve_fit(double_gaussian, wav, sp / np.max(sp), p0=[1, 800, 20, 1, 850, 20])
                A1_fit, mu1_fit, sigma1_fit, A2_fit, mu2_fit, sigma2_fit = popt
                # print(f'拟合结果: A1 = {A1_fit:.2f}, mu1 = {mu1_fit:.2f}, sigma1 = {sigma1_fit:.2f}')
                # print(f'拟合结果: A2 = {A2_fit:.2f}, mu2 = {mu2_fit:.2f}, sigma2 = {sigma2_fit:.2f}')
                y_fit = double_gaussian(wav, *popt)
                A1_ax3.append(mu1_fit)
                A2_ax3.append(mu2_fit)
                ax3.plot(wav, y_fit, 'r-', label='Fitted Gaussian')
    title = 'WSe2 ML/AuFilm'
    set_figure.set_label_and_title(ax3, title=title, ylabel='Intensity(counts)',
                                   label_fontsize=25, title_fontsize=25,
                                   label_font_family='Times New Roman', title_font_family='Times New Roman',
                                   label_fontweight='bold', title_fontweight='bold',
                                   label_pad=8, title_pad=15)
    set_figure.set_spines(ax3, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
    set_figure.set_tick(ax3, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                        linewidth=3, tick_pad=5, direction='in',
                        ticks_xlabel=np.linspace(700, 1100, 5))  # Normalized
    set_figure.set_legend(ax3, legend_labels=legend_labels, font_size=10, location='upper right')
    # from src.general.save_figure import save_subfig
    # plt.savefig(os.path.join(datapath2, 'OceanVsMorpho.png'))

    ax4 = fig.add_subplot(222)
    legend_labels = []
    A1_ax4 = []
    A2_ax4 = []
    with h5py.File(datapath2, "r") as f:
        # for key in f.keys():
        #     # print(f[key], key, f[key].name, f[key].value) # 因为这里有group对象它是没有value属性的,故会异常。另外字符串读出来是字节流，需要解码成字符串。
        data = f['OceanOpticsSpectrometer']
        for key in data.keys():
            if 'AuNP' not in key and 'BL' in key:
                sp = data[key]
                bgd = np.array(sp.attrs['background'])
                wav = np.array(sp.attrs['wavelengths'])
                sp = np.array(sp) - bgd
                ax4.plot(wav, sp / np.max(sp))
                # ax4.plot(wav, sp)
                legend_labels.append(key)

                popt, pcov = curve_fit(double_gaussian, wav, sp / np.max(sp), p0=[1, 800, 20, 1, 850, 20])
                A1_fit, mu1_fit, sigma1_fit, A2_fit, mu2_fit, sigma2_fit = popt
                # print(f'拟合结果: A1 = {A1_fit:.2f}, mu1 = {mu1_fit:.2f}, sigma1 = {sigma1_fit:.2f}')
                # print(f'拟合结果: A2 = {A2_fit:.2f}, mu2 = {mu2_fit:.2f}, sigma2 = {sigma2_fit:.2f}')
                y_fit = double_gaussian(wav, *popt)
                A1_ax4.append(mu1_fit)
                A2_ax4.append(mu2_fit)
                ax4.plot(wav, y_fit, 'r-', label='Fitted Gaussian')
    title = 'WSe2 TBL/AuFilm'
    set_figure.set_label_and_title(ax4, title=title, ylabel='Intensity(counts)',
                                   label_fontsize=25, title_fontsize=25,
                                   label_font_family='Times New Roman', title_font_family='Times New Roman',
                                   label_fontweight='bold', title_fontweight='bold',
                                   label_pad=8, title_pad=15)
    set_figure.set_spines(ax4, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
    set_figure.set_tick(ax4, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                        linewidth=3, tick_pad=5, direction='in',
                        ticks_xlabel=np.linspace(700, 1100, 5))  # Normalized
    set_figure.set_legend(ax4, legend_labels=legend_labels, font_size=10, location='upper right')
    fig.tight_layout()
    # 设置刻度为科学计数法
    set_figure.set_scientific_y_ticks(ax1, 12, 'bold')
    set_figure.set_scientific_y_ticks(ax2, 12, 'bold')
    set_figure.set_scientific_y_ticks(ax3, 12, 'bold')
    set_figure.set_scientific_y_ticks(ax4, 12, 'bold')

    ax1.set_xlim(700, 1000)
    ax2.set_xlim(700, 1000)
    ax3.set_xlim(700, 1000)
    ax4.set_xlim(700, 1000)

    from src.general import save_subfig
    plt.savefig(r'D:\\XmuNetDisk\\WSe2_TBL_PL.png')

    print("A1_ax1:")
    print(A1_ax1)
    print("A2_ax1:")
    print(A2_ax1)

    print("A1_ax2:")
    print(A1_ax2)
    print("A2_ax2:")
    print(A2_ax2)

    print("A1_ax3:")
    print(A1_ax3)
    print("A2_ax3:")
    print(A2_ax3)

    print("A1_ax4:")
    print(A1_ax4)
    print("A2_ax4:")
    print(A2_ax4)

    fig2 = plt.figure(figsize=(8, 6))
    ax5 = fig.add_subplot(221)
    ax5.hist(A1_ax1 + A2_ax1, bins=100, edgecolor='black')  # bins设置间隔为5
    set_figure.set_label_and_title(ax5, title=title, ylabel='Intensity(counts)',
                                   label_fontsize=25, title_fontsize=25,
                                   label_font_family='Times New Roman', title_font_family='Times New Roman',
                                   label_fontweight='bold', title_fontweight='bold',
                                   label_pad=8, title_pad=15)
    set_figure.set_spines(ax5, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
    set_figure.set_tick(ax5, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                        linewidth=3, tick_pad=5, direction='in',
                        ticks_xlabel=np.linspace(700, 1100, 5))  # Normalized
    set_figure.set_legend(ax5, legend_labels=legend_labels, font_size=10, location='upper right')

    ax6 = fig.add_subplot(222)
    ax6.hist(A1_ax2 + A2_ax2, bins=100, edgecolor='black')  # bins设置间隔为5

    ax7 = fig.add_subplot(223)
    ax7.hist(A1_ax3 + A2_ax3, bins=100, edgecolor='black')  # bins设置间隔为5

    ax8 = fig.add_subplot(224)
    ax8.hist(A1_ax4 + A2_ax4, bins=100, edgecolor='black')  # bins设置间隔为5
    plt.show()