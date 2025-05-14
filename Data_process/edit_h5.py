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
    except h5py.H5Error as h5_err:
        print(f"HDF5 操作错误: {h5_err}")
    except ValueError as val_err:
        print(f"值错误: {val_err}")
    except Exception as e:
        print(f"未知错误: {e}")

if __name__ == '__main__':
    pass
    # source_file = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-9\20250224_SPE_hBN_afterSEM_measurement-9.h5"
    # source_path = "LumeneraCamera"
    # target_file = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-9\20250224_SPE_hBN_afterSEM_measurement-9-final.h5"
    # target_path = "LumeneraCamera"
    # copy_group_between_files(source_file, source_path, target_file, target_path)

    # h5_file = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-9\20250224_SPE_hBN_afterSEM_measurement-9.h5"
    # source_path = 'OceanOpticsSpectrometer/hBN_afterSEM_mapping_3'
    # target_path = 'OceanOpticsSpectrometer/hBN_afterSEM_mapping_0'
    # move_h5_group(h5_file, source_path, target_path)

    # h5_file = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-9\20250224_SPE_hBN_afterSEM_measurement-9.h5"
    # delete_h5_group(h5_file, "OceanOpticsSpectrometer/hBN_afterSEM_mapping_1")
    # delete_h5_group(h5_file, "OceanOpticsSpectrometer/hBN_afterSEM_mapping_4")
    # delete_h5_group(h5_file, "hBN_afterSEM_mapping_3")
    # delete_h5_group(h5_file, "hBN_afterSEM_mapping_4")