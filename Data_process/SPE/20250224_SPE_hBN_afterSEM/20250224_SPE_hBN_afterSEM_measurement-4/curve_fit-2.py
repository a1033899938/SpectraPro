import os
import spe_loader as sl

import scipy.io as sio


class read_file:
    def __init__(self, filepath, strip='all', show_data_flag=True):
        self.filepath = filepath
        self.strip = strip
        self.show_data_flag = show_data_flag
        self.filetype = None
        self.data = None
        self.determine_filetype()
        self.data = self.read_data()

    def determine_filetype(self):
        """determine_filetype"""
        self.filetype = os.path.splitext(self.filepath)[1]
        return self.filetype

    def read_data(self):
        if self.filetype == '.spe':
            return self.read_spe()
        elif self.filetype == '.mat':
            return self.read_mat()
        elif self.filetype == '.txt':
            return self.read_txt()
        elif self.filetype == '.h5':
            return self.read_h5()
        else:
            raise ValueError("Unsupported file type")

    def read_spe(self):
        try:
            print('path now:')
            print(self.filepath)
            sp = sl.load_from_files([self.filepath])
            data = {}
            if sp.xdim[0] > sp.ydim[0]:
                data['xdim'] = sp.xdim[0]
                data['ydim'] = sp.ydim[0]
                data['intensity_image'] = np.squeeze(np.array(sp.data))
                data['wavelength'] = sp.wavelength
                data['strip'] = range(data['ydim'])
            else:
                data['xdim'] = sp.ydim[0]
                data['ydim'] = sp.xdim[0]
                data['intensity_image'] = np.transpose(np.squeeze(np.array(sp.data)))
                data['wavelength'] = sp.wavelength
                data['strip'] = range(data['ydim'])

            if self.strip == 'all':
                data['intensity'] = np.sum(data['intensity_image'], axis=0)
            else:
                self.strip = np.array(self.strip)
                data['intensity'] = np.sum(data['intensity_image'][self.strip.min():self.strip.max(), :], axis=0)

            if self.show_data_flag:
                print("==========data==========")
                pprint.pprint(data)
                print("========data end========")
            return data
        except Exception as e:
            print(f"Error read_file.read_spe:\n  |--> {e}")

    def read_mat(self):
        try:
            print('path now:')
            print(self.filepath)
            mat_data = sio.loadmat(self.filepath, squeeze_me=True, struct_as_record=False)
            sp = matstruct_to_dict(mat_data['spnow'])
            print(sp['xdim'])
            print(dir(sp))
            data = {}
            if sp['xdim'] > sp['ydim']:
                data['xdim'] = sp['xdim']
                data['ydim'] = sp['ydim']
                data['intensity_image'] = np.squeeze(np.array(sp['int']))
                data['wavelength'] = sp['wavelength']
                data['strip'] = range(data['ydim'])
            else:
                data['xdim'] = sp['ydim']
                data['ydim'] = sp['xdim']
                data['intensity_image'] = np.transpose(np.squeeze(np.array(sp['int'])))
                data['wavelength'] = sp['wavelength']
                data['strip'] = range(data['ydim'])

            if self.strip == 'all':
                data['intensity'] = np.sum(data['intensity_image'], axis=0)
            else:
                self.strip = np.array(self.strip)
                data['intensity'] = np.sum(data['intensity_image'][self.strip.min():self.strip.max(), :], axis=0)

            if self.show_data_flag:
                print("==========data==========")
                pprint.pprint(data)
                print("========data end========")
            return data
        except Exception as e:
            print(f"Error read_file.read_spe:\n  |--> {e}")

    def read_txt(self):
        try:
            with open(self.filepath, "r") as f:  # 打开文件
                sp = np.loadtxt(f, usecols=(0, 1), skiprows=0)

            data = {}
            data['wavelength'] = sp[:, 0]
            data['intensity'] = sp[:, 1]

            if self.show_data_flag:
                print("==========data==========")
                pprint.pprint(data)
                print("========data end========")
            return data
        except Exception as e:
            print(f"Error read_file.read_txt:\n  |--> {e}")

    def read_h5(self):
        try:
            pass
        except Exception as e:
            print(f"Error read_file.read_h5:\n  |--> {e}")


def matstruct_to_dict(matstruct):
    """
    递归函数，用于将 mat_struct 对象转换为字典。
    """
    if isinstance(matstruct, sio.matlab.mio5_params.mat_struct):
        d = {}
        for field_name in matstruct._fieldnames:
            item = getattr(matstruct, field_name)
            if isinstance(item, sio.matlab.mio5_params.mat_struct):
                d[field_name] = matstruct_to_dict(item)
            else:
                d[field_name] = item
        return d
    else:
        return matstruct


