import cv2
import numpy as np
import matplotlib.pyplot as plt


def detect_and_mark_circles(image_path, min_radius=10, max_radius=100, dp=1.2, param1=50, param2=30):
    """
    检测图像中的圆形物体并用圆标注

    参数:
    image_path: 输入图像路径
    min_radius: 最小圆半径
    max_radius: 最大圆半径
    dp: 累加器图像的反比分辨率
    param1: Canny边缘检测的高阈值
    param2: 霍夫变换的累加器阈值
    """
    # 读取图像
    original_image = cv2.imread(image_path)
    if original_image is None:
        print(f"无法加载图像: {image_path}")
        return

    # 转换为灰度图
    gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # 高斯模糊，减少噪声
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # 使用霍夫圆变换检测圆形
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=dp,
        minDist=20,  # 检测到的圆的圆心之间的最小距离
        param1=param1,
        param2=param2,
        minRadius=min_radius,
        maxRadius=max_radius
    )

    # 复制原始图像用于绘制
    marked_image = original_image.copy()

    # 如果检测到圆
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

        # 绘制检测到的圆
        for (x, y, r) in circles:
            # 绘制外圆
            cv2.circle(marked_image, (x, y), r, (0, 255, 0), 2)
            # 绘制圆心
            cv2.circle(marked_image, (x, y), 2, (0, 0, 255), 3)

        print(f"检测到 {len(circles)} 个圆形物体")
    else:
        print("未检测到圆形物体")

    # 显示原始图像和标记后的图像
    plt.figure(figsize=(15, 5))

    plt.subplot(121)
    plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    plt.title('原始图像')
    plt.axis('off')

    plt.subplot(122)
    plt.imshow(cv2.cvtColor(marked_image, cv2.COLOR_BGR2RGB))
    plt.title(f'标记后的图像 ({len(circles) if circles is not None else 0} 个圆)')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    return marked_image, circles


def main():
    # 默认图片路径（请替换为你的图片路径）
    # default_image_path = r"D:\ExpData\ps_sphere.jpg"
    # default_image_path = r"D:\ExpData\fft.png"
    default_image_path = r"D:\ExpData\np.png"

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

    # 检测并标记圆形物体
    marked_image, circles = detect_and_mark_circles(
        image_path,
        min_radius=10,  # 调整最小圆半径
        max_radius=20,  # 调整最大圆半径
        dp=1.2,  # 调整累加器分辨率
        param1=50,  # 调整Canny边缘阈值
        param2=10  # 调整霍夫变换阈值
    )

    # 如果检测到圆，可以进一步处理
    if circles is not None:
        # 计算并显示检测到的圆的统计信息
        radii = [r for (x, y, r) in circles]
        avg_radius = np.mean(radii)
        print(f"平均圆半径: {avg_radius:.2f} 像素")
        print(f"最小圆半径: {np.min(radii)} 像素")
        print(f"最大圆半径: {np.max(radii)} 像素")


if __name__ == "__main__":
    import os

    main()