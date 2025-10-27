"""
Author: Junjie-Xie
Updated: 2025/10/13
Functions: 
"""
import numpy as np
import matplotlib.pyplot as plt
import h5py

from src.general.figure.draw_figure import *
from src.general.numerical.edit_data import *
from src.my_style.my_figure import *
from src.my_style.my_color import *
from src.general.numerical.filter import *
import json

filepath = r"D:\ExpData\SPE\20251015_HQ-hBN_PDMSvs.Tap\measurement-1_basic_PL.h5"
jsonpath = r"D:\GitProject\SpectraPro\Data_process\SPE\20251015_HQ-hBN_PDMSvsTap\sort.json"

with open(jsonpath, "r", encoding="utf-8") as F:
    jsondata = json.load(F)

with h5py.File(filepath, "r") as f:
    data = f[f'OceanOpticsSpectrometer']

    "包含各自定义组"
    xs = []
    ys = []
    les_group = []
    les_sg = []
    colors_group = [MyColor.vibrant for _ in range(len(jsondata))]
    remover = SpikeRemover()
    filter = SignalFilter()

    """历遍所有自定义组"""
    for iGroup, menugroup in enumerate(jsondata):
        "读取一个自定义组的json数据"
        h5groups = jsondata[menugroup]["keys"]
        prefix = jsondata[menugroup]["number"][0]
        suffix = jsondata[menugroup]["number"][1]
        h5groups = sort_by_middle_number(h5groups, prefix=prefix, suffix=suffix)
        subnum = jsondata[menugroup]["subnum"]

        "包含各h5group（实际上一个h5group就对应一条光谱（扫描某点的z轴得到的一系列光谱，处理后最后得到一条））"
        xs_h5group = []
        ys_h5group = []
        les_h5group = []

        """历遍所有h5组"""
        for iH5group, h5group in enumerate(h5groups):
            # if iH5group != 0:
            #     continue

            num_h5group_now = h5group[len(prefix):len(h5group) - len(suffix)]

            # 历遍每条光谱
            keys = data[h5group].keys()
            keys = sort_by_end_number(keys, subnum)

            "包含各扫描光谱"
            ys_now = np.array([]).reshape(0, 0)

            """历遍当前h5组中所有光谱"""
            for iKey, key in enumerate(keys):
                sp = data[h5group][key]

                # 只读一次波长和背景
                if iH5group == 0 and iKey == 0:
                    x_now = np.array(sp.attrs['wavelengths'])
                    bgd = np.array(sp.attrs['background'])
                    bgd_time = sp.attrs['background_int'] / 1000
                    bgd = bgd / bgd_time


                sp_time = sp.attrs['integration_time'] / 1000
                sp = np.array(sp)
                sp = sp / sp_time

                sp = sp - bgd
                sp, _ = remover.remove_spikes_unified(
                wavelengths=x_now,
                signal=sp,
                target_idx=None,  # 自动检测模式
                max_fwhm=5,
                repair_method='median'
                )

                if iKey == 0:
                    ys_now = sp
                else:
                    ys_now = np.vstack((ys_now, sp))

            per_spectrum_max = ys_now.max(axis=1)  # 结果是 shape 为 (50,) 的一维数组，每个元素是对应光谱的最大值
            max_index = np.argmax(per_spectrum_max)  # 得到“最大值最大”的光谱在数组中的索引
            y_max_now = ys_now[max_index]

            # y_max_now = np.max(ys_now, axis=0)
            # y_max_now, _ = remover.remove_spikes_unified(
            #     wavelengths=x_now,
            #     signal=y_max_now,
            #     target_idx=None,  # 自动检测模式
            #     max_fwhm=5,
            #     repair_method='median'
            # )

            xs_h5group.append(x_now)
            ys_h5group.append(y_max_now)
            les_h5group.append(num_h5group_now)

        xs.append(xs_h5group)
        ys.append(ys_h5group)
        les_group.append(les_h5group)
        les_sg.append(menugroup)

print(len(xs))
fig, axes = draw_cascade_group_2d(xs, ys, les_group=les_group, les_sg=les_sg, colors_group=colors_group)
for ax in axes:
    ax.legend()

fig2 = plt.figure(figsize=(12,8), dpi=200)
ax2 = fig2.add_subplot(1, 1, 1)
step = 0
iSp = 0
les_added = set()
for xs_h5group, ys_h5group, les, le_sg in zip(xs, ys, les_group, les_sg):
    for x, y, le in zip(xs_h5group, ys_h5group, les_group):
        if "hBN w/." in le_sg:
            if "PDMS" in le_sg:
                color = 'blue'
                alpha = 1
                le = "HQ-PDMS-hBN w/. exposure"
            elif "HQ" in le_sg:
                color='red'
                alpha = 1
                le = "HQ-Tap-hBN w/. exposure"
        elif "hBN w/o" in le_sg:
            if "PDMS" in le_sg:
                color = 'blue'
                alpha = 0.5
            elif "HQ" in le_sg:
                color = 'red'
                alpha = 0.5
            continue
        elif "sub w/." in le_sg:
            color='black'
            le = "PDMS-sub w/. exposure"
        elif "sub w/o" in le_sg:
            color='gray'
            continue

        y /= np.max(y)
        y = filter.apply_filter(x, y, filter_type="median", x_window_width=1)

        if le not in les_added:
            ax2.plot(x, y+step*iSp, label=le, color=color, alpha=alpha, linewidth=1)
            les_added.add(le)
        else:
            ax2.plot(x, y+step, label='', color=color, alpha=alpha, linewidth=1)
        iSp += 1
ax2.legend()
plt.show()