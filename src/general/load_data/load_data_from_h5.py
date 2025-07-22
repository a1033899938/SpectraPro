"""
Author: Junjie-Xie
Updated: 2025/07/18
Functions:
    1. 从HDF5文件中加载指定目录下的名称（支持关键词筛选和排序）
    2. 从HDF5文件中加载、筛选、保存图像（支持显示图像）
    3. 从HDF5文件中加载映射（mapping）数据，计算像素点参数并保存结果
"""
import h5py
from src.my_style.my_mapping_para import *
from src.general.sys.folder import *
from src.general.numerical.edit_data import *

def load_names(h5file: str, dir_name: str='OceanOpticsSpectrometer', field_in: list=None, field_out: list=None, sort_field: list=None, print_names: bool=True):
    """
    :param h5file: 文件路径
    :param dir_name: h5文件中存储目标光谱的组路径
    :param field_in: 必须包含的关键词列表，全部满足才会被选中
    :param field_out: 必须排除的关键词列表，全部不包含才会被选中
    :param sort_field: 排序字段，格式为(前缀字符串, 后缀字符串)
    :param print_names: 是否打印筛选出的名称
    :return: 无返回值
    """
    with h5py.File(h5file, 'r') as f:
        data = f[dir_name]
        sp_names = []
        nums = []
        for key in data.keys():
            if_print = True
            if field_in is None:
                pass
            else:
                if not all(element in key for element in field_in):
                    if_print = False

            if field_out is None:
                pass
            else:
                if not all(element not in key for element in field_out):
                    if_print = False

            if if_print:
                sp_names.append(key)
                if sort_field is not None:
                    idx_start = len(sort_field[0]) if sort_field[0] else None
                    idx_end = -len(sort_field[1]) if sort_field[1] else None
                    nums.append(int(key[idx_start : idx_end]))

        if sort_field is not None:
            nums, sp_names = sort_lists(nums, sp_names)

        if print_names:
            for sp_name in sp_names:
                print(f"\"{sp_name}\",")
    return nums, sp_names

def load_images(h5file: str, dir_name: str='LumeneraCamera', save_folder: list=None, field_in: list=None, field_out: list=None, draw_image: bool=False):
    """
    从.h5文件中导入读取并保存指定图像
    :param h5file: 文件路径
    :param dir_name: h5文件中存储图像的组路径
    :param save_folder: 保存图像的文件夹路径，默认为h5文件同级目录
    :param field_in: 必须包含的关键词列表，全部满足才会被显示/保存
    :param field_out: 必须包含的关键词列表，全部满足才会被显示/保存
    :param draw_image: 是否在加载时显示图像
    :return: 无返回值
    """
    from PIL import Image

    with h5py.File(h5file, "r") as f:
        data = f[dir_name]
        for i, key in enumerate(data.keys()):

            if_save = True
            # 只有满足包含field_in中所有元素, 且不包含field_out中的任意元素, 图片才会被保存
            if field_in is None:
                pass
            else:
                if not all(element in key for element in field_in):
                    if_save = False

            if field_out is None:
                pass
            else:
                if not all(element not in key for element in field_out):
                    if_save = False

            # 如果没有给出图片保存路径, 则默认保存在h5文件的同级目录中
            if save_folder is None:
                save_folder = os.path.dirname(h5file)

            if if_save:
                img = data[key]
                img = np.asarray(img)
                if data[key].ndim == 2:
                    img = Image.fromarray(img.astype(np.uint8))  # 转换为 PIL 图像
                    img.save(os.path.join(save_folder, f'{key}.png'))
                elif data[key].ndim == 3:
                    img = Image.fromarray(img.astype(np.uint8))  # 转换为 PIL 图像
                    img.save(os.path.join(save_folder, f'{key}.png'))
                else:
                    print(f"图像 {i} 的维度不支持：{img.shape}")

            if draw_image:
                # 可选：使用 matplotlib 显示图像
                plt.imshow(img, cmap='gray' if data[key].ndim == 2 else None)
                plt.title(f'Image {i}')
                plt.show()

