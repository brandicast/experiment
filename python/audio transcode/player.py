import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.uic import loadUi

from util import play




def start_to_play ():
    global audioFilename
    if audioFilename:
        play (audioFilename)
        
def selectFile ():
    global audioFilename
    input_source_is_mic = False
    #fileName,_ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Audio File(*.m4a)")
    fileName,_ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Audio File(*.*)")
    w.statusbar.showMessage('Input Source is File: ' + fileName)
    audioFilename = fileName


audioFilename = ''

app = QApplication(sys.argv)
w = loadUi('./gui/main.ui')

w.actionOpen.triggered.connect (selectFile)
w.pushButton.clicked.connect(start_to_play)



w.show()

app.exec_()