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
            keys = sort_by_end_number(keys)

            # print("---------------")
            # print(f"h5group now: {h5group}")
            # print(f"keys now: {keys}")
            "包含各扫描光谱"
            ys_now = np.array([]).reshape(0, 0)

            """历遍当前h5组中所有光谱"""
            for iKey, key in enumerate(keys):
                if iKey <= 0: # 没有设置sleep，第一条谱有问题
                    continue

                sp = data[h5group][key]

                # 只读一次波长和背景
                if iH5group == 0 and iKey == 1:
                    x_now = np.array(sp.attrs['wavelengths'])
                    bgd = np.array(sp.attrs['background'])
                    bgd_time = sp.attrs['background_int'] / 1000
                    bgd = bgd / bgd_time


                sp_time = sp.attrs['integration_time'] / 1000
                sp = np.array(sp)
                sp = sp / sp_time

                sp = sp - bgd
                # sp, _ = remover.remove_spikes_unified(
                # wavelengths=x_now,
                # signal=sp,
                # target_idx=None,  # 自动检测模式
                # max_fwhm=5,
                # repair_method='median'
                # )

                if iKey == 1:
                    ys_now = sp
                else:
                    ys_now = np.vstack((ys_now, sp))

            "三维瀑布图"
            # fig0 = plt.figure(figsize=(12, 8), dpi=200)
            # ax0 = fig0.add_subplot(1, 1, 1, projection='3d')
            #
            # draw_cascade_3d(x_now, np.arange(0, len(ys_now)), ys_now, ax0, normalize = False, connect_peaks=False, find_peak_args=None, draw_polygon= True, alpha = 0.5)
            #
            # the_cascade_3d(ax0, title=h5group)

            "找到最强的一条光谱"
            # per_spectrum_max = ys_now.max(axis=1)  # 结果是 shape 为 (50,) 的一维数组，每个元素是对应光谱的最大值
            # max_index = np.argmax(per_spectrum_max)  # 得到“最大值最大”的光谱在数组中的索引
            # y_max_now = ys_now[max_index]

            "找到每个波长的最大值"
            y_max_now = np.max(ys_now, axis=0)

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
#
# fig, axes = draw_cascade_group_2d(xs, ys, les_group=les_group, les_sg=les_sg, colors_group=colors_group)
#
idx_start = find_val_idx(x_now, 500)
idx_end = find_val_idx(x_now, 650)




# for x_group, y_group, le_group, le_sg in zip(xs, ys, les_group, les_sg):
#     fig_temp = plt.figure(figsize=(12,8), dpi=200)
#     ax_temp = fig_temp.add_subplot(1, 1, 1)
#
#     for j in range(np.shape(x_group)[0]):
#         x = x_group[j]
#         y = y_group[j]
#
#         # 对ROI区域，最大强度归一化
#         y_max_roi = np.max(y[idx_start: idx_end])
#         y = y / y_max_roi
#
#         # 选择区域
#         x, y = choose_range(x, y, x1=450, x2=950)
#         ax_temp.plot(x, y, label=le_sg)
#         ax_temp.set_ylim([-0.2, 1.2])
#
#     the_graph4(ax=ax_temp, title=le_sg)

