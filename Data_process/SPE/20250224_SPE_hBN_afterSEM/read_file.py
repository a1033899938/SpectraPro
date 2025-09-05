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
    import re
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D


    def gaussian(x, A, mu, sigma):
        return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))


    def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
        return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))

    # # 启用 LaTeX 渲染
    # plt.rcParams['text.usetex'] = True
    # plt.rcParams['font.family'] = 'sans-serif'  # 设置字体为无衬线字体
    # plt.rcParams['font.sans-serif'] = ['Helvetica']  # 设置具体字体名称
    datapath1 = r'D:\XmuNetDisk\20250224_SPE_hBN_afterSEM\20250224_SPE_hBN_afterSEM.h5'

    legend_labels = []
    sp_mag = np.zeros((6, 4))
    print(sp_mag)
    fig2 = plt.figure(figsize=(8, 6))
    ax2 = fig2.add_subplot(111)
    with h5py.File(datapath1, "r") as f:
        data = f['OceanOpticsSpectrometer']
        keys = [key for key in data.keys()]
        keys.remove('hBN_10keV_5min_1')
        keys.remove('hBN_10keV_5min_1_0')
        keys.remove('hBN-1_0')
        keys.remove('hBN-2_0')
        keys.remove('hBN-2_after5min_0')
        keys.remove('hBN-1_1')
        keys.remove('hBN_10keV_1min_0')
        keys.remove('hBN_10keV_2min_0')
        keys.remove('hBN_10keV_5min_0')
        keys.remove('hBN_10keV_1min_100KX_0')
        keys.remove('hBN_15keV_5min_100KX_0')
        for key in keys:
            print(key)
            fig1 = plt.figure(figsize=(8, 6))
            ax1 = fig1.add_subplot(111)

            sp = data[key]
            bgd = np.array(sp.attrs['background'])
            wav = np.array(sp.attrs['wavelengths'])
            sp_time = sp.attrs['integration_time'] / 1000
            bgd_time = sp.attrs['background_int'] / 1000
            sp = sp / sp_time
            bgd = bgd / bgd_time
            sp = np.array(sp) - bgd

            ax1.plot(wav, sp)
            ax2.plot(wav, sp)
            legend_labels.append(key)

            # 拟合
            popt, pcov = curve_fit(gaussian, wav, sp, p0=[100, 550, 100])
            A_fit, mu_fit, sigma_fit = popt
            print(f'拟合结果: A = {A_fit:.2f}, mu = {mu_fit:.2f}, sigma = {sigma_fit:.2f}')
            y_fit = gaussian(wav, *popt)
            ax1.plot(wav, y_fit, 'r-', label='Fitted Gaussian')
            plt.close(fig1)

            if '15keV' in key:
                r = 2
            elif '10keV' in key:
                r = 1
            elif '5keV' in key:
                r = 0
            else:
                print('error')

            if  '0.5min' in key:
                c = 0
            elif '1min' in key:
                c = 1
            elif '2min' in key:
                c = 2
            elif '5min' in key:
                c = 3
            else:
                print('error')

            if '100KX' in key:
                r = r + 3
            elif 'SEM' in key:
                continue
            elif 'sub' in key:
                continue
            else:
                pass
            sp_mag[r][c] = A_fit
            print(f'r = {r}, c = {c}')
    # 绘制 3D 图
    x = [5, 10, 15, 20, 25, 30]
    y = [0.5, 1, 2, 5]

    z = np.array(sp_mag)
    print(np.shape(x[0] * len(y)))
    print(np.shape(y))
    print(np.shape(z[0][:]))
    fig0 = plt.figure(figsize=(8, 6))
    # ax0 = fig0.add_subplot(111, projection='3d')
    # ax0.plot([x[0]] * len(y), y, z[0][:], label='Curve 1: y=1')
    # ax0.plot([x[1]] * len(y), y, z[1][:], label='Curve 2: y=2')
    # ax0.plot([x[2]] * len(y), y, z[2][:], label='Curve 3: y=3')
    # ax0.plot([x[3]] * len(y), y, z[3][:], label='Curve 4: y=4')
    # ax0.plot([x[4]] * len(y), y, z[4][:], label='Curve 5: y=5')
    # ax0.plot([x[5]] * len(y), y, z[5][:], label='Curve 6: y=6')
    ax0 = fig0.add_subplot(111)
    ax0.plot(y, z[0][:], label='5keV_60KX')
    ax0.plot(y, z[1][:], label='10keV_60KX')
    ax0.plot(y, z[2][:], label='15keV_60KX')
    ax0.plot(y, z[3][:], label='5keV_100KX')
    ax0.plot(y, z[4][:], label='10keV_100KX')
    ax0.plot(y, z[5][:], label='15keV_100KX')
    legend_labels0 = ['5keV_60KX', '10keV_60KX', '15keV_60KX', '5keV_100KX', '10keV_100KX', '15keV_100KX']

    # from src.general.save_figure import save_subfig
    # plt.savefig(r'D:\\XmuNetDisk\\WSe2_ML_PL.png')
    # fig.tight_layout()
    title = 'hBN-after-SEM-process'
    set_figure.set_label_and_title(ax2, title=title, ylabel='Intensity(counts)',
                                   label_fontsize=25, title_fontsize=25,
                                   label_font_family='Times New Roman', title_font_family='Times New Roman',
                                   label_fontweight='bold', title_fontweight='bold',
                                   label_pad=8, title_pad=15)
    set_figure.set_spines(ax2, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
    set_figure.set_tick(ax2, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                        linewidth=3, tick_pad=5, direction='in',
                        ticks_xlabel=np.linspace(400, 1100, 15))  # Normalized
    set_figure.set_legend(ax2, legend_labels=legend_labels, font_size=7, location='upper right')


    title = 'hBN-after-SEM-process'
    set_figure.set_label_and_title(ax0, title=title, xlabel='Process time(min)', ylabel='Intensity(counts)',
                                   label_fontsize=25, title_fontsize=25,
                                   label_font_family='Times New Roman', title_font_family='Times New Roman',
                                   label_fontweight='bold', title_fontweight='bold',
                                   label_pad=8, title_pad=15)
    set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
    set_figure.set_tick(ax0, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                        linewidth=3, tick_pad=5, direction='in')  # Normalized
    set_figure.set_legend(ax0, legend_labels=legend_labels0, font_size=15, location='upper right')

    # fig2.savefig(r'D:\\XmuNetDisk\\hBN_SEMprocess_PL.png')
    # fig0.savefig(r'D:\\XmuNetDisk\\hBN_SEMprocess_PL_para.png')
    plt.show()