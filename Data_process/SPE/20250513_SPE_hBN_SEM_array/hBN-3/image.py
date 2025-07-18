import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image  # 用于保存图像
from skimage import exposure

datapath1 = r"D:\ExpData\Fellows\WYQ\20250630_WYQ_SHIN\R-Hu_S-Hu.h5"
save_fig = 1

with h5py.File(datapath1, "r") as f:
    data = f['LumeneraCamera']
    for i, key in enumerate(data.keys()):
        img = data[key]
        img = np.asarray(img)
        if data[key].ndim == 2:
            img = Image.fromarray(img.astype(np.uint8))  # 转换为 PIL 图像
        elif data[key].ndim == 3:
            img = Image.fromarray(img.astype(np.uint8))  # 转换为 PIL 图像
            img = np.array(img)
            img_enhanced  = np.zeros_like(img,dtype=np.float32)
            for channel in range(3):
                if channel == 3:
                    img_enhanced[:,:,channel] = exposure.equalize_hist(img[:,:,channel])
                else:
                    img_enhanced[:, :, channel] = img[:,:,channel]
        else:
            print(f"图像 {i} 的维度不支持：{img.shape}")

        # if save_fig == 1:
        #     save_name = os.path.dirname(datapath1)
        #     save_name = os.path.join(save_name, fr'image\{key}.png')
        #     img.save(save_name)

        # 可选：使用 matplotlib 显示图像
        fig0 = plt.figure(figsize=(8, 6))
        ax0 = fig0.add_subplot(111)
        # 直方图均衡化
        ax0.imshow(img_enhanced, cmap='gray' if data[key].ndim == 2 else None)
        row, column, channel = img.shape
        print(np.shape(img))
        # ax0.axvline(x=537.8, color='blue', linestyle='--', linewidth=1.5, alpha=0.7)  # 蓝色虚线
        # ax0.axhline(x=6, color='green', linestyle='-.', linewidth=3, alpha=0.5)  # 绿色点划线
        plt.show()