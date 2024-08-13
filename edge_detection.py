import os
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import re

# ret, thresh = cv.threshold(img, 127, 255, 0)
# contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# cv.namedWindow("contour", 0)
# cv.resizeWindow("contour", 800, 600)
# cv.drawContours(img, contours, -1, (0, 255, 0), 3)
# cv.imshow("contour", img)
# cv.waitKey(0)  # 等待按键命令, 1000ms 后自动关闭


def sobel_filter(img):
    sobelx = cv.Sobel(img, cv.CV_64F, 1, 0, ksize=5)
    sobely = cv.Sobel(img, cv.CV_64F, 0, 1, ksize=5)
    sobelx = cv.convertScaleAbs(sobelx)
    sobely = cv.convertScaleAbs(sobely)
    sobelxy = cv.addWeighted(sobelx, 0.5, sobely, 0.5, 0)
    return sobelxy


def scharr_filter(img):
    scharrx = cv.Scharr(img, cv.CV_64F, 1, 0)
    scharry = cv.Scharr(img, cv.CV_64F, 0, 1)
    scharrx = cv.convertScaleAbs(scharrx)
    scharry = cv.convertScaleAbs(scharry)
    scharrxy = cv.addWeighted(scharrx, 0.5, scharry, 0.5, 0)
    return scharrxy


def laplacian_filter(img):
    laplacian = cv.Laplacian(img, cv.CV_64F)
    laplacian = cv.convertScaleAbs(laplacian)
    return laplacian


if __name__ == '__main__':
    filepath = r'D:\BaiduSyncdisk\Junjie Xie Backup\Processing\image'
    filenames = []
    for key in os.listdir(filepath):
        if 1:
            if 'DF' in key:
                filenames.append(key)
        else:
            print(f"Pass file: {key}")
    for key in filenames:
        file_fullpath = os.path.join(filepath, key)
        img = cv.imread(file_fullpath, flags=1)  # flags=1 读取彩色图像(BGR), flags=0 读取为灰度图像
        # 路径不能有中文！！
        # rows, cols, channels = img.shape
        # roi = img[0:rows, 0:cols, :]

        sobel = sobel_filter(img)
        # cv.namedWindow("sobel", 0)
        # cv.resizeWindow("sobel", 400, 300)
        # cv.imshow("sobel", sobel)
        newname = os.path.join(filepath, f'sobel_{key}')
        cv.imwrite(newname, sobel)
        # plt.hist(sobel.ravel(), 256, [0, 256])
        # plt.show()

        # # 二值化图像，并叠加覆盖至原图
        # ret, mask = cv.threshold(sobel, 125, 255, cv.THRESH_BINARY)
        #
        # cv.namedWindow("mask", 0)
        # cv.resizeWindow("mask", 400, 300)
        # cv.imshow("mask", mask)
        #
        # rows, cols, channels = img_DF.shape
        # roi_DF = img_DF[0:rows, 0:cols, :]
        # mask_invert = cv.bitwise_not(mask)
        # img_bg = np.zeros(np.shape(img))
        # mask_fg = np.zeros(np.shape(img_DF))
        # dst = np.zeros(np.shape(img))
        # for channel in range(3):
        #     img_bg[:, :, channel] = cv.bitwise_and(roi[:, :, channel], roi[:, :, channel], mask=mask_invert[:, :, channel])
        #     if channel == 2:
        #         mask_fg[:, :, channel] = cv.bitwise_and(roi_DF[:, :, channel], roi_DF[:, :, channel], mask=mask[:, :, channel])
        #     else:
        #         mask_fg[:, :, channel] = 0
        #     dst[:, :, channel] = cv.add(img_bg[:, :, channel], mask_fg[:, :, channel])
        # res = img
        # res[0:rows, 0:cols, :] = dst
        # cv.namedWindow(f"{key}", 0)
        # cv.resizeWindow(f"{key}", 400, 300)
        # cv.imshow(f"{key}", res)
# cv.waitKey(0)  # 等有键输入或者1000ms后自动将窗口消除，0表示只用键输入结束窗口
# cv.destroyAllWindows()