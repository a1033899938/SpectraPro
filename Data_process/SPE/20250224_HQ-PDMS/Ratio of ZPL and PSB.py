"""
Author: Junjie-Xie
Updated: 2025/10/14
Functions: 
"""
import numpy as np
import matplotlib.pyplot as plt
import h5py
from scipy.optimize import curve_fit
from src.general.numerical.edit_data import *
from src.my_style.my_color import *
from src.general.numerical.curve_functions import *

filepath1 = r"D:\ExpData\SPE\20250224_HQ-PDMS\20250224_SPE_hBN_afterSEM_measurement-3.h5"
filepath2 = r"D:\ExpData\SPE\20250224_HQ-PDMS\measurement-2_try_power-dependent-PL.h5"

keys1 = ["hBN_afterSEM_5kV_2min_3000uW_0", "hBN_afterSEM_5kV_1min_3000uW_0", "hBN_afterSEM_5kV_0.5min_3000uW_0"]
colors = MyColor.vibrant

mag2s = []
mag3s = []
with h5py.File(filepath1, "r") as f:
    data = f[f'OceanOpticsSpectrometer']

    for i, key in enumerate(keys1):
        raw = data[key]

        bgd = np.array(raw.attrs['background'])
        bgd_time = raw.attrs['background_int'] / 1000
        bgd = bgd / bgd_time

        wav = np.array(raw.attrs['wavelengths'])

        raw_time = raw.attrs['integration_time'] / 1000
        raw = np.array(raw)
        raw = raw / raw_time

        wav, bgd, raw = choose_range(wav, bgd, raw, x1=400, x2=1100)
        sp = raw - bgd

        # int_538nm = sp[find_val_idx(wav, 538)]
        # sp = sp / int_538nm
        sp = sp / np.max(sp)

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)

        ax.plot(wav, sp, label=key)
        p0 = [100, 537, 6,
              100, 550, 6,
              10, 577, 6]

        bounds = ([0, 527, 5,
                   0, 540, 5,
                   0, 567, 5],
                  [100000, 547, 15,
                   100000, 560, 15,
                   100000, 587, 15])

        x, y = choose_range(wav, sp, x1=510, x2=900)
        popt, pcov = curve_fit(triple_lorentzian, x, y, p0=p0, bounds=bounds)
        A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3 = popt
        y_fit1 = lorentzian(x, A1, x1, gamma1)
        y_fit2 = lorentzian(x, A2, x2, gamma2)
        y_fit3 = lorentzian(x, A3, x3, gamma3)
        ax.plot(x, y_fit1)
        ax.plot(x, y_fit2)
        ax.plot(x, y_fit3)
        ax.plot(x, y_fit1 + y_fit2 + y_fit3, "--", color='blue')
        ax.set_title(key)
        mag2 =  (A2/gamma2)/(A1/gamma1)
        mag3 = (A3/gamma3)/(A1/gamma1)
        print(f"Ratio: 1: {mag2}: {mag3}")
        mag2s.append(mag2)
        mag3s.append(mag3)

keys2 = ["hBN_afterSEM_5kV_5min_expose10s_3000uW__1"]
with h5py.File(filepath2, "r") as f:
    data = f[f'OceanOpticsSpectrometer']

    for i, key in enumerate(keys2):
        raw = data[key]

        bgd = np.array(raw.attrs['background'])
        bgd_time = raw.attrs['background_int'] / 1000
        bgd = bgd / bgd_time

        wav = np.array(raw.attrs['wavelengths'])

        raw_time = raw.attrs['integration_time'] / 1000
        raw = np.array(raw)
        raw = raw / raw_time

        wav, bgd, raw = choose_range(wav, bgd, raw, x1=400, x2=1100)
        sp = raw - bgd

        # int_538nm = sp[find_val_idx(wav, 538)]
        sp = sp / np.max(sp)

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        ax.plot(wav, sp)
        x, y = choose_range(wav, sp, x1=510, x2=900)
        popt, pcov = curve_fit(triple_lorentzian, x, y, p0=p0, bounds=bounds)
        A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3 = popt
        y_fit1 = lorentzian(x, A1, x1, gamma1)
        y_fit2 = lorentzian(x, A2, x2, gamma2)
        y_fit3 = lorentzian(x, A3, x3, gamma3)
        ax.plot(x, y_fit1)
        ax.plot(x, y_fit2)
        ax.plot(x, y_fit3)
        ax.plot(x, y_fit1+y_fit2+y_fit3, "--", color='blue')
        ax.set_title(key)
        mag2 = (A2 / gamma2) / (A1 / gamma1)
        mag3 = (A3 / gamma3) / (A1 / gamma1)
        print(f"Ratio: 1: {mag2}: {mag3}")
        mag2s.append(mag2)
        mag3s.append(mag3)

print(f"AVG Ratio: 1: {np.mean(mag2s)}: {np.mean(mag3s)}")
ax.legend()

plt.show()