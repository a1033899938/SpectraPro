import os.path
import h5py
import matplotlib.pyplot as plt
import numpy as np

datapath1 = r"D:\ExpData\SPE\20250513_SPE_hBN_SEM_array\measurement-1.h5"

"""fig0"""
with h5py.File(datapath1, "r") as f:
    mapping_name = 'hBN_1-2_beforeSEM_mapping_0'
    data = f['OceanOpticsSpectrometer'][mapping_name]
    row_keys = data.keys()
    row1_key = list(data.keys())[0]
    row1 = data[row1_key]
    column_keys_of_row1 = row1.keys()


    bgd = np.array(data[f'x-0/{mapping_name[:-2]}-x0-y0'].attrs['background'])
    bgd_time = data[f'x-0/{mapping_name[:-2]}-x0-y0'].attrs['background_int'] / 1000
    wav = np.array(data[f'x-0/{mapping_name[:-2]}-x0-y0'].attrs['wavelengths'])
    bgd = bgd / bgd_time
    mapping_range = [len(row_keys), len(column_keys_of_row1)]
    mapping = np.zeros([mapping_range[0], mapping_range[1]])

    # 拟合参数
    p0 = [100, 537, 6,
          20, 550, 10,
          20, 577, 6]

    bounds = ([0, 535, 0,
               0, 540, 0,
               0, 570, 0],
              [1000, 540, 10,
               1000, 565, 12,
               1000, 580, 10])
    min_differences_for_fit = np.abs(wav - 505)
    min_index_for_fit = np.argmin(min_differences_for_fit)
    max_differences_for_fit = np.abs(wav - 600)
    max_index_for_fit = np.argmin(max_differences_for_fit)

    for i in range(mapping_range[0]):
        parent_key = f"x-{i}"
        for j in range(mapping_range[1]):
            print(f"i now: {i}, j now: {j}")
            child_key = f"{mapping_name[:-2]}-x{i}-y{j}"
            sp = data[f"{parent_key}/{child_key}"]
            sp_time = sp.attrs['integration_time'] / 1000
            sp = np.array(sp)
            sp = sp / sp_time
            sp = sp - bgd
            # print(sp)

            # """三峰拟合"""
            # try:
            #     x_for_fit = wav[min_index_for_fit:max_index_for_fit]
            #     y_for_fit = sp[min_index_for_fit:max_index_for_fit]
            #     popt, pcov = curve_fit(triple_gaussian, x_for_fit, y_for_fit, p0=p0, bounds=bounds)
            #     A1, x1, gamma1, A2, x2, gamma2, A3, x3, gamma3 = popt
            #     # mag_now = (A1/np.pi)/(gamma1/2)
            #     mag_now = A1
            #     mapping_5[i][j] = mag_now

                # fig2 = plt.figure(figsize=(8, 6))
                # y_fit = lorentzian_plus_gaussian(wav, *popt)
                # ax2 = fig2.add_subplot(111)
                # ax2.plot(wav, sp, 'b')
                # ax2.plot(wav, y_fit, '--r')
                # plt.show()
            # except Exception as e:
            #     print(e)

            # mapping_5[i][j] = np.mean(sp[min_index_for_fit:max_index_for_fit])
            mapping[i][j] = sp[min_index_for_fit]

np.save(os.path.join(os.path.dirname(datapath1), fr'm2\mapping_505.npy'), mapping)

# save_fig = 0
# mapping_5 =np.load(os.path.join(os.path.dirname(datapath1), fr'm2\mapping_500to600.npy'))
# mapping_range = [mapping_5.shape[0], mapping_5.shape[1]]
#
# fig0 = plt.figure(figsize=(8, 6))
# ax0 = fig0.add_subplot(111)
# x = range(mapping_range[0])
# y = range(mapping_range[1])
# X, Y = np.meshgrid(x, y)
# print(f"shape x: {np.shape(X)}")
# print(f"shape y: {np.shape(Y)}")
# Z = mapping_5
# im=ax0.pcolor(X, Y, np.transpose(Z), cmap='viridis')
#
# # 添加颜色条
# cbar = plt.colorbar(im)
# cbar.set_label('Intensity')
#
# # 设置标题和轴标签
# plt.title('PL mapping_5-hBN_afterSEM')
# plt.xlabel('X Position')
# plt.ylabel('Y Position')

# with h5py.File(datapath1, "r") as f:
#     data = f['LumeneraCamera']
#     for i, key in enumerate(data.keys()):
#         img = data[key]
#         img = np.asarray(img)
#         if data[key].ndim == 2:
#             img = Images.fromarray(img.astype(np.uint8))  # 转换为 PIL 图像
#         elif data[key].ndim == 3:
#             img = Images.fromarray(img.astype(np.uint8))  # 转换为 PIL 图像
#         else:
#             print(f"图像 {i} 的维度不支持：{img.shape}")
#
#         save_name = os.path.dirname(datapath1)
#         save_name = os.path.join(save_name, fr'm2\{key}.png')
#         img.save(save_name)
#         # 可选：使用 matplotlib 显示图像
#         fig1 = plt.figure(figsize=(8, 6))
#         ax1 = fig1.add_subplot(111)
#         ax1.imshow(img, cmap='gray' if data[key].ndim == 2 else None)

# if save_fig == 1:
#     # 隐藏 x 轴和 y 轴的刻度
#     ax0.set_xticks([])
#     ax0.set_yticks([])
#     # ax1.set_xticks([])
#     # ax1.set_yticks([])
#
#     # 隐藏 x 轴和 y 轴的刻度标签
#     ax0.set_xticklabels([])
#     ax0.set_yticklabels([])
#     # ax1.set_xticklabels([])
#     # ax1.set_yticklabels([])
#
#     # 隐藏 x 轴和 y 轴的标签
#     ax0.set_xlabel('')
#     ax0.set_ylabel('')
#     # ax1.set_xlabel('')
#     # ax1.set_ylabel('')
#
#     # fig0.savefig(os.path.join(os.path.dirname(datapath1), f'PL_mapping_hBN_afterSEM_m5_peak1fit_viridis.png'))
#     # fig1.savefig(os.path.join(os.path.dirname(datapath1), f'OM_image_WS2_ML.png'))
plt.show()