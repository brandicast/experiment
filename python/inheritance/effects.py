from modules.abstract import image_effect
import cv2


class rotate(image_effect):

    def getName(self):
        return "Rotate"

    def apply(self, image_array: cv2.Mat) -> cv2.Mat:
        return cv2.rotate(image_array, cv2.ROTATE_90_COUNTERCLOCKWISE)
