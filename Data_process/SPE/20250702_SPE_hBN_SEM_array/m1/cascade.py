import h5py

from src.my_style.my_mapping_para import *
from src.general.numerical.edit_data import *

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
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
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
    return ax

if __name__ == '__main__':
    h5_file = r"D:\ExpData\SPE\20250702_SPE_hBN_SEM_array\measurement-1.h5"
    dir_name = "OceanOpticsSpectrometer"
    bgd_name = "P1-450ex-10uW_0"
    sp_names = ["P1-450ex-10uW_0",
                "P1-450ex-20uW_0",
                "P1-450ex-50uW_0",
                "P1-450ex-100uW_0",
                "P1-450ex-200uW_0",
                "P1-450ex-500uW_0",
                "P1-450ex-1000uW_0",
                "P1-450ex-1000uW_1",
                "P1-450ex-1000uW_2",
                "P1-450ex-1000uW_3",
                "P1-450ex-1000uW_4",
                "P1-450ex-1000uW_5",
                "P1-450ex-1000uW_6",
                "P1-450ex-1000uW_7",
                "P1-450ex-1000uW_8",
                "P1-450ex-1000uW_9"]
    load_data(h5_file, dir_name, bgd_name, sp_names)
    plt.show()

