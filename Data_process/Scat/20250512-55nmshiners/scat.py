"""
Author: Junjie-Xie
Updated: 2025/7/31
Functions: 
"""
import h5py
import numpy as np
import os
from matplotlib import pyplot as plt
from src.general.numerical.edit_data import *
from src.general.load_data.save_read_data import *

filepath = r"D:\ExpData\temp20250516\55shiners.h5"

with h5py.File(filepath, "r") as f:
    data = f['OceanOpticsSpectrometer']
    for key in data.keys():
        sp = data[key]

        # 读取第一个子group下的第一个sp的bgd和wav，并对积分时间作归一化
        bgd = np.array(sp.attrs['background'])
        bgd_time = sp.attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        ref = np.array(sp.attrs['reference'])
        ref_time = sp.attrs['reference_int'] / 1000
        ref = ref / ref_time
        wav = np.array(sp.attrs['wavelengths'])

        sp_time = sp.attrs['integration_time'] / 1000
        raw = np.array(sp)
        raw = raw / sp_time

        wav, bgd, ref, raw = choose_range(wav, bgd, ref, raw, x1=400, x2=1100)
        scat = (raw - bgd) / (ref - bgd)
        savepath = os.path.join(os.path.dirname(filepath), f"{key}.txt")
        lines_name = ['wavelengths', 'scattering']
        save_lines_txt(data1=wav, data2=raw, lines_names=lines_name, save_path=savepath)