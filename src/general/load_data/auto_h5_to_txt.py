"""
Author: Junjie-Xie
Updated: 2025/9/6
Functions: 
"""
import h5py
from PIL import Image
from src.general.sys.folder import *
from src.general.load_data.save_read_data import *

def h5_to_txt(h5_filepath, des_folder):
    """
    将h5文件中的内容，按照原本层级保存
    :param h5_filepath:
    :param des_folder:
    :return:
    """
    """暂时只能读取一维数据，读取时间序列数据部分待完成"""
    def traversal_all_level(f, folder_now):
        for key in f.keys():
            print(key, type(f[key]))
            if isinstance(f[key], h5py._hl.group.Group):
                create_folder(os.path.join(folder_now, key))
                traversal_all_level(f[key], os.path.join(folder_now, key))
                pass
            elif isinstance(f[key], h5py._hl.dataset.Dataset):
                try:
                    data = f[key]
                    if "integration_time" in data.attrs:  # 视为光谱文件
                        sp = np.array(data)
                        sp_time = np.array(data.attrs.get('integration_time', []))
                        sp = sp / sp_time

                        bgd = np.array(data.attrs.get('background', []))
                        bgd_time = np.array(data.attrs.get('background_int', [])) / 1000
                        bgd = bgd / bgd_time

                        ref = np.array(data.attrs.get('reference', []))
                        ref_time = np.array(data.attrs.get('reference_int', [])) /1000
                        ref = ref / ref_time

                        wav = np.array(data.attrs.get('wavelengths', []))

                        datas = [sp, bgd, ref, wav]
                        lines_names = ["sp", "bgd", "ref", "wav"]
                        filtered = [(d, n) for d, n in zip(datas, lines_names) if d.size > 0]
                        datas, lines_names = zip(*filtered) if filtered else ([], [])
                        save_path = os.path.join(folder_now, f"{key}.txt")
                        save_lines_txt(*datas, save_path=save_path, separator= ' ', lines_names=lines_names, confirm_all_overwrite=False)
                    elif "image_size" in data.attrs:  # 视为图像
                        img = np.asarray(data)
                        save_path = os.path.join(folder_now, f"{key}.png")
                        if data.ndim == 2 or data.ndim == 3:
                            img = Image.fromarray(img.astype(np.uint8))  # 转换为 PIL 图像
                            img.save(save_path)
                        else:
                            print(f"图像的维度不支持：{img.shape}")
                except Exception as e:
                    print(e)

    with h5py.File(h5_filepath, 'r') as f:
        # f = f["LumeneraCamera"]
        traversal_all_level(f, des_folder)

if __name__ == "__main__":
    h5_filepath = r"D:\ExpData\Fellows\WYQ\20250904_WYQ_Cube\20250904_Viologen.h5"
    des_folder = r"D:\ExpData\Fellows\WYQ\20250904_WYQ_Cube\20250904_Viologen"
    h5_to_txt(h5_filepath, des_folder)