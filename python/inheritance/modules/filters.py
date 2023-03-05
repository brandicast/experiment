import cv2
from modules.abstract import image_effect


class grey_scale (image_effect):

    def getName(self):
        return "Grey Scale"

    def apply(self, image_array: cv2.Mat) -> cv2.Mat:
        greyscale = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        return greyscale
