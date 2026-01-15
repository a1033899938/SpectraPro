import numpy as np
import h5py
import cv2
import matplotlib.pyplot as plt


def spiral_position(n):
    """根据编号n返回像素在螺旋路径中的相对中心位置"""
    if n <= 0:
        return (0, 0)

    layer = int(np.ceil((np.sqrt(n) - 1) / 2))
    if layer == 0:
        return (0, 0)

    side_length = 2 * layer
    start_num = (2 * layer - 1) ** 2 + 1
    pos_in_layer = n - start_num
    side = pos_in_layer // side_length
    offset = pos_in_layer % side_length

    if side == 0:  # 右边
        x = layer
        y = -layer + 1 + offset
    elif side == 1:  # 上边
        x = layer - 1 - offset
        y = layer
    elif side == 2:  # 左边
        x = -layer
        y = layer - 1 - offset
    else:  # 下边
        x = -layer + 1 + offset
        y = -layer

    return (x, y)


# ===================== 新增：对比度增强函数 =====================
def enhance_contrast(img, method="clahe", gamma=1.5, clip_limit=2.0, grid_size=(8, 8)):
    """
    图像对比度增强
    :param img: 输入图像（numpy数组，灰度/RGB）
    :param method: 增强方法：
                   - "stretch": 线性拉伸（动态范围0~255）
                   - "hist_eq": 全局直方图均衡化
                   - "clahe": 局部自适应直方图均衡化（推荐）
                   - "gamma": 伽马校正
    :param gamma: 伽马值（gamma<1提亮，gamma>1变暗但增强对比度）
    :param clip_limit: CLAHE的对比度限制（越大增强越明显）
    :param grid_size: CLAHE的网格大小
    :return: 增强后的图像
    """
    # 确保图像是uint8类型
    if img.dtype != np.uint8:
        img = img.astype(np.uint8)

    # 灰度图增强
    if len(img.shape) == 2:
        if method == "stretch":
            # 线性拉伸至0~255
            min_val = np.min(img)
            max_val = np.max(img)
            if max_val - min_val == 0:
                return img
            enhanced = ((img - min_val) / (max_val - min_val) * 255).astype(np.uint8)

        elif method == "hist_eq":
            # 全局直方图均衡化
            enhanced = cv2.equalizeHist(img)

        elif method == "clahe":
            # 局部自适应直方图均衡化（推荐）
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
            enhanced = clahe.apply(img)

        elif method == "gamma":
            # 伽马校正
            img_norm = img / 255.0
            enhanced = (np.power(img_norm, gamma) * 255).astype(np.uint8)

    # RGB图增强（转HSV后增强V通道）
    else:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        if method == "stretch":
            min_val = np.min(v)
            max_val = np.max(v)
            if max_val - min_val != 0:
                v = ((v - min_val) / (max_val - min_val) * 255).astype(np.uint8)

        elif method == "hist_eq":
            v = cv2.equalizeHist(v)

        elif method == "clahe":
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
            v = clahe.apply(v)

        elif method == "gamma":
            v_norm = v / 255.0
            v = (np.power(v_norm, gamma) * 255).astype(np.uint8)

        enhanced_hsv = cv2.merge((h, s, v))
        enhanced = cv2.cvtColor(enhanced_hsv, cv2.COLOR_HSV2BGR)

    return enhanced


# ===================== 配置参数 =====================
filepath = r"D:\ExpData\NP_scattering_Dispersion\ZZS_AuNC_65nm_20251206\ZZS_AuNC_65nm_20251206.h5"
do_image = "subimage-origin"
max_tile = 25  # 仅处理前25个Tile
tile_size = None  # 自动获取Tile尺寸
tile_gap = 0  # Tile间隙
bg_color = 0  # 背景色

# ===================== 步骤1：读取Tile图像 =====================
tile_images = []
tile_positions = []

with h5py.File(filepath, "r") as f:
    root_folder = f["OceanOpticsSpectrometer/20251207/sample2"]
    tiled_image_keys = list(root_folder.keys())
    tiled_image_keys = sorted(tiled_image_keys, key=lambda x: int(x.split("_")[-1]))

    for iTile, tiled_image_key in enumerate(tiled_image_keys):
        if iTile > max_tile:
            break

        # 读取图像并转换为uint8
        image_data = root_folder[tiled_image_key][f"tiled_image/{do_image}"][:]
        if image_data.dtype != np.uint8:
            # 若图像是float类型，先归一化到0~255
            image_data = (image_data - np.min(image_data)) / (np.max(image_data) - np.min(image_data)) * 255
            image_data = image_data.astype(np.uint8)

        tile_images.append(image_data)

        if tile_size is None:
            tile_size = image_data.shape[:2]

        x_rel, y_rel = spiral_position(iTile)
        tile_positions.append((x_rel, y_rel))

tile_height, tile_width = tile_size

# 计算画布坐标
x_rels = [p[0] for p in tile_positions]
y_rels = [p[1] for p in tile_positions]
x_rel_min, x_rel_max = min(x_rels), max(x_rels)
y_rel_min, y_rel_max = min(y_rels), max(y_rels)

tile_abs_positions = []
for x_rel, y_rel in tile_positions:
    x_abs = (x_rel - x_rel_min) * (tile_width + tile_gap)
    y_abs = (y_rel - y_rel_min) * (tile_height + tile_gap)
    tile_abs_positions.append((int(x_abs), int(y_abs)))

# 计算画布尺寸
canvas_height = (y_rel_max - y_rel_min + 1) * (tile_height + tile_gap) - tile_gap
canvas_width = (x_rel_max - x_rel_min + 1) * (tile_width + tile_gap) - tile_gap

# 创建画布并拼接Tile
canvas = np.full((canvas_height, canvas_width, 3), bg_color, dtype=np.uint8)
for img, (x_abs, y_abs) in zip(tile_images, tile_abs_positions):
    if img.shape[:2] != (tile_height, tile_width):
        img = cv2.resize(img, (tile_width, tile_height))

    y_end = y_abs + tile_height
    x_end = x_abs + tile_width

    if y_end > canvas_height:
        y_end = canvas_height
        img = img[:canvas_height - y_abs, :, :]
    if x_end > canvas_width:
        x_end = canvas_width
        img = img[:, :canvas_width - x_abs, :]

    canvas[y_abs:y_end, x_abs:x_end, :] = img

fig = plt.figure(figsize=(24, 24), dpi=300)
ax = fig.add_subplot(1, 1, 1)

canvas = cv2.cvtColor(canvas, cv2.COLOR_RGB2GRAY)
print(np.min(canvas), np.max(canvas))
# enhanced_canvas = cv2.cvtColor(enhanced_canvas, cv2.COLOR_GRAY2RGB)
# cmap = "viridis"

ax.imshow(canvas, cmap="coolwarm")

# ax.set_title("Original Image (Low Contrast)", fontsize=14)
ax.axis("off")

save_original = fr"D:\ExpData\NP_scattering_Dispersion\ZZS_AuNC_65nm_20251206\spiral_original_{do_image}.png"

fig.savefig(save_original)
print(f"原始图像保存至：{save_original}")
plt.tight_layout()
# plt.show()