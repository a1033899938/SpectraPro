"""
Author: Junjie-Xie
Updated: 2025/10/14
Functions: 
"""
import numpy as np
import matplotlib.pyplot as plt
import h5py
from scipy.optimize import curve_fit
from src.general.numerical.edit_data import *
from src.my_style.my_color import *
from src.general.numerical.curve_functions import *
import json

# 自定义编码器：处理 ndarray
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # 转为列表
        # 处理其他可能的 NumPy 类型（如 numpy 数字类型）
        if np.isscalar(obj):
            return obj.item()
        return super().default(obj)

all_bgd_data = {
    1:
        {
            r"D:\ExpData\SPE\20250224_HQ-PDMS\measurement-2_try_power-dependent-PL.h5":
                {
                    "OceanOpticsSpectrometer":
                        {"name": "hBN_afterSEM_5kV_5min_expose10s_10uW__1"}
                },
        },
    2:
        {
            r"D:\ExpData\SPE\20250224_HQ-PDMS\20250224_SPE_hBN_afterSEM_measurement-3.h5":
                {
                    "OceanOpticsSpectrometer":
                        {
                            "type": "dir",
                            "hBN_afterSEM_5kV_2min_10uW_1":
                                {
                                    "type": "spectrum"
                                },
                            "hBN_afterSEM_5kV_2min_10uW_2":
                                {
                                    "type": "spectrum"
                                }
                        }
                }
        },
    3:
        {
            r"D:\ExpData\SPE\20250305_SPE_hBN_SEM_array\20250403_SPE_hBN_SEM_array-measurement-1.h5":
                {
                    "OceanOpticsSpectrometer":
                        {
                            "type": "dir",
                            "hBN_SEM_array-1#_200KX-1_200uW_0":
                                {
                                    "type": "spectrum"
                                },
                            "hBN_SEM_array-1#_1000KX-1_200uW_0":
                                {
                                    "type": "spectrum"
                                }
                        }
                }
        },
    4:
        {
            r
        }
}
# print(np.max(list(all_bgd_data.keys())))

# with open("All_bgd.json", "r", encoding="utf-8") as F:
#     jsondata = json.load(F)
#     print(jsondata)
#     with h5py.File(filepath, "r") as f:
#         data = f[f'OceanOpticsSpectrometer']
#
#         for i, key in enumerate(keys3):
#             raw = data[key]
#
#             bgd = np.array(raw.attrs['background'])
#             bgd_time = raw.attrs['background_int'] / 1000
#             bgd = bgd / bgd_time
#
#             wav = np.array(raw.attrs['wavelengths'])
#
#             raw_time = raw.attrs['integration_time'] / 1000
#             raw = np.array(raw)
#             raw = raw / raw_time
#
#             wav, bgd, raw = choose_range(wav, bgd, raw, x1=400, x2=1100)
#             sp = raw - bgd
#
#             p0 = [100, 535, 30,
#                   100, 585, 30]
#
#             bounds = ([0, 520, 5,
#                        0, 560, 5],
#                       [100000, 560, 100,
#                        100000, 600, 100])
#
#             if i == 0:
#                 fig = plt.figure(figsize=(12, 8))
#                 ax = fig.add_subplot(111)
#
#             sp = sp / np.max(sp)
#             ax.plot(wav, sp, label=key)
#
#             jsondata.update({f"20250224_HQ-PDMS_key={key}": {"wav": wav, "sp": sp}})
#             # x, y = choose_range(wav, sp, x1=510, x2=900)
#             # popt, pcov = curve_fit(double_gaussian, x, y, p0=p0, bounds=bounds)
#             # A1, mu1, sigma1, A2, mu2, sigma2 = popt
#             # y_fit1 = gaussian(x, A1, mu1, sigma1)
#             # y_fit2 = gaussian(x, A2, mu2, sigma2)
#             # ax.plot(x, y_fit1)
#             # ax.plot(x, y_fit2)
#             # ax.plot(x, y_fit1 + y_fit2, "--", color='blue')
#
# with open("All_bgd.json", 'w', encoding='utf-8') as F:
#     json.dump(jsondata, F, ensure_ascii=False, indent=4, cls=NumpyEncoder)
#
# print(f"数据已成功保存")
plt.show()