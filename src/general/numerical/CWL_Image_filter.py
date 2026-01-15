import numpy as np
import cv2
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import as_strided


class ImageFilter:
    def __init__(self, threshold=10, bin_fac=4, min_size=5, max_size=25,
                 bilat_size=3, bilat_height=40, morph_kernel_size=5):
        self.threshold = threshold
        self.bin_fac = bin_fac
        self.min_size = min_size
        self.max_size = max_size
        self.bilat_size = bilat_size
        self.bilat_height = bilat_height
        self.morph_kernel_size = morph_kernel_size
        self.show_particles = False
        self.return_original_with_particles = False
        self.filter_options = ['None', 'STBOC_with_size_filter', 'strided_rescale', 'StrBiThresOpen']
        self.current_filter_index = 0
        self.update_functions = []

    def set_param(self, param_name, value):
        if hasattr(self, param_name):
            old_value = getattr(self, param_name)
            setattr(self, param_name, value)
            for func in self.update_functions:
                func(param_name, old_value, value)

    def get_current_params(self):
        return {
            'threshold': int(self.threshold),
            'bin_fac': int(self.bin_fac),
            'min_size': int(self.min_size),
            'max_size': int(self.max_size),
            'bilat_size': int(self.bilat_size),
            'bilat_height': int(self.bilat_height),
            'morph_kernel_size': int(self.morph_kernel_size)
        }

    def STBOC_with_size_filter(self, g, return_centers=False, return_centers_and_radii=False):
        try:
            # 核心修复1：统一转换输入为numpy数组（解决memoryview问题）
            g = self._convert_to_numpy_array(g)
            # 核心修复2：确保输入是8位单通道灰度图（解决OpenCV类型错误）
            g_gray = self._convert_to_8uc1_gray(g)

            result = STBOC_with_size_filter(
                g_gray,
                bin_fac=self.bin_fac,
                bilat_size=self.bilat_size,
                bilat_height=self.bilat_height,
                threshold=self.threshold,
                min_size=self.min_size,
                max_size=self.max_size,
                morph_kernel_size=self.morph_kernel_size,
                show_particles=self.show_particles,
                return_original_with_particles=self.return_original_with_particles,
                return_centers=return_centers,
                return_centers_and_radii=return_centers_and_radii
            )
            return result
        except Exception as e:
            print(f"[WARN] Image processing has failed due to: {str(e)}")
            # 兜底返回空的8位灰度图（避免None）
            return np.zeros((200, 200), dtype=np.uint8)

    def _convert_to_numpy_array(self, img):
        """将memoryview/其他类型转为numpy数组"""
        if isinstance(img, memoryview):
            img = np.array(img)
        elif not isinstance(img, np.ndarray):
            raise TypeError(f"输入必须是numpy数组/memoryview，当前类型：{type(img)}")
        return img

    def _convert_to_8uc1_gray(self, img):
        """统一转换为8位单通道灰度图（OpenCV轮廓检测要求）"""
        # 1. 处理浮点数组（归一化到0-255）
        if img.dtype in [np.float32, np.float64]:
            img = (img - np.min(img)) / (np.max(img) - np.min(img) + 1e-8) * 255
            img = img.astype(np.uint8)
        # 2. 处理多通道（转为灰度）
        if len(img.shape) == 3:
            if img.shape[-1] == 3:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            elif img.shape[-1] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
            else:
                img = img.sum(axis=-1).astype(np.uint8)  # 其他通道数求和
        # 3. 确保是单通道
        if len(img.shape) > 2:
            img = img.squeeze()
        return img


