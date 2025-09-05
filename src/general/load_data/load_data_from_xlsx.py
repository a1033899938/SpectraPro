"""
Author: Junjie-Xie
Updated: 2025/8/5
Functions: 
"""
import pandas as pd
import os
from openpyxl import load_workbook
import numpy as np
from typing import Union, Dict, List, Tuple
from src.general.progress_bar import *

def str_to_int(value):
    """尝试将值转换为int，无法转换则保持原类型"""
    try:
        # 先去除可能的空格
        if isinstance(value, str):
            value = value.strip()
        return int(float(value))
    except (ValueError, TypeError):
        # 无法转换（如包含非数字字符、None等），返回原值
        return value

def read_sheet(
        filepath: str,
        sheet_name: List[str],
        header_row: Union[None, int, List[int]]=None
)-> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]
]:

    df = pd.read_excel(filepath, header=header_row, sheet_name=sheet_name)  # 读取excel的DataFrame数据

    if isinstance(sheet_name, list):
        data_dict = {}
        header_dict = {}
        for key in df.keys():
            data_dict[key] = df[key].values
            if header_row is not None:
                header_dict[key] = np.transpose(np.array(df[key].columns.values.tolist()))
            else:
                header_dict[key] = None
        return data_dict, header_dict
    else:
        raise TypeError('sheet_name must be str or list')

def write_sheet(
        savepath: str,
        data_dict: Dict[str, np.ndarray],
        header_dict: Dict[str, np.ndarray] = None,
        if_sheet_exists: str = "replace"
) -> None:

    # 检查文件是否存在，决定打开模式
    file_exists = os.path.exists(savepath)
    mode = "a" if file_exists else "w"

    existing_sheets = []
    if file_exists:
        # 只读模式打开文件，获取所有工作表名
        wb = load_workbook(savepath, read_only=True)
        existing_sheets = wb.sheetnames
        wb.close()  # 关闭文件，避免占用

    if if_sheet_exists == "skip":
        ise = "replace"
    else:
        ise = if_sheet_exists

    # 创建ExcelWriter对象
    with pd.ExcelWriter(
            savepath,
            engine="openpyxl",
            mode=mode,
            if_sheet_exists=ise if mode == "a" else None
    ) as writer:

        columns = None
        # 遍历每个需要保存的工作表数据
        for sheet_name, data_array in data_dict.items():
            # 如果工作表已存在且需要跳过，则不执行写入
            if if_sheet_exists == "skip" and sheet_name in existing_sheets:
                print(f"工作表 '{sheet_name}' 已存在，已跳过写入")
                continue  # 跳过当前工作表，处理下一个

            # 处理表头（如果提供）
            if header_dict and sheet_name in header_dict:
                header_array = header_dict[sheet_name]

                if header_array is not None:
                    if header_array.size > 0:  # 表头需不为空
                        columns = header_array

            if columns is not None:
                data_array = np.vstack([columns, data_array])  # 将（行）表头和数据组合在一起，一起作为数据写入excel

            data_list = data_array.tolist()
            converted_data = [
                [str_to_int(cell) for cell in row]  # 处理每行的每个单元格
                for row in data_list
            ]
            # 写入Excel
            df = pd.DataFrame(converted_data)
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)  # 不写入行、列的索引标签

def process_1(data):
    new_data = np.array([], dtype=object).reshape(0, 6)
    prof_data = np.array([], dtype=object).reshape(0, 3)

    for iRow in range(data.shape[0]):  # 逐行读取
        # print_progress_bar(iRow, data.shape[0])
        row = data[iRow, :]
        if row[0] is np.nan:  # 如果本行的第一列为nan则跳过（认为是空行）
            continue
        else:
            prof_data = np.vstack([prof_data, row])
            if "选科要求" in row[0]:  # 直到读取到"选科要求"这一栏，开始处理本专业的信息
                n_data = prof_data.shape[0]
                if n_data not in [2, 3]:
                    print(f"警告：第{iRow}行附近的专业信息行数异常（{n_data}行），已跳过")
                    continue

                if n_data == 3:
                    prof_data_dict = {
                        "专业名称": prof_data[0, 0],
                        "计划招生": prof_data[0, 1],
                        "学制": prof_data[0, 2],

                        "招生要求": prof_data[1, 0],
                        "学费": prof_data[1, 2],

                        "选科要求": prof_data[2, 0],
                    }
                elif n_data == 2:
                    prof_data_dict = {
                        "专业名称": prof_data[0, 0],
                        "计划招生": prof_data[0, 1],
                        "学制": prof_data[0, 2],

                        "选科要求": prof_data[1, 0],
                        "学费": prof_data[1, 2],

                        "招生要求": "",
                    }
                else:
                    raise ValueError
                new_row = [prof_data_dict["专业名称"], prof_data_dict["计划招生"], prof_data_dict["招生要求"], prof_data_dict["选科要求"], prof_data_dict["学制"], prof_data_dict["学费"]]
                new_data = np.vstack([new_data, new_row])
                prof_data = np.array([], dtype=object).reshape(0, 3)  # 请空本专业信息，等待下一个专业信息
                prof_data_dict = {
                    "专业名称": "",
                    "计划招生": "",
                    "学制": "",
                    "招生要求": "",  # 如办学地点
                    "选科要求": "",
                    "学费": ""
                }
    return new_data

