import h5py
import os

from src.general.figure import set_figure
from src.my_style.my_mapping_para import *
from src.general.figure.draw_figure import *

def load_data(h5_file, dir_name, save_folder=None):
    sp_series_name = []
    powers = []
    with h5py.File(h5_file, "r") as f:
        # 读取sp目录
        data = f[dir_name]

        # 读取sp key序列
        for key in data.keys():
            if ("hBN_afterSEM_5kV_5min_60KX_time_series_m4_P" in key
                    and 'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P3000uW_0' not in key
                    and 'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P5000uW_0' not in key
                    and 'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P11000uW_0' not in key
                    and 'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P5000uW_2' not in key
                    and 'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P5000uW_3' not in key):
                sp_series_name.append(key)
                if key == 'hBN_afterSEM_5kV_5min_60KX_time_series_m4_P15000uW_0':
                    powers.append(12000)
                else:
                    powers.append(int(key[len("hBN_afterSEM_5kV_5min_60KX_time_series_m4_P"):-len("uW_0")]))
        # 根据powers重新排序
        powers, sp_series_name = sort_lists(powers, sp_series_name)
        print(sp_series_name)
        print(powers)

        # 读取目录下的第一个sp的bgd和wav，并对积分时间作归一化
        bgd = np.array(data["hBN_afterSEM_5kV_5min_60KX_time_series_m2_P10uW_0"].attrs['background'])
        bgd_time = data["hBN_afterSEM_5kV_5min_60KX_time_series_m2_P10uW_0"].attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        wav = np.array(data["hBN_afterSEM_5kV_5min_60KX_time_series_m2_P10uW_0"].attrs['wavelengths'])

        # 储存不同功率的拟合参数
        ints = []
        cws = []
        gammas = []
        err_ints = []
        err_cws = []
        err_gammas = []
        # 历遍所有sp_2d
        for i, key in enumerate(sp_series_name):
            print(f"\nkey: {key}")
            sp_2d = data[key]
            sp_time = sp_2d.attrs['integration_time'] / 1000
            sp_2d = np.array(sp_2d)
            sp_2d = sp_2d / sp_time

            # 储存同一功率下，不同时间的拟合参数
            ints_row = []
            cws_row = []
            gammas_row = []
            for row in range(sp_2d.shape[0]):
                # 创建画布
                fig = plt.figure(figsize=(12, 8))
                ax = fig.add_subplot(111)
                sp_row = sp_2d[row, :]
                sp_row = sp_row - bgd

                """数据处理区域"""
                x, y = choose_range(wav, sp_row, x1=400, x2=900)
                ax.plot(x, y)
                # 曲线拟合
                x_for_fit, y_for_fit = choose_range(wav, sp_row, x1=510, x2=900)
                fitting_paras = triple_peaks_fitting(x_for_fit, y_for_fit, ax=ax)
                # 储存拟合参数
                ints_row.append(fitting_paras["mag"])
                cws_row.append(fitting_paras["cw"])
                gammas_row.append(fitting_paras["linewidth"])

                the_figure(ax, title=f"{powers[i]}uW_{row}")
                if save_folder:
                    fig.savefig(os.path.join(save_folder, f'{powers[i]}uW_{row}.png'))
                plt.close(fig)

            # 强度与err
            ints_row = sorted(ints_row)
            ints_row = ints_row[1:-1]  # 去掉最小值和最大值
            ints.append(np.mean(ints_row))  # 去掉最小值和最大值再平均
            err_ints_row = np.max(ints_row) - np.min(ints_row)  # 去掉最小值和最大值再取range
            err_ints.append(err_ints_row)

            # 中心波长与err
            cws_row = sorted(cws_row)
            cws_row = cws_row[1:-1]
            cws.append(np.mean(cws_row))
            err_cws_row = np.max(cws_row) - np.min(cws_row)
            err_cws.append(err_cws_row)

            # 线宽与err
            gammas_row = sorted(gammas_row)
            gammas_row = gammas_row[1:-1]
            gammas.append(np.mean(gammas_row))
            err_gammas_row = np.max(gammas_row) - np.min(gammas_row)
            err_gammas.append(err_gammas_row)
    return powers, ints, cws, gammas, err_ints, err_cws, err_gammas

def the_figure(ax, title):
    """拟合曲线"""
    set_figure.set_label_and_title(ax, title=title, ylabel='Intensity(cts)')
    set_figure.set_spines(ax)
    set_figure.set_tick(ax, ticks_xlabel=np.arange(400, 901, 50))  # Normalized
    plt.tight_layout()

