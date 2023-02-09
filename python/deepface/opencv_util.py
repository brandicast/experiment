import cv2
import numpy as np

def cv2_loadimage(filePath):
    img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
    return img 