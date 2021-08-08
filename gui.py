import sys
import random
from PyQt6 import QtCore, QtWidgets, QtGui
import time
import macappsearch as appsearch
import json
import os

class KeyHelper(QtCore.QObject):
    pressed = QtCore.pyqtSignal()

    def __init__(self, window, widget):
        super().__init__(window)
        self._window = window

        self.window.installEventFilter(self)

    @property
    def window(self):
        return self._window

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.KeyPress:
            if widget.listwidget.hasFocus():
                if event.key() in (
                    QtCore.Qt.Key.Key_Return,
                    QtCore.Qt.Key.Key_Enter,
                    QtCore.Qt.Key.Key_Right,
                ):
                    self.pressed.emit()
                    print("yes")
                    return True
            elif widget.textbox.hasFocus():
                if event.key() in (
                    QtCore.Qt.Key.Key_Down,
                    QtCore.Qt.Key.Key_Right,
                ):
                    widget.listwidget.setFocus()
                    index = widget.listwidget.model().index(0, 0)
                    if index.isValid():
                        widget.listwidget.setCurrentIndex(index)
        if event.type() == QtCore.QEvent.Type.KeyPress:
            if event.key() == QtCore.Qt.Key.Key_Escape:
                self.window.close()
                return True
        
                
        return super().eventFilter(obj, event)


class launchiiwidget(QtWidgets.QWidget):
    def __init__(self, index):
        self.index = index
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)

        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter) 
        self.textbox.setFixedSize(QtCore.QSize(600, 100))

        self.textbox.setPlaceholderText("Search...")
        self.textbox.returnPressed.connect(self.onPressed)
        
        
        layout.addWidget(self.textbox)

        font = self.textbox.font()
        font.setPointSize(80)
        self.textbox.setFont(font)

        self.listwidget = QtWidgets.QListWidget(self)
        self.listwidget.setItemAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.listwidget)

    def onPressed(self):
        self.listwidget.setFocus()
        index = self.listwidget.model().index(0, 0)
        if index.isValid():
            self.listwidget.setCurrentIndex(index)
    def enterpressed(self):
        item = self.listwidget.currentItem()
        if item is not None:
            print(item.text())
            apppath = appsearch.getPath(self.index, item.text())
            if apppath is not None:
                print(apppath)
                os.system("open " + apppath)
                self.window.close()



class Worker(QtCore.QThread):
    def __init__(self, widget, index):
        QtCore.QThread.__init__(self)
        self.widget = widget
        self.index = index

    def __del__(self):
        self.wait()

    def run(self):
        self.previous = ""
        while True:
            try:
                term = self.widget.textbox.text()
                if term != "" and term != self.previous:
                    self.widget.listwidget.clear()
                    for i in appsearch.searchIndex(self.index, term):
                        item = QtWidgets.QListWidgetItem(i)
                        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        #item.setIcon(QtGui.QIcon(appsearch.getIcon(i)))
                        #print(appsearch.getIcon(i))
                        self.widget.listwidget.addItem(item)
                self.previous = term
            except:
                pass

            time.sleep(0.1)
                

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    with open("index.json", "r") as f: # load index
        index = json.load(f)

    widget = launchiiwidget(index)
    widget.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
    widget.resize(600, 200)
    widget.show()


    thread = Worker(widget, index)
    thread.start()

    key_helper = KeyHelper(widget.windowHandle(), widget)
    key_helper.pressed.connect(widget.enterpressed)
    

    sys.exit(app.exec())