if __name__ == '__main__':
    import h5py
    import matplotlib.pyplot as plt
    import pprint
    from src.general.figure import set_figure
    from scipy.optimize import curve_fit
    import numpy as np
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection


    def the_figure(ax):
        """拟合曲线"""
        set_figure.set_label_and_title(ax, title=f'', ylabel='Intensity(cts)')
        set_figure.set_spines(ax)
        set_figure.set_tick(ax, ticks_xlabel=np.arange(500, 701, 50))  # Normalized
        set_figure.set_scientific_y_ticks(ax, sci_fontsize=20)
        plt.tight_layout()

    def gaussian(x, A, mu, sigma):
        return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))


    def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
        return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))

    def lorentzian(x, A, x0, gamma):
        """
        洛伦兹函数
        :param x: 自变量
        :param A: 峰值面积
        :param x0: 峰值中心位置
        :param gamma: 半高全宽 (FWHM)
        :return: 洛伦兹函数值
        """
        return (A / np.pi) * (0.5 * gamma) / ((x - x0) ** 2 + (0.5 * gamma) ** 2)

    def double_lorentzian(x, A1, x1, gamma1, A2, x2, gamma2):
        peak1 = lorentzian(x, A1, x1, gamma1)
        peak2 = lorentzian(x, A2, x2, gamma2)
        return peak1 + peak2


    def triple_lorentzian(x, A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3):
        peak1 = lorentzian(x, A1, x1, gamma1)
        peak2 = lorentzian(x, A2, x2, gamma2)
        peak3 = lorentzian(x, A3, x3, gamma3)
        return peak1 + peak2 + peak3

    def lorentzian_plus_gaussian(x, A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3):
        peak1 = lorentzian(x, A1, x1, gamma1)
        peak2 = gaussian(x, A2, x2, gamma2)
        peak3 = lorentzian(x, A3, x3, gamma3)
        return peak1 + peak2 + peak3

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import numpy as np

    datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-4\measurement-4.h5"
    save_fig = 1

    """fig0"""
    with h5py.File(datapath1, "r") as f:
        data = f['OceanOpticsSpectrometer']

        mag_fits = np.zeros([6, 4])
        wav_fits = np.zeros([6, 4])
        gamma_fits = np.zeros([6, 4])
        mag_max = np.zeros([6, 4])
        fig0 = plt.figure(figsize=(8, 6))
        ax0 = fig0.add_subplot(111)
        for key in data.keys():
            print(key)

            sp = data[key]
            bgd = np.array(sp.attrs['background'])
            wav = np.array(sp.attrs['wavelengths'])
            sp_time = sp.attrs['integration_time'] / 1000
            bgd_time = sp.attrs['background_int'] / 1000
            sp = sp / sp_time
            bgd = bgd / bgd_time
            sp = np.array(sp) - bgd

            min_differences = np.abs(wav - 500)
            min_index = np.argmin(min_differences)
            max_differences = np.abs(wav - 700)
            max_index = np.argmin(max_differences)

            x = wav[min_index:max_index]
            y = sp[min_index:max_index]

            ax0.plot(x, y)

            try:
                if '15kV' in key:
                    row = 2
                elif '10kV' in key:
                    row = 1
                elif '5kV' in key:
                    row = 0
                else:
                    print('error: kV')

                if '0.5min' in key:
                    col = 0
                elif '1min' in key:
                    col = 1
                elif '2min' in key:
                    col = 2
                elif '5min' in key:
                    col = 3
                else:
                    print('error: min')

                if '60KX' in key:
                    pass
                elif '100KX' in key:
                    row += 3
                else:
                    print('error: KX')

                """三峰拟合"""
                p0 = [100, 537, 6,
                        20, 550, 10,
                         20, 577, 6]

                bounds = ([0, 535, 0,
                           0, 540, 0,
                           0, 570, 0],
                          [100000, 540, 10,
                            100000, 565, 100,
                            100000, 580, 26])
                min_differences_for_fit = np.abs(wav - 510)
                min_index_for_fit = np.argmin(min_differences_for_fit)
                max_differences_for_fit = np.abs(wav - 900)
                max_index_for_fit = np.argmin(max_differences_for_fit)

                x_for_fit = wav[min_index_for_fit:max_index_for_fit]
                y_for_fit = sp[min_index_for_fit:max_index_for_fit]
                popt, pcov = curve_fit(lorentzian_plus_gaussian, x_for_fit, y_for_fit, p0=p0, bounds=bounds)

                # popt, pcov = curve_fit(triple_lorentzian, x, y, p0=p0, bounds=bounds)
                A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3 = popt
                mag_now = (A1/np.pi)/(gamma1/2)
                wav_now = x1
                gamma_now = gamma1

                # mag_fits.append(mag_now)
                # wav_fits.append(wav_now)
                # gamma_fits.append(gamma_now)
                mag_fits[row][col] = mag_now
                mag_max[row][col] = np.max(y_for_fit)
                wav_fits[row][col] = wav_now
                gamma_fits[row][col] = gamma_now

                print(f'拟合结果: A1 = {A1:.2f}, mu1 = {x1:.2f}, sigma1 = {gamma1:.2f}, '
                      f'A2 = {A2:.2f}, mu2 = {x2:.2f}, sigma2 = {gamma2:.2f}',
                      f'A3 = {A2:.2f}, mu3 = {x3:.2f}, sigma3 = {gamma3:.2f}')
                y_fit = lorentzian_plus_gaussian(x, *popt)
                y_fit1 = lorentzian(x_for_fit, A1, x1, gamma1)
                y_fit2 = gaussian(x_for_fit, A2, x2, gamma2)
                y_fit3 = lorentzian(x_for_fit, A3, x3, gamma3)
                # ax0.plot(x, y_fit, 'r-', label='Fitted Gaussian')
                # ax0.plot(x_for_fit, y_fit1, 'b--', label='Fitted Gaussian')
                # ax0.plot(x_for_fit, y_fit2, 'g--', label='Fitted Gaussian')
                # ax0.plot(x_for_fit, y_fit3, 'm--', label='Fitted Gaussian', linewidth=2)
            except Exception as e:
                print(e)

            the_figure(ax0)
            # title = f'{key[:-2]}'
            # set_figure.set_label_and_title(ax0, title=title, ylabel='Intensity(counts)',
            #                                label_fontsize=25, title_fontsize=25,
            #                                label_font_family='Times New Roman', title_font_family='Times New Roman',
            #                                label_fontweight='bold', title_fontweight='bold',
            #                                label_pad=15, title_pad=15)
            # set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
            # set_figure.set_tick(ax0, xbins=16, ybins=10, fontsize=10, fontweight='bold',
            #                     linewidth=3, tick_pad=5, direction='in',
            #                     ticks_xlabel=np.arange(400, 901, 50))  # Normalized
            # # ax0.grid(True)
            # plt.tight_layout()
            if save_fig == 1:
                plt.savefig(fr'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-4\curve_fit-2\20250224_SPE_hBN_afterSEM_measurement4_curve_fit-{key}.png')

        """peak1"""
        """fig1"""
        fig0 = plt.figure(figsize=(8, 6))
        ax0 = fig0.add_subplot(111, projection='3d')
        x = np.array([0.5, 1, 2, 5])
        y = np.arange(0, 6, 1)
        X, Y = np.meshgrid(x, y)
        Z = gamma_fits

        for i in y:
            ax0.plot(Y[i], X[i], Z[i], 'o-', markeredgecolor='black', markerfacecolor=plt.cm.viridis(i / len(y)), markersize=8, linewidth=1, alpha=1)
            ax0.plot(Y[i], X[i], np.zeros_like(Z[i]), color='gray', alpha=1)

            polygon = [
                [Y[i, 0], X[i, 0], 0],  # 左下
                [Y[i, -1], X[i, -1], 0],  # 右下
            ]
            for j in range(len(x) - 1, -1, -1):  # 依次添加点，使得polygon成为一个完整的闭合多边形
                polygon.append([Y[i, j], X[i, j], Z[i, j]])
            ax0.add_collection3d(Poly3DCollection([polygon], color=plt.cm.viridis(i / len(y)), alpha=0.5))

        # title = f'Linewidth of peak-1'
        # set_figure.set_label_and_title(ax0, title=title, xlabel='Exposure time(min)', ylabel='Intensity(counts)',
        #                                label_fontsize=20, title_fontsize=25,
        #                                label_font_family='Times New Roman', title_font_family='Times New Roman',
        #                                label_fontweight='bold', title_fontweight='bold',
        #                                label_pad=15, title_pad=5, mode='3d')
        # set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
        # set_figure.set_tick(ax0, xbins=6, ybins=5, fontsize=15, fontweight='bold',
        #                     linewidth=3, tick_pad=5, direction='in', mode='3d')  # Normalized
        # plt.xticks(np.arange(0, 6), ['5', '10', '15', '5*', '10*', '15*'], rotation=0)
        # ax0.set_ylabel(ylabel='Exposure Time(min)', labelpad=15)
        # ax0.set_xlabel(xlabel='EHT(kV)', labelpad=15)
        # ax0.zaxis.set_rotate_label(False)  # 关闭默认旋转设置
        # ax0.set_zlabel(zlabel='FWHM(nm)', rotation=90, labelpad=15)
        # # ax0.grid(True)
        # ax0.view_init(elev=20, azim=45)
        # # ax0.view_init(elev=0, azim=0)
        # ax0.set_zlim([0, 12])
        # plt.tight_layout()

        # from src.general.save_figure import save_subfig
        if save_fig == 1:
            plt.savefig(
                fr'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-4\curve_fit-2\20250224_SPE_hBN_afterSEM_measurement4_curve_fit-paras_phase_linewidth_peak-1.png')

        """fig2"""
        fig0 = plt.figure(figsize=(8, 6))
        ax0 = fig0.add_subplot(111, projection='3d')
        x = np.array([0.5, 1, 2, 5])
        y = np.arange(0, 6, 1)
        X, Y = np.meshgrid(x, y)
        Z = mag_fits

        for i in y:
            ax0.plot(Y[i], X[i], Z[i], 'o-', markeredgecolor='black', markerfacecolor=plt.cm.viridis(i / len(y)), markersize=8, linewidth=1, alpha=1)
            ax0.plot(Y[i], X[i], np.zeros_like(Z[i]), color='gray', alpha=1)

            polygon = [
                [Y[i, 0], X[i, 0], 0],  # 左下
                [Y[i, -1], X[i, -1], 0],  # 右下
            ]
            for j in range(len(x) - 1, -1, -1):  # 依次添加点，使得polygon成为一个完整的闭合多边形
                polygon.append([Y[i, j], X[i, j], Z[i, j]])
            ax0.add_collection3d(Poly3DCollection([polygon], color=plt.cm.viridis(i / len(y)), alpha=0.5))

        # title = f'Magnitude of peak-1'
        # set_figure.set_label_and_title(ax0, title=title, xlabel='Process time(min)', ylabel='Intensity(counts)',
        #                                label_fontsize=20, title_fontsize=25,
        #                                label_font_family='Times New Roman', title_font_family='Times New Roman',
        #                                label_fontweight='bold', title_fontweight='bold',
        #                                label_pad=15, title_pad=5, mode='3d')
        # set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
        # set_figure.set_tick(ax0, xbins=6, ybins=5, fontsize=15, fontweight='bold',
        #                     linewidth=3, tick_pad=5, direction='in', mode='3d')  # Normalized
        # plt.xticks(np.arange(0, 6), ['5', '10', '15', '5*', '10*', '15*'], rotation=0)
        # ax0.set_ylabel(ylabel='Exposure Time(min)', labelpad=15)
        # ax0.set_xlabel(xlabel='EHT(kV)', labelpad=15)
        # ax0.zaxis.set_rotate_label(False)  # 关闭默认旋转设置
        # ax0.set_zlabel(zlabel='Intensity(counts)', rotation=90, labelpad=15)
        # # ax0.grid(True)
        # ax0.view_init(elev=20, azim=45)
        # # ax0.view_init(elev=0, azim=0)
        # plt.tight_layout()

        # from src.general.save_figure import save_subfig
        if save_fig == 1:
            plt.savefig(
                fr'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-4\curve_fit-2\20250224_SPE_hBN_afterSEM_measurement4_curve_fit-paras_phase_magnitude_peak-1.png')

        """fig3"""
        fig0 = plt.figure(figsize=(8, 6))
        ax0 = fig0.add_subplot(111, projection='3d')
        x = np.array([0.5, 1, 2, 5])
        y = np.arange(0, 6, 1)
        X, Y = np.meshgrid(x, y)
        Z = wav_fits
        np.save(os.path.join(os.path.dirname(datapath1), fr'wavlength_fit.npy'), Z)

        for i in y:
            ax0.plot(Y[i], X[i], Z[i], 'o-', markeredgecolor='black', markerfacecolor=plt.cm.viridis(i / len(y)), markersize=8, linewidth=1, alpha=1)
            ax0.plot(Y[i], X[i], np.zeros_like(Z[i])+535, color='gray', alpha=1)

            polygon = [
                [Y[i, 0], X[i, 0], 535],  # 左下
                [Y[i, -1], X[i, -1], 535],  # 右下
            ]
            for j in range(len(x) - 1, -1, -1):  # 依次添加点，使得polygon成为一个完整的闭合多边形
                polygon.append([Y[i, j], X[i, j], Z[i, j]])
            ax0.add_collection3d(Poly3DCollection([polygon], color=plt.cm.viridis(i / len(y)), alpha=0.5))

        # title = f'Center-wavelength of peak-1'
        # set_figure.set_label_and_title(ax0, title=title, xlabel='Process time(min)', ylabel='Intensity(counts)',
        #                                label_fontsize=20, title_fontsize=25,
        #                                label_font_family='Times New Roman', title_font_family='Times New Roman',
        #                                label_fontweight='bold', title_fontweight='bold',
        #                                label_pad=15, title_pad=5, mode='3d')
        # set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
        # set_figure.set_tick(ax0, xbins=6, ybins=5, fontsize=15, fontweight='bold',
        #                     linewidth=3, tick_pad=5, direction='in', mode='3d')  # Normalized
        # plt.xticks(np.arange(0, 6), ['5', '10', '15', '5*', '10*', '15*'], rotation=0)
        # ax0.set_ylabel(ylabel='Exposure Time(min)', labelpad=15)
        # ax0.set_xlabel(xlabel='EHT(kV)', labelpad=15)
        # ax0.zaxis.set_rotate_label(False)  # 关闭默认旋转设置
        # ax0.set_zlabel(zlabel='Wavelength(nm)', rotation=90, labelpad=15)
        # # ax0.grid(True)
        # ax0.view_init(elev=20, azim=45)
        # # ax0.view_init(elev=0, azim=0)
        # ax0.set_zlim([535, 540])
        # plt.tight_layout()

        # from src.general.save_figure import save_subfig
        if save_fig == 1:
            plt.savefig(
                fr'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-4\curve_fit-2\20250224_SPE_hBN_afterSEM_measurement4_curve_fit-paras_phase_centerwavelength_peak-1.png')

        """fig4"""
        fig0 = plt.figure(figsize=(8, 6))
        ax0 = fig0.add_subplot(111, projection='3d')
        x = np.array([0.5, 1, 2, 5])
        y = np.arange(0, 6, 1)
        X, Y = np.meshgrid(x, y)
        Z = mag_max

        for i in y:
            ax0.plot(Y[i], X[i], Z[i], 'o-', markeredgecolor='black', markerfacecolor=plt.cm.viridis(i / len(y)), markersize=8, linewidth=1, alpha=1)
            ax0.plot(Y[i], X[i], np.zeros_like(Z[i]), color='gray', alpha=1)

            polygon = [
                [Y[i, 0], X[i, 0], 0],  # 左下
                [Y[i, -1], X[i, -1], 0],  # 右下
            ]
            for j in range(len(x) - 1, -1, -1):  # 依次添加点，使得polygon成为一个完整的闭合多边形
                polygon.append([Y[i, j], X[i, j], Z[i, j]])
            ax0.add_collection3d(Poly3DCollection([polygon], color=plt.cm.viridis(i / len(y)), alpha=0.5))

        # title = f'Maximum of curve'
        # set_figure.set_label_and_title(ax0, title=title, xlabel='Process time(min)', ylabel='Intensity(counts)',
        #                                label_fontsize=20, title_fontsize=25,
        #                                label_font_family='Times New Roman', title_font_family='Times New Roman',
        #                                label_fontweight='bold', title_fontweight='bold',
        #                                label_pad=15, title_pad=5, mode='3d')
        # set_figure.set_spines(ax0, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
        # set_figure.set_tick(ax0, xbins=6, ybins=5, fontsize=15, fontweight='bold',
        #                     linewidth=3, tick_pad=5, direction='in', mode='3d')  # Normalized
        # plt.xticks(np.arange(0, 6), ['5', '10', '15', '5*', '10*', '15*'], rotation=0)
        # ax0.set_ylabel(ylabel='Exposure Time(min)', labelpad=15)
        # ax0.set_xlabel(xlabel='EHT(kV)', labelpad=15)
        # ax0.zaxis.set_rotate_label(False)  # 关闭默认旋转设置
        # ax0.set_zlabel(zlabel='Peak Intensity(counts)', rotation=90, labelpad=15)
        # # ax0.grid(True)
        # ax0.view_init(elev=20, azim=45)
        # # ax0.view_init(elev=0, azim=0)
        # plt.tight_layout()

        if save_fig == 1:
            plt.savefig(
                fr'D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-4\curve_fit-2\20250224_SPE_hBN_afterSEM_measurement4_curve_fit-paras_phase_Maximum_of_peaks.png')
    plt.show()