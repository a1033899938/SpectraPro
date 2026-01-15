"""
Author: Junjie-Xie
Updated: 2025/12/19
Functions: 
"""
from src.general.proc.ProcTrack import *
from src.general.numerical.edit_data import *
import matplotlib.pyplot as plt
import numpy as np

filepath = r"D:\ExpData\Fellows\WYQ\20251220_QD_measured_by_Xie\TestHWL_QD_2025-12-19.h5"

keys = ["2000x_200uW_p1_3", "2000x_200uW_p3_0", "2000x_200uW_p4_1", "2000x_200uW_p5_0", "2000x_200uW_p6_0"]

roi_range = [620, 640]

with h5py.File(filepath, mode="r") as f:
    root = f["OceanOpticsSpectrometer"]

    for key in keys:
        print(key)
        fig = plt.figure(figsize=(12 * 3, 8), dpi=200)
        ax1 = fig.add_subplot(131)
        ax2 = fig.add_subplot(132)
        ax3 = fig.add_subplot(133)

        sp = root[key]
        wav = np.array(sp.attrs['wavelengths'])

        bgd = np.array(sp.attrs['background'])
        bgd_time = sp.attrs['background_int'] / 1000
        bgd = bgd / bgd_time

        signal_time = sp.attrs['integration_time'] / 1000
        signals = np.array(sp)
        signals = signals / signal_time

        PL = None
        integrated_ints = []
        for signal in signals:
            signal = np.array(signal)
            signal = signal - bgd
            PL = signal if PL is None else np.vstack((PL, signal))
            ax2.plot(wav, signal)

            wav_idx1 = find_val_idx(wav, roi_range[0])
            wav_idx2 = find_val_idx(wav, roi_range[1])
            roi_signal = signal[wav_idx1:wav_idx2]
            integrated_int = np.sum(roi_signal[roi_signal>25])
            integrated_ints.append(integrated_int)

        len_time = np.shape(signals)[0]
        times = range(len_time)
        ax1.pcolor(wav, times, PL)
        ax3.plot(times, integrated_ints)
        save_path = os.path.join(os.path.dirname(filepath), "Images", f"{key}.png")
        fig.savefig(save_path)
        plt.close(fig)
        # plt.show()