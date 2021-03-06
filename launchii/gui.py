from launchii.api import Launchii, Solution
import sys
from PyQt6 import QtCore, QtWidgets
import time


class KeyHelper(QtCore.QObject):
    pressed = QtCore.pyqtSignal()

    def __init__(self, window, widget):
        super().__init__(window)
        self._window = window
        self.widget = widget

        self.window.installEventFilter(self)

    @property
    def window(self):
        return self._window

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.KeyPress:
            if self.widget.listwidget.hasFocus():
                if event.key() in (
                    QtCore.Qt.Key.Key_Return,
                    QtCore.Qt.Key.Key_Enter,
                    QtCore.Qt.Key.Key_Right,
                ):
                    self.pressed.emit()
                    return True
            elif self.widget.textbox.hasFocus():
                if event.key() in (
                    QtCore.Qt.Key.Key_Down,
                    QtCore.Qt.Key.Key_Right,
                ):
                    self.widget.listwidget.setFocus()
                    index = self.widget.listwidget.model().index(0, 0)
                    if index.isValid():
                        self.widget.listwidget.setCurrentIndex(index)
        if event.type() == QtCore.QEvent.Type.KeyPress:
            if event.key() == QtCore.Qt.Key.Key_Escape:
                self.window.close()
                return True

        return super().eventFilter(obj, event)


class launchiiwidget(QtWidgets.QWidget):
    def __init__(self):
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
        item: QListWidgetResult = self.listwidget.currentItem()
        if item is not None:
            item.launchii_solution.execute()
            self.close()


class QListWidgetResult(QtWidgets.QListWidgetItem):
    launchii_solution: Solution


class Worker(QtCore.QThread):
    def __init__(self, widget, launchii: Launchii):
        QtCore.QThread.__init__(self)
        self.widget = widget
        self.launchii = launchii

    def __del__(self):
        self.wait()

    def run(self):
        self.previous = ""
        while True:
            try:
                term = self.widget.textbox.text()
                if term != "" and term != self.previous:
                    self.widget.listwidget.clear()
                    results = self.launchii.search(term)
                    for result in results:
                        item = QListWidgetResult(result.describe())
                        item.launchii_solution = result
                        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        # item.setIcon(QtGui.QIcon(self.launchii.getIcon(i)))
                        # print(self.launchii.getIcon(i))
                        self.widget.listwidget.addItem(item)
                self.previous = term
            except:
                pass
            time.sleep(0.1)


class Gui:
    def __init__(self, launchii: Launchii) -> None:
        self.launchii = launchii

    def start(self):
        app = QtWidgets.QApplication([])

        widget = launchiiwidget()
        widget.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        widget.resize(600, 200)
        widget.show()

        thread = Worker(widget, self.launchii)
        thread.start()

        key_helper = KeyHelper(widget.windowHandle(), widget)
        key_helper.pressed.connect(widget.enterpressed)

        sys.exit(app.exec())
