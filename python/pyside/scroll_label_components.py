from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import QSize
from PySide6.QtGui import Qt
import PySide6
import logging
from typing import Union

from PySide6.QtGui import QPixmap
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QLabel

logger = logging.getLogger(__name__)


class ImageDisplayWidget(QLabel):
    def __init__(self, max_enlargement=2.0):
        super().__init__()
        self.max_enlargement = max_enlargement
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(1, 1)
        self.__image = None

    def setImage(self, image):
        self.__image = image
        pixmap = QPixmap.fromImage(self.__image)
        scaled = pixmap.scaled(self.size(), Qt.KeepAspectRatio)
        self.setPixmap(scaled)

        # self.resize(self.sizeHint())
        # self.update()

    '''
    def sizeHint(self):
        return QSize(1, 1)
        if self.__image:
            return self.__image.size()  # * self.max_enlargement
        else:
            return QSize(1, 1)
    '''

    def resizeEvent(self, event):

        if False:  # self.__image:
            pixmap = QPixmap.fromImage(self.__image)
            print(str(event) + " and self size is :" + str(self.size()))
            scaled = pixmap.scaled(event.size(), Qt.KeepAspectRatio)
            self.setPixmap(scaled)
        super().resizeEvent(event)

    def wheelEvent(self, event):
        newSize = None
        if event.angleDelta().y() > 0:
            print("Zoom In")
            if self.pixmap().size().width() < self.__image.size().width() and self.pixmap().size().height() < self.__image.size().height():
                newSize = QSize(self.pixmap().size().width() + 100,
                                self.pixmap().size().height() + 100)
        else:
            print("Zoom Out")
            if self.pixmap().size().width() > 300 and self.pixmap().size().height() > 300:
                newSize = QSize(self.pixmap().size().width() - 100,
                                self.pixmap().size().height() - 100)
        if newSize != None:
            pixmap = QPixmap.fromImage(self.__image)
            scaled = pixmap.scaled(newSize, Qt.KeepAspectRatio)
            self.setPixmap(scaled)

            # ******************************************
            # Without below, the label will not adjust its size
            # And the viewport will remain the same size as label size
            # The key is also to set ScrollArea's property "widgetResizable" to False
            # ************

            self.resize(newSize)
            print("Label Size is : " + str(self.size()) +
                  "Pixmap Size is :" + str(newSize))

        # return super().wheelEvent(event)


class ImageDisplayWidget2(QLabel):
    def __init__(self, max_enlargement=2.0):
        super().__init__()
        self.max_enlargement = max_enlargement
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(1, 1)
        self.__image = None

    def setImage(self, image):
        self.__image = image
        # self.resize(self.sizeHint())
        # self.update()

    def sizeHint(self):
        if self.__image:
            return self.__image.size()  # * self.max_enlargement
        else:
            return QSize(1, 1)

    def resizeEvent(self, event):

        if self.__image:
            pixmap = QPixmap.fromImage(self.__image)
            print(str(event) + " and self size is :" + str(self.size()))
            scaled = pixmap.scaled(event.size(), Qt.KeepAspectRatio)
            self.setPixmap(scaled)
        super().resizeEvent(event)

    def wheelEvent(self, event):
        newSize = None
        if event.angleDelta().y() > 0:
            print("Zoom In")
            if self.pixmap().size().width() < self.__image.size().width() and self.pixmap().size().height() < self.__image.size().height():
                newSize = QSize(self.pixmap().size().width() + 100,
                                self.pixmap().size().height() + 100)
        else:
            print("Zoom Out")
            if self.pixmap().size().width() > 300 and self.pixmap().size().height() > 300:
                newSize = QSize(self.pixmap().size().width() - 100,
                                self.pixmap().size().height() - 100)
        if newSize != None:
            pixmap = QPixmap.fromImage(self.__image)
            scaled = pixmap.scaled(newSize, Qt.KeepAspectRatio)
            self.setPixmap(scaled)

            # ******************************************
            # Without below, the label will not adjust its size
            # And the viewport will remain the same size as label size
            # The key is also to set ScrollArea's property "widgetResizable" to False
            # ************
            # self.resize(newSize)

            print("Label Size is : " + str(self.size()) +
                  "Pixmap Size is :" + str(newSize))

        # return super().wheelEvent(event)
