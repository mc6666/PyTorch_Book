import cv2 as cv
import sys

img_path = './images_Object_Detection/bike2.jpg'
if len(sys.argv) > 1:
    img_path = sys.argv[1]
img = cv.imread(img_path)

cv.setUseOptimized(True)
cv.setNumThreads(8)

gs = cv.ximgproc.segmentation.createSelectiveSearchSegmentation()
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

while True:
    wimg = img.copy()

    for i in range(len(rects)):
        if (i < nb_rects):
            x, y, w, h = rects[i]
            cv.rectangle(wimg, (x, y), (x + w, y + h), (0, 255, 0), 1, cv.LINE_AA)

    cv.imshow("Output", wimg)
    c = cv.waitKey()

    if (c == 43): # +
        nb_rects += 10

    elif (c == 45 and nb_rects > 10): # -
        nb_rects -= 10

    elif (c == 113): # q
        break

cv.destroyAllWindows()
