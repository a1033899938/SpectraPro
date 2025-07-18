import h5py

from src.my_style.my_mapping_para import *


def load_data(h5_file, dir_name, bgd_name, sp_names):
    with h5py.File(h5_file, "r") as f:
        # 读取mapping group
        data = f[dir_name]
        # 读取第一个sp的bgd和wav，并对积分时间作归一化
        bgd = np.array(data[bgd_name].attrs['background'])
        bgd_time = data[bgd_name].attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        wav = np.array(data[bgd_name].attrs['wavelengths'])

        sps = None
        for sp_name in sp_names:
            sps_now = data[sp_name]
            sp_time = sps_now.attrs['integration_time'] / 1000
            sps_now = np.array(sps_now)
            sps_now = sps_now / sp_time
            bgds, _ = np.meshgrid(bgd,range(sps_now.shape[0]))
            sps_now = sps_now - bgd

            # 首次循环时初始化sps
            if sps is None:
                sps = sps_now
            else:
                # 后续循环中，纵向堆叠数组
                sps = np.vstack((sps, sps_now))

        # sps = np.array(sps)
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        x = wav
        y = range(sps.shape[0])
        X, Y = np.meshgrid(x,y)
        Z = sps
        print(np.shape(x))
        print(np.shape(y))
        print(np.shape(X))
        print(np.shape(Y))
        print(np.shape(Z))
        cascade_3d(X, Y, Z, ax)
        ax.view_init(elev=20, azim=45)  # 调整视角

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        peaks = peak_component_evolution(wav, sps, [538, 550, 575], ax)
        idx_max = np.argmax(peaks[0])
        val_max = peaks[0, idx_max]
        idx_min = np.argmin(np.abs(peaks[0, :] - val_max/np.exp(1)))
        print(idx_max-idx_min)
        decline_single_step = 1/((idx_max-idx_min)*0.5)
        print(decline_single_step)
    return ax

if __name__ == '__main__':
    h5_file = r"D:\ExpData\SPE\20250704_SPE_hBN_SEM_array\measurement-1.h5"
    dir_name = "OceanOpticsSpectrometer"
    bgd_name = "hBN_1#_1$_P7-1_10uW_0"
    with h5py.File(h5_file, "r") as f:
        data = f[dir_name]

    from src.general.load_data.read_name import *
    nums,  sp_names= print_name_in_h5(h5_file, dir_name, field_in=["forward"], sort_field=["hBN_1#_2$_P1_100uW_forward_", ""], print_names=False)
    # sp_names = ["hBN_1#_1$_P7-1_10uW_0",
    #             "hBN_1#_1$_P7-1_20uW_0",
    #             "hBN_1#_1$_P7-1_50uW_0",
    #             "hBN_1#_1$_P7-1_100uW_0",
    #             "hBN_1#_1$_P7-1_200uW_0",
    #             "hBN_1#_1$_P7-1_500uW_0",
    #             "hBN_1#_1$_P7-1_1000uW_0",
    #             "hBN_1#_1$_P7-1_2000uW_0",
    #             "hBN_1#_1$_P7-1_2000uW_1",
    #             "hBN_1#_1$_P7-1_2000uW_2",
    #             "hBN_1#_1$_P7-1_2000uW_3"]
    # sp_names = ["hBN_1#_1$_P4-1_m2_1000uW_0"]
    ax = load_data(h5_file, dir_name, bgd_name, sp_names)
    plt.show()

