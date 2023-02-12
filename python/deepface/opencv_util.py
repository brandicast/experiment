import cv2
import numpy as np

def cv2_loadimage(filePath, mode= cv2.IMREAD_UNCHANGED):
    img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), mode)
    return img 