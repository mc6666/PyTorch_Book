#!/usr/bin/env python
# coding: utf-8

# # 范例1. 对图片滑动视窗并作影像金字塔
# ### 原程式来自Sliding Windows for Object Detection with Python and OpenCV (https://www.pyimagesearch.com/2015/03/23/sliding-windows-for-object-detection-with-python-and-opencv/)

# 载入套件
import cv2
import time
import imutils

# 影像金字塔操作
# image：原图，scale：每次缩小倍数，minSize：最小尺寸
def pyramid(image, scale=1.5, minSize=(30, 30)):
    # 第一次传回原图
    yield image

    while True:
        # 计算缩小后的尺寸
        w = int(image.shape[1] / scale)
        # 缩小
        image = imutils.resize(image, width=w)
        # 直到最小尺寸为止
        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
            break
        # 传回缩小后的图像
        yield image

# 滑动视窗        
def sliding_window(image, stepSize, windowSize):    
    for y in range(0, image.shape[0], stepSize):     # 向下滑动 stepSize 格
        for x in range(0, image.shape[1], stepSize): # 向右滑动 stepSize 格
            # 传回裁剪后的视窗
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


# ## 测试
# 读取一个图档
image = cv2.imread('./images_Object_Detection/lena.jpg')

# 视窗尺寸
(winW, winH) = (128, 128)

# 取得影像金字塔各种尺寸
for resized in pyramid(image, scale=1.5):
    # 滑动视窗
    for (x, y, window) in sliding_window(resized, stepSize=32, 
                                         windowSize=(winW, winH)):
        # 视窗尺寸不合即放弃，滑动至边缘时，尺寸过小
        if window.shape[0] != winH or window.shape[1] != winW:
            continue
        # 标示滑动的视窗
        clone = resized.copy()
        cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
        cv2.imshow("Window", clone)
        cv2.waitKey(1)
        # 暂停
        time.sleep(0.025)

# 结束时关闭视窗        
cv2.destroyAllWindows()