def process_2(data):
    new_data = np.array([], dtype=object).reshape(0, 1)
    for iRow in range(data.shape[0]):  # 逐行读取
        row = data[iRow, :]
        if row[0] not in new_data:
            new_data = np.vstack([new_data, row[0]])
    return new_data

def process_3(data):
    without_zero_data = np.array([], dtype=object).reshape(0, 4)
    for iRow in range(data.shape[0]):  # 逐行读取
        row = data[iRow, :]
        if row[2] != 0:
            without_zero_data = np.vstack([without_zero_data, row])

    new_data = sorted(without_zero_data, key=lambda x: (x[2], x[3]), reverse=False)
    new_data = np.array(new_data)
    return new_data

def process_4(data, my_sorted_profs):
    naked_colls_profs_data = {}
    num_last_row = -1
    for iRow in range(data.shape[0]):  # 逐行读取
        is_last_row = (iRow + 1 == data.shape[0])
        next_is_first_row = False
        if not is_last_row:
            next_is_first_row = not np.isnan(data[iRow+1, 0])

        if is_last_row or next_is_first_row:  # 如果读取完毕，或者下一行的第一列非空，则收集该学校数据
            naked_coll_profs_data = data[num_last_row+1:iRow+1, :]

            naked_colls_profs_data[naked_coll_profs_data[0, 1]] = {
                "序号": np.nan,
                "学校": naked_coll_profs_data[0, 1],
                "学校代码": naked_coll_profs_data[0, 2],
                "往年分数线2024": naked_coll_profs_data[0, 4],
                "往年分数线2023": naked_coll_profs_data[0, 5],
                "地区": naked_coll_profs_data[0, 6],
                "类别": naked_coll_profs_data[0, 7],
                "分数段": naked_coll_profs_data[0, 8],
                "专业信息-未整合": naked_coll_profs_data[1:, :]
            }
            num_last_row = iRow

    # # 处理收集完的学校数据
    header = ["序号", "学校", "学校代码", "往年分数线2024", "往年分数线2023", "地区", "类别", "分数段", "专业", "计划招生", "招生要求", "选科要求", "学制", "学费", "优先级1", "优先级2"]
    new_data = np.array(header)
    for coll, coll_data in naked_colls_profs_data.items():
        prof_data = coll_data["专业信息-未整合"][:, 1:4]
        integrated_prof_data = process_1(prof_data)

        # 排序
        sorted_prof_data = process_5(integrated_prof_data, my_sorted_profs)

        naked_colls_profs_data[coll].update({"专业信息-已整合": sorted_prof_data})
        del naked_colls_profs_data[coll]["专业信息-未整合"]

        new_row = np.array([])
        for i, (coll_data_key, coll_data_value) in enumerate(naked_colls_profs_data[coll].items()):
            if coll_data_key != "专业信息-已整合":
                new_row = np.append(new_row, coll_data_value)

        new_row = np.append(new_row, [np.nan] * 8)
        new_data = np.vstack([new_data, new_row])

        for iRow in range(naked_colls_profs_data[coll]["专业信息-已整合"].shape[0]):
            new_row = np.array([])
            row = naked_colls_profs_data[coll]["专业信息-已整合"][iRow]
            new_row = np.append([np.nan] * 8, row)
            new_data = np.vstack([new_data, new_row])
    return new_data

