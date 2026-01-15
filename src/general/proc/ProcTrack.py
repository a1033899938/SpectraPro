import cv2
import h5py
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from functools import wraps
from scipy import signal

from src.general.numerical.curve_functions import *
from src.general.numerical.edit_data import *
from datetime import datetime

def sigma_moment(y, x):
    y = np.nan_to_num(y, nan=0.0, posinf=0.0, neginf=0.0)
    x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)

    total = np.sum(y)
    if total == 0:
        return 0
    mu  = np.sum(x * y) / total
    sigma = np.sqrt(np.sum((x - mu ) ** 2 * y) / total)

    # width_997 = 6*sigma
    width_1e2 = 4*sigma
    return mu, width_1e2

def exception_handler(default_return=None, log_error=True):
    """
    方法异常处理装饰器
    :param default_return: 异常时的默认返回值
    :param log_error: 是否打印错误日志
    """
    def decorator(func):
        @wraps(func)  # 保留原方法的元信息（如名称、文档字符串）
        def wrapper(self, *args, **kwargs):
            try:
                # 执行原方法
                return func(self, *args, **kwargs)
            except FileNotFoundError as e:
                if log_error:
                    print(f"【文件错误】方法 {func.__name__} 执行失败：文件不存在 - {str(e)}")
                return default_return
            except KeyError as e:
                if log_error:
                    print(f"【键错误】方法 {func.__name__} 执行失败：键不存在 - {str(e)}")
                return default_return
            except ValueError as e:
                if log_error:
                    print(f"【值错误】方法 {func.__name__} 执行失败：{str(e)}")
                return default_return
            except Exception as e:
                if log_error:
                    print(f"【未知错误】方法 {func.__name__} 执行失败：{type(e).__name__} - {str(e)}")
                return default_return
        return wrapper
    return decorator

