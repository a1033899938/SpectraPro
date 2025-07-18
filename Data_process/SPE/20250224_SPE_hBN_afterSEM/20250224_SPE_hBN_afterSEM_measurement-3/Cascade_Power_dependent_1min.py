import os
import spe_loader as sl

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
    import matplotlib.pyplot as plt
    import pprint
    from src.general.figure import set_figure
    import numpy as np


    def gaussian(x, A, mu, sigma):
        return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))


    def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
        return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))


    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import numpy as np

    datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-3\measurement-3.h5"
    def the_figure0(ax, powers):
        """拟合曲线"""
        set_figure.set_label_and_title(ax, title=f'Power-dependent PL', xlabel='Excitation Power(uW)', ylabel='Wavelength(nm)', zlabel='Normalized Intensity(a.u.)', zlabel_rotation=90, mode='3d', x_label_pad=32, xlabel_rotation=-30, z_label_pad=25, title_pad=0)
        set_figure.set_spines(ax)
        ticks_xlabel = np.arange(0, len(powers), 2)
        set_figure.set_tick(ax, ticks_xlabel=ticks_xlabel, change_ticks_xlabel=[powers[i] for i in ticks_xlabel if i < len(powers)], ticks_ylabel=np.arange(400, 901, 100), mode='3d', ticks_xlabel_rotation=35, ticks_zlabel_pad=10)  # Normalized
        ax.zaxis.set_rotate_label(False)
        ax.set_box_aspect([1, 1, 1])
        ax.view_init(elev=20, azim=-45)  # elev 是仰角，azim 是方位角
        ax.grid(True)
        plt.tight_layout()

    """fig0"""
    with h5py.File(datapath1, "r") as f:
        data = f['OceanOpticsSpectrometer']
        keys_afterSEM = []
        keys_afterSEM.append('hBN_afterSEM_5kV_1min_10uW_1')
        keys_afterSEM.append('hBN_afterSEM_5kV_1min_20uW_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_1min_50uW_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_1min_100uW_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_1min_500uW_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_1min_1000uW_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_1min_2000uW_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_1min_3000uW_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_1min_2000uW_back_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_1min_1000uW_back_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_1min_500uW_back_0')
        # keys_afterSEM.append('hBN_afterSEM_5kV_1min_200uW_back_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_1min_100uW_back_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_1min_50uW_back_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_1min_20uW_back_0')
        keys_afterSEM.append('hBN_afterSEM_5kV_1min_10uW_back_0')
        legend_labels_afterSEM = ['10uW', '20uW', '50uW', '100uW', '500uW', '1000uW', '2000uW', '3000uW',
                                  '2000uW*', '1000uW*', '500uW*', # '200uW*',
                                  '100uW*', '50uW*',
                                  '20uW*', '10uW*']
        powers = [10, 20, 50, 100 , 500 ,1000, 2000, 3000, 2000, 1000, 500, 100, 50, 20, 10]
        fig0 = plt.figure(figsize=(8*1.5, 6*1.5))
        ax0 = fig0.add_subplot(111, projection='3d')
        sps = []
        for i, key in enumerate(keys_afterSEM):
            sp = data[key]
            bgd = np.array(sp.attrs['background'])
            wav = np.array(sp.attrs['wavelengths'])
            sp_time = sp.attrs['integration_time'] / 1000
            bgd_time = sp.attrs['background_int'] / 1000
            sp = sp / sp_time
            bgd = bgd / bgd_time
            sp = np.array(sp) - bgd
            sp = sp / powers[i]
            sps.append(sp)

        x = wav
        y = np.arange(len(keys_afterSEM))
        Z = np.array(sps)
        # Z = np.log(Z)

        min_differences = np.abs(wav - 400)
        min_index = np.argmin(min_differences)
        max_differences = np.abs(wav - 900)
        max_index = np.argmin(max_differences)
        x = x[min_index:max_index]
        Z = Z[:, min_index:max_index]
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

    the_figure0(ax0, powers)
    # title = f'hBN-after-SEM-process_5kV_1min\n Excitation power-dependent PL spectra'
    # set_figure.set_label_and_title(ax0, title=title, xlabel='Process time(min)', ylabel='Intensity(counts)',
    #                                label_fontsize=25, title_fontsize=25,
    #                                label_font_family='Times New Roman', title_font_family='Times New Roman',
    #                                label_fontweight='bold', title_fontweight='bold',
    #                                label_pad=15, title_pad=15, mode='3d')
    # set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
    # set_figure.set_tick(ax0, xbins=6, ybins=10, fontsize=10, fontweight='bold',
    #                     linewidth=3, tick_pad=5, direction='in',
    #                     ticks_xlabel=np.arange(0, len(keys_afterSEM), 1),
    #                     ticks_ylabel=np.arange(400, 901, 50), mode='3d')  # Normalized
    # plt.xticks(np.arange(0, len(legend_labels_afterSEM)), legend_labels_afterSEM, rotation=-60)
    # ax0.set_xlabel(xlabel='Excitation Power(uW)', labelpad=30)
    # ax0.set_ylabel(ylabel='Wavelength(nm)', labelpad=15)
    # ax0.zaxis.set_rotate_label(False)  # 关闭默认旋转设置
    # ax0.set_zlabel(zlabel='Intensity(counts)', rotation=90, labelpad=15)
    # # ax0.set_zlabel(zlabel='log(I)', rotation=90, labelpad=15)
    #
    # ax0.grid(True)
    # ax0.set_box_aspect([1, 1, 1])
    # ax0.view_init(elev=20, azim=45)
    # # plt.tight_layout()
    # from src.general.save_figure import save_subfig
    # # plt.savefig(r'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-3\1min\1min_cascade\\20250224_SPE_hBN_afterSEM_measurement-3_logI.png')
    # plt.savefig(r'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-3\1min\1min_cascade\\20250224_SPE_hBN_afterSEM_measurement-3.png')

    plt.show()