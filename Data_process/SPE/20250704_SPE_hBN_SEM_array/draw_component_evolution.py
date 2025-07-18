import h5py

from src.general.figure.draw_figure import *
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

        sp_names = []
        for key in data.keys():
            if "$" in key:
                sp_names.append(key)

        sps = None
        for sp_name in sp_names:
            print(sp_name)
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111)
            sps_now = data[sp_name]
            sp_time = sps_now.attrs['integration_time'] / 1000
            sps_now = np.array(sps_now)
            sps_now = sps_now / sp_time
            bgds, _ = np.meshgrid(bgd,range(sps_now.shape[0]))
            sps_now = sps_now - bgd

            peak_component_evolution(wav, sps_now, [538, 550, 575, 700], ax)
            ax.set_title(sp_name)
            set_legend(ax)
    return ax

if __name__ == '__main__':
    h5_file = r"D:\ExpData\SPE\20250704_SPE_hBN_SEM_array\measurement-1.h5"
    dir_name = "OceanOpticsSpectrometer"
    bgd_name = "hBN_1#_1$_P7-1_10uW_0"
    with h5py.File(h5_file, "r") as f:
        data = f[dir_name]

    # from src.general.load_data.read_name import *
    # print_name_in_h5(h5_file, dir_name, field_in=["hBN_1#_1$_P6-1"], sort_field=["hBN_1#_1$_P6-1", "uW_0"])
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
    sp_names = ["hBN_1#_1$_P2-1_1000uW_2",
                "hBN_1#_1$_P3-1_2000uW_1",
                "hBN_1#_1$_P4-1_m2_2000uW_0",
                "hBN_1#_1$_P4-1_m2_2000uW_1",
                "hBN_1#_1$_P4-1_m2_2000uW_2",
                "hBN_1#_1$_P5-1_1000uW_0",
                "hBN_1#_1$_P5-1_2000uW_0"]
    ax = load_data(h5_file, dir_name, bgd_name, sp_names)
    plt.show()

