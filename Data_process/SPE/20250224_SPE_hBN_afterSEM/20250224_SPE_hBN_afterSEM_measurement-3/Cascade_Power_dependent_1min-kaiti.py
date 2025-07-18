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


    def the_figure1(ax):
        """拟合曲线"""
        set_figure.set_label_and_title(ax, title='', ylabel='Intensity(cts)')
        set_figure.set_spines(ax)
        set_figure.set_tick(ax, ticks_xlabel=np.arange(500, 701, 50))  # Normalized
        set_figure.set_legend(ax, font_size=20)
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
        fig0 = plt.figure(figsize=(8, 6))
        ax0 = fig0.add_subplot(111)
        sps = []
        les = ['Before Irradiation', 'After Irradiation']
        j = 0
        for i, key in enumerate(keys_afterSEM):
            if i != 1 and i != len(powers)-2:
                continue
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
            x, y = choose_range(wav, sp, min_val=500, max_val=700)
            ax0.plot(x, y, label=les[j], linewidth=2)
            j += 1
            ax0.set_ylim([-0.5 ,8])
            the_figure1(ax0)

    plt.show()