import os
import numpy as np
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

    datapath1 = r'D:\WechatFile\WeChat Files\wxid_4ugho6kb3jdv12\FileStorage\File\2025-01\20250115_OceanVsMorpho\2025-01-15.h5'
    datapath2 = r'D:\WechatFile\WeChat Files\wxid_4ugho6kb3jdv12\FileStorage\File\2025-01\20250115_OceanVsMorpho\AuNP.csv'

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    with h5py.File(datapath1, "r") as f:
        # for key in f.keys():
        #     # print(f[key], key, f[key].name, f[key].value) # 因为这里有group对象它是没有value属性的,故会异常。另外字符串读出来是字节流，需要解码成字符串。
        data = f['OceanOpticsSpectrometer']
        for key in data.keys():
            if key == '80nmAuNP_this_0':
                sp = data[key]
                ref = np.array(sp.attrs['reference'])
                ref = ref*10
                bgd = np.array(sp.attrs['background'])
                wav = np.array(sp.attrs['wavelengths'])
                # print(np.shape(ref), np.shape(bgd))

                dfs = (np.array(sp) - bgd) / (ref - bgd)
                ax.plot(wav, dfs)


    import pandas as pd
    df = pd.read_csv(datapath2, encoding="utf-8")
    wav = np.array(df.iloc[11:-1, 0])
    bgd = np.array(df.iloc[11:-1, 1])
    ref = np.array(df.iloc[11:-1, 2])
    spe = np.array(df.iloc[11:-1, 3])

    wav = wav.astype(float)
    bgd = bgd.astype(float)
    ref = ref.astype(float)
    spe = spe.astype(float)

    print(len(wav), len(bgd), len(ref), len(spe))
    ax.plot(wav, (spe - bgd) / (ref - bgd))


    title = 'Dark Field Scattering'
    set_figure.set_label_and_title(ax, title=title, ylabel='Intensity(a.u.)',
                                   label_fontsize=25, title_fontsize=25,
                                   label_font_family='Times New Roman', title_font_family='Times New Roman',
                                   label_fontweight='bold', title_fontweight='bold',
                                   label_pad=8, title_pad=15)
    set_figure.set_spines(ax, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
    set_figure.set_tick(ax, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                        linewidth=3, tick_pad=5, direction='in',
                        ticks_xlabel=np.linspace(400, 1100, 8),
                        ticks_ylabel=np.linspace(0, 0.02, 6))  # Normalized
    set_figure.set_legend(ax, legend_labels=['Ocean', 'Morpho'], font_size=20, location='upper right')
    # from src.general.save_figure import save_subfig
    # plt.savefig(os.path.join(datapath2, 'OceanVsMorpho.png'))
    ax.set_ylim(-0.01, 0.02)
    fig.tight_layout()
    plt.show()