def the_figure1(ax1):
    """P—I"""
    set_figure.set_label_and_title(ax1, title=f'',
                                   xlabel='Excitaion Power(uW)', ylabel='Intensity(cts)')
    set_figure.set_spines(ax1)
    set_figure.set_tick(ax1, ticks_xlabel=np.arange(0, 12001, 2000))  # Normalized
    plt.tight_layout()

def the_figure2(ax2):
    """P-CW"""
    set_figure.set_label_and_title(ax2, title=f'',
                                   xlabel='Excitaion Power(uW)', ylabel='Center Wavelength(nm)')
    set_figure.set_spines(ax2)
    set_figure.set_tick(ax2, ticks_xlabel=np.arange(0, 12001, 2000),
                        ticks_ylabel=np.arange(535, 541, 1))
    plt.tight_layout()

def the_figure3(ax3):
    """P-FWHM"""
    set_figure.set_label_and_title(ax3, title=f'',
                                   xlabel='Excitaion Power(uW)', ylabel='FWHM(nm)')
    set_figure.set_spines(ax3)
    set_figure.set_tick(ax3, ticks_xlabel=np.arange(0, 12001, 2000), ticks_ylabel=np.arange(0, 11, 1))
    plt.tight_layout()

if __name__ == '__main__':
    """路径"""
    h5_file = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6\measurement-6.h5"
    save_folder = os.path.join(os.path.dirname(h5_file), 'series-4', 'curve_fit')
    npz_file = os.path.join(os.path.dirname(save_folder), f'power_dependent_paras.npz')
    fig1_file = os.path.join(os.path.dirname(save_folder), f'power_dependent_intensity_of_peak-1.png')
    fig2_file = os.path.join(os.path.dirname(save_folder), f'power_dependent_center_wavelength_of_peak-1.png')
    fig3_file = os.path.join(os.path.dirname(save_folder), f'power_dependent_FWHM_of_peak-1.png')

    # 创建文件夹
    if not os.path.exists(save_folder):
        os.makedirs(save_folder, exist_ok=True)

    """加载并保存拟合数据"""
    # dir_name = 'OceanOpticsSpectrometer'
    # powers, ints, cws, gammas, err_ints, err_cws, err_gammas = load_data(h5_file, dir_name, save_folder=save_folder)
    # # 保存拟合数据
    # np.savez(npz_file, powers=powers, ints=ints, cws=cws, gammas=gammas, err_ints=err_ints, err_cws=err_cws, err_gammas=err_gammas)

    """作图并保存"""
    # 读取拟合数据
    data = np.load(npz_file)

    # 作图
    powers = np.array(data['powers'])
    ints = np.array(data['ints'])
    cws = np.array(data['cws'])
    gammas = np.array(data['gammas'])
    err_ints = np.array(data['err_ints'])
    err_cws = np.array(data['err_cws'])
    err_gammas = np.array(data['err_gammas'])

    """fig1-intensity"""
    colors = ['#1f77b4', '#1b1bff', '#ff7f0e']
    fmts = ['o', 'o--', '^']

    fig1 = plt.figure(figsize=(8*1.1, 6*1.1))
    fig2 = plt.figure(figsize=(8*1.1, 6*1.1))
    fig3 = plt.figure(figsize=(8*1.1, 6*1.1))
    ax1 = fig1.add_subplot(111)
    ax2 = fig2.add_subplot(111)
    ax3 = fig3.add_subplot(111)

    x = np.array(powers)

    y = np.array(ints)
    ax1.errorbar(powers, ints, yerr=err_ints, fmt=fmts[0], color=colors[0], ecolor=colors[0], capsize=10, label='Experimental Data')
    draw_power_dependent(powers, ints, ax=ax1)

    y = np.array(cws)
    ax2.errorbar(powers, cws, yerr=err_cws, fmt=fmts[1], color=colors[1], ecolor=colors[1], capsize=10)

    y = np.array(gammas)
    ax3.errorbar(powers, gammas, yerr=err_gammas, fmt=fmts[2], color=colors[2], ecolor=colors[2], capsize=10)

    # 保存图片
    the_figure1(ax1)
    fig1.savefig(fig1_file)
    the_figure2(ax2)
    fig2.savefig(fig2_file)
    the_figure3(ax3)
    fig3.savefig(fig3_file)

    plt.show()