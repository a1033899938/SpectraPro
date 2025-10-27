"""
Author: Junjie-Xie
Updated: 2025/7/23
Functions: 对比不同样品5kV, 50KX, 1min点位在50uW辐照下的光谱(未消去bgd之前). 探明中心在550nm, FWHM约100-150nm的bgd的来源
"""
import numpy as np
import matplotlib.pyplot as plt
import h5py
from src.my_style.my_color import *
from src.my_style.my_figure import the_cascade_2d

h5_files = [r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-3\measurement-3.h5",
            r"D:\ExpData\SPE\20250305_SPE_hBN_SEM_array\20250403_SPE_hBN_SEM_array-measurement-2.h5",
            r"D:\ExpData\SPE\20250513_SPE_hBN_SEM_array\hBN-3\20250513_SPE_hBN-3_SEM_array-measurement-1.h5",
            r"D:\ExpData\SPE\20250620_SPE_hBN_SEM_array\m2_20250618_2sample+20250620_3sample.h5",
            r"D:\ExpData\SPE\20250620_SPE_hBN_SEM_array\m2_20250618_2sample+20250620_3sample.h5",
            r"D:\ExpData\SPE\20250620_SPE_hBN_SEM_array\m2_20250618_2sample+20250620_3sample.h5",
            r"D:\ExpData\SPE\20250702_SPE_hBN_SEM_array\measurement-1.h5",
            r"D:\ExpData\SPE\20250702_SPE_hBN_SEM_array\measurement-1.h5",
            r"D:\ExpData\SPE\20250702_SPE_hBN_SEM_array\measurement-1.h5",
            r"D:\ExpData\SPE\20250702_SPE_hBN_SEM_array\measurement-1.h5",
            r"D:\ExpData\SPE\20250704_SPE_hBN_SEM_array\measurement-1.h5"]

dirnames = ['OceanOpticsSpectrometer',
           'OceanOpticsSpectrometer',
           'OceanOpticsSpectrometer/hBN_3_afterSEM_mapping_0/x-11',
           'OceanOpticsSpectrometer',
           'OceanOpticsSpectrometer',
           'OceanOpticsSpectrometer',
           'OceanOpticsSpectrometer',
           'OceanOpticsSpectrometer',
           'OceanOpticsSpectrometer',
           'OceanOpticsSpectrometer',
           'OceanOpticsSpectrometer',]

lowpower_sp_names = ["hBN_afterSEM_5kV_1min_50uW_0",
                     None,
                    "hBN_3_afterSEM_mapping-x11-y21",
                    "hBN-HQ-PDMS-1_0",
                    "hBN-Onway-PDMS-1_0",
                    "hBN-HQ-ScotchTap-1_0",
                    "P1-450ex-50uW_0",
                    "Onway_P2-450ex-50uW_0",
                    "Onway_P4-450ex-50uW_0",
                    "Onway_P7-450ex-50uW_0",
                    "hBN_1#_1$_P3-1_50uW_0",]

highpower_sp_names = ["hBN_afterSEM_5kV_1min_3000uW_0",
                      "20250403_hBN_SEMarray_10kV_30s_450ex_500uW_m1_50kx_row3_0_0",
                      None,
                      None,
                      None,
                      None,
                      "P1-450ex-1000uW_9",
                      None,
                      None,
                      None,
                      "hBN_1#_1$_P3-1_2000uW_1"
                      ]
sample_names = ["20250224_HQ_PDMS",
                "20250305_HQ_PDMS",
                "20250513_Onway_PDMS",
                "20250620_HQ_PDMS",
                "20250620_Onway_PDMS",
                "20250620_HQ_pdmsAssistTap",
                "20250702_HQ_PDMS",
                "20250702_Onway_PDMS",
                "20250702_Onway_PDMS",
                "20250702_Onway_PDMS",
                "20250704_HQ_PDMS",]

