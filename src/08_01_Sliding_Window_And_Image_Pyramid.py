#!/usr/bin/env python
# coding: utf-8

# # 範例1. 對圖片滑動視窗並作影像金字塔
# ### 原程式來自Sliding Windows for Object Detection with Python and OpenCV (https://www.pyimagesearch.com/2015/03/23/sliding-windows-for-object-detection-with-python-and-opencv/)

# 載入套件
import cv2
import time
import imutils

# 影像金字塔操作
# image：原圖，scale：每次縮小倍數，minSize：最小尺寸
def pyramid(image, scale=1.5, minSize=(30, 30)):
    # 第一次傳回原圖
    yield image

    while True:
        # 計算縮小後的尺寸
        w = int(image.shape[1] / scale)
        # 縮小
        image = imutils.resize(image, width=w)
        # 直到最小尺寸為止
        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
            break
        # 傳回縮小後的圖像
        yield image

# 滑動視窗        
def sliding_window(image, stepSize, windowSize):    
    for y in range(0, image.shape[0], stepSize):     # 向下滑動 stepSize 格
        for x in range(0, image.shape[1], stepSize): # 向右滑動 stepSize 格
            # 傳回裁剪後的視窗
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


# ## 測試
# 讀取一個圖檔
image = cv2.imread('./images_Object_Detection/lena.jpg')

# 視窗尺寸
(winW, winH) = (128, 128)

# 取得影像金字塔各種尺寸
for resized in pyramid(image, scale=1.5):
    # 滑動視窗
    for (x, y, window) in sliding_window(resized, stepSize=32, 
                                         windowSize=(winW, winH)):
        # 視窗尺寸不合即放棄，滑動至邊緣時，尺寸過小
        if window.shape[0] != winH or window.shape[1] != winW:
            continue
        # 標示滑動的視窗
        clone = resized.copy()
        cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
        cv2.imshow("Window", clone)
        cv2.waitKey(1)
        # 暫停
        time.sleep(0.025)

# 結束時關閉視窗        
cv2.destroyAllWindows()




