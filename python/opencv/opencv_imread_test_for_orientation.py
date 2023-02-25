
import cv2
import opencv_util as cv_util

img_path =  "resources/rotated.jpg"
img = cv2.imread(img_path,cv2.IMREAD_COLOR)

cv2.namedWindow("output", cv2.WINDOW_NORMAL)    
cv2.imshow ("output", img)
cv2.waitKey(0)


img = cv_util.cv2_loadimage (img_path, cv2.IMREAD_COLOR)

cv2.imshow ("output", img)
cv2.waitKey(0)
