import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QImageReader


from scroll_label_components import *

app = QApplication(sys.argv)

ui_file = QFile('gui\\scrollarea.ui')
ui_file.open(QFile.ReadOnly)

loader = QUiLoader()
main_window = loader.load(ui_file)

#label = ImageDisplayWidget()
label = ImageDisplayWidget2()

f = "D:\\CouldStation_Photo\\2009\\小娃\\0829 - 第二次玩大武崙\\DSC03540.JPG"
reader = QImageReader(f)
reader.setAutoTransform(True)
image = reader.read()  # QImage
label.setImage(image)

scroll = main_window.scrollArea
scroll.setWidget (label)


print ("scrollarea size :" +  str(scroll.size()) + " and minimum size :" + str(scroll.minimumSize()))

main_window.show()
sys.exit(app.exec())