import cv2
import numpy as np
import matplotlib.pyplot as plt


def edge_detection_comparison(image_path):
    """比较不同边缘检测算法的效果"""
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法加载图像: {image_path}")
        return

    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 高斯模糊，减少噪声
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 1. Sobel算子
    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    sobel_edges = np.sqrt(sobelx ** 2 + sobely ** 2)
    sobel_edges = cv2.normalize(sobel_edges, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # 2. Canny边缘检测
    canny_edges = cv2.Canny(blurred, 50, 150)

    # 3. Prewitt算子
    kernelx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    kernely = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
    prewittx = cv2.filter2D(blurred, -1, kernelx)
    prewitty = cv2.filter2D(blurred, -1, kernely)
    prewitt_edges = cv2.addWeighted(prewittx, 0.5, prewitty, 0.5, 0)

    # 4. Laplacian算子
    laplacian_edges = cv2.Laplacian(blurred, cv2.CV_64F)
    laplacian_edges = cv2.convertScaleAbs(laplacian_edges)

    # 5. Scharr算子
    scharrx = cv2.Scharr(blurred, cv2.CV_64F, 1, 0)
    scharry = cv2.Scharr(blurred, cv2.CV_64F, 0, 1)
    scharr_edges = np.sqrt(scharrx ** 2 + scharry ** 2)
    scharr_edges = cv2.normalize(scharr_edges, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # 可视化结果
    plt.figure(figsize=(15, 10))

    plt.subplot(231)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('原始图像')
    plt.axis('off')

    plt.subplot(232)
    plt.imshow(sobel_edges, cmap='gray')
    plt.title('Sobel边缘')
    plt.axis('off')

    plt.subplot(233)
    plt.imshow(canny_edges, cmap='gray')
    plt.title('Canny边缘')
    plt.axis('off')

    plt.subplot(234)
    plt.imshow(prewitt_edges, cmap='gray')
    plt.title('Prewitt边缘')
    plt.axis('off')

    plt.subplot(235)
    plt.imshow(laplacian_edges, cmap='gray')
    plt.title('Laplacian边缘')
    plt.axis('off')

    plt.subplot(236)
    plt.imshow(scharr_edges, cmap='gray')
    plt.title('Scharr边缘')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # 返回各种方法的边缘检测结果
    return {
        'original': image,
        'sobel': sobel_edges,
        'canny': canny_edges,
        'prewitt': prewitt_edges,
        'laplacian': laplacian_edges,
        'scharr': scharr_edges
    }


def edge_enhancement(image_path):
    """使用Canny边缘检测增强图像边缘"""
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法加载图像: {image_path}")
        return

    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Canny边缘检测
    edges = cv2.Canny(blurred, 50, 150)

    # 将边缘转换为彩色图像
    edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # 增强边缘（在原始图像上叠加边缘）
    alpha = 0.5  # 透明度
    enhanced = cv2.addWeighted(image, 1, edges_color, alpha, 0)

    # 显示结果
    plt.figure(figsize=(12, 5))

    plt.subplot(121)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('原始图像')
    plt.axis('off')

    plt.subplot(122)
    plt.imshow(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))
    plt.title('边缘增强图像')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    return enhanced


def main():
    # 默认图片路径（请替换为你的图片路径）
    default_image_path = r"D:\ExpData\ps_sphere.jpg"

    # 如果默认图片不存在，则提示用户输入路径
    if not os.path.exists(default_image_path):
        image_path = input("请输入图片的路径: ").strip()
        if not image_path:
            print("未输入有效路径，程序退出。")
            return
    else:
        image_path = default_image_path

    # 检查文件是否存在
    if not os.path.exists(image_path):
        print(f"错误：文件 '{image_path}' 不存在。")
        return

    print(f"正在处理图片: {image_path}")

    # 比较不同边缘检测算法
    edge_detection_comparison(image_path)

    # 边缘增强示例
    edge_enhancement(image_path)


if __name__ == "__main__":
    import os

    main()