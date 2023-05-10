Note  
====  

<br  /><br  />              
      
# PyQT vs PySide

* 差不多的library，PyQT有license issue, while PySide沒有

* (2023.02) 在anaconda環境下安裝PySide6會有問題。 目前作法是
    ```
    conda install pip
    ```
    之後，再
    ```
    pip install PySide6
    ```
<br  /><br  />

# Qt Designer

## 載入ui檔的方式

1. pyuic
    
    在拉完gui，產生.ui檔之後，執行
    ```
    pyuic  xxxxxx
    ```
    產生相對應的.py檔案。  之後再到程式中引用

2. loadUI

    直接在程式中
    ```
    ui_file = QFile('gui\\main.ui')
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    main_window = loader.load(ui_file)
    ```
    引用載入

    **note** PyQT跟PySide載入的方式有一點不太一樣。  上面範例是PySide

<br/>

## 讓QT Object可以根據主視窗的尺寸動態調整

1. 需要過layout的元件，且sizePolicy設定成expanding
2. **需要在designer的top level空白處，設定佈局(layout)**

<br />

## QSplitter的layout stretch

要設定的是在QSplitter內的QT Object. 在程式內是

```
QSplitter.setLayoutStretch (index, stretch)
```

Stretch works only as value of 0 or 1

<br />

## 讓QSplitter裡面的元件可以維持minimum size，而不會被強迫隱藏 (answer provided by ChatGPT and it works)


```
QSplitter.setCollapsible
```

<br />

## QThread

Reference : https://doc.qt.io/qtforpython/PySide6/QtCore/QThread.html

[To Do]

1. 2 ways of writing QThread 
2. Signal and Slot
3. Multi-threading safe :  mutex and stuff

<br />

## QTTreeWidget

1. expand item on click
```
    def onTreeItemClicked(self, item, col):
        item.setExpanded (True)
```
<br />

## QTTabWidget

1. To change the focus tab ->  setCurrentIndex()
2. To close tab 

```
 tabWidget.tabCloseRequested.connect(onTabClosed)

       .
       .
       .

 def onTabClosed (self, index):
    self.tabWidget.removeTab(index)
```

<br />

## QLabel 
1. add picture on QLabel
```
    label = QLabel()
    label.setPixmap(Qpixmap, xxx)
```
2. To align the content 
```
    import Qtcode.Qt
        .
        . 
        . 
    label.setAlignment (Qt.AlignCenter)  

    # more parameters refer to https://doc.qt.io/qtforpython-5/PySide2/QtCore/Qt.html
```
3. Resizing Image inside

    https://stackoverflow.com/questions/8211982/qt-resizing-a-qlabel-containing-a-qpixmap-while-keeping-its-aspect-ratio

<br />

## QMainWindow

- Launch with maximize size 
```
    QMainWindow.showMaximized()
```

## QSCrollArea

1. setMinimumSize 
    When the widget inside is bigger than this size, it "may" display scrollbar.  It may because of below proerty
2. widgetResizable
    This is one key property in order to display the scrollbar when the widget inside is "bigger" than scrollarea's minimum size
3. 

