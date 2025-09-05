"""
Author: Junjie-Xie
Updated: 2025/8/8
Functions: 
"""

import h5py
from src.general.load_data.load_data_from_h5 import *

# 原数据集名称和新名称
filepath = r"D:\ExpData\LabInstrumentTest\NewVsOld Ocean-20250807\new\NewVsOldSpectrometer.h5"

# old_name = "original_dataset"
# new_name = "new_dataset_name"

# 打开文件（读写模式）
with h5py.File(filepath, "r+") as f:
    data = f["OceanOpticsSpectrometer"]
    # 复制原数据集到新名称
    # data["newSM_MoSe2ML_m2-1uW_0"] = data["newSM_MoSe2ML_m2-1uW_1"]

    # 删除原数据集
    del data["oldSM_Lamp_1_0"]
    del data["oldSM_Lamp_2_0"]
    del data["oldSM_Lamp_new_0"]
    pass
# print(f"数据集已从 {old_name} 重命名为 {new_name}")

load_names(filepath, field_out=None, sort_field=None, print_names=True)