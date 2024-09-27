import os
import numpy as np
import pprint
import spe_loader as sl
import h5py


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
        elif self.filetype == '.txt':
            return self.read_txt()
        elif self.filetype == '.h5':
            return self.read_h5()
        else:
            raise ValueError("Unsupported file type")

    def read_spe(self):
        try:
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


if __name__ == '__main__':
    print("Run test")
    import matplotlib.pyplot as plt

    filetype = 'txt'

    if filetype == 'spe':
        filepath = r'D:\BaiduSyncdisk\Junjie Xie Backup\Processing\new-NPs-20240731\newNPs 13.spe'
        # data = read_spe(filepath)
        readFile = read_file(filepath=filepath)
        data = readFile.data
        print('data is: ')
        print(data)
        wavelength = data['wavelength']
        strip = data['strip']
        intensity_image = data['intensity_image']
        intensity = data['intensity']

        fig = plt.figure()
        ax = fig.add_subplot(211)
        ax.imshow(intensity_image)

        ax2 = fig.add_subplot(212)
        ax2.plot(wavelength, intensity)
        plt.show()
    elif filetype == 'h5':
        filepath = r'C:\Users\a1033\Desktop\Contemporary\20240620\2024-05-31.h5'
        print(filepath)
        with h5py.File(filepath, "r") as f:
            print(f'Key:')
            for key in f.keys():
                print({key})
        # for key in f.keys():
        #     print(f'key: {key} \n')
        print(dir(f))
    elif filetype == 'txt':
        filepath = r'C:\Users\a1033\Desktop\Contemporary\test.txt'
        readFile = read_file(filepath=filepath)
        data = readFile.data
        print('data is: ')
        print(data)

        wavelength = data['wavelength']
        intensity = data['intensity']

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(wavelength, intensity)
        plt.show()

