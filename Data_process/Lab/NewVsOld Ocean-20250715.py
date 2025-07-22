"""
Author: Junjie-Xie
Updated: 2025/7/16
Functions: 
"""
import h5py
import matplotlib.pyplot as plt

from src.general.figure import set_figure
from src.general.load_data.read_name import *
from src.my_style.my_mapping_para import *

def the_figure1(ax, title):
    set_figure.set_label_and_title(ax, title=title, ylabel='Intensity(cts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 1101, 100), show_xlabel_every_ticks=2, yaxis_use_log_scale=False)  # Normalized
    set_figure.set_legend(ax, font_size=12)
    plt.tight_layout()

def the_figure2(ax, title, ylabel='Intensity(cts)'):
    set_figure.set_label_and_title(ax, title=title, ylabel=ylabel)
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 1101, 100), show_xlabel_every_ticks=2, yaxis_use_log_scale=False)  # Normalized
    set_figure.set_legend(ax, font_size=20)
    plt.tight_layout()

# def the_figure3(ax, title):
#     set_figure.set_label_and_title(ax, title=title, ylabel="Intensity(cts)")
#     set_figure.set_spines(ax)
#     set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 1101, 100), show_xlabel_every_ticks=2, yaxis_use_log_scale=False)  # Normalized
#     set_figure.set_legend(ax, font_size=20)
#     plt.tight_layout()

# """路径"""
h5file = r"D:\ExpData\LabInstrumentTest\NewVsOldOcean-20250715\NewVsOldSpectrometer.h5"
dir_name = 'OceanOpticsSpectrometer'

# print_name_in_h5(h5file, dir_name, field_in=["MoSe2", "new"], field_out=None, sort_field=None, print_names=True)

Lamp_old = [
            "Lamp-1000_0",
            "Lamp-2000_0",
            "Lamp-5000_0",
            "Lamp-10000_0",
            "Lamp-20000_0",
            "Lamp-50000_0",
            "Lamp-100000_0",
            "Lamp-150000_0",
            "Lamp-200000_0"
            ]
Lamp_old_les = [key[:-2] for key in Lamp_old]

Lamp_new = [
            "Lamp-1000-newSM_0",
            "Lamp-2000-newSM_0",
            "Lamp-5000-newSM_0",
            "Lamp-10000-newSM_0",
            "Lamp-20000-newSM_0",
            "Lamp-50000-newSM_0",
            "Lamp-100000-newSM_0",
            "Lamp-150000-newSM_0",
            "Lamp-200000-newSM_0",
           ]
Lamp_new_les = [key[:-2] for key in Lamp_new]

AgNT = ["75AgNT-Scat_0",
        "75AgNT-Scat-newSM_0"]
AgNT_les = ["old SM", "new SM"]

hBN_SPE_old = [
                "hBNSPE_450ex_5uW_0",
                "hBNSPE_450ex_10uW_1",
                "hBNSPE_450ex_20uW_0",
                "hBNSPE_450ex_50uW_1",
              ]

hBN_SPE_new = [
                "hBNSPE_450ex_5uW-newSM_1",
                "hBNSPE_450ex_10uW-newSM_1",
                "hBNSPE_450ex_20uW-newSM_1",
                "hBNSPE_450ex_50uW-newSM_1"
              ]
hBN_SPE_les = ["5uW", "10uW", "20uW", "50uW"]

WS2ML_old = [
            "WS2ML_450ex_10nW_0",
            "WS2ML_450ex_1uW_1",
            "WS2ML_450ex_5uW_0",
            "WS2ML_450ex_10uW_0",
            "WS2ML_450ex_20uW_0",
            "WS2ML_450ex_50uW_1"
            ]

WS2ML_new = [
            "WS2ML_450ex_10nW-newSM_0",
            "WS2ML_450ex_1uW-newSM_0",
            "WS2ML_450ex_5uW-newSM_0",
            "WS2ML_450ex_10uW-newSM_0",
            "WS2ML_450ex_20uW-newSM_0",
            "WS2ML_450ex_50uW-newSM_0"
            ]

WSe2ML_old = [
            "WSe2ML_450ex_10nW_0",
            "WSe2ML_450ex_1uW_1",
            "WSe2ML_450ex_5uW_0",
            "WSe2ML_450ex_10uW_0",
            "WSe2ML_450ex_20uW_0",
            "WSe2ML_450ex_50uW_1"
            ]

