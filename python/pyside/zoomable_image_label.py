import inspect
from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import Qt, QPixmap, QImageReader, QImage
from PySide6.QtCore import QSize, QObject, Signal, QThread

import cv2
from utils.opencv_util import cv2_loadimage

import sys


import logging
logger = logging.getLogger(__name__)


class Zoomable_Mat_Label(QLabel):

    def __init__(self):
        super().__init__()
        self.image = None

    # [Override] Load Image as OpenCV Mat
    def setImagePath(self, image_path):
        try:
            print("A")
            self.image = cv2_loadimage(image_path, cv2.IMREAD_COLOR)
            print("B")
            self.updateMatToPixmap(self.image)
            print("C")
        except Exception as e:
            print(e)

    # [Override] Load Image as OpenCV Mat

    def setImagePath2(self, image_path):
        try:
            print("A")
            pix = QPixmap()
            pix.load(image_path)
            print("B")
            self.setPixmap(pix)
            print("C")
        except Exception as e:
            print(e)

    # [Override]

    def getImageSize(self) -> QSize:
        return QSize(self.image.shape[1], self.image.shape[0])

    # This is when Mat is temperary being changed and want to keep the origin mat
    # May change to graphic item instead

    def updateMatToPixmap(self, mat):
        try:
            x = self.__Mat_To_QImage__(mat)

            print("W")
            pixmap = QPixmap.fromImage(x)
            print("F")
            scaled = pixmap.scaled(self.size(), Qt.KeepAspectRatio)
            self.setPixmap(scaled)
            print("G")
        except Exception as e:
            print(e)
        except:
            print("Unexpected error:", sys.exc_info()[0])

    def __Mat_To_QImage__(self, mat):
        try:
            print(f"D :  {mat.shape} ")
            qimage = QImage(mat, mat.shape[1],
                            mat.shape[0], 3 * mat.shape[1], QImage.Format_BGR888)
            print(f"E : {type(qimage)}")
        except:
            print("?????????")
        return qimage
