import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, Qt
from PySide6.QtUiTools import QUiLoader


from zoomable_image_label import *    


app = QApplication(sys.argv)

#ui_file = QFile('gui\\scrollarea.ui')
ui_file = QFile('gui/scrollarea.ui')
ui_file.open(QFile.ReadOnly)

loader = QUiLoader()
main_window = loader.load(ui_file)

#label = ImageDisplayWidget()
label = Zoomable_Mat_Label()

f = "D:\\CouldStation_Photo\\2009\\小娃\\0829 - 第二次玩大武崙\\DSC03540.JPG"
g = "D:\\CouldStation_Photo\\2023\\兩姊妹\\0109 - 幫老師慶生\\2023-01-09 21.19.22.jpg"

#f = "/home/brandon/圖片/IMG_8647.jpg"


label.setImagePath (g)

scroll = main_window.scrollArea
#label.resize(scroll.size())
scroll.setWidget (label)



main_window.show()
sys.exit(app.exec())