"""处理"""
class ProcTrack:
    def __init__(self, filepath, root_folder_str):
        self.filepath = filepath
        self.root_folder_str = root_folder_str
        self.fig = None
        self.axes = None

    """获取key"""
    @exception_handler(default_return=([], []))  # 异常时返回空列表
    def get_tile_keys(self, mask=None):
        with h5py.File(self.filepath, "r") as f:
            root_folder = f[self.root_folder_str]
            tile_keys = list(root_folder.keys())
            tile_keys = sorted(tile_keys, key=lambda k: int(k.split("_")[-1]))

            # 排除mask中的键值
            if mask is not None:
                keys = []
                for key in tile_keys:
                    if key not in mask:
                        keys.append(key)
                tile_keys = keys

            # 排序
            tile_keys = self.sort_keys_by_end(tile_keys)

            # 获取fullpath
            keys = []
            for key in tile_keys:
                key = f"{self.root_folder_str}//{key}"
                keys.append(key)
            full_tile_keys = keys

        return tile_keys, full_tile_keys

    @exception_handler(default_return=([], []))  # 异常时返回空列表
    def get_particle_keys(self, full_tile_key, mask=["tiled_image"]):
        with h5py.File(self.filepath, "r") as f:
            tile = f[full_tile_key]
            particle_keys = list(tile.keys())

            # 排除mask中的键值
            if mask is not None:
                keys = []
                for key in particle_keys:
                    if key not in mask:
                        keys.append(key)
                particle_keys = keys

            # 排序
            particle_keys = self.sort_keys_by_end(particle_keys)

            # 获取fullpath
            keys = []
            for key in particle_keys:
                key = f"{full_tile_key}//{key}"
                keys.append(key)
            full_particle_keys = keys

        return particle_keys, full_particle_keys

    @exception_handler(default_return=([], []))  # 异常时返回空列表
    def get_spectra_key(self, full_particle_key, spectra_type):
        with h5py.File(self.filepath, "r") as f:
            particle = f[f"{full_particle_key}//Spectra"]
            spectra_keys = list(particle.keys())

            for key in spectra_keys:
                if key in spectra_type:
                    full_key = f"{full_particle_key}//Spectra//{key}"
                    return key, full_key

            return None, None

    @exception_handler(default_return=([], []))  # 异常时返回空列表
    def get_image_key(self, full_particle_key, image_type=0):
        with h5py.File(self.filepath, "r") as f:
            particle = f[f"{full_particle_key}//Image"]
            image_keys = list(particle.keys())

            if isinstance(image_type, int):
                if image_type == 0:
                    image_type = "OM thumb image"
                else:
                    image_type = "particle feature"
            elif isinstance(image_type, str):
                pass
            else:
                print("Wrong image type")
                return None, None

            for key in image_keys:
                if key in image_type:
                    full_key = f"{full_particle_key}//Image//{key}"
                    return key, full_key

            return None, None

    "处理"
    @exception_handler(default_return=([], []))  # 异常时返回空列表
    def get_scanning(self, full_spectra_key, wav_range=None, spectra_type="scat", if_despiking=False, bgd=None, ref=None, ref_minus_bgd=None):
        with h5py.File(self.filepath, "r") as f:
            spectra = f[full_spectra_key]
            spectrum_keys = list(spectra.keys())
            spectrum_keys = sorted(spectrum_keys, key=lambda k: int(k.split("_")[-1][1:]))

            signals = None
            times = []

            for iSpectrum, spectrum_key in enumerate(spectrum_keys):
                sp = spectra[spectrum_key]

                wav = np.array(sp.attrs['wavelengths'])
                if bgd is None:
                    # 仅获取第一条光谱的bgd, ref, 节省时间
                    bgd = np.array(sp.attrs['background'])
                    bgd_time = sp.attrs['background_int'] / 1000
                    bgd = bgd / bgd_time

                if spectra_type == "scat":
                    if ref is None and ref_minus_bgd is None:
                        ref = np.array(sp.attrs['reference'])
                        ref_time = sp.attrs['reference_int'] / 1000
                        ref = ref / ref_time

                signal_time = sp.attrs['integration_time'] / 1000
                signal = np.array(sp)
                signal = signal / signal_time

                if if_despiking:
                    noise_wavs = self.find_noise(signal, wav)
                    if noise_wavs is not None:
                        signal = self.despiking(signal, wav, noise_wavs)

                numerator = signal - bgd  # 分子
                if spectra_type == "scat":
                    if ref_minus_bgd is None:
                        denominator = ref - bgd  # 分母
                    else:
                        denominator = ref_minus_bgd

                    denominator[denominator == 0] = 1  # 如果分母为0，设为1
                    numerator[denominator == 0] = 0  # 对应的分子，设为0

                    scat = numerator / denominator

                    signal = scat
                else:
                    signal = numerator

                if wav_range is not None:
                    x1 = wav_range[0]
                    x2 = wav_range[1]
                    wav, signal = choose_range(wav, signal, x1=x1, x2=x2)

                signals = signal if signals is None else np.vstack([signals, signal])

                # time
                time_now = sp.attrs["creation_timestamp"]
                time_now = datetime.fromisoformat(time_now)
                times.append(time_now)

            steps = int(spectra.attrs["steps"])
            total_length = float(spectra.attrs["total length(um)"])
            half_length = total_length / 2
            positions = np.linspace(-half_length, half_length, steps)

        return wav, positions, signals, times

    """处理s"""
    @exception_handler(default_return=([], []))  # 异常时返回空列表
    def proc_reconstruct_time(self, full_spectra_key, idx1, idx2):
        with h5py.File(self.filepath, "r") as f:
            spectra = f[full_spectra_key]
            spectrum_keys = list(spectra.keys())
            spectrum_keys = sorted(spectrum_keys, key=lambda k: int(k.split("_")[-1][1:]))

            spectrum_1 = spectra[spectrum_keys[idx1]]
            spectrum_2 = spectra[spectrum_keys[idx2]]

            time1 = spectrum_1.attrs["creation_timestamp"]
            time2 = spectrum_2.attrs["creation_timestamp"]

            time1 = datetime.fromisoformat(time1)
            time2 = datetime.fromisoformat(time2)

            time_diff = (time2 - time1).total_seconds()

            ratio = (idx2 - idx1 + 1) / (idx2 - idx1)
            reconstructed_time = time_diff * ratio
            return reconstructed_time

    @exception_handler(default_return=([], []))  # 异常时返回空列表
    def get_added_noise_scanning(self, full_spectra_key, noise, wav_range=None, spectra_type="scat"):
        with h5py.File(self.filepath, "r") as f:
            spectra = f[full_spectra_key]
            spectrum_keys = list(spectra.keys())
            spectrum_keys = sorted(spectrum_keys, key=lambda k: int(k.split("_")[-1][1:]))

            signals = None
            times = []

            for iSpectrum, spectrum_key in enumerate(spectrum_keys):
                sp = spectra[spectrum_key]

                wav = np.array(sp.attrs['wavelengths'])
                # 仅获取第一条光谱的bgd, ref, 节省时间
                bgd = np.array(sp.attrs['background'])
                bgd_time = sp.attrs['background_int'] / 1000
                bgd = bgd / bgd_time

                if spectra_type == "scat":
                    ref = np.array(sp.attrs['reference'])
                    ref_time = sp.attrs['reference_int'] / 1000
                    ref = ref / ref_time

                signal_time = sp.attrs['integration_time'] / 1000
                signal = np.array(sp)
                signal = signal / signal_time

                signal = signal + noise

                numerator = signal - bgd  # 分子
                if spectra_type == "scat":
                    denominator = ref - bgd  # 分母

                    denominator[denominator == 0] = 1  # 如果分母为0，设为1
                    numerator[denominator == 0] = 0  # 对应的分子，设为0

                    scat = numerator / denominator

                    signal = scat
                else:
                    signal = numerator

                if wav_range is not None:
                    x1 = wav_range[0]
                    x2 = wav_range[1]
                    wav, signal = choose_range(wav, signal, x1=x1, x2=x2)

                signals = signal if signals is None else np.vstack([signals, signal])

                # time
                time_now = sp.attrs["creation_timestamp"]
                time_now = datetime.fromisoformat(time_now)
                times.append(time_now)

            steps = int(spectra.attrs["steps"])
            total_length = float(spectra.attrs["total length(um)"])
            half_length = total_length / 2
            positions = np.linspace(-half_length, half_length, steps)

        return wav, positions, signals, times

    @exception_handler(default_return=([], []))  # 异常时返回空列表
    def get_spectrum_maximum(self, wav, positions, scats, x1, x2):
        x1_idx = find_val_idx(wav, x1)
        x2_idx = find_val_idx(wav, x2)

        scats_roi = scats[:, x1_idx:x2_idx]

        maximum_idx = np.argmax(scats_roi)  # 扁平索引
        maximum_idx = np.unravel_index(maximum_idx, scats_roi.shape)  # 二维索引

        wav0_idx = maximum_idx[1]
        position0_idx = maximum_idx[0]

        wav0 = wav[wav0_idx]
        position0 = positions[position0_idx]

        return wav0, position0, wav0_idx, position0_idx

    @exception_handler(default_return=([], []))  # 异常时返回空列表
    def proc_reconstruct_error(self, scats, jump_steps, save_path_key=None, wav=None):
        reconstruct_scat = np.max(scats, axis=0)

        reconstruct_error = []
        jump_step_reconstruct_scats = None
        for jump_step in jump_steps:
            # 保证经过中间位置(起始位置)
            center_idx = int(np.ceil(np.shape(scats)[0] / 2))
            start_idx = center_idx % jump_step

            jump_step_scats = scats[start_idx::jump_step]
            jump_step_reconstruct_scat = np.max(jump_step_scats, axis=0)

            # peason_error = calc_pearson(reconstruct_scat, jump_step_reconstruct_scat)
            error = cal_error(reconstruct_scat, jump_step_reconstruct_scat)
            reconstruct_error.append(error)

            jump_step_reconstruct_scats = jump_step_reconstruct_scat if jump_step_reconstruct_scats is None else np.vstack([jump_step_reconstruct_scats, jump_step_reconstruct_scat])

        if save_path_key is not None:
            if wav is not None:
                self.set_attrs(save_path_key, "reconstruct_wav", wav)
            self.set_attrs(save_path_key, "reconstruct_scat", reconstruct_scat)
            self.set_attrs(save_path_key, "reconstruct_error", reconstruct_error)
            self.set_attrs(save_path_key, "reconstruct_jump_steps", jump_steps)

        return reconstruct_error, jump_step_reconstruct_scats

    @exception_handler(default_return=([], []))  # 异常时返回空列表
    def proc_maxz(self, wav, positions, scats):
        maxz_indice = []
        for iWav, wav0 in enumerate(wav):
            ints = scats[:, iWav]
            maxz_idx = np.argmax(ints)
            maxz_indice.append(maxz_idx)

        maxz = positions[maxz_indice]

        return maxz

    @exception_handler(default_return=([], []))  # 异常时返回空列表
    def proc_int_at_wav0(self, wav0, wav, scats):
        wav0_index = find_val_idx(wav, wav0)
        ints_at_wav0 = scats[:, wav0_index]
        return ints_at_wav0

    @exception_handler(default_return=([], []))  # 异常时返回空列表
    def proc_tiled_image(self, full_tile_key, image_type=0):
        with h5py.File(self.filepath, "r") as f:
            tiled_images = f[full_tile_key]["tiled_image"]

            if image_type == 0:
                image_key = "subimage-origin"
            elif image_type == 1:
                image_key = "subimage-markers"
            elif image_type == 2:
                image_key = "image-origin"
            elif image_type == 3:
                image_key = "image-markers"

            img = tiled_images[image_key]
            img = np.asarray(img)
            return img

    @exception_handler(default_return=([], []))  # 异常时返回空列表
    def proc_thumb_image(self, full_image_key, save_path_key=None, cut_from_color_image=False):
        if save_path_key is not None:
            open_mode = "a"
        else:
            open_mode = "r"

        with h5py.File(self.filepath, open_mode) as f:
            img = f[full_image_key]
            img = np.asarray(img)
            if cut_from_color_image:
                h, w = img.shape[:2]
                start_x = max(0, (w - 100) // 2)
                start_y = max(0, (h - 100) // 2)
                img = img[start_y:start_y+100, start_x:start_x+100]

            img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

            proj_h = np.sum(img_gray, axis=0)
            proj_v = np.sum(img_gray, axis=1)

            # 判断粒子是否居中"
            max_h_idx = np.argmax(proj_h)
            max_v_idx = np.argmax(proj_v)

            len_h = max_h_idx - len(proj_h) / 2
            len_v = max_v_idx - len(proj_v) / 2

            len_from_center = np.sqrt(len_h ** 2 + len_v ** 2)

            if len_from_center < 7:
                is_valid = True
            else:
                is_valid = False

            if save_path_key is not None:
                self.set_attrs(save_path_key, "is_valid", is_valid)

            return img, img_gray

    "default"
    @exception_handler(default_return=([], []))  # 异常时返回空列表
    def get_attrs(self, full_path_key, attr_name):
        with h5py.File(self.filepath, "r") as f:
            path = f[full_path_key]
            if attr_name in path.attrs.keys():
                return path.attrs[attr_name]
            else:
                return None

    @exception_handler(default_return=([], []))  # 异常时返回空列表
    def set_attrs(self, full_path_key, attr_name, attr_value, is_cover=False):
        with h5py.File(self.filepath, "a") as f:
            path = f[full_path_key]

            if attr_name in path.attrs.keys():
                if is_cover:
                    print(f"attr: {attr_name} exist, return")
                    return
                else:
                    print(f"attr: {attr_name} exist, cover!!!")

            path.attrs.update({f"JunProc: {attr_name}": attr_value})

    def sort_keys_by_end(self, keys):
        def end_number(key):
            return int(key.split("_")[-1])

        sorted_keys = self._sort_keys(keys, func=end_number)
        return sorted_keys

    def _sort_keys(self, keys, func):
        sorted_keys = sorted(keys, key=lambda k: func(k))
        return sorted_keys

    def find_noise(self, sp, wav):
        window_size = 11
        baseline = signal.medfilt(sp, kernel_size=window_size)
        residual = sp - baseline
        residual[residual < 30] = 0
        indice = np.where(residual != 0)[0]
        if indice.size > 0:
            noise_wavs = wav[indice]

            return noise_wavs
        else:
            return None

    def despiking(self, sp, wav, noise_wavs, half_window=15//2):
        noise_idx = [find_val_idx(wav, wav0) for wav0 in noise_wavs]
        mask = np.ones_like(wav)
        mask[noise_idx] = 0

        correct_sp = np.array(sp)
        for noise_wav in noise_wavs:
            wav_idx = find_val_idx(wav, noise_wav)

            wav_start_idx = max(0, wav_idx - half_window)
            wav_end_idx = min(len(wav)-1, wav_idx + half_window)

            wav_section = wav[wav_start_idx: wav_end_idx]
            mask_section = mask[wav_start_idx: wav_end_idx]
            sp_section = sp[wav_start_idx: wav_end_idx]

            sp_section_without_noise = sp_section * mask_section
            this_correct_sp = np.median(sp_section_without_noise)

            correct_sp[wav_idx] = this_correct_sp
        return correct_sp