int_HQs = None
int_Ons = None
int_HPs = None  #HP: High power excitation HQ
wav_HQs = None
wav_Ons = None
wav_HPs = None
le_HQs = None
le_Ons = None
le_HPs = None
for i in range(len(h5_files)):
    h5_file = h5_files[i]

    with h5py.File(h5_file, "r") as f:
        dirname = dirnames[i]
        data = f[dirname]

        # 未大功率辐照前的光谱
        lowpower_sp_name = lowpower_sp_names[i]
        if lowpower_sp_name is not None:
            sp = data[lowpower_sp_name]

            bgd = np.array(sp.attrs['background'])
            bgd_time = sp.attrs['background_int'] / 1000
            bgd = bgd / bgd_time
            wav = np.array(sp.attrs['wavelengths'])
            sp_time = sp.attrs['integration_time'] / 1000
            sp_int = np.array(sp)
            if sp_int.ndim == 2:
                sp_int = sp_int[5, :]

            sp_int = sp_int / sp_time
            sp_int = sp_int - bgd
            sp_int = sp_int / np.max(sp_int)
            le = sample_names[i]
            if 'HQ' in le:
                if int_HQs is None:
                    int_HQs = sp_int
                    wav_HQs = wav
                    le_HQs = [le]
                else:
                    int_HQs = np.vstack((int_HQs, sp_int))
                    wav_HQs = np.vstack((wav_HQs, wav))
                    le_HQs.append(le)
            else:
                if int_Ons is None:
                    int_Ons = sp_int
                    wav_Ons = wav
                    le_Ons = [le]
                else:
                    int_Ons = np.vstack((int_Ons, sp_int))
                    wav_Ons = np.vstack((wav_Ons, wav))
                    le_Ons.append(le)

            # print(le_HQs)
        # 大功率辐照后的光谱
        highpower_sp_name = highpower_sp_names[i]
        if highpower_sp_name is not None:
            sp = data[highpower_sp_name]

            bgd = np.array(sp.attrs['background'])
            bgd_time = sp.attrs['background_int'] / 1000
            bgd = bgd / bgd_time
            wav = np.array(sp.attrs['wavelengths'])
            sp_time = sp.attrs['integration_time'] / 1000
            sp_int = np.array(sp)
            if sp_int.ndim == 2:
                sp_int = sp_int[5, :]

            sp_int = sp_int / sp_time
            sp_int = sp_int - bgd
            sp_int = sp_int / np.max(sp_int)
            le = sample_names[i]

            if int_HPs is None:
                int_HPs = sp_int
                wav_HPs = wav
                le_HPs = [le]
            else:
                int_HPs = np.vstack((int_HPs, sp_int))
                wav_HPs = np.vstack((wav_HPs, wav))
                le_HPs.append(le)
h5_file = r"D:\ExpData\SPE\20250722_SPE_hBN_SEM_array\measurement-1.h5"
dirname = 'OceanOpticsSpectrometer'
with h5py.File(h5_file, "r") as f:
    data = f[dirname]
    int_Ps = None
    int_Ss = None
    int_Subs = None
    wav_Ps = None
    wav_Ss = None
    wav_Subs = None
    le_Ps = None
    le_Ss = None
    le_Subs = None

    for key in data.keys():
        if any([name in key for name in ["P6-450ex_50uW_0", "P8-450ex_50uW_0"]]):
            continue
        sp = data[key]

        bgd = np.array(sp.attrs['background'])
        bgd_time = sp.attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        wav = np.array(sp.attrs['wavelengths'])
        sp_time = sp.attrs['integration_time'] / 1000
        sp_int = np.array(sp)
        sp_int = sp_int[5, :]
        sp_int = sp_int / sp_time
        sp_int = sp_int - bgd
        sp_int = sp_int / np.max(sp_int)
        le = key[:-len("-450ex_50uW_0")]

        if "P" in le:
            if int_Ps is None:
                int_Ps = sp_int
                wav_Ps = wav
                le_Ps = [le]
            else:
                int_Ps = np.vstack((int_Ps, sp_int))
                wav_Ps = np.vstack((wav_Ps, wav))
                le_Ps.append(le)

        if "S" in le and "Sub" not in le:
            if int_Ss is None:
                int_Ss = sp_int
                wav_Ss = wav
                le_Ss = [le]
            else:
                int_Ss = np.vstack((int_Ss, sp_int))
                wav_Ss = np.vstack((wav_Ss, wav))
                le_Ss.append(le)

        if "Sub" in le:
            if int_Subs is None:
                int_Subs = sp_int
                wav_Subs = wav
                le_Subs = [le]
            else:
                int_Subs = np.vstack((int_Subs, sp_int))
                wav_Subs = np.vstack((wav_Subs, wav))
                le_Subs.append(le)

xs_group = [wav_HQs, wav_Ons, wav_HPs, wav_Ps, wav_Ss, wav_Subs]
ys_group = [int_HQs, int_Ons, int_HPs, int_Ps, int_Ss, int_Subs]
les_group = [le_HQs, le_Ons, le_HPs, le_Ps, le_Ss, le_Subs]
les_sg = ["HQ_50uW", "Onway_50uW", "HQ_500/1000uW", "HQ_Tap-50uW", "Sub_w/. exposed-50uW", "Sub_w/o exposed-50uW"]
cc = MyColor.get_color_series("cold_colors")
wc = MyColor.get_color_series("warm_colors")
colors_group = [wc, cc, wc, cc, cc, cc]
from src.general.figure.draw_figure import *
fig, axes = draw_cascade_group_2d(xs_group=xs_group, ys_group=ys_group, les_sg=les_sg, les_group=les_group, colors_group=colors_group, space = 0.1, axis = 0, figsize=None, dpi=300)
the_cascade_2d(axes, title="HQ/Onway hBN exfoliated\nfrom PDMS/Tap")

plt.show()