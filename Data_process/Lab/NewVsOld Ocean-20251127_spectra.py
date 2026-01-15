"""
Author: Junjie-Xie
Updated: 2025/7/16
Functions: 
"""
import h5py
import matplotlib.pyplot as plt
import numpy as np

from src.general.figure import set_figure
from src.general.load_data.load_data_from_h5 import *
from src.my_style.my_mapping_para import *
from src.my_style.my_figure import *
from src.my_style.my_color import *

# """路径"""
h5file = r"D:\ExpData\LabInstrumentTest\NewVsOld Ocean-20251127\NewVsOldSpectrometer.h5"
dir_name = 'OceanOpticsSpectrometer'
from figure_setting import *

with h5py.File(h5file, "r") as f:
    root = f["OceanOpticsSpectrometer"]

    """荧光光谱"""
    names = ["WS2ML", "WSe2ML", "AuNC-1", "AuNC-2", "AuNC-3", "AuNC-4", "AuNC-5"]
    old_sm_group = {name: {} for name in names}  # {sample组: {光谱名称: h5路径}}
    new_sm_group = {name: {} for name in names}

    for key in root.keys():
        if "1000ms" in key:
            group_now = root[key]
            for name in names:
                if name in key:
                    old_sm_group[name].update({key: group_now})

    new_root = root["New"]
    for key in root["New"].keys():
        if "1000ms" in key:
            group_now = new_root[key]
            for name in names:
                if name in key:
                    new_sm_group[name].update({key: group_now})

    Figures = []
    Axes = []
    for i in range(len(names)):
        fig = plt.figure(i, figsize=(12, 8), dpi=200)
        ax = fig.add_subplot(111)
        Figures.append(fig)
        Axes.append(ax)

    A_old = []
    A_new = []
    sm_groups = [old_sm_group, new_sm_group]
    for iSmGroup, sm_group in enumerate(sm_groups):  # old_sm_group

        for iName, name in enumerate(names):  # WS2
            fig = Figures[iName]
            ax = Axes[iName]
            sample_now = sm_group[name]  # 0.05uW 1000ms: h5group

            sps_min = None
            sps_max = None

            if "WS2" in name:
                sorted_pair = sorted(zip(sample_now.keys(), sample_now.values()), key=lambda pair: float(pair[0][len("WS2ML_450ex-"):-len("uW_1000ms")]))
            elif "WSe2" in name:
                sorted_pair = sorted(zip(sample_now.keys(), sample_now.values()), key=lambda pair: float(pair[0][len("WSe2ML_450ex-"):-len("uW_1000ms")]))
            elif "AuNC" in name:
                sorted_pair = sorted(zip(sample_now.keys(), sample_now.values()), key=lambda pair: float(pair[0][len("65nmAuNC-"):-len("_1000ms")]))

            sample_keys, sample_values = zip(*sorted_pair)

            for sp_parent_name, sp_parent_group in zip(sample_keys, sample_values):
                sp_group = sp_parent_group["Spectra"]

                sps = None
                sp_group_keys = sorted(sp_group.keys(), key=lambda k: float(k[len("scan_z_p")::]))
                for sp_key in sp_group_keys:
                    sp_now = sp_group[sp_key]

                    wav = np.array(sp_now.attrs['wavelengths'])
                    bgd = np.array(sp_now.attrs['background'])
                    bgd_time = sp_now.attrs['background_int'] / 1000
                    bgd = bgd / bgd_time

                    sp_time = sp_now.attrs['integration_time'] / 1000
                    sp = np.array(sp_now)
                    sp = sp / sp_time

                    if "AuNC" in name:
                        ref = sp_now.attrs["reference"]
                        ref_time = sp_now.attrs["reference_int"] / 1000
                        ref = ref / ref_time

                        sp = (sp - bgd) / (ref - bgd)
                    else:
                        sp = sp - bgd

                    sps = sp if sps is None else np.vstack((sps, sp))

                if iSmGroup == 0:
                    color = "blue"
                    label = "old_" + sp_parent_name
                else:
                    color = "red"
                    label = "new_" + sp_parent_name

                if "AuNC" in name: # 取所有波长的最大值
                    sp_max = np.max(sps, axis=0)
                else: # 取最大强度那一条
                    max_idx = np.argmax(sps)
                    idx_row, idx_col = np.unravel_index(max_idx, sps.shape)
                    sp_max = sps[idx_row, :]

                    A = np.max(sp_max)
                    x0 = wav[np.argmax(sp_max)]
                    sigma = 20
                    p0 = [A, x0, sigma]

                    popt, pcov = curve_fit(gaussian, wav, sp_max, p0=p0)
                    # fitted_curve = gaussian(wav, *popt)
                    # ax.plot(wav, fitted_curve, "--", color="purple")
                    A = popt[0]
                    if iSmGroup == 0:
                        A_old.append(A)
                    else:
                        A_new.append(A)

                # 自动调整scale
                idx_1 = find_val_idx(wav, 500)
                idx_2 = find_val_idx(wav, 1020)
                minimum_sp_max = np.min(sp_max[idx_1:idx_2])
                maximun_sp_max = np.max(sp_max[idx_1:idx_2])
                sps_min = [minimum_sp_max] if sps_min is None else sps_min + [minimum_sp_max]
                sps_max = [maximun_sp_max] if sps_max is None else sps_max + [maximun_sp_max]

                ax.plot(wav, sp_max, color=color, label=label)

            if iSmGroup == 0:  # old sm 强度更高， 以它为标准
                if "AuNC" in name:
                    lim_min = np.min(sps_min)
                    lim_max = np.max(sps_max)
                    diff = lim_max - lim_min
                    ax.set_ylim([np.min(sps_min) - 0.1*diff , np.max(sps_max) + 0.1*diff])
            else: # 运行完New以后设置格式
                if "AuNC" not in name:
                    my_graph1(ax, title=name)
                else:
                    my_graph2(ax, title=name)

print(A_old)
print(A_new)
ratio = [value1/value2 for value1, value2 in zip(A_old, A_new)]
print(np.mean(ratio))

plt.show()

# keys = list(old_sm_group["WS2 ML"].keys())
# values = list(old_sm_group["WS2 ML"].values())
#
# sorted_pair = sorted(zip(keys, values), key=lambda pair: pair[0][len("WS2ML_450ex-"):-len("uW_1000ms")])  # 用zip(keys, values)中的第一位作为参数获取排序值
# sorted_keys, sorted_values = zip(*sorted_pair)
#
# print(sorted_keys)