# import tifffile as tf
# from PIL import Images
import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt

filepath = r"D:\ExpData\ps_sphere.jpg"

# img = tf.imread(filepath)
# img = Images.open(filepath)
img = mpimg.imread(filepath)

# 打印图片信息
# print(f"图片格式: {img.format}")
print(f"图片尺寸: {img.shape}")

# 对于RGB图像，显示各通道数据范围
if len(img.shape) == 3 and img.shape[2] == 3:
    print("RGB各通道数据范围:")
    print(f"R通道: {img[:,:,0].min()}-{img[:,:,0].max()}")
    print(f"G通道: {img[:,:,1].min()}-{img[:,:,1].max()}")
    print(f"B通道: {img[:,:,2].min()}-{img[:,:,2].max()}")

    # 分离RGB通道
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]

    # 使用ITU-R 601-2标准的加权平均公式：Gray = 0.299*R + 0.587*G + 0.114*B
    img = 0.299 * r + 0.587 * g + 0.114 * b

fig1 = plt.figure(figsize=(8*3, 6))
ax11 = fig1.add_subplot(131)
ax12 = fig1.add_subplot(132)
ax13 = fig1.add_subplot(133)

im1 = ax11.imshow(img, cmap='gray')
ax11.set_title('Origin')

fft_result = np.fft.fft2(img)
fft_shifted = np.fft.fftshift(fft_result)
magnitude_spectrum = 20 * np.log(np.abs(fft_shifted) + 1)
phase_spectrum = np.angle(fft_shifted)

im2 = ax12.imshow(magnitude_spectrum, cmap='gray')
ax12.set_title('fft-magnitude')

im3 = ax13.imshow(phase_spectrum, cmap='gray')
ax13.set_title('fft-phase')

"""
掩模
"""

# 创建高通滤波器
filter_type = 'ideal'
cutoff = 20

rows, cols = img.shape
crow, ccol = rows // 2, cols // 2
u, v = np.meshgrid(np.arange(cols), np.arange(rows))
d = np.sqrt((u - ccol) ** 2 + (v - crow) ** 2)

if filter_type == 'ideal':
    # 理想高通滤波器
    mask = np.ones((rows, cols), np.uint8)
    mask[crow - cutoff:crow + cutoff, ccol - cutoff:ccol + cutoff] = 0
elif filter_type == 'butterworth':
    # 巴特沃斯高通滤波器
    n = 2  # 阶数
    mask = 1 / (1 + (cutoff / (d + 1e-10)) ** (2 * n))  # 添加小值避免除零
elif filter_type == 'gaussian':
    # 高斯高通滤波器
    mask = 1 - np.exp(-(d ** 2) / (2 * cutoff ** 2))
elif filter_type == 'hanning':
    hanning_row = np.hanning(img.shape[0])
    hanning_col = np.hanning(img.shape[1])
    mask = np.outer(hanning_row, hanning_col)
else:
    raise ValueError("不支持的滤波器类型")

fig2 = plt.figure(figsize=(8*3, 6))
ax21 = fig2.add_subplot(131)
ax22 = fig2.add_subplot(132)
ax23 = fig2.add_subplot(133)

ax21.imshow(mask, cmap='gray')
ax21.set_title('mask')

fft_shifted_filtered = fft_shifted * mask
magnitude_spectrum = 20 * np.log(np.abs(fft_shifted_filtered) + 1)
phase_spectrum = np.angle(fft_shifted_filtered)

ax22.imshow(magnitude_spectrum, cmap='gray')
ax22.set_title('filtered_magnitude')

ax23.imshow(phase_spectrum, cmap='gray')
ax23.set_title('filtered_phase')

fig3 = plt.figure(figsize=(8, 6))
ax31 = fig3.add_subplot(111)
# ax31 = fig3.add_subplot(131)
# ax32 = fig3.add_subplot(132)
# ax33 = fig3.add_subplot(133)

img = np.fft.ifft2(np.fft.ifftshift(fft_shifted_filtered))
img = np.abs(img)
ax31.imshow(img, cmap='gray')
plt.show()