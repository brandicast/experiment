import cv2
from effects import rotate
from modules.filters import *


img = cv2.imread(
    'C:\\workbench\\experiment\\python\\deepface\\resources_big\\006.jpg')

r = rotate()
img = r.apply(img)

print(r.getName())

cv2.namedWindow("test", cv2.WINDOW_FREERATIO)
cv2.imshow("test", img)
cv2.waitKey(0)

grey = grey_scale()

img = grey.apply(img)

print(grey.getName())

cv2.namedWindow("test", cv2.WINDOW_FREERATIO)
cv2.imshow("test", img)
cv2.waitKey(0)
