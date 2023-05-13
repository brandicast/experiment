import sys
from PySide6.QtWidgets import QApplication, QWidget, QTabWidget
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader


def addTab():
    global counter
    counter = counter + 1
    main_window.tabWidget.addTab(QWidget(), "new tab " + str(counter))


def delTab():
    global counter
    counter = counter - 1
    main_window.tabWidget.removeTab(main_window.tabWidget.count() - 1)


def hideTab():
    main_window.tabWidget.setTabBarAutoHide(True)


def visibleTab():
    main_window.tabWidget.setTabVisible(
        1, not main_window.tabWidget.isTabVisible(1))


def changeTabShape():
    if main_window.tabWidget.tabShape() == QTabWidget.Rounded:
        main_window.tabWidget.setTabShape(QTabWidget.Triangular)
    else:
        main_window.tabWidget.setTabShape(QTabWidget.Rounded)


counter = 0
app = QApplication(sys.argv)

ui_file = QFile('gui\\tabwidget.ui')
ui_file.open(QFile.ReadOnly)

loader = QUiLoader()
main_window = loader.load(ui_file)


main_window.pushButton.clicked.connect(addTab)
main_window.pushButton_2.clicked.connect(delTab)
main_window.pushButton_3.clicked.connect(hideTab)
main_window.pushButton_4.clicked.connect(visibleTab)
main_window.pushButton_5.clicked.connect(changeTabShape)


main_window.show()
sys.exit(app.exec())
