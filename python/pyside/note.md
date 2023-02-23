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

