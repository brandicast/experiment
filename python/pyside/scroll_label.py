import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QImageReader


from scroll_label_components import *

x = 0
y = 0

def mouse_press (event):
    global x, y
    print (event)
    print ("h: " + str (scroll.horizontalScrollBar().value())  + " (max: " + str (scroll.horizontalScrollBar().maximum()) + ")" + " v:" + str(scroll.verticalScrollBar().value()) + " (max: " + str (scroll.verticalScrollBar().maximum()) + ")")
    x = event.globalPosition().x()
    y = event.globalPosition().y()
    app.setOverrideCursor(Qt.OpenHandCursor)

def mouse_release (event):
    print (event)
    app.restoreOverrideCursor()

def mouse_move(event):
    #app.changeOverrideCursor(Qt.ClosedHandCursor)
    global x, y
    #print (event)    
    x_diff = x - event.globalPosition().x() #- x 
    y_diff = y - event.globalPosition().y() #- y

    x_max = scroll.horizontalScrollBar().maximum()
    y_max = scroll.verticalScrollBar().maximum()

    x_now = scroll.horizontalScrollBar().value()
    y_now = scroll.verticalScrollBar().value()

    print ( f"origin: ({x},{y}),  moveto: (({event.globalPosition().x()},{event.globalPosition().y()})),  mouse diff : ({x_diff}, {y_diff}),     scrollbar current value : ({x_now}, {y_now})  ,  scrollbar max value : ({x_max},{y_max})")

    if (x_max > 0):         # if the bar shows
        if (x_diff >0 and x_now < x_max)  or (x_diff<0 and x_now > 0):
            scroll.horizontalScrollBar().setValue(x_now + x_diff)
            print ("h setValue : " + str(x_now + x_diff))
            x = event.globalPosition().x()

    if (y_max > 0):         # if the bar shows
        if (y_diff >0 and y_now < y_max)  or (y_diff<0 and y_now > 0):
            
            scroll.verticalScrollBar().setValue(y_now  + y_diff)
            print ("v setValue : " + str(y_now + y_diff))
            y = event.globalPosition().y()

    

    

    


app = QApplication(sys.argv)

#ui_file = QFile('gui\\scrollarea.ui')
ui_file = QFile('gui/scrollarea.ui')
ui_file.open(QFile.ReadOnly)

loader = QUiLoader()
main_window = loader.load(ui_file)

#label = ImageDisplayWidget()
label = ImageDisplayWidget2()

f = "D:\\CouldStation_Photo\\2009\\小娃\\0829 - 第二次玩大武崙\\DSC03540.JPG"
#f = "/home/brandon/圖片/IMG_8647.jpg"

reader = QImageReader(f)
reader.setAutoTransform(True)
image = reader.read()  # QImage
label.setImage(image)

scroll = main_window.scrollArea
scroll.setWidget (label)


print ("scrollarea size :" +  str(scroll.size()) + " and minimum size :" + str(scroll.minimumSize()))


label.mousePressEvent  = mouse_press 
label.mouseReleaseEvent  = mouse_release 
label.mouseMoveEvent  = mouse_move


main_window.show()
sys.exit(app.exec())