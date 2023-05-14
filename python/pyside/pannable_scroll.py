
from PySide6.QtWidgets import QScrollArea
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

class Pannable  (QScrollArea):

    def __init__(self):
        self.x = 0
        self.y = 0

def mouse_press (self, event):
    global x, y
    print (event)
    print ("h: " + str (self.horizontalScrollBar().value())  + " (max: " + str (self.horizontalScrollBar().maximum()) + ")" + " v:" + str(self.verticalScrollBar().value()) + " (max: " + str (self.verticalScrollBar().maximum()) + ")")
    x = event.globalPosition().x()
    y = event.globalPosition().y()
    QApplication.setOverrideCursor(Qt.OpenHandCursor)

def mouse_release (self, event):
    print (event)
    QApplication.restoreOverrideCursor()

def mouse_move(self, event):
    #app.changeOverrideCursor(Qt.ClosedHandCursor)
    global x, y
    #print (event)    
    x_diff = x - event.globalPosition().x() #- x 
    y_diff = y - event.globalPosition().y() #- y

    x_max = self.horizontalScrollBar().maximum()
    y_max = self.verticalScrollBar().maximum()

    x_now = self.horizontalScrollBar().value()
    y_now = self.verticalScrollBar().value()

    print ( f"origin: ({x},{y}),  moveto: (({event.globalPosition().x()},{event.globalPosition().y()})),  mouse diff : ({x_diff}, {y_diff}),     scrollbar current value : ({x_now}, {y_now})  ,  scrollbar max value : ({x_max},{y_max})")

    if (x_max > 0):         # if the bar shows
        if (x_diff >0 and x_now < x_max)  or (x_diff<0 and x_now > 0):
            self.horizontalScrollBar().setValue(x_now + x_diff)
            print ("h setValue : " + str(x_now + x_diff))
            x = event.globalPosition().x()

    if (y_max > 0):         # if the bar shows
        if (y_diff >0 and y_now < y_max)  or (y_diff<0 and y_now > 0):
            
            self.verticalScrollBar().setValue(y_now  + y_diff)
            print ("v setValue : " + str(y_now + y_diff))
            y = event.globalPosition().y()
    
        