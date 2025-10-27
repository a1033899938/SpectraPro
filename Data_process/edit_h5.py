import h5py
import os


def delete_h5_group(file_path, group_rel_path):
    print("危险操作：此操作将永久删除HDF5文件中的Group及其所有内容")
    confirmation = input("输入 'go' 继续，其他输入取消：")
    if confirmation.lower() != 'go':
        print("操作已取消")
        return

    with h5py.File(file_path, 'a') as f:
        if group_rel_path in f:
            del f[group_rel_path]
            print(f"已删除 Group: {group_rel_path}")
        else:
            print(f"错误：Group '{group_rel_path}' 不存在")


def move_h5_group(h5_file_path, source_path, target_path):
    """
    在HDF5文件中移动Group，从源路径到目标路径

    参数:
    h5_file_path (str): HDF5文件路径
    source_path (str): 源Group路径
    target_path (str): 目标Group路径
    """
    print("危险操作：此操作将永久移动HDF5文件中的Group，源路径内容将被删除")
    confirmation = input("输入 'go' 继续，其他输入取消：")
    if confirmation.lower() != 'go':
        print("操作已取消")
        return

    with h5py.File(h5_file_path, 'a') as f:
        # 检查源Group是否存在
        if source_path not in f:
            print(f"错误：源Group '{source_path}' 不存在")
            return

        # 检查目标路径是否已存在
        if target_path in f:
            print(f"错误：目标路径 '{target_path}' 已存在")
            return

        # 创建目标路径的父级Group（如果不存在）
        target_parent = f.get(target_path.rsplit('/', 1)[0])
        if target_parent is None and '/' in target_path:
            f.create_group(target_path.rsplit('/', 1)[0])

        # 复制源Group到目标路径
        f.copy(source_path, target_path)

        # 删除源Group
        del f[source_path]

        print(f"成功将Group从 '{source_path}' 移动到 '{target_path}'")


def copy_group_between_files(source_file_path, source_path, target_file_path, target_path):
    """
    将一个HDF5文件中的Group复制到另一个HDF5文件的指定路径

    参数:
    source_file_path (str): 源HDF5文件路径
    source_path (str): 源Group路径
    target_file_path (str): 目标HDF5文件路径
    target_path (str): 目标Group路径
    """
    print("危险操作：此操作可能覆盖目标HDF5文件中的现有内容")
    confirmation = input("输入 'go' 继续，其他输入取消：")
    if confirmation.lower() != 'go':
        print("操作已取消")
        return

    try:
        # 打开源文件（只读模式）
        with h5py.File(source_file_path, 'r') as source_file:
            # 检查源路径是否存在
            if source_path not in source_file:
                raise ValueError(f"源路径 '{source_path}' 不存在于文件 '{source_file_path}' 中")

            # 打开目标文件（读写模式，如果不存在则创建）
            with h5py.File(target_file_path, 'a') as target_file:
                # 检查目标路径是否已存在
                if target_path in target_file:
                    print(f"警告: 目标路径 '{target_path}' 已存在，将被覆盖")
                    # 删除现有目标路径
                    del target_file[target_path]

                # 复制Group（使用浅复制，不递归复制外部链接）
                source_file.copy(source_path, target_file, name=target_path,
                                 shallow=True, expand_external=False)

                print(
                    f"成功将 Group '{source_path}' 从 '{source_file_path}' 复制到 '{target_file_path}' 的 '{target_path}'")

    except FileNotFoundError:
        print(f"错误: 文件未找到 - 源文件: {source_file_path}, 目标文件: {target_file_path}")
    except PermissionError:
        print(f"错误: 权限不足，无法访问文件 - 源文件: {source_file_path}, 目标文件: {target_file_path}")
    except ValueError as val_err:
        print(f"值错误: {val_err}")
    except Exception as e:
        print(f"未知错误: {e}")


import h5py


def rename_h5_object(file_path, old_path, new_path):
    """
    修改HDF5文件中Group或Dataset的名称

    参数:
        file_path (str): HDF5文件路径
        old_path (str): 原对象（Group或Dataset）的路径
        new_path (str): 新对象的路径
    """
    print("危险操作：此操作可能覆盖目标HDF5文件中的现有内容")
    confirmation = input("输入 'go' 继续，其他输入取消：")
    if confirmation.lower() != 'go':
        print("操作已取消")
        return

    # 验证路径格式（确保以 '/' 开头，避免相对路径问题）
    if not old_path.startswith('/'):
        old_path = '/' + old_path
    if not new_path.startswith('/'):
        new_path = '/' + new_path

    # 检查新旧路径是否相同
    if old_path == new_path:
        print("原路径与新路径相同，无需修改")
        return

    try:
        with h5py.File(file_path, 'r+') as f:
            # 检查原路径是否存在
            if old_path not in f:
                raise ValueError(f"路径 '{old_path}' 不存在于文件中")

            # 检查新路径是否已存在
            if new_path in f:
                raise ValueError(f"路径 '{new_path}' 已存在，无法重命名（避免覆盖）")

            # 获取原对象
            old_obj = f[old_path]

            # 复制原对象到新路径（h5py的copy方法会自动处理Group的递归复制）
            f.copy(old_obj, new_path)

            # 删除原对象
            del f[old_path]

            # 判断对象类型并输出结果
            obj_type = "Group" if isinstance(old_obj, h5py.Group) else "Dataset"
            print(f"成功将{obj_type} '{old_path}' 重命名为 '{new_path}'")

    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 未找到")
    except PermissionError:
        print(f"错误：没有权限操作文件 '{file_path}'")
    except ValueError as e:
        print(f"错误：{e}")
    except Exception as e:
        print(f"操作失败：{e}")

if __name__ == '__main__':
    pass
    filepath = r"E:\Data\ExpData\SPE\20251015_HQ-hBN_PDMSvsTap\measurement-1_basic_PL.h5"
    del_groups = ["HQ-PDMS10times-hBN_1$_p1_scan_z_0", "HQ-PDMS10times-hBN_2-1$_p1_scan_z_0", "HQ-PDMS10times-hBN_2-2$_p1_scan_z_0", "HQ-PDMS10times-hBN_3$_p1_scan_z_0",
                  "HQ-PDMS10times-hBN_3woSEM$_p1_scan_z_0", "HQ-PDMS10times-hBN_sub_p1_scan_z_0", "HQ-allTap-hBN_1$_p1_scan_z_0", "HQ-allTap-hBN_2$_p1_scan_z_0", "HQ-allTap-hBN_3$_p1_scan_z_0"]

    for del_group in del_groups:
        del_group = f"OceanOpticsSpectrometer/{del_group}"
        delete_h5_group(filepath, del_group)




    # old_path = "OceanOpticsSpectrometer/HQ-PDMS10times-hBN_1$_p7_scan_z_450ex-50uW_0"
    # new_path = "OceanOpticsSpectrometer/HQ-PDMS10times-hBN_1$_p6_scan_z_450ex-50uW_0"
    # rename_h5_object(filepath, old_path, new_path)
    #
    # old_path = "OceanOpticsSpectrometer/HQ-PDMS10times-hBN_1$_p7_scan_z_450ex-50uW_1"
    # new_path = "OceanOpticsSpectrometer/HQ-PDMS10times-hBN_1$_p7_scan_z_450ex-50uW_0"
    # rename_h5_object(filepath, old_path, new_path)

