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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # resize first column to the full width
        self.setColumnWidth(0, self.width())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
