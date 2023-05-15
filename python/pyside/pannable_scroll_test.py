import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QImageReader

from pannable_scroll import Pannable
from scroll_label_components import  ImageDisplayWidget

def window():
    app = QApplication(sys.argv)

    win = QMainWindow ()
    scrollarea = Pannable()

    label = ImageDisplayWidget()

    #f = "D:\\CouldStation_Photo\\2009\\小娃\\0829 - 第二次玩大武崙\\DSC03540.JPG"
    f = "/home/brandon/圖片/IMG_8647.jpg"
    reader = QImageReader(f)
    reader.setAutoTransform(True)
    image = reader.read()  # QImage
    label.setImage(image)

    label.mousePressEvent = scrollarea.mouse_press
    label.mouseReleaseEvent = scrollarea.mouse_release
    label.mouseMoveEvent = scrollarea.mouse_move

    scrollarea.setWidget(label)

    win.setCentralWidget(scrollarea)
    win.show()
    sys.exit(app.exec_())
	
if __name__ == '__main__':
   window()