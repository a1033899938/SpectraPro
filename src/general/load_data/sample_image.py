if __name__ == '__main__':
    import h5py
    import matplotlib.pyplot as plt
    import numpy as np
    from PIL import Image  # 用于保存图像
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    """before_SEM"""
    datapath1 = r"D:\ExpData\Fellows\WYQ\20250714_WYQ_SHIN\20250714_WYQ_SHIN.h5"

    """fig0"""
    with h5py.File(datapath1, "r") as f:
        data = f['LumeneraCamera']
        for i, key in enumerate(data.keys()):
            # if key == 'mapping_range_m4_0':
            img = data[key]
            img = np.asarray(img)
            if data[key].ndim == 2:
                img = Image.fromarray(img.astype(np.uint8))  # 转换为 PIL 图像
                img.save(os.path.join(os.path.dirname(datapath1), f'{key}.png'))
            elif data[key].ndim == 3:
                img = Image.fromarray(img.astype(np.uint8))  # 转换为 PIL 图像
                img.save(os.path.join(os.path.dirname(datapath1), f'{key}.png'))
            else:
                print(f"图像 {i} 的维度不支持：{img.shape}")

            # 可选：使用 matplotlib 显示图像
            plt.imshow(img, cmap='gray' if data[key].ndim == 2 else None)
            plt.title(f'Image {i}')
            plt.show()

    # """after_SEM"""
    # datapath1 = r"D:\ExpData\SPE\20250305_SPE_hBN_SEM_array\20250305_SPE_hBN_SEM_array-measurement-1.h5"

    # """fig1"""
    # with h5py.File(datapath1, "r") as f:
    #     data = f['LumeneraCamera']
    #     for i, key in enumerate(data.keys()):
    #         img = data[key]
    #         img = np.asarray(img)
    #         if data[key].ndim == 2:
    #             img = Image.fromarray(img.astype(np.uint8))  # 转换为 PIL 图像
    #             img.save(fr'D:\ExpData\SPE\20250305_SPE_hBN_SEM_array\Sample_Image\{key}.png')
    #         elif data[key].ndim == 3:
    #             img = Image.fromarray(img.astype(np.uint8))  # 转换为 PIL 图像
    #             img.save(fr'D:\ExpData\SPE\20250305_SPE_hBN_SEM_array\Sample_Image\{key}.png')
    #         else:
    #             print(f"图像 {i} 的维度不支持：{img.shape}")
    #
    #         # 可选：使用 matplotlib 显示图像
    #         plt.imshow(img, cmap='gray' if data[key].ndim == 2 else None)
    #         plt.title(f'Image {i}')
    #         plt.show()