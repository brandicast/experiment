import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QGraphicsView, QGraphicsScene, QSizePolicy


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # create a QHBoxLayout to contain the widgets
        hbox = QHBoxLayout(self)

        # create the QTreeWidget and add some items to it
        tree = QTreeWidget(self)
        tree.setColumnCount(1)
        parent = QTreeWidgetItem(tree)
        parent.setText(0, "Parent")
        child1 = QTreeWidgetItem(parent)
        child1.setText(0, "Child 1")
        child2 = QTreeWidgetItem(parent)
        child2.setText(0, "Child 2")
        tree.expandAll()

        # create the QGraphicsView and add a QGraphicsScene to it
        view = QGraphicsView(self)
        scene = QGraphicsScene(self)
        view.setScene(scene)
        scene.addRect(0, 0, 50, 50)

        # add the widgets to the QHBoxLayout
        hbox.addWidget(tree)
        hbox.addWidget(view)

        # set the main layout of the window
        self.setLayout(hbox)

        # set the minimum width of the QTreeWidget
        tree.setMinimumWidth(100)

        # set the size policy of the QGraphicsView to expand horizontally
        view.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)

        # connect the resize signal of the QTreeWidget to a slot that adjusts the size of the QGraphicsView
        tree.resized.connect(lambda: view.setMaximumWidth(
            view.width() + tree.width() - tree.minimumWidth()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
