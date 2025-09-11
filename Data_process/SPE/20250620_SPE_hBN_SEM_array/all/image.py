import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image  # 用于保存图像

datapath1 = r"D:\ExpData\SPE\20250620_SPE_hBN_SEM_array\m2_20250618_2sample+20250620_3sample.h5"
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
        else:
            print(f"图像 {i} 的维度不支持：{img.shape}")

        if save_fig == 1:
            save_name = os.path.dirname(datapath1)
            save_name = os.path.join(save_name, fr'image\{key}.png')
            img.save(save_name)

        # 可选：使用 matplotlib 显示图像
        # fig0 = plt.figure(figsize=(8, 6))
        # ax0 = fig0.add_subplot(111)
        # ax0.imshow(img, cmap='gray' if data[key].ndim == 2 else None)

        # if save_fig == 1:
        #     # 隐藏 x 轴和 y 轴的刻度
        #     ax0.set_xticks([])
        #     ax0.set_yticks([])
        #
        #     # 隐藏 x 轴和 y 轴的刻度标签
        #     ax0.set_xticklabels([])
        #     ax0.set_yticklabels([])
        #
        #     # 隐藏 x 轴和 y 轴的标签
        #     ax0.set_xlabel('')
        #     ax0.set_ylabel('')
        #
        #     fig0.savefig(os.path.join(os.path.dirname(datapath1), fr'Images\{key}.png'))