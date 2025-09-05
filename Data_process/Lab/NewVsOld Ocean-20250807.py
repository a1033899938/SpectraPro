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
h5file = r"D:\ExpData\LabInstrumentTest\NewVsOld Ocean-20250807\NewVsOldSpectrometer.h5"
dir_name = 'OceanOpticsSpectrometer'

load_names(h5file, dir_name, field_in=["new", "m2","MoSe2"], field_out=None, sort_field=["newSM_MoSe2ML_m2-", "uW_0"], print_names=True)
colors = MyColor.get_color_series("vibrant")
names = {
    "WS2 ML": {
        "new":
            ["newSM_WS2_1uW_0",
            "newSM_WS2_2uW_0",
            "newSM_WS2_5uW_0",
            "newSM_WS2_10uW_0",
            "newSM_WS2_20uW_0",
            "newSM_WS2_50uW_0",],
        "old":
            ["oldSM_WS2ML_1uW_0",
            "oldSM_WS2ML_2uW_0",
            "oldSM_WS2ML_5uW_0",
            "oldSM_WS2ML_10uW_0",
            "oldSM_WS2ML_20uW_0",
            "oldSM_WS2ML_50uW_0",]
    },
    "WSe2 ML":{
        "new":
            ["newSM_WSe2_1uW_0",
            "newSM_WSe2_2uW_0",
            "newSM_WSe2_5uW_0",
            "newSM_WSe2_10uW_0",
            "newSM_WSe2_20uW_0",
            "newSM_WSe2_50uW_0",],
        "old":
            [
            "oldSM_WSe2ML_1uW_0",
            "oldSM_WSe2ML_2uW_0",
            "oldSM_WSe2ML_5uW_0",
            "oldSM_WSe2ML_10uW_0",
            "oldSM_WSe2ML_20uW_0",
            "oldSM_WSe2ML_50uW_0",
            ]
    },
    "MoSe2 ML":{
        "m1":{
            "new":
                ["newSM_MoSe2_1uW_0",
                "newSM_MoSe2_2uW_0",
                "newSM_MoSe2_5uW_0",
                "newSM_MoSe2_10uW_0",
                "newSM_MoSe2_20uW_0",
                "newSM_MoSe2_50uW_0",],
            "old":
                ["oldSM_MoSe2ML_1uW_0",
                "oldSM_MoSe2ML_2uW_0",
                "oldSM_MoSe2ML_5uW_0",
                "oldSM_MoSe2ML_10uW_0",
                "oldSM_MoSe2ML_20uW_0",
                "oldSM_MoSe2ML_50uW_0",
                ]
        },
        "m2":{
            "new":
                ["newSM_MoSe2ML_m2-1uW_0",
                "newSM_MoSe2ML_m2-2uW_0",
                "newSM_MoSe2ML_m2-5uW_0",
                "newSM_MoSe2ML_m2-10uW_0",
                "newSM_MoSe2ML_m2-20uW_0",
                "newSM_MoSe2ML_m2-50uW_0",],
            "old":
                ["oldSM_MoSe2ML_m2-1uW_0",
                "oldSM_MoSe2ML_m2-2uW_0",
                "oldSM_MoSe2ML_m2-5uW_0",
                "oldSM_MoSe2ML_m2-10uW_0",
                "oldSM_MoSe2ML_m2-20uW_0",
                "oldSM_MoSe2ML_m2-50uW_0",
                ]
        }

    },
    "hBN SPE":{
        "new":
            ["newSM_hBNSPE_1uW_0",
            "newSM_hBNSPE_2uW_0",
            "newSM_hBNSPE_5uW_0",
            "newSM_hBNSPE_10uW_0",
            "newSM_hBNSPE_20uW_0",
            "newSM_hBNSPE_50uW_0",
            "newSM_hBNSPE_500uW_0",],
        "old":
            ["oldSM_hBNSPE_1uW_0",
            "oldSM_hBNSPE_2uW_0",
            "oldSM_hBNSPE_5uW_0",
            "oldSM_hBNSPE_10uW_0",
            "oldSM_hBNSPE_20uW_0",
            "oldSM_hBNSPE_50uW_0",
            "oldSM_hBNSPE_500uW_0",]
    },
    "Lamp":{
        "m1":{
            "new":
                ["oldSM_Lamp_1000cts_1",
                 "oldSM_Lamp_2000cts_1",
                 "oldSM_Lamp_5000cts_1",
                 "oldSM_Lamp_10000cts_1",
                 "oldSM_Lamp_20000cts_1",
                 "oldSM_Lamp_50000cts_1",
                 "oldSM_Lamp_100000cts_1",
                 "oldSM_Lamp_150000cts_1",],
            "old":
                ["oldSM_Lamp_1000cts_0",
                "oldSM_Lamp_2000cts_0",
                "oldSM_Lamp_5000cts_0",
                "oldSM_Lamp_10000cts_0",
                "oldSM_Lamp_20000cts_0",
                "oldSM_Lamp_50000cts_0",
                "oldSM_Lamp_100000cts_0",
                "oldSM_Lamp_150000cts_0",],
              },
        "m2":{
            "new":["newSM_newLamp_0"],
            "old":["oldSM_newLamp_0"],
        }


    },
    "SHIN":{
        "m1":{
            "new":["newSM_50nmSHIN_scat_3",],
            "old":["oldSM_50nmSHIN_scat_0",]
        },
        "m2":{
            "new sp":["newSM_newLamp_scat_sp_0",],
            "old sp":["oldSM_newLamp_scat_sp_0",],
            "new ref":["newSM_newLamp_scat_ref_0",],
            "old ref":["oldSM_newLamp_scat_ref_0",]
        }

    }
}