fig2 = plt.figure(figsize=(12,8), dpi=200)
ax2 = fig2.add_subplot(1, 1, 1)
step = 0
iSp = 0
les_added = set()
for i, (xs_h5group, ys_h5group, les, le_sg) in enumerate(zip(xs, ys, les_group, les_sg)):
    print(i, le_sg)
    if not (i == 2 or i == 9 or i == 5):  # HQ-PDMS-hBN w/. exposure 2-2$, HQ-Tape-hBN w/. exposure 3$, PDMS-sub w/. exposure
        continue

    for j, (x, y, le) in enumerate(zip(xs_h5group, ys_h5group, les_group)):
        if "hBN w/." in le_sg:
            if "PDMS" in le_sg:
                if j != 0:
                    continue
                color = 'blue'
                alpha = 1
                le = "HQ-PDMS-hBN w/. exposure"
            elif "Tape" in le_sg:
                if j != 5:
                    continue
                color='red'
                alpha = 1
                le = "HQ-Tape-hBN w/. exposure"
        elif "hBN w/o" in le_sg:
            continue
            if "PDMS" in le_sg:
                color = 'blue'
                alpha = 0.5
            elif "Tape" in le_sg:
                color = 'red'
                alpha = 0.5
            # continue
        elif "sub w/." in le_sg:
            if j != 4:
                continue
            color='black'
            le = "PDMS-sub w/. exposure"
        elif "sub w/o" in le_sg:
            continue
            color='gray'

        # print(le)

        x, y = choose_range(x, y, x1=450, x2=950)
        y /= np.max(y)

        # if i == 2 or i == 5:
        #     p0 = [1, 550, 100]
        #
        #     bounds = ([0, 510, 0],
        #               [1, 600, 100])
        #     x_for_fit, y_for_fit = choose_range(x, y, x1=505, x2=650)
        #     popt, pcov = curve_fit(gaussian, x_for_fit, y_for_fit, p0=p0, bounds=bounds)
        #     y_fit = gaussian(x, *popt)
        # elif i == 9:
        #     p0 = [100, 537, 6,
        #           100, 550, 6,
        #           1, 577, 6,
        #           10, 550, 100]
        #
        #     bounds = ([0, 527, 0,
        #                0, 540, 6,
        #                0.1, 567, 0.3,
        #                0, 520, 20],
        #               [100000, 547, 10,
        #                100000, 560, 20,
        #                10, 587, 20,
        #                100000, 700, 300])
        #     x_for_fit, y_for_fit = choose_range(x, y, x1=505, x2=650)
        #     def quatra_peaks(x, A1, x1, gamma1, A2, x2, gamma2, RatioA_23, x3, gamma3, A4, x4, gamma4):
        #         A3 = A2 * RatioA_23
        #         peaks = triple_lorentzian(x, A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3)
        #         peak4 = gaussian(x, A4, x4, gamma4)
        #         return peaks + peak4
        #     popt, pcov = curve_fit(quatra_peaks, x_for_fit, y_for_fit, p0=p0, bounds=bounds)
        #     A1, x1, gamma1, A2, x2, gamma2, RatioA_23, x3, gamma3, A4, x4, gamma4 = popt
        #     y_fit1 = triple_lorentzian(x, A1, x1, gamma1, A2, x2, gamma2, RatioA_23, x3, gamma3)
        #     y_fit2 = gaussian(x, A4, x4, gamma4)
        #     y_fit = quatra_peaks(x, *popt)

        # y = filter.apply_filter(x, y, filter_type="median", x_window_width=1)

        if le not in les_added:
            if i == 9:
                y *= 1.5
            ax2.plot(x, y+step*iSp, '-', label=le, color=color, alpha=alpha, linewidth=1)

            #     ax2.plot(x, y_fit1, '-', label='', color=color, alpha=alpha, linewidth=2)
            #     ax2.plot(x, y_fit2, '-', label='', color=color, alpha=alpha, linewidth=2)
            #     ax2.plot(x, y_fit, '-', label='', color=color, alpha=alpha, linewidth=2)
            # else:
            #     ax2.plot(x, y_fit, '-', label='', color=color, alpha=alpha, linewidth=2)
            les_added.add(le)
        else:
            ax2.plot(x, y+step, 'o', label='', color=color, alpha=alpha, linewidth=1)
            ax2.plot(x_for_fit, y_for_fit, '-', label='', color=color, alpha=alpha, linewidth=1)
        iSp += 1
ax2.set_ylim([-0.2, 1.6])

the_graph4(ax2, title="Comparison of Irradiated Samples PL")

handles, labels = plt.gca().get_legend_handles_labels()

# 打印查看当前的顺序
print("原始顺序:", labels)

# 定义你想要的顺序（使用标签名称）
desired_order = [1, 0, 2]  # 索引顺序
# 或者直接指定标签名
# desired_order = ['Line 3', 'Line 1', 'Line 2']

# 按新顺序重新排列
handles = [handles[i] for i in desired_order]
labels = [labels[i] for i in desired_order]


ax2.legend(handles, labels, fontsize=20)
plt.show()