WSe2ML_new = [
            "WSe2ML_450ex_10nW-newSM_0",
            "WSe2ML_450ex_1uW-newSM_0",
            "WSe2ML_450ex_5uW-newSM_0",
            "WSe2ML_450ex_10uW-newSM_0",
            "WSe2ML_450ex_20uW-newSM_0",
            "WSe2ML_450ex_50uW-newSM_0"
            ]

MoSe2ML_old = [
            "MoSe2ML_450ex_10nW_0",
            "MoSe2ML_450ex_1uW_1",
            "MoSe2ML_450ex_5uW_0",
            "MoSe2ML_450ex_10uW_0",
            "MoSe2ML_450ex_20uW_0",
            "MoSe2ML_450ex_50uW_0"
            ]

MoSe2ML_new = [
             "MoSe2ML_450ex_10nW-newSM_0",
            "MoSe2ML_450ex_1uW-newSM_0",
            "MoSe2ML_450ex_5uW-newSM_0",
            "MoSe2ML_450ex_10uW-newSM_0",
            "MoSe2ML_450ex_20uW-newSM_0",
            "MoSe2ML_450ex_50uW-newSM_0",
                ]

TMDC_les = ["10nW", "1uW", "5uW", "10uW", "20uW", "50uW"]

noise = ["noise_0",
         "noise_1"]

colors1 = [
    '#4477AA',  # 蓝色（最弱）
    '#66CCEE',
    '#228833',
    '#CCBB44',
    '#EE6677',
    '#AA3377'   # 紫红色（最强）
]

colors2 = [
    '#003f5c',  # 深青蓝（强度1：最低）
    '#2f4b7c',  # 靛蓝色
    '#665191',  # 暗紫色
    '#a05195',  # 紫粉色
    '#d45087',  # 玫瑰红
    '#f95d6a',  # 珊瑚红
    '#ff7c43',  # 橙红色
    '#ffa600',  # 琥珀橙
    '#ffd700'   # 金黄色（强度9：最高）
]


