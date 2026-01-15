"""
Author: Junjie-Xie
Updated: 2025/12/9
Functions: 
"""
import numpy as np
import matplotlib.pyplot as plt
import h5py
import cv2
import os
from figure_setting import *


def sigma_moment(proj, x):
    total = np.sum(proj)
    if total == 0:
        return 0
    mean = np.sum(x * proj) / total
    sigma = np.sqrt(np.sum((x - mean) ** 2 * proj) / total)
    return sigma

filepath = r"D:\ExpData\LabInstrumentTest\TestLaserAutoFocus\TestLaserAutoFocus.h5"

with h5py.File(filepath, "r") as f:
    folder = f["OceanOpticsSpectrometer/20251209"]
    offsets = np.arange(-50, 50, 1)

    sigmas = []
    sharps = []
    for iOffset, offset in enumerate(offsets):
        thumb_image = folder[f"thumb_image_{iOffset}"]
        color_image = folder[f"color_image_{iOffset}"]

        "激光"
        thumb_image = np.array(thumb_image)
        thumb_image_blue = thumb_image[:, :, 2]

        proj_h = np.sum(thumb_image_blue, axis=0)
        proj_v = np.sum(thumb_image_blue, axis=1)

        x_h = np.arange(len(proj_h))
        x_v = np.arange(len(proj_v))

        sigma_h = sigma_moment(proj_h, x_h)
        sigma_v = sigma_moment(proj_v, x_v)

        sigma = (sigma_h + sigma_v) / 2
        sigmas.append(sigma)

        fig = plt.figure(figsize=(8, 8), dpi=100)
        ax = fig.add_subplot(111)
        thumb_image_blue_show = np.zeros_like(thumb_image)
        thumb_image_blue_show[:,:,2] = thumb_image_blue
        ax.imshow(thumb_image_blue_show)
        save_path = os.path.join(os.path.dirname(filepath),
                                 fr"Image/thumb_image_{iOffset}.png")
        ax.set_aspect("equal")
        fig.savefig(save_path)
        plt.close(fig)
        # blurred_img = cv2.GaussianBlur(thumb_image_blue, (3, 3), 0)  # 高斯核大小(3,3)，标准差0
        # laplacian = cv2.Laplacian(blurred_img, cv2.CV_64F)
        # laplacian_abs = np.absolute(laplacian)
        # sharp = laplacian_abs.var()
        # sigmas.append(sharp)

        "图像"
        # color_image = np.array(color_image)
        # blurred_img = cv2.GaussianBlur(color_image, (3, 3), 0)  # 高斯核大小(3,3)，标准差0
        # laplacian = cv2.Laplacian(blurred_img, cv2.CV_64F)
        # laplacian_abs = np.absolute(laplacian)
        # sharp = laplacian_abs.var()
        # sharps.append(sharp)
        #
        # fig = plt.figure(figsize=(12, 8), dpi=100)
        # ax = fig.add_subplot(111)
        # ax.imshow(color_image)
        # save_path = os.path.join(os.path.dirname(filepath),
        #                          fr"Image/color_image_{iOffset}.png")
        # fig.savefig(save_path)

fig = plt.figure(figsize=(12, 8*2), dpi=100)
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

# x = range(len(offsets))
x = offsets
color1 = "blue"
color2 = "orange"
ax1.plot(x, sigmas, linewidth=3, color=color1)
ax2.plot(x, sharps, linewidth=3, color=color2)

text_x = 0.4
text_y = 0.95
text_content = f"best z: {offsets[np.argmin(sigmas)]} um"
ax1.text(
    x=text_x,
    y=text_y,
    s=text_content,
    fontsize=20,  # 字体大小（关键）
    ha='left',  # 水平右对齐（避免文本超出图像）
    va='top',  # 垂直上对齐
    color=color1,  # 文本颜色
    weight='bold',  # 加粗（可选）
    transform=ax1.transAxes
)

text_x = 0.05
text_y = 0.95
text_content = f"best z: {offsets[np.argmax(sharps)]} um"
ax2.text(
    x=text_x,
    y=text_y,
    s=text_content,
    fontsize=20,  # 字体大小（关键）
    ha='left',  # 水平右对齐（避免文本超出图像）
    va='top',  # 垂直上对齐
    color=color2,  # 文本颜色
    weight='bold',  # 加粗（可选）
    transform=ax2.transAxes
)
my_auto_focus(ax1, title="Thumb Image Fit Sharpness", ylabel="Sharpness")
my_auto_focus(ax2, title="Color Image Sharpness", ylabel="Sharpness")
# save_path = os.path.join(os.path.dirname(filepath),
#                                  fr"Image/AutoFocusScore.png")
# fig.savefig(save_path)
plt.show()