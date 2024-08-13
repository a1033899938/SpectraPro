from __future__ import print_function
import os
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import re
import cv2 as cv


filepath = r'D:\BaiduSyncdisk\Junjie Xie Backup\motion detection'
filenames = []
for key in os.listdir(filepath):
    if '.png' in key:
        filename_now = key
        filenames.append(filename_now)
        print(filename_now)
    else:
        print(f"Pass file: {key}")


"""读取所有帧"""
frames = []
for key in filenames:
    filename_full_now = os.path.join(filepath, key)
    frame_now = cv.imread(filename_full_now, flags=1)
    frames.append(frame_now)


'''
该代码尝试使用背景差分法，完成了固定摄像头中，动态物体的提取。
'''
# 有两种算法可选，KNN和MOG2，下面的代码使用KNN作为尝试
algo = 'KNN'
if algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()


frame1 = frames[0]
frame2 = frames[1]
gray1 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
gray2 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
print(np.shape(gray2))
"""原始图"""
cv.namedWindow('Origin1', 0)
cv.resizeWindow('Origin1', 400, 300)
cv.imshow('Origin1', frame1)
cv.namedWindow('Origin2', 0)
cv.resizeWindow('Origin2', 400, 300)
cv.imshow('Origin2', frame2)
"""灰度图"""
cv.namedWindow('Gray1', 0)
cv.resizeWindow('Gray1', 400, 300)
cv.imshow('Gray1', gray1)
cv.namedWindow('Gray2', 0)
cv.resizeWindow('Gray2', 400, 300)
cv.imshow('Gray2', gray2)

# 定义矩形卷积核
rectangle_kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))

# 计算两帧的差异
diff = cv.absdiff(gray1, gray2)

# 二值化以突出差异
_, thresh_nonDilate = cv.threshold(diff, 30, 255, cv.THRESH_BINARY)
thresh = cv.dilate(thresh_nonDilate, rectangle_kernel, iterations=2)  # 膨胀操作，使轮廓更清晰
"""差分图"""
cv.namedWindow('Diff', 0)
cv.resizeWindow('Diff', 400, 300)
cv.imshow('Diff', diff)
cv.namedWindow('thresh_nonDilate', 0)
cv.resizeWindow('thresh_nonDilate', 400, 300)
cv.imshow('thresh_nonDilate', thresh_nonDilate)
cv.namedWindow('thresh', 0)
cv.resizeWindow('thresh', 400, 300)
cv.imshow('thresh', thresh)

# 找出轮廓
contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
print(contours)
# 识别面积最大的轮廓
if contours:
    largest_contour = max(contours, key=cv.contourArea)
    x, y, w, h = cv.boundingRect(largest_contour)
    cv.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 用绿色矩形框出

    # 将 B、G、R 单通道合并为 3 通道 BGR 彩色图像
    thresh_img = cv.merge([thresh, thresh, thresh])
    cv.namedWindow('Difference', 0)
    cv.resizeWindow('Difference', 400, 300)
    cv.imshow('Difference', frame2)
#     # 准备下一次迭代
#     gray1 = gray2
#
#     # # 按'q'退出
#     # if cv.waitKey(1) & 0xFF == ord('q'):
#     #     break
#
cv.waitKey(0)  # 等有键输入或者1000ms后自动将窗口消除，0表示只用键输入结束窗口
cv.destroyAllWindows()

# plt.show()


"""new part"""
# 导入OpenCV，初始化MOG背景差分器，定义erode（腐蚀）、dilate（膨胀）运算的核大小
# 初始化函数中接收一个参数detectShadows，将其设置为True，就会标记出阴影区域，而不会标记为前景的一部分。
# 使用腐蚀与膨胀的形态学操作是为了抑制一些细微的振动频率。
bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
erode_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

# 捕捉摄像头帧，并使用MOG差分器获得背景掩膜
# 当我们把每一帧传递给背景差分器的 apply 方法时，差分器就会更新它的内部背景模型，然后返回一个掩膜。
# 其中，前景部分的掩膜是白色（255），阴影部分的掩膜是灰色（127），背景部分的掩膜是黑色（0）
cap = cv2.VideoCapture(0)
success, frame = cap.read()
while success:
    fg_mask = bg_subtractor.apply(frame)

    # 然后对掩膜应用阈值来获得纯黑白图像，并通过形态学运算对阈值化图像进行平滑处
    # （本示例中，我们开启了阴影检测，但我们仍然想把阴影认为是背景，所以对掩膜应用一个接近白色（244）的阈值）
    _, thresh = cv2.threshold(fg_mask, 244, 255, cv2.THRESH_BINARY)
    cv2.erode(thresh, erode_kernel, thresh, iterations=2)
    cv2.dilate(thresh, dilate_kernel, thresh, iterations=2)

    # 现在，如果我们直接查看阈值化后的图像，会发现运动物体呈现白色斑点，我们想找到白色斑点的轮廓，并在其周围绘制轮廓。其中，我们将应用一个基于轮廓面积的阈值，如果轮廓太小，就认为它不是真正的运动物体（或者不使用此阈值），检测轮廓与绘制边框的代码
    contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                      cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) > 1000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

    # 显示掩膜图像/阈值化图像/检测结果图像，继续读取帧，直到按下ESC退出
    cv2.imshow('mog', fg_mask)
    cv2.imshow('thresh', thresh)
    cv2.imshow('detection', frame)

    k = cv2.waitKey(30)
    if k == 27:  # Escape
        break

    success, frame = cap.read()

"""Full"""
import cv2

OPENCV_MAJOR_VERSION = int(cv2.__version__.split('.')[0])

bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

erode_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

cap = cv2.VideoCapture(0)
success, frame = cap.read()
while success:

    fg_mask = bg_subtractor.apply(frame)

    _, thresh = cv2.threshold(fg_mask, 244, 255, cv2.THRESH_BINARY)
    cv2.erode(thresh, erode_kernel, thresh, iterations=2)
    cv2.dilate(thresh, dilate_kernel, thresh, iterations=2)

    if OPENCV_MAJOR_VERSION >= 4:
        # OpenCV 4 or a later version is being used.
        contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)
    else:
        # OpenCV 3 or an earlier version is being used.
        # cv2.findContours has an extra return value.
        # The extra return value is the thresholded image, which is
        # unchanged, so we can ignore it.
        _, contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                             cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) > 1000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

    cv2.imshow('mog', fg_mask)
    cv2.imshow('thresh', thresh)
    cv2.imshow('detection', frame)

    k = cv2.waitKey(30)
    if k == 27:  # Escape
        break

    success, frame = cap.read()

cap.release()
cv2.destroyAllWindows()