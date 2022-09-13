import cv2
import sys

# 读取影像
img_path = './images_Object_Detection/bike2.jpg'
if len(sys.argv) > 1:
    img_path = sys.argv[1]
img = cv2.imread(img_path)

# 执行 Selective Search
cv2.setUseOptimized(True)
cv2.setNumThreads(8)
gs = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
gs.setBaseImage(img)

select_mode = 'f'
if len(sys.argv)  > 2 and sys.argv[2] == 's':
    gs.switchToSingleStrategy()
elif len(sys.argv)  > 2 and sys.argv[2] == 'q':
    gs.switchToSelectiveSearchQuality()
else:
    gs.switchToSelectiveSearchFast()

rects = gs.process()
print('个数:', len(rects))
nb_rects = 10

# 画框
while True:
    wimg = img.copy()

    for i in range(len(rects)):
        if (i < nb_rects):
            x, y, w, h = rects[i]
            cv2.rectangle(wimg, (x, y), (x + w, y + h), 
                        (0, 255, 0), 1, cv2.LINE_AA)

    cv2.imshow("Output", wimg)
    key = cv2.waitKey()

    if (key == 43): # +
        nb_rects += 10

    elif (key == 45 and nb_rects > 10): # -
        nb_rects -= 10

    elif (key == 113): # q
        break

cv2.destroyAllWindows()
