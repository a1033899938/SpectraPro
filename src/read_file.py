import spe_loader as sl
import numpy as np


def read_spe(file_path):
    sp = sl.load_from_files([file_path])
    data = {}
    data['xdim'] = sp.xdim[0]
    data['ydim'] = sp.ydim[0]
    data['intensity'] = np.squeeze(np.array(sp.data))
    data['wavelength'] = sp.wavelength
    data['strip'] = range(data['ydim'])
    print(data)
    return data


def read_txt(file_path):
    print("under doing.")