def STBOC_with_size_filter(g,
                           bin_fac=4,
                           bilat_size=3,
                           bilat_height=40,
                           threshold=20,
                           min_size=2,
                           max_size=6,
                           morph_kernel_size=3,
                           show_particles=False,
                           return_original_with_particles=False,
                           return_centers=False,
                           return_centers_and_radii=False):
    g = np.copy(g)
    # 确保输入是8位单通道
    if g.dtype != np.uint8 or len(g.shape) != 2:
        raise ValueError(f"输入必须是8位单通道灰度图，当前：dtype={g.dtype}, shape={g.shape}")

    strided = StrBiThresOpen(g, bin_fac, threshold, bilat_size, bilat_height, morph_kernel_size)

    # 适配OpenCV版本的轮廓检测
    if cv2.__version__.startswith('4'):
        contours, hierarchy = cv2.findContours(strided, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        _, contours, hierarchy = cv2.findContours(strided, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    centers = []
    radii = []
    for cnt in contours:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        if radius > max_size or radius < min_size:
            radius_expand = int(radius) + 2
            y1 = max(0, center[1] - radius_expand)
            y2 = min(strided.shape[0], center[1] + radius_expand)
            x1 = max(0, center[0] - radius_expand)
            x2 = min(strided.shape[1], center[0] + radius_expand)
            strided[y1:y2, x1:x2] = 0
        else:
            M = cv2.moments(cnt, binaryImage=True)
            if M['m00'] == 0:
                continue
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            centers.append((cx, cy))
            radii.append(radius)

    if return_centers:
        return np.array(centers)[:, ::-1] if centers else np.array([])

    if return_centers_and_radii:
        return (np.array(centers)[:, ::-1], np.array(radii)) if centers else (np.array([]), np.array([]))

    if return_original_with_particles:
        g_rgb = cv2.cvtColor(g, cv2.COLOR_GRAY2RGB)
        for cnt, radius in zip(centers, radii):
            cv2.circle(g_rgb, cnt, int(radius * 2), (255, 0, 0), 2)
        return g_rgb

    if show_particles:
        strided_rgb = cv2.cvtColor(strided, cv2.COLOR_GRAY2RGB)
        for cnt, radius in zip(centers, radii):
            cv2.circle(strided_rgb, cnt, int(radius * 2), (255, 0, 0), 2)
        strided = strided_rgb

    strided[strided != 0] = 255
    return strided.astype(np.uint8)  # 确保返回8位数组


def StrBiThresOpen(g, bin_fac=4, threshold=40, bilat_size=3, bilat_height=40, morph_kernel_size=3):
    try:
        # 确保输入是8位单通道
        if g.dtype != np.uint8 or len(g.shape) != 2:
            raise ValueError(f"输入必须是8位单通道灰度图，当前：dtype={g.dtype}, shape={g.shape}")

        strided = strided_rescale(g, bin_fac=bin_fac)
        strided = cv2.bilateralFilter(strided, bilat_size, bilat_size, 50)
        strided = cv2.adaptiveThreshold(
            strided, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            blockSize=101,
            C=-1 * threshold
        )
        strided = cv2.bilateralFilter(strided, bilat_size, bilat_height // 4, 50)
        kernel = np.ones((morph_kernel_size, morph_kernel_size), np.uint8)
        strided = cv2.morphologyEx(strided, cv2.MORPH_OPEN, kernel)
        strided = cv2.morphologyEx(strided, cv2.MORPH_CLOSE, kernel)
        strided[strided != 0] = 255
        return strided.astype(np.uint8)
    except Exception as e:
        print(f"StrBiThresOpen error: {e}")
        return np.zeros_like(g, dtype=np.uint8)  # 兜底返回同尺寸空图


def strided_rescale(g, bin_fac=4):
    try:
        # 核心修复：处理memoryview，确保是numpy数组
        if isinstance(g, memoryview):
            g = np.array(g)
        if not isinstance(g, np.ndarray) or len(g.shape) != 2 or g.dtype != np.uint8:
            raise TypeError(f"输入必须是8位单通道numpy数组，当前：{type(g)}, {g.shape}, {g.dtype}")

        # 步长缩放逻辑
        new_shape = (g.shape[0] // bin_fac, g.shape[1] // bin_fac, bin_fac, bin_fac)
        new_strides = (g.strides[0] * bin_fac, g.strides[1] * bin_fac) + g.strides
        strided = as_strided(g, shape=new_shape, strides=new_strides)
        strided = strided.sum(axis=-1).sum(axis=-1)

        # 归一化到0-255
        strided = (strided - np.min(strided)) / (np.max(strided) - np.min(strided) + 1e-8) * 254
        strided = strided.astype(np.uint8)

        # 升采样恢复尺寸
        strided = strided.repeat(bin_fac, axis=0)
        strided = strided.repeat(bin_fac, axis=1)
        return strided
    except Exception as e:
        print(f"strided_rescale error: {e}")
        return np.zeros_like(g, dtype=np.uint8)


def safe_imshow(img, title="Image"):
    """安全显示图像，处理所有类型/维度异常"""
    # 1. 处理空值/非数组
    if img is None or not isinstance(img, np.ndarray):
        print(f"[{title}] 无效图像，显示空图")
        img = np.zeros((200, 200), dtype=np.uint8)

    # 2. 处理对象数组
    if img.dtype == object:
        try:
            img = img.astype(np.float32)
        except:
            img = np.zeros_like(img, dtype=np.float32)

    # 3. 归一化显示
    img_norm = (img - np.min(img)) / (np.max(img) - np.min(img) + 1e-8)

    # 4. 显示
    fig, ax = plt.subplots()
    cmap = 'gray' if len(img_norm.shape) == 2 else None
    ax.imshow(img_norm, cmap=cmap)
    ax.set_title(title)
    ax.set_aspect("equal")
    plt.show()


# -------------------------- 测试代码 --------------------------
if __name__ == "__main__":
    # 生成测试图像（8位单通道灰度图，模拟真实场景）
    path = r"D:\img.png"
    test_img = cv2.imread(path)
    test_img = np.asarray(test_img)
    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    # 初始化过滤器
    filter_obj = ImageFilter(
        threshold=8,
        bin_fac=2,
        min_size=10,
        max_size=25,
        morph_kernel_size=3
    )
    filter_obj.show_particles = True

    # 执行检测
    result_img = filter_obj.STBOC_with_size_filter(test_img)
    centers, radii = filter_obj.STBOC_with_size_filter(test_img, return_centers_and_radii=True)

    # 输出结果
    print("检测到的粒子中心（x,y）：", centers)
    # 安全显示图像（解决imshow报错）

    for center, radius in zip(centers, radii):
        result_img = cv2.circle(result_img, center, int(radius), color=(255, 0, 0), thickness=2)

    safe_imshow(result_img, title="STBOC Particle Detection")