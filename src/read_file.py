import spe_loader as sl
import numpy as np
import pprint


def read_spe(file_path, strip='all'):
    sp = sl.load_from_files([file_path])
    data = {}
    data['xdim'] = sp.xdim[0]
    data['ydim'] = sp.ydim[0]
    data['intensity_image'] = np.squeeze(np.array(sp.data))
    data['wavelength'] = sp.wavelength
    data['strip'] = range(data['ydim'])

    if strip == 'all':
        data['intensity'] = np.sum(data['intensity_image'], axis=0)
    print("==========data==========")
    pprint.pprint(data)
    print("========data end========")
    return data


def read_txt(file_path):
    print("under doing.")


if __name__ == '__main__':
    print("Run test")
    import matplotlib.pyplot as plt

    filetype = 'spe'

    if filetype == 'spe':
        filepath = r'D:\BaiduSyncdisk\Junjie Xie Backup\Processing\new-NPs-20240731\newNPs 13.spe'
        data = read_spe(filepath)
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