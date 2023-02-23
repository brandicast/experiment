from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
import sys


class Example(QTreeWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Dynamic Resize Example')
        self.setGeometry(100, 100, 400, 300)

        self.addTopLevelItem(QTreeWidgetItem(['Item 1']))
        self.addTopLevelItem(QTreeWidgetItem(['Item 2']))
        self.addTopLevelItem(QTreeWidgetItem(['Item 3']))

        self.__mousePressPos = QPoint(0, 0)
        self.__mouseMovePos = QPoint(0, 0)
        self.__isResizing = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()
            self.__isResizing = True

    def mouseMoveEvent(self, event):
        if self.__isResizing:
            diff = QPoint(event.globalPos() - self.__mouseMovePos)
            self.resize(self.width() + diff.x(), self.height() + diff.y())
            self.__mouseMovePos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.__isResizing = False
            QCursor.setPos(self.__mousePressPos)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
