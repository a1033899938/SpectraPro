"""
Author: Junjie-Xie
Updated: 2025/12/9
Functions: 
"""
import numpy as np
import matplotlib.pyplot as plt
import h5py
import time
import cv2
import os
from figure_setting import *
from pathlib import Path

def sigma_moment(proj, x):
    total = np.sum(proj)
    if total == 0:
        return 0
    mean = np.sum(x * proj) / total
    sigma = np.sqrt(np.sum((x - mean) ** 2 * proj) / total)
    return sigma

filepath = r"D:\ExpData\LabInstrumentTest\TestLaserAutoFocus\TestLaserAutoFocus_20260109-2.h5"
folder_names_1 = [f"on_sub-{i}" for i in np.arange(1,6,1)]
folder_names_2 = [f"on_np-{i}" for i in np.arange(1,6,1)]
folder_names = folder_names_1 + folder_names_2

sigmas = []
ratios = []
times = [0, 0]
count = 0
with h5py.File(filepath, "a") as f:
    # del f["/OceanOpticsSpectrometer/M1/on_sub-2/Tile_-1"]

    for iM in range(2):
        for iFolder, folder_name in enumerate(folder_names):
            count += 1
            folder = f[f"OceanOpticsSpectrometer/M{iM+1}/{folder_name}"]
            keys = folder.keys()
            len_keys = len(keys)
            offsets = np.arange(-len_keys//2, len_keys//2, 1)

            this_sigmas = []
            this_ratios = []
            sharps = []

            save_folder_path = os.path.join(os.path.dirname(filepath), "Images3", folder_name)
            # exist_ok=True 避免重复创建报错
            os.makedirs(save_folder_path, exist_ok=True)

            for iOffset, offset in enumerate(offsets):
                # if iOffset != 200:
                #     continue
                print(iFolder, iOffset)
                thumb_image = folder[f"thumb_image_{iOffset}"]
                thumb_image = np.array(thumb_image)
                thumb_image_blue = thumb_image[:, :, 2]

                """Projection"""
                start = time.time()
                proj_h = np.sum(thumb_image_blue, axis=0)
                proj_v = np.sum(thumb_image_blue, axis=1)

                x_h = np.arange(len(proj_h))
                x_v = np.arange(len(proj_v))

                sigma_h = sigma_moment(proj_h, x_h)
                sigma_v = sigma_moment(proj_v, x_v)

                sigma = (sigma_h + sigma_v) / 2
                this_sigmas.append(sigma)
                proj_time = time.time() - start
                times[0] += proj_time

                """FFT"""
                start = time.time()
                ff = np.fft.fft2(thumb_image_blue)
                ff_shift = np.fft.ifftshift(ff)

                # 计算高频分量占比
                rows, cols = thumb_image_blue.shape
                crow, ccol = rows // 2, cols // 2
                mask = np.ones((rows, cols), np.uint8)
                cv2.circle(mask, (ccol, crow), (min(rows, cols) // 8), 0, -1)
                high_freq_energy = np.sum(np.abs(ff_shift) * mask)
                total_energy = np.sum(np.abs(ff_shift))
                high_freq_ratio = high_freq_energy / total_energy if total_energy > 0 else 0
                this_ratios.append(high_freq_ratio)
                fft_time = time.time() - start
                times[1] += fft_time

                # fig = plt.figure(figsize=(8, 8), dpi=100)
                # ax = fig.add_subplot(111)
                # thumb_image_blue_show = np.zeros_like(thumb_image)
                # thumb_image_blue_show[:,:,2] = thumb_image_blue
                # ax.imshow(thumb_image_blue_show)
                # save_path = os.path.join(save_folder_path,f"G{iFolder}_O{iOffset}.png")
                # ax.set_aspect("equal")
                # fig.savefig(save_path)
                # plt.close(fig)

                # blurred_img = cv2.GaussianBlur(thumb_image_blue, (3, 3), 0)  # 高斯核大小(3,3)，标准差0
                # laplacian = cv2.Laplacian(blurred_img, cv2.CV_64F)
                # laplacian_abs = np.absolute(laplacian)
                # sharp = laplacian_abs.var()
                # sigmas.append(sharp)
            sigmas.append(this_sigmas)
            ratios.append(this_ratios)


fig = plt.figure(figsize=(12, 8*4), dpi=100)
ax1 = fig.add_subplot(411)
ax2 = fig.add_subplot(412)
ax3 = fig.add_subplot(413)
ax4 = fig.add_subplot(414)
section_colors = ["#0E8585", "#830783", "#FFA500"]
x = offsets
for i, sigma in enumerate(sigmas):
    if i%10 < 5:
        ax = ax1
    else:
        ax = ax2

    ax.plot(x, sigma, "o", linewidth=1, color=section_colors[0 if i<10 else 1])

for i, ratio in enumerate(ratios):
    if i%10 < 5:
        ax = ax3
    else:
        ax = ax4

    ax.plot(x, ratio, "o", linewidth=1, color=section_colors[0 if i<10 else 1])

print(f"总耗时: {times[0]:.2f} s, {times[1]:.2f} s")
print(f"平均耗时: {times[0]/count:.2f} s/pic, {times[1]/count:.2f}  s/pic")
plt.show()