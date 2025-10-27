import os.path

if __name__ == '__main__':
    import h5py
    import matplotlib.pyplot as plt
    import numpy as np
    from PIL import Image  # 用于保存图像
    import matplotlib.pyplot as plt
    import numpy as np

    """before_SEM"""
    datapath1 = r"E:\LabInstrumentTest\Infinity1vsXintu - 副本\v2.h5"

    """fig0"""
    with h5py.File(datapath1, "r") as f:
        data = f['LumeneraCamera']
        for i, key in enumerate(data.keys()):
            # if '20250625' not in key:
            #     continue

            print(f"current key: {key}")
            img = data[key]
            img = np.asarray(img)
            img_file = os.path.join(os.path.dirname(datapath1), fr'{key}.png')
            if data[key].ndim == 2:
                img = Image.fromarray(img.astype(np.uint8))  # 转换为 PIL 图像
                img.save(img_file)
            elif data[key].ndim == 3:
                img = Image.fromarray(img.astype(np.uint8))  # 转换为 PIL 图像
                img.save(img_file)
            else:
                print(f"图像 {i} 的维度不支持：{img.shape}")

            # 可选：使用 matplotlib 显示图像
            plt.imshow(img, cmap='gray' if data[key].ndim == 2 else None)
            plt.title(f'')
            # plt.show()