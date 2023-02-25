import sys
import os
from PySide6.QtWidgets import QApplication, QTreeWidgetItem, QTreeWidget, QFrame
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader


def collectTreeNodes(path, parent):
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir():
                node = QTreeWidgetItem(parent)
                node.setText(0, entry.name)
                parent.addChild(node)
                collectTreeNodes(entry.path, node)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file = QFile('gui\\main.ui')
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    main_window = loader.load(ui_file)

    root = 'C:\\workbench\\experiment'
    #root = '.'
    root_node = QTreeWidgetItem(main_window.treeWidget)
    root_node.setText(0, root)
    collectTreeNodes(root, root_node)
    main_window.treeWidget.setColumnCount(1)
    main_window.treeWidget.insertTopLevelItem(0, root_node)

    main_window.show()
    sys.exit(app.exec())