with h5py.File(h5file, "r") as f:
    # 读取sp目录
    data = f[dir_name]

    # # 归一化光源效率曲线
    # fig = plt.figure(figsize=(12 * 2, 8), dpi=100)
    # ax1 = fig.add_subplot(121)
    # ax2 = fig.add_subplot(122)
    # for i, key in enumerate(Lamp_old+Lamp_new):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sp = data[key]
    #     sp_time = sp.attrs['integration_time'] / 1000
    #     sp = np.array(sp)
    #     sp = sp / sp_time
    #     sp = sp - bgd
    #     sp /= np.max(sp)
    #     if "new" not in key:
    #         ax1.plot(wav, sp, label=Lamp_old_les[i], color=colors2[i])
    #     else:
    #         ax2.plot(wav, sp, label=Lamp_new_les[i-9], color=colors2[i-9])
    # fig.suptitle("Normalized Lamp Spectrum", fontsize=36, fontfamily='arial', fontweight='bold')
    # the_figure1(ax1, title="old SM")
    # the_figure1(ax2, title="new SM")
    #
    # # 同一最高强度下的光源效率曲线
    # fig = plt.figure(figsize=(12*2, 8), dpi=100)
    # ax1 = fig.add_subplot(121)
    # ax2 = fig.add_subplot(122)
    # for i, key in enumerate(Lamp_old):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sp = data[key]
    #     sp_time = sp.attrs['integration_time'] / 1000
    #     sp = np.array(sp)
    #     sp = sp / sp_time
    #     sp = sp - bgd
    #     if i < 4:
    #         ax1.plot(wav, sp, label=Lamp_old_les[i], color=colors2[i])
    #     else:
    #         ax2.plot(wav, sp, label=Lamp_old_les[i], color=colors2[i])
    #
    # for i, key in enumerate(Lamp_new):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sp = data[key]
    #     sp_time = sp.attrs['integration_time'] / 1000
    #     sp = np.array(sp)
    #     sp = sp / sp_time
    #     sp = sp - bgd
    #     if i < 4:
    #         ax1.plot(wav, sp, '--', label=Lamp_new_les[i], color=colors2[i])
    #     else:
    #         ax2.plot(wav, sp, '--', label=Lamp_new_les[i], color=colors2[i])
    # fig.suptitle("Lamp spectrum", fontsize=36, fontfamily='arial', fontweight='bold')
    # the_figure1(ax1, title='Low intensity')
    # the_figure1(ax2, title='High intensity')
    #
    # # 1、同一卤素灯功率下的光源曲线 2、暗场散射
    # fig1 = plt.figure(figsize=(12*1.1, 8), dpi=100)
    # ax1 = fig1.add_subplot(111)
    # fig2 = plt.figure(figsize=(12 * 1.1, 8), dpi=100)
    # ax2 = fig2.add_subplot(111)
    # fig3 = plt.figure(figsize=(12*1.1, 8), dpi=100)
    # ax3 = fig3.add_subplot(111)
    # for i, key in enumerate(AgNT):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     if i == 1:
    #         bgd = np.array(data["hBNSPE_450ex_50uW-newSM_1"].attrs['background'])
    #     else:
    #         bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     ref = np.array(data[key].attrs['reference'])
    #     ref_time = data[key].attrs['reference_int'] / 1000
    #     ref = ref / ref_time
    #     ref = ref - bgd
    #
    #     sp = data[key]
    #     sp_time = sp.attrs['integration_time'] / 1000
    #     sp = np.array(sp)
    #     sp = sp / sp_time
    #     sp = sp - bgd
    #     sp = sp / ref
    #
    #     ax1.plot(wav, ref, '-', label=AgNT_les[i])
    #     ax2.plot(wav, ref/np.max(ref), '-', label=AgNT_les[i])
    #     ax3.plot(wav, sp, '-', label=AgNT_les[i])
    # the_figure2(ax1, title='Lamp spectrum', ylabel='Intensity(cts)')
    # the_figure2(ax2, title='Lamp spectrum-Normalized', ylabel='Normalized Intensity(a.u.)')
    # ax3.set_ylim([-0.002, 0.004])
    # the_figure2(ax3, title='AgNT Scattering Spectrum', ylabel='Intensity(a.u.)')

    # # hBN SPE
    # for i, (key1, key2) in enumerate(zip(hBN_SPE_old, hBN_SPE_new)):
    #     fig = plt.figure(figsize=(12, 8), dpi=100)
    #     ax = fig.add_subplot(111)
    #     wav1 = np.array(data[key1].attrs['wavelengths'])
    #     bgd = np.array(data[key1].attrs['background'])
    #     bgd_time = data[key1].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sps = data[key1]
    #     sp_time = sps.attrs['integration_time'] / 1000
    #     sps = np.array(sps)
    #     sp = sps[1:-1]
    #     sp = np.mean(sp, axis=0)
    #     sp = sp / sp_time
    #     sp1 = sp - bgd
    #
    #     wav2 = np.array(data[key2].attrs['wavelengths'])
    #     bgd = np.array(data[key2].attrs['background'])
    #     bgd_time = data[key2].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sps = data[key2]
    #     sp_time = sps.attrs['integration_time'] / 1000
    #     sps = np.array(sps)
    #     sp = sps[1:-1]
    #     sp = np.mean(sp, axis=0)
    #     sp = sp / sp_time
    #     sp2 = sp - bgd
    #
    #     ax.plot(wav1, sp1, '-', label=hBN_SPE_les[i] + "_oldSM", linewidth=1)
    #     ax.plot(wav2, sp2, '-', label=hBN_SPE_les[i] + "_newSM", markersize=5)
    # the_figure2(ax, title="hBN  " + hBN_SPE_les[i])

    # # WS2
    # for i, (key1, key2) in enumerate(zip(WS2ML_old, WS2ML_new)):
    #     fig = plt.figure(figsize=(12, 8), dpi=100)
    #     ax = fig.add_subplot(111)
    #     wav1 = np.array(data[key1].attrs['wavelengths'])
    #     bgd = np.array(data[key1].attrs['background'])
    #     bgd_time = data[key1].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sps = data[key1]
    #     sp_time = sps.attrs['integration_time'] / 1000
    #     sps = np.array(sps)
    #     sp = sps[1:-1]
    #     sp = np.mean(sp, axis=0)
    #     sp = sp / sp_time
    #     sp1 = sp - bgd
    #
    #     wav2 = np.array(data[key2].attrs['wavelengths'])
    #     bgd = np.array(data[key2].attrs['background'])
    #     bgd_time = data[key2].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sps = data[key2]
    #     sp_time = sps.attrs['integration_time'] / 1000
    #     sps = np.array(sps)
    #     sp = sps[1:-1]
    #     sp = np.mean(sp, axis=0)
    #     sp = sp / sp_time
    #     sp2 = sp - bgd
    #
    #     ax.plot(wav1, sp1, '-', label=TMDC_les[i]+"_oldSM", linewidth=1)
    #     ax.plot(wav2, sp2, '-', label=TMDC_les[i]+"_newSM", markersize=5)
    # the_figure2(ax, title="$WS_2ML$ " + TMDC_les[i])

    # # WSe2
    # for i, (key1, key2) in enumerate(zip(WSe2ML_old, WSe2ML_new)):
    #     fig = plt.figure(figsize=(12, 8), dpi=100)
    #     ax = fig.add_subplot(111)
    #     wav1 = np.array(data[key1].attrs['wavelengths'])
    #     bgd = np.array(data[key1].attrs['background'])
    #     bgd_time = data[key1].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sps = data[key1]
    #     sp_time = sps.attrs['integration_time'] / 1000
    #     sps = np.array(sps)
    #     sp = sps[1:-1]
    #     sp = np.mean(sp, axis=0)
    #     sp = sp / sp_time
    #     sp1 = sp - bgd
    #
    #     wav2 = np.array(data[key2].attrs['wavelengths'])
    #     bgd = np.array(data[key2].attrs['background'])
    #     bgd_time = data[key2].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sps = data[key2]
    #     sp_time = sps.attrs['integration_time'] / 1000
    #     sps = np.array(sps)
    #     sp = sps[1:-1]
    #     sp = np.mean(sp, axis=0)
    #     sp = sp / sp_time
    #     sp2 = sp - bgd
    #
    #     ax.plot(wav1, sp1, '-', label=TMDC_les[i] + "_oldSM", linewidth=1)
    #     ax.plot(wav2, sp2, '-', label=TMDC_les[i] + "_newSM", markersize=5)
    # the_figure2(ax, title="$WeS_2ML$ " + TMDC_les[i])

    # # WSe2
    # for i, (key1, key2) in enumerate(zip(MoSe2ML_old, MoSe2ML_new)):
    #     fig = plt.figure(figsize=(12, 8), dpi=100)
    #     ax = fig.add_subplot(111)
    #     wav1 = np.array(data[key1].attrs['wavelengths'])
    #     bgd = np.array(data[key1].attrs['background'])
    #     bgd_time = data[key1].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sps = data[key1]
    #     sp_time = sps.attrs['integration_time'] / 1000
    #     sps = np.array(sps)
    #     sp = sps[1:-1]
    #     sp = np.mean(sp, axis=0)
    #     sp = sp / sp_time
    #     sp1 = sp - bgd
    #
    #     wav2 = np.array(data[key2].attrs['wavelengths'])
    #     bgd = np.array(data[key2].attrs['background'])
    #     bgd_time = data[key2].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sps = data[key2]
    #     sp_time = sps.attrs['integration_time'] / 1000
    #     sps = np.array(sps)
    #     sp = sps[1:-1]
    #     sp = np.mean(sp, axis=0)
    #     sp = sp / sp_time
    #     sp2 = sp - bgd
    #
    #     ax.plot(wav1, sp1, '-', label=TMDC_les[i] + "_oldSM", linewidth=1)
    #     ax.plot(wav2, sp2, '-', label=TMDC_les[i] + "_newSM", markersize=5)
    # the_figure2(ax, title="$MoSe_2ML$ " + TMDC_les[i])

    # noise
    fig = plt.figure(figsize=(12*2, 8), dpi=100)
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    for i, key in enumerate(noise):
        wav = np.array(data[key].attrs['wavelengths'])
        bgd = np.array(data[key].attrs['background'])
        bgd_time = data[key].attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        sps = data[key]
        sp_time = sps.attrs['integration_time'] / 1000
        sps = np.array(sps)

        for sp in sps:
            sp = sp / sp_time
            sp = sp - bgd
            if i == 0:
                ax1.plot(wav, sp, '-', linewidth=1)
            else:
                ax2.plot(wav, sp, '-', markersize=5)
    fig.suptitle("Noise(Background) Time Sequence", fontsize=36, fontfamily='arial', fontweight='bold')
    the_figure2(ax1, title="oldSM")
    the_figure2(ax2, title="newSM")
plt.show()