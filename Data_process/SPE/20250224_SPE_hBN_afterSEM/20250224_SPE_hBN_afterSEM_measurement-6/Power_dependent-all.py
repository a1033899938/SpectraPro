import os

from src.general.figure import set_figure
from src.general.figure.draw_figure import draw_power_dependent
from src.my_style.my_mapping_para import *

def the_figure1(ax1):
    """P—I"""
    set_figure.set_label_and_title(ax1, title=f'',
                                   xlabel='Excitaion Power(uW)', ylabel='Intensity(cts)')
    set_figure.set_spines(ax1)
    set_figure.set_tick(ax1, ticks_xlabel=np.arange(0, 12001, 2000), yaxis_use_log_scale=True)  # Normalized
    set_figure.set_scientific_y_ticks(ax1)
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
    npz_files = [r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6\single_spectrum-0\PL_mapping.npz",
                 r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6\series-1\power_dependent_paras.npz",
                 r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6\series-4\power_dependent_paras.npz",
                 r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6\series-5\power_dependent_paras.npz"]
    le = ["single_spectrum",
          "series-1",
          "series-4",
          "series-5"]
    save_folder = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-6\all"
    fig1_file = os.path.join(save_folder, f'power_dependent_intensity_of_peak-1.png')
    fig2_file = os.path.join(save_folder, f'power_dependent_center_wavelength_of_peak-1.png')
    fig3_file = os.path.join(save_folder, f'power_dependent_FWHM_of_peak-1.png')

    # 创建文件夹
    if not os.path.exists(save_folder):
        os.makedirs(save_folder, exist_ok=True)

    """作图并保存"""
    fig1 = plt.figure(figsize=(8 * 1.2, 6 * 1.3))
    fig2 = plt.figure(figsize=(8 * 1.2, 6 * 1.2))
    fig3 = plt.figure(figsize=(8 * 1.2, 6 * 1.2))
    ax1 = fig1.add_subplot(111)
    ax2 = fig2.add_subplot(111)
    ax3 = fig3.add_subplot(111)
    colors = ['#1f77b4', '#1b1bff', '#ff7f0e']
    fmts = ['o-', 'o-', 'o-']
    for i, npz_file in enumerate(npz_files):
        # 读取拟合数据
        data = np.load(npz_file)

        # 作图
        powers = np.array(data['powers'])
        ints = np.array(data['ints'])
        cws = np.array(data['cws'])
        gammas = np.array(data['gammas'])
        if i != 0:
            err_ints = np.array(data['err_ints'])
            err_cws = np.array(data['err_cws'])
            err_gammas = np.array(data['err_gammas'])

        """fig1-intensity"""
        x = np.array(powers)

        if i != 0:
            y = np.array(ints)
            ax1.errorbar(powers, ints, yerr=err_ints, markersize=10, markerfacecolor='none', markeredgecolor='blue', markeredgewidth=1.5, fmt=fmts[0], color=colors[0], ecolor=colors[0], capsize=10, label='Experimental Data')
            draw_power_dependent(powers, ints, ax=ax1)

            y = np.array(cws)
            ax2.errorbar(powers, cws, yerr=err_cws, markersize=10, markerfacecolor='none', markeredgecolor='blue',
                         markeredgewidth=1.5, fmt=fmts[1], color=colors[1], ecolor=colors[1], capsize=10)

            y = np.array(gammas)
            ax3.errorbar(powers, gammas, yerr=err_gammas, markersize=10, markerfacecolor='none', markeredgecolor='blue',
                         markeredgewidth=1.5, fmt=fmts[2], color=colors[2], ecolor=colors[2], capsize=10)
        else:
            y = np.array(ints)
            ax1.plot(x, y, 'o-', markersize=10, markerfacecolor='none', markeredgecolor='blue', markeredgewidth=1.5)

            y = np.array(cws)
            ax2.plot(x, y, 'o-', markersize=10, markerfacecolor='none', markeredgecolor='blue', markeredgewidth=1.5)

            y = np.array(gammas)
            ax3.plot(x, y, 'o-', markersize=10, markerfacecolor='none', markeredgecolor='blue', markeredgewidth=1.5)

    # 保存图片
    the_figure1(ax1)
    fig1.savefig(fig1_file)
    the_figure2(ax2)
    fig2.savefig(fig2_file)
    the_figure3(ax3)
    fig3.savefig(fig3_file)

    plt.show()