with h5py.File(h5file, "r") as f:
    # 读取sp目录
    data = f[dir_name]

    "同一最高强度下的光源效率曲线"
    # fig = plt.figure(figsize=(12, 8), dpi=200)
    # ax = fig.add_subplot(111)
    # for i, key in enumerate(names["Lamp"]["new"]):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sp = data[key]
    #     sp_time = sp.attrs['integration_time'] / 1000
    #     sp = np.array(sp)
    #     sp = sp / sp_time
    #     sp = sp - bgd
    #     ax.plot(wav, sp, '-', color=colors[i], label=f"newSM_{key[11:-2]}")
    # for i, key in enumerate(names["Lamp"]["old"]):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sp = data[key]
    #     sp_time = sp.attrs['integration_time'] / 1000
    #     sp = np.array(sp)
    #     sp = sp / sp_time
    #     sp = sp - bgd
    #     ax.plot(wav, sp, '--', linewidth=0.5, color=colors[i], label=f"oldSM_{key[11:-2]}")
    #
    # ax.set_ylim([0, 1000])
    # the_graph(ax, title="Lamp Spectra")

    "同一卤素灯强度下的光源效率曲线"
    # fig = plt.figure(figsize=(12, 8), dpi=200)
    # ax = fig.add_subplot(111)
    # key = "oldSM_Lamp_(newLamp150000cts)_0"
    # wav = np.array(data[key].attrs['wavelengths'])
    # bgd = np.array(data[key].attrs['background'])
    # bgd_time = data[key].attrs['background_int'] / 1000
    # bgd = bgd / bgd_time
    # sp = data[key]
    # sp_time = sp.attrs['integration_time'] / 1000
    # sp = np.array(sp)
    # sp = sp / sp_time
    # sp = sp - bgd
    # ax.plot(wav, sp, '-', linewidth=0.5, color=colors[0], label=f"newSM")
    # key = "oldSM_Lamp_150000cts_0"
    # wav = np.array(data[key].attrs['wavelengths'])
    # bgd = np.array(data[key].attrs['background'])
    # bgd_time = data[key].attrs['background_int'] / 1000
    # bgd = bgd / bgd_time
    # sp = data[key]
    # sp_time = sp.attrs['integration_time'] / 1000
    # sp = np.array(sp)
    # sp = sp / sp_time
    # sp = sp - bgd
    # ax.plot(wav, sp, '--', color=colors[1], label=f"oldSM")
    # # ax.set_ylim([0, 1000])
    # the_graph(ax, title="Lamp Spectra-Same Lamp Power")

    "50nmAuSHIN on AuMirror的暗场散射谱"
    # fig = plt.figure(figsize=(12, 8), dpi=200)
    # ax = fig.add_subplot(111)
    # for i, key in enumerate(names["SHIN"]["new"]):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     ref = np.array(data[key].attrs['reference'])
    #     ref_time = data[key].attrs['reference_int'] / 1000
    #     ref = ref / ref_time
    #     sp2d = data[key]
    #
    #     sp_time = sp2d.attrs['integration_time'] / 1000
    #     sp = np.array(sp2d[2])
    #     sp = sp / sp_time
    #     sp = (sp - bgd) / (ref - bgd)
    #     ax.plot(wav, sp, '-', color=colors[0], label=f"newSM_scattering")
    # for i, key in enumerate(names["SHIN"]["old"]):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     ref = np.array(data[key].attrs['reference'])
    #     ref_time = data[key].attrs['reference_int'] / 1000
    #     ref = ref / ref_time
    #     sp2d = data[key]
    #
    #     sp_time = sp2d.attrs['integration_time'] / 1000
    #     sp = np.array(sp2d[2])
    #     sp = sp / sp_time
    #     sp = (sp - bgd) / (ref - bgd)
    #     ax.plot(wav, sp, '--', linewidth=0.5, color=colors[1], label=f"oldSM_scattering")
    #
    # ax.set_ylim([-0.001, 0.005])
    # the_graph(ax, title="Scattering-50nm AuSHIN on AuMirror")

    "WS2 ML"
    # fig = plt.figure(figsize=(12, 8), dpi=200)
    # ax = fig.add_subplot(111)
    # for i, key in enumerate(names["WS2 ML"]["new"]):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sp2d = data[key]
    #
    #     sp_time = sp2d.attrs['integration_time'] / 1000
    #     sp = np.array(sp2d[2])
    #     sp = sp / sp_time
    #     sp = sp - bgd
    #     ax.plot(wav, sp, '-', color=colors[i], label=f"newSM_450ex_{key[10:-2]}")
    # for i, key in enumerate(names["WS2 ML"]["old"]):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sp2d = data[key]
    #
    #     sp_time = sp2d.attrs['integration_time'] / 1000
    #     sp = np.array(sp2d[2])
    #     sp = sp / sp_time
    #     sp = sp - bgd
    #     ax.plot(wav, sp, '--', linewidth=0.5, color=colors[i], label=f"oldSM_450ex_{key[12:-2]}")
    #
    # the_graph(ax, title="PL-WS2 ML")

    "WSe2 ML"
    # fig = plt.figure(figsize=(12, 8), dpi=200)
    # ax = fig.add_subplot(111)
    # for i, key in enumerate(names["WSe2 ML"]["new"]):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sp2d = data[key]
    #
    #     sp_time = sp2d.attrs['integration_time'] / 1000
    #     sp = np.array(sp2d[2])
    #     sp = sp / sp_time
    #     sp = sp - bgd
    #     ax.plot(wav, sp, '-', color=colors[i], label=f"newSM_450ex_{key[11:-2]}")
    # for i, key in enumerate(names["WSe2 ML"]["old"]):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sp2d = data[key]
    #
    #     sp_time = sp2d.attrs['integration_time'] / 1000
    #     sp = np.array(sp2d[2])
    #     sp = sp / sp_time
    #     sp = sp - bgd
    #     ax.plot(wav, sp, '--', linewidth=0.5, color=colors[i], label=f"oldSM_450ex_{key[13:-2]}")
    #
    # the_graph(ax, title="PL-WSe2 ML")

    "MoSe2 ML"
    # fig = plt.figure(figsize=(12, 8), dpi=500)
    # ax = fig.add_subplot(111)
    # for i, key in enumerate(names["MoSe2 ML"]["new"]):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sp2d = data[key]
    #
    #     sp_time = sp2d.attrs['integration_time'] / 1000
    #     sp = np.array(sp2d[2])
    #     sp = sp / sp_time
    #     sp = sp - bgd
    #     ax.plot(wav, sp, '-', color=colors[i], label=f"newSM_450ex_{key[12:-2]}")
    # for i, key in enumerate(names["MoSe2 ML"]["old"]):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sp2d = data[key]
    #
    #     sp_time = sp2d.attrs['integration_time'] / 1000
    #     sp = np.array(sp2d[2])
    #     sp = sp / sp_time
    #     sp = sp - bgd
    #     ax.plot(wav, sp, '--', linewidth=0.5, color=colors[i], label=f"oldSM_450ex_{key[14:-2]}")
    #
    # the_graph(ax, title="PL-MoSe2 ML")

    "hBN SPE"
    # fig = plt.figure(figsize=(12*3, 8*2.2), dpi=200)
    # ax1 = fig.add_subplot(231)
    # axs = [fig.add_subplot(231), fig.add_subplot(232), fig.add_subplot(233),
    #        fig.add_subplot(234), fig.add_subplot(235), fig.add_subplot(236)]
    # for i, key in enumerate(names["hBN SPE"]["new"][:-1]):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sp2d = data[key]
    #
    #     sp_time = sp2d.attrs['integration_time'] / 1000
    #     sp = np.array(sp2d[2])
    #     sp = sp / sp_time
    #     sp = sp - bgd
    #     axs[i].plot(wav, sp, '-', color=colors[0], label=f"newSM_450ex_{key[13:-2]}")
    # for i, key in enumerate(names["hBN SPE"]["old"][:-1]):
    #     wav = np.array(data[key].attrs['wavelengths'])
    #     bgd = np.array(data[key].attrs['background'])
    #     bgd_time = data[key].attrs['background_int'] / 1000
    #     bgd = bgd / bgd_time
    #     sp2d = data[key]
    #
    #     sp_time = sp2d.attrs['integration_time'] / 1000
    #     sp = np.array(sp2d[2])
    #     sp = sp / sp_time
    #     sp = sp - bgd
    #     axs[i].plot(wav, sp, '--', linewidth=0.5, color=colors[1], label=f"oldSM_450ex_{key[13:-2]}")
    #     the_graph(axs[i])
    #
    # title = plt.suptitle("PL-hBN SPE", fontsize=30, fontweight='bold', fontfamily='serif')
    # plt.tight_layout()

    "Lamp Spectra-m2"
    fig = plt.figure(figsize=(12, 8), dpi=200)
    ax = fig.add_subplot(111)
    key = names["Lamp"]["m2"]["new"][0]
    wav = np.array(data[key].attrs['wavelengths'])
    bgd = np.array(data[key].attrs['background'])
    bgd_time = data[key].attrs['background_int'] / 1000
    bgd = bgd / bgd_time
    sp = data[key]
    sp_time = sp.attrs['integration_time'] / 1000
    sp = np.array(sp)
    sp = sp / sp_time
    sp = sp - bgd
    ax.plot(wav, sp, '-', linewidth=0.5, color=colors[0], label=f"newSM")
    key = names["Lamp"]["m2"]["old"][0]
    wav = np.array(data[key].attrs['wavelengths'])
    bgd = np.array(data[key].attrs['background'])
    bgd_time = data[key].attrs['background_int'] / 1000
    bgd = bgd / bgd_time
    sp = data[key]
    sp_time = sp.attrs['integration_time'] / 1000
    sp = np.array(sp)
    sp = sp / sp_time
    sp = sp - bgd
    ax.plot(wav, sp, '--', color=colors[1], label=f"oldSM")
    the_graph(ax, title="Lamp Spectra-Same Lamp Power")

    "50nmAuSHIN on AuMirror的暗场散射谱-m2"
    fig = plt.figure(figsize=(12, 8), dpi=200)
    ax = fig.add_subplot(111)
    # 新
    key = names["SHIN"]["m2"]["new ref"][0]
    wav = np.array(data[key].attrs['wavelengths'])
    bgd = np.array(data[key].attrs['background'])
    bgd_time = data[key].attrs['background_int'] / 1000
    bgd = bgd / bgd_time

    ref_time = data[key].attrs['integration_time'] / 1000
    ref = np.array(data[key])
    ref = ref / ref_time
    ref = ref - bgd

    key = names["SHIN"]["m2"]["new sp"][0]
    wav = np.array(data[key].attrs['wavelengths'])
    bgd = np.array(data[key].attrs['background'])
    bgd_time = data[key].attrs['background_int'] / 1000
    bgd = bgd / bgd_time

    sp_time = data[key].attrs['integration_time'] / 1000
    sp = np.array(data[key])
    sp = sp / sp_time
    sp = sp - bgd

    scat = sp / ref
    ax.plot(wav, scat, '-', color=colors[0], label=f"newSM_scattering")

    # 旧
    key = names["SHIN"]["m2"]["old ref"][0]
    wav = np.array(data[key].attrs['wavelengths'])
    bgd = np.array(data[key].attrs['background'])
    bgd_time = data[key].attrs['background_int'] / 1000
    bgd = bgd / bgd_time

    ref_time = data[key].attrs['integration_time'] / 1000
    ref = np.array(data[key])
    ref = ref / ref_time
    ref = ref - bgd

    key = names["SHIN"]["m2"]["old sp"][0]
    wav = np.array(data[key].attrs['wavelengths'])
    bgd = np.array(data[key].attrs['background'])
    bgd_time = data[key].attrs['background_int'] / 1000
    bgd = bgd / bgd_time

    sp_time = data[key].attrs['integration_time'] / 1000
    sp = np.array(data[key])
    sp = sp / sp_time
    sp = sp - bgd

    scat = sp / ref

    ax.plot(wav, scat, '--', color=colors[1], label=f"oldSM_scattering")
    ax.set_ylim([-0.001, 0.005])
    the_graph(ax, title="Scattering-50nm AuSHIN on AuMirror")

    "MoSe2 ML-m2"
    fig = plt.figure(figsize=(12, 8), dpi=500)
    ax = fig.add_subplot(111)
    for i, key in enumerate(names["MoSe2 ML"]["m2"]["new"]):
        wav = np.array(data[key].attrs['wavelengths'])
        bgd = np.array(data[key].attrs['background'])
        bgd_time = data[key].attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        sp2d = data[key]

        sp_time = sp2d.attrs['integration_time'] / 1000
        sp = np.array(sp2d[2])
        sp = sp / sp_time
        sp = sp - bgd
        ax.plot(wav, sp, '-', color=colors[i], label=f"newSM_450ex_{key[12:-2]}")
    for i, key in enumerate(names["MoSe2 ML"]["m2"]["old"]):
        wav = np.array(data[key].attrs['wavelengths'])
        bgd = np.array(data[key].attrs['background'])
        bgd_time = data[key].attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        sp2d = data[key]

        sp_time = sp2d.attrs['integration_time'] / 1000
        sp = np.array(sp2d[2])
        sp = sp / sp_time
        sp = sp - bgd
        ax.plot(wav, sp, '--', linewidth=0.5, color=colors[i], label=f"oldSM_450ex_{key[14:-2]}")

    the_graph(ax, title="PL-MoSe2 ML")
plt.show()