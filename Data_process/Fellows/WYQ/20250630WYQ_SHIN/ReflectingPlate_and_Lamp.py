import h5py
import os
import matplotlib.pyplot as plt
import numpy as np

from src.general.figure import set_figure
from src.general import draw_power_dependent
from src.general import choose_range, sort_lists
from src.my_style.my_mapping_para import *

def load_data(h5_file, dir_name, sp_names, les, save_folder=None):
    with h5py.File(h5_file, "r") as f:
        # 读取sp目录
        data = f[dir_name]

        lamp_Li_old_names = []
        lamp_Li_new_names = []

        np_names = []
        # 读取sp key序列
        for key in data.keys():
            if "R-Li_S-Li" in key and "new" not in key:
                lamp_Li_old_names.append(key)
            if "R-Li_S-Li_new" in key:
                lamp_Li_new_names.append(key)
            if "R-Hu_S-Hu_NP" in key:
                np_names.append(key)

        # 读取目录下的第一个sp的bgd和wav，并对积分时间作归一化
        bgd = np.array(data[sp_names[0]].attrs['background'])
        bgd_time = data[sp_names[0]].attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        wav = np.array(data[sp_names[0]].attrs['wavelengths'])

        # 创建画布
        fig1 = plt.figure(figsize=(12, 8))
        ax1 = fig1.add_subplot(111)

        # 作不同反射板和光源的曲线
        for key in sp_names:
            sp = data[key]
            sp_time = sp.attrs['integration_time'] / 1000
            sp = np.array(sp)
            sp = sp / sp_time
            sp = sp - bgd
            sp = sp / np.max(sp)
            ax1.plot(wav, sp, label=key)

        # 创建画布
        fig2 = plt.figure(figsize=(12, 8))
        ax2 = fig2.add_subplot(111)
        for i, key in enumerate(lamp_Li_old_names):
            sp = data[key]
            sp_time = sp.attrs['integration_time'] / 1000
            sp = np.array(sp)
            sp = sp / sp_time
            sp = sp - bgd
            sp = sp / np.max(sp)
            ax2.plot(wav, sp, label=key[-1:])

        # 创建画布
        fig3 = plt.figure(figsize=(12, 8))
        ax3 = fig3.add_subplot(111)
        for i, key in enumerate(lamp_Li_new_names):
            sp = data[key]
            sp_time = sp.attrs['integration_time'] / 1000
            sp = np.array(sp)
            sp = sp / sp_time
            sp = sp - bgd
            sp = sp / np.max(sp)
            ax3.plot(wav, sp, label=key[-1:])

        # 创建画布
        fig4 = plt.figure(figsize=(12, 8))
        ax4 = fig4.add_subplot(111)
        for i, key in enumerate(np_names):
            sp = data[key]
            sp_time = sp.attrs['integration_time'] / 1000
            sp = np.array(sp)
            sp = sp / sp_time

            ref = np.array(data[key].attrs['reference'])
            ref_time = data[key].attrs['reference_int'] / 1000
            ref = ref / ref_time
            sp = (sp - bgd) / (ref - bgd)
            ax4.plot(wav, sp, label=key[10:-2])

    return fig1, fig2, fig3, fig4, ax1, ax2, ax3, ax4

def the_figure1(ax, les):
    set_figure.set_label_and_title(ax, title='Source Spectra of different RP and Lamp', ylabel='Normalized Intensity(a.u.)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(300, 1101, 100))  # Normalized
    set_figure.set_legend(ax, legend_labels=les)

def the_figure2(ax):
    set_figure.set_label_and_title(ax, title='Source Spectra of different Lamp-power(old)', ylabel='Normalized Intensity(a.u.)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(300, 1101, 100))  # Normalized
    set_figure.set_legend(ax)

def the_figure3(ax):
    set_figure.set_label_and_title(ax, title='Source Spectra of different Lamp-power(new)', ylabel='Normalized Intensity(a.u.)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(300, 1101, 100))  # Normalized
    set_figure.set_legend(ax)

def the_figure4(ax):
    set_figure.set_label_and_title(ax, title='Dark Field Scattering', ylabel='Normalized Intensity(a.u.)')
    set_figure.set_spines(ax)
    ax.set_ylim([-0.002, 0.032])
    set_figure.set_tick(ax, ticks_xlabel=np.arange(300, 1101, 100), ticks_ylabel=np.arange(-0.002, 0.032, 0.002))  # Normalized
    set_figure.set_legend(ax)

if __name__ == '__main__':
    """路径"""
    h5_file = r"D:\ExpData\Fellows\WYQ\20250630_WYQ_SHIN\R-Hu_S-Hu.h5"
    dir_name = 'OceanOpticsSpectrometer'
    sp_names = ["R-Li_0",
                "R-Hu_2",
                "R-Li_S-Li_0",
                "R-Li_S-Li_2"]
    les = ["RP-Hu-Lamp-Hu",
           "RP-Li_Lamp-Hu",
           "RP-Li_Lamp-Li(old)",
           "RP-Li_Lamp-Li(new)"]
    save_folder = os.path.dirname(h5_file)
    fig1_file = os.path.join(save_folder, f'Source Spectra of different RP and Lamp.png')
    fig2_file = os.path.join(save_folder, f'Source Spectra of different Lamp-power(old).png')
    fig3_file = os.path.join(save_folder, f'Source Spectra of different Lamp-power(new).png')
    fig4_file = os.path.join(save_folder, f'Dark Field Scattering.png')

    # 创建文件夹
    if not os.path.exists(save_folder):
        os.makedirs(save_folder, exist_ok=True)

    """加载并保存拟合数据"""
    dir_name = 'OceanOpticsSpectrometer'
    fig1, fig2, fig3, fig4, ax1, ax2, ax3, ax4= load_data(h5_file, dir_name, sp_names, les, save_folder=save_folder)

    # 保存图片
    the_figure1(ax1, les)
    ax1.set_position([0.1, 0.1, 0.8, 0.8])  # 左0.2，下0.2，宽0.6，高0.6
    fig1.savefig(fig1_file)

    the_figure2(ax2)
    ax2.set_position([0.1, 0.1, 0.8, 0.8])
    fig2.savefig(fig2_file)

    the_figure3(ax3)
    ax3.set_position([0.1, 0.1, 0.8, 0.8])
    fig3.savefig(fig3_file)

    the_figure4(ax4)
    ax4.set_position([0.1, 0.1, 0.8, 0.8])
    fig4.savefig(fig4_file)
    plt.show()