def process_5(integrated_prof_data, my_sorted_profs):
    list0 = my_sorted_profs[:, 1]
    list1 = integrated_prof_data[:, 0]
    prof_data = {}

    # 计算专业优先级
    in_list0 = [prof for prof in list1 if prof in list0]  # 步骤1：筛选list1中存在于list0的专业，并按在list0中的位置排序
    in_list0_sorted = sorted(in_list0, key=lambda x: np.where(list0 == x)[0][0])  # 按在np.array中的索引排序（保证优先级顺序）
    priority0 = in_list0_sorted[:6]  # 步骤2：选前6个作为优先级0

    for iRow, prof in enumerate(list1):
        prof_data[prof] = {
            "计划招生": integrated_prof_data[iRow, 1],
            "招生要求": integrated_prof_data[iRow, 2],
            "选科要求": integrated_prof_data[iRow, 3],
            "学制": integrated_prof_data[iRow, 4],
            "学费": integrated_prof_data[iRow, 5],
        }
        if prof in priority0:
            idx_in_list0 = np.where(list0 == prof)[0][0]
            prof_data[prof].update({"优先级1": 0})
            prof_data[prof].update({"优先级2": idx_in_list0})
        elif prof in list0:
            idx_in_list0 = np.where(list0 == prof)[0][0]
            prof_data[prof].update({"优先级1": 2})
            prof_data[prof].update({"优先级2": idx_in_list0})
        else:
            prof_data[prof].update({"优先级1": 1})
            prof_data[prof].update({"优先级2": np.nan})

    sorted_prof_dict = sorted(
        prof_data.items(),
        key=lambda x: (
            x[1]["优先级1"],  # 取第一个元素（value）的优先级1
            x[1]["优先级2"]  # 取第一个元素的优先级2
        )
    )

    sorted_prof_data = np.array([], dtype=object).reshape(0, 8)
    for prof, prof_data in sorted_prof_dict:
        row = [prof]
        for prof_data_key, prof_data_value in prof_data.items():
            row.append(prof_data_value)
        sorted_prof_data = np.vstack((sorted_prof_data, row))

    return sorted_prof_data
if __name__ == '__main__':
    filepath = r"E:\梦鑫志愿\Backup\梦鑫志愿-从头开始处理.xlsx"

    """读取专业裸数据 -> 整合专业数据"""
    # sheet_name = ["专业裸数据"]
    # data_dict, header_dict = read_sheet(filepath, sheet_name=sheet_name, header_row=None)
    # naked_profs_data = data_dict["专业裸数据"]
    #
    # integrated_profs_data = process_1(data=naked_profs_data)
    # data_dict.update({"专业数据-整合后": integrated_profs_data})
    # header_dict.update({"专业数据-整合后": np.array(["专业名称", "计划招生", "招生要求", "选科要求", "学制", "学费"])})
    # write_sheet(filepath, data_dict=data_dict, header_dict=header_dict, if_sheet_exists='skip')

    """读取整合的专业数据 -> 筛选不重复的专业"""
    # sheet_name = ["专业数据-整合后"]
    # data_dict, header_dict = read_sheet(filepath, sheet_name=sheet_name, header_row=None)
    # integrated_profs_data = data_dict["专业数据-整合后"]
    #
    # non_repetitive_profs = process_2(data=integrated_profs_data)
    # data_dict.update({"专业-不重复": non_repetitive_profs})
    # header_dict.update({"专业-不重复": None})
    # write_sheet(filepath, data_dict=data_dict, header_dict=header_dict, if_sheet_exists='skip')

    # 用ai给专业分类，并手动进行专业排序

    """读取手动排序的专业 -> 自动给专业排序（除去为0的专业）"""
    # sheet_name = ["专业-手动排序"]
    # data_dict, header_dict = read_sheet(filepath, sheet_name=sheet_name, header_row=[0])
    # manually_sorted_profs = data_dict["专业-手动排序"]
    #
    # auto_sorted_profs = process_3(data=manually_sorted_profs)
    # data_dict.update({"专业-自动排序": auto_sorted_profs})
    # header_dict.update({"专业-自动排序": None})
    # write_sheet(filepath, data_dict=data_dict, header_dict=header_dict, if_sheet_exists='replace')

    # 手动copy学校和专业的裸数据

    """读取学校和专业的裸数据 -> 整合学校和专业数据"""
    # 读取我的排序
    sheet_name = ["专业-自动排序"]
    data_dict, header_dict = read_sheet(filepath, sheet_name=sheet_name, header_row=[0])
    my_sorted_profs = data_dict["专业-自动排序"]

    sheet_name = ["学校&专业裸数据"]
    data_dict, header_dict = read_sheet(filepath, sheet_name=sheet_name, header_row=[0])
    naked_colls_profs_data = data_dict["学校&专业裸数据"]

    sorted_colls_profs_data = process_4(data=naked_colls_profs_data, my_sorted_profs=my_sorted_profs)
    data_dict.update({"学校&专业数据-排序后": sorted_colls_profs_data})
    header_dict.update({"学校&专业数据-排序后": None})
    write_sheet(filepath, data_dict=data_dict, header_dict=header_dict, if_sheet_exists='skip')



