import h5py
import numpy as np
import matplotlib.pyplot as plt
from src.general.figure.draw_figure import *
from src.my_style.my_mapping_para import *
from src.general.numerical.edit_data import *


def load_and_compare_data(h5_file, dir_name, bgd_name):
    with h5py.File(h5_file, "r") as f:
        # 读取mapping group
        data = f[dir_name]

        # 读取第一个sp的bgd和wav，并对积分时间作归一化
        bgd = np.array(data[bgd_name].attrs['background'])
        bgd_time = data[bgd_name].attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        wav = np.array(data[bgd_name].attrs['wavelengths'])

        # 创建主画布
        fig_main = plt.figure(figsize=(10, 8))
        ax_main = fig_main.add_subplot(111)

        # 存储拟合结果
        fitting_results = {}

        # 处理第一组数据 (Onway_P1-450ex-*)
        print("处理第一组数据 (Onway):")
        sp_names_1 = []
        powers_1 = []
        for key in data.keys():
            if 'Onway_P1-450ex-' in key and not any(
                    sub_key in key for sub_key in ['P1-450ex-10uW_1', 'P1-450ex-10uW_2']):
                sp_names_1.append(key)
                powers_1.append(int(key[len('Onway_P1-450ex-'):-len("uW_0")]))

        powers_1, sp_names_1 = sort_lists(powers_1, sp_names_1)

        # 专门提取并处理 "Onway_P1-450ex-1000uW_0"
        target_sp1 = "Onway_P1-450ex-1000uW_0"
        if target_sp1 in sp_names_1:
            print(f"处理目标光谱: {target_sp1}")
            sp_2d = data[target_sp1]
            sp_time = sp_2d.attrs['integration_time'] / 1000
            sp_2d = np.array(sp_2d)

            for row in range(sp_2d.shape[0]):
                if row != 20:  # 只处理第20行
                    continue
                sp = sp_2d[row, :]
                sp = sp / sp_time
                sp = sp - bgd
                power = 1000  # 已知功率
                sp = sp / power

                x, y = choose_range(wav, sp, x1=510, x2=900, axis=0)

                # 绘制原始数据
                ax_main.plot(x, y, 'b-', linewidth=2, label="Onway_hBN")

                # 进行拟合
                # fitting_paras = quatra_peaks_fitting(x, y, ax=ax_main)
                # fitting_results[target_sp1] = fitting_paras

                # # 在图上标注拟合信息
                # ax_main.text(0.05, 0.95, f'{target_sp1} 拟合结果:',
                #              transform=ax_main.transAxes, fontsize=10, color='blue')
                # for j, mag in enumerate(['mag1', 'mag2', 'mag3', 'mag4']):
                #     if mag in fitting_paras:
                #         ax_main.text(0.05, 0.90 - j * 0.05, f'Peak{j + 1}: {fitting_paras[mag]:.2f}',
                #                      transform=ax_main.transAxes, fontsize=9, color='blue')

        # 处理第二组数据 (P1-450ex-*)
        print("\n处理第二组数据:")
        sp_names_2 = []
        powers_2 = []
        for key in data.keys():
            if 'P1-450ex-' in key and not any(
                    sub_key in key for sub_key in ['P1-450ex-10uW_1', 'P1-450ex-10uW_2', 'Onway']):
                sp_names_2.append(key)
                powers_2.append(int(key[len('P1-450ex-'):-len("uW_0")]))

        powers_2, sp_names_2 = sort_lists(powers_2, sp_names_2)

        # 专门提取并处理 "P1-450ex-1000uW_4"
        target_sp2 = "P1-450ex-1000uW_4"
        if target_sp2 in sp_names_2:
            print(f"处理目标光谱: {target_sp2}")
            sp_2d = data[target_sp2]
            sp_time = sp_2d.attrs['integration_time'] / 1000
            sp_2d = np.array(sp_2d)

            for row in range(sp_2d.shape[0]):
                if row != 20:  # 只处理第20行
                    continue
                sp = sp_2d[row, :]
                sp = sp / sp_time
                sp = sp - bgd
                power = 1000  # 已知功率
                sp = sp / power

                x, y = choose_range(wav, sp, x1=510, x2=900, axis=0)

                # 绘制原始数据
                ax_main.plot(x, y, 'r-', linewidth=2, label="HQ_hBN")

                # 进行拟合
                fitting_paras = quatra_peaks_fitting(x, y, ax=ax_main)
                fitting_results[target_sp2] = fitting_paras

                # # 在图上标注拟合信息
                # ax_main.text(0.55, 0.95, f'{target_sp2} 拟合结果:',
                #              transform=ax_main.transAxes, fontsize=10, color='red')
                # for j, mag in enumerate(['mag1', 'mag2', 'mag3', 'mag4']):
                #     if mag in fitting_paras:
                #         ax_main.text(0.55, 0.90 - j * 0.05, f'Peak{j + 1}: {fitting_paras[mag]:.2f}',
                #                      transform=ax_main.transAxes, fontsize=9, color='red')

        # 设置图形属性
        set_label_and_title(ax_main, title='Comparison between hBN from Onway and HQ',
                            xlabel='Wavelength (nm)', ylabel='Normalized Intensity')
        set_spines(ax_main)
        set_tick(ax_main, ticks_xlabel=np.arange(510, 901, 100))
        set_legend(ax_main)
        plt.tight_layout()

        return fig_main, fitting_results


def the_figure(ax):
    """图形设置函数"""
    set_label_and_title(ax, title=f'', ylabel='Intensity(cts)')
    set_spines(ax)
    set_tick(ax, ticks_xlabel=np.arange(510, 901, 100))
    set_legend(ax)
    plt.tight_layout()


if __name__ == '__main__':
    # 读取mapping数据
    h5_file = r"D:\ExpData\SPE\20250702_SPE_hBN_SEM_array\measurement-1.h5"
    bgd_name = "P1-450ex-10uW_0"

    # 执行比较分析
    fig_comparison, fitting_results = load_and_compare_data(
        h5_file=h5_file,
        dir_name='OceanOpticsSpectrometer',
        bgd_name=bgd_name
    )

    # 打印拟合结果
    print("\n=== 拟合结果汇总 ===")
    for sp_name, paras in fitting_results.items():
        print(f"\n{sp_name}:")
        for key, value in paras.items():
            if 'mag' in key:
                print(f"  {key}: {value:.4f}")

    plt.show()