def load_mapping(h5_file, dir_name, group_name, calculate_mapping_para, sp_name=None, save_path=None, bgd_name=None):
    """
    从.h5文件中导入指定mapping数据
    :param h5_file: 文件路径
    :param dir_name: h5文件中存储目标mapping组的组路径
    :param group_name: 目标mapping组的名称
    :param sp_name: mapping子光谱的文件名(有时因为重命名, group_name与sp_name不一致), 默认为group_name[:-2]
    :param save_path: mapping数据文件保存路径, 默认为h5文件同级目录, 默认名称为sp_name
    :param calculate_mapping_para: 计算mapping像素点数据的方法, 可以返回多种参数值, 对应不同参数的mapping图(请统一写在my_style/my_mapping_para.py中, 然后调用)
    :param bgd_name: 背景光谱的文件名(有时mapping的背景采集有问题, bgd_name与sp_name不一致)
    :return: 最终的mapping数据
    """
    if sp_name is None:
        sp_name = group_name[:-2]

    mapping_paras = {}

    if bgd_name is None:
        print(f"Read 'bgd' from first file.")
    with h5py.File(h5_file, "r") as f:
        # 读取mapping group
        data = f[dir_name][group_name]

        # 读取group下的keys（子group）和第一个子group下的所有keys（sp）
        row_keys = data.keys()
        row1_key = list(data.keys())[0]
        row1 = data[row1_key]
        column_keys_of_row1 = row1.keys()

        # 创建储存mapping数据的空数组
        mapping_shape = [len(row_keys), len(column_keys_of_row1)]
        empty_mapping = np.zeros([mapping_shape[0], mapping_shape[1]])

        if bgd_name is None:
            bgd_name = f'{dir_name}/{group_name}/x-0/{sp_name}-x0-y0'  # 读取第一个子group下的第一个sp的bgd

        # 读取对应光谱中的bgd和wav，并对积分时间作归一化
        bgd = np.array(f[bgd_name].attrs['background'])
        bgd_time = f[bgd_name].attrs['background_int'] / 1000
        bgd = bgd / bgd_time
        wav = np.array(f[bgd_name].attrs['wavelengths'])

        # 历遍所有sp
        for i in range(mapping_shape[0]):
            parent_key = f"x-{i}"
            for j in range(mapping_shape[1]):
                print(f"i now: {i}, j now: {j}")
                child_key = f"{sp_name}-x{i}-y{j}"
                sp = data[f"{parent_key}/{child_key}"]
                sp_time = sp.attrs['integration_time'] / 1000
                sp = np.array(sp)
                sp = sp / sp_time
                sp = sp - bgd

                # 调用计算mapping像素数据的函数
                fitting_paras = calculate_mapping_para(wav, sp)

                # 根据计算返回的拟合mapping参数
                if i == 0 and j == 0:
                    for key, value in fitting_paras.items():
                        mapping_paras[key] = np.zeros_like(empty_mapping)  # 以返回的参数字典的key作为这种变量对应mapping的参数名，并且创建空数组

                # 保存数据
                for key, value in fitting_paras.items():
                    mapping_paras[key][i][j] = value

    if save_path is None:
        save_path = f"{sp_name}.npz"

    create_folder(save_path)
    np.save(save_path, mapping_paras)
    return mapping_paras

if __name__ == '__main__':
    """读取mapping数据"""
    h5_file = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-9\20250224_SPE_hBN_afterSEM_measurement-9.h5"
    mapping_paras = load_mapping(
                        h5_file=h5_file,
                        dir_name='OceanOpticsSpectrometer',
                        group_name='hBN_afterSEM_mapping_6',
                        sp_name='hBN_1-2_beforeSEM_mapping',
                        save_path=os.path.join(os.path.dirname(h5_file), 'hBN_afterSEM_mapping_6'),
                        calculate_mapping_para=triple_peaks_fitting,
                        bgd_name=None)

    for key, value in mapping_paras.items():
        print('\n')
        print(key)
        print(np.shape(value))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(value)